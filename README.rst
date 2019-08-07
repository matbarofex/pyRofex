Welcome to pyRofex's Documentation
===================================

Overview
--------
*pyRofex* is a python library that allows interactions with ROFEX's Rest and Websocket APIs.

The library is designed to avoid developers hours of research and coding needed to connect with ROFEX APIs, so they could focused on the important part of their software.

Although, we recommend to take a look at the official `API documentation <http://api.primary.com.ar/docs/Primary-API.pdf>`_ to get familiarize with the API Responses and functionality.

Installing
----------
*pyRofex* is avilable at Python Package Index (PyPI) repository. Install and update using `pip <https://pip.pypa.io/en/stable/quickstart/>`_\ :

.. code-block:: python

   pip install -U pyRofex

Features
--------

This sections describe the functionality and components of the library.

Available methods
^^^^^^^^^^^^^^^^^

Initialization
~~~~~~~~~~~~~~

Before you start using the library, you need to initialize the environment that you want to connect with.

Functions
"""""""""
* **initialize**: Initialize the specified environment. Set the default user, password and account for the environment.
* **set_default_environment**: Set default environment. The default environment that is going to be used when no environment is specified.

Rest
~~~~

The library provides functions to make requests to the REST API and return the corresponding response.

Functions
"""""""""

* **get_segments**\ : gets a list of valid segments.
* **get_all_instruments**\ : gets a list of all available instruments.
* **get_detailed_instruments**\ : gets a detailed list of all available instruments.
* **get_market_data**\ : gets market data information for an instrument.
* **get_trade_history**\ : gets a list of historic trades for an instrument.
* **send_order**\ : sends a new order to the Market.
* **cancel_order**\ : cancels an order.
* **get_order_status**\ : gets the status of the specified order.
* **get_all_orders_status**\ : gets the status of all the orders associated with an account.

..

  *All functions return a dict of the JSON response.*


Websocket
~~~~~~~~~

The library allows users to start a connection to the websocket API. The connection will be monitored by a separated thread, so its very important to set the proper handlers to process new incoming messages.

Functions
"""""""""

* **init_websocket_connection**\ : configure the Websocket Client with the handlers and then start a Websocket connection with API.
* **close_websocket_connection**\ : close the connection with the API.
* **market_data_subscription**\ : sends a Market Data Subscription Message through the connection.
* **order_report_subscription**\ : sends an Order Report Subscription Message through the connection.
* **add_websocket_market_data_handler** \**: adds a new Market Data handler to the Websocket Client. This handler is going to be call when a new Market Data Message is received.
* **add_websocket_order_report_handler** \**: adds a new Order Report handler to the Websocket Client. This handler is going to be call when a new Order Report Message is received.
* **add_websocket_error_handler** \**: adds a new Error handler to the Websocket Client. This handler is going to be call when a new Error Message is received.
* **set_websocket_exception_handler**: sets an exception handler to the Websocket Client. This handler is going to be called when an Exception occurred in the client.

** **handlers** are pythons functions that will be call whenever the specific event occurred.

Enumerations
^^^^^^^^^^^^

The library also provides some enumerations to help developers avoid errors and improve readability. Next, you have the list of available enums:

* **Environment**: Identifies the environment to use. (REMARKET: Demo environment; LIVE: Production environment)
* **MarketDataEntry**: Identifies market data entries for an instrument.
* **Market**: Market ID associated to the instruments.
* **OrderType**: Identifies the different order types.
* **Side**\ : Identifies the side of an order.
* **TimeInForce**: Time modifier of the order that defines the time the order will be active.

How to use it
-------------

Once the library is install, we import and initialize it.

The initialization sets the user, password and account to the environment specified. Then, trys to authenticate with the given user/password.

If the authentication fails, an ApiException is raised.

Finally, sets the environment as the default one. (you can change it with the set_default_environment function)

.. code-block:: python

   import pyRofex

   # Set the the parameter for the REMARKET environment
   pyRofex.initialize(user="sampleUser",
                      password="samplePassword",
                      account="sampleAccount",
                      environment=pyRofex.Environment.REMARKET)


Rest
^^^^
.. code-block:: python

   # Makes a request to the Rest API and get the last price
   # Use the MarketDataEntry enum to specify the data
   pyRofex.get_market_data(ticker="DODic19",
                           entries=[pyRofex.MarketDataEntry.LAST])

   # Gets all segments
   pyRofex.get_segments()

   # Gets available instruments list
   pyRofex.get_all_instruments()

   # Gets detailed instruments list
   pyRofex.get_detailed_instruments()

   # Get all order report for the configured account
   pyRofex.get_all_orders_status()

   # Gets historic trades
   pyRofex.get_trade_history(ticker="DOJun19",
                             start_date="2018-12-01",
                             end_date="2019-01-10")

   # Sends a Limit order to the market
   order = pyRofex.send_order(ticker="DODic19",
                              side=pyRofex.Side.BUY,
                              size=10,
                              price=55.8,
                              order_type=pyRofex.OrderType.LIMIT)

   # Gets the last order status for the previous order
   pyRofex.get_order_status(order["order"]["clientId"])

   # Cancels the previous order
   cancel_order = pyRofex.cancel_order(order["order"]["clientId"])

   # Checks the order status of the cancellation order
   pyRofex.get_order_status(cancel_order["order"]["clientId"])

Websocket
^^^^^^^^^

.. code-block:: python

   # First we define the handlers that will process the messages and exceptions.
   def market_data_handler(message):
       print("Market Data Message Received: {0}".format(message))
   def order_report_handler(message):
       print("Order Report Message Received: {0}".format(message))
   def error_handler(message):
       print("Error Message Received: {0}".format(message))
   def exception_handler(e):
       print("Exception Occurred: {0}".format(e.message))

   # Initiate Websocket Connection
   pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                     order_report_handler=order_report_handler,
                                     error_handler=error_handler,
                                     exception_handler=exception_handler)

   # Instruments list to subscribe
   instruments = ["DONov19", "DODic19"]
   # Uses the MarketDataEntry enum to define the entries we want to subscribe to
   entries = [pyRofex.MarketDataEntry.BIDS,
              pyRofex.MarketDataEntry.OFFERS,
              pyRofex.MarketDataEntry.LAST]

   # Subscribes to receive market data messages **
   pyRofex.market_data_subscription(tickers=instruments,
                                    entries=entries)

   # Subscribes to receive order report messages (default account will be used) **
   pyRofex.order_report_subscription()

** Every time a new message is received, the correct handler will be call.

Official API Documentation
==========================

For more detailed information about ROFEX Rest and Websocket APIs go to the `Primary API Documentation <http://api.primary.com.ar/docs/Primary-API.pdf>`_.

Acknowledgements
================

Development of this software was driven by
`Primary <https://www.primary.com.ar/>`_ as part of an Open Source
initiative of `Grupo Rofex <https://www.rofex.com.ar/>`_.

Author/Maintainer
-----------------

* `Franco Zanuso <https://github.com/fzanuso>`_