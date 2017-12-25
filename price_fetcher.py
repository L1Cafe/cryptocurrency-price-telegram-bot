#!/usr/bin/env python3

import csv
import os
import requests
import time
import datetime
from decimal import *
import logging

# constants
eur = 'eur'
usd = 'usd'

btc = 'btc'
bch = 'bch'
ltc = 'ltc'
eth = 'eth'
dash = 'dash'

# Supported currencies
cryptocurrencies = (btc,bch,ltc,eth,dash)
fiatcurrencies   = (eur,usd)

# private functions
def __get_prices__():
    ret_val = None
    try:
        response = requests.get(url="https://api.coinmarketcap.com/v1/ticker/?convert=EUR")
        print(f'{time.asctime(time.localtime(time.time()))} // Response HTTP Status Code: {response.status_code}')
        ret_val = response.json()
    except Exception as err:
        raise Exception(f'An exception occurred: {err}')
    return ret_val

def __parse_prices__(json,from_currency,to_currency):
    ret_val = None
    try:
        ret_val = Decimal(float(json[1]['price_eur'])).quantize(Decimal(".01"))
        i=0
        while (json[i]['symbol'] != from_currency.upper()):
            i+=1
        ret_val = Decimal(float(json[i]['price_'+to_currency])).quantize(Decimal(".01"))
    except Exception as err:
        raise Exception(f'Error when parsing prices: {err}')
    return ret_val

# public functions
def fetch_prices(): # returns a dictionary with the first element being the
                    # currency and the second element being the currency to
                    # convert to


    try:
        prices = __get_prices__()
        
        btc_eur = __parse_prices__(prices,btc,eur)
        btc_usd = __parse_prices__(prices,btc,usd)
        bch_eur = __parse_prices__(prices,bch,eur)
        bch_usd = __parse_prices__(prices,bch,usd)
        ltc_eur = __parse_prices__(prices,ltc,eur)
        ltc_usd = __parse_prices__(prices,ltc,usd)
        eth_eur = __parse_prices__(prices,eth,eur)
        eth_usd = __parse_prices__(prices,eth,usd)
        dash_eur = __parse_prices__(prices,dash,eur)
        dash_usd = __parse_prices__(prices,dash,usd)

        return {"btc": {eur: btc_eur,  usd: btc_usd},
                "bch": {eur: bch_eur,  usd: bch_usd},
                "ltc": {eur: ltc_eur,  usd: ltc_usd},
                "eth": {eur: eth_eur,  usd: eth_usd},
                "dash":{eur: dash_eur, usd: dash_usd}}
    except Exception as err:
        print(f'Error when fetching data: {err}')
        return None

def save_prices():
    try:
        prices = fetch_prices()
        with open('prices.csv', 'w') as pricescsv:
            writer = csv.DictWriter(pricescsv, fieldnames = ['date', 'cryptocurrency', 'price_eur', 'price_usd'], delimiter = ';')
            writer.writeheader()
            #writer.writerow([time.asctime(), prices[btc][eur], prices[btc][usd]])  # TODO FIX DATE FORMAT
            #writer.writerow({'date': time.asctime(), 'cryptocurrency': btc, 'price_eur': prices[btc][eur], 'price_usd': prices[btc][usd]})
            for crypto in cryptocurrencies:
                writer.writerow({'date': time.asctime(), 'cryptocurrency': crypto, 'price_eur': prices[crypto][fiatcurrencies[0]],
                                     'price_usd': prices[crypto][fiatcurrencies[1]]})
            pricescsv.close()
    except Exception as err:
        print(f'Error when saving prices: {err}')

#TODO: Call savePricesDB every hour, initially with cron
save_prices()
