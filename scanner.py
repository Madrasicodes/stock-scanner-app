import pandas as pd
import yfinance as yf
import ta

# NSE stock universe
NSE_STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "ITC.NS",
    "AXISBANK.NS",
    "WIPRO.NS"
]


def get_data(symbol):
    """
    Download stock data from Yahoo Finance
    """
    df = yf.download(
        symbol,
        period="3mo",
        interval="1d"
    )

    df.dropna(inplace=True)

    return df


def analyze_stock(df, trade_type):
    """
    Analyze stock for swing or intraday setups
    """

    # Technical indicators
    df["ema20"] = ta.trend.ema_indicator(
        close=df["Close"],
        window=20
    )

    df["ema50"] = ta.trend.ema_indicator(
        close=df["Close"],
        window=50
    )

    latest = df.iloc[-1]

    # Convert to single values
    ema20 = float(latest["ema20"])
    ema50 = float(latest["ema50"])
    price = float(latest["Close"])

    signal = None
    confidence = 0

    # Swing logic
    if trade_type == "Swing":
        if ema20 > ema50:
            signal = "BUY"
            confidence = 0.75

    # Intraday breakout logic
    elif trade_type == "Intraday":
        breakout_level = float(
            df["High"].rolling(10).max().iloc[-2]
        )

        if price > breakout_level:
            signal = "BREAKOUT BUY"
            confidence = 0.80

    return signal, confidence, price


def scan_market(trade_type):
    """
    Scan all stocks and return top setups
    """

    results = []

    for stock in NSE_STOCKS:
        try:
            df = get_data(stock)

            if len(df) < 50:
                continue

            signal, confidence, price = analyze_stock(
                df,
                trade_type
            )

            if signal:
                results.append(
                    {
                        "stock": stock,
                        "signal": signal,
                        "price": price,
                        "confidence": confidence
                    }
                )

        except Exception as e:
            print(f"Error scanning {stock}: {e}")
            continue

    # Sort by confidence
    results = sorted(
        results,
        key=lambda x: x["confidence"],
        reverse=True
    )

    return results[:10]
