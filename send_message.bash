#!/usr/bin env bash

# Telegram Bot token
export telegram_token="DEPRECATED"
# Telegram admin ID
export telegram_admin_id="DEPRECATED"
# Telegram chat ID
export telegram_chat_id="DEPRECATED"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

`which /usr/local/bin/python3.6` src/send_message.py