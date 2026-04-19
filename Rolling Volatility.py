import pandas as pd
import numpy as np
import yfinance as yf

# Step 1: Define stock
tickers = ["NESTLEIND.NS"]

for ticker in tickers:
    print(f"Processing {ticker}...")

    # Step 2: Download data
    data = yf.download(
        ticker,
        period="6mo",
        interval="1d"
    )

    # Step 3: Log Returns
    data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))

    # Step 4: Turnover (₹ traded)
    data["Turnover"] = data["Close"] * data["Volume"]

    # Step 5: Average Turnover
    avg_turnover = data["Turnover"].mean()

    # Step 6: Turnover Ratio (normalized)
    data["Turnover Ratio"] = data["Turnover"] / avg_turnover

    # Step 7: Amihud Illiquidity
    data["Amihud"] = abs(data["Log Return"]) / data["Turnover"]

    # Step 8: Clean data
    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    # Step 9: Output
    print(data[["Close", "Volume", "Log Return", "Turnover", "Turnover Ratio", "Amihud"]].head())

    # Step 10: Save
    data.to_excel(f"{ticker}_full_liquidity_analysis.xlsx")

    # Rolling 20-day volatility
    data["Rolling Volatility (20D)"] = data["Log Return"].rolling(20).std()

    # Annualized volatility
    data["Annualized Volatility"] = data["Rolling Volatility (20D)"] * (252 ** 0.5)

    # Clean
    data = data.dropna()

    print(data[["Log Return", "Rolling Volatility (20D)", "Annualized Volatility"]].head())
    # Save
    data.to_excel("volatility_analysis.xlsx")