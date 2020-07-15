import csv
import json
import numpy
import sys
from tick.symbol import Symbol
from tick.trade import Trade
from utils.kinesis import Kinesis
from utils.util import Util


class Consumer:
    def __init__(self, stream, shard, batch_size):
        self.stream = stream
        self.shard = shard
        self.batch_size = batch_size
        self.client = Kinesis(stream)
        self.log = Util.get_logger("consumer:{}".format(self.stream))
    
    def get_shards(self):
        return self.client.get_shards()
    
    def consume(self, position):
        """
        param position: where the iterator should start reading
        return: none

        position can take the following values:
        - AT_SEQUENCE_NUMBER: start reading at the specified position
        - AFTER_SEQUENCE_NUMBER: start reading right after the specified position
        - AT_TIMESTAMP: start reading at the position denoted by the tiemstamp
        - TRIM_HORIZON: start reading at the last untrimmed record (oldest record)
        - LATEST: start reading after the most recent record (latest record)
        """

        # tracking values        
        i = 1
        j = 1
        latencies = {}

        # initialize iterator
        iterator = self.client.get_iterator(self.shard, position)
        self.log.info("shard={}, iterator={}".format(self.shard, iterator))
        while True:
            try:
                output = self.client.get_records(iterator, self.batch_size)
                iterator = output["NextShardIterator"]
                for record in output["Records"]:
                    data = json.loads(record["Data"])
                    current_epoch = Util.get_epoch()
                    ingest_epoch = data["ingest_epoch"]
                    latency = (current_epoch - ingest_epoch) * 1000
                    symbol = data["symbol"]
                    if symbol not in latencies.keys():
                        latencies[symbol] = []
                    latencies[symbol].append(latency)
                    values = {
                        "symbol": symbol,
                        "price": data["price"],
                        "current_epoch": current_epoch,
                        "ingest_epoch": ingest_epoch,
                        "latency_ms": latency
                    }
                    self.log.info("i={}, j={}, values={}".format(i, j, json.dumps(values)))
                    i = 1 if i == self.batch_size else i + 1
                    j += 1
            except KeyboardInterrupt:
                self.log.info("KeyboardInterrupt")
                for symbol in latencies:
                    total_measurements = len(latencies[symbol])
                    average_latency = numpy.convolve(latencies[symbol], numpy.ones(total_measurements,)/total_measurements, mode='valid')
                    self.log.info("symbol={}, processed_records={}, average_latency_ms={}".format(symbol, total_measurements, average_latency))
                sys.exit(1)
