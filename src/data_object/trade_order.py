from src.enums.place_order import OrderType, VolumeType


class TradeOrder:
    def __init__(self, order_type, volume: VolumeType, stop_loss, take_profit):
        self.order_type = order_type
        self.volume = volume
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    @property
    def to_json(self):
        return self.__dict__


class MarketTradeOrder(TradeOrder):
    def __init__(self, volume, stop_loss, take_profit):
        super().__init__(OrderType.MARKET, volume, stop_loss, take_profit)


class LimitTradeOrder(TradeOrder):
    def __init__(self, volume, price, stop_loss, take_profit, expiry):
        super().__init__(OrderType.LIMIT, volume, stop_loss, take_profit)
        self.price = price
        self.expiry = expiry


class StopTradeOrder(TradeOrder):
    def __init__(self, volume, price, stop_loss, take_profit, expiry):
        super().__init__(OrderType.LIMIT, volume, stop_loss, take_profit)
        self.price = price
        self.expiry = expiry
