import yfinance as yf
import pandas as pd

def get_all_stock_data():
    # Step 1: Read stock symbols from file
    try:
        with open('symbols.txt', 'r') as file:
            stock_symbols = [line.strip() for line in file if line.strip()]
            
        if not stock_symbols:
            print("Error: The symbols.txt file is empty")
            return
            
    except FileNotFoundError:
        print("Error: Could not find symbols.txt in current folder")
        return

    # This will store all our results
    results = []
    
    # Step 2: Get data for each stock symbol
    for symbol in stock_symbols:
        try:
            company = yf.Ticker(symbol)
            
            # Try to get current price and market cap
            try:
                current_price = company.history(period='1d')['Close'].iloc[-1]
                market_cap = company.info.get('marketCap', None)
            except:
                current_price = 'N/A'
                market_cap = 'N/A'
            
            # Get the balance sheet data
            balance_sheet = company.quarterly_balance_sheet
            
            # Skip if no balance sheet data
            if balance_sheet.empty:
                results.append({
                    'Symbol': symbol,
                    'Current Price': 'N/A',
                    'Current Assets (Millions)': 'N/A',
                    'Market Cap': 'N/A',
                    'Most Recent Financial Date': 'N/A',
                    'Current Assets Per Share': 'N/A'
                })
                continue
            
            # Find current assets and the date they were reported
            current_assets_value = None
            found_date = None
            
            # Look through each quarter's data to find current assets
            for i in range(len(balance_sheet.columns)):
                quarter = balance_sheet.columns[i]
                if "Current Assets" in balance_sheet.index:
                    value = balance_sheet.loc["Current Assets", quarter]
                    if pd.notna(value):
                        current_assets_value = int(value)
                        found_date = quarter.strftime('%Y-%m-%d')
                        break
            
            # Calculate the values we want to save
            if current_assets_value:
                current_assets_millions = round(current_assets_value / 1000000, 2)
            else:
                current_assets_millions = 'N/A'
            
            # Calculate current assets per share if we have all needed data
            if (current_assets_value and 
                current_price != 'N/A' and 
                market_cap and 
                market_cap != 0):
                current_assets_per_share = round((current_assets_value * current_price) / market_cap, 4)
            else:
                current_assets_per_share = 'N/A'
            
            # Add this stock's data to our results
            results.append({
                'Symbol': symbol,
                'Current Price': round(current_price, 2) if current_price != 'N/A' else 'N/A',
                'Current Assets (Millions)': current_assets_millions,
                'Market Cap': market_cap,
                'Most Recent Financial Date': found_date if found_date else 'N/A',
                'Current Assets Per Share': current_assets_per_share
            })
            
        except Exception as e:
            # If anything goes wrong, just record N/A for everything
            results.append({
                'Symbol': symbol,
                'Current Price': 'N/A',
                'Current Assets (Millions)': 'N/A',
                'Market Cap': 'N/A',
                'Most Recent Financial Date': 'N/A',
                'Current Assets Per Share': 'N/A'
            })
            continue
    
    # Step 3: Save all results to a CSV file
    results_df = pd.DataFrame(results)
    
    # Put the columns in the right order
    columns_order = [
        'Symbol',
        'Current Price',
        'Current Assets (Millions)',
        'Market Cap',
        'Most Recent Financial Date',
        'Current Assets Per Share'
    ]
    
    results_df = results_df[columns_order]
    results_df.to_csv('stock_data_complete.csv', index=False)
    
    print("Done! Data saved to stock_data_complete.csv")

# Run the function
get_all_stock_data()