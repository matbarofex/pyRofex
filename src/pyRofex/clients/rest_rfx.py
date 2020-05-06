# -*- coding: utf-8 -*-
"""
    pyRofex.rest_client

    Defines a Rest Client that implements ROFEX Rest API.
"""
import requests
import simplejson

from ..components import urls
from ..components import globals
from ..components.enums import OrderType
from ..components.enums import TimeInForce
from ..components.exceptions import ApiException


class RestClient:
    """ Rest Client that implements call to ROFEX REST API.

    For more information about the API go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf
    """

    def __init__(self, environment):
        """Initialization of the Client.

        :param environment: the environment that will be associated with the client.
        :type environment: Environment (Enum)
         """

        # Environment associated with Client
        self.environment = globals.environment_config[environment]

        # Get the authentication Token.
        self.update_token()

    def get_trade_history(self, ticker, start_date, end_date, market):
        """Makes a request to the API and get trade history for the instrument.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :param ticker: Ticker of the instrument to send in the request. Example: DODic19
        :type ticker: str
        :param start_date: Start date for the trades. Format: yyyy-MM-dd
        :type start_date: str
        :param end_date: End date for the trades. Format: yyyy-MM-dd
        :type end_date: str
        :param market: Market ID related to the instrument.
        :type market: Market (Enum).
        :return: List of trades returned by the API.
        :rtype: dict of JSON response.
        """
        return self.api_request(urls.historic_trades.format(m=market.value,
                                                            s=ticker,
                                                            df=start_date,
                                                            dt=end_date))

    def get_segments(self):
        """Make a request to the API and get a list of valid segments.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :return: A list of valid ROFEXs segments returned by the API.
        :rtype: dict of JSON response.
        """
        return self.api_request(urls.segments)

    def get_all_instruments(self):
        """Make a request to the API and get a list of all available instruments.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :return: A list of valid instruments returned by the API.
        :rtype: dict of JSON response.
        """
        return self.api_request(urls.instruments)

    def get_detailed_instruments(self):
        """Make a request to the API and get a list of all available instruments.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :return: A list of valid instruments returned by the API.
        :rtype: dict of JSON response.
        """
        return self.api_request(urls.detailed_instruments)

    def get_instrument_details(self, ticker, market):
        """Make a request to the API and get the details of the instrument.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :param ticker: Instrument symbol to send in the request. Example: DODic19
        :type ticker: str
        :param market: Market ID related to the instrument. Default Market.ROFEX.
        :type market: Market (Enum).
        :return: Details of the instrument returned by the API.
        :rtype: dict of JSON response.
        """
        return self.api_request(urls.instrument_details.format(ticker=ticker, market=market.value))

    def get_market_data(self, ticker, entries, depth, market):
        """Make a request to the API to get the Market Data Entries of the specified instrument.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :param ticker: Instrument symbol to send in the request. Example: DODic19
        :type ticker: str
        :param entries: List of entries to send in the request. Example: [MarketDataEntry.BIDS, MarketDataEntry.OFFERS]
        :type entries: List of MarketDataEntry (Enum).
        :param depth: Specify the depth of the book to be request. Default: 1.
        :type depth: int
        :param market: Market ID related to the instrument.
        :type market: Market (Enum).
        :return: Market Data response of the API.
        :rtype: dict of JSON response.
        """

        # Creates a comma separated string with the entries in the list.
        entry_string = ",".join([entry.value for entry in entries])
        return self.api_request(urls.market_data.format(m=market.value,
                                                        s=ticker,
                                                        e=entry_string,
                                                        d=depth))

    def get_order_status(self, client_order_id, proprietary):
        """Make a request to the API to get the status of the specified order.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :param client_order_id: Client Order ID of the order.
        :type client_order_id: str
        :param proprietary: Proprietary of the order.
        :type proprietary: str
        :return: Order status response of the API.
        :rtype: dict of JSON response.
        """
        return self.api_request(urls.order_status.format(c=client_order_id,
                                                         p=proprietary))

    def get_all_orders_by_account(self, account):
        """Make a request to the API and get the status of all the orders associated with the account.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :param account: Account associated with the orders.
        :type account: str
        :return: List of all orders status associated with the user returned by the API.
        :rtype: dict of JSON response.
        """
        return self.api_request(urls.all_orders_status.format(a=account))

    def send_order(self, ticker, size, order_type, side,
                   account, price, time_in_force, market,
                   cancel_previous, iceberg, expire_date,
                   display_quantity):
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
        :param account: Account to used.
        :type account: str
        :param price: Order price.
        :type price: int
        :param time_in_force: Order modifier that defines the active time of the order.
        :type time_in_force: TimeInForce (Enum).
        :param market: Market ID related to the instrument.
        :type market: Market (Enum).
        :param cancel_previous: True: cancels actives orders that match with the account, side and ticker.
        False: send the order without cancelling previous ones. Useful for replacing old orders.
        :type cancel_previous: boolean.
        :param iceberg: True: if it is an iceberg order. False: if it's not an iceberg order.
        :type iceberg: boolean.
        :param expire_date: Indicates the Expiration date for a GTD order. Example: 20170720.
        :type expire_date: str (Enum).
        :param display_quantity: Indicates the amount to be disclosed for GTD orders.
        :type display_quantity: int
        :return: Client Order ID and Proprietary of the order returned by the API.
        :rtype: dict of JSON response.
        """
        new_order_url = urls.new_order

        # Adds Optional Parameters
        if order_type is OrderType.LIMIT:
            new_order_url = new_order_url + urls.limit_order

        if time_in_force is TimeInForce.GoodTillDate:
            new_order_url = new_order_url + urls.good_till_date

        if iceberg:
            new_order_url = new_order_url + urls.iceberg

        return self.api_request(new_order_url.format(market=market.value,
                                                     ticker=ticker,
                                                     size=size,
                                                     type=order_type.value,
                                                     side=side.value,
                                                     time_force=time_in_force.value,
                                                     account=account,
                                                     price=price,
                                                     cancel_previous=cancel_previous,
                                                     iceberg=iceberg,
                                                     expire_date=expire_date,
                                                     display_quantity=display_quantity))

    def cancel_order(self, client_order_id, proprietary):
        """Make a request to the API and cancel the order specified.

        The market will respond with a client order id, then you should verify the status of the request with this id.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :param client_order_id: Client Order ID of the order.
        :type client_order_id: str
        :param proprietary: Proprietary of the order.
        :type proprietary: str
        :return: Client Order ID of cancellation request returned by the API.
        :rtype: dict of JSON response.
        """
        return self.api_request(urls.cancel_order.format(id=client_order_id,
                                                         p=proprietary))

    def api_request(self, path, retry=True):
        """ Make a GET request to the API.

        :param path: path to the API resource.
        :type path: str
        :param retry: (optional) True: update the token and resend the request if the response code is 401.
        False: raise an exception if the response code is 401.
        :type retry: str
        :return: response of the API.
        :rtype: dict of JSON response.
        """
        headers = {'X-Auth-Token': self.environment["token"]}
        response = requests.get(self._url(path),
                                headers=headers,
                                verify=self.environment["ssl"],
                                proxies=self.environment["proxies"])

        # Checks if the response code is 401 (Unauthorized)
        if response.status_code == 401:
            if retry:
                self.update_token()
                self.api_request(path, False)
            else:
                raise ApiException("Authentication Fails.")

        return simplejson.loads(response.content)

    def update_token(self):
        """ Authenticate using the environment user and password.

        Then save the token in the environment parameters and set the initialized parameter to True.
        """
        headers = {'X-Username': self.environment["user"],
                   'X-Password': self.environment["password"]}
        response = requests.post(self._url(urls.auth),
                                 headers=headers,
                                 verify=self.environment["ssl"],
                                 proxies=self.environment["proxies"])

        if not response.ok:
            raise ApiException("Authentication fails. Incorrect User or Password")

        self.environment["token"] = response.headers['X-Auth-Token']
        self.environment["initialized"] = True

    def _url(self, path):
        """ Helper function that concatenate the path to the environment url.

        :param path: path to the API resource.
        :type path: str
        :return: URL to be call.
        :rtype: str
        """
        return self.environment["url"] + path
