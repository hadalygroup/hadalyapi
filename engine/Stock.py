class Stock:
    def __init__(self, data):
        self.price = data['close'][0]
        self.close_time = data['close_time'][0]