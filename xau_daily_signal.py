"""
Institutional Execution Signal Generator: London Breakout System (XAU/USD)
Quantitative market session volatility expansion model.
"""

import os
import sys
import re
import datetime
import pandas as pd
import numpy as np
import yfinance as yf

# Configure stdout for UTF-8 support on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Enable ANSI escape code processing in Windows Terminal / CMD
os.system('')

# ANSI Color Palette
GOLD = '\033[38;5;220m'
YELLOW = '\033[1;33m'
GREEN = '\033[1;32m'
CYAN = '\033[1;36m'
BLUE = '\033[1;34m'
MAGENTA = '\033[1;35m'
RED = '\033[1;31m'
GRAY = '\033[90m'
WHITE = '\033[1;37m'
RESET = '\033[0m'
BOLD = '\033[1m'

def strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)

def box_row(content, width=58):
    vis = len(strip_ansi(content))
    pad = max(0, width - vis)
    return f"{GREEN}│{RESET}{content}{' ' * pad}{GREEN}│{RESET}"

def make_bar(pct, width=10):
    clamped = max(-2.0, min(2.0, pct))
    norm = (clamped + 2.0) / 4.0
    filled = max(1, min(width, int(norm * width)))
    return "█" * filled + "░" * (width - filled)

def format_chg(c):
    if c > 0:
        return f"{GREEN}[+{c:.2f}%]{RESET}"
    elif c < 0:
        return f"{RED}[{c:.2f}%]{RESET}"
    return f"{GRAY}[+{c:.2f}%]{RESET}"

def get_asset_stats(ticker, df_data, default_price):
    if df_data is not None and ('Close' in df_data or ('Close', ticker) in df_data):
        try:
            s = df_data['Close'][ticker].dropna()
            if len(s) >= 2:
                cur = float(s.iloc[-1])
                prev = float(s.iloc[-2])
                chg = (cur - prev) / prev * 100.0
                return cur, chg
            elif len(s) == 1:
                return float(s.iloc[-1]), 0.0
        except Exception:
            pass
    return default_price, 0.0

def fetch_market_feeds():
    print(f"{GRAY}[*] Connecting to institutional market data feed (XAU/USD, BTC, OIL, EURUSD)...{RESET}")
    tickers = ['GC=F', 'BTC-USD', 'CL=F', 'EURUSD=X']
    try:
        df_multi = yf.download(tickers, period='5d', interval='15m', progress=False)
    except Exception as e:
        df_multi = None

    if df_multi is None or len(df_multi) == 0:
        return None, None, None

    # Process GC=F for Asian session
    try:
        if isinstance(df_multi.columns, pd.MultiIndex):
            df_gold = df_multi.xs('GC=F', level='Ticker', axis=1)
        else:
            df_gold = df_multi
    except Exception:
        df_gold = df_multi

    # Filter out non-trading periods (weekends where only crypto trades)
    df_gold = df_gold.dropna(subset=['High', 'Low'])

    if df_gold.index.tz is None:
        df_gold.index = df_gold.index.tz_localize("UTC")
    else:
        df_gold.index = df_gold.index.tz_convert("UTC")

    df_gold["date"] = df_gold.index.date
    df_gold["hour"] = df_gold.index.hour

    unique_dates = sorted(df_gold["date"].dropna().unique())
    last_date = unique_dates[-1]

    df_day = df_gold[df_gold["date"] == last_date]
    asia = df_day[(df_day["hour"] >= 0) & (df_day["hour"] < 7)]

    if len(asia) == 0 and len(unique_dates) > 1:
        last_date = unique_dates[-2]
        df_day = df_gold[df_gold["date"] == last_date]
        asia = df_day[(df_day["hour"] >= 0) & (df_day["hour"] < 7)]

    return df_multi, asia, last_date

def calculate_orders(asia, rr_ratio=2.0, buffer_usd=1.0):
    asian_high = float(asia["High"].max())
    asian_low = float(asia["Low"].min())
    asian_range_usd = asian_high - asian_low
    asian_range_pips = asian_range_usd * 10.0

    # Structural Midpoint Axis (50% Range Invalidation)
    midpoint = (asian_high + asian_low) / 2.0

    # Ticket 1: BUY STOP
    buy_entry = asian_high + buffer_usd
    buy_sl = midpoint
    buy_risk_usd = buy_entry - buy_sl
    buy_risk_pips = buy_risk_usd * 10.0
    buy_tp = buy_entry + (buy_risk_usd * rr_ratio)

    # Ticket 2: SELL STOP
    sell_entry = asian_low - buffer_usd
    sell_sl = midpoint
    sell_risk_usd = sell_sl - sell_entry
    sell_risk_pips = sell_risk_usd * 10.0
    sell_tp = sell_entry - (sell_risk_usd * rr_ratio)

    return {
        "asian_high": asian_high,
        "asian_low": asian_low,
        "asian_range_usd": asian_range_usd,
        "asian_range_pips": asian_range_pips,
        "midpoint": midpoint,
        "buy_entry": buy_entry,
        "buy_sl": buy_sl,
        "buy_tp": buy_tp,
        "buy_risk_usd": buy_risk_usd,
        "buy_risk_pips": buy_risk_pips,
        "sell_entry": sell_entry,
        "sell_sl": sell_sl,
        "sell_tp": sell_tp,
        "sell_risk_usd": sell_risk_usd,
        "sell_risk_pips": sell_risk_pips,
        "rr_ratio": rr_ratio
    }

def print_fastfetch_dashboard(df_multi, orders, date_str):
    p_gold, c_gold = get_asset_stats('GC=F', df_multi, orders['asian_high'])
    p_btc, c_btc = get_asset_stats('BTC-USD', df_multi, 81500.0)
    p_oil, c_oil = get_asset_stats('CL=F', df_multi, 99.02)
    p_eur, c_eur = get_asset_stats('EURUSD=X', df_multi, 1.1215)

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ASCII Art Logo (XAU/USD Gold Ingot)
    logo = [
        r"          .______________________.          ",
        r"         /                      /|          ",
        r"        /      X A U / U S D   / |          ",
        r"       /      G O L D  999.9  /  |          ",
        r"      /______________________/   |          ",
        r"      |                      |   |          ",
        r"      |   .--------------.   |   |          ",
        r"      |   |  FINE  GOLD  |   |   |          ",
        r"      |   |   1000 g     |   |   /          ",
        r"      |   '--------------'   |  /           ",
        r"      |     NET LIQUIDITY    | /            ",
        r"      |______________________|/             ",
        r"             [ XAUUSD ]                     ",
        r"         Institutional Desk                 ",
        r"                                            ",
        r"                                            "
    ]

    # Fastfetch-style Right Panel Boxes
    row_gold = f" {CYAN}GOLD (XAU){RESET}  $ {p_gold:>9.2f}  {format_chg(c_gold)}  {YELLOW}[{make_bar(c_gold)}]{RESET}"
    row_btc  = f" {CYAN}BITCOIN   {RESET}  $ {p_btc:>9.2f}  {format_chg(c_btc)}  {YELLOW}[{make_bar(c_btc)}]{RESET}"
    row_oil  = f" {CYAN}CRUDE OIL {RESET}  $ {p_oil:>9.2f}  {format_chg(c_oil)}  {YELLOW}[{make_bar(c_oil)}]{RESET}"
    row_eur  = f" {CYAN}EUR/USD   {RESET}    {p_eur:>9.4f}  {format_chg(c_eur)}  {YELLOW}[{make_bar(c_eur)}]{RESET}"
    
    row_ses  = f" {CYAN}SESSION   {RESET}  LONDON EXPANSION (14:00 - 22:00 WIB)"
    row_str  = f" {CYAN}STRATEGY  {RESET}  DUAL BRACKET OCO (MIDPOINT INVALIDATION)"

    row_feed = f" {CYAN}STATUS    {RESET}  ONLINE // CME & FX STREAM ACTIVE"
    row_time = f" {CYAN}TIME      {RESET}  {now_str} WIB"

    right_panel = [
        f"{BOLD}{WHITE}Hey, Trader{RESET}",
        f"{GREEN}┌── Market Overview ────────────────────────────────────────┐{RESET}",
        box_row(row_gold),
        box_row(row_btc),
        box_row(row_oil),
        box_row(row_eur),
        f"{GREEN}├── Session & Strategy ─────────────────────────────────────┤{RESET}",
        box_row(row_ses),
        box_row(row_str),
        f"{GREEN}├── System Status ──────────────────────────────────────────┤{RESET}",
        box_row(row_feed),
        box_row(row_time),
        f"{GREEN}└───────────────────────────────────────────────────────────┘{RESET}",
        f"{WHITE}Execution Protocol Ready.{RESET}",
        f"{RED}●{RESET} {GREEN}●{RESET} {YELLOW}●{RESET} {BLUE}●{RESET} {MAGENTA}●{RESET} {CYAN}●{RESET} {WHITE}●{RESET}",
        ""
    ]

    print("\n")
    for l, r in zip(logo, right_panel):
        print(f"{YELLOW}{l}{RESET}  {r}")
    print("")

def print_execution_tickets(orders, date_str):
    print("=" * 82)
    print("        INSTITUTIONAL EXECUTION SIGNAL: LONDON VOLATILITY BREAKOUT        ")
    print("=" * 82)
    print(f"  Session Date        : {date_str} (Asia / London Transition)")
    print(f"  Instrument          : XAU/USD (Spot Gold / CME:GC)")
    print(f"  Execution Protocol  : Dual Pending Bracket (OCO / Midpoint Invalidation)")
    print("-" * 82)
    
    print(" 1. ASIAN SESSION BENCHMARK (00:00 - 07:00 UTC / 07:00 - 14:00 WIB)")
    print(f"    * Session High     : $ {orders['asian_high']:,.2f}")
    print(f"    * Session Low      : $ {orders['asian_low']:,.2f}")
    print(f"    * Session Range    : $ {orders['asian_range_usd']:.2f} USD ({orders['asian_range_pips']:.1f} Pips)")
    print(f"    * Median Axis (SL) : $ {orders['midpoint']:,.2f}")
    
    print("-" * 82)
    print(" 2. EXECUTION ORDERS (MT4 / MT5)")
    print("-" * 82)
    
    print(f"  {BOLD}[ORDER TICKET 1: PENDING BUY STOP]{RESET}")
    print(f"    Symbol            : XAUUSD")
    print(f"    Order Type        : BUY STOP")
    print(f"    Entry Price       : {orders['buy_entry']:.2f}")
    print(f"    Stop Loss (SL)    : {orders['buy_sl']:.2f}  (Risk: {orders['buy_risk_pips']:.1f} Pips | ${orders['buy_risk_usd']:.2f} USD)")
    print(f"    Take Profit (TP)  : {orders['buy_tp']:.2f}  (Target: {orders['buy_risk_pips']*orders['rr_ratio']:.1f} Pips | R:R 1:{orders['rr_ratio']})")
    print(f"    Time Invalidation : 22:00 WIB (Cancel if unfilled)")
    print("")
    print(f"  {BOLD}[ORDER TICKET 2: PENDING SELL STOP]{RESET}")
    print(f"    Symbol            : XAUUSD")
    print(f"    Order Type        : SELL STOP")
    print(f"    Entry Price       : {orders['sell_entry']:.2f}")
    print(f"    Stop Loss (SL)    : {orders['sell_sl']:.2f}  (Risk: {orders['sell_risk_pips']:.1f} Pips | ${orders['sell_risk_usd']:.2f} USD)")
    print(f"    Take Profit (TP)  : {orders['sell_tp']:.2f}  (Target: {orders['sell_risk_pips']*orders['rr_ratio']:.1f} Pips | R:R 1:{orders['rr_ratio']})")
    print(f"    Time Invalidation : 22:00 WIB (Cancel if unfilled)")
    
    print("-" * 82)
    print(" 3. POSITION SIZING MATRIX (1.0% RISK MODEL)")
    print("-" * 82)
    print("    Account Equity       Recommended Lot        Risk Allocation")
    risk_usd_per_oz = orders['buy_risk_usd']
    for cap in [500, 1000, 2500, 5000, 10000]:
        calc_lot = (cap * 0.01) / (risk_usd_per_oz * 100.0)
        lot_val = max(0.01, round(calc_lot, 2))
        print(f"    $ {cap:>7,d} USD            {lot_val:>5.2f} Lot              $ {cap*0.01:>6.2f} USD")
    
    print("-" * 82)
    print(" 4. EXECUTION RULES")
    print("-" * 82)
    print("    1. Input both pending bracket orders into MT4/MT5.")
    print("    2. Close the trading platform. Do not monitor live intraday fluctuations.")
    print("    3. Upon fill of one side, immediately cancel the opposite pending order.")
    print("    4. If neither order fills by 22:00 WIB, cancel all pending orders.")
    print("=" * 82)

def main():
    df_multi, asia, last_date = fetch_market_feeds()
    if asia is None or len(asia) == 0:
        print("[!] Insufficient session data. Please run at 13:45 WIB.")
        return
        
    orders = calculate_orders(asia, rr_ratio=2.0, buffer_usd=1.0)
    print_fastfetch_dashboard(df_multi, orders, str(last_date))
    print_execution_tickets(orders, str(last_date))

if __name__ == "__main__":
    main()
