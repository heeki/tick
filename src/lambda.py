import base64
import json
import os
import uuid

# initialization, mapping
sandbox_id = uuid.uuid1()

# helper functions
def build_response(code, body, include_headers=False):
    # headers for cors
    if include_headers:
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        }
    else:
        headers = {}

    # lambda proxy integration
    response = {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": headers,
        "body": body
    }
    return response

# function: lambda invoker handler
def handler(event, context):
    exclude = ["Records"]
    print(json.dumps({x: event[x] for x in event if x not in exclude}))

    if "state" in event and "count" in event["state"]:
        count = event["state"]["count"]
    else:
        count = 0
    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"])
        partition_key = record["kinesis"]["partitionKey"]
        count += 1
        output = {
            "request_id": context.aws_request_id,
            "sandbox_id": str(sandbox_id),
            "partition_key": partition_key
        }

        try:
            output["payload"] = json.loads(payload)
        except json.JSONDecodeError:
            output["payload"] = payload.decode("utf-8")
        # print(json.dumps(output))

    response = {
        "state": {
            "count": count
        }
    }
    print(json.dumps(response))

    return response
