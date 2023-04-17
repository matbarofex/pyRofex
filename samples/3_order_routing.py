# -*- coding: utf-8 -*-
"""
    Sample Module.

    Example of order routing using the library.

    The code show how to send, cancel and get the status of an order using pyRofex.

    Go to the official Documentation to check the API Responses.

    Steps:
    1-Initialize the environment
    2-Get the best bid offer in the market for DLR/MAR22
    3-Send a Buy Limit Order for DLR/MAR22 with the same price as the best bid
    4-Check the order status
    5-If order status is PENDING_NEW then we keep checking the status until the market accept or reject the order
    6-If the status is NEW, cancel the order
"""
import time

import pyRofex

# 1-Initialize the environment
pyRofex.initialize(user="XXXXXXX",
                   password="XXXXXXX",
                   account="XXXXXXX",
                   environment=pyRofex.Environment.REMARKET)

# 2-Get the best bid offer in the market for DLR/MAR22
md = pyRofex.get_market_data(ticker="DLR/MAR22",
                             entries=[pyRofex.MarketDataEntry.BIDS])

# Print the response
print("Market Data Response: {0}".format(md))

# 3-Send a Buy Limit Order for DLR/ENE24 with the same price as the best bid
order = pyRofex.send_order(ticker="DLR/ENE24",
                           side=pyRofex.Side.BUY,
                           size=10,
                           price=md["marketData"]["BI"][0]["price"],
                           order_type=pyRofex.OrderType.LIMIT)

# Print the response
print("Send Order Response: {0}".format(order))

# 4-Check the order status
order_status = pyRofex.get_order_status(order["order"]["clientId"])

# Print the response
print("Order Status Response: {0}".format(order_status))

# 5-If order status is PENDING_NEW then we keep checking the status until
# the market accept or reject the order or timeout is reach
timeout = 5 # Time out 5 seconds

while order_status["order"]["status"] == "PENDING_NEW" and timeout > 0:
    time.sleep(1)
    order_status = pyRofex.get_order_status(order["order"]["clientId"])

    # Print Order Status
    print("Recheck Order Status Response: {0}".format(order_status))

    timeout = timeout - 1


# 6-If the status is NEW, cancel the order
if order_status["order"]["status"] == "NEW":
    # Cancel Order
    cancel_order = pyRofex.cancel_order(order["order"]["clientId"])

    # Print the response
    print("Cancel Order Response: {0}".format(cancel_order))

    # Check cancel order status
    cancel_order_status = pyRofex.get_order_status(cancel_order["order"]["clientId"])
    print("Cancel Order Status Response: {0}".format(cancel_order_status))

    # Check original order status
    original_order_status = pyRofex.get_order_status(order["order"]["clientId"])
    print("Original Order Status Response: {0}".format(original_order_status))
