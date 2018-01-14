#!/usr/bin/env python3
"""this is meant to be run every hour, it will process the subscriptions and send messages every
   time it is run"""

import csv
import json
from configparser import SafeConfigParser
from telegram import Bot as telegram_bot

SETTINGSINI = 'settings.ini'

CONFIG = SafeConfigParser()
CONFIG.read(SETTINGSINI)

TELEGRAM_TOKEN = CONFIG['main']['telegram_token']
USER_SUBS = json.loads(CONFIG['daily-subscriptions']['users'])
GROUP_SUBS = json.loads(CONFIG['daily-subscriptions']['groups'])
CHANNEL_SUBS = json.loads(CONFIG['daily-subscriptions']['channels'])
SUBSCRIPTIONS = USER_SUBS+GROUP_SUBS+CHANNEL_SUBS
MESSAGE = ''

TELEGRAM_BOT = telegram_bot(token=TELEGRAM_TOKEN)

with open('prices.csv', 'r') as prices:
    READER = csv.DictReader(prices)
    for line in READER:
        MESSAGE += '1 #' + line["cryptocurrency"].upper() + ' = ' + line["price_eur"]+' EUR & '
        MESSAGE += line["price_usd"] + ' USD \n'
        last_update=line["date"]
MESSAGE += '--\n'
MESSAGE += 'The information displayed above was last updated at: '+last_update

for subscription in SUBSCRIPTIONS:
    TELEGRAM_BOT.send_message(chat_id=subscription, text=MESSAGE)
