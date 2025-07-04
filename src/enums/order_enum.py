class OrderType:
    MARKET = "Market"
    LIMIT = "Limit"
    STOP = "Stop"


class VolumeType:
    SIZE = "Size"
    UNITS = "Units"


class OrderSide:
    BUY = "Buy"
    SELL = "Sell"


class AssetOrderType:
    OPEN_POSITIONS = "Open Positions"
    PENDING_ORDERS = "Pending Orders"
    ORDER_HISTORY = "Order History"