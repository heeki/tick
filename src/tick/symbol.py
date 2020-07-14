import json


class Symbol:
    def __init__(self, payload):
        self.payload = payload
        self.symbol = self.payload[0]
        self.company_name = self.payload[2]
        self.company_id = self.payload[8]

    def __repr__(self):
        return self.payload

    def __str__(self):
        values = {
            'symbol': self.symbol,
            'company_name': self.company_name,
            'company_id': self.company_id
        }
        return json.dumps(values)

