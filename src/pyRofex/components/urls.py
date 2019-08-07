# -*- coding: utf-8 -*-
"""
    pyRofex.urls

    Defines all API Paths
"""
from .enums import OrderType

auth = "auth/getToken"
segments = "rest/segment/all"
instruments = "rest/instruments/all"
detailed_instruments = "rest/instruments/details"
market_data = "rest/marketdata/get?marketId={m}&symbol={s}&entries={e}&depth={d}"
historic_trades = "rest/data/getTrades?marketId={m}&symbol={s}&dateFrom={df}&dateTo={dt}"
order_status = "rest/order/id?clOrdId={c}&proprietary={p}"
new_order = {
    OrderType.MARKET: "rest/order/newSingleOrder?marketId={market}&symbol={ticker}"
                      "&orderQty={size}&ordType={type}&side={side}&timeInForce={time_force}"
                      "&account={account}&cancelPrevious={cancel_previous}",
    OrderType.LIMIT: "rest/order/newSingleOrder?marketId={market}&symbol={ticker}"
                     "&price={price}&orderQty={size}&ordType={type}&side={side}"
                     "&timeInForce={time_force}&account={account}&cancelPrevious={cancel_previous}"
}
cancel_order = "rest/order/cancelById?clOrdId={id}&proprietary={p}"
all_orders_status = "rest/order/all?accountId={a}"
