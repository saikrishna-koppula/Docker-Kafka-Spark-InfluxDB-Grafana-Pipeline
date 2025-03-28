import pandas as pd

top_50_us_equity_symbols = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.B', 'UNH', 'V',
    'JNJ', 'WMT', 'HD', 'PG', 'DIS', 'PYPL', 'MA', 'NVDA', 'INTC', 'PEP', 'PFE',
    'CSCO', 'KO', 'VZ', 'XOM', 'IBM', 'MRK', 'ABT', 'NKE', 'AMD', 'BA', 'CVX',
    'NFLX', 'GS', 'MCD', 'AMGN', 'ADBE', 'BABA', 'WFC', 'RTX', 'GM', 'CAT',
    'T', 'TMO', 'LLY', 'UPS', 'COST', 'BA', 'NVDIA', 'SQ', 'LMT', 'SPG',
    'MELI', 'STZ', 'MU', 'ORCL', 'LULU', 'BIDU', 'RBLX', 'AIG', 'FTNT', 
    'PXD', 'ZTS', 'ISRG', 'SYK', 'MAR', 'MS', 'GE', 'C', 'SLB', 'TGT', 
    'UAL', 'PLD', 'NDAQ', 'VLO', 'DE', 'CB', 'F', 'FIS', 'FISV', 'INTU'
]


symbols_data = pd.read_csv('asset_details.csv')
symbols_data = symbols_data[(symbols_data['class']=="us_equity") & (symbols_data['status']=="active")]
symbols_list = list(symbols_data.symbol)

common_values = list(set(top_50_us_equity_symbols) & set(symbols_list))
print("Common Values:", len(common_values), "\n", common_values)

file_path = 'Top_75_Active_US_Equity Symbols.txt'
with open(file_path, 'w') as file:
    file.write(repr(common_values))