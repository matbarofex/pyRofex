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
SEND_ORDER = '{{"type":"no","product":{{"marketId":"ROFX","symbol":"{ticker}"}},"price":"{price}","quantity":"{size}",\
                "side":"{side}","account":"{account}", "allOrNone":"{all_or_none}", "clOrdId":"{id}"}}'
