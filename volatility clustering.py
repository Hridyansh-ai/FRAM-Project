import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

ticker = "NESTLEIND.NS"   # change for second stock

data = yf.download(ticker, period="6mo", interval="1d")

# Log returns
data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))

# Squared returns (key for clustering)
data["Squared Return"] = data["Log Return"] ** 2

# Rolling volatility (20-day)
data["Rolling Volatility(annualized)"] = data["Log Return"].rolling(20).std()*(252**0.5)

data = data.dropna()

# 📊 Plot
plt.figure(figsize=(12, 10))

# Log returns
plt.subplot(3, 1, 1)
plt.plot(data.index, data["Log Return"])
plt.title(f"{ticker} - Log Returns")

# Squared returns
plt.subplot(3, 1, 2)
plt.plot(data.index, data["Squared Return"])
plt.title(f"{ticker} - Squared Returns (Volatility Clustering)")

# Rolling volatility
plt.subplot(3, 1, 3)
plt.plot(data.index, data["Rolling Volatility(annualized)"])
plt.title(f"{ticker} - Rolling Volatility (20D)")

plt.tight_layout()
plt.show()