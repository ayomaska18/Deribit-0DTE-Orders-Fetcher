import requests
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import time
import csv
import logging
import pandas as pd 
import os

# logging.basicConfig(filename='atm_iv_BTC.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

base_url = 'https://deribit.com/api/v2/public'
script_dir = os.path.dirname(os.path.abspath(__file__))

# get current index_price of the asset
def get_index_price(index_name: str):
    endpoint = '/get_index_price'
    url = base_url + endpoint
    params = {
        'index_name': index_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        index_price = response_data['result']['index_price']
        return index_price
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.text}")
        return None
    
# get the order book of the specifized instrument
def get_order_book(instrument_name: str, depth: int):
    endpoint = '/get_order_book'
    url = base_url + endpoint
    params = {
        'instrument_name': instrument_name,
        'depth': depth

    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.text}")
        return None

# get the list of instruments
def get_instruments(currency: str, kind: str, expired: str):
    endpoint = '/get_instruments'
    url = base_url + endpoint
    params = {
        'currency': currency,
        'kind': kind,
        'expired': expired

    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.text}")
        return None

# get all instruments that expire tomorrow
def get_0dte_instruments(data: dict, start_timestamp, end_timestamp):
    instruments = data['result']

    tomorrow_options = []

    for instrument in instruments:
        tomorrow_options.append(instrument)
    
    return tomorrow_options

# get the atm option 
def get_sol_options(instruments: list):
    sol_options = [instrument for instrument in instruments if 'SOL' in instrument['instrument_name']]
    return sol_options

def get_last_trades_by_instrument_and_time(instrument_name: str, start_timestamp: int, end_timestamp: int):
    endpoint = '/get_last_trades_by_instrument_and_time'
    url = base_url + endpoint
    params = {
        'instrument_name': instrument_name,
        'start_timestamp': start_timestamp,
        'end_timestamp': end_timestamp,
        'count': 1000
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        return response_data['result']['trades']
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.text}")
        return None

def filter_orders(trades: list, instrument_name: str):
    buy_calls = []
    sell_calls = []
    buy_puts = []
    sell_puts = []

    strike_price = int(instrument_name.split('-')[-2])
    
    for trade in trades:
        direction = trade['direction']
        trade['strike_price'] = strike_price
        is_call = instrument_name.endswith('C')
        is_put = instrument_name.endswith('P')

        if is_call:
            if direction == 'buy':
                buy_calls.append(trade)
            elif direction == 'sell':
                sell_calls.append(trade)
        elif is_put:
            if direction == 'buy':
                buy_puts.append(trade)
            elif direction == 'sell':
                sell_puts.append(trade)
    
    save_trades_to_csv(buy_calls, 'SOL_buy_calls')
    save_trades_to_csv(sell_calls, 'SOL_sell_calls')
    save_trades_to_csv(buy_puts, 'SOL_buy_puts')
    save_trades_to_csv(sell_puts, 'SOL_sell_puts')

def save_trades_to_csv(trades: list, file_prefix: str):
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    file_name = os.path.join(script_dir, 'Orders', f'{file_prefix}_{today_date}.csv')
    
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        for trade in trades:
            writer.writerow([trade['timestamp'], trade['trade_id'], trade['instrument_name'], trade['direction'], trade['price'], trade['amount'], trade['strike_price']])


def plot_vol_graph():
    buy_calls_df = pd.read_csv('Orders/SOL-5AUG24_buy_calls.csv', header=None, names=['timestamp', 'trade_id', 'instrument_name', 'direction', 'price', 'amount', 'strike'])
    sell_calls_df = pd.read_csv('Orders/SOL-5AUG24_sell_calls.csv', header=None, names=['timestamp', 'trade_id', 'instrument_name', 'direction', 'price', 'amount', 'strike'])
    buy_puts_df = pd.read_csv('Orders/SOL-5AUG24_buy_puts.csv', header=None, names=['timestamp', 'trade_id', 'instrument_name', 'direction', 'price', 'amount', 'strike'])
    sell_puts_df = pd.read_csv('Orders/SOL-5AUG24_sell_puts.csv', header=None, names=['timestamp', 'trade_id', 'instrument_name', 'direction', 'price', 'amount', 'strike'])

    buy_calls_agg = buy_calls_df.groupby('strike')['amount'].sum()
    sell_calls_agg = sell_calls_df.groupby('strike')['amount'].sum()
    buy_puts_agg = buy_puts_df.groupby('strike')['amount'].sum()
    sell_puts_agg = sell_puts_df.groupby('strike')['amount'].sum()

    ig, ax = plt.subplots(figsize=(12, 6))

    # Define positions for the bars
    bar_width = 0.2
    strikes = sorted(set(buy_calls_agg.index) | set(sell_calls_agg.index) | set(buy_puts_agg.index) | set(sell_puts_agg.index))

    buy_calls_positions = [x - 1.5 * bar_width for x in range(len(strikes))]
    sell_calls_positions = [x - 0.5 * bar_width for x in range(len(strikes))]
    buy_puts_positions = [x + 0.5 * bar_width for x in range(len(strikes))]
    sell_puts_positions = [x + 1.5 * bar_width for x in range(len(strikes))]

    ax.bar(buy_calls_positions, buy_calls_agg.reindex(strikes, fill_value=0), width=bar_width, label='Buy Calls', color='blue')
    ax.bar(sell_calls_positions, sell_calls_agg.reindex(strikes, fill_value=0), width=bar_width, label='Sell Calls', color='cyan')
    ax.bar(buy_puts_positions, buy_puts_agg.reindex(strikes, fill_value=0), width=bar_width, label='Buy Puts', color='green')
    ax.bar(sell_puts_positions, sell_puts_agg.reindex(strikes, fill_value=0), width=bar_width, label='Sell Puts', color='red')

    # Add labels and title
    ax.set_xlabel('Strike Price')
    ax.set_ylabel('Volume')
    ax.set_title('BTC-5AUG24 - Volumes of Executed Orders by Strike Price')
    ax.set_xticks(range(len(strikes)))
    ax.set_xticklabels(strikes, rotation=45)
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

     
def main():

    today = datetime.datetime.now(datetime.timezone.utc)
    start_time = datetime.datetime(today.year, today.month, today.day - 1, 8, 0)
    end_time = datetime.datetime(today.year, today.month, today.day, 8, 0)
    # end_time = today
    end_timestamp = int(end_time.timestamp() * 1000)
    start_timestamp = int(start_time.timestamp() * 1000)

    instruments_USDC = get_instruments('USDC', 'option', 'true')

    sol_options = get_sol_options(instruments_USDC['result'])

    SOL_0dte = get_0dte_instruments({'result': sol_options}, start_timestamp, end_timestamp)

    for instrument in SOL_0dte:
        trades = get_last_trades_by_instrument_and_time(instrument['instrument_name'], start_timestamp, end_timestamp)
        if trades:
            filter_orders(trades, instrument['instrument_name'])
    
    # plot_vol_graph()
        
if __name__ == "__main__":
    main()
