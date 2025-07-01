from src.data_object.trade_order import MarketTradeOrder
from src.utils import logger


def test_place_market_order_with_stop_loss_and_take_profit(web):
    logger.info("Step 1: Get live buy price")
    live_buy_price = float(web.trade_page.place_order.get_live_buy_price())

    logger.info("Step 2: Fill in buy order info")
    web.trade_page.place_order.swap_to_size()
    web.trade_page.place_order.swap_to_units()
