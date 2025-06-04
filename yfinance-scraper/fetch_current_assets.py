import yfinance as yf
import pandas as pd

# Read the stock symbols from file
try:
    with open('symbols.txt', 'r') as file:
        stock_symbols = []
        for line in file:
            clean_line = line.strip()
            if clean_line:
                stock_symbols.append(clean_line)
                
    if not stock_symbols:
        raise ValueError("The symbols.txt file is empty")
        
except FileNotFoundError:
    raise FileNotFoundError("Could not find symbols.txt in current folder")

def get_current_assets():
    final_results = []
    
    for symbol in stock_symbols:
        try:
            # Get company data
            company = yf.Ticker(symbol)
            
            # Get the balance sheet
            balance_sheet = company.quarterly_balance_sheet
            
            # Check if we got data
            if balance_sheet.empty:
                raise ValueError("No balance sheet data available")
            
            # Variables to store our findings
            current_assets_value = None
            found_date = None
            
            # Look through each quarter (newest to oldest)
            for i in range(len(balance_sheet.columns)):
                quarter = balance_sheet.columns[i]
                
                # Check if "Current Assets" exists in this quarter
                if "Current Assets" in balance_sheet.index:
                    value = balance_sheet.loc["Current Assets", quarter]
                    
                    # If we found a valid number, save it
                    if pd.notna(value):
                        current_assets_value = int(value)
                        found_date = quarter.strftime('%Y-%m-%d')
                        break
            
            # If we found current assets, add to results
            if current_assets_value is not None:
                final_results.append({
                    'Symbol': symbol,
                    'Current Assets': current_assets_value,
                    'Date': found_date
                })
            else:
                # If no current assets found in any quarter
                print(f"\nCould not find Current Assets for {symbol}")
                print("Available data items:", list(balance_sheet.index))
                
                # Add as N/A but still record the symbol
                first_quarter = balance_sheet.columns[0]
                final_results.append({
                    'Symbol': symbol,
                    'Current Assets': 'N/A',
                    'Date': first_quarter.strftime('%Y-%m-%d')
                })
                
        except Exception as error:
            print(f"Error processing {symbol}: {error}")
            final_results.append({
                'Symbol': symbol,
                'Current Assets': 'N/A',
                'Date': 'N/A'
            })
    
    # Save results to CSV
    results_df = pd.DataFrame(final_results)
    results_df.to_csv('current_assets_quarterly.csv', index=False)
    print("\nDone! Results saved to current_assets_quarterly.csv")

# Run the function
get_current_assets()