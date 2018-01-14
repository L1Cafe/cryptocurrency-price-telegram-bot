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
        ret_val = Decimal(float(json[1]['price_eur'])).quantize(Decimal(".01"))
        i = 0
        while json[i]['symbol'] != from_currency.upper():
            i += 1
        ret_val = Decimal(float(json[i]['price_'+to_currency])).quantize(Decimal(".01"))
    except Exception as err:
        raise Exception(f'Error when parsing prices: {err}')
    finally:
        return ret_val

#TODO: FIXME: There is an app-breaking bug where the prices appear to be the same.
# public functions
def fetch_prices():
    """Returns a dictionary with the first element being the currency and the second element being
    the currency to convert to.
    """
    ret_val = None
    try:
        prices = _get_prices_()

        btc_eur = _parse_prices_(prices, BTC, EUR)
        btc_usd = _parse_prices_(prices, BTC, USD)
        bch_eur = _parse_prices_(prices, BCH, EUR)
        bch_usd = _parse_prices_(prices, BCH, USD)
        ltc_eur = _parse_prices_(prices, LTC, EUR)
        ltc_usd = _parse_prices_(prices, LTC, USD)
        eth_eur = _parse_prices_(prices, ETH, EUR)
        eth_usd = _parse_prices_(prices, ETH, USD)
        dash_eur = _parse_prices_(prices, DASH, EUR)
        dash_usd = _parse_prices_(prices, DASH, USD)
        xmr_eur = _parse_prices_(prices, XMR, EUR)
        xmr_usd = _parse_prices_(prices, XMR, USD)
        xrp_eur = _parse_prices_(prices, XRP, EUR)
        xrp_usd = _parse_prices_(prices, XRP, USD)

        ret_val = {"BTC": {EUR: btc_eur, USD: btc_usd},
                   "BCH": {EUR: bch_eur, USD: bch_usd},
                   "LTC": {EUR: ltc_eur, USD: ltc_usd},
                   "ETH": {EUR: eth_eur, USD: eth_usd},
                   "DASH":{EUR: dash_eur, USD: dash_usd},
                   "XMR": {EUR: xmr_eur, USD: xmr_usd},
                   "XRP": {EUR: xrp_eur, USD: xrp_usd}}
    except Exception as err:
        print(f'Error when fetching data: {err}') # TODO: Probably should move this into a proper error logging method
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
