import csv
import json
from tick.symbol import Symbol
from tick.trade import Trade
from utils.kinesis import Kinesis
from utils.util import Util


class Producer:
    def __init__(self, rfile, dfile, stream, batch_size):
        self.rfile = rfile
        self.dfile = dfile
        self.stream = stream
        self.batch_size = batch_size
        self.client = Kinesis(self.stream)

        mapper = {}
        with open(rfile, 'r') as csv_file:
            ref_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            next(ref_reader, None)
            for ref_data in ref_reader:
                ref = Symbol(ref_data)
                mapper[ref.company_id] = ref
        
        company_id = self.dfile.split('/')[-1].split('.')[0]
        self.symbol = mapper[company_id].symbol
        self.log = Util.get_logger("producer:{}".format(self.stream))
    
    def produce(self, limit):
        status = {
            "FailedRecordCount": 0,
            "SuccessfulRecordCount": 0,
        }
        total_count = 0
        batch_count = 0
        batch_bytes = 0
        batch_records = []
        try:
            with open(self.dfile, 'r') as csv_file:
                trade_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
                # process in batches
                for trade_record in trade_reader:
                    if limit is not None and total_count < int(limit):
                        trade = Trade(self.symbol, trade_record)
                        trade.update_datetime()
                        record = {
                            'Data': str(trade),
                            'PartitionKey': trade.symbol
                        }
                        record_size = len(json.dumps(record).encode('utf-8'))
                        batch_bytes += record_size
                        batch_records.append(record)
                        total_count += 1
                        batch_count += 1
                        self.log.info("total_count={}, record_size={}, trade={}".format(total_count, record_size, str(trade)))
                    else:
                        break
                    if batch_count % self.batch_size == 0:
                        response = self.client.put_batch(batch_records)
                        self.log.info(json.dumps(response))
                        status = { k: status[k] + v for (k, v) in response.items() }
                        batch_records = []
                # process the last set of data beyond batch_size
                if len(batch_records) > 1:
                    response = self.client.put_batch(batch_records)
                    self.log.info(json.dumps(response))
                    status = { k: status[k] + v for (k, v) in response.items() }
        except KeyboardInterrupt:
            self.log.error("keyboard interrupted")
        finally:
            self.log.info("processed_records={}, total_bytes={}, avg_bytes={}".format(total_count, batch_bytes, batch_bytes/total_count))
            self.log.info("final_status={}".format(json.dumps(status)))
