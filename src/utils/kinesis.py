import boto3
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
        return values

    def get_iterator(self, shard, position):
        return self.client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=shard,
            ShardIteratorType=position)["ShardIterator"]

    def get_records(self, iterator, batch_size):
        try:
            return self.client.get_records(
                ShardIterator=iterator,
                Limit=batch_size)
        except self.client.exceptions.ProvisionedThroughputExceededException:
            self.log.error("ProvisionedThroughputExceededException")
            time.sleep(0.2)
