#!/usr/bin/env python3
"""this is the main Telegram bot"""

import csv
from configparser import SafeConfigParser
import json
import telegram
import telegram.ext

SETTINGSINI = 'settings.ini'

CONFIG = SafeConfigParser()
CONFIG.read(SETTINGSINI)
TELEGRAM_TOKEN = CONFIG['main']['telegram_token']

TELEGRAM_UPDATER = telegram.ext.Updater(token=TELEGRAM_TOKEN)
TELEGRAM_DISPATCHER = TELEGRAM_UPDATER.dispatcher

# private functions

def _is_subscribed_(telegram_id):
    """checks whether a given Telegram ID (user or group) is subscribed or not, returns a bool"""
    CONFIG.read(SETTINGSINI)
    user_subs = json.loads(CONFIG['daily-subscriptions']['users'])
    group_subs = json.loads(CONFIG['daily-subscriptions']['groups'])
    channel_subs = json.loads(CONFIG['daily-subscriptions']['channels'])
    subscriptions = user_subs+group_subs+channel_subs
    return telegram_id in subscriptions

def _is_group_(telegram_id):
    return telegram_id < 0

# TODO: Maybe condense the two functions below into a single _edit_subscription_ that takes a
# Telegram ID and an operation mode (add or remove) and correctly operates.

def _add_subscription_(telegram_id):
    """takes a telegram ID (user or group) and adds it to the config file"""
    CONFIG.read(SETTINGSINI)
    if _is_group_(telegram_id):
        group_subs = json.loads(CONFIG['daily-subscriptions']['groups'])
        group_subs.append(telegram_id)
        CONFIG['daily-subscriptions']['groups'] = json.dumps(group_subs)
    else:
        user_subs = json.loads(CONFIG['daily-subscriptions']['users'])
        user_subs.append(telegram_id)
        CONFIG['daily-subscriptions']['users'] = json.dumps(user_subs)
    with open(SETTINGSINI, 'w') as configfile:
        CONFIG.write(configfile)

def _remove_subscription_(telegram_id):
    """takes a telegram ID (user or group) and removes it from the config file"""
    CONFIG.read(SETTINGSINI)
    if _is_group_(telegram_id):
        group_subs = json.loads(CONFIG['daily-subscriptions']['groups'])
        group_subs.remove(telegram_id)
        CONFIG['daily-subscriptions']['groups'] = json.dumps(group_subs)
    else:
        user_subs = json.loads(CONFIG['daily-subscriptions']['users'])
        user_subs.remove(telegram_id)
        CONFIG['daily-subscriptions']['users'] = json.dumps(user_subs)
    with open(SETTINGSINI, 'w') as configfile:
        CONFIG.write(configfile)

# public functions

def start(bot, update):
    """this function is called when the command /start is issued"""
    message = "Hello! I'm a cryptocurrency price watching bot."
    bot.send_message(chat_id=update.message.chat_id, text=message)
START_HANDLER = telegram.ext.CommandHandler("start", start)
TELEGRAM_DISPATCHER.add_handler(START_HANDLER)

def get_prices(bot, update):
    """this function is called when the command /get_prices is issued"""
    reply = ''
    with open('prices.csv', 'r') as prices:
        reader = csv.DictReader(prices)
        for line in reader:
            reply += '1 #'+line["cryptocurrency"].upper()+' = '
            reply += line["price_eur"]+' EUR & '+line["price_usd"]+' USD \n'
            last_update = line["date"]
        reply += 'The information displayed above was last updated at: '+last_update
    bot.send_message(chat_id=update.message.chat_id, text=reply)
GET_PRICES_HANDLER = telegram.ext.CommandHandler("get_prices", get_prices)
TELEGRAM_DISPATCHER.add_handler(GET_PRICES_HANDLER)

def subscribe(bot, update):
    """this function adds the current chat ID (be it person or group) to send periodic updates to"""
    if _is_subscribed_(update.message.chat_id):
        reply = 'You are already subscribed.'
    else:
        _add_subscription_(update.message.chat_id)
        reply = 'You have subscribed to daily updates.'
    bot.send_message(chat_id=update.message.chat_id, text=reply)
SUBSCRIBE_HANDLER = telegram.ext.CommandHandler("subscribe", subscribe)
TELEGRAM_DISPATCHER.add_handler(SUBSCRIBE_HANDLER)

def unsubscribe(bot, update):
    """this function checks if the user is subscribed and removes it"""
    if _is_subscribed_(update.message.chat_id):
        _remove_subscription_(update.message.chat_id)
        reply = 'You have unsubscribed from daily updates.'
    else:
        reply = 'You are not subscribed.'
    bot.send_message(chat_id=update.message.chat_id, text=reply)
UNSUBSCRIBE_HANDLER = telegram.ext.CommandHandler("unsubscribe", unsubscribe)
TELEGRAM_DISPATCHER.add_handler(UNSUBSCRIBE_HANDLER)

def subscription_status(bot, update):
    """this function returns the subscription status for a given user or group"""
    pass
SUBSCRIPTION_STATUS_HANDLER = telegram.ext.CommandHandler("subscription_status",
                                                          subscription_status)
TELEGRAM_DISPATCHER.add_handler(SUBSCRIPTION_STATUS_HANDLER)

TELEGRAM_UPDATER.start_polling()
