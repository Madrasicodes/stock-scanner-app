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

    ema20 = float(latest['ema20'])
    ema50 = float(latest['ema50'])
    price = float(latest['Close'])

    signal = None
    confidence = 0

    if trade_type == "Swing":
        if ema20 > ema50:
            signal = "BUY"
            confidence = 0.7

    if trade_type == "Intraday":
        if price > df['High'].rolling(10).max().iloc[-2]:
            signal = "BREAKOUT BUY"
            confidence = 0.8

    return signal, confidence, price
