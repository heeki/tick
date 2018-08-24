import csv
import sys
from utils.kinesis import Kinesis
from utils.util import Util
from tick.symbol import Symbol
from tick.trade import Trade


def main():
    log = Util.get_logger("producer")

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

    batch_iter = 0
    batch_size = 50
    batch_records = []
    kinesis_stream = "tick-ingest"
    kclient = Kinesis(kinesis_stream)
    with open(data_file, 'r') as csv_file:
        trade_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for trade_data in trade_reader:
            trade = Trade(mapper[company_id].symbol, trade_data, Util.get_epoch())
            log.info(str(trade))

            batch_iter += 1
            record = {
                'Data': str(trade),
                'PartitionKey': trade.symbol
            }
            batch_records.append(record)
            if batch_iter % batch_size == 0:
                response = kclient.put_batch(batch_records)
                log.info(response)
                batch_records = []


if __name__ == "__main__":
    main()
