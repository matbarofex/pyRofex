# -*- coding: utf-8 -*-
"""
    pyRofex: Python connector for ROFEX Rest and Websocket APIs.

    This modules expose functions and enumerations of the library.
"""
from .service import initialize
from .service import set_default_environment
from .service import _set_environment_parameter

from .service import init_websocket_connection
from .service import close_websocket_connection
from .service import market_data_subscription
from .service import order_report_subscription
from .service import add_websocket_market_data_handler
from .service import remove_websocket_market_data_handler
from .service import add_websocket_order_report_handler
from .service import remove_websocket_order_report_handler
from .service import add_websocket_error_handler
from .service import remove_websocket_error_handler
from .service import set_websocket_exception_handler

from .service import get_segments
from .service import get_all_instruments
from .service import get_detailed_instruments
from .service import get_instrument_details
from .service import get_market_data
from .service import get_trade_history
from .service import send_order
from .service import cancel_order
from .service import get_order_status
from .service import get_all_orders_status

from .components.enums import Environment
from .components.enums import MarketDataEntry
from .components.enums import Market
from .components.enums import OrderType
from .components.enums import Side
from .components.enums import TimeInForce

__version__ = "0.3.0"
