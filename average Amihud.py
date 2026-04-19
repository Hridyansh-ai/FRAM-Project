import pandas as pd
import numpy as np
import yfinance as yf

# Step 1: Load tickers
file_path = "ind_nifty50list.xlsx"
df = pd.read_excel(file_path)

tickers = [symbol + ".NS" for symbol in df["Symbol"].tolist()]

# Step 2: Store results
avg_illiquidity = []

# Step 3: Loop
for ticker in tickers:
    print(f"Processing {ticker}...")

    data = yf.download(ticker, period="6mo", interval="1d")

    if data.empty:
        avg_illiquidity.append(None)
        continue

    # Step 4: Log returns
    data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))

    # Step 5: Turnover
    data["Turnover"] = data["Close"] * data["Volume"]

    # Step 6: Amihud Illiquidity
    data["Amihud"] = abs(data["Log Return"]) / data["Turnover"]

    # Clean NaNs / inf
    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    # Step 7: Average Amihud
    avg_illiquidity.append(data["Amihud"].mean())

# Step 8: Add to Excel
df["Average Amihud Illiquidity"] = avg_illiquidity

# Step 9: Save file
output_file = "nifty50_with_illiquidity.xlsx"
df.to_excel(output_file, index=False)

print("File saved as:", output_file)