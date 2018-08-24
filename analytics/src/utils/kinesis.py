import boto3
import json
import time
import sys


class Kinesis:
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.client = boto3.client('kinesis')

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

    def get_continuous(self, shard, log):
        # AT_SEQUENCE_NUMBER | AFTER_SEQUENCE_NUMBER | AT_TIMESTAMP | TRIM_HORIZON | LATEST
        position = "LATEST"
        iterator = self.client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=shard,
            ShardIteratorType=position)["ShardIterator"]
        while 1 == 1:
            try:
                output = self.client.get_records(
                    ShardIterator=iterator,
                    Limit=200)
                iterator = output["NextShardIterator"]
                for record in output["Records"]:
                    log.info(json.loads(record["Data"])["ingest_epoch"])
                time.sleep(0.2)
            except self.client.exceptions.ProvisionedThroughputExceededException:
                log.error("ProvisionedThroughputExceededException")
                time.sleep(0.2)
            except KeyboardInterrupt:
                log.info("KeyboardInterrupt")
                sys.exit(0)




