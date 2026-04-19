import pandas as pd
import numpy as np
import yfinance as yf
from scipy.stats import norm
import os

# -----------------------------
# STEP 1: Download data
# -----------------------------
ticker = "HDFCBANK.NS"

if os.path.exists("hdfcbank_data.csv"):
    data = pd.read_csv("hdfcbank_data.csv", index_col=0, parse_dates=True)
    data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
    data = data.dropna()
else:
    data = yf.download("HDFCBANK.NS", period="6mo", interval="1d")
    data.to_csv("hdfcbank_data.csv")

# -----------------------------
# STEP 2: Volatility
# -----------------------------
data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))
data = data.dropna()

voldaily = data["Log Return"].std()
vol = voldaily * np.sqrt(252)

print("Daily Volatility:", voldaily)
print("Annualized Historical Volatility:", vol)

# -----------------------------
# STEP 3: BSM function
# -----------------------------
def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# -----------------------------
# STEP 4: Parameters
# -----------------------------
S = data["Close"].iloc[-1]
r = 0.06

# GIVEN MARKET DATA
option_data = [
    # Expiry, Days, Option Type, Strike, Market Price
    ("28-Apr", 17, "OTM Put", 750, 4.35),
    ("28-Apr", 17, "ATM Call", 810, 20.30),
    ("28-Apr", 17, "ATM Put", 810, 18.95),
    ("28-Apr", 17, "OTM Call", 870, 3.50),

    ("26-May", 45, "OTM Put", 750, 9.50),
    ("26-May", 45, "ATM Call", 810, 31.05),
    ("26-May", 45, "ATM Put", 810, 21.70),
    ("26-May", 45, "OTM Call", 870, 11.15),
]

df = pd.DataFrame(option_data, columns=["Expiry", "Days", "Option", "Strike", "Market Price"])

# -----------------------------
# STEP 5: BSM Pricing
# -----------------------------
bsm_prices = []

for i in range(len(df)):
    K = df.loc[i, "Strike"]
    T = df.loc[i, "Days"] / 365
    opt_type = df.loc[i, "Option"]

    if "Call" in opt_type:
        price = black_scholes(S, K, T, r, vol, "call")
    else:
        price = black_scholes(S, K, T, r, vol, "put")

    bsm_prices.append(price)

df["BSM Price"] = bsm_prices

# -----------------------------
# STEP 6: Mispricing
# -----------------------------
df["Difference"] = df["Market Price"] - df["BSM Price"]

# -----------------------------
# STEP 7: Add useful columns
# -----------------------------
df["Spot Price (S)"] = S
df["Volatility (σ)"] = vol
df["Risk-Free Rate (r)"] = r

# -----------------------------
# STEP 8: Output
# -----------------------------
print("\nFinal Option Pricing Comparison:\n")
print(df)

# -----------------------------
# STEP 9: Export to Excel
# -----------------------------
file_name = f"{ticker}_BSM_Comparison.xlsx"

df.to_excel(file_name, index=False)

print(f"\n✅ Excel file saved as: {file_name}")