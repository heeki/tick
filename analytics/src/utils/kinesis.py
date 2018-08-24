import boto3
import json


class Kinesis:
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.client = boto3.client('kinesis')

    def batch_put(self, records):
        response = self.client.put_records(Records=records, StreamName=self.stream_name)
        values = {
            "FailedRecordCount": response["FailedRecordCount"],
            "SuccessfulRecordCount": len(response["Records"])
        }
        return json.dumps(values)
        # return json.dumps(response)


