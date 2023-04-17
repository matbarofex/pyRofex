# -*- coding: utf-8 -*-
"""
    Sample Module.

    Example of Market Data manipulation using the library.

    The code show how to get different market data for an instrument and
    how to get historical trade data using pyRofex.

    Go to the official Documentation to check the API Responses.

    Steps:
    1-Initialize the environment
    2-Set the instrument to use
    3-Get the two Best Bids and Best Offers for the instrument (using depth parameter)
    4-Get all available entries for the instrument
    5-Get the historical trades for the instrument from the beginning of the year until today
"""
import datetime

import pyRofex

# 1-Initialize the environment
pyRofex.initialize(user="XXXXXXX",
                   password="XXXXXXX",
                   account="XXXXXXX",
                   environment=pyRofex.Environment.REMARKET)

# 2-Set the instrument to use
instrument = "DLR/ENE24"

# 3-Get the two Best Bids and Best Offers for the instrument (using depth parameter)
entries = [pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.OFFERS, pyRofex.MarketDataEntry.LAST]
market_data = pyRofex.get_market_data(instrument, entries, depth=2)

print("Market Data Response for {0}: {1}".format(instrument, market_data))

# 4-Get all available entries for the instrument
entries = [
    pyRofex.MarketDataEntry.BIDS,
    pyRofex.MarketDataEntry.OFFERS,
    pyRofex.MarketDataEntry.LAST,
    pyRofex.MarketDataEntry.CLOSING_PRICE,
    pyRofex.MarketDataEntry.OPENING_PRICE,
    pyRofex.MarketDataEntry.HIGH_PRICE,
    pyRofex.MarketDataEntry.LOW_PRICE,
    pyRofex.MarketDataEntry.SETTLEMENT_PRICE,
    pyRofex.MarketDataEntry.NOMINAL_VOLUME,
    pyRofex.MarketDataEntry.TRADE_EFFECTIVE_VOLUME,
    pyRofex.MarketDataEntry.TRADE_VOLUME,
    pyRofex.MarketDataEntry.OPEN_INTEREST
]
market_data = pyRofex.get_market_data(instrument, entries)
print("Full Market Data Response for {0}: {1}".format(instrument, market_data))

# 5-Get the historical trades for the instrument from the beginning of the year until today
end = datetime.date.today()
start = datetime.date(year=end.year, month=1, day=1)
historic_trades = pyRofex.get_trade_history(ticker=instrument, start_date=start, end_date=end)
print("Historic Trades Response for {0} from {1} to {2}: {3}".format(instrument, start, end, historic_trades))
