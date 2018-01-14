#!/usr/bin env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

`which /usr/local/bin/python3.6` src/price_fetcher.py

