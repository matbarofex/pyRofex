# -*- coding: utf-8 -*-
"""
    pyRofex.components.messages

    Defines APIs messages templates
"""

# Template for a Market Data Subscription message
MARKET_DATA_SUBSCRIPTION = '{{"type":"smd","level":1,"depth":{depth},"entries":[{entries}],"products":[{symbols}]}}'
# Template for an Order Subscription message
ORDER_SUBSCRIPTION = '{{"type":"os","account":{{"id":"{a}"}},"snapshotOnlyActive":{snapshot}}}'
# Template to specify an instrument in a market data subscription message
INSTRUMENT = '{{"symbol":"{ticker}","marketId":"{market}"}}'
# Template to insert a Double Quote
DOUBLE_QUOTES = '"{item}"'
# Template for sending an Order via WebSocket
SEND_ORDER = '{{"type":"no","product":{{"marketId":"{market}","symbol":"{ticker}"}},"quantity":"{size}",' \
             '"ordType":"{order_type}","side":"{side}","account":"{account}","allOrNone":"{all_or_none}",' \
             '"timeInForce":"{time_force}"{optional_params}}}'
# Template to cancel an Order via WebSocket
CANCEL_ORDER = '{{"type":"co", "clientId":"{id}", "proprietary":"{p}"}}'
# Template for Optional order parameters
ICEBERG = ',"iceberg":"{iceberg}","displayQuantity":"{display_quantity}"'
GOOD_TILL_DATE = ',"expireDate":"{expire_date}"'
WS_CLIENT_ORDER_ID = ',"wsClOrdId":"{wsClOrdID}"'
PRICE = ',"price":"{price}"'
