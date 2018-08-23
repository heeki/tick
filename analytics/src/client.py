import json
from utils.util import Util
from tick.trade import Trade


def main():
    log = Util.get_logger("client")

    trade = Trade()
    log.info("exchanges={}".format(json.dumps(trade.exchanges)))


if __name__ == "__main__":
    main()
