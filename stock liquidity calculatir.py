import pandas as pd
import yfinance as yf

# Step 1: Load Excel
file_path = "ind_nifty50list.xlsx"
df = pd.read_excel(file_path)

# Step 2: Add .NS to tickers
tickers = [symbol + ".NS" for symbol in df["Symbol"].tolist()]

# Step 3: Create empty list for results
avg_turnover_list = []

# Step 4: Loop through each stock
for ticker in tickers:
    print(f"Processing {ticker}...")

    data = yf.download(
        ticker,
        period="6mo",
        interval="1d"
    )

    if data.empty:
        avg_turnover_list.append(None)
        continue

    # Calculate daily turnover
    data["Turnover"] = data["Close"] * data["Volume"]

    # Calculate average turnover
    avg_turnover = data["Turnover"].mean()

    avg_turnover_list.append(avg_turnover)

# Step 5: Add new column to dataframe
df["Average Turnover"] = avg_turnover_list

# Step 6: Save to new Excel file
output_file = "nifty50_with_turnover.xlsx"
df.to_excel(output_file, index=False)

print("File saved as:", output_file)