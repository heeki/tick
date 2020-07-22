import base64
import json
import os
import uuid
from utils.response import success, failure


# function: initialization
def initialization():
    # print("ENV1={}".format(env1))
    # print("ENV2={}".format(env2))
    pass


# function: lambda invoker handler
def handler(event, context):
    # print("event={}".format(json.dumps(event)))
    # print("request_id={}".format(context.aws_request_id))

    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"])
        partition_key = record["kinesis"]["partitionKey"]
        output = {
            "request_id": context.aws_request_id,
            "sandbox_id": str(sandbox_id),
            "partition_key": partition_key
        }

        try:
            output["payload"] = json.loads(payload)
            status = 200
        except json.JSONDecodeError:
            output["payload"] = payload.decode("utf-8")
            status = 500
        print(json.dumps(output))

    if status == 200:
        response = success("success")
    else:
        response = failure("failure")

    return response


# initialization, mapping
env1 = os.environ['ENV1']
env2 = os.environ['ENV2']
sandbox_id = uuid.uuid1()
initialization()
