import pyRofex

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import time

instrument = "DLR/ENE24"

# Create empty DataFrame to store MarketData
prices = pd.DataFrame(columns=["Time", "Bid", "Offer", "Last"])
prices.set_index('Time', inplace=True)

plt.ion()
fig, ax = plt.subplots(figsize=(14, 5))
count = 0

# Initialize the environment
pyRofex.initialize(user="XXXXXXX",
                   password="XXXXXXX",
                   account="XXXXXXX",
                   environment=pyRofex.Environment.REMARKET)


def update_plot():
    global ax, prices, count
    if len(prices.index) > count:
        count = len(prices.index)
        ax.clear()
        plt.title('Price %s' % instrument, fontsize=15)
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        prices.plot(kind='line', y='Bid', lw=1.5, color='b', label='Bid Price', ax=ax)
        prices.plot(kind='line', y='Offer', lw=1.5, color='b', label='Offer Price', ax=ax)
        prices.plot(kind='line', y='Last', lw=1.5, marker='.', color='r', label='Last Price', ax=ax)
        ax.grid(True, linestyle='--')
        plt.tight_layout()
        plt.draw()
        plt.pause(0.2)


# Defines the handlers that will process the messages
def market_data_handler(message):
    global prices
    print("Market Data Message Received: {0}".format(message))
    last = None if not message["marketData"]["LA"] else message["marketData"]["LA"]["price"]
    prices.loc[datetime.fromtimestamp(message["timestamp"]/1000)] = [
        message["marketData"]["BI"][0]["price"],
        message["marketData"]["OF"][0]["price"],
        last
    ]


# Initialize Websocket Connection with the handlers
pyRofex.init_websocket_connection(market_data_handler=market_data_handler)


# Subscribes to receive market data messages
pyRofex.market_data_subscription(
    tickers=[instrument],
    entries=[
        pyRofex.MarketDataEntry.BIDS,
        pyRofex.MarketDataEntry.OFFERS,
        pyRofex.MarketDataEntry.LAST]
)

while True:
    update_plot()
    time.sleep(0.5)