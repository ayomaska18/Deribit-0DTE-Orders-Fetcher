import pandas as pd
import os
import gspread
from gspread_formatting import CellFormat, format_cell_range
from datetime import date

date_str = date.today()
output_file = 'Daily_Trades_Summary.xlsx'

def update_google_sheet(df, asset):
    gc = gspread.service_account('service_account.json')
    sh = gc.open("Daily_Trades_Summary_New")

    worksheet = sh.worksheet(asset)
    rows = df.values.tolist()

    for row in rows:
        row = [str(item) if isinstance(item, date) else item for item in row]
        worksheet.append_row(row, value_input_option='USER_ENTERED')
                
    last_row_index = len(worksheet.get_all_values())
    cell_format = CellFormat(horizontalAlignment='RIGHT')
    format_cell_range(worksheet, f'A{last_row_index}:E{last_row_index}', cell_format)

    print(f"{asset} data has been updated to Google Sheet")

# Function to load existing data from a sheet if it exists
def load_existing_data(sheet_name, writer):
    try:
        existing_data = pd.read_excel(writer, sheet_name=sheet_name)
    except ValueError:
        existing_data = pd.DataFrame()  # Sheet does not exist, return empty DataFrame
    return existing_data

# Load new data
buy_calls_ETH = pd.read_csv(f'Orders/ETH_buy_calls_{date_str}.csv')
buy_puts_ETH = pd.read_csv(f'Orders/ETH_buy_puts_{date_str}.csv')
sell_calls_ETH = pd.read_csv(f'Orders/ETH_sell_calls_{date_str}.csv')
sell_puts_ETH = pd.read_csv(f'Orders/ETH_sell_puts_{date_str}.csv')

buy_calls_BTC = pd.read_csv(f'Orders/BTC_buy_calls_{date_str}.csv')
buy_puts_BTC = pd.read_csv(f'Orders/BTC_buy_puts_{date_str}.csv')
sell_calls_BTC = pd.read_csv(f'Orders/BTC_sell_calls_{date_str}.csv')
sell_puts_BTC = pd.read_csv(f'Orders/BTC_sell_puts_{date_str}.csv')

buy_calls_SOL = pd.read_csv(f'Orders/SOL_buy_calls_{date_str}.csv')
buy_puts_SOL = pd.read_csv(f'Orders/SOL_buy_puts_{date_str}.csv')
sell_calls_SOL = pd.read_csv(f'Orders/SOL_sell_calls_{date_str}.csv')
sell_puts_SOL = pd.read_csv(f'Orders/SOL_sell_puts_{date_str}.csv')

# Calculate the counts
eth_data = {
    'Date': [date_str],
    'Buy Calls': [len(buy_calls_ETH)],
    'Buy Puts': [len(buy_puts_ETH)],
    'Sell Calls': [len(sell_calls_ETH)],
    'Sell Puts': [len(sell_puts_ETH)]
}

btc_data = {
    'Date': [date_str],
    'Buy Calls': [len(buy_calls_BTC)],
    'Buy Puts': [len(buy_puts_BTC)],
    'Sell Calls': [len(sell_calls_BTC)],
    'Sell Puts': [len(sell_puts_BTC)]
}

sol_data = {
    'Date': [date_str],
    'Buy Calls': [len(buy_calls_SOL)],
    'Buy Puts': [len(buy_puts_SOL)],
    'Sell Calls': [len(sell_calls_SOL)],
    'Sell Puts': [len(sell_puts_SOL)]
}

# Convert to DataFrame
df_eth = pd.DataFrame(eth_data)
df_btc = pd.DataFrame(btc_data)
df_sol = pd.DataFrame(sol_data)

# Open the existing Excel file or create a new one
if os.path.exists(output_file):
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        # Load existing data from each sheet
        existing_eth = load_existing_data('ETH', writer)
        existing_btc = load_existing_data('BTC', writer)
        existing_sol = load_existing_data('SOL', writer)
        
        # Append the new data as a new row
        updated_eth = pd.concat([existing_eth, df_eth], ignore_index=True)
        updated_btc = pd.concat([existing_btc, df_btc], ignore_index=True)
        updated_sol = pd.concat([existing_sol, df_sol], ignore_index=True)
        
        # Write the updated data back to the Excel file
        updated_eth.to_excel(writer, sheet_name='ETH', index=False)
        updated_btc.to_excel(writer, sheet_name='BTC', index=False)
        updated_sol.to_excel(writer, sheet_name='SOL', index=False)
    
    print(f"Data for {date_str} has been added to {output_file}")
else:
    # If the file doesn't exist, create it with the new data
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_eth.to_excel(writer, sheet_name='ETH', index=False)
        df_btc.to_excel(writer, sheet_name='BTC', index=False)
        df_sol.to_excel(writer, sheet_name='SOL', index=False)

# update to google sheet

update_google_sheet(df_btc, 'btc')
update_google_sheet(df_eth, 'eth')
update_google_sheet(df_sol, 'sol')

print(f"Data for {date_str} has been added to Google Sheet")
