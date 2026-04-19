import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

tickers = ["HDFCBANK.NS", "NESTLEIND.NS"]

for ticker in tickers:
    data = yf.download(ticker, period="6mo", interval="1d")
    data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))
    data["Turnover"] = data["Close"] * data["Volume"]
    data["Amihud"] = abs(data["Log Return"]) / data["Turnover"]
    data = data.dropna()

    plt.plot(data.index, data["Amihud"], label=ticker)

plt.title("Amihud Illiquidity Comparison")
plt.legend()
plt.show()