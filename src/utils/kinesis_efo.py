import boto3
import sys
from utils.util import Util


class KinesisEnhanced:
    def __init__(self, stream_name, consumer_name):
        self.stream_name = stream_name
        self.consumer_name = consumer_name
        self.client = boto3.client('kinesis')
        self.log = Util.get_logger("kinesis-enhanced")

        response = self.client.describe_stream(
            StreamName=self.stream_name
        )
        self.stream_arn = response["StreamDescription"]["StreamARN"]

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

    def subscribe(self, shard_id):
        self.log.info("need to make a call to the java implementation")
        # response = self.client.subscribe_to_shard(
        #     ConsumerARN=self.consumer_arn,
        #     ShardId=shard_id
        # )
        # return response
