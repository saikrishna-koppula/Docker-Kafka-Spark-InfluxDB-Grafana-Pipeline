import requests
import pandas as pd
import io

url = "https://paper-api.alpaca.markets/v2/assets"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": "PKYR8K4C102QUVUO3P9O",
    "APCA-API-SECRET-KEY": "5KlIUpgWYdMbBHlNvNh08AbchflKrwOzNWO3henI"
}

response = requests.get(url, headers=headers)
asset_data = pd.read_json(io.StringIO(response.text))
asset_data.to_csv('asset_details.csv')

# # ------------------------------------------------------------------------------------ # #
# The same can also be achieved using python functions as below.
# # ------------------------------------------------------------------------------------ # #
# # The below is for Active Stocks
# from alpaca.trading.client import TradingClient

# # Initialize the trading client
# trading_client = TradingClient(api_key="your_api_key", secret_key="your_secret_key")

# # Get all active assets (stocks)
# active_assets = trading_client.get_all_active_assets()

# # Filter symbols that are tradable
# active_symbols = [asset.symbol for asset in active_assets if asset.tradable]

# print(active_symbols)  # List of active stock symbols

# # ------------------------------------------------------------------------------------ # #
# # The below is for Active Crypto Currency
# from alpaca.data import CryptoHistoricalDataClient

# # Initialize the crypto data client
# crypto_client = CryptoHistoricalDataClient()

# # Fetch supported crypto symbols
# crypto_assets = crypto_client.get_supported_assets()

# print(crypto_assets)  # List of active crypto trading pairs
