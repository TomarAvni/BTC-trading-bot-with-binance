import time
import datetime
import gspread
from binance.client import Client
from binance.enums import *


class BinanceTrader:
    BUY_THRESHOLD = 0.997
    SELL_THRESHOLD = 1.003
    QUANTITY = '0.001'

    def __init__(self, api_key, secret_key, symbol='BTCEUR'):
        self.client = Client(api_key, secret_key)
        self.symbol = symbol
        self.ticker = None
        self.price = None
        self.buy_price = None
        self.sell_price = None
        self.eur_balance = None
        self.btc_balance = None

    def get_ticker_price(self):
        try:
            self.ticker = self.client.get_symbol_ticker(symbol=self.symbol)
            self.price = float(self.ticker['price'])
        except Exception as e:
            self.log_error(f'Error getting ticker price: {e}')
            self.price = 0.0

    def get_btc_balance(self):
        try:
            balance_info = self.client.get_asset_balance(asset='BTC')
            self.btc_balance = float(balance_info['free'])
        except Exception as e:
            self.log_error(f'Error getting BTC balance: {e}')
            self.btc_balance = None

    def sell_btc(self):
        self.get_ticker_price()
        self.get_btc_balance()
        if self.btc_balance is not None and self.btc_balance >= float(self.QUANTITY):
            order = self.client.create_order(
                symbol=self.symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=self.QUANTITY
            )
            print(order)
            print('Finish selling')
            self.update_spreadsheet('sell_btc')
            self.update_prices()
        else:
            self.log_error('Not enough BTC to sell or unable to retrieve balance')

    def buy_btc(self):
        self.get_ticker_price()
        self.get_btc_balance()
        if self.eur_balance >= 25:
            order = self.client.create_order(
                symbol=self.symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=self.QUANTITY
            )
            print(order)
            print('Finish buying')
            self.update_spreadsheet('buy_btc')
            self.update_prices()
        else:
            self.log_error('Not enough EUR for the order')

    def watch_btc_price(self):
        while True:
            try:
                self.get_ticker_price()
                current_time = datetime.datetime.now()
                if self.price >= self.sell_price:
                    self.sell_btc()
                elif self.price <= self.buy_price:
                    self.buy_btc()
                else:
                    print(f'Did not do any trading at: {current_time}, '
                          f'Value to follow = {self.buy_price / self.price * 100}, '
                          f'{self.price / self.sell_price * 100}')
                time.sleep(60)
            except Exception as e:
                self.log_error(f'Error during trading: {e}')
                time.sleep(60)

    def update_spreadsheet(self, action):
        sa = gspread.service_account("path to your gspread API")
        spreadsheet = sa.open('N_T_M_action')
        worksheet = spreadsheet.get_worksheet(0)
        cell_skip_down = 787
        cell_skip_right = 1
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%m/%d/%Y %H:%M:%S")

        worksheet.update_cell(cell_skip_down, cell_skip_right, action)
        cell_skip_right += 1
        worksheet.update_cell(cell_skip_down, cell_skip_right, self.btc_balance)
        cell_skip_right += 1
        worksheet.update_cell(cell_skip_down, cell_skip_right, self.eur_balance)
        cell_skip_right += 1
        worksheet.update_cell(cell_skip_down, cell_skip_right, self.price)
        cell_skip_right += 1
        worksheet.update_cell(cell_skip_down, cell_skip_right, current_time_str)
        cell_skip_right += 1

    def update_prices(self):
        self.buy_price = self.BUY_THRESHOLD * self.price
        self.sell_price = self.SELL_THRESHOLD * self.price

    def log_error(self, message):
        current_time = datetime.datetime.now()
        print(f'Error at {current_time}: {message}')
        # Consider logging to a file or taking appropriate actions


if __name__ == "__main__":
    trader = BinanceTrader(api_key='your_api_key',
                           secret_key='your_secret_key')
    trader.watch_btc_price()
