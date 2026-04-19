import pandas as pd
import numpy as np
import yfinance as yf

# Step 1: Define stock
tickers = ["RELIANCE.NS"]

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

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Step 1: Load data
ticker = "RELIANCE.NS"

data = yf.download(ticker, period="6mo", interval="1d")

# Step 2: Compute metrics
data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))
data["Turnover"] = data["Close"] * data["Volume"]
data["Amihud"] = abs(data["Log Return"]) / data["Turnover"]

# Clean
data = data.replace([np.inf, -np.inf], np.nan).dropna()

# Step 3: Create plots
plt.figure(figsize=(12, 10))

# 🔹 Plot 1: Log Returns
plt.subplot(3, 1, 1)
plt.plot(data.index, data["Log Return"])
plt.title(f"{ticker} - Daily Log Returns")
plt.xlabel("Date")
plt.ylabel("Log Return")

# 🔹 Plot 2: Turnover
plt.subplot(3, 1, 2)
plt.plot(data.index, data["Turnover"])
plt.title(f"{ticker} - Daily Turnover")
plt.xlabel("Date")
plt.ylabel("Turnover")

# 🔹 Plot 3: Amihud Illiquidity
plt.subplot(3, 1, 3)
plt.plot(data.index, data["Amihud"])
plt.title(f"{ticker} - Amihud Illiquidity")
plt.xlabel("Date")
plt.ylabel("Amihud")

# Layout fix
plt.tight_layout()

# Show graph
plt.show()
