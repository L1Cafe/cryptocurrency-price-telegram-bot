#! /usr/bin env bash

# Telegram Bot token
export telegramToken="<YOUR BOT TOKEN HERE>"
# Telegram admin ID
export telegramAdminId="<YOUR ID HERE>"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

`which /usr/local/bin/python3.6` bot.py
