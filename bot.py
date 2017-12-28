#!/usr/bin/env python3
# TODO: Make sure Vim uses Python3 (probably homebrew) by default

import telegram
import telegram.ext # TODO: fix
import os
import logging
import csv

telegram_updater = telegram.ext.Updater(token=os.environ["telegram_token"])
telegram_dispatcher = telegram_updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello. I'm a"+
                     " cryptocurrency price watching bot.")
start_handler = telegram.ext.CommandHandler("start", start)
telegram_dispatcher.add_handler(start_handler)

def get_prices(bot,update):
    reply = ''
    # TODO: Fetch BTC price from FILE, assign it to btc_price
    # TODO: Fetch BCH price from FILE, assign it to bch_price
    # TODO: Fetch LTC price from FILE, assign it to ltc_price
    # TODO: Fetch ETH price from FILE, assign it to eth_price
    # TODO: Fetch DASH price from FILE, assign it to dash_price
    with open('prices.csv', 'r') as prices:
        reader = csv.DictReader(prices)
        for line in reader:
            reply+='1 #'+line["cryptocurrency"].upper()+' = '+line["price_eur"]+' EUR & '+line["price_usd"]+' USD \n'
            last_update=line["date"]
        reply+='Last update performed at '+last_update
    bot.send_message(chat_id=update.message.chat_id, text=reply)
get_prices_handler = telegram.ext.CommandHandler("get_prices", get_prices)
telegram_dispatcher.add_handler(get_prices_handler)

telegram_updater.start_polling()
