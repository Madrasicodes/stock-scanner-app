import pandas as pd
import ta
import yfinance as yf

NSE_STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

def get_data(symbol):
    return yf.download(symbol, period="3mo", interval="1d")

def analyze_stock(df, trade_type):
    df['ema20'] = ta.trend.ema_indicator(df['Close'], window=20)
    df['ema50'] = ta.trend.ema_indicator(df['Close'], window=50)

    latest = df.iloc[-1]

    if trade_type == "Swing" and latest['ema20'] > latest['ema50']:
        return "BUY", 0.7, latest['Close']

    return None, 0, latest['Close']

def scan_market(trade_type):
    results = []

    for stock in NSE_STOCKS:
        df = get_data(stock)
        signal, confidence, price = analyze_stock(df, trade_type)

        if signal:
            results.append({
                "stock": stock,
                "signal": signal,
                "price": price,
                "confidence": confidence
            })

    return results
