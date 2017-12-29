import telegram
import telegram.ext
from telegram import Bot as telegramBot
import os
import csv

telegram_token =   os.environ["telegram_token"]
telegram_admin =   os.environ["telegram_admin_id"]
telegram_chat_id = os.environ["telegram_chat_id"]
telegram_text = ''

telegram_bot = telegramBot(token=telegram_token)

with open('prices.csv', 'r') as prices:
    reader = csv.DictReader(prices)
    for line in reader:
        telegram_text+='1 #'+line["cryptocurrency"].upper()+' = '+line["price_eur"]+' EUR & '+line["price_usd"]+' USD \n'
        last_update=line["date"]
telegram_text+='The information displayed above was last updated at: '+last_update

telegram_bot.send_message(chat_id=telegram_chat_id, text=telegram_text)
