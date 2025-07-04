from src.data_object.trade_order import MarketTradeOrder
from src.enums.order_enum import OrderSide, VolumeType
from src.utils import logger
from src.utils.assert_util import verify
from src.utils.string_util import format_number_string


def test_place_market_order_with_stop_loss_and_take_profit(web, symbol):
    logger.info(f"Step 1: Select {symbol!r}")
    web.trade_page.select_symbol(symbol)

    logger.info("Step 2: Get live buy price")
    live_buy_price = round(float(format_number_string(web.trade_page.place_order.get_live_buy_price())), ndigits=1)

    logger.info("Step 3: Fill in buy order info")
    trade_order = MarketTradeOrder(OrderSide.BUY, {VolumeType.UNITS: 1}, live_buy_price - 5, live_buy_price + 5)
    web.trade_page.place_order.place_an_order(trade_order, False)

    verify(
        web.trade_page.trade_confirmation_popup.get_confirmation_symbol() == symbol,
        f"Verify {symbol!r} is correct in confirmation popup"
    )

    actual_trade_order_info = web.trade_page.trade_confirmation_popup.get_confirmation_trade_order_info()
    expected_values = [
        ("order_side", trade_order.order_side),
        ("volume", str(trade_order.get_volume_value())),
        ("stop_loss", f"{trade_order.stop_loss:,.1f}"),
        ("take_profit", f"{trade_order.take_profit:,.1f}"),
    ]
    for i, (field_name, expected) in enumerate(expected_values):
        verify(
            actual_trade_order_info[i] == expected,
            f"Verify {field_name} '{expected}' is correct in confirmation popup"
        )

    server_time = web.home_page.get_server_time()

    logger.info("Step 4: Click 'Confirm'")
    web.trade_page.trade_confirmation_popup.confirm()
    web.trade_page.wait_for_loading_complete()

    logger.info("Step 5: Focus on 'Open Position' area")
