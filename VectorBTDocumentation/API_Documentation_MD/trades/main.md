records trades

#  trades module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades "Permanent link")

Base class for working with trade records.

Trade records capture information on trades.

In vectorbt, a trade is a sequence of orders that starts with an opening order and optionally ends with a closing order. Every pair of opposite orders can be represented by a trade. Each trade has a PnL info attached to quickly assess its performance. An interesting effect of this representation is the ability to aggregate trades: if two or more trades are happening one after another in time, they can be aggregated into a bigger trade. This way, for example, single-order trades can be aggregated into positions; but also multiple positions can be aggregated into a single blob that reflects the performance of the entire symbol.

Warning

All classes return both closed AND open trades/positions, which may skew your performance results. To only consider closed trades/positions, you should explicitly query the `status_closed` attribute.

## Trade types[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#trade-types "Permanent link")

There are three main types of trades.

### Entry trades[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#entry-trades "Permanent link")

An entry trade is created from each order that opens or adds to a position.

For example, if we have a single large buy order and 100 smaller sell orders, we will see a single trade with the entry information copied from the buy order and the exit information being a size-weighted average over the exit information of all sell orders. On the other hand, if we have 100 smaller buy orders and a single sell order, we will see 100 trades, each with the entry information copied from the buy order and the exit information being a size-based fraction of the exit information of the sell order.

Use [EntryTrades.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades.from_orders "vectorbtpro.portfolio.trades.EntryTrades.from_orders") to build entry trades from orders. Also available as [Portfolio.entry_trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.entry_trades "vectorbtpro.portfolio.base.Portfolio.entry_trades").

### Exit trades[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#exit-trades "Permanent link")

An exit trade is created from each order that closes or removes from a position.

Use [ExitTrades.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades.from_orders "vectorbtpro.portfolio.trades.ExitTrades.from_orders") to build exit trades from orders. Also available as [Portfolio.exit_trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.exit_trades "vectorbtpro.portfolio.base.Portfolio.exit_trades").

### Positions[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#positions "Permanent link")

A position is created from a sequence of entry or exit trades.

Use [Positions.from_trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Positions.from_trades "vectorbtpro.portfolio.trades.Positions.from_trades") to build positions from entry or exit trades. Also available as [Portfolio.positions](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.positions "vectorbtpro.portfolio.base.Portfolio.positions").

## Example[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#example "Permanent link")

  * Increasing position:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-3)>>> # Entry trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-4)>>> pf_kwargs = dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-5)...     close=pd.Series([1., 2., 3., 4., 5.]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-6)...     size=pd.Series([1., 1., 1., 1., -4.]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-7)...     fixed_fees=1.
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-8)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-9)>>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-10)>>> entry_trades.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-11)   Entry Trade Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-12)0               0       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-13)1               1       0   1.0               1            1              2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-14)2               2       0   1.0               2            2              3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-15)3               3       0   1.0               3            3              4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-16)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-17)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees   PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-18)0         1.0              4           4             5.0       0.25  2.75
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-19)1         1.0              4           4             5.0       0.25  1.75
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-20)2         1.0              4           4             5.0       0.25  0.75
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-21)3         1.0              4           4             5.0       0.25 -0.25
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-22)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-23)   Return Direction  Status  Position Id
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-24)0  2.7500      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-25)1  0.8750      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-26)2  0.2500      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-27)3 -0.0625      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-28)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-29)>>> # Exit trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-30)>>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-31)>>> exit_trades.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-32)   Exit Trade Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-33)0              0       0   4.0               0            0              2.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-34)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-35)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-36)0         4.0              4           4             5.0        1.0  5.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-37)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-38)   Return Direction  Status  Position Id
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-39)0     0.5      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-40)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-41)>>> # Positions
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-42)>>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-43)>>> positions.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-44)   Position Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-45)0            0       0   4.0               0            0              2.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-46)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-47)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-48)0         4.0              4           4             5.0        1.0  5.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-49)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-50)   Return Direction  Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-51)0     0.5      Long  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-52)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-53)>>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-0-54)True
    

  * Decreasing position:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-1)>>> # Entry trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-2)>>> pf_kwargs = dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-3)...     close=pd.Series([1., 2., 3., 4., 5.]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-4)...     size=pd.Series([4., -1., -1., -1., -1.]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-5)...     fixed_fees=1.
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-7)>>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-8)>>> entry_trades.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-9)   Entry Trade Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-10)0               0       0   4.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-12)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-13)0         1.0              4           4             3.5        4.0  5.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-15)   Return Direction  Status  Position Id
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-16)0    1.25      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-17)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-18)>>> # Exit trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-19)>>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-20)>>> exit_trades.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-21)   Exit Trade Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-22)0              0       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-23)1              1       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-24)2              2       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-25)3              3       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-27)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees   PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-28)0        0.25              1           1             2.0        1.0 -0.25
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-29)1        0.25              2           2             3.0        1.0  0.75
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-30)2        0.25              3           3             4.0        1.0  1.75
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-31)3        0.25              4           4             5.0        1.0  2.75
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-32)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-33)   Return Direction  Status  Position Id
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-34)0   -0.25      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-35)1    0.75      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-36)2    1.75      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-37)3    2.75      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-38)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-39)>>> # Positions
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-40)>>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-41)>>> positions.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-42)   Position Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-43)0            0       0   4.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-44)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-45)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-46)0         1.0              4           4             3.5        4.0  5.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-47)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-48)   Return Direction  Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-49)0    1.25      Long  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-50)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-51)>>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-1-52)True
    

  * Multiple reversing positions:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-1)>>> # Entry trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-2)>>> pf_kwargs = dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-3)...     close=pd.Series([1., 2., 3., 4., 5.]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-4)...     size=pd.Series([1., -2., 2., -2., 1.]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-5)...     fixed_fees=1.
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-7)>>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-8)>>> entry_trades.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-9)   Entry Trade Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-10)0               0       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-11)1               1       0   1.0               1            1              2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-12)2               2       0   1.0               2            2              3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-13)3               3       0   1.0               3            3              4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-15)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-16)0         1.0              1           1             2.0        0.5 -0.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-17)1         0.5              2           2             3.0        0.5 -2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-18)2         0.5              3           3             4.0        0.5  0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-19)3         0.5              4           4             5.0        1.0 -2.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-21)   Return Direction  Status  Position Id
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-22)0  -0.500      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-23)1  -1.000     Short  Closed            1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-24)2   0.000      Long  Closed            2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-25)3  -0.625     Short  Closed            3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-27)>>> # Exit trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-28)>>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-29)>>> exit_trades.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-30)   Exit Trade Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-31)0              0       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-32)1              1       0   1.0               1            1              2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-33)2              2       0   1.0               2            2              3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-34)3              3       0   1.0               3            3              4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-35)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-36)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-37)0         1.0              1           1             2.0        0.5 -0.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-38)1         0.5              2           2             3.0        0.5 -2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-39)2         0.5              3           3             4.0        0.5  0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-40)3         0.5              4           4             5.0        1.0 -2.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-41)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-42)   Return Direction  Status  Position Id
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-43)0  -0.500      Long  Closed            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-44)1  -1.000     Short  Closed            1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-45)2   0.000      Long  Closed            2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-46)3  -0.625     Short  Closed            3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-47)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-48)>>> # Positions
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-49)>>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-50)>>> positions.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-51)   Position Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-52)0            0       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-53)1            1       0   1.0               1            1              2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-54)2            2       0   1.0               2            2              3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-55)3            3       0   1.0               3            3              4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-56)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-57)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-58)0         1.0              1           1             2.0        0.5 -0.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-59)1         0.5              2           2             3.0        0.5 -2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-60)2         0.5              3           3             4.0        0.5  0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-61)3         0.5              4           4             5.0        1.0 -2.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-62)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-63)   Return Direction  Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-64)0  -0.500      Long  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-65)1  -1.000     Short  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-66)2   0.000      Long  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-67)3  -0.625     Short  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-68)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-69)>>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-2-70)True
    

  * Open position:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-1)>>> # Entry trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-2)>>> pf_kwargs = dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-3)...     close=pd.Series([1., 2., 3., 4., 5.]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-4)...     size=pd.Series([1., 0., 0., 0., 0.]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-5)...     fixed_fees=1.
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-7)>>> entry_trades = vbt.Portfolio.from_orders(**pf_kwargs).entry_trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-8)>>> entry_trades.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-9)   Entry Trade Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-10)0               0       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-12)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-13)0         1.0             -1           4             5.0        0.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-15)   Return Direction Status  Position Id
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-16)0     3.0      Long   Open            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-17)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-18)>>> # Exit trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-19)>>> exit_trades = vbt.Portfolio.from_orders(**pf_kwargs).exit_trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-20)>>> exit_trades.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-21)   Exit Trade Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-22)0              0       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-23)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-24)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-25)0         1.0             -1           4             5.0        0.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-27)   Return Direction Status  Position Id
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-28)0     3.0      Long   Open            0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-29)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-30)>>> # Positions
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-31)>>> positions = vbt.Portfolio.from_orders(**pf_kwargs).positions
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-32)>>> positions.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-33)   Position Id  Column  Size  Entry Order Id  Entry Index  Avg Entry Price  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-34)0            0       0   1.0               0            0              1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-35)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-36)   Entry Fees  Exit Order Id  Exit Index  Avg Exit Price  Exit Fees  PnL  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-37)0         1.0             -1           4             5.0        0.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-38)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-39)   Return Direction Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-40)0     3.0      Long   Open
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-41)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-42)>>> entry_trades.pnl.sum() == exit_trades.pnl.sum() == positions.pnl.sum()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-3-43)True
    

Get trade count, trade PnL, and winning trade PnL:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-1)>>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.])
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-2)>>> size = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5])
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-3)>>> trades = vbt.Portfolio.from_orders(price, size).trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-5)>>> trades.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-6)6
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-8)>>> trades.pnl.sum()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-9)-3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-11)>>> trades.winning.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-12)2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-13)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-14)>>> trades.winning.pnl.sum()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-4-15)1.5
    

Get count and PnL of trades with duration of more than 2 days:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-5-1)>>> mask = (trades.records['exit_idx'] - trades.records['entry_idx']) > 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-5-2)>>> trades_filtered = trades.apply_mask(mask)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-5-3)>>> trades_filtered.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-5-4)2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-5-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-5-6)>>> trades_filtered.pnl.sum()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-5-7)-3.0
    

## Stats[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#stats "Permanent link")

Hint

See [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats") and [Trades.metrics](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.metrics "vectorbtpro.portfolio.trades.Trades.metrics").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-6-1)>>> price = vbt.RandomData.pull(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-6-2)...     ['a', 'b'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-6-3)...     start=datetime(2020, 1, 1),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-6-4)...     end=datetime(2020, 3, 1),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-6-5)...     seed=vbt.symbol_dict(a=42, b=43)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-6-6)... ).get()
    

100%
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-1)>>> size = pd.DataFrame({
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-2)...     'a': np.random.randint(-1, 2, size=len(price.index)),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-3)...     'b': np.random.randint(-1, 2, size=len(price.index)),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-4)... }, index=price.index, columns=price.columns)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-5)>>> pf = vbt.Portfolio.from_orders(price, size, fees=0.01, init_cash="auto")
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-7)>>> pf.trades['a'].stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-8)Start                          2019-12-31 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-9)End                            2020-02-29 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-10)Period                                  61 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-11)First Trade Start              2019-12-31 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-12)Last Trade End                 2020-02-29 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-13)Coverage                                60 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-14)Overlap Coverage                        49 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-15)Total Records                                       19.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-16)Total Long Trades                                    2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-17)Total Short Trades                                  17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-18)Total Closed Trades                                 18.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-19)Total Open Trades                                    1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-20)Open Trade PnL                                    16.063
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-21)Win Rate [%]                                   61.111111
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-22)Max Win Streak                                      11.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-23)Max Loss Streak                                      7.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-24)Best Trade [%]                                  3.526377
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-25)Worst Trade [%]                                -6.543679
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-26)Avg Winning Trade [%]                           2.225861
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-27)Avg Losing Trade [%]                           -3.601313
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-28)Avg Winning Trade Duration    32 days 19:38:10.909090909
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-29)Avg Losing Trade Duration                5 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-30)Profit Factor                                   1.022425
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-31)Expectancy                                      0.028157
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-32)SQN                                             0.039174
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-7-33)Name: agg_stats, dtype: object
    

Positions share almost identical metrics with trades:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-1)>>> pf.positions['a'].stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-2)Start                         2019-12-31 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-3)End                           2020-02-29 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-4)Period                                 61 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-5)First Trade Start             2019-12-31 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-6)Last Trade End                2020-02-29 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-7)Coverage                               60 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-8)Overlap Coverage                        0 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-9)Total Records                                       5.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-10)Total Long Trades                                   2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-11)Total Short Trades                                  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-12)Total Closed Trades                                 4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-13)Total Open Trades                                   1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-14)Open Trade PnL                                38.356823
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-15)Win Rate [%]                                        0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-16)Max Win Streak                                      0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-17)Max Loss Streak                                     4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-18)Best Trade [%]                                -1.529613
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-19)Worst Trade [%]                               -6.543679
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-20)Avg Winning Trade [%]                               NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-21)Avg Losing Trade [%]                          -3.786739
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-22)Avg Winning Trade Duration                          NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-23)Avg Losing Trade Duration               4 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-24)Profit Factor                                       0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-25)Expectancy                                    -5.446748
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-26)SQN                                           -1.794214
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-8-27)Name: agg_stats, dtype: object
    

To also include open trades/positions when calculating metrics such as win rate, pass `incl_open=True`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-1)>>> pf.trades['a'].stats(settings=dict(incl_open=True))
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-2)Start                         2019-12-31 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-3)End                           2020-02-29 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-4)Period                                 61 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-5)First Trade Start             2019-12-31 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-6)Last Trade End                2020-02-29 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-7)Coverage                               60 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-8)Overlap Coverage                       49 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-9)Total Records                                      19.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-10)Total Long Trades                                   2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-11)Total Short Trades                                 17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-12)Total Closed Trades                                18.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-13)Total Open Trades                                   1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-14)Open Trade PnL                                   16.063
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-15)Win Rate [%]                                  61.111111
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-16)Max Win Streak                                     12.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-17)Max Loss Streak                                     7.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-18)Best Trade [%]                                 3.526377
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-19)Worst Trade [%]                               -6.543679
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-20)Avg Winning Trade [%]                          2.238896
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-21)Avg Losing Trade [%]                          -3.601313
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-22)Avg Winning Trade Duration             33 days 18:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-23)Avg Losing Trade Duration               5 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-24)Profit Factor                                  1.733143
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-25)Expectancy                                     0.872096
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-26)SQN                                            0.804714
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-9-27)Name: agg_stats, dtype: object
    

[StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.trades.Trades.stats") also supports (re-)grouping:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-1)>>> pf.trades.stats(group_by=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-2)Start                          2019-12-31 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-3)End                            2020-02-29 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-4)Period                                  61 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-5)First Trade Start              2019-12-31 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-6)Last Trade End                 2020-02-29 23:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-7)Coverage                                61 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-8)Overlap Coverage                        61 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-9)Total Records                                         37
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-10)Total Long Trades                                      5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-11)Total Short Trades                                    32
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-12)Total Closed Trades                                   35
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-13)Total Open Trades                                      2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-14)Open Trade PnL                                  1.336259
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-15)Win Rate [%]                                   37.142857
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-16)Max Win Streak                                        11
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-17)Max Loss Streak                                       10
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-18)Best Trade [%]                                  3.526377
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-19)Worst Trade [%]                                -8.710238
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-20)Avg Winning Trade [%]                           1.907799
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-21)Avg Losing Trade [%]                           -3.259135
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-22)Avg Winning Trade Duration    28 days 14:46:09.230769231
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-23)Avg Losing Trade Duration               14 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-24)Profit Factor                                   0.340493
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-25)Expectancy                                     -1.292596
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-26)SQN                                            -2.509223
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-10-27)Name: group, dtype: object
    

## Plots[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#plots "Permanent link")

Hint

See [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots") and [Trades.subplots](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.subplots "vectorbtpro.portfolio.trades.Trades.subplots").

[Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades") class has two subplots based on [Trades.plot](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot "vectorbtpro.portfolio.trades.Trades.plot") and [Trades.plot_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_pnl "vectorbtpro.portfolio.trades.Trades.plot_pnl"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-11-1)>>> pf.trades['a'].plots().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plots.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plots.dark.svg#only-dark)

* * *

## entry_trades_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.entry_trades_field_config "Permanent link")

Field config for [EntryTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades "vectorbtpro.portfolio.trades.EntryTrades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-2)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-3)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-4)            title='Entry Trade Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-5)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-6)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-7)            name='entry_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-8)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-9)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-12-10))
    

* * *

## exit_trades_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.exit_trades_field_config "Permanent link")

Field config for [ExitTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades "vectorbtpro.portfolio.trades.ExitTrades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-13-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-13-2)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-13-3)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-13-4)            title='Exit Trade Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-13-5)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-13-6)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-13-7))
    

* * *

## positions_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.positions_field_config "Permanent link")

Field config for [Positions](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Positions "vectorbtpro.portfolio.trades.Positions").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-2)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-3)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-4)            title='Position Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-5)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-6)        parent_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-7)            title='Parent Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-8)            ignore=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-9)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-10)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-14-11))
    

* * *

## trades_attach_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.trades_attach_field_config "Permanent link")

Config of fields to be attached to [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-2)    return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-3)        attach='returns'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-4)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-5)    direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-6)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-8)    status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-9)        attach_filters=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-10)        on_conflict='ignore'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-11)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-15-12))
    

* * *

## trades_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.trades_field_config "Permanent link")

Field config for [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-5)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-6)        ('entry_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-7)        ('entry_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-8)        ('entry_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-9)        ('entry_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-10)        ('exit_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-11)        ('exit_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-12)        ('exit_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-13)        ('exit_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-14)        ('pnl', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-15)        ('return', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-16)        ('direction', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-17)        ('status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-18)        ('parent_id', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-19)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-20)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-21)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-22)            title='Trade Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-23)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-24)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-25)            name='exit_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-26)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-27)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-28)            name='entry_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-29)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-30)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-31)            name='exit_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-32)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-33)        size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-34)            title='Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-35)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-36)        entry_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-37)            title='Entry Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-38)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-39)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-40)        entry_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-41)            title='Entry Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-42)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-43)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-44)        entry_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-45)            title='Avg Entry Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-46)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-47)        entry_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-48)            title='Entry Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-49)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-50)        exit_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-51)            title='Exit Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-52)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-53)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-54)        exit_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-55)            title='Exit Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-56)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-57)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-58)        exit_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-59)            title='Avg Exit Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-60)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-61)        exit_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-62)            title='Exit Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-63)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-64)        pnl=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-65)            title='PnL'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-66)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-67)        return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-68)            title='Return',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-69)            hovertemplate='$title: %{customdata[$index]:,%}'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-70)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-71)        direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-72)            title='Direction',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-73)            mapping=TradeDirectionT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-74)                Long=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-75)                Short=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-76)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-77)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-78)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-79)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-80)            mapping=TradeStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-81)                Open=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-82)                Closed=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-83)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-84)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-85)        parent_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-86)            title='Position Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-87)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-88)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-89)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-16-90))
    

* * *

## trades_shortcut_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.trades_shortcut_config "Permanent link")

Config of shortcut properties to be attached to [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-2)    ranges=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-3)    long_view=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-4)    short_view=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-5)    winning=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-6)    losing=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-7)    winning_streak=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-8)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-9)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-10)    losing_streak=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-11)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-12)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-13)    win_rate=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-14)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-15)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-16)    profit_factor=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-17)        obj_type='red_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-18)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-19)            use_returns=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-20)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-21)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-22)    rel_profit_factor=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-23)        obj_type='red_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-24)        method_name='get_profit_factor',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-25)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-26)            use_returns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-27)            wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-28)                name_or_index='rel_profit_factor'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-29)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-30)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-31)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-32)    expectancy=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-33)        obj_type='red_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-34)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-35)            use_returns=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-36)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-37)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-38)    rel_expectancy=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-39)        obj_type='red_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-40)        method_name='get_expectancy',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-41)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-42)            use_returns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-43)            wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-44)                name_or_index='rel_expectancy'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-45)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-46)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-47)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-48)    sqn=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-49)        obj_type='red_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-50)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-51)            use_returns=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-52)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-53)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-54)    rel_sqn=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-55)        obj_type='red_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-56)        method_name='get_sqn',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-57)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-58)            use_returns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-59)            wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-60)                name_or_index='rel_sqn'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-61)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-62)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-63)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-64)    best_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-65)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-66)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-67)    worst_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-68)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-69)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-70)    best_price_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-71)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-72)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-73)    worst_price_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-74)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-75)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-76)    expanding_best_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-77)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-78)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-79)    expanding_worst_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-80)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-81)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-82)    mfe=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-83)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-84)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-85)    mfe_returns=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-86)        obj_type='mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-87)        method_name='get_mfe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-88)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-89)            use_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-90)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-91)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-92)    mae=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-93)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-94)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-95)    mae_returns=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-96)        obj_type='mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-97)        method_name='get_mae',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-98)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-99)            use_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-100)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-101)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-102)    expanding_mfe=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-103)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-104)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-105)    expanding_mfe_returns=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-106)        obj_type='array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-107)        method_name='get_expanding_mfe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-108)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-109)            use_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-110)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-111)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-112)    expanding_mae=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-113)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-114)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-115)    expanding_mae_returns=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-116)        obj_type='array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-117)        method_name='get_expanding_mae',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-118)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-119)            use_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-120)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-121)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-122)    edge_ratio=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-123)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-124)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-125)    running_edge_ratio=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-126)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-127)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-17-128))
    

* * *

## EntryTrades class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2418-L2639 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-1)EntryTrades(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-18-9))
    

Extends [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades") for working with entry trade records.

**Superclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")
  * [IndexApplier](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "vectorbtpro.base.indexes.IndexApplier")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords "vectorbtpro.generic.price_records.PriceRecords")
  * [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges")
  * [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.portfolio.trades.Trades.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.portfolio.trades.Trades.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.portfolio.trades.Trades.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.portfolio.trades.Trades.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.portfolio.trades.Trades.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.portfolio.trades.Trades.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.portfolio.trades.Trades.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.portfolio.trades.Trades.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.portfolio.trades.Trades.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.portfolio.trades.Trades.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.portfolio.trades.Trades.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.portfolio.trades.Trades.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.portfolio.trades.Trades.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.portfolio.trades.Trades.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.portfolio.trades.Trades.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.portfolio.trades.Trades.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.portfolio.trades.Trades.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.portfolio.trades.Trades.prettify")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.portfolio.trades.Trades.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.portfolio.trades.Trades.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.portfolio.trades.Trades.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.portfolio.trades.Trades.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.portfolio.trades.Trades.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.portfolio.trades.Trades.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.portfolio.trades.Trades.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.portfolio.trades.Trades.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.portfolio.trades.Trades.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.portfolio.trades.Trades.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.portfolio.trades.Trades.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.portfolio.trades.Trades.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.portfolio.trades.Trades.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.portfolio.trades.Trades.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.portfolio.trades.Trades.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.portfolio.trades.Trades.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.portfolio.trades.Trades.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.portfolio.trades.Trades.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.portfolio.trades.Trades.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.portfolio.trades.Trades.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.portfolio.trades.Trades.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.portfolio.trades.Trades.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.portfolio.trades.Trades.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.portfolio.trades.Trades.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.portfolio.trades.Trades.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.portfolio.trades.Trades.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.portfolio.trades.Trades.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.portfolio.trades.Trades.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.portfolio.trades.Trades.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.portfolio.trades.Trades.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.portfolio.trades.Trades.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.portfolio.trades.Trades.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.portfolio.trades.Trades.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.portfolio.trades.Trades.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.portfolio.trades.Trades.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.portfolio.trades.Trades.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.portfolio.trades.Trades.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.portfolio.trades.Trades.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.portfolio.trades.Trades.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.portfolio.trades.Trades.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.portfolio.trades.Trades.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.portfolio.trades.Trades.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.portfolio.trades.Trades.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.portfolio.trades.Trades.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.portfolio.trades.Trades.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.portfolio.trades.Trades.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.portfolio.trades.Trades.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.portfolio.trades.Trades.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.portfolio.trades.Trades.pprint")
  * [PriceRecords.from_records](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.from_records "vectorbtpro.portfolio.trades.Trades.from_records")
  * [PriceRecords.get_bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close "vectorbtpro.portfolio.trades.Trades.get_bar_close")
  * [PriceRecords.get_bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close_time "vectorbtpro.portfolio.trades.Trades.get_bar_close_time")
  * [PriceRecords.get_bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_high "vectorbtpro.portfolio.trades.Trades.get_bar_high")
  * [PriceRecords.get_bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_low "vectorbtpro.portfolio.trades.Trades.get_bar_low")
  * [PriceRecords.get_bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open "vectorbtpro.portfolio.trades.Trades.get_bar_open")
  * [PriceRecords.get_bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open_time "vectorbtpro.portfolio.trades.Trades.get_bar_open_time")
  * [PriceRecords.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func "vectorbtpro.portfolio.trades.Trades.indexing_func")
  * [PriceRecords.indexing_func_meta](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func_meta "vectorbtpro.portfolio.trades.Trades.indexing_func_meta")
  * [PriceRecords.resample](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resample "vectorbtpro.portfolio.trades.Trades.resample")
  * [PriceRecords.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_column_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_column_stack_kwargs")
  * [PriceRecords.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_row_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_row_stack_kwargs")
  * [Ranges.crop](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.crop "vectorbtpro.portfolio.trades.Trades.crop")
  * [Ranges.filter_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_max_duration "vectorbtpro.portfolio.trades.Trades.filter_max_duration")
  * [Ranges.filter_min_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_min_duration "vectorbtpro.portfolio.trades.Trades.filter_min_duration")
  * [Ranges.from_array](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_array "vectorbtpro.portfolio.trades.Trades.from_array")
  * [Ranges.from_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta "vectorbtpro.portfolio.trades.Trades.from_delta")
  * [Ranges.get_avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_avg_duration "vectorbtpro.portfolio.trades.Trades.get_avg_duration")
  * [Ranges.get_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_coverage "vectorbtpro.portfolio.trades.Trades.get_coverage")
  * [Ranges.get_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_duration "vectorbtpro.portfolio.trades.Trades.get_duration")
  * [Ranges.get_first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_idx "vectorbtpro.portfolio.trades.Trades.get_first_idx")
  * [Ranges.get_first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_pd_mask "vectorbtpro.portfolio.trades.Trades.get_first_pd_mask")
  * [Ranges.get_invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_invalid "vectorbtpro.portfolio.trades.Trades.get_invalid")
  * [Ranges.get_last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_idx "vectorbtpro.portfolio.trades.Trades.get_last_idx")
  * [Ranges.get_last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_pd_mask "vectorbtpro.portfolio.trades.Trades.get_last_pd_mask")
  * [Ranges.get_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_max_duration "vectorbtpro.portfolio.trades.Trades.get_max_duration")
  * [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.portfolio.trades.Trades.get_projections")
  * [Ranges.get_ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_ranges_pd_mask "vectorbtpro.portfolio.trades.Trades.get_ranges_pd_mask")
  * [Ranges.get_real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_real_duration "vectorbtpro.portfolio.trades.Trades.get_real_duration")
  * [Ranges.get_valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_valid "vectorbtpro.portfolio.trades.Trades.get_valid")
  * [Ranges.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections "vectorbtpro.portfolio.trades.Trades.plot_projections")
  * [Ranges.plot_shapes](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_shapes "vectorbtpro.portfolio.trades.Trades.plot_shapes")
  * [Ranges.with_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.with_delta "vectorbtpro.portfolio.trades.Trades.with_delta")
  * [Records.apply](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply "vectorbtpro.portfolio.trades.Trades.apply")
  * [Records.apply_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply_mask "vectorbtpro.portfolio.trades.Trades.apply_mask")
  * [Records.build_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.build_field_config_doc "vectorbtpro.portfolio.trades.Trades.build_field_config_doc")
  * [Records.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack "vectorbtpro.portfolio.trades.Trades.column_stack")
  * [Records.column_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack_records_arrs "vectorbtpro.portfolio.trades.Trades.column_stack_records_arrs")
  * [Records.count](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.count "vectorbtpro.portfolio.trades.Trades.count")
  * [Records.coverage_map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.coverage_map "vectorbtpro.portfolio.trades.Trades.coverage_map")
  * [Records.first_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.first_n "vectorbtpro.portfolio.trades.Trades.first_n")
  * [Records.get_apply_mapping_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_arr "vectorbtpro.portfolio.trades.Trades.get_apply_mapping_arr")
  * [Records.get_apply_mapping_str_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_str_arr "vectorbtpro.portfolio.trades.Trades.get_apply_mapping_str_arr")
  * [Records.get_column_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_column_stack_record_indices "vectorbtpro.portfolio.trades.Trades.get_column_stack_record_indices")
  * [Records.get_field_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_arr "vectorbtpro.portfolio.trades.Trades.get_field_arr")
  * [Records.get_field_mapping](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_mapping "vectorbtpro.portfolio.trades.Trades.get_field_mapping")
  * [Records.get_field_name](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_name "vectorbtpro.portfolio.trades.Trades.get_field_name")
  * [Records.get_field_setting](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_setting "vectorbtpro.portfolio.trades.Trades.get_field_setting")
  * [Records.get_field_title](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_title "vectorbtpro.portfolio.trades.Trades.get_field_title")
  * [Records.get_map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field "vectorbtpro.portfolio.trades.Trades.get_map_field")
  * [Records.get_map_field_to_columns](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_columns "vectorbtpro.portfolio.trades.Trades.get_map_field_to_columns")
  * [Records.get_map_field_to_index](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_index "vectorbtpro.portfolio.trades.Trades.get_map_field_to_index")
  * [Records.get_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_pd_mask "vectorbtpro.portfolio.trades.Trades.get_pd_mask")
  * [Records.get_row_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_row_stack_record_indices "vectorbtpro.portfolio.trades.Trades.get_row_stack_record_indices")
  * [Records.has_conflicts](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.has_conflicts "vectorbtpro.portfolio.trades.Trades.has_conflicts")
  * [Records.is_sorted](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.is_sorted "vectorbtpro.portfolio.trades.Trades.is_sorted")
  * [Records.last_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.last_n "vectorbtpro.portfolio.trades.Trades.last_n")
  * [Records.map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map "vectorbtpro.portfolio.trades.Trades.map")
  * [Records.map_array](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_array "vectorbtpro.portfolio.trades.Trades.map_array")
  * [Records.map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_field "vectorbtpro.portfolio.trades.Trades.map_field")
  * [Records.override_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.override_field_config_doc "vectorbtpro.portfolio.trades.Trades.override_field_config_doc")
  * [Records.prepare_customdata](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.prepare_customdata "vectorbtpro.portfolio.trades.Trades.prepare_customdata")
  * [Records.random_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.random_n "vectorbtpro.portfolio.trades.Trades.random_n")
  * [Records.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.replace "vectorbtpro.portfolio.trades.Trades.replace")
  * [Records.resample_meta](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_meta "vectorbtpro.portfolio.trades.Trades.resample_meta")
  * [Records.resample_records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_records_arr "vectorbtpro.portfolio.trades.Trades.resample_records_arr")
  * [Records.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack "vectorbtpro.portfolio.trades.Trades.row_stack")
  * [Records.row_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack_records_arrs "vectorbtpro.portfolio.trades.Trades.row_stack_records_arrs")
  * [Records.select_cols](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.select_cols "vectorbtpro.portfolio.trades.Trades.select_cols")
  * [Records.sort](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.sort "vectorbtpro.portfolio.trades.Trades.sort")
  * [Records.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.to_readable "vectorbtpro.portfolio.trades.Trades.to_readable")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.portfolio.trades.Trades.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.portfolio.trades.Trades.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.portfolio.trades.Trades.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.trades.Trades.stats")
  * [Trades.avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.avg_duration "vectorbtpro.portfolio.trades.Trades.avg_duration")
  * [Trades.bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close "vectorbtpro.portfolio.trades.Trades.bar_close")
  * [Trades.bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close_time "vectorbtpro.portfolio.trades.Trades.bar_close_time")
  * [Trades.bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_high "vectorbtpro.portfolio.trades.Trades.bar_high")
  * [Trades.bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_low "vectorbtpro.portfolio.trades.Trades.bar_low")
  * [Trades.bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open "vectorbtpro.portfolio.trades.Trades.bar_open")
  * [Trades.bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open_time "vectorbtpro.portfolio.trades.Trades.bar_open_time")
  * [Trades.best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price "vectorbtpro.portfolio.trades.Trades.best_price")
  * [Trades.best_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price_idx "vectorbtpro.portfolio.trades.Trades.best_price_idx")
  * [Trades.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.portfolio.trades.Trades.close")
  * [Trades.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.portfolio.trades.Trades.cls_dir")
  * [Trades.col](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.col "vectorbtpro.portfolio.trades.Trades.col")
  * [Trades.col_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_arr "vectorbtpro.portfolio.trades.Trades.col_arr")
  * [Trades.col_mapper](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_mapper "vectorbtpro.portfolio.trades.Trades.col_mapper")
  * [Trades.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.portfolio.trades.Trades.column_only_select")
  * [Trades.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.portfolio.trades.Trades.config")
  * [Trades.coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.coverage "vectorbtpro.portfolio.trades.Trades.coverage")
  * [Trades.direction](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction "vectorbtpro.portfolio.trades.Trades.direction")
  * [Trades.direction_long](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction_long "vectorbtpro.portfolio.trades.Trades.direction_long")
  * [Trades.direction_short](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction_short "vectorbtpro.portfolio.trades.Trades.direction_short")
  * [Trades.duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.duration "vectorbtpro.portfolio.trades.Trades.duration")
  * [Trades.edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.edge_ratio "vectorbtpro.portfolio.trades.Trades.edge_ratio")
  * [Trades.end_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.end_idx "vectorbtpro.portfolio.trades.Trades.end_idx")
  * [Trades.entry_fees](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_fees "vectorbtpro.portfolio.trades.Trades.entry_fees")
  * [Trades.entry_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_idx "vectorbtpro.portfolio.trades.Trades.entry_idx")
  * [Trades.entry_order_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_order_id "vectorbtpro.portfolio.trades.Trades.entry_order_id")
  * [Trades.entry_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_price "vectorbtpro.portfolio.trades.Trades.entry_price")
  * [Trades.exit_fees](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_fees "vectorbtpro.portfolio.trades.Trades.exit_fees")
  * [Trades.exit_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_idx "vectorbtpro.portfolio.trades.Trades.exit_idx")
  * [Trades.exit_order_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_order_id "vectorbtpro.portfolio.trades.Trades.exit_order_id")
  * [Trades.exit_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_price "vectorbtpro.portfolio.trades.Trades.exit_price")
  * [Trades.expanding_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_best_price "vectorbtpro.portfolio.trades.Trades.expanding_best_price")
  * [Trades.expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae "vectorbtpro.portfolio.trades.Trades.expanding_mae")
  * [Trades.expanding_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae_returns "vectorbtpro.portfolio.trades.Trades.expanding_mae_returns")
  * [Trades.expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe "vectorbtpro.portfolio.trades.Trades.expanding_mfe")
  * [Trades.expanding_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns "vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns")
  * [Trades.expanding_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_worst_price "vectorbtpro.portfolio.trades.Trades.expanding_worst_price")
  * [Trades.expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expectancy "vectorbtpro.portfolio.trades.Trades.expectancy")
  * [Trades.field_names](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.field_names "vectorbtpro.portfolio.trades.Trades.field_names")
  * [Trades.first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_idx "vectorbtpro.portfolio.trades.Trades.first_idx")
  * [Trades.first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_pd_mask "vectorbtpro.portfolio.trades.Trades.first_pd_mask")
  * [Trades.get_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price "vectorbtpro.portfolio.trades.Trades.get_best_price")
  * [Trades.get_best_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price_idx "vectorbtpro.portfolio.trades.Trades.get_best_price_idx")
  * [Trades.get_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_edge_ratio "vectorbtpro.portfolio.trades.Trades.get_edge_ratio")
  * [Trades.get_expanding_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_best_price "vectorbtpro.portfolio.trades.Trades.get_expanding_best_price")
  * [Trades.get_expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mae "vectorbtpro.portfolio.trades.Trades.get_expanding_mae")
  * [Trades.get_expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mfe "vectorbtpro.portfolio.trades.Trades.get_expanding_mfe")
  * [Trades.get_expanding_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price "vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price")
  * [Trades.get_expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expectancy "vectorbtpro.portfolio.trades.Trades.get_expectancy")
  * [Trades.get_long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_long_view "vectorbtpro.portfolio.trades.Trades.get_long_view")
  * [Trades.get_losing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing "vectorbtpro.portfolio.trades.Trades.get_losing")
  * [Trades.get_losing_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing_streak "vectorbtpro.portfolio.trades.Trades.get_losing_streak")
  * [Trades.get_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mae "vectorbtpro.portfolio.trades.Trades.get_mae")
  * [Trades.get_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mfe "vectorbtpro.portfolio.trades.Trades.get_mfe")
  * [Trades.get_profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_profit_factor "vectorbtpro.portfolio.trades.Trades.get_profit_factor")
  * [Trades.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_ranges "vectorbtpro.portfolio.trades.Trades.get_ranges")
  * [Trades.get_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio "vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio")
  * [Trades.get_short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_short_view "vectorbtpro.portfolio.trades.Trades.get_short_view")
  * [Trades.get_sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_sqn "vectorbtpro.portfolio.trades.Trades.get_sqn")
  * [Trades.get_win_rate](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_win_rate "vectorbtpro.portfolio.trades.Trades.get_win_rate")
  * [Trades.get_winning](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning "vectorbtpro.portfolio.trades.Trades.get_winning")
  * [Trades.get_winning_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning_streak "vectorbtpro.portfolio.trades.Trades.get_winning_streak")
  * [Trades.get_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price "vectorbtpro.portfolio.trades.Trades.get_worst_price")
  * [Trades.get_worst_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price_idx "vectorbtpro.portfolio.trades.Trades.get_worst_price_idx")
  * [Trades.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.portfolio.trades.Trades.group_select")
  * [Trades.high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.high "vectorbtpro.portfolio.trades.Trades.high")
  * [Trades.id](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.id "vectorbtpro.portfolio.trades.Trades.id")
  * [Trades.id_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.id_arr "vectorbtpro.portfolio.trades.Trades.id_arr")
  * [Trades.idx_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.idx_arr "vectorbtpro.portfolio.trades.Trades.idx_arr")
  * [Trades.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.portfolio.trades.Trades.iloc")
  * [Trades.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.portfolio.trades.Trades.indexing_kwargs")
  * [Trades.invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.invalid "vectorbtpro.portfolio.trades.Trades.invalid")
  * [Trades.last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_idx "vectorbtpro.portfolio.trades.Trades.last_idx")
  * [Trades.last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_pd_mask "vectorbtpro.portfolio.trades.Trades.last_pd_mask")
  * [Trades.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.portfolio.trades.Trades.loc")
  * [Trades.long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.long_view "vectorbtpro.portfolio.trades.Trades.long_view")
  * [Trades.losing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.losing "vectorbtpro.portfolio.trades.Trades.losing")
  * [Trades.losing_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.losing_streak "vectorbtpro.portfolio.trades.Trades.losing_streak")
  * [Trades.low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.low "vectorbtpro.portfolio.trades.Trades.low")
  * [Trades.mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae "vectorbtpro.portfolio.trades.Trades.mae")
  * [Trades.mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae_returns "vectorbtpro.portfolio.trades.Trades.mae_returns")
  * [Trades.max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.max_duration "vectorbtpro.portfolio.trades.Trades.max_duration")
  * [Trades.mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe "vectorbtpro.portfolio.trades.Trades.mfe")
  * [Trades.mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe_returns "vectorbtpro.portfolio.trades.Trades.mfe_returns")
  * [Trades.open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.open "vectorbtpro.portfolio.trades.Trades.open")
  * [Trades.overlap_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.overlap_coverage "vectorbtpro.portfolio.trades.Trades.overlap_coverage")
  * [Trades.parent_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.parent_id "vectorbtpro.portfolio.trades.Trades.parent_id")
  * [Trades.pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.pd_mask "vectorbtpro.portfolio.trades.Trades.pd_mask")
  * [Trades.plot](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot "vectorbtpro.portfolio.trades.Trades.plot")
  * [Trades.plot_against_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_against_pnl "vectorbtpro.portfolio.trades.Trades.plot_against_pnl")
  * [Trades.plot_expanding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding "vectorbtpro.portfolio.trades.Trades.plot_expanding")
  * [Trades.plot_expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mae "vectorbtpro.portfolio.trades.Trades.plot_expanding_mae")
  * [Trades.plot_expanding_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mae_returns "vectorbtpro.portfolio.trades.Trades.plot_expanding_mae_returns")
  * [Trades.plot_expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe "vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe")
  * [Trades.plot_expanding_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe_returns "vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe_returns")
  * [Trades.plot_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mae "vectorbtpro.portfolio.trades.Trades.plot_mae")
  * [Trades.plot_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mae_returns "vectorbtpro.portfolio.trades.Trades.plot_mae_returns")
  * [Trades.plot_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mfe "vectorbtpro.portfolio.trades.Trades.plot_mfe")
  * [Trades.plot_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mfe_returns "vectorbtpro.portfolio.trades.Trades.plot_mfe_returns")
  * [Trades.plot_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_pnl "vectorbtpro.portfolio.trades.Trades.plot_pnl")
  * [Trades.plot_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_returns "vectorbtpro.portfolio.trades.Trades.plot_returns")
  * [Trades.plot_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_running_edge_ratio "vectorbtpro.portfolio.trades.Trades.plot_running_edge_ratio")
  * [Trades.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plots_defaults "vectorbtpro.portfolio.trades.Trades.plots_defaults")
  * [Trades.pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.pnl "vectorbtpro.portfolio.trades.Trades.pnl")
  * [Trades.profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.profit_factor "vectorbtpro.portfolio.trades.Trades.profit_factor")
  * [Trades.projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.projections "vectorbtpro.portfolio.trades.Trades.projections")
  * [Trades.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.portfolio.trades.Trades.range_only_select")
  * [Trades.ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.ranges "vectorbtpro.portfolio.trades.Trades.ranges")
  * [Trades.ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.ranges_pd_mask "vectorbtpro.portfolio.trades.Trades.ranges_pd_mask")
  * [Trades.readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.readable "vectorbtpro.portfolio.trades.Trades.readable")
  * [Trades.real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.real_duration "vectorbtpro.portfolio.trades.Trades.real_duration")
  * [Trades.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.portfolio.trades.Trades.rec_state")
  * [Trades.recarray](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.recarray "vectorbtpro.portfolio.trades.Trades.recarray")
  * [Trades.records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records "vectorbtpro.portfolio.trades.Trades.records")
  * [Trades.records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_arr "vectorbtpro.portfolio.trades.Trades.records_arr")
  * [Trades.records_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_readable "vectorbtpro.portfolio.trades.Trades.records_readable")
  * [Trades.rel_expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_expectancy "vectorbtpro.portfolio.trades.Trades.rel_expectancy")
  * [Trades.rel_profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_profit_factor "vectorbtpro.portfolio.trades.Trades.rel_profit_factor")
  * [Trades.rel_sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_sqn "vectorbtpro.portfolio.trades.Trades.rel_sqn")
  * [Trades.returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.returns "vectorbtpro.portfolio.trades.Trades.returns")
  * [Trades.running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.running_edge_ratio "vectorbtpro.portfolio.trades.Trades.running_edge_ratio")
  * [Trades.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.portfolio.trades.Trades.self_aliases")
  * [Trades.short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.short_view "vectorbtpro.portfolio.trades.Trades.short_view")
  * [Trades.size](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.size "vectorbtpro.portfolio.trades.Trades.size")
  * [Trades.sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.sqn "vectorbtpro.portfolio.trades.Trades.sqn")
  * [Trades.start_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.start_idx "vectorbtpro.portfolio.trades.Trades.start_idx")
  * [Trades.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.stats_defaults "vectorbtpro.portfolio.trades.Trades.stats_defaults")
  * [Trades.status](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status "vectorbtpro.portfolio.trades.Trades.status")
  * [Trades.status_closed](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_closed "vectorbtpro.portfolio.trades.Trades.status_closed")
  * [Trades.status_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_open "vectorbtpro.portfolio.trades.Trades.status_open")
  * [Trades.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.portfolio.trades.Trades.unwrapped")
  * [Trades.valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.valid "vectorbtpro.portfolio.trades.Trades.valid")
  * [Trades.values](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.values "vectorbtpro.portfolio.trades.Trades.values")
  * [Trades.win_rate](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.win_rate "vectorbtpro.portfolio.trades.Trades.win_rate")
  * [Trades.winning](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.winning "vectorbtpro.portfolio.trades.Trades.winning")
  * [Trades.winning_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.winning_streak "vectorbtpro.portfolio.trades.Trades.winning_streak")
  * [Trades.worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price "vectorbtpro.portfolio.trades.Trades.worst_price")
  * [Trades.worst_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price_idx "vectorbtpro.portfolio.trades.Trades.worst_price_idx")
  * [Trades.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.portfolio.trades.Trades.wrapper")
  * [Trades.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.portfolio.trades.Trades.xloc")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.portfolio.trades.Trades.apply_to_index")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.portfolio.trades.Trades.regroup")
  * [Wrapping.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "vectorbtpro.portfolio.trades.Trades.resolve_self")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_stack_kwargs")



* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades.field_config "Permanent link")

Field config of [EntryTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades "vectorbtpro.portfolio.trades.EntryTrades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-5)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-6)        ('entry_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-7)        ('entry_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-8)        ('entry_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-9)        ('entry_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-10)        ('exit_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-11)        ('exit_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-12)        ('exit_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-13)        ('exit_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-14)        ('pnl', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-15)        ('return', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-16)        ('direction', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-17)        ('status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-18)        ('parent_id', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-19)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-20)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-21)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-22)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-23)            title='Entry Trade Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-24)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-25)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-26)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-27)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-28)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-29)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-30)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-31)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-32)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-33)            name='entry_idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-34)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-35)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-36)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-37)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-38)            title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-39)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-40)            name='entry_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-41)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-42)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-43)            title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-44)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-45)            name='exit_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-46)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-47)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-48)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-49)            mapping=TradeStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-50)                Open=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-51)                Closed=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-52)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-53)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-54)        size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-55)            title='Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-56)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-57)        entry_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-58)            title='Entry Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-59)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-60)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-61)        entry_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-62)            title='Entry Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-63)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-64)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-65)        entry_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-66)            title='Avg Entry Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-67)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-68)        entry_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-69)            title='Entry Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-70)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-71)        exit_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-72)            title='Exit Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-73)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-74)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-75)        exit_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-76)            title='Exit Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-77)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-78)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-79)        exit_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-80)            title='Avg Exit Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-81)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-82)        exit_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-83)            title='Exit Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-84)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-85)        pnl=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-86)            title='PnL'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-87)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-88)        return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-89)            title='Return',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-90)            hovertemplate='$title: %{customdata[$index]:,%}'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-91)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-92)        direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-93)            title='Direction',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-94)            mapping=TradeDirectionT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-95)                Long=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-96)                Short=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-97)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-98)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-99)        parent_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-100)            title='Position Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-101)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-102)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-103)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-19-104))
    

Returns `EntryTrades._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `EntryTrades._field_config`.

* * *

### from_orders class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2426-L2470 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades.from_orders "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-1)EntryTrades.from_orders(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-2)    orders,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-3)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-4)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-5)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-6)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-7)    init_position=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-8)    init_price=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-9)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-10)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-11)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-12)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-13)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-20-14))
    

Build [EntryTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades "vectorbtpro.portfolio.trades.EntryTrades") from [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").

* * *

### plot_signals method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2472-L2639 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades.plot_signals "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-1)EntryTrades.plot_signals(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-3)    plot_ohlc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-4)    plot_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-5)    ohlc_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-6)    ohlc_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-7)    close_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-8)    long_entry_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-9)    short_entry_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-10)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-11)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-12)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-21-13))
    

Plot entry trade signals.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`plot_ohlc`** : `bool`
    Whether to plot OHLC.
**`plot_close`** : `bool`
    Whether to plot close.
**`ohlc_type`**
    

Either 'OHLC', 'Candlestick' or Plotly trace.

Pass None to use the default.

**`ohlc_trace_kwargs`** : `dict`
    Keyword arguments passed to `ohlc_type`.
**`close_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [EntryTrades.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.portfolio.trades.EntryTrades.close").
**`long_entry_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Long Entry" markers.
**`short_entry_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Short Entry" markers.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-22-1)>>> index = pd.date_range("2020", periods=7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-22-2)>>> price = pd.Series([1, 2, 3, 2, 3, 4, 3], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-22-3)>>> orders = pd.Series([1, 0, -1, 0, -1, 2, -2], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-22-4)>>> pf = vbt.Portfolio.from_orders(price, orders)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-22-5)>>> pf.entry_trades.plot_signals().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/entry_trades_plot_signals.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/entry_trades_plot_signals.dark.svg#only-dark)

* * *

## ExitTrades class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2662-L2879 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-1)ExitTrades(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-23-9))
    

Extends [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades") for working with exit trade records.

**Superclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")
  * [IndexApplier](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "vectorbtpro.base.indexes.IndexApplier")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords "vectorbtpro.generic.price_records.PriceRecords")
  * [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges")
  * [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.portfolio.trades.Trades.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.portfolio.trades.Trades.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.portfolio.trades.Trades.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.portfolio.trades.Trades.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.portfolio.trades.Trades.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.portfolio.trades.Trades.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.portfolio.trades.Trades.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.portfolio.trades.Trades.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.portfolio.trades.Trades.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.portfolio.trades.Trades.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.portfolio.trades.Trades.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.portfolio.trades.Trades.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.portfolio.trades.Trades.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.portfolio.trades.Trades.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.portfolio.trades.Trades.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.portfolio.trades.Trades.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.portfolio.trades.Trades.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.portfolio.trades.Trades.prettify")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.portfolio.trades.Trades.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.portfolio.trades.Trades.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.portfolio.trades.Trades.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.portfolio.trades.Trades.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.portfolio.trades.Trades.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.portfolio.trades.Trades.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.portfolio.trades.Trades.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.portfolio.trades.Trades.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.portfolio.trades.Trades.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.portfolio.trades.Trades.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.portfolio.trades.Trades.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.portfolio.trades.Trades.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.portfolio.trades.Trades.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.portfolio.trades.Trades.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.portfolio.trades.Trades.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.portfolio.trades.Trades.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.portfolio.trades.Trades.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.portfolio.trades.Trades.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.portfolio.trades.Trades.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.portfolio.trades.Trades.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.portfolio.trades.Trades.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.portfolio.trades.Trades.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.portfolio.trades.Trades.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.portfolio.trades.Trades.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.portfolio.trades.Trades.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.portfolio.trades.Trades.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.portfolio.trades.Trades.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.portfolio.trades.Trades.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.portfolio.trades.Trades.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.portfolio.trades.Trades.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.portfolio.trades.Trades.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.portfolio.trades.Trades.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.portfolio.trades.Trades.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.portfolio.trades.Trades.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.portfolio.trades.Trades.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.portfolio.trades.Trades.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.portfolio.trades.Trades.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.portfolio.trades.Trades.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.portfolio.trades.Trades.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.portfolio.trades.Trades.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.portfolio.trades.Trades.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.portfolio.trades.Trades.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.portfolio.trades.Trades.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.portfolio.trades.Trades.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.portfolio.trades.Trades.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.portfolio.trades.Trades.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.portfolio.trades.Trades.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.portfolio.trades.Trades.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.portfolio.trades.Trades.pprint")
  * [PriceRecords.from_records](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.from_records "vectorbtpro.portfolio.trades.Trades.from_records")
  * [PriceRecords.get_bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close "vectorbtpro.portfolio.trades.Trades.get_bar_close")
  * [PriceRecords.get_bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close_time "vectorbtpro.portfolio.trades.Trades.get_bar_close_time")
  * [PriceRecords.get_bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_high "vectorbtpro.portfolio.trades.Trades.get_bar_high")
  * [PriceRecords.get_bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_low "vectorbtpro.portfolio.trades.Trades.get_bar_low")
  * [PriceRecords.get_bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open "vectorbtpro.portfolio.trades.Trades.get_bar_open")
  * [PriceRecords.get_bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open_time "vectorbtpro.portfolio.trades.Trades.get_bar_open_time")
  * [PriceRecords.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func "vectorbtpro.portfolio.trades.Trades.indexing_func")
  * [PriceRecords.indexing_func_meta](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func_meta "vectorbtpro.portfolio.trades.Trades.indexing_func_meta")
  * [PriceRecords.resample](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resample "vectorbtpro.portfolio.trades.Trades.resample")
  * [PriceRecords.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_column_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_column_stack_kwargs")
  * [PriceRecords.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_row_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_row_stack_kwargs")
  * [Ranges.crop](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.crop "vectorbtpro.portfolio.trades.Trades.crop")
  * [Ranges.filter_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_max_duration "vectorbtpro.portfolio.trades.Trades.filter_max_duration")
  * [Ranges.filter_min_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_min_duration "vectorbtpro.portfolio.trades.Trades.filter_min_duration")
  * [Ranges.from_array](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_array "vectorbtpro.portfolio.trades.Trades.from_array")
  * [Ranges.from_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta "vectorbtpro.portfolio.trades.Trades.from_delta")
  * [Ranges.get_avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_avg_duration "vectorbtpro.portfolio.trades.Trades.get_avg_duration")
  * [Ranges.get_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_coverage "vectorbtpro.portfolio.trades.Trades.get_coverage")
  * [Ranges.get_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_duration "vectorbtpro.portfolio.trades.Trades.get_duration")
  * [Ranges.get_first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_idx "vectorbtpro.portfolio.trades.Trades.get_first_idx")
  * [Ranges.get_first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_pd_mask "vectorbtpro.portfolio.trades.Trades.get_first_pd_mask")
  * [Ranges.get_invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_invalid "vectorbtpro.portfolio.trades.Trades.get_invalid")
  * [Ranges.get_last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_idx "vectorbtpro.portfolio.trades.Trades.get_last_idx")
  * [Ranges.get_last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_pd_mask "vectorbtpro.portfolio.trades.Trades.get_last_pd_mask")
  * [Ranges.get_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_max_duration "vectorbtpro.portfolio.trades.Trades.get_max_duration")
  * [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.portfolio.trades.Trades.get_projections")
  * [Ranges.get_ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_ranges_pd_mask "vectorbtpro.portfolio.trades.Trades.get_ranges_pd_mask")
  * [Ranges.get_real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_real_duration "vectorbtpro.portfolio.trades.Trades.get_real_duration")
  * [Ranges.get_valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_valid "vectorbtpro.portfolio.trades.Trades.get_valid")
  * [Ranges.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections "vectorbtpro.portfolio.trades.Trades.plot_projections")
  * [Ranges.plot_shapes](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_shapes "vectorbtpro.portfolio.trades.Trades.plot_shapes")
  * [Ranges.with_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.with_delta "vectorbtpro.portfolio.trades.Trades.with_delta")
  * [Records.apply](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply "vectorbtpro.portfolio.trades.Trades.apply")
  * [Records.apply_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply_mask "vectorbtpro.portfolio.trades.Trades.apply_mask")
  * [Records.build_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.build_field_config_doc "vectorbtpro.portfolio.trades.Trades.build_field_config_doc")
  * [Records.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack "vectorbtpro.portfolio.trades.Trades.column_stack")
  * [Records.column_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack_records_arrs "vectorbtpro.portfolio.trades.Trades.column_stack_records_arrs")
  * [Records.count](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.count "vectorbtpro.portfolio.trades.Trades.count")
  * [Records.coverage_map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.coverage_map "vectorbtpro.portfolio.trades.Trades.coverage_map")
  * [Records.first_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.first_n "vectorbtpro.portfolio.trades.Trades.first_n")
  * [Records.get_apply_mapping_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_arr "vectorbtpro.portfolio.trades.Trades.get_apply_mapping_arr")
  * [Records.get_apply_mapping_str_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_str_arr "vectorbtpro.portfolio.trades.Trades.get_apply_mapping_str_arr")
  * [Records.get_column_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_column_stack_record_indices "vectorbtpro.portfolio.trades.Trades.get_column_stack_record_indices")
  * [Records.get_field_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_arr "vectorbtpro.portfolio.trades.Trades.get_field_arr")
  * [Records.get_field_mapping](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_mapping "vectorbtpro.portfolio.trades.Trades.get_field_mapping")
  * [Records.get_field_name](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_name "vectorbtpro.portfolio.trades.Trades.get_field_name")
  * [Records.get_field_setting](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_setting "vectorbtpro.portfolio.trades.Trades.get_field_setting")
  * [Records.get_field_title](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_title "vectorbtpro.portfolio.trades.Trades.get_field_title")
  * [Records.get_map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field "vectorbtpro.portfolio.trades.Trades.get_map_field")
  * [Records.get_map_field_to_columns](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_columns "vectorbtpro.portfolio.trades.Trades.get_map_field_to_columns")
  * [Records.get_map_field_to_index](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_index "vectorbtpro.portfolio.trades.Trades.get_map_field_to_index")
  * [Records.get_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_pd_mask "vectorbtpro.portfolio.trades.Trades.get_pd_mask")
  * [Records.get_row_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_row_stack_record_indices "vectorbtpro.portfolio.trades.Trades.get_row_stack_record_indices")
  * [Records.has_conflicts](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.has_conflicts "vectorbtpro.portfolio.trades.Trades.has_conflicts")
  * [Records.is_sorted](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.is_sorted "vectorbtpro.portfolio.trades.Trades.is_sorted")
  * [Records.last_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.last_n "vectorbtpro.portfolio.trades.Trades.last_n")
  * [Records.map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map "vectorbtpro.portfolio.trades.Trades.map")
  * [Records.map_array](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_array "vectorbtpro.portfolio.trades.Trades.map_array")
  * [Records.map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_field "vectorbtpro.portfolio.trades.Trades.map_field")
  * [Records.override_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.override_field_config_doc "vectorbtpro.portfolio.trades.Trades.override_field_config_doc")
  * [Records.prepare_customdata](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.prepare_customdata "vectorbtpro.portfolio.trades.Trades.prepare_customdata")
  * [Records.random_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.random_n "vectorbtpro.portfolio.trades.Trades.random_n")
  * [Records.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.replace "vectorbtpro.portfolio.trades.Trades.replace")
  * [Records.resample_meta](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_meta "vectorbtpro.portfolio.trades.Trades.resample_meta")
  * [Records.resample_records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_records_arr "vectorbtpro.portfolio.trades.Trades.resample_records_arr")
  * [Records.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack "vectorbtpro.portfolio.trades.Trades.row_stack")
  * [Records.row_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack_records_arrs "vectorbtpro.portfolio.trades.Trades.row_stack_records_arrs")
  * [Records.select_cols](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.select_cols "vectorbtpro.portfolio.trades.Trades.select_cols")
  * [Records.sort](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.sort "vectorbtpro.portfolio.trades.Trades.sort")
  * [Records.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.to_readable "vectorbtpro.portfolio.trades.Trades.to_readable")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.portfolio.trades.Trades.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.portfolio.trades.Trades.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.portfolio.trades.Trades.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.trades.Trades.stats")
  * [Trades.avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.avg_duration "vectorbtpro.portfolio.trades.Trades.avg_duration")
  * [Trades.bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close "vectorbtpro.portfolio.trades.Trades.bar_close")
  * [Trades.bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close_time "vectorbtpro.portfolio.trades.Trades.bar_close_time")
  * [Trades.bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_high "vectorbtpro.portfolio.trades.Trades.bar_high")
  * [Trades.bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_low "vectorbtpro.portfolio.trades.Trades.bar_low")
  * [Trades.bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open "vectorbtpro.portfolio.trades.Trades.bar_open")
  * [Trades.bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open_time "vectorbtpro.portfolio.trades.Trades.bar_open_time")
  * [Trades.best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price "vectorbtpro.portfolio.trades.Trades.best_price")
  * [Trades.best_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price_idx "vectorbtpro.portfolio.trades.Trades.best_price_idx")
  * [Trades.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.portfolio.trades.Trades.close")
  * [Trades.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.portfolio.trades.Trades.cls_dir")
  * [Trades.col](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.col "vectorbtpro.portfolio.trades.Trades.col")
  * [Trades.col_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_arr "vectorbtpro.portfolio.trades.Trades.col_arr")
  * [Trades.col_mapper](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_mapper "vectorbtpro.portfolio.trades.Trades.col_mapper")
  * [Trades.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.portfolio.trades.Trades.column_only_select")
  * [Trades.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.portfolio.trades.Trades.config")
  * [Trades.coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.coverage "vectorbtpro.portfolio.trades.Trades.coverage")
  * [Trades.direction](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction "vectorbtpro.portfolio.trades.Trades.direction")
  * [Trades.direction_long](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction_long "vectorbtpro.portfolio.trades.Trades.direction_long")
  * [Trades.direction_short](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction_short "vectorbtpro.portfolio.trades.Trades.direction_short")
  * [Trades.duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.duration "vectorbtpro.portfolio.trades.Trades.duration")
  * [Trades.edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.edge_ratio "vectorbtpro.portfolio.trades.Trades.edge_ratio")
  * [Trades.end_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.end_idx "vectorbtpro.portfolio.trades.Trades.end_idx")
  * [Trades.entry_fees](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_fees "vectorbtpro.portfolio.trades.Trades.entry_fees")
  * [Trades.entry_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_idx "vectorbtpro.portfolio.trades.Trades.entry_idx")
  * [Trades.entry_order_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_order_id "vectorbtpro.portfolio.trades.Trades.entry_order_id")
  * [Trades.entry_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_price "vectorbtpro.portfolio.trades.Trades.entry_price")
  * [Trades.exit_fees](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_fees "vectorbtpro.portfolio.trades.Trades.exit_fees")
  * [Trades.exit_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_idx "vectorbtpro.portfolio.trades.Trades.exit_idx")
  * [Trades.exit_order_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_order_id "vectorbtpro.portfolio.trades.Trades.exit_order_id")
  * [Trades.exit_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_price "vectorbtpro.portfolio.trades.Trades.exit_price")
  * [Trades.expanding_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_best_price "vectorbtpro.portfolio.trades.Trades.expanding_best_price")
  * [Trades.expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae "vectorbtpro.portfolio.trades.Trades.expanding_mae")
  * [Trades.expanding_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae_returns "vectorbtpro.portfolio.trades.Trades.expanding_mae_returns")
  * [Trades.expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe "vectorbtpro.portfolio.trades.Trades.expanding_mfe")
  * [Trades.expanding_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns "vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns")
  * [Trades.expanding_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_worst_price "vectorbtpro.portfolio.trades.Trades.expanding_worst_price")
  * [Trades.expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expectancy "vectorbtpro.portfolio.trades.Trades.expectancy")
  * [Trades.field_names](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.field_names "vectorbtpro.portfolio.trades.Trades.field_names")
  * [Trades.first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_idx "vectorbtpro.portfolio.trades.Trades.first_idx")
  * [Trades.first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_pd_mask "vectorbtpro.portfolio.trades.Trades.first_pd_mask")
  * [Trades.get_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price "vectorbtpro.portfolio.trades.Trades.get_best_price")
  * [Trades.get_best_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price_idx "vectorbtpro.portfolio.trades.Trades.get_best_price_idx")
  * [Trades.get_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_edge_ratio "vectorbtpro.portfolio.trades.Trades.get_edge_ratio")
  * [Trades.get_expanding_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_best_price "vectorbtpro.portfolio.trades.Trades.get_expanding_best_price")
  * [Trades.get_expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mae "vectorbtpro.portfolio.trades.Trades.get_expanding_mae")
  * [Trades.get_expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mfe "vectorbtpro.portfolio.trades.Trades.get_expanding_mfe")
  * [Trades.get_expanding_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price "vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price")
  * [Trades.get_expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expectancy "vectorbtpro.portfolio.trades.Trades.get_expectancy")
  * [Trades.get_long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_long_view "vectorbtpro.portfolio.trades.Trades.get_long_view")
  * [Trades.get_losing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing "vectorbtpro.portfolio.trades.Trades.get_losing")
  * [Trades.get_losing_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing_streak "vectorbtpro.portfolio.trades.Trades.get_losing_streak")
  * [Trades.get_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mae "vectorbtpro.portfolio.trades.Trades.get_mae")
  * [Trades.get_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mfe "vectorbtpro.portfolio.trades.Trades.get_mfe")
  * [Trades.get_profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_profit_factor "vectorbtpro.portfolio.trades.Trades.get_profit_factor")
  * [Trades.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_ranges "vectorbtpro.portfolio.trades.Trades.get_ranges")
  * [Trades.get_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio "vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio")
  * [Trades.get_short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_short_view "vectorbtpro.portfolio.trades.Trades.get_short_view")
  * [Trades.get_sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_sqn "vectorbtpro.portfolio.trades.Trades.get_sqn")
  * [Trades.get_win_rate](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_win_rate "vectorbtpro.portfolio.trades.Trades.get_win_rate")
  * [Trades.get_winning](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning "vectorbtpro.portfolio.trades.Trades.get_winning")
  * [Trades.get_winning_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning_streak "vectorbtpro.portfolio.trades.Trades.get_winning_streak")
  * [Trades.get_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price "vectorbtpro.portfolio.trades.Trades.get_worst_price")
  * [Trades.get_worst_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price_idx "vectorbtpro.portfolio.trades.Trades.get_worst_price_idx")
  * [Trades.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.portfolio.trades.Trades.group_select")
  * [Trades.high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.high "vectorbtpro.portfolio.trades.Trades.high")
  * [Trades.id](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.id "vectorbtpro.portfolio.trades.Trades.id")
  * [Trades.id_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.id_arr "vectorbtpro.portfolio.trades.Trades.id_arr")
  * [Trades.idx_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.idx_arr "vectorbtpro.portfolio.trades.Trades.idx_arr")
  * [Trades.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.portfolio.trades.Trades.iloc")
  * [Trades.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.portfolio.trades.Trades.indexing_kwargs")
  * [Trades.invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.invalid "vectorbtpro.portfolio.trades.Trades.invalid")
  * [Trades.last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_idx "vectorbtpro.portfolio.trades.Trades.last_idx")
  * [Trades.last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_pd_mask "vectorbtpro.portfolio.trades.Trades.last_pd_mask")
  * [Trades.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.portfolio.trades.Trades.loc")
  * [Trades.long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.long_view "vectorbtpro.portfolio.trades.Trades.long_view")
  * [Trades.losing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.losing "vectorbtpro.portfolio.trades.Trades.losing")
  * [Trades.losing_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.losing_streak "vectorbtpro.portfolio.trades.Trades.losing_streak")
  * [Trades.low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.low "vectorbtpro.portfolio.trades.Trades.low")
  * [Trades.mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae "vectorbtpro.portfolio.trades.Trades.mae")
  * [Trades.mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae_returns "vectorbtpro.portfolio.trades.Trades.mae_returns")
  * [Trades.max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.max_duration "vectorbtpro.portfolio.trades.Trades.max_duration")
  * [Trades.mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe "vectorbtpro.portfolio.trades.Trades.mfe")
  * [Trades.mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe_returns "vectorbtpro.portfolio.trades.Trades.mfe_returns")
  * [Trades.open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.open "vectorbtpro.portfolio.trades.Trades.open")
  * [Trades.overlap_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.overlap_coverage "vectorbtpro.portfolio.trades.Trades.overlap_coverage")
  * [Trades.parent_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.parent_id "vectorbtpro.portfolio.trades.Trades.parent_id")
  * [Trades.pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.pd_mask "vectorbtpro.portfolio.trades.Trades.pd_mask")
  * [Trades.plot](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot "vectorbtpro.portfolio.trades.Trades.plot")
  * [Trades.plot_against_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_against_pnl "vectorbtpro.portfolio.trades.Trades.plot_against_pnl")
  * [Trades.plot_expanding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding "vectorbtpro.portfolio.trades.Trades.plot_expanding")
  * [Trades.plot_expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mae "vectorbtpro.portfolio.trades.Trades.plot_expanding_mae")
  * [Trades.plot_expanding_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mae_returns "vectorbtpro.portfolio.trades.Trades.plot_expanding_mae_returns")
  * [Trades.plot_expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe "vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe")
  * [Trades.plot_expanding_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe_returns "vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe_returns")
  * [Trades.plot_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mae "vectorbtpro.portfolio.trades.Trades.plot_mae")
  * [Trades.plot_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mae_returns "vectorbtpro.portfolio.trades.Trades.plot_mae_returns")
  * [Trades.plot_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mfe "vectorbtpro.portfolio.trades.Trades.plot_mfe")
  * [Trades.plot_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mfe_returns "vectorbtpro.portfolio.trades.Trades.plot_mfe_returns")
  * [Trades.plot_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_pnl "vectorbtpro.portfolio.trades.Trades.plot_pnl")
  * [Trades.plot_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_returns "vectorbtpro.portfolio.trades.Trades.plot_returns")
  * [Trades.plot_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_running_edge_ratio "vectorbtpro.portfolio.trades.Trades.plot_running_edge_ratio")
  * [Trades.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plots_defaults "vectorbtpro.portfolio.trades.Trades.plots_defaults")
  * [Trades.pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.pnl "vectorbtpro.portfolio.trades.Trades.pnl")
  * [Trades.profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.profit_factor "vectorbtpro.portfolio.trades.Trades.profit_factor")
  * [Trades.projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.projections "vectorbtpro.portfolio.trades.Trades.projections")
  * [Trades.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.portfolio.trades.Trades.range_only_select")
  * [Trades.ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.ranges "vectorbtpro.portfolio.trades.Trades.ranges")
  * [Trades.ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.ranges_pd_mask "vectorbtpro.portfolio.trades.Trades.ranges_pd_mask")
  * [Trades.readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.readable "vectorbtpro.portfolio.trades.Trades.readable")
  * [Trades.real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.real_duration "vectorbtpro.portfolio.trades.Trades.real_duration")
  * [Trades.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.portfolio.trades.Trades.rec_state")
  * [Trades.recarray](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.recarray "vectorbtpro.portfolio.trades.Trades.recarray")
  * [Trades.records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records "vectorbtpro.portfolio.trades.Trades.records")
  * [Trades.records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_arr "vectorbtpro.portfolio.trades.Trades.records_arr")
  * [Trades.records_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_readable "vectorbtpro.portfolio.trades.Trades.records_readable")
  * [Trades.rel_expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_expectancy "vectorbtpro.portfolio.trades.Trades.rel_expectancy")
  * [Trades.rel_profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_profit_factor "vectorbtpro.portfolio.trades.Trades.rel_profit_factor")
  * [Trades.rel_sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_sqn "vectorbtpro.portfolio.trades.Trades.rel_sqn")
  * [Trades.returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.returns "vectorbtpro.portfolio.trades.Trades.returns")
  * [Trades.running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.running_edge_ratio "vectorbtpro.portfolio.trades.Trades.running_edge_ratio")
  * [Trades.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.portfolio.trades.Trades.self_aliases")
  * [Trades.short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.short_view "vectorbtpro.portfolio.trades.Trades.short_view")
  * [Trades.size](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.size "vectorbtpro.portfolio.trades.Trades.size")
  * [Trades.sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.sqn "vectorbtpro.portfolio.trades.Trades.sqn")
  * [Trades.start_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.start_idx "vectorbtpro.portfolio.trades.Trades.start_idx")
  * [Trades.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.stats_defaults "vectorbtpro.portfolio.trades.Trades.stats_defaults")
  * [Trades.status](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status "vectorbtpro.portfolio.trades.Trades.status")
  * [Trades.status_closed](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_closed "vectorbtpro.portfolio.trades.Trades.status_closed")
  * [Trades.status_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_open "vectorbtpro.portfolio.trades.Trades.status_open")
  * [Trades.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.portfolio.trades.Trades.unwrapped")
  * [Trades.valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.valid "vectorbtpro.portfolio.trades.Trades.valid")
  * [Trades.values](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.values "vectorbtpro.portfolio.trades.Trades.values")
  * [Trades.win_rate](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.win_rate "vectorbtpro.portfolio.trades.Trades.win_rate")
  * [Trades.winning](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.winning "vectorbtpro.portfolio.trades.Trades.winning")
  * [Trades.winning_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.winning_streak "vectorbtpro.portfolio.trades.Trades.winning_streak")
  * [Trades.worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price "vectorbtpro.portfolio.trades.Trades.worst_price")
  * [Trades.worst_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price_idx "vectorbtpro.portfolio.trades.Trades.worst_price_idx")
  * [Trades.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.portfolio.trades.Trades.wrapper")
  * [Trades.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.portfolio.trades.Trades.xloc")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.portfolio.trades.Trades.apply_to_index")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.portfolio.trades.Trades.regroup")
  * [Wrapping.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "vectorbtpro.portfolio.trades.Trades.resolve_self")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_stack_kwargs")



* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades.field_config "Permanent link")

Field config of [ExitTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades "vectorbtpro.portfolio.trades.ExitTrades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-5)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-6)        ('entry_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-7)        ('entry_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-8)        ('entry_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-9)        ('entry_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-10)        ('exit_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-11)        ('exit_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-12)        ('exit_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-13)        ('exit_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-14)        ('pnl', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-15)        ('return', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-16)        ('direction', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-17)        ('status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-18)        ('parent_id', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-19)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-20)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-21)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-22)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-23)            title='Exit Trade Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-24)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-25)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-26)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-27)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-28)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-29)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-30)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-31)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-32)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-33)            name='exit_idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-34)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-35)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-36)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-37)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-38)            title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-39)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-40)            name='entry_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-41)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-42)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-43)            title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-44)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-45)            name='exit_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-46)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-47)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-48)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-49)            mapping=TradeStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-50)                Open=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-51)                Closed=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-52)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-53)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-54)        size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-55)            title='Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-56)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-57)        entry_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-58)            title='Entry Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-59)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-60)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-61)        entry_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-62)            title='Entry Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-63)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-64)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-65)        entry_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-66)            title='Avg Entry Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-67)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-68)        entry_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-69)            title='Entry Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-70)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-71)        exit_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-72)            title='Exit Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-73)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-74)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-75)        exit_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-76)            title='Exit Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-77)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-78)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-79)        exit_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-80)            title='Avg Exit Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-81)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-82)        exit_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-83)            title='Exit Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-84)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-85)        pnl=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-86)            title='PnL'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-87)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-88)        return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-89)            title='Return',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-90)            hovertemplate='$title: %{customdata[$index]:,%}'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-91)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-92)        direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-93)            title='Direction',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-94)            mapping=TradeDirectionT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-95)                Long=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-96)                Short=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-97)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-98)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-99)        parent_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-100)            title='Position Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-101)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-102)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-103)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-24-104))
    

Returns `ExitTrades._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `ExitTrades._field_config`.

* * *

### from_orders class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2670-L2714 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades.from_orders "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-1)ExitTrades.from_orders(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-2)    orders,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-3)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-4)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-5)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-6)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-7)    init_position=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-8)    init_price=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-9)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-10)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-11)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-12)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-13)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-25-14))
    

Build [ExitTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades "vectorbtpro.portfolio.trades.ExitTrades") from [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").

* * *

### plot_signals method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2716-L2879 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades.plot_signals "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-1)ExitTrades.plot_signals(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-3)    plot_ohlc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-4)    plot_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-5)    ohlc_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-6)    ohlc_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-7)    close_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-8)    long_exit_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-9)    short_exit_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-10)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-11)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-12)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-26-13))
    

Plot exit trade signals.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`plot_ohlc`** : `bool`
    Whether to plot OHLC.
**`plot_close`** : `bool`
    Whether to plot close.
**`ohlc_type`**
    

Either 'OHLC', 'Candlestick' or Plotly trace.

Pass None to use the default.

**`ohlc_trace_kwargs`** : `dict`
    Keyword arguments passed to `ohlc_type`.
**`close_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [ExitTrades.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.portfolio.trades.ExitTrades.close").
**`long_exit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Long Exit" markers.
**`short_exit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Short Exit" markers.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-27-1)>>> index = pd.date_range("2020", periods=7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-27-2)>>> price = pd.Series([1, 2, 3, 2, 3, 4, 3], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-27-3)>>> orders = pd.Series([1, 0, -1, 0, -1, 2, -2], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-27-4)>>> pf = vbt.Portfolio.from_orders(price, orders)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-27-5)>>> pf.exit_trades.plot_signals().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/exit_trades_plot_signals.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/exit_trades_plot_signals.dark.svg#only-dark)

* * *

## Positions class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2904-L2944 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Positions "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-1)Positions(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-28-9))
    

Extends [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades") for working with position records.

**Superclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")
  * [IndexApplier](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "vectorbtpro.base.indexes.IndexApplier")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords "vectorbtpro.generic.price_records.PriceRecords")
  * [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges")
  * [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.portfolio.trades.Trades.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.portfolio.trades.Trades.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.portfolio.trades.Trades.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.portfolio.trades.Trades.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.portfolio.trades.Trades.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.portfolio.trades.Trades.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.portfolio.trades.Trades.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.portfolio.trades.Trades.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.portfolio.trades.Trades.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.portfolio.trades.Trades.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.portfolio.trades.Trades.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.portfolio.trades.Trades.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.portfolio.trades.Trades.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.portfolio.trades.Trades.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.portfolio.trades.Trades.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.portfolio.trades.Trades.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.portfolio.trades.Trades.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.portfolio.trades.Trades.prettify")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.portfolio.trades.Trades.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.portfolio.trades.Trades.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.portfolio.trades.Trades.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.portfolio.trades.Trades.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.portfolio.trades.Trades.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.portfolio.trades.Trades.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.portfolio.trades.Trades.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.portfolio.trades.Trades.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.portfolio.trades.Trades.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.portfolio.trades.Trades.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.portfolio.trades.Trades.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.portfolio.trades.Trades.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.portfolio.trades.Trades.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.portfolio.trades.Trades.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.portfolio.trades.Trades.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.portfolio.trades.Trades.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.portfolio.trades.Trades.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.portfolio.trades.Trades.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.portfolio.trades.Trades.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.portfolio.trades.Trades.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.portfolio.trades.Trades.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.portfolio.trades.Trades.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.portfolio.trades.Trades.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.portfolio.trades.Trades.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.portfolio.trades.Trades.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.portfolio.trades.Trades.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.portfolio.trades.Trades.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.portfolio.trades.Trades.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.portfolio.trades.Trades.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.portfolio.trades.Trades.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.portfolio.trades.Trades.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.portfolio.trades.Trades.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.portfolio.trades.Trades.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.portfolio.trades.Trades.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.portfolio.trades.Trades.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.portfolio.trades.Trades.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.portfolio.trades.Trades.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.portfolio.trades.Trades.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.portfolio.trades.Trades.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.portfolio.trades.Trades.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.portfolio.trades.Trades.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.portfolio.trades.Trades.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.portfolio.trades.Trades.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.portfolio.trades.Trades.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.portfolio.trades.Trades.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.portfolio.trades.Trades.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.portfolio.trades.Trades.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.portfolio.trades.Trades.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.portfolio.trades.Trades.pprint")
  * [PriceRecords.from_records](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.from_records "vectorbtpro.portfolio.trades.Trades.from_records")
  * [PriceRecords.get_bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close "vectorbtpro.portfolio.trades.Trades.get_bar_close")
  * [PriceRecords.get_bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close_time "vectorbtpro.portfolio.trades.Trades.get_bar_close_time")
  * [PriceRecords.get_bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_high "vectorbtpro.portfolio.trades.Trades.get_bar_high")
  * [PriceRecords.get_bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_low "vectorbtpro.portfolio.trades.Trades.get_bar_low")
  * [PriceRecords.get_bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open "vectorbtpro.portfolio.trades.Trades.get_bar_open")
  * [PriceRecords.get_bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open_time "vectorbtpro.portfolio.trades.Trades.get_bar_open_time")
  * [PriceRecords.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func "vectorbtpro.portfolio.trades.Trades.indexing_func")
  * [PriceRecords.indexing_func_meta](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func_meta "vectorbtpro.portfolio.trades.Trades.indexing_func_meta")
  * [PriceRecords.resample](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resample "vectorbtpro.portfolio.trades.Trades.resample")
  * [PriceRecords.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_column_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_column_stack_kwargs")
  * [PriceRecords.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_row_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_row_stack_kwargs")
  * [Ranges.crop](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.crop "vectorbtpro.portfolio.trades.Trades.crop")
  * [Ranges.filter_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_max_duration "vectorbtpro.portfolio.trades.Trades.filter_max_duration")
  * [Ranges.filter_min_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_min_duration "vectorbtpro.portfolio.trades.Trades.filter_min_duration")
  * [Ranges.from_array](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_array "vectorbtpro.portfolio.trades.Trades.from_array")
  * [Ranges.from_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta "vectorbtpro.portfolio.trades.Trades.from_delta")
  * [Ranges.get_avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_avg_duration "vectorbtpro.portfolio.trades.Trades.get_avg_duration")
  * [Ranges.get_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_coverage "vectorbtpro.portfolio.trades.Trades.get_coverage")
  * [Ranges.get_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_duration "vectorbtpro.portfolio.trades.Trades.get_duration")
  * [Ranges.get_first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_idx "vectorbtpro.portfolio.trades.Trades.get_first_idx")
  * [Ranges.get_first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_pd_mask "vectorbtpro.portfolio.trades.Trades.get_first_pd_mask")
  * [Ranges.get_invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_invalid "vectorbtpro.portfolio.trades.Trades.get_invalid")
  * [Ranges.get_last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_idx "vectorbtpro.portfolio.trades.Trades.get_last_idx")
  * [Ranges.get_last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_pd_mask "vectorbtpro.portfolio.trades.Trades.get_last_pd_mask")
  * [Ranges.get_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_max_duration "vectorbtpro.portfolio.trades.Trades.get_max_duration")
  * [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.portfolio.trades.Trades.get_projections")
  * [Ranges.get_ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_ranges_pd_mask "vectorbtpro.portfolio.trades.Trades.get_ranges_pd_mask")
  * [Ranges.get_real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_real_duration "vectorbtpro.portfolio.trades.Trades.get_real_duration")
  * [Ranges.get_valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_valid "vectorbtpro.portfolio.trades.Trades.get_valid")
  * [Ranges.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections "vectorbtpro.portfolio.trades.Trades.plot_projections")
  * [Ranges.plot_shapes](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_shapes "vectorbtpro.portfolio.trades.Trades.plot_shapes")
  * [Ranges.with_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.with_delta "vectorbtpro.portfolio.trades.Trades.with_delta")
  * [Records.apply](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply "vectorbtpro.portfolio.trades.Trades.apply")
  * [Records.apply_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply_mask "vectorbtpro.portfolio.trades.Trades.apply_mask")
  * [Records.build_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.build_field_config_doc "vectorbtpro.portfolio.trades.Trades.build_field_config_doc")
  * [Records.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack "vectorbtpro.portfolio.trades.Trades.column_stack")
  * [Records.column_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack_records_arrs "vectorbtpro.portfolio.trades.Trades.column_stack_records_arrs")
  * [Records.count](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.count "vectorbtpro.portfolio.trades.Trades.count")
  * [Records.coverage_map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.coverage_map "vectorbtpro.portfolio.trades.Trades.coverage_map")
  * [Records.first_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.first_n "vectorbtpro.portfolio.trades.Trades.first_n")
  * [Records.get_apply_mapping_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_arr "vectorbtpro.portfolio.trades.Trades.get_apply_mapping_arr")
  * [Records.get_apply_mapping_str_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_str_arr "vectorbtpro.portfolio.trades.Trades.get_apply_mapping_str_arr")
  * [Records.get_column_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_column_stack_record_indices "vectorbtpro.portfolio.trades.Trades.get_column_stack_record_indices")
  * [Records.get_field_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_arr "vectorbtpro.portfolio.trades.Trades.get_field_arr")
  * [Records.get_field_mapping](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_mapping "vectorbtpro.portfolio.trades.Trades.get_field_mapping")
  * [Records.get_field_name](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_name "vectorbtpro.portfolio.trades.Trades.get_field_name")
  * [Records.get_field_setting](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_setting "vectorbtpro.portfolio.trades.Trades.get_field_setting")
  * [Records.get_field_title](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_title "vectorbtpro.portfolio.trades.Trades.get_field_title")
  * [Records.get_map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field "vectorbtpro.portfolio.trades.Trades.get_map_field")
  * [Records.get_map_field_to_columns](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_columns "vectorbtpro.portfolio.trades.Trades.get_map_field_to_columns")
  * [Records.get_map_field_to_index](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_index "vectorbtpro.portfolio.trades.Trades.get_map_field_to_index")
  * [Records.get_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_pd_mask "vectorbtpro.portfolio.trades.Trades.get_pd_mask")
  * [Records.get_row_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_row_stack_record_indices "vectorbtpro.portfolio.trades.Trades.get_row_stack_record_indices")
  * [Records.has_conflicts](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.has_conflicts "vectorbtpro.portfolio.trades.Trades.has_conflicts")
  * [Records.is_sorted](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.is_sorted "vectorbtpro.portfolio.trades.Trades.is_sorted")
  * [Records.last_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.last_n "vectorbtpro.portfolio.trades.Trades.last_n")
  * [Records.map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map "vectorbtpro.portfolio.trades.Trades.map")
  * [Records.map_array](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_array "vectorbtpro.portfolio.trades.Trades.map_array")
  * [Records.map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_field "vectorbtpro.portfolio.trades.Trades.map_field")
  * [Records.override_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.override_field_config_doc "vectorbtpro.portfolio.trades.Trades.override_field_config_doc")
  * [Records.prepare_customdata](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.prepare_customdata "vectorbtpro.portfolio.trades.Trades.prepare_customdata")
  * [Records.random_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.random_n "vectorbtpro.portfolio.trades.Trades.random_n")
  * [Records.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.replace "vectorbtpro.portfolio.trades.Trades.replace")
  * [Records.resample_meta](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_meta "vectorbtpro.portfolio.trades.Trades.resample_meta")
  * [Records.resample_records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_records_arr "vectorbtpro.portfolio.trades.Trades.resample_records_arr")
  * [Records.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack "vectorbtpro.portfolio.trades.Trades.row_stack")
  * [Records.row_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack_records_arrs "vectorbtpro.portfolio.trades.Trades.row_stack_records_arrs")
  * [Records.select_cols](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.select_cols "vectorbtpro.portfolio.trades.Trades.select_cols")
  * [Records.sort](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.sort "vectorbtpro.portfolio.trades.Trades.sort")
  * [Records.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.to_readable "vectorbtpro.portfolio.trades.Trades.to_readable")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.portfolio.trades.Trades.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.portfolio.trades.Trades.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.portfolio.trades.Trades.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.trades.Trades.stats")
  * [Trades.avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.avg_duration "vectorbtpro.portfolio.trades.Trades.avg_duration")
  * [Trades.bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close "vectorbtpro.portfolio.trades.Trades.bar_close")
  * [Trades.bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close_time "vectorbtpro.portfolio.trades.Trades.bar_close_time")
  * [Trades.bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_high "vectorbtpro.portfolio.trades.Trades.bar_high")
  * [Trades.bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_low "vectorbtpro.portfolio.trades.Trades.bar_low")
  * [Trades.bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open "vectorbtpro.portfolio.trades.Trades.bar_open")
  * [Trades.bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open_time "vectorbtpro.portfolio.trades.Trades.bar_open_time")
  * [Trades.best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price "vectorbtpro.portfolio.trades.Trades.best_price")
  * [Trades.best_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price_idx "vectorbtpro.portfolio.trades.Trades.best_price_idx")
  * [Trades.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.portfolio.trades.Trades.close")
  * [Trades.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.portfolio.trades.Trades.cls_dir")
  * [Trades.col](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.col "vectorbtpro.portfolio.trades.Trades.col")
  * [Trades.col_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_arr "vectorbtpro.portfolio.trades.Trades.col_arr")
  * [Trades.col_mapper](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_mapper "vectorbtpro.portfolio.trades.Trades.col_mapper")
  * [Trades.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.portfolio.trades.Trades.column_only_select")
  * [Trades.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.portfolio.trades.Trades.config")
  * [Trades.coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.coverage "vectorbtpro.portfolio.trades.Trades.coverage")
  * [Trades.direction](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction "vectorbtpro.portfolio.trades.Trades.direction")
  * [Trades.direction_long](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction_long "vectorbtpro.portfolio.trades.Trades.direction_long")
  * [Trades.direction_short](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction_short "vectorbtpro.portfolio.trades.Trades.direction_short")
  * [Trades.duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.duration "vectorbtpro.portfolio.trades.Trades.duration")
  * [Trades.edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.edge_ratio "vectorbtpro.portfolio.trades.Trades.edge_ratio")
  * [Trades.end_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.end_idx "vectorbtpro.portfolio.trades.Trades.end_idx")
  * [Trades.entry_fees](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_fees "vectorbtpro.portfolio.trades.Trades.entry_fees")
  * [Trades.entry_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_idx "vectorbtpro.portfolio.trades.Trades.entry_idx")
  * [Trades.entry_order_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_order_id "vectorbtpro.portfolio.trades.Trades.entry_order_id")
  * [Trades.entry_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_price "vectorbtpro.portfolio.trades.Trades.entry_price")
  * [Trades.exit_fees](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_fees "vectorbtpro.portfolio.trades.Trades.exit_fees")
  * [Trades.exit_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_idx "vectorbtpro.portfolio.trades.Trades.exit_idx")
  * [Trades.exit_order_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_order_id "vectorbtpro.portfolio.trades.Trades.exit_order_id")
  * [Trades.exit_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_price "vectorbtpro.portfolio.trades.Trades.exit_price")
  * [Trades.expanding_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_best_price "vectorbtpro.portfolio.trades.Trades.expanding_best_price")
  * [Trades.expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae "vectorbtpro.portfolio.trades.Trades.expanding_mae")
  * [Trades.expanding_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae_returns "vectorbtpro.portfolio.trades.Trades.expanding_mae_returns")
  * [Trades.expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe "vectorbtpro.portfolio.trades.Trades.expanding_mfe")
  * [Trades.expanding_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns "vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns")
  * [Trades.expanding_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_worst_price "vectorbtpro.portfolio.trades.Trades.expanding_worst_price")
  * [Trades.expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expectancy "vectorbtpro.portfolio.trades.Trades.expectancy")
  * [Trades.field_names](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.field_names "vectorbtpro.portfolio.trades.Trades.field_names")
  * [Trades.first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_idx "vectorbtpro.portfolio.trades.Trades.first_idx")
  * [Trades.first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_pd_mask "vectorbtpro.portfolio.trades.Trades.first_pd_mask")
  * [Trades.get_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price "vectorbtpro.portfolio.trades.Trades.get_best_price")
  * [Trades.get_best_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price_idx "vectorbtpro.portfolio.trades.Trades.get_best_price_idx")
  * [Trades.get_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_edge_ratio "vectorbtpro.portfolio.trades.Trades.get_edge_ratio")
  * [Trades.get_expanding_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_best_price "vectorbtpro.portfolio.trades.Trades.get_expanding_best_price")
  * [Trades.get_expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mae "vectorbtpro.portfolio.trades.Trades.get_expanding_mae")
  * [Trades.get_expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mfe "vectorbtpro.portfolio.trades.Trades.get_expanding_mfe")
  * [Trades.get_expanding_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price "vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price")
  * [Trades.get_expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expectancy "vectorbtpro.portfolio.trades.Trades.get_expectancy")
  * [Trades.get_long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_long_view "vectorbtpro.portfolio.trades.Trades.get_long_view")
  * [Trades.get_losing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing "vectorbtpro.portfolio.trades.Trades.get_losing")
  * [Trades.get_losing_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing_streak "vectorbtpro.portfolio.trades.Trades.get_losing_streak")
  * [Trades.get_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mae "vectorbtpro.portfolio.trades.Trades.get_mae")
  * [Trades.get_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mfe "vectorbtpro.portfolio.trades.Trades.get_mfe")
  * [Trades.get_profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_profit_factor "vectorbtpro.portfolio.trades.Trades.get_profit_factor")
  * [Trades.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_ranges "vectorbtpro.portfolio.trades.Trades.get_ranges")
  * [Trades.get_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio "vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio")
  * [Trades.get_short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_short_view "vectorbtpro.portfolio.trades.Trades.get_short_view")
  * [Trades.get_sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_sqn "vectorbtpro.portfolio.trades.Trades.get_sqn")
  * [Trades.get_win_rate](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_win_rate "vectorbtpro.portfolio.trades.Trades.get_win_rate")
  * [Trades.get_winning](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning "vectorbtpro.portfolio.trades.Trades.get_winning")
  * [Trades.get_winning_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning_streak "vectorbtpro.portfolio.trades.Trades.get_winning_streak")
  * [Trades.get_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price "vectorbtpro.portfolio.trades.Trades.get_worst_price")
  * [Trades.get_worst_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price_idx "vectorbtpro.portfolio.trades.Trades.get_worst_price_idx")
  * [Trades.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.portfolio.trades.Trades.group_select")
  * [Trades.high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.high "vectorbtpro.portfolio.trades.Trades.high")
  * [Trades.id](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.id "vectorbtpro.portfolio.trades.Trades.id")
  * [Trades.id_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.id_arr "vectorbtpro.portfolio.trades.Trades.id_arr")
  * [Trades.idx_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.idx_arr "vectorbtpro.portfolio.trades.Trades.idx_arr")
  * [Trades.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.portfolio.trades.Trades.iloc")
  * [Trades.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.portfolio.trades.Trades.indexing_kwargs")
  * [Trades.invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.invalid "vectorbtpro.portfolio.trades.Trades.invalid")
  * [Trades.last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_idx "vectorbtpro.portfolio.trades.Trades.last_idx")
  * [Trades.last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_pd_mask "vectorbtpro.portfolio.trades.Trades.last_pd_mask")
  * [Trades.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.portfolio.trades.Trades.loc")
  * [Trades.long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.long_view "vectorbtpro.portfolio.trades.Trades.long_view")
  * [Trades.losing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.losing "vectorbtpro.portfolio.trades.Trades.losing")
  * [Trades.losing_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.losing_streak "vectorbtpro.portfolio.trades.Trades.losing_streak")
  * [Trades.low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.low "vectorbtpro.portfolio.trades.Trades.low")
  * [Trades.mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae "vectorbtpro.portfolio.trades.Trades.mae")
  * [Trades.mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae_returns "vectorbtpro.portfolio.trades.Trades.mae_returns")
  * [Trades.max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.max_duration "vectorbtpro.portfolio.trades.Trades.max_duration")
  * [Trades.mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe "vectorbtpro.portfolio.trades.Trades.mfe")
  * [Trades.mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe_returns "vectorbtpro.portfolio.trades.Trades.mfe_returns")
  * [Trades.open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.open "vectorbtpro.portfolio.trades.Trades.open")
  * [Trades.overlap_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.overlap_coverage "vectorbtpro.portfolio.trades.Trades.overlap_coverage")
  * [Trades.parent_id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.parent_id "vectorbtpro.portfolio.trades.Trades.parent_id")
  * [Trades.pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.pd_mask "vectorbtpro.portfolio.trades.Trades.pd_mask")
  * [Trades.plot](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot "vectorbtpro.portfolio.trades.Trades.plot")
  * [Trades.plot_against_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_against_pnl "vectorbtpro.portfolio.trades.Trades.plot_against_pnl")
  * [Trades.plot_expanding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding "vectorbtpro.portfolio.trades.Trades.plot_expanding")
  * [Trades.plot_expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mae "vectorbtpro.portfolio.trades.Trades.plot_expanding_mae")
  * [Trades.plot_expanding_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mae_returns "vectorbtpro.portfolio.trades.Trades.plot_expanding_mae_returns")
  * [Trades.plot_expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe "vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe")
  * [Trades.plot_expanding_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe_returns "vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe_returns")
  * [Trades.plot_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mae "vectorbtpro.portfolio.trades.Trades.plot_mae")
  * [Trades.plot_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mae_returns "vectorbtpro.portfolio.trades.Trades.plot_mae_returns")
  * [Trades.plot_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mfe "vectorbtpro.portfolio.trades.Trades.plot_mfe")
  * [Trades.plot_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mfe_returns "vectorbtpro.portfolio.trades.Trades.plot_mfe_returns")
  * [Trades.plot_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_pnl "vectorbtpro.portfolio.trades.Trades.plot_pnl")
  * [Trades.plot_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_returns "vectorbtpro.portfolio.trades.Trades.plot_returns")
  * [Trades.plot_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_running_edge_ratio "vectorbtpro.portfolio.trades.Trades.plot_running_edge_ratio")
  * [Trades.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plots_defaults "vectorbtpro.portfolio.trades.Trades.plots_defaults")
  * [Trades.pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.pnl "vectorbtpro.portfolio.trades.Trades.pnl")
  * [Trades.profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.profit_factor "vectorbtpro.portfolio.trades.Trades.profit_factor")
  * [Trades.projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.projections "vectorbtpro.portfolio.trades.Trades.projections")
  * [Trades.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.portfolio.trades.Trades.range_only_select")
  * [Trades.ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.ranges "vectorbtpro.portfolio.trades.Trades.ranges")
  * [Trades.ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.ranges_pd_mask "vectorbtpro.portfolio.trades.Trades.ranges_pd_mask")
  * [Trades.readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.readable "vectorbtpro.portfolio.trades.Trades.readable")
  * [Trades.real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.real_duration "vectorbtpro.portfolio.trades.Trades.real_duration")
  * [Trades.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.portfolio.trades.Trades.rec_state")
  * [Trades.recarray](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.recarray "vectorbtpro.portfolio.trades.Trades.recarray")
  * [Trades.records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records "vectorbtpro.portfolio.trades.Trades.records")
  * [Trades.records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_arr "vectorbtpro.portfolio.trades.Trades.records_arr")
  * [Trades.records_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_readable "vectorbtpro.portfolio.trades.Trades.records_readable")
  * [Trades.rel_expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_expectancy "vectorbtpro.portfolio.trades.Trades.rel_expectancy")
  * [Trades.rel_profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_profit_factor "vectorbtpro.portfolio.trades.Trades.rel_profit_factor")
  * [Trades.rel_sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_sqn "vectorbtpro.portfolio.trades.Trades.rel_sqn")
  * [Trades.returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.returns "vectorbtpro.portfolio.trades.Trades.returns")
  * [Trades.running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.running_edge_ratio "vectorbtpro.portfolio.trades.Trades.running_edge_ratio")
  * [Trades.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.portfolio.trades.Trades.self_aliases")
  * [Trades.short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.short_view "vectorbtpro.portfolio.trades.Trades.short_view")
  * [Trades.size](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.size "vectorbtpro.portfolio.trades.Trades.size")
  * [Trades.sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.sqn "vectorbtpro.portfolio.trades.Trades.sqn")
  * [Trades.start_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.start_idx "vectorbtpro.portfolio.trades.Trades.start_idx")
  * [Trades.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.stats_defaults "vectorbtpro.portfolio.trades.Trades.stats_defaults")
  * [Trades.status](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status "vectorbtpro.portfolio.trades.Trades.status")
  * [Trades.status_closed](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_closed "vectorbtpro.portfolio.trades.Trades.status_closed")
  * [Trades.status_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_open "vectorbtpro.portfolio.trades.Trades.status_open")
  * [Trades.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.portfolio.trades.Trades.unwrapped")
  * [Trades.valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.valid "vectorbtpro.portfolio.trades.Trades.valid")
  * [Trades.values](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.values "vectorbtpro.portfolio.trades.Trades.values")
  * [Trades.win_rate](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.win_rate "vectorbtpro.portfolio.trades.Trades.win_rate")
  * [Trades.winning](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.winning "vectorbtpro.portfolio.trades.Trades.winning")
  * [Trades.winning_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.winning_streak "vectorbtpro.portfolio.trades.Trades.winning_streak")
  * [Trades.worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price "vectorbtpro.portfolio.trades.Trades.worst_price")
  * [Trades.worst_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price_idx "vectorbtpro.portfolio.trades.Trades.worst_price_idx")
  * [Trades.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.portfolio.trades.Trades.wrapper")
  * [Trades.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.portfolio.trades.Trades.xloc")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.portfolio.trades.Trades.apply_to_index")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.portfolio.trades.Trades.regroup")
  * [Wrapping.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "vectorbtpro.portfolio.trades.Trades.resolve_self")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.portfolio.trades.Trades.resolve_stack_kwargs")



* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Positions.field_config "Permanent link")

Field config of [Positions](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Positions "vectorbtpro.portfolio.trades.Positions").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-5)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-6)        ('entry_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-7)        ('entry_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-8)        ('entry_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-9)        ('entry_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-10)        ('exit_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-11)        ('exit_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-12)        ('exit_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-13)        ('exit_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-14)        ('pnl', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-15)        ('return', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-16)        ('direction', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-17)        ('status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-18)        ('parent_id', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-19)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-20)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-21)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-22)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-23)            title='Position Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-24)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-25)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-26)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-27)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-28)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-29)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-30)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-31)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-32)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-33)            name='exit_idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-34)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-35)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-36)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-37)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-38)            title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-39)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-40)            name='entry_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-41)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-42)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-43)            title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-44)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-45)            name='exit_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-46)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-47)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-48)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-49)            mapping=TradeStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-50)                Open=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-51)                Closed=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-52)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-53)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-54)        size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-55)            title='Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-56)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-57)        entry_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-58)            title='Entry Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-59)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-60)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-61)        entry_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-62)            title='Entry Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-63)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-64)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-65)        entry_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-66)            title='Avg Entry Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-67)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-68)        entry_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-69)            title='Entry Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-70)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-71)        exit_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-72)            title='Exit Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-73)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-74)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-75)        exit_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-76)            title='Exit Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-77)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-78)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-79)        exit_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-80)            title='Avg Exit Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-81)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-82)        exit_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-83)            title='Exit Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-84)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-85)        pnl=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-86)            title='PnL'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-87)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-88)        return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-89)            title='Return',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-90)            hovertemplate='$title: %{customdata[$index]:,%}'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-91)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-92)        direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-93)            title='Direction',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-94)            mapping=TradeDirectionT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-95)                Long=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-96)                Short=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-97)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-98)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-99)        parent_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-100)            title='Parent Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-101)            mapping='ids',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-102)            ignore=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-103)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-104)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-29-105))
    

Returns `Positions._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `Positions._field_config`.

* * *

### from_trades class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2912-L2944 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Positions.from_trades "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-1)Positions.from_trades(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-2)    trades,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-3)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-4)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-5)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-6)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-7)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-8)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-9)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-30-10))
    

Build [Positions](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Positions "vectorbtpro.portfolio.trades.Positions") from [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades").

* * *

## Trades class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L658-L2392 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-1)Trades(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-31-9))
    

Extends [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for working with trade-like records, such as entry trades, exit trades, and positions.

**Superclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")
  * [IndexApplier](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "vectorbtpro.base.indexes.IndexApplier")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords "vectorbtpro.generic.price_records.PriceRecords")
  * [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges")
  * [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.generic.ranges.Ranges.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.generic.ranges.Ranges.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.generic.ranges.Ranges.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.generic.ranges.Ranges.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.generic.ranges.Ranges.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.ranges.Ranges.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.ranges.Ranges.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.ranges.Ranges.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.ranges.Ranges.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.ranges.Ranges.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.ranges.Ranges.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.ranges.Ranges.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.ranges.Ranges.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.ranges.Ranges.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.ranges.Ranges.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.ranges.Ranges.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.ranges.Ranges.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.ranges.Ranges.prettify")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.ranges.Ranges.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.ranges.Ranges.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.ranges.Ranges.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.ranges.Ranges.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.ranges.Ranges.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.ranges.Ranges.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.ranges.Ranges.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.ranges.Ranges.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.ranges.Ranges.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.ranges.Ranges.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.ranges.Ranges.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.ranges.Ranges.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.ranges.Ranges.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.ranges.Ranges.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.generic.ranges.Ranges.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.generic.ranges.Ranges.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.generic.ranges.Ranges.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.generic.ranges.Ranges.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.generic.ranges.Ranges.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.generic.ranges.Ranges.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.generic.ranges.Ranges.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.generic.ranges.Ranges.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.generic.ranges.Ranges.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.generic.ranges.Ranges.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.generic.ranges.Ranges.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.generic.ranges.Ranges.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.generic.ranges.Ranges.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.generic.ranges.Ranges.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.generic.ranges.Ranges.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.generic.ranges.Ranges.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.generic.ranges.Ranges.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.generic.ranges.Ranges.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.generic.ranges.Ranges.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.ranges.Ranges.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.ranges.Ranges.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.ranges.Ranges.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.ranges.Ranges.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.ranges.Ranges.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.ranges.Ranges.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.ranges.Ranges.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.ranges.Ranges.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.ranges.Ranges.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.ranges.Ranges.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.ranges.Ranges.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.ranges.Ranges.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.generic.ranges.Ranges.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.generic.ranges.Ranges.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.ranges.Ranges.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.generic.ranges.Ranges.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.ranges.Ranges.pprint")
  * [PriceRecords.from_records](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.from_records "vectorbtpro.generic.ranges.Ranges.from_records")
  * [PriceRecords.get_bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close "vectorbtpro.generic.ranges.Ranges.get_bar_close")
  * [PriceRecords.get_bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close_time "vectorbtpro.generic.ranges.Ranges.get_bar_close_time")
  * [PriceRecords.get_bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_high "vectorbtpro.generic.ranges.Ranges.get_bar_high")
  * [PriceRecords.get_bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_low "vectorbtpro.generic.ranges.Ranges.get_bar_low")
  * [PriceRecords.get_bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open "vectorbtpro.generic.ranges.Ranges.get_bar_open")
  * [PriceRecords.get_bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open_time "vectorbtpro.generic.ranges.Ranges.get_bar_open_time")
  * [PriceRecords.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func "vectorbtpro.generic.ranges.Ranges.indexing_func")
  * [PriceRecords.indexing_func_meta](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func_meta "vectorbtpro.generic.ranges.Ranges.indexing_func_meta")
  * [PriceRecords.resample](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resample "vectorbtpro.generic.ranges.Ranges.resample")
  * [PriceRecords.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_column_stack_kwargs "vectorbtpro.generic.ranges.Ranges.resolve_column_stack_kwargs")
  * [PriceRecords.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_row_stack_kwargs "vectorbtpro.generic.ranges.Ranges.resolve_row_stack_kwargs")
  * [Ranges.avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.avg_duration "vectorbtpro.generic.ranges.Ranges.avg_duration")
  * [Ranges.bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close "vectorbtpro.generic.ranges.Ranges.bar_close")
  * [Ranges.bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close_time "vectorbtpro.generic.ranges.Ranges.bar_close_time")
  * [Ranges.bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_high "vectorbtpro.generic.ranges.Ranges.bar_high")
  * [Ranges.bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_low "vectorbtpro.generic.ranges.Ranges.bar_low")
  * [Ranges.bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open "vectorbtpro.generic.ranges.Ranges.bar_open")
  * [Ranges.bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open_time "vectorbtpro.generic.ranges.Ranges.bar_open_time")
  * [Ranges.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.generic.ranges.Ranges.close")
  * [Ranges.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.generic.ranges.Ranges.cls_dir")
  * [Ranges.col](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.col "vectorbtpro.generic.ranges.Ranges.col")
  * [Ranges.col_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_arr "vectorbtpro.generic.ranges.Ranges.col_arr")
  * [Ranges.col_mapper](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_mapper "vectorbtpro.generic.ranges.Ranges.col_mapper")
  * [Ranges.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.generic.ranges.Ranges.column_only_select")
  * [Ranges.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.ranges.Ranges.config")
  * [Ranges.coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.coverage "vectorbtpro.generic.ranges.Ranges.coverage")
  * [Ranges.crop](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.crop "vectorbtpro.generic.ranges.Ranges.crop")
  * [Ranges.duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.duration "vectorbtpro.generic.ranges.Ranges.duration")
  * [Ranges.end_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.end_idx "vectorbtpro.generic.ranges.Ranges.end_idx")
  * [Ranges.field_names](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.field_names "vectorbtpro.generic.ranges.Ranges.field_names")
  * [Ranges.filter_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_max_duration "vectorbtpro.generic.ranges.Ranges.filter_max_duration")
  * [Ranges.filter_min_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_min_duration "vectorbtpro.generic.ranges.Ranges.filter_min_duration")
  * [Ranges.first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_idx "vectorbtpro.generic.ranges.Ranges.first_idx")
  * [Ranges.first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_pd_mask "vectorbtpro.generic.ranges.Ranges.first_pd_mask")
  * [Ranges.from_array](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_array "vectorbtpro.generic.ranges.Ranges.from_array")
  * [Ranges.from_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta "vectorbtpro.generic.ranges.Ranges.from_delta")
  * [Ranges.get_avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_avg_duration "vectorbtpro.generic.ranges.Ranges.get_avg_duration")
  * [Ranges.get_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_coverage "vectorbtpro.generic.ranges.Ranges.get_coverage")
  * [Ranges.get_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_duration "vectorbtpro.generic.ranges.Ranges.get_duration")
  * [Ranges.get_first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_idx "vectorbtpro.generic.ranges.Ranges.get_first_idx")
  * [Ranges.get_first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_pd_mask "vectorbtpro.generic.ranges.Ranges.get_first_pd_mask")
  * [Ranges.get_invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_invalid "vectorbtpro.generic.ranges.Ranges.get_invalid")
  * [Ranges.get_last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_idx "vectorbtpro.generic.ranges.Ranges.get_last_idx")
  * [Ranges.get_last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_pd_mask "vectorbtpro.generic.ranges.Ranges.get_last_pd_mask")
  * [Ranges.get_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_max_duration "vectorbtpro.generic.ranges.Ranges.get_max_duration")
  * [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.generic.ranges.Ranges.get_projections")
  * [Ranges.get_ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_ranges_pd_mask "vectorbtpro.generic.ranges.Ranges.get_ranges_pd_mask")
  * [Ranges.get_real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_real_duration "vectorbtpro.generic.ranges.Ranges.get_real_duration")
  * [Ranges.get_valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_valid "vectorbtpro.generic.ranges.Ranges.get_valid")
  * [Ranges.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.generic.ranges.Ranges.group_select")
  * [Ranges.high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.high "vectorbtpro.generic.ranges.Ranges.high")
  * [Ranges.id](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.id "vectorbtpro.generic.ranges.Ranges.id")
  * [Ranges.id_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.id_arr "vectorbtpro.generic.ranges.Ranges.id_arr")
  * [Ranges.idx_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.idx_arr "vectorbtpro.generic.ranges.Ranges.idx_arr")
  * [Ranges.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.generic.ranges.Ranges.iloc")
  * [Ranges.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.generic.ranges.Ranges.indexing_kwargs")
  * [Ranges.invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.invalid "vectorbtpro.generic.ranges.Ranges.invalid")
  * [Ranges.last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_idx "vectorbtpro.generic.ranges.Ranges.last_idx")
  * [Ranges.last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_pd_mask "vectorbtpro.generic.ranges.Ranges.last_pd_mask")
  * [Ranges.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.generic.ranges.Ranges.loc")
  * [Ranges.low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.low "vectorbtpro.generic.ranges.Ranges.low")
  * [Ranges.max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.max_duration "vectorbtpro.generic.ranges.Ranges.max_duration")
  * [Ranges.open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.open "vectorbtpro.generic.ranges.Ranges.open")
  * [Ranges.overlap_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.overlap_coverage "vectorbtpro.generic.ranges.Ranges.overlap_coverage")
  * [Ranges.pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.pd_mask "vectorbtpro.generic.ranges.Ranges.pd_mask")
  * [Ranges.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections "vectorbtpro.generic.ranges.Ranges.plot_projections")
  * [Ranges.plot_shapes](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_shapes "vectorbtpro.generic.ranges.Ranges.plot_shapes")
  * [Ranges.projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.projections "vectorbtpro.generic.ranges.Ranges.projections")
  * [Ranges.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.generic.ranges.Ranges.range_only_select")
  * [Ranges.ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.ranges_pd_mask "vectorbtpro.generic.ranges.Ranges.ranges_pd_mask")
  * [Ranges.readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.readable "vectorbtpro.generic.ranges.Ranges.readable")
  * [Ranges.real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.real_duration "vectorbtpro.generic.ranges.Ranges.real_duration")
  * [Ranges.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.ranges.Ranges.rec_state")
  * [Ranges.recarray](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.recarray "vectorbtpro.generic.ranges.Ranges.recarray")
  * [Ranges.records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records "vectorbtpro.generic.ranges.Ranges.records")
  * [Ranges.records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_arr "vectorbtpro.generic.ranges.Ranges.records_arr")
  * [Ranges.records_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_readable "vectorbtpro.generic.ranges.Ranges.records_readable")
  * [Ranges.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.generic.ranges.Ranges.self_aliases")
  * [Ranges.start_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.start_idx "vectorbtpro.generic.ranges.Ranges.start_idx")
  * [Ranges.status](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status "vectorbtpro.generic.ranges.Ranges.status")
  * [Ranges.status_closed](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_closed "vectorbtpro.generic.ranges.Ranges.status_closed")
  * [Ranges.status_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_open "vectorbtpro.generic.ranges.Ranges.status_open")
  * [Ranges.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.generic.ranges.Ranges.unwrapped")
  * [Ranges.valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.valid "vectorbtpro.generic.ranges.Ranges.valid")
  * [Ranges.values](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.values "vectorbtpro.generic.ranges.Ranges.values")
  * [Ranges.with_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.with_delta "vectorbtpro.generic.ranges.Ranges.with_delta")
  * [Ranges.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.generic.ranges.Ranges.wrapper")
  * [Ranges.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.generic.ranges.Ranges.xloc")
  * [Records.apply](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply "vectorbtpro.generic.ranges.Ranges.apply")
  * [Records.apply_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply_mask "vectorbtpro.generic.ranges.Ranges.apply_mask")
  * [Records.build_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.build_field_config_doc "vectorbtpro.generic.ranges.Ranges.build_field_config_doc")
  * [Records.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack "vectorbtpro.generic.ranges.Ranges.column_stack")
  * [Records.column_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack_records_arrs "vectorbtpro.generic.ranges.Ranges.column_stack_records_arrs")
  * [Records.count](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.count "vectorbtpro.generic.ranges.Ranges.count")
  * [Records.coverage_map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.coverage_map "vectorbtpro.generic.ranges.Ranges.coverage_map")
  * [Records.first_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.first_n "vectorbtpro.generic.ranges.Ranges.first_n")
  * [Records.get_apply_mapping_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_arr "vectorbtpro.generic.ranges.Ranges.get_apply_mapping_arr")
  * [Records.get_apply_mapping_str_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_str_arr "vectorbtpro.generic.ranges.Ranges.get_apply_mapping_str_arr")
  * [Records.get_column_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_column_stack_record_indices "vectorbtpro.generic.ranges.Ranges.get_column_stack_record_indices")
  * [Records.get_field_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_arr "vectorbtpro.generic.ranges.Ranges.get_field_arr")
  * [Records.get_field_mapping](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_mapping "vectorbtpro.generic.ranges.Ranges.get_field_mapping")
  * [Records.get_field_name](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_name "vectorbtpro.generic.ranges.Ranges.get_field_name")
  * [Records.get_field_setting](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_setting "vectorbtpro.generic.ranges.Ranges.get_field_setting")
  * [Records.get_field_title](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_title "vectorbtpro.generic.ranges.Ranges.get_field_title")
  * [Records.get_map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field "vectorbtpro.generic.ranges.Ranges.get_map_field")
  * [Records.get_map_field_to_columns](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_columns "vectorbtpro.generic.ranges.Ranges.get_map_field_to_columns")
  * [Records.get_map_field_to_index](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_index "vectorbtpro.generic.ranges.Ranges.get_map_field_to_index")
  * [Records.get_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_pd_mask "vectorbtpro.generic.ranges.Ranges.get_pd_mask")
  * [Records.get_row_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_row_stack_record_indices "vectorbtpro.generic.ranges.Ranges.get_row_stack_record_indices")
  * [Records.has_conflicts](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.has_conflicts "vectorbtpro.generic.ranges.Ranges.has_conflicts")
  * [Records.is_sorted](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.is_sorted "vectorbtpro.generic.ranges.Ranges.is_sorted")
  * [Records.last_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.last_n "vectorbtpro.generic.ranges.Ranges.last_n")
  * [Records.map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map "vectorbtpro.generic.ranges.Ranges.map")
  * [Records.map_array](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_array "vectorbtpro.generic.ranges.Ranges.map_array")
  * [Records.map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_field "vectorbtpro.generic.ranges.Ranges.map_field")
  * [Records.override_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.override_field_config_doc "vectorbtpro.generic.ranges.Ranges.override_field_config_doc")
  * [Records.prepare_customdata](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.prepare_customdata "vectorbtpro.generic.ranges.Ranges.prepare_customdata")
  * [Records.random_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.random_n "vectorbtpro.generic.ranges.Ranges.random_n")
  * [Records.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.replace "vectorbtpro.generic.ranges.Ranges.replace")
  * [Records.resample_meta](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_meta "vectorbtpro.generic.ranges.Ranges.resample_meta")
  * [Records.resample_records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_records_arr "vectorbtpro.generic.ranges.Ranges.resample_records_arr")
  * [Records.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack "vectorbtpro.generic.ranges.Ranges.row_stack")
  * [Records.row_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack_records_arrs "vectorbtpro.generic.ranges.Ranges.row_stack_records_arrs")
  * [Records.select_cols](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.select_cols "vectorbtpro.generic.ranges.Ranges.select_cols")
  * [Records.sort](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.sort "vectorbtpro.generic.ranges.Ranges.sort")
  * [Records.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.to_readable "vectorbtpro.generic.ranges.Ranges.to_readable")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.generic.ranges.Ranges.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.generic.ranges.Ranges.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.generic.ranges.Ranges.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.ranges.Ranges.stats")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.generic.ranges.Ranges.apply_to_index")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.generic.ranges.Ranges.regroup")
  * [Wrapping.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "vectorbtpro.generic.ranges.Ranges.resolve_self")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.generic.ranges.Ranges.resolve_stack_kwargs")



**Subclasses**

  * [EntryTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades "vectorbtpro.portfolio.trades.EntryTrades")
  * [ExitTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades "vectorbtpro.portfolio.trades.ExitTrades")
  * [Positions](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Positions "vectorbtpro.portfolio.trades.Positions")



* * *

### best_price cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price "Permanent link")

[Trades.get_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price "vectorbtpro.portfolio.trades.Trades.get_best_price") with default arguments.

* * *

### best_price_idx cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price_idx "Permanent link")

[Trades.get_best_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price_idx "vectorbtpro.portfolio.trades.Trades.get_best_price_idx") with default arguments.

* * *

### direction cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction "Permanent link")

Mapped array of the field `direction`.

* * *

### direction_long cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction_long "Permanent link")

Records filtered by `direction == 0`.

* * *

### direction_short cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.direction_short "Permanent link")

Records filtered by `direction == 1`.

* * *

### edge_ratio cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.edge_ratio "Permanent link")

[Trades.get_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_edge_ratio "vectorbtpro.portfolio.trades.Trades.get_edge_ratio") with default arguments.

* * *

### entry_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_fees "Permanent link")

Mapped array of the field `entry_fees`.

* * *

### entry_idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_idx "Permanent link")

Mapped array of the field `entry_idx`.

* * *

### entry_order_id cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_order_id "Permanent link")

Mapped array of the field `entry_order_id`.

* * *

### entry_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.entry_price "Permanent link")

Mapped array of the field `entry_price`.

* * *

### exit_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_fees "Permanent link")

Mapped array of the field `exit_fees`.

* * *

### exit_idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_idx "Permanent link")

Mapped array of the field `exit_idx`.

* * *

### exit_order_id cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_order_id "Permanent link")

Mapped array of the field `exit_order_id`.

* * *

### exit_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.exit_price "Permanent link")

Mapped array of the field `exit_price`.

* * *

### expanding_best_price cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_best_price "Permanent link")

[Trades.get_expanding_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_best_price "vectorbtpro.portfolio.trades.Trades.get_expanding_best_price") with default arguments.

* * *

### expanding_mae cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae "Permanent link")

[Trades.get_expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mae "vectorbtpro.portfolio.trades.Trades.get_expanding_mae") with default arguments.

* * *

### expanding_mae_returns cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae_returns "Permanent link")

[Trades.get_expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mae "vectorbtpro.portfolio.trades.Trades.get_expanding_mae") with arguments `{'use_returns': True}`.

* * *

### expanding_mfe cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe "Permanent link")

[Trades.get_expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mfe "vectorbtpro.portfolio.trades.Trades.get_expanding_mfe") with default arguments.

* * *

### expanding_mfe_returns cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns "Permanent link")

[Trades.get_expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mfe "vectorbtpro.portfolio.trades.Trades.get_expanding_mfe") with arguments `{'use_returns': True}`.

* * *

### expanding_worst_price cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_worst_price "Permanent link")

[Trades.get_expanding_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price "vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price") with default arguments.

* * *

### expectancy cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expectancy "Permanent link")

[Trades.get_expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expectancy "vectorbtpro.portfolio.trades.Trades.get_expectancy") with arguments `{'use_returns': False}`.

* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.field_config "Permanent link")

Field config of [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-5)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-6)        ('entry_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-7)        ('entry_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-8)        ('entry_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-9)        ('entry_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-10)        ('exit_order_id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-11)        ('exit_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-12)        ('exit_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-13)        ('exit_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-14)        ('pnl', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-15)        ('return', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-16)        ('direction', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-17)        ('status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-18)        ('parent_id', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-19)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-20)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-21)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-22)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-23)            title='Trade Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-24)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-25)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-26)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-27)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-28)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-29)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-30)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-31)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-32)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-33)            name='exit_idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-34)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-35)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-36)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-37)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-38)            title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-39)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-40)            name='entry_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-41)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-42)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-43)            title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-44)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-45)            name='exit_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-46)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-47)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-48)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-49)            mapping=TradeStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-50)                Open=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-51)                Closed=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-52)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-53)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-54)        size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-55)            title='Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-56)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-57)        entry_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-58)            title='Entry Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-59)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-60)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-61)        entry_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-62)            title='Entry Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-63)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-64)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-65)        entry_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-66)            title='Avg Entry Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-67)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-68)        entry_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-69)            title='Entry Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-70)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-71)        exit_order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-72)            title='Exit Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-73)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-74)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-75)        exit_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-76)            title='Exit Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-77)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-78)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-79)        exit_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-80)            title='Avg Exit Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-81)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-82)        exit_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-83)            title='Exit Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-84)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-85)        pnl=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-86)            title='PnL'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-87)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-88)        return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-89)            title='Return',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-90)            hovertemplate='$title: %{customdata[$index]:,%}'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-91)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-92)        direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-93)            title='Direction',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-94)            mapping=TradeDirectionT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-95)                Long=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-96)                Short=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-97)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-98)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-99)        parent_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-100)            title='Position Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-101)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-102)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-103)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-32-104))
    

Returns `Trades._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `Trades._field_config`.

* * *

### get_best_price method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L816-L836 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-33-1)Trades.get_best_price(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-33-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-33-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-33-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-33-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-33-6))
    

Get best price.

See [best_price_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.best_price_nb "vectorbtpro.portfolio.nb.records.best_price_nb").

* * *

### get_best_price_idx method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L860-L883 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_best_price_idx "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-34-1)Trades.get_best_price_idx(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-34-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-34-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-34-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-34-5)    relative=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-34-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-34-7))
    

Get (relative) index of best price.

See [best_price_idx_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.best_price_idx_nb "vectorbtpro.portfolio.nb.records.best_price_idx_nb").

* * *

### get_edge_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1110-L1173 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_edge_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-1)Trades.get_edge_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-2)    volatility=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-3)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-4)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-5)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-6)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-7)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-8)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-9)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-35-10))
    

Get edge ratio.

See [edge_ratio_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.edge_ratio_nb "vectorbtpro.portfolio.nb.records.edge_ratio_nb").

If `volatility` is None, calculates the 14-period ATR if both high and low are provided, otherwise the 14-period rolling standard deviation.

* * *

### get_expanding_best_price method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L910-L946 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_best_price "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-36-1)Trades.get_expanding_best_price(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-36-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-36-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-36-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-36-5)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-36-6)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-36-7)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-36-8))
    

Get expanding best price.

See [expanding_best_price_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.expanding_best_price_nb "vectorbtpro.portfolio.nb.records.expanding_best_price_nb").

* * *

### get_expanding_mae method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1080-L1108 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mae "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-1)Trades.get_expanding_mae(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-5)    use_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-6)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-7)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-37-9))
    

Get expanding MAE.

See [expanding_mae_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.expanding_mae_nb "vectorbtpro.portfolio.nb.records.expanding_mae_nb").

* * *

### get_expanding_mfe method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1050-L1078 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_mfe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-1)Trades.get_expanding_mfe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-5)    use_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-6)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-7)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-38-9))
    

Get expanding MFE.

See [expanding_mfe_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.expanding_mfe_nb "vectorbtpro.portfolio.nb.records.expanding_mfe_nb").

* * *

### get_expanding_worst_price method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L948-L984 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expanding_worst_price "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-39-1)Trades.get_expanding_worst_price(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-39-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-39-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-39-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-39-5)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-39-6)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-39-7)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-39-8))
    

Get expanding worst price.

See [expanding_worst_price_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.expanding_worst_price_nb "vectorbtpro.portfolio.nb.records.expanding_worst_price_nb").

* * *

### get_expectancy method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L766-L788 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expectancy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-40-1)Trades.get_expectancy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-40-2)    use_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-40-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-40-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-40-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-40-6)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-40-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-40-8))
    

Get average profitability.

* * *

### get_long_view method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L689-L692 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_long_view "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-41-1)Trades.get_long_view(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-41-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-41-3))
    

Get long view.

* * *

### get_losing method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L706-L709 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-42-1)Trades.get_losing(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-42-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-42-3))
    

Get losing trades.

* * *

### get_losing_streak method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L717-L721 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing_streak "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-43-1)Trades.get_losing_streak(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-43-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-43-3))
    

Get losing streak at each trade in the current column.

See [trade_losing_streak_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.trade_losing_streak_nb "vectorbtpro.portfolio.nb.records.trade_losing_streak_nb").

* * *

### get_mae method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1018-L1048 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mae "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-1)Trades.get_mae(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-5)    use_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-6)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-7)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-44-9))
    

Get MAE.

See [mae_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.mae_nb "vectorbtpro.portfolio.nb.records.mae_nb").

* * *

### get_mfe method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L986-L1016 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mfe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-1)Trades.get_mfe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-5)    use_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-6)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-7)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-45-9))
    

Get MFE.

See [mfe_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.mfe_nb "vectorbtpro.portfolio.nb.records.mfe_nb").

* * *

### get_profit_factor method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L742-L764 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_profit_factor "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-46-1)Trades.get_profit_factor(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-46-2)    use_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-46-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-46-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-46-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-46-6)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-46-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-46-8))
    

Get profit factor.

* * *

### get_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L669-L685 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-47-1)Trades.get_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-47-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-47-3))
    

Get records of type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").

* * *

### get_running_edge_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1175-L1238 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-1)Trades.get_running_edge_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-2)    volatility=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-3)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-4)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-5)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-6)    incl_shorter=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-7)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-8)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-9)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-48-10))
    

Get running edge ratio.

See [running_edge_ratio_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.running_edge_ratio_nb "vectorbtpro.portfolio.nb.records.running_edge_ratio_nb").

If `volatility` is None, calculates the 14-period ATR if both high and low are provided, otherwise the 14-period rolling standard deviation.

* * *

### get_short_view method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L694-L697 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_short_view "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-49-1)Trades.get_short_view(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-49-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-49-3))
    

Get short view.

* * *

### get_sqn method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L790-L814 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_sqn "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-1)Trades.get_sqn(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-2)    ddof=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-3)    use_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-4)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-5)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-6)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-7)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-50-9))
    

Get System Quality Number (SQN).

* * *

### get_win_rate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L723-L740 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_win_rate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-51-1)Trades.get_win_rate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-51-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-51-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-51-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-51-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-51-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-51-7))
    

Get rate of winning trades.

* * *

### get_winning method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L701-L704 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-52-1)Trades.get_winning(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-52-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-52-3))
    

Get winning trades.

* * *

### get_winning_streak method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L711-L715 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning_streak "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-53-1)Trades.get_winning_streak(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-53-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-53-3))
    

Get winning streak at each trade in the current column.

See [trade_winning_streak_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.trade_winning_streak_nb "vectorbtpro.portfolio.nb.records.trade_winning_streak_nb").

* * *

### get_worst_price method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L838-L858 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-54-1)Trades.get_worst_price(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-54-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-54-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-54-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-54-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-54-6))
    

Get worst price.

See [worst_price_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.worst_price_nb "vectorbtpro.portfolio.nb.records.worst_price_nb").

* * *

### get_worst_price_idx method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L885-L908 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price_idx "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-55-1)Trades.get_worst_price_idx(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-55-2)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-55-3)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-55-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-55-5)    relative=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-55-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-55-7))
    

Get (relative) index of worst price.

See [worst_price_idx_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.worst_price_idx_nb "vectorbtpro.portfolio.nb.records.worst_price_idx_nb").

* * *

### long_view cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.long_view "Permanent link")

[Trades.get_long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_long_view "vectorbtpro.portfolio.trades.Trades.get_long_view") with default arguments.

* * *

### losing cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.losing "Permanent link")

[Trades.get_losing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing "vectorbtpro.portfolio.trades.Trades.get_losing") with default arguments.

* * *

### losing_streak cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.losing_streak "Permanent link")

[Trades.get_losing_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_losing_streak "vectorbtpro.portfolio.trades.Trades.get_losing_streak") with default arguments.

* * *

### mae cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae "Permanent link")

[Trades.get_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mae "vectorbtpro.portfolio.trades.Trades.get_mae") with default arguments.

* * *

### mae_returns cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae_returns "Permanent link")

[Trades.get_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mae "vectorbtpro.portfolio.trades.Trades.get_mae") with arguments `{'use_returns': True}`.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.metrics "Permanent link")

Metrics supported by [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-4)        calc_func=<function Trades.<lambda> at 0x174ea9760>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-10)        calc_func=<function Trades.<lambda> at 0x174ea9800>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-16)        calc_func=<function Trades.<lambda> at 0x174ea98a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-21)    first_trade_start=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-22)        title='First Trade Start',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-23)        calc_func='entry_idx.nth',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-24)        n=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-25)        wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-26)            to_index=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-27)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-28)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-29)            'trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-30)            'index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-31)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-32)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-33)    last_trade_end=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-34)        title='Last Trade End',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-35)        calc_func='exit_idx.nth',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-36)        n=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-37)        wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-38)            to_index=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-39)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-40)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-41)            'trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-42)            'index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-43)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-44)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-45)    coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-46)        title='Coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-47)        calc_func='coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-48)        overlapping=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-49)        normalize=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-50)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-51)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-52)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-53)            'coverage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-54)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-55)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-56)    overlap_coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-57)        title='Overlap Coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-58)        calc_func='coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-59)        overlapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-60)        normalize=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-61)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-62)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-63)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-64)            'coverage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-65)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-66)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-67)    total_records=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-68)        title='Total Records',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-69)        calc_func='count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-70)        tags='records'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-71)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-72)    total_long_trades=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-73)        title='Total Long Trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-74)        calc_func='direction_long.count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-75)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-76)            'trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-77)            'long'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-78)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-79)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-80)    total_short_trades=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-81)        title='Total Short Trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-82)        calc_func='direction_short.count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-83)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-84)            'trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-85)            'short'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-86)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-87)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-88)    total_closed_trades=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-89)        title='Total Closed Trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-90)        calc_func='status_closed.count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-91)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-92)            'trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-93)            'closed'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-94)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-95)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-96)    total_open_trades=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-97)        title='Total Open Trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-98)        calc_func='status_open.count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-99)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-100)            'trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-101)            'open'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-102)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-103)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-104)    open_trade_pnl=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-105)        title='Open Trade PnL',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-106)        calc_func='status_open.pnl.sum',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-107)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-108)            'trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-109)            'open'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-110)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-111)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-112)    win_rate=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-113)        title='Win Rate [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-114)        calc_func='status_closed.get_win_rate',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-115)        post_calc_func=<function Trades.<lambda> at 0x174ea9940>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-116)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-117)            template="['trades', *incl_open_tags]",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-118)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-119)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-120)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-121)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-122)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-123)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-124)    winning_streak=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-125)        title='Max Win Streak',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-126)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-127)            template="'winning_streak.max' if incl_open else 'status_closed.winning_streak.max'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-128)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-129)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-130)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-131)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-132)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-133)        wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-134)            dtype=Int64Dtype()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-135)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-136)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-137)            template="['trades', *incl_open_tags, 'streak']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-138)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-139)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-140)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-141)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-142)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-143)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-144)    losing_streak=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-145)        title='Max Loss Streak',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-146)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-147)            template="'losing_streak.max' if incl_open else 'status_closed.losing_streak.max'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-148)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-149)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-150)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-151)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-152)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-153)        wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-154)            dtype=Int64Dtype()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-155)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-156)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-157)            template="['trades', *incl_open_tags, 'streak']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-158)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-159)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-160)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-161)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-162)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-163)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-164)    best_trade=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-165)        title='Best Trade [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-166)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-167)            template="'returns.max' if incl_open else 'status_closed.returns.max'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-168)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-169)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-170)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-171)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-172)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-173)        post_calc_func=<function Trades.<lambda> at 0x174ea99e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-174)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-175)            template="['trades', *incl_open_tags]",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-176)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-177)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-178)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-179)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-180)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-181)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-182)    worst_trade=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-183)        title='Worst Trade [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-184)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-185)            template="'returns.min' if incl_open else 'status_closed.returns.min'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-186)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-187)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-188)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-189)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-190)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-191)        post_calc_func=<function Trades.<lambda> at 0x174ea9a80>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-192)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-193)            template="['trades', *incl_open_tags]",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-194)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-195)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-196)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-197)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-198)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-199)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-200)    avg_winning_trade=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-201)        title='Avg Winning Trade [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-202)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-203)            template="'winning.returns.mean' if incl_open else 'status_closed.winning.returns.mean'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-204)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-205)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-206)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-207)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-208)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-209)        post_calc_func=<function Trades.<lambda> at 0x174ea9b20>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-210)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-211)            template="['trades', *incl_open_tags, 'winning']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-212)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-213)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-214)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-215)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-216)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-217)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-218)    avg_losing_trade=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-219)        title='Avg Losing Trade [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-220)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-221)            template="'losing.returns.mean' if incl_open else 'status_closed.losing.returns.mean'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-222)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-223)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-224)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-225)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-226)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-227)        post_calc_func=<function Trades.<lambda> at 0x174ea9bc0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-228)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-229)            template="['trades', *incl_open_tags, 'losing']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-230)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-231)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-232)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-233)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-234)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-235)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-236)    avg_winning_trade_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-237)        title='Avg Winning Trade Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-238)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-239)            template="'winning.avg_duration' if incl_open else 'status_closed.winning.get_avg_duration'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-240)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-241)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-242)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-243)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-244)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-245)        fill_wrap_kwargs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-246)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-247)            template="['trades', *incl_open_tags, 'winning', 'duration']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-248)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-249)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-250)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-251)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-252)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-253)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-254)    avg_losing_trade_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-255)        title='Avg Losing Trade Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-256)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-257)            template="'losing.avg_duration' if incl_open else 'status_closed.losing.get_avg_duration'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-258)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-259)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-260)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-261)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-262)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-263)        fill_wrap_kwargs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-264)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-265)            template="['trades', *incl_open_tags, 'losing', 'duration']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-266)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-267)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-268)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-269)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-270)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-271)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-272)    profit_factor=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-273)        title='Profit Factor',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-274)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-275)            template="'profit_factor' if incl_open else 'status_closed.get_profit_factor'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-276)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-277)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-278)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-279)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-280)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-281)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-282)            template="['trades', *incl_open_tags]",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-283)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-284)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-285)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-286)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-287)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-288)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-289)    expectancy=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-290)        title='Expectancy',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-291)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-292)            template="'expectancy' if incl_open else 'status_closed.get_expectancy'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-293)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-294)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-295)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-296)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-297)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-298)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-299)            template="['trades', *incl_open_tags]",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-300)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-301)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-302)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-303)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-304)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-305)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-306)    sqn=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-307)        title='SQN',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-308)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-309)            template="'sqn' if incl_open else 'status_closed.get_sqn'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-310)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-311)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-312)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-313)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-314)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-315)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-316)            template="['trades', *incl_open_tags]",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-317)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-318)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-319)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-320)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-321)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-322)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-323)    edge_ratio=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-324)        title='Edge Ratio',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-325)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-326)            template="'edge_ratio' if incl_open else 'status_closed.get_edge_ratio'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-327)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-328)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-329)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-330)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-331)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-332)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-333)            template="['trades', *incl_open_tags]",
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-334)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-335)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-336)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-337)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-338)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-339)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-56-340))
    

Returns `Trades._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `Trades._metrics`.

* * *

### mfe cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe "Permanent link")

[Trades.get_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mfe "vectorbtpro.portfolio.trades.Trades.get_mfe") with default arguments.

* * *

### mfe_returns cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe_returns "Permanent link")

[Trades.get_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_mfe "vectorbtpro.portfolio.trades.Trades.get_mfe") with arguments `{'use_returns': True}`.

* * *

### parent_id cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.parent_id "Permanent link")

Mapped array of the field `parent_id`.

* * *

### plot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2018-L2357 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-1)Trades.plot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-3)    plot_ohlc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-4)    plot_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-5)    plot_markers=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-6)    plot_zones=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-7)    plot_by_type=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-8)    ohlc_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-9)    ohlc_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-10)    close_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-11)    entry_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-12)    exit_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-13)    exit_profit_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-14)    exit_loss_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-15)    active_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-16)    profit_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-17)    loss_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-18)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-19)    xref='x',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-20)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-21)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-22)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-57-23))
    

Plot trades.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`plot_ohlc`** : `bool`
    Whether to plot OHLC.
**`plot_close`** : `bool`
    Whether to plot close.
**`plot_markers`** : `bool`
    Whether to plot markers.
**`plot_zones`** : `bool`
    Whether to plot zones.
**`plot_by_type`** : `bool`
    

Whether to plot exit trades by type.

Otherwise, the appearance will be controlled using `exit_trace_kwargs`.

**`ohlc_type`**
    

Either 'OHLC', 'Candlestick' or Plotly trace.

Pass None to use the default.

**`ohlc_trace_kwargs`** : `dict`
    Keyword arguments passed to `ohlc_type`.
**`close_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Trades.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.portfolio.trades.Trades.close").
**`entry_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Entry" markers.
**`exit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit" markers.
**`exit_profit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit - Profit" markers.
**`exit_loss_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Exit - Loss" markers.
**`active_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Active" markers.
**`profit_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for profit zones.
**`loss_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for loss zones.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`xref`** : `str`
    X coordinate axis.
**`yref`** : `str`
    Y coordinate axis.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-58-1)>>> index = pd.date_range("2020", periods=7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-58-2)>>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-58-3)>>> size = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-58-4)>>> pf = vbt.Portfolio.from_orders(price, size)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-58-5)>>> pf.trades.plot().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plot.dark.svg#only-dark)

* * *

### plot_against_pnl method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1589-L1801 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_against_pnl "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-1)Trades.plot_against_pnl(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-2)    field,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-3)    field_label=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-4)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-5)    group_by=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-6)    pct_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-7)    field_pct_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-8)    closed_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-9)    closed_profit_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-10)    closed_loss_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-11)    open_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-12)    hline_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-13)    vline_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-14)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-15)    xref='x',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-16)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-17)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-18)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-59-19))
    

Plot a field against PnL or returns.

**Args**

**`field`** : `str`, `MappedArray`, `or array_like`
    

Field to be plotted.

Can be also provided as a mapped array or 1-dim array.

**`field_label`** : `str`
    Label of the field.
**`column`** : `str`
    Name of the column to plot.
**`group_by`** : `any`
    Group columns. See [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/base/#vectorbtpro.base.grouping.base.Grouper "vectorbtpro.base.grouping.base.Grouper").
**`pct_scale`** : `bool`
    Whether to set x-axis to [Trades.returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.returns "vectorbtpro.portfolio.trades.Trades.returns"), otherwise to [Trades.pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.pnl "vectorbtpro.portfolio.trades.Trades.pnl").
**`field_pct_scale`** : `bool`
    Whether to make y-axis a percentage scale.
**`closed_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed" markers.
**`closed_profit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed - Profit" markers.
**`closed_loss_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed - Loss" markers.
**`open_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Open" markers.
**`hline_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for horizontal zeroline.
**`vline_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for vertical zeroline.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`xref`** : `str`
    X coordinate axis.
**`yref`** : `str`
    Y coordinate axis.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-60-1)>>> index = pd.date_range("2020", periods=10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-60-2)>>> price = pd.Series([1., 2., 3., 4., 5., 6., 5., 3., 2., 1.], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-60-3)>>> orders = pd.Series([1., -0.5, 0., -0.5, 2., 0., -0.5, -0.5, 0., -0.5], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-60-4)>>> pf = vbt.Portfolio.from_orders(price, orders)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-60-5)>>> trades = pf.trades
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-60-6)>>> trades.plot_against_pnl("MFE").show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plot_against_pnl.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plot_against_pnl.dark.svg#only-dark)

* * *

### plot_expanding method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1843-L1916 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-1)Trades.plot_expanding(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-2)    field,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-3)    field_label=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-4)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-5)    group_by=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-6)    plot_bands=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-7)    colorize='last',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-8)    field_pct_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-9)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-10)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-11)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-61-12))
    

Plot projections of an expanding field.

**Args**

**`field`** : `str` or `array_like`
    

Field to be plotted.

Can be also provided as a 2-dim array.

**`field_label`** : `str`
    Label of the field.
**`column`** : `str`
    Name of the column to plot. Optional.
**`group_by`** : `any`
    Group columns. See [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/base/#vectorbtpro.base.grouping.base.Grouper "vectorbtpro.base.grouping.base.Grouper").
**`plot_bands`** : `bool`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`colorize`** : `bool`, `str` or `callable`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`field_pct_scale`** : `bool`
    Whether to make y-axis a percentage scale.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**kwargs`**
    Keyword arguments passed to [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-62-1)>>> index = pd.date_range("2020", periods=10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-62-2)>>> price = pd.Series([1., 2., 3., 2., 4., 5., 6., 5., 6., 7.], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-62-3)>>> orders = pd.Series([1., 0., 0., -2., 0., 0., 2., 0., 0., -1.], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-62-4)>>> pf = vbt.Portfolio.from_orders(price, orders)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-62-5)>>> pf.trades.plot_expanding("MFE").show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plot_expanding.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plot_expanding.dark.svg#only-dark)

* * *

### plot_expanding_mae method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1937-L1944 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mae "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-63-1)Trades.plot_expanding_mae(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-63-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-63-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-63-4))
    

[Trades.plot_expanding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding "vectorbtpro.portfolio.trades.Trades.plot_expanding") for [Trades.expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae "vectorbtpro.portfolio.trades.Trades.expanding_mae").

* * *

### plot_expanding_mae_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1946-L1954 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mae_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-64-1)Trades.plot_expanding_mae_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-64-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-64-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-64-4))
    

[Trades.plot_expanding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding "vectorbtpro.portfolio.trades.Trades.plot_expanding") for [Trades.expanding_mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae_returns "vectorbtpro.portfolio.trades.Trades.expanding_mae_returns").

* * *

### plot_expanding_mfe method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1918-L1925 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-65-1)Trades.plot_expanding_mfe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-65-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-65-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-65-4))
    

[Trades.plot_expanding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding "vectorbtpro.portfolio.trades.Trades.plot_expanding") for [Trades.expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe "vectorbtpro.portfolio.trades.Trades.expanding_mfe").

* * *

### plot_expanding_mfe_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1927-L1935 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding_mfe_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-66-1)Trades.plot_expanding_mfe_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-66-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-66-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-66-4))
    

[Trades.plot_expanding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_expanding "vectorbtpro.portfolio.trades.Trades.plot_expanding") for [Trades.expanding_mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns "vectorbtpro.portfolio.trades.Trades.expanding_mfe_returns").

* * *

### plot_mae method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1823-L1830 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mae "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-67-1)Trades.plot_mae(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-67-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-67-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-67-4))
    

[Trades.plot_against_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_against_pnl "vectorbtpro.portfolio.trades.Trades.plot_against_pnl") for [Trades.mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae "vectorbtpro.portfolio.trades.Trades.mae").

* * *

### plot_mae_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1832-L1841 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mae_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-68-1)Trades.plot_mae_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-68-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-68-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-68-4))
    

[Trades.plot_against_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_against_pnl "vectorbtpro.portfolio.trades.Trades.plot_against_pnl") for [Trades.mae_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mae_returns "vectorbtpro.portfolio.trades.Trades.mae_returns").

* * *

### plot_mfe method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1803-L1810 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mfe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-69-1)Trades.plot_mfe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-69-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-69-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-69-4))
    

[Trades.plot_against_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_against_pnl "vectorbtpro.portfolio.trades.Trades.plot_against_pnl") for [Trades.mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe "vectorbtpro.portfolio.trades.Trades.mfe").

* * *

### plot_mfe_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1812-L1821 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_mfe_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-70-1)Trades.plot_mfe_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-70-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-70-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-70-4))
    

[Trades.plot_against_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_against_pnl "vectorbtpro.portfolio.trades.Trades.plot_against_pnl") for [Trades.mfe_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.mfe_returns "vectorbtpro.portfolio.trades.Trades.mfe_returns").

* * *

### plot_pnl method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1398-L1579 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_pnl "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-1)Trades.plot_pnl(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-3)    group_by=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-4)    pct_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-5)    marker_size_range=(7, 14),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-6)    opacity_range=(0.75, 0.9),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-7)    closed_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-8)    closed_profit_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-9)    closed_loss_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-10)    open_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-11)    hline_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-12)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-13)    xref='x',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-14)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-15)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-16)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-71-17))
    

Plot trade PnL or returns.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`group_by`** : `any`
    Group columns. See [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/base/#vectorbtpro.base.grouping.base.Grouper "vectorbtpro.base.grouping.base.Grouper").
**`pct_scale`** : `bool`
    Whether to set y-axis to [Trades.returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.returns "vectorbtpro.portfolio.trades.Trades.returns"), otherwise to [Trades.pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.pnl "vectorbtpro.portfolio.trades.Trades.pnl").
**`marker_size_range`** : `tuple`
    Range of marker size.
**`opacity_range`** : `tuple`
    Range of marker opacity.
**`closed_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed" markers.
**`closed_profit_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed - Profit" markers.
**`closed_loss_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Closed - Loss" markers.
**`open_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Open" markers.
**`hline_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for zeroline.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`xref`** : `str`
    X coordinate axis.
**`yref`** : `str`
    Y coordinate axis.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-72-1)>>> index = pd.date_range("2020", periods=7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-72-2)>>> price = pd.Series([1., 2., 3., 4., 3., 2., 1.], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-72-3)>>> orders = pd.Series([1., -0.5, -0.5, 2., -0.5, -0.5, -0.5], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-72-4)>>> pf = vbt.Portfolio.from_orders(price, orders)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-72-5)>>> pf.trades.plot_pnl().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plot_pnl.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/trades_plot_pnl.dark.svg#only-dark)

* * *

### plot_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1581-L1587 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-73-1)Trades.plot_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-73-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-73-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-73-4))
    

[Trades.plot_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_pnl "vectorbtpro.portfolio.trades.Trades.plot_pnl") for [Trades.returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.returns "vectorbtpro.portfolio.trades.Trades.returns").

* * *

### plot_running_edge_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1956-L2016 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_running_edge_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-1)Trades.plot_running_edge_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-3)    volatility=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-4)    entry_price_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-5)    exit_price_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-6)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-7)    incl_shorter=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-8)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-9)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-10)    xref='x',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-11)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-12)    hline_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-13)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-74-14))
    

Plot one column/group of edge ratio.

`**kwargs` are passed to [GenericAccessor.plot_against](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot_against "vectorbtpro.generic.accessors.GenericSRAccessor.plot_against").

* * *

### plots_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L2359-L2369 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plots_defaults "Permanent link")

Defaults for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.portfolio.trades.Trades.plots").

Merges [Ranges.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plots_defaults "vectorbtpro.generic.ranges.Ranges.plots_defaults") and `plots` from [trades](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.trades "vectorbtpro._settings.trades").

* * *

### pnl cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.pnl "Permanent link")

Mapped array of the field `pnl`.

* * *

### profit_factor cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.profit_factor "Permanent link")

[Trades.get_profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_profit_factor "vectorbtpro.portfolio.trades.Trades.get_profit_factor") with arguments `{'use_returns': False}`.

* * *

### ranges cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.ranges "Permanent link")

[Trades.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_ranges "vectorbtpro.portfolio.trades.Trades.get_ranges") with default arguments.

* * *

### rel_expectancy cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_expectancy "Permanent link")

[Trades.get_expectancy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_expectancy "vectorbtpro.portfolio.trades.Trades.get_expectancy") with arguments `{'use_returns': True, 'wrap_kwargs': {'name_or_index': 'rel_expectancy'}}`.

* * *

### rel_profit_factor cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_profit_factor "Permanent link")

[Trades.get_profit_factor](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_profit_factor "vectorbtpro.portfolio.trades.Trades.get_profit_factor") with arguments `{'use_returns': True, 'wrap_kwargs': {'name_or_index': 'rel_profit_factor'}}`.

* * *

### rel_sqn cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.rel_sqn "Permanent link")

[Trades.get_sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_sqn "vectorbtpro.portfolio.trades.Trades.get_sqn") with arguments `{'use_returns': True, 'wrap_kwargs': {'name_or_index': 'rel_sqn'}}`.

* * *

### returns cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.returns "Permanent link")

Mapped array of the field `return`.

* * *

### running_edge_ratio cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.running_edge_ratio "Permanent link")

[Trades.get_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio "vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio") with default arguments.

* * *

### short_view cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.short_view "Permanent link")

[Trades.get_short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_short_view "vectorbtpro.portfolio.trades.Trades.get_short_view") with default arguments.

* * *

### size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.size "Permanent link")

Mapped array of the field `size`.

* * *

### sqn cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.sqn "Permanent link")

[Trades.get_sqn](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_sqn "vectorbtpro.portfolio.trades.Trades.get_sqn") with arguments `{'use_returns': False}`.

* * *

### stats_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py#L1240-L1250 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.stats_defaults "Permanent link")

Defaults for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.trades.Trades.stats").

Merges [Ranges.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.stats_defaults "vectorbtpro.generic.ranges.Ranges.stats_defaults") and `stats` from [trades](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.trades "vectorbtpro._settings.trades").

* * *

### subplots property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.subplots "Permanent link")

Subplots supported by [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-2)    plot=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-3)        title='Trades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-4)        yaxis_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-5)            title='Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-6)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-7)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-8)        plot_func='plot',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-9)        tags='trades'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-10)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-11)    plot_pnl=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-12)        title='Trade PnL',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-13)        yaxis_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-14)            title='Trade PnL'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-15)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-16)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-17)        plot_func='plot_pnl',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-18)        tags='trades'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-19)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#__codelineno-75-20))
    

Returns `Trades._subplots`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `Trades._subplots`.

* * *

### win_rate cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.win_rate "Permanent link")

[Trades.get_win_rate](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_win_rate "vectorbtpro.portfolio.trades.Trades.get_win_rate") with default arguments.

* * *

### winning cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.winning "Permanent link")

[Trades.get_winning](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning "vectorbtpro.portfolio.trades.Trades.get_winning") with default arguments.

* * *

### winning_streak cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.winning_streak "Permanent link")

[Trades.get_winning_streak](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning_streak "vectorbtpro.portfolio.trades.Trades.get_winning_streak") with default arguments.

* * *

### worst_price cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price "Permanent link")

[Trades.get_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price "vectorbtpro.portfolio.trades.Trades.get_worst_price") with default arguments.

* * *

### worst_price_idx cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/trades.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price_idx "Permanent link")

[Trades.get_worst_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_worst_price_idx "vectorbtpro.portfolio.trades.Trades.get_worst_price_idx") with default arguments.
