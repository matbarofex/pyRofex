# -*- coding: utf-8 -*-
"""
    pyRofex.service

    All the library exposed functionality
"""
from inspect import getargspec

from .clients.rest_rfx import RestClient
from .clients.websocket_rfx import WebSocketClient
from .components import globals
from .components.exceptions import ApiException
from .components.enums import Environment
from .components.enums import MarketDataEntry
from .components.enums import TimeInForce
from .components.enums import Market


# ######################################################
# ##            Initialization functions              ##
# ######################################################


def initialize(user, password, account, environment, proxies=None):
    """ Initialize the specified environment.

     Set the default user, password and account for the environment.

    :param user: the user used for authentication.
    :type user: str
    :param password: the password used for authentication.
    :type password: str
    :param account: user's default account.
    :type account: str
    :param environment: the environment that is gonna be initialized.
    :type environment: Environment (Enum)
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :type proxies: dict
    """
    _validate_environment(environment)
    _set_environment_parameters(user, password, account, environment, proxies)
    globals.environment_config[environment]["rest_client"] = RestClient(environment)
    globals.environment_config[environment]["ws_client"] = WebSocketClient(environment)
    set_default_environment(environment)


def set_default_environment(environment):
    """Set default environment.

    The environment that is gonna be used as default when it's not specified.

    Example: if we send an order using the send_order function and
    we do not specified and Environment, the order is going to be send to the default one.

    :param environment: the environment that is going to be set as default.
    :type environment: Environment
    """
    _validate_environment(environment)
    globals.default_environment = environment


def _set_environment_parameter(parameter, value, environment):
    """Set environment parameter.

    Set 'value' into the specified 'parameter' for the environment 'environment'.

    :param parameter: parameter of the environment to be set.
    :type parameter: string
    :param value: new value for the parameter.
    :type value: string
    :param environment: the environment to set the parameter.
    :type environment: Environment
    """
    environment = _validate_environment(environment)
    _validate_parameter(parameter, environment)
    globals.environment_config[environment][parameter] = value


def _set_environment_parameters(user, password, account, environment, proxies):
    """Configure the environment parameters into global configuration.

    Set the user, password and account into globals configuration.
    These variables are going to be used as the default parameters for the environment.

    :param user: the user used for authentication.
    :param password: the password used for authentication.
    :param account: user's default account.
    :param environment: the environment that is going to be configured.
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :type proxies: dict
    """
    globals.environment_config[environment]["user"] = user
    globals.environment_config[environment]["password"] = password
    globals.environment_config[environment]["account"] = account
    globals.environment_config[environment]["proxies"] = proxies


# ######################################################
# ##                REST functions                    ##
# ######################################################


def get_segments(environment=None):
    """Make a request to the API and get a list of valid segments.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param environment: The environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: A list of valid ROFEXs segments returned by the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Get the client for the environment and start the connection
    response = globals.environment_config[environment]["rest_client"].get_segments()
    return response


def get_all_instruments(environment=None):
    """Make a request to the API and get a list of all available instruments.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: A list of valid instruments returned by the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.get_all_instruments()


def get_detailed_instruments(environment=None):
    """Make a request to the API and get a detailed list of all available instruments.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: A list of valid instruments returned by the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.get_detailed_instruments()


def get_instrument_details(ticker, market=Market.ROFEX, environment=None):
    """Make a request to the API and get the details of the instrument.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param ticker: Instrument symbol to send in the request. Example: DODic19
    :type ticker: str
    :param market: Market ID related to the instrument. Default Market.ROFEX.
    :type market: Market (Enum).
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: Details of the instrument returned by the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.get_instrument_details(ticker, market)


def get_market_data(ticker, entries=None, depth=1, market=Market.ROFEX, environment=None):
    """Make a request to the API to get the Market Data Entries of the specified instrument.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param ticker: Instrument symbol to send in the request. Example: DODic19
    :type ticker: str
    :param entries: List of entries to send in the request. Default: all available entries.
    Example: [MarketDataEntry.BIDS, MarketDataEntry.OFFERS]
    :type entries: List of MarketDataEntry (Enum).
    :param depth: Specify the depth of the book to be request. Default: 1.
    :type depth: int
    :param market: Market ID related to the instrument. Default Market.ROFEX.
    :type market: Market (Enum).
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: Market Data response of the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    entries = _validate_market_data_entries(entries)

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.get_market_data(ticker, entries, depth, market)


def get_order_status(client_order_id, proprietary=None, environment=None):
    """Make a request to the API to get the status of the specified order.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param client_order_id: Client Order ID of the order.
    :type client_order_id: str
    :param proprietary: Proprietary of the order. Default None: environment default proprietary is used.
    :type proprietary: str
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: Order status response of the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Checks the proprietary and sets the default one if None is received.
    if proprietary is None:
        proprietary = globals.environment_config[environment]["proprietary"]

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.get_order_status(client_order_id, proprietary)


def send_order(ticker, size, order_type, side,
               market=Market.ROFEX,
               time_in_force=TimeInForce.DAY,
               account=None,
               price=None,
               cancel_previous=False,
               iceberg=False,
               expire_date=None,
               display_quantity=None,
               environment=None):
    """Make a request to the API that send a new order to the Market.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param ticker: Instrument symbol to send in the request. Example: DODic19.
    :type ticker: str
    :param size: Order size.
    :type size: int
    :param order_type: Order type. Example: OrderType.LIMIT.
    :type order_type: OrderType (Enum).
    :param side: Order side. Example: Side.BUY.
    :type side: Side (Enum).
    :param market: Market ID related to the instrument. Default Market.ROFEX.
    :type market: Market (Enum).
    :param time_in_force: Order modifier that defines the active time of the order. Default TimeInForce.Day.
    :type time_in_force: TimeInForce (Enum).
    :param account: Account to used. Default None: default account is used.
    :type account: str
    :param price: Order price. Default None: when no price is required.
    :type price: int
    :param cancel_previous: True: cancels actives orders that match with the account, side and ticker.
    False: send the order without cancelling previous ones. Useful for replacing old orders. Default: False.
    :type cancel_previous: boolean.
    :param iceberg: True: if it is an iceberg order. False: if it's not an iceberg order.
    :type iceberg: boolean.
    :param expire_date: Indicates the Expiration date for a GTD order. Example: 20170720.
    :type expire_date: str (Enum).
    :param display_quantity: Indicates the amount to be disclosed for GTD orders.
    :type display_quantity: int
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: Client Order ID and Proprietary of the order returned by the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    _validate_account(account, environment)

    # Checks the account and sets the default one if None is received.
    if account is None:
        account = globals.environment_config[environment]["account"]

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.send_order(ticker, size, order_type, side, account,
                             price, time_in_force, market, cancel_previous,
                             iceberg, expire_date, display_quantity)


def cancel_order(client_order_id, proprietary=None, environment=None):
    """Make a request to the API and cancel the order specified.

    The market will respond with a client order id, then you should verify the status of the request with this id.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param client_order_id: Client Order ID of the order.
    :type client_order_id: str
    :param proprietary: Proprietary of the order. Default None: environment default proprietary is used.
    :type proprietary: str
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: Client Order ID of cancellation request returned by the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Checks the proprietary and sets the default one if None is received.
    if proprietary is None:
        proprietary = globals.environment_config[environment]["proprietary"]

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.cancel_order(client_order_id,
                               proprietary)


def get_all_orders_status(account=None, environment=None):
    """Make a request to the API and get the status of all the orders associated with the account.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param account: Account associated with the orders. Default None: default account is used.
    :type account: str
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: List of all orders status associated with the user returned by the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    _validate_account(account, environment)

    # Checks the account and sets the default one if None is received.
    if account is None:
        account = globals.environment_config[environment]["account"]

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.get_all_orders_by_account(account)


def get_trade_history(ticker, start_date, end_date, market=Market.ROFEX, environment=None):
    """Makes a request to the API and get trade history for the instrument specified.

    For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    :param ticker: Instrument symbol to send in the request. Example: DODic19
    :type ticker: str
    :param start_date: Start date for the trades. Format: yyyy-MM-dd
    :type start_date: str
    :param end_date: End date for the trades. Format: yyyy-MM-dd
    :type end_date: str
    :param market: Market ID related to the instrument. Default Market.ROFEX.
    :type market: Market (Enum).
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    :return: List of trades returned by the API.
    :rtype: dict of JSON response.
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Get the client for the environment and make the request
    client = globals.environment_config[environment]["rest_client"]
    return client.get_trade_history(ticker, start_date, end_date, market)


# ######################################################
# ##              Websocket functions                 ##
# ######################################################


def init_websocket_connection(market_data_handler=None,
                              order_report_handler=None,
                              error_handler=None,
                              exception_handler=None,
                              environment=None):
    """Initialize the Websocket Client with the handlers and then start the connection with Primary Websocket API.

    A new thread is created in order to motorize the connection and check new incoming messages.

    :param market_data_handler: function called when a new Market Data Message is received. Default None.
    :type market_data_handler: callable.
    :param order_report_handler: function called when a new Order Report Message is received. Default None.
    :type order_report_handler: callable.
    :param error_handler: function called when an Error Message is received. Default None.
    :type error_handler: callable.
    :param exception_handler: function called when an Exception occurred in the client. Default None.
    :type exception_handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Gets the client for the environment
    client = globals.environment_config[environment]["ws_client"]

    # Checks handlers and adds the them into the client.
    if market_data_handler is not None:
        _validate_handler(market_data_handler)
        client.add_market_data_handler(market_data_handler)

    if order_report_handler is not None:
        _validate_handler(order_report_handler)
        client.add_order_report_handler(order_report_handler)

    if error_handler is not None:
        _validate_handler(error_handler)
        client.add_error_handler(error_handler)

    if exception_handler is not None:
        _validate_handler(error_handler)
        client.add_error_handler(exception_handler)

    # Initiates the connection with the Websocket API
    client.connect()


def close_websocket_connection(environment=None):
    """Close the connection with the API.

    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)

    # Gets the client for the environment
    client = globals.environment_config[environment]["ws_client"]

    # Close Websocket connection with the API
    client.close_connection()


def order_report_subscription(account=None, snapshot=True, handler=None, environment=None):
    """Send an Order Report Subscription Message through the connection.

    :param account: account that will be send in the message.
    Default None: default environment account is used.
    :type account: str.
    :param snapshot: True: old Order Reports won't be received; False: old Order Report will be received. Default True.
    :type snapshot: boolean.
    :param handler: function that is going to be call when a new Order Report Message is received. Default None.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    _validate_websocket_connection(environment)
    _validate_account(account, environment)

    # Checks the account and sets the default one if None is received.
    if account is None:
        account = globals.environment_config[environment]["account"]

    # Checks the handler, then validates and adds it into the client.
    if handler is not None:
        _validate_handler(handler)
        globals.environment_config[environment]["ws_client"].add_order_report_handler(handler)

    # Get the client for the environment and send the subscription message
    client = globals.environment_config[environment]["ws_client"]
    client.order_report_subscription(account, snapshot)


def market_data_subscription(tickers, entries, market=Market.ROFEX, handler=None, environment=None):
    """Send a Market Data Subscription Message through the connection.

    :param tickers: list of the the instruments to be subscribe.
    :type tickers: List of str.
    :param entries: List of market data entries that want to be received.
    Example: [MarketDataEntry.BIDS, MarketDataEntry.OFFERS]
    :type entries: List of MarketDataEntry (Enum).
    :param market: Market id associated to the tickers. Default Market.ROFEX.
    :type market: Market (Enum).
    :param handler: function that is going to be call when a new Market Data Message is received. Default None.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    _validate_websocket_connection(environment)
    _validate_market_data_entries(entries)

    # Checks the handler, then validates and adds it into the client.
    if handler is not None:
        _validate_handler(handler)
        globals.environment_config[environment]["ws_client"].add_market_data_handler(handler)

    # Get the client for the environment and send the subscription message
    client = globals.environment_config[environment]["ws_client"]
    client.market_data_subscription(tickers, entries, market)


def add_websocket_market_data_handler(handler, environment=None):
    """Adds a new Market Data handler to the Websocket Client.

    This handler is going to be call when a new Market Data Message is received.

    :param handler: function that is going to be call when a new Market Data Message is received.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    _validate_handler(handler)

    # Get the client for the environment and adds the handler
    client = globals.environment_config[environment]["ws_client"]
    client.add_market_data_handler(handler)


def add_websocket_order_report_handler(handler, environment=None):
    """Adds a new Order Report handler to the Websocket Client.

    This handler is going to be call when a new Order Report Message is received.

    :param handler: function that is going to be call when a new Order Report Message is received.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    _validate_handler(handler)

    # Get the client for the environment and adds the handler
    client = globals.environment_config[environment]["ws_client"]
    client.add_order_report_handler(handler)


def add_websocket_error_handler(handler, environment=None):
    """Adds a new Error handler to the Websocket Client.

    This handler is going to be call when a new Error Message is received.

    :param handler: function that is going to be call when a new Error Message is received.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    _validate_handler(handler)

    # Get the client for the environment and adds the handler
    client = globals.environment_config[environment]["ws_client"]
    client.add_error_handler(handler)


def remove_websocket_market_data_handler(handler, environment=None):
    """Removes the Market Data handler from the Websocket Client.

    :param handler: function to be removed from the handlers list.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Get the client for the environment and adds the handler
    client = globals.environment_config[environment]["ws_client"]
    client.remove_market_data_handler(handler)


def remove_websocket_order_report_handler(handler, environment=None):
    """Removes the Order Report handler from the Websocket Client.

    :param handler: function to be removed from the handlers list.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Get the client for the environment and adds the handler
    client = globals.environment_config[environment]["ws_client"]
    client.remove_order_report_handler(handler)


def remove_websocket_error_handler(handler, environment=None):
    """Removes the Error handler from the Websocket Client.

    :param handler: function to be removed from the handlers list.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)

    # Get the client for the environment and adds the handler
    client = globals.environment_config[environment]["ws_client"]
    client.remove_error_handler(handler)


def set_websocket_exception_handler(handler, environment=None):
    """Set the Exception handler to the Websocket Client.

    This handler is going to be called when an Exception occurred in the client.

    :param handler: function called when Exception is raised.
    :type handler: callable.
    :param environment: Environment used. Default None: the default environment is used.
    :type environment: Environment (Enum).
    """

    # Validations
    environment = _validate_environment(environment)
    _validate_initialization(environment)
    _validate_handler(handler)

    # Get the client for the environment and adds the handler
    client = globals.environment_config[environment]["ws_client"]
    client.set_exception_handler(handler)


# ######################################################
# ##              Validations functions               ##
# ######################################################


def _validate_parameter(parameter, environment):
    """Check if the parameter exist for the environment.

    If parameter does not exist then raise an ApiException.

    :param parameter: Parameter to be validated.
    :type parameter: string
    :param environment: Environment to check for parameter.
    :type environment: Environment (Enum).
    """
    if parameter not in globals.environment_config[environment]:
        raise ApiException("Invalid parameter '%s' for the environment %s." % (parameter, environment.name))


def _validate_environment(environment):
    """Check if the environment sent is an instance of the Environment enum.

    If None environment is send then check if default environment is set.

    If none environment is set or the environment is not an instance of Environment raise an ApiException.

    :param environment: Environment to be validated.
    :type environment: Environment (Enum).
    :return: the environment to be used.
    :rtype: Environment (Enum).
    """
    if environment is None:
        if globals.default_environment is None:
            raise ApiException("Environment not specify.")
        else:
            environment = globals.default_environment

    if not isinstance(environment, Environment):
        raise ApiException("Invalid Environment.")

    return environment


def _validate_initialization(environment):
    """Validate if the environment is initialized. If not it raised an ApiException.

    :param environment: Environment used.
    :type environment: Environment (Enum).
    """
    if not globals.environment_config[environment]["initialized"]:
        raise ApiException("The Environment is not initialized.")


def _validate_market_data_entries(entries):
    """Validate if the list of entries are instance of the MarketDataEntry enum.

    If the entry list is None or Empty, the full list of MarketDataEntry will be return.

    :param entries: list of entries to be validated.
    :type entries: list of MarketDataEntry (Enum).
    :return: a list of validated MarketDataEntry.
    :rtype: List of MarketDataEntry (Enum).
    """
    if entries is None:
        entries = [entry for entry in MarketDataEntry]
    else:
        for entry in entries:
            if not isinstance(entry, MarketDataEntry):
                raise ApiException("Invalid Market Data Entry: " + str(entry))

    return entries


def _validate_websocket_connection(environment):
    """Checks if the websocket connection was established.

    If the client is not connected then tries to initialize the connection.

    :param environment: Environment used.
    :type environment: Environment (Enum).
    """
    if not globals.environment_config[environment]["ws_client"].is_connected():
        globals.environment_config[environment]["ws_client"].connect()


def _validate_account(account, environment):
    """Checks if the account if None account is send, then the environment account
    must be set, if not raised an ApiException.

    :param account: account to be validated.
    :type account: str.
    :param environment: Environment used.
    :type environment: Environment (Enum).
    """
    if account is None and globals.environment_config[environment]["account"] is None:
        raise ApiException("Account not specified.")


def _validate_handler(handler):
    """ Checks if the handler is callable and that can received one argument, if not raised an ApiException.

    :param handler: handler to be validated.
    :type handler: callable.
    """

    # Checks if it is callable
    if not callable(handler):
        raise ApiException("Handler '{handler}' is not callable.".format(handler=handler))

    # Checks if function can receive an argument
    fun_arg_spec = getargspec(handler)
    if not fun_arg_spec.args and not fun_arg_spec.varargs:
        print("Handler '{handler}' can't receive an argument.".format(handler=handler))
