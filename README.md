# Stock Current Assets Tracker

A Python script that fetches quarterly current assets data for stocks using Yahoo Finance (yfinance).

## Features
- Reads stock symbols from a text file
- Fetches quarterly balance sheet data for each stock
- Extracts current assets values from most recent quarter
- Falls back to previous quarter if current quarter data isn't available
- Outputs results to a clean CSV file

## Requirements
- Python 3.x
- yfinance
- pandas

## Installation

pip install yfinance pandas

Usage
Create a symbols.txt file with one stock symbol per line

Run the script:

bash
python current_assets.py
Results will be saved to current_assets_quarterly.csv

Output Format
CSV file containing:

Stock symbol

Current assets value (in USD)

Report date (YYYY-MM-DD)

Example
Input (symbols.txt):

AAPL
MSFT
GOOG
Output (current_assets_quarterly.csv):

Symbol,Current Assets,Date
AAPL,118674000000,2025-03-31
MSFT,156644000000,2025-03-31
GOOG,162052000000,2025-03-31
Notes
Data is sourced from Yahoo Finance

Some stocks may show 'N/A' if data isn't available


**Alternative simpler description if preferred:**

markdown
# Stock Current Assets

Python script that pulls quarterly current assets data for stocks from Yahoo Finance.

Simply add stock symbols to `symbols.txt`, run the script, and get a CSV with current assets values.

Requirements: Python 3, yfinance, pandas
Choose the repository name that best fits your style - I recommend either StockCurrentAssets or CurrentAssetsTracker as they're both clear and professional. The README can be as detailed or concise as you prefer.
