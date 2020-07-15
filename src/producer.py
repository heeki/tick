import argparse
import csv
import json
import sys
from tick.symbol import Symbol
from tick.trade import Trade
from utils.kinesis_std import Kinesis
from utils.util import Util


log = Util.get_logger("producer")
batch_size = -1
company_id = -1
mapper = {}


def init():
    global batch_size, company_id, mapper

    ap = argparse.ArgumentParser()
    ap.add_argument('--rfile', required=True, help='data/SampleEquityData_US/CompanyInfo/CompanyInfo.asc')
    ap.add_argument('--dfile', required=True, help='data/SampleEquityData_US/Trades/14081.csv')
    ap.add_argument('--batch_size', required=False, help='500')
    args = ap.parse_args()

    batch_size = int(args.batch_size) if args.batch_size is not None else 100
    company_id = args.dfile.split('/')[-1].split('.')[0]
    with open(args.rfile, 'r') as csv_file:
        ref_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(ref_reader, None)
        for ref_data in ref_reader:
            ref = Symbol(ref_data)
            mapper[ref.company_id] = ref

    return args


def produce(dfile):
    status = {
        "FailedRecordCount": 0,
        "SuccessfulRecordCount": 0,
    }
    total_count = 0
    batch_iter = 0
    batch_bytes = 0
    batch_records = []
    kinesis_stream = "tick-ingest"
    kclient = Kinesis(kinesis_stream)
    try:
        with open(dfile, 'r') as csv_file:
            trade_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            # process in batches
            for trade_data in trade_reader:
                total_count += 1
                batch_iter += 1

                trade = Trade(mapper[company_id].symbol, trade_data, Util.get_epoch())
                trade.update_datetime()
                record = {
                    'Data': str(trade),
                    'PartitionKey': trade.symbol
                }
                record_size = len(json.dumps(record).encode('utf-8'))
                batch_bytes += record_size
                batch_records.append(record)
                log.info("i={}, record_size={}, trade={}".format(total_count, record_size, str(trade)))

                if batch_iter % batch_size == 0:
                    response = kclient.put_batch(batch_records)
                    log.info(json.dumps(response))
                    status["FailedRecordCount"] += response["FailedRecordCount"]
                    status["SuccessfulRecordCount"] += response["SuccessfulRecordCount"]
                    batch_records = []
            # process the last set of data beyond batch_size
            response = kclient.put_batch(batch_records)
            log.info(json.dumps(response))
            status["FailedRecordCount"] += response["FailedRecordCount"]
            status["SuccessfulRecordCount"] += response["SuccessfulRecordCount"]
    except KeyboardInterrupt:
        log.error("keyboard interrupted")
    finally:
        log.info("processed_records={}, total_bytes={}, avg_bytes={}".format(total_count, batch_bytes, batch_bytes/total_count))
        log.info("final_status={}".format(json.dumps(status)))


def main():
    args = init()
    produce(args.dfile)


if __name__ == "__main__":
    main()
