import argparse
import json
import logging
import os
import sys
from tick.trade import Trade
from utils.util import Util


log = Util.get_logger('tick')


def _init():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', required=True, help='MM/DD/YYYY')
    ap.add_argument('--price', required=True, help='dddd.dd')
    args = ap.parse_args()
    log.info("date={}, price={}".format(args.date, args.price))
    return (args.date, args.price)

def main():
    (date, price) = _init()
    symbols = ["AAPL", "INTC", "MSFT"]
    symbol = symbols[0]
    payload = [
        date,
        "09:45:53.950",
        price,
        "100",
        "N",
        "C"
    ]
    ingest_epoch = Util.get_timestamp()
    trade = Trade(symbol, payload, ingest_epoch)
    log.info(trade)


if __name__ == "__main__":
    main()
