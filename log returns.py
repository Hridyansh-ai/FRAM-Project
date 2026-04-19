import pandas as pd
import numpy as np
import yfinance as yf

# Step 1: Load tickers
file_path = "ind_nifty50list.xlsx"
df = pd.read_excel(file_path)

tickers = [symbol + ".NS" for symbol in df["Symbol"].tolist()]

# Step 2: Download all data at once (FASTER than loop)
data = yf.download(
    tickers,
    period="6mo",
    interval="1d"
)

# Step 3: Extract only Close prices
close_prices = data["Close"]

# Step 4: Calculate log returns
log_returns = np.log(close_prices / close_prices.shift(1))

# Step 5: Drop first row (NaN)
log_returns = log_returns.dropna()

# Step 6: View result
print(log_returns.head())