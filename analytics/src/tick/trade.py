import json


class Trade:
    def __init__(self, symbol, payload):
        self.symbol = symbol
        self.payload = payload
        self.date = payload[0]
        self.time = payload[1]
        self.price = payload[2]
        self.volume = payload[3]
        self.exchange_code = payload[4]
        self.sales_condition = payload[5]

    def __repr__(self):
        return self.payload

    def __str__(self):
        values = {
            'symbol': self.symbol,
            'date': self.date,
            'time': self.time,
            'price': self.price,
            'volume': self.volume
        }
        return json.dumps(values)
