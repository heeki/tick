import argparse
import csv
import json
import sys
from tick.symbol import Symbol
from tick.trade import Trade
from utils.kinesis_std import Kinesis
from utils.util import Util


def main():
    log = Util.get_logger("producer")

    ap = argparse.ArgumentParser()
    ap.add_argument('--rfile', required=True, help='MM/DD/YYYY')
    ap.add_argument('--dfile', required=True, help='dddd.dd')
    args = ap.parse_args()

    ref_file = args.rfile
    log.info("ref_file={}".format(ref_file))

    mapper = {}
    with open(ref_file, 'r') as csv_file:
        ref_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(ref_reader, None)
        for ref_data in ref_reader:
            ref = Symbol(ref_data)
            log.info(str(ref))
            mapper[ref.company_id] = ref

    data_file = args.dfile
    log.info("data_file={}".format(data_file))
    company_id = data_file.split('/')[-1].split('.')[0]
    log.info(mapper)

    total_count = 0
    status = {
        "FailedRecordCount": 0,
        "SuccessfulRecordCount": 0,
    }
    batch_iter = 0
    batch_size = 500
    batch_bytes = 0
    batch_records = []
    kinesis_stream = "tick-ingest"
    kclient = Kinesis(kinesis_stream)
    try:
        with open(data_file, 'r') as csv_file:
            trade_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for trade_data in trade_reader:
                total_count += 1
                batch_iter += 1

                trade = Trade(mapper[company_id].symbol, trade_data, Util.get_epoch())
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
                    log.info(response)
                    status["FailedRecordCount"] += json.loads(response)["FailedRecordCount"]
                    status["SuccessfulRecordCount"] += json.loads(response)["SuccessfulRecordCount"]
                    batch_records = []
            # processing the last set of data beyond batch_size
            response = kclient.put_batch(batch_records)
            log.info(response)
            status["FailedRecordCount"] += json.loads(response)["FailedRecordCount"]
            status["SuccessfulRecordCount"] += json.loads(response)["SuccessfulRecordCount"]
    except KeyboardInterrupt:
        log.error("keyboard interrupted")
    finally:
        log.info("processed_records={}, total_bytes={}, avg_bytes={}".format(total_count, batch_bytes, batch_bytes/total_count))
        log.info("final_status={}".format(json.dumps(status)))


if __name__ == "__main__":
    main()
