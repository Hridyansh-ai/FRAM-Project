import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

ticker = "HDFCBANK.NS"

#Downloading the Data
data = yf.download(ticker, period="6mo", interval="1d")

#Computing the Metrics
data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))#Daily Log Returns

data["Turnover"] = data["Close"] * data["Volume"]#Daily Turnover

avg_turnover = data["Turnover"].mean()
data["Turnover Ratio"] = data["Turnover"] / avg_turnover #Daily Turnover Ratio

data["Amihud"] = abs(data["Log Return"]) / data["Turnover"] #Daily Amihud Illiquidity

# Volatility
data["Rolling Volatility"] = data["Log Return"].rolling(20).std() * (252**0.5)

#Cleaning the data
data = data.replace([np.inf, -np.inf], np.nan).dropna()

#Exporting the data to Excel
data.to_excel(f"{ticker}_final_analysis.xlsx")

#Plots for Data Analysis
plt.figure(figsize=(12, 12))

# Log Returns
plt.subplot(4, 1, 1)
plt.plot(data.index, data["Log Return"])
plt.title(f"{ticker} - Log Returns")
plt.grid(True)

# Turnover
plt.subplot(4, 1, 2)
plt.plot(data.index, data["Turnover"])
plt.title(f"{ticker} - Turnover")
plt.grid(True)

# Amihud
plt.subplot(4, 1, 3)
plt.plot(data.index, data["Amihud"])
plt.title(f"{ticker} - Amihud Illiquidity")
plt.grid(True)

# Volatility
plt.subplot(4, 1, 4)
plt.plot(data.index, data["Rolling Volatility"])
plt.title(f"{ticker} - Rolling Volatility (Annualized)")
plt.grid(True)

plt.tight_layout()
plt.show()

#Creates the metric table for data representation
metrics_df = data[[
    "Log Return",
    "Rolling Volatility",
    "Amihud",
    "Turnover Ratio"
]]

log_returns = metrics_df["Log Return"]

#Summarising the data table
summary = {
    "Mean Return": log_returns.mean(),
    "Std Dev": log_returns.std(),
    "Min Return": log_returns.min(),
    "Max Return": log_returns.max(),
    "Skewness": skew(log_returns),
    "Kurtosis": kurtosis(log_returns),

    "Avg Volatility": metrics_df["Rolling Volatility"].mean(),
    "Avg Amihud": metrics_df["Amihud"].mean(),
    "Avg Turnover Ratio": metrics_df["Turnover Ratio"].mean()
}

summary_df = pd.DataFrame(summary, index=[ticker])

#Exporting the Data to Excel for proper analysis
with pd.ExcelWriter(f"{ticker}_final_report.xlsx") as writer:
    metrics_df.to_excel(writer, sheet_name="Daily Metrics")
    summary_df.to_excel(writer, sheet_name="Summary Stats")

print("Analysis Complete")
