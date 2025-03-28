import pandas as pd

symbols_data = pd.read_csv('asset_details.csv')
symbols_data = symbols_data[(symbols_data['class']=="crypto") & (symbols_data['status']=="active")]
symbols_list = list(symbols_data.symbol)

filter_symbol_list = []

for symbol in symbols_list:
    if symbol.endswith("USD"):
        filter_symbol_list.append(symbol)

print(filter_symbol_list)