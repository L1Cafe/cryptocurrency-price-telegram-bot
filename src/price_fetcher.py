#!/usr/bin/env python3
"""this file simply fetches and creates (or overwrites) a file named prices.csv containing the
latest crypto prices"""

import csv
from decimal import *
from datetime import datetime
import requests

# constants
EUR = 'EUR'
USD = 'USD'

BTC = 'BTC'
BCH = 'BCH'
LTC = 'LTC'
ETH = 'ETH'
DASH = 'DASH'
XMR = 'XMR'
XRP = 'XRP'

# Supported currencies
CRYPTO_CURRENCIES = (BTC, BCH, LTC, ETH, DASH, XMR, XRP)
FIAT_CURRENCIES = (EUR, USD)


# private functions
def _get_prices_():
    ret_val = None
    try:
        ret_val = requests.get(url="https://api.coinmarketcap.com/v1/ticker/?convert=EUR").json()
    except Exception as err:
        raise Exception(f'An exception occurred: {err}')
    finally:
        return ret_val

def _parse_prices_(json, from_currency, to_currency):
    ret_val = None
    try:
        i = 0
        while json[i]['symbol'] != from_currency.upper():
            i += 1
        ret_val = Decimal(float(json[i]['price_'+to_currency.lower()])).quantize(Decimal(".01"))
    except Exception as err:
        raise Exception(f'Error when parsing prices: {err}')
    finally:
        return ret_val

# public functions
def fetch_prices():
    """Returns a dictionary with the first element being the currency and the second element being
    the currency to convert to.
    """
    ret_val = {}

    try:
        prices = _get_prices_()

        for crypto in CRYPTO_CURRENCIES:
            for fiat in FIAT_CURRENCIES:
                if crypto not in ret_val:
                    ret_val[crypto] = {}
                ret_val[crypto][fiat] = _parse_prices_(prices, crypto, fiat)
    except Exception as err:
        print(f'Error when fetching data: {err}')
    finally:
        return ret_val


def save_prices():
    """this function tries to overwrite a file called prices.csv with the latest prices fetched"""
    try:
        prices = fetch_prices()
        with open('prices.csv', 'w') as pricescsv:
            writer = csv.DictWriter(pricescsv, fieldnames=
                                    ['date', 'cryptocurrency', 'price_eur', 'price_usd'],
                                    delimiter=',')
            writer.writeheader()
            for crypto in CRYPTO_CURRENCIES:
                writer.writerow({'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 'cryptocurrency': crypto,
                                 'price_eur': prices[crypto][FIAT_CURRENCIES[0]],
                                 'price_usd': prices[crypto][FIAT_CURRENCIES[1]]})
            pricescsv.close()
    except Exception as err:
        print(f'Error when saving prices: {err}')


def main():
    """main function"""
    save_prices()

main()
