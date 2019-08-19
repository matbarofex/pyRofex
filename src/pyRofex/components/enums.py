# -*- coding: utf-8 -*-
"""
    pyRofex.components.enums

    Defines all library enumerations
"""
from enum import Enum


class Environment(Enum):
    """Available environments to used.
    REMARKET: Demo environment used for testing purpose.
    LIVE: ROFEX production environment.
    """
    REMARKET = 1
    LIVE = 2


class TimeInForce(Enum):
    """Time Modifier of the order that defines the time the order will be active.
    DAY: Order valid during the day. It will expires when the market close.
    IOC: Immediate or Cancel
    FOK: Fill or Kill
    GTD: Good Till Date (Must send expireDate field).
    """
    DAY = 'Day'
    ImmediateOrCancel = 'IOC'
    FillOrKill = 'FOK'
    GoodTillDate = 'GTD'


class Market(Enum):
    """Market ID associated to the instruments.
    ROFEX: ROFEX Exchange.
    """
    ROFEX = 'ROFX'


class Side(Enum):
    """Identifies the side of an order.
    BUY: Buy Order
    SELL: Sell Order
    """
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    """Identifies the different order types.
    LIMIT: For Limit Orders.
    MARKET: For Market Orders.
    MARKET_TO_LIMIT: For Market To Limit Orders.
    """
    LIMIT = "limit"
    MARKET = "market"
    MARKET_TO_LIMIT = "market_to_limit"


class MarketDataEntry(Enum):
    """Identifies market data entries for an instrument.
    BIDS: Best buy offer in the Market Book.
    OFFERS: Best sell offer in the Market Book.
    LAST: Last price traded in the Market Book.
    OPENING_PRICE: Opening price in the Market Book.
    CLOSING_PRICE: Closing price in the Market Book.
    SETTLEMENT_PRICE: Settlement price (only for futures)
    HIGH_PRICE: Highest price traded.
    LOW_PRICE: Lowest price traded.
    TRADE_VOLUME: Traded volume in contracts/nominal.
    OPEN_INTEREST: Open interest in contracts (only for futures)
    INDEX_VALUE: Calculated Index Value (only for Index)
    TRADE_EFFECTIVE_VOLUME: Effective traded volume.
    NOMINAL_VOLUME: Nominal traded volume.
    """
    BIDS = "BI"
    OFFERS = "OF"
    LAST = "LA"
    OPENING_PRICE = "OP"
    CLOSING_PRICE = "CL"
    SETTLEMENT_PRICE = "SE"
    HIGH_PRICE = "HI"
    LOW_PRICE = "LO"
    TRADE_VOLUME = "TV"
    OPEN_INTEREST = "OI"
    INDEX_VALUE = "IV"
    TRADE_EFFECTIVE_VOLUME = "EV"
    NOMINAL_VOLUME = "NV"
