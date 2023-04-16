# -*- coding: utf-8 -*-
"""
    pyRofex.urls

    Defines all API Paths
"""
from .enums import OrderType
from .enums import TimeInForce

auth = "auth/getToken"
segments = "rest/segment/all"
instruments = {"all": "rest/instruments/all",
               "details": "rest/instruments/details",
               "detail": "rest/instruments/detail?symbol={ticker}&marketId={market}",
               "by_cfi": "rest/instruments/byCFICode?CFICode={cfi_code}",
               "by_segments": "rest/instruments/bySegment?MarketSegmentID={market_segment}&MarketID={market}"}
market_data = "rest/marketdata/get?marketId={m}&symbol={s}&entries={e}&depth={d}"
historic_trades = "rest/data/getTrades?marketId={m}&symbol={s}&dateFrom={df}&dateTo={dt}"
order_status = "rest/order/id?clOrdId={c}&proprietary={p}"
new_order = "rest/order/newSingleOrder?marketId={market}&symbol={ticker}" \
            "&orderQty={size}&ordType={type}&side={side}&timeInForce={time_force}" \
            "&account={account}&cancelPrevious={cancel_previous}"
cancel_order = "rest/order/cancelById?clOrdId={id}&proprietary={p}"
all_orders_status = "rest/order/all?accountId={a}"
account_position = "rest/risk/position/getPositions/{a}"
detailed_position = "rest/risk/detailedPosition/{a}"
account_report = "rest/risk/accountReport/{a}"

# Optional Parameters
iceberg = "&iceberg=true&displayQty={display_quantity}"
limit_order = "&price={price}"
good_till_date = "&expireDate={expire_date}"
