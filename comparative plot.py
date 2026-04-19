import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Define two stocks
tickers = ["HDFCBANK.NS", "NESTLEIND.NS"]

# Store processed data
stock_data = {}

#Computing metrics for both plots
for ticker in tickers:
    data = yf.download(ticker, period="6mo", interval="1d")

    data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1)) #Daily Log Return
    data["Turnover"] = data["Close"] * data["Volume"] #Daily Turnover Data

    avg_turnover = data["Turnover"].mean()
    data["Turnover Ratio"] = data["Turnover"] / avg_turnover #Daily Turnover Ratio

    data["Amihud"] = abs(data["Log Return"]) / data["Turnover"] #Daily Amihud Illiquidity

    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    stock_data[ticker] = data #Storing Data frame as dictionary

#Comparison plots for both the data
plt.figure(figsize=(14, 12))

#1. Log Returns
plt.subplot(3, 1, 1)
for ticker in tickers:
    plt.plot(stock_data[ticker].index, stock_data[ticker]["Log Return"], label=ticker)

plt.title("Log Returns Comparison")
plt.legend()
plt.grid(True)

#2. Amihud Illiquidity
plt.subplot(3, 1, 2)
for ticker in tickers:
    plt.plot(stock_data[ticker].index, stock_data[ticker]["Amihud"], label=ticker)

plt.title("Amihud Illiquidity Comparison")
plt.legend()
plt.grid(True)

#3. Turnover Ratio
plt.subplot(3, 1, 3)
for ticker in tickers:
    plt.plot(stock_data[ticker].index, stock_data[ticker]["Turnover Ratio"], label=ticker)

plt.title("Turnover Ratio Comparison")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()