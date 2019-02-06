import boto3
import numpy as np
import json
import time
import sys
from utils.util import Util


class Kinesis:
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.client = boto3.client('kinesis')
        self.log = Util.get_logger("kinesis")

    def get_shards(self):
        response = self.client.describe_stream(StreamName=self.stream_name)
        return [shard["ShardId"] for shard in response["StreamDescription"]["Shards"]]

    def put_batch(self, records):
        response = self.client.put_records(Records=records, StreamName=self.stream_name)
        values = {
            "FailedRecordCount": response["FailedRecordCount"],
            "SuccessfulRecordCount": len(response["Records"])
        }
        return json.dumps(values)
        # return json.dumps(response)

    def get_continuous(self, shard_id, batch_size):
        # AT_SEQUENCE_NUMBER | AFTER_SEQUENCE_NUMBER | AT_TIMESTAMP | TRIM_HORIZON | LATEST
        position = "LATEST"
        # position = "TRIM_HORIZON"
        iterator = self.client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=shard_id,
            ShardIteratorType=position)["ShardIterator"]
        i = 1
        j = 1
        latencies = []
        self.log.info("shard={}, iterator={}".format(shard_id, iterator))
        while 1 == 1:
            try:
                output = self.client.get_records(ShardIterator=iterator)
                # output = self.client.get_records(
                #     ShardIterator=iterator,
                #     Limit=batch_size)
                iterator = output["NextShardIterator"]
                for record in output["Records"]:
                    data = json.loads(record["Data"])
                    ingest_epoch = data["ingest_epoch"]
                    current_epoch = Util.get_epoch()
                    latency = (current_epoch - ingest_epoch) * 1000
                    latencies.append(latency)
                    values = {
                        # "ingest_epoch": ingest_epoch,
                        # "ingest_timestamp": Util.convert_timestamp(ingest_epoch),
                        # "current_epoch": current_epoch,
                        # "current_timestamp": Util.convert_timestamp(current_epoch),
                        "time": data["time"],
                        "volume": data["volume"],
                        "price": data["price"],
                        "latency_ms": latency
                    }
                    self.log.info("i={}, j={}, values={}".format(i, j, json.dumps(values)))
                    i = 1 if i == batch_size else i + 1
                    j += 1
                time.sleep(0.2)
            except self.client.exceptions.ProvisionedThroughputExceededException:
                self.log.error("ProvisionedThroughputExceededException")
                time.sleep(0.2)
            except KeyboardInterrupt:
                self.log.info("KeyboardInterrupt")
                total_measurements = len(latencies)
                average_latency = np.convolve(latencies, np.ones(total_measurements,)/total_measurements, mode='valid')
                self.log.info("processed_records={}, average_latency={}".format(total_measurements, average_latency))
                sys.exit(0)

    def get_vwap(self, shard_id, batch_size):
        # AT_SEQUENCE_NUMBER | AFTER_SEQUENCE_NUMBER | AT_TIMESTAMP | TRIM_HORIZON | LATEST
        position = "LATEST"
        # position = "TRIM_HORIZON"
        iterator = self.client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=shard_id,
            ShardIteratorType=position)["ShardIterator"]
        i = 1
        j = 1
        latencies = {}
        self.log.info("shard={}, iterator={}".format(shard_id, iterator))
        while 1 == 1:
            try:
                output = self.client.get_records(
                    ShardIterator=iterator,
                    Limit=batch_size)
                iterator = output["NextShardIterator"]
                for record in output["Records"]:
                    data = json.loads(record["Data"])
                    earliest_epoch = data["earliest_epoch"]
                    current_epoch = Util.get_epoch()
                    latency = (current_epoch - earliest_epoch) * 1000
                    symbol = data["symbol"]
                    if symbol not in latencies.keys():
                        latencies[symbol] = []
                    latencies[symbol].append(latency)
                    values = {
                        "symbol": symbol,
                        "vwap": data["vwap"],
                        "latency_ms": latency
                    }
                    self.log.info("i={}, j={}, values={}".format(i, j, json.dumps(values)))
                    i = 1 if i == batch_size else i + 1
                    j += 1
                time.sleep(0.2)
            except self.client.exceptions.ProvisionedThroughputExceededException:
                self.log.error("ProvisionedThroughputExceededException")
                time.sleep(0.2)
            except KeyboardInterrupt:
                self.log.info("KeyboardInterrupt")
                for symbol in latencies:
                    total_measurements = len(latencies[symbol])
                    average_latency = np.convolve(latencies[symbol], np.ones(total_measurements,)/total_measurements, mode='valid')
                    self.log.info("symbol={}, processed_records={}, average_latency_ms={}".format(symbol, total_measurements, average_latency))
                sys.exit(0)
