# -*- coding: utf-8 -*-
"""
    Sample Module.

    Example of order routing using websocket API.

    The code show how to initialize the connection,
    subscribe to receive order reports for a valid account,
    send an order to the market and if the status is pending_new then
    we cancel the order, and finally close the connection.

    Go to the official Documentation to check the API Responses.

    Steps:
    1-Initialize the environment
    2-Defines the handlers that will process the messages and exceptions.
    3-Initialize Websocket Connection with the handlers
    4-Subscribes to receive order report for the default account
    5-Send an order via websocket message then check that order_report_handler is called
    6-Handler will validate if the order is in the correct state (pending_new)
    6.1-We cancel the order using the websocket connection
    7-Handler will receive an Order Report indicating that the order is cancelled (will print it)
    8-Wait 5 sec then close the connection
"""
import time

import pyRofex

# 1-Initialize the environment
pyRofex.initialize(user="XXXXXXX",
                   password="XXXXXXX",
                   account="XXXXXXX",
                   environment=pyRofex.Environment.REMARKET)


# 2-Defines the handlers that will process the messages and exceptions.
def order_report_handler(message):
    print("Order Report Message Received: {0}".format(message))
    # 6-Handler will validate if the order is in the correct state (pending_new)
    if message["orderReport"]["status"] == "NEW":
        # 6.1-We cancel the order using the websocket connection
        print("Send to Cancel Order with clOrdID: {0}".format(message["orderReport"]["clOrdId"]))
        pyRofex.cancel_order_via_websocket(message["orderReport"]["clOrdId"])

    # 7-Handler will receive an Order Report indicating that the order is cancelled (will print it)
    if message["orderReport"]["status"] == "CANCELLED":
        print("Order with ClOrdID '{0}' is Cancelled.".format(message["orderReport"]["clOrdId"]))


def error_handler(message):
    print("Error Message Received: {0}".format(message))


def exception_handler(e):
    print("Exception Occurred: {0}".format(e.msg))


# 3-Initialize Websocket Connection with the handlers
pyRofex.init_websocket_connection(order_report_handler=order_report_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)

# 4-Subscribes to receive order report for the default account
pyRofex.order_report_subscription()

# 5-Send an order via websocket message then check that order_report_handler is called
pyRofex.send_order_via_websocket(ticker="DLR/ENE24",
                                 side=pyRofex.Side.BUY,
                                 size=100,
                                 order_type=pyRofex.OrderType.LIMIT,
                                 price=210)  # validate correct price

# 8-Wait 5 sec then close the connection
time.sleep(5)
pyRofex.close_websocket_connection()
