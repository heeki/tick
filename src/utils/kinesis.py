import boto3
import json
import time
import sys
from utils.util import Util


class Kinesis:
    def __init__(self, stream_name, consumer_name=None):
        self.stream_name = stream_name
        self.client = boto3.client("kinesis")
        self.log = Util.get_logger("kinesis")
        self.consumer_name = consumer_name if consumer_name is not None else "default"
        self.stream_arn = self.client.describe_stream(StreamName=stream_name)["StreamDescription"]["StreamARN"]

    # efo functions
    def __enter__(self):
        self.log.info("registering stream consumer with {} ({})".format(self.stream_name, self.stream_arn))
        try:
            response = self.client.register_stream_consumer(
                StreamARN=self.stream_arn,
                ConsumerName=self.consumer_name
            )
            self.consumer_arn = response["Consumer"]["ConsumerARN"]
        except self.client.exceptions.ResourceInUseException:
            self.log.error("consumer name in use: {}".format(self.consumer_name))
            sys.exit(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log.info("deregistering stream consumer ({}) from {}".format(self.consumer_arn, self.stream_name))
        self.client.deregister_stream_consumer(
            StreamARN=self.stream_arn,
            ConsumerName=self.consumer_name,
            ConsumerARN=self.consumer_arn
        )

    def get_stream_consumers(self):
        response = self.client.list_stream_consumers(
            StreamARN=self.stream_arn
        )
        return response["Consumers"]

    def subscribe(self, shard):
        self.log.info("need to make a call to the java implementation")
        # response = self.client.subscribe_to_shard(
        #     ConsumerARN=self.consumer_arn,
        #     ShardId=shard
        # )
        # return response

    # standard functions
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
