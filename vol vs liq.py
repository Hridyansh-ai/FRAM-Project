import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

ticker = "NESTLEIND.NS"

# Step 1: Download data
data = yf.download(ticker, period="6mo", interval="1d")

# Step 2: Core calculations
data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))

data["Turnover"] = data["Close"] * data["Volume"]

data["Amihud"] = abs(data["Log Return"]) / data["Turnover"]

# Rolling volatility (annualized)
data["Volatility"] = data["Log Return"].rolling(20).std() * (252**0.5)

# Squared returns (for clustering)
data["Squared Return"] = data["Log Return"] ** 2

# Step 3: Clean AFTER all calculations
data = data.replace([np.inf, -np.inf], np.nan).dropna()

#PLOT: Volatility vs Illiquidity
plt.figure(figsize=(8,6))

plt.scatter(data["Amihud"], data["Volatility"])

plt.xlabel("Amihud Illiquidity")
plt.ylabel("Volatility (Annualized)")
plt.title(f"{ticker} - Volatility vs Illiquidity")

plt.grid(True)
plt.show()

#Correlation
correlation = data["Amihud"].corr(data["Volatility"])
print("Correlation between Amihud and Volatility:", correlation)