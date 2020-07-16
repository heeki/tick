import json


def success(body):
    return build_response(200, body)


def failure(body):
    return build_response(500, body)


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
