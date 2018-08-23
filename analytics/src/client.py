import csv
import sys
from utils.util import Util
from tick.symbol import Symbol
from tick.trade import Trade


def main():
    log = Util.get_logger("client")

    ref_file = sys.argv[1]
    log.info("ref_file={}".format(ref_file))

    mapper = {}
    with open(ref_file, 'r') as csv_file:
        ref_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(ref_reader, None)
        for ref_data in ref_reader:
            ref = Symbol(ref_data)
            log.info(str(ref))
            mapper[ref.company_id] = ref

    data_file = sys.argv[2]
    log.info("data_file={}".format(data_file))
    company_id = data_file.split('/')[-1].split('.')[0]
    log.info("symbol={}, company_id={}, company_name='{}'"
             .format(mapper[company_id].symbol, mapper[company_id].company_id, mapper[company_id].company_name))

    with open(data_file, 'r') as csv_file:
        trade_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for trade_data in trade_reader:
            trade = Trade(mapper[company_id].symbol, trade_data)
            log.info(str(trade))


if __name__ == "__main__":
    main()
