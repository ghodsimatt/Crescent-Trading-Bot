import yfinance as yf
import pandas as pd
import ta
import requests
import warnings

warnings.filterwarnings("ignore")

# --- CONFIGURATION ---
TOPIC_NAME = "CrescentTrading"
TOTAL_MONEY = 10000 
ALERT_THRESHOLD = 9      

# --- TICKER LIST ---
raw_tickers = [
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AAP", "AMD", "AES", "AMG", "AFL", "A",
    "APD", "AKAM", "ALK", "ALB", "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL", "GOOG",
    "MO", "AMZN", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "AME", "AMGN", "APH", "APC",
    "ADI", "AON", "APA", "AIV", "AAPL", "AMAT", "APTV", "ADM", "AJG", "AIZ", "T",
    "ADSK", "ADP", "AZO", "AVB", "AVY", "AVGO", "BALL", "BAC", "BAX", "BDX", "BRK-B", "BBY", "BIIB",
    "BLK", "HRB", "BA", "BWA", "BXP", "BSX", "BHF", "BMY", "CA", "COF", "CAH", "CSCO", "CTSH", "CMG", "CHD",
    "CI", "CTAS", "CME", "CMS", "KO", "CPB", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI", "DVA", "DE",
    "DAL", "DVN", "DLR", "DXC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "EMR", "ETR",
    "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HPQ", "HUM", "HBAN", "HII", "IDXX", "SPGI",
    "ITW", "ILMN", "INCY", "IR", "INTC", "ICE", "IBM", "IP", "IPG", "IFF", "INTU", "ISRG", "IVZ", "IQV", "IRM",
    "JBHT", "J", "SJM", "JNJ", "JCI", "JPM", "LHX", "LH", "LRCX", "LEG", "LEN", "LYB", "LIN", "LMT", "L", "LLY",
    "MCO", "MSFT", "MRK", "MET", "MGM", "MHK", "MOH", "MPC", "MLM", "MMC", "MA", "MCD", "MCK", "META",
    "MDT", "MRNA", "MKC", "MU", "GEN", "NKE", "NCLH", "NTRS", "NOC", "NRG", "NUE", "NVR", "NWSA", "OXY",
    "ODFL", "O", "ON", "PKG", "PSKY", "PFG", "PNC", "PGR", "RVTY", "PLD", "PNR", "PPG", "PPL", "PFGC",
    "PM", "PSX", "PNW", "PEP", "PFE", "POOL", "QRVO", "QLYS", "RTX", "REG", "REGN", "RF", "RSG", "EG",
    "ROP", "ROST", "RCL", "CRM", "SCHW", "STZ", "SYK", "SEDG", "SEE", "SRE", "SHW", "SNA",
    "SWK", "SLB", "SBUX", "STT", "SWKS", "SYY", "TDG", "TT", "TER", "TSLA", "TEX", "TFC", "TDY",
    "TFX", "TRV", "TRMB", "TCOM", "UDR", "UAA", "UA", "UNP", "UAL", "UPS", "URI", "UHS", "USB", "VLO", "VTRS",
    "VZ", "VFC", "VTR", "WMT", "WEC", "WFC", "WRB", "WY", "WDC", "WM", "WAT", "WYNN", "CTRA",
    "XEL", "XRX", "XOM", "XYL", "YUM", "ZBRA", "ZTS", "NVDA", "ORCL", "ASML", "PLTR", "COST", "BABA",
    "NFLX", "TM", "CAT", "AZN", "MS", "SAP", "GS", "HSBC", "NVS", "NVO", "RY", "TMO", "APP", "SHOP", "TMUS",
    "SHEL", "MUFG", "BX", "KLAC", "SAN", "QCOM", "UBER", "GEV", "TJX", "BKNG", "TXN", "HDB", "NEE", "RTNTF",
    "BHP", "ANET", "DTEGY", "PDD", "TD", "LOW", "HTHIY", "GILD", "UBS", "SONY", "NOW", "SCCO", "UL", "TTE",
    "BBVA", "RIO", "BUD", "SMFG", "PANW", "WELL", "NEM", "BTI", "CEG", "COP", "KKR", "IBKR", "CB", "PH",
    "CRWD", "ARM", "SNY", "IBN", "CMCSA", "HCA", "SPOT", "GLD", "HOOD", "BN", "MELI", "ATEYY", "MFG", "CVNA",
    "ENB", "GSK", "AEM", "GD", "SNPS", "SO", "BMO", "DASH", "NTES", "DUK", "BNS", "BP", "BCS", "HWM", "CDNS",
    "MAR", "BK", "ABNB", "CM", "FCX", "CRH", "B", "ING", "BAM", "IAU", "MGCLY", "ELV", "APO", "BAESY",
    "ITUB", "LYG", "NU", "DELL", "ORLY", "PBR", "GM", "EQIX", "NGG", "GLW", "SE", "RELX", "MNST", "DB", "WMB",
    "FDX", "MDLZ", "SNOW", "MRVL", "WBD", "INFY", "EPD", "TEL", "SPG", "STX", "CNQ", "COIN", "NWG", "COR", "CL",
    "PWR", "NET", "VRT", "MSI", "NSC", "CP", "IFNNY", "RKT", "RACE", "BMWKY", "PCAR", "LSEGY", "MFC",
    "AMX", "EQNR", "CNI", "KMI", "NXPI", "VALE", "FTNT", "ET", "RBLX", "WPM", "EOG", "SU", "VST", "TRI", "E",
    "NDAQ", "TRP", "MPLX", "F", "ARES", "PYPL", "WDAY", "TAK", "BIDU", "GBTC", "AXON", "EONGY", "D", "ARGX",
    "DEO", "GWW", "PSA", "HEI", "RDDT", "CBRE", "ALNY", "IMO", "FER", "FERG", "FAST", "BKR", "CCJ", "MPWR",
    "CARR", "ROK", "OKE", "CTVA", "BSBR", "RKLB", "FNV", "TTWO", "MSCI", "GFI", "JD", "DDOG", "FANG", "EXC",
    "HLN", "CRWV", "FICO", "ALC", "WAB", "ONC", "TRGP", "GEHC", "CPRT", "FIX", "CCI", "CLS", "KDP", "VEEV",
    "TEVA", "RMD", "EXPE", "NOK", "HIG", "MT", "TEAM", "FISV", "ED", "KEYS", "BBD", "RYAAY", "FLUT", "SATS",
    "FMX", "UI", "OTIS", "INSM", "CIEN", "ZS", "PCG", "SOFI", "SLF", "ASTS", "LYV", "ACGL", "MDLN", "IX", "FIS",
    "MDB", "DG", "CVE", "NTRA", "BE", "RJF", "KMB", "MTB", "CHT", "KVUE", "FOXA", "ESLT", "EQT", "WTW", "KB",
    "VIK", "QSR", "ERIC", "AMRZ", "VOD", "EXR", "WDS", "VRSK", "WIT", "MTD", "EME", "NTR", "COHR", "ULTA",
    "VICI", "ROL", "TME", "STLA", "LPLA", "CRDO", "SYF", "PHG", "DOV", "DLTR", "CBOE", "KHC", "TPR", "HAL",
    "FCNCA", "DXCM", "DTE", "TSCO", "ATO", "NMR", "CHTR", "BRO", "BNTX", "SLV", "EFX", "MKL", "CQP", "PHM",
    "CSGP", "FE", "FTAI", "FTS", "FSLR", "BR", "CFG", "AER", "ES", "FUTU", "LITE", "HUBB", "STE", "JBL", "VLTO",
    "STM", "CNP", "CINF", "LDOS", "LULU", "AFRM", "TPG", "STLD", "PSTG", "ZM", "WSM", "BAP", "OMC", "TECK",
    "EC", "FLEX", "CW", "OWL", "EQR", "CG", "GIS", "PAAS", "RPRX", "CPAY", "CYBR", "RVMD", "SQM", "RIVN",
    "VRSN", "KEY", "TROW", "GFS", "LUV", "TW", "CNC", "CASY", "SW", "RL", "TPL", "BCE", "PBA", "EXPD", "UMC",
    "TLK", "UTHR", "TEF", "RGLD", "NTAP", "TS", "KOF", "GMAB", "FTI", "SSNC", "TU", "RBA", "CHRW", "TOST",
    "GIB", "PTC", "KTOS", "AMCR", "DGX", "NI", "XPEV", "SBAC", "CHKP", "TWLO", "BG", "WWD"
]

def send_phone_alert(message, tags="moneybag"):
    try:
        requests.post(f"https://ntfy.sh/{TOPIC_NAME}", data=message.encode(encoding='utf-8'), headers={"Title": "Crescent Alert 🌙", "Priority": "high", "Tags": tags})
    except: pass

def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y") 
        if df.empty or len(df) < 201: return None

        # --- TECHNICAL INDICATORS ---
        df['SMA_200'] = ta.trend.SMAIndicator(df['Close'], window=200).sma_indicator()
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        macd = ta.trend.MACD(df['Close']); df['MACD'], df['MACD_Signal'] = macd.macd(), macd.macd_signal()
        bb = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2); df['BB_Low'], df['BB_High'] = bb.bollinger_lband(), bb.bollinger_hband()
        df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
        df['ATR'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], window=14).average_true_range()
        df['ADX'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'], window=14).adx()
        df['MFI'] = ta.volume.MFIIndicator(df['High'], df['Low'], df['Close'], df['Volume'], window=14).money_flow_index()
        df['OBV'] = ta.volume.OnBalanceVolumeIndicator(df['Close'], df['Volume']).on_balance_volume()
        df['OBV_SMA'] = df['OBV'].rolling(window=20).mean()
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'], window=14, smooth_window=3); df['Stoch_K'], df['Stoch_D'] = stoch.stoch(), stoch.stoch_signal()
        df['CCI'] = ta.trend.CCIIndicator(df['High'], df['Low'], df['Close'], window=20).cci()

        latest = df.iloc[-1]
        price = latest['Close']
        sma = latest['SMA_200']
        score = 0; reasons = []; signal_type = "NEUTRAL"
        trend = "UP" if price > sma else "DOWN"

        # --- SCORING SYSTEM ---
        if trend == "UP":
            signal_type = "BUY"; score += 1
            if latest['RSI'] < 55: score += 1; reasons.append("RSI")
            if latest['MACD'] > latest['MACD_Signal']: score += 1; reasons.append("MACD")
            if price <= latest['BB_Low'] * 1.05: score += 1; reasons.append("BB")
            if latest['Volume'] > latest['Vol_Avg']: score += 1; reasons.append("Vol")
            if latest['ADX'] > 20: score += 1; reasons.append("ADX")
            if latest['MFI'] < 50: score += 1; reasons.append("MFI")
            if latest['OBV'] > latest['OBV_SMA']: score += 1; reasons.append("OBV")
            if latest['Stoch_K'] < 40 and latest['Stoch_K'] > latest['Stoch_D']: score += 1; reasons.append("Stoch")
            if latest['CCI'] < -100: score += 1; reasons.append("CCI")
            score += 1
        elif trend == "DOWN":
            signal_type = "SHORT"; score += 1
            if latest['RSI'] > 45: score += 1; reasons.append("RSI")
            if latest['MACD'] < latest['MACD_Signal']: score += 1; reasons.append("MACD")
            if price >= latest['BB_High'] * 0.95: score += 1; reasons.append("BB")
            if latest['Volume'] > latest['Vol_Avg']: score += 1; reasons.append("Vol")
            if latest['ADX'] > 20: score += 1; reasons.append("ADX")
            if latest['MFI'] > 50: score += 1; reasons.append("MFI")
            if latest['OBV'] < latest['OBV_SMA']: score += 1; reasons.append("OBV")
            if latest['Stoch_K'] > 60 and latest['Stoch_K'] < latest['Stoch_D']: score += 1; reasons.append("Stoch")
            if latest['CCI'] > 100: score += 1; reasons.append("CCI")
            score += 1

        stop_loss = 0; take_profit = 0; shares = 0
        if signal_type == "BUY": stop_loss = price - (1.5 * latest['ATR']); take_profit = price + (2.0 * latest['ATR'])
        elif signal_type == "SHORT": stop_loss = price + (1.5 * latest['ATR']); take_profit = price - (2.0 * latest['ATR'])
        if stop_loss != 0: shares = int((TOTAL_MONEY * 0.02) / abs(price - stop_loss)) if abs(price - stop_loss) > 0 else 0
        
        vol_pct = (latest['ATR'] / price) * 100
        duration = "1-5 Days" if vol_pct > 2.5 else "1-2 Weeks" if vol_pct > 1.5 else "3-6 Weeks"

        return {"Stock": ticker, "Type": signal_type, "Score": score, "Price": price, "Stop_Loss": stop_loss, "Take_Profit": take_profit, "Shares": shares, "Duration": duration, "Reasons": ", ".join(reasons)}
    except: return None

# --- MAIN EXECUTION ---
print("✅ Starting Scan...")
results = []

for ticker in raw_tickers:
    r = analyze_stock(ticker)
    if r and r['Score'] >= ALERT_THRESHOLD:
        results.append(r)

results.sort(key=lambda x: x['Score'], reverse=True)
alert_count = 0

for r in results:
    msg = f"💎 CRESCENT ALPHA: {r['Type']} {r['Stock']}\nScore: {r['Score']}/11\nDuration: {r['Duration']}\nEntry: ${r['Price']:.2f}\nShares: {r['Shares']}\nStop: ${r['Stop_Loss']:.2f}\nTarget: ${r['Take_Profit']:.2f}"
    send_phone_alert(msg, tags="rocket,moneybag")
    alert_count += 1

print(f"✅ Scan Complete. Sent {alert_count} alerts.")
