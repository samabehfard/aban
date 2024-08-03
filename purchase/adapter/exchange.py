class ExchangeAdapter:
    def __init__(self):
        ...

    def check_buy_was_success(self, result):
        ...
        is_success = True
        return is_success

    def buy_from_exchange(self, name, count):
        try:
            ...
            is_success = True
        except:
            is_success = False
        return is_success
