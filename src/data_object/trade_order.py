from src.enums.place_order import OrderType, OrderSide, VolumeType


class TradeOrder:
    def __init__(self, order_type: OrderType, order_side: OrderSide, volume: dict, stop_loss, take_profit):
        self.order_type = order_type
        self.order_side = order_side
        self.volume = volume  # Ex: {VolumeType.UNITS: 1}
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    @property
    def to_json(self):
        return self.__dict__

    def is_volume_size(self):
        return VolumeType.SIZE in self.volume

    def is_volume_units(self):
        return not self.is_volume_size()

    def get_volume_value(self):
        k = VolumeType.UNITS if self.is_volume_units() else VolumeType.SIZE
        return self.volume[k]


class MarketTradeOrder(TradeOrder):
    def __init__(self, order_side, volume, stop_loss, take_profit):
        super().__init__(OrderType.MARKET, order_side, volume, stop_loss, take_profit)


class LimitTradeOrder(TradeOrder):
    def __init__(self, order_side, volume, price, stop_loss, take_profit, expiry):
        super().__init__(OrderType.LIMIT, order_side, volume, stop_loss, take_profit)
        self.price = price
        self.expiry = expiry


class StopTradeOrder(TradeOrder):
    def __init__(self, order_side, volume, price, stop_loss, take_profit, expiry):
        super().__init__(OrderType.LIMIT, order_side, volume, stop_loss, take_profit)
        self.price = price
        self.expiry = expiry
