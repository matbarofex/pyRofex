# -*- coding: utf-8 -*-
"""
    Sample Module.

    Example for reference data using the library.

    The code show how to work with segments and instrument data using pyRofex.

    Go to the official Documentation to check the API Responses.

    Steps:
    1-Initialize the environment
    2-Get all available segments and print all segment ids
    3-Get a list of all instruments and then count the number of instruments return
    4-Get a detailed list of the instruments and then check the Low Limit Price for the first instrument return
"""
import pyRofex

# 1-Initialize the environment
pyRofex.initialize(user="XXXXXXXXX",
                   password="XXXXXXXX",
                   account="XXXXXXXXX",
                   environment=pyRofex.Environment.REMARKET)

# 2-Get all available segments and print all segment ids
segments = pyRofex.get_segments()
for segment in segments['segments']:
    print("Segment ID: {0}".format(segment['marketSegmentId']))

# 3-Get a list of all instruments and then count the number of instruments return
instruments = pyRofex.get_all_instruments()
print("Number of all Instruments: {0}".format(len(instruments['instruments'])))

# 3.1 - Alternative way to get all available instruments
instruments = pyRofex.get_instruments('all')
print("Number of all Instruments: {0}".format(len(instruments['instruments'])))

# 3.2 - Alternative way to get instruments by segment: DDF and MERV
instruments = pyRofex.get_instruments('by_segments',
                                      market=pyRofex.Market.ROFEX,
                                      market_segment=[pyRofex.MarketSegment.DDF, pyRofex.MarketSegment.MERV])
print("Number of Instruments by given segments: {0}".format(len(instruments['instruments'])))

# 3.3 - Alternative way to get instruments by CFI code
instruments = pyRofex.get_instruments('by_cfi',
                                      cfi_code=[pyRofex.CFICode.STOCK, pyRofex.CFICode.BOND, pyRofex.CFICode.CEDEAR])
print("Number of Instruments by given CFI code: {0}".format(len(instruments['instruments'])))

# 4-Get a detailed list of the instruments and then check the Low Limit Price for the first instrument return
detailed = pyRofex.get_detailed_instruments()
print("Low Limit Price for {0} is {1}.".format(detailed['instruments'][0]['instrumentId']['symbol'],
                                               detailed['instruments'][0]['lowLimitPrice']))

# 4.1 - Alternative way get a detailed list of the instruments
detailed = pyRofex.get_instruments('details')
print("Low Limit Price for {0} is {1}.".format(detailed['instruments'][0]['instrumentId']['symbol'],
                                               detailed['instruments'][0]['lowLimitPrice']))


# 5 - Get the details of a specific instrument
# Set the instrument to use
ticker = "DLR/ENE24"
instrument = pyRofex.get_instrument_details(ticker=ticker)
print("The minimum Price Increment for {0} is set to {1}.".format(instrument['instrument']['instrumentId']['symbol'],
                                                                  instrument['instrument']['minPriceIncrement']))

# 5.1 - Alternative way to get the details of a specific instrument
instrument = pyRofex.get_instruments('detail', ticker=ticker, market=pyRofex.Market.ROFEX)
print("The minimum Price Increment for {0} is set to {1}.".format(instrument['instrument']['instrumentId']['symbol'],
                                                                  instrument['instrument']['minPriceIncrement']))