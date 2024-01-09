# Binance Trading Bot

## Overview
This Python script is a simple Binance trading bot that automatically buys and sells BTC based on predefined thresholds. It uses the Binance API for trading and gspread for updating a Google Spreadsheet with trading actions.

## Features
- Automated buying and selling of BTC based on price thresholds.
- Integration with Binance API for real-time market data and trading.
- Logging of trading actions to a Google Spreadsheet using gspread.
- Changing the trading symbols as you wish, the bot not only for BTC.

## Getting Started
1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/your-username/binance-trading-bot.git

## Install the required dependencies.
    pip install -r requirements.txt

Set up your Binance API keys.

Obtain API key and secret from Binance.
Replace the placeholder API key and secret in the script with your actual credentials.
Set up Google Sheets API credentials.

Download the JSON key file for your service account from the Google Cloud Console.
Replace the placeholder JSON key file path in the script with the path to your key file.
Run the script.


    python N_T_M_2_main.py

## Configuration
    api_key and secret_key: Your Binance API credentials.
    json_key_file_path: Path to the JSON key file for your Google Sheets API service account.
    symbol: Trading pair symbol (default is 'BTCEUR').
    BUY_THRESHOLD and SELL_THRESHOLD: Buy and sell price thresholds.
    QUANTITY: Quantity of BTC to buy or sell.

 ## License
  This project is licensed under the MIT License.

## Disclaimer
  Use this trading bot at your own risk. Cryptocurrency trading involves significant risk, and it's important to carefully test and understand the behavior of any automated trading system.
  you can use the simupation i uploaded to check your trading algorithem.

## Contributing
  Contributions are welcome! Feel free to open issues or pull requests.

## Acknowledgements
  Binance API
  gspread
  Python-Binance
  Contact
  For questions or support, contact Tomer Avni - avni1tomer@gmail.com.
