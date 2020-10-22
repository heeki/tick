import base64
import json
import os
import uuid


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
        'isBase64Encoded': False,
        'statusCode': code,
        'headers': headers,
        'body': body
    }
    return response


# function: lambda invoker handler
def handler(event, context):

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

    payload = "success" if status == 200 else "failure"
    response = build_response(status, payload)

    return response


# initialization, mapping
sandbox_id = uuid.uuid1()
