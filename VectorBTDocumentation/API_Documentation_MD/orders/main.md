orders records

#  orders module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders "Permanent link")

Base class for working with order records.

Order records capture information on filled orders. Orders are mainly populated when simulating a portfolio and can be accessed as [Portfolio.orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.orders "vectorbtpro.portfolio.base.Portfolio.orders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-0-3)>>> price = vbt.RandomData.pull(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-0-4)...     ['a', 'b'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-0-5)...     start=datetime(2020, 1, 1),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-0-6)...     end=datetime(2020, 3, 1),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-0-7)...     seed=vbt.key_dict(a=42, b=43)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-0-8)... ).get()
    

100%
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-1)>>> size = pd.DataFrame({
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-2)...     'a': np.random.randint(-1, 2, size=len(price.index)),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-3)...     'b': np.random.randint(-1, 2, size=len(price.index)),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-4)... }, index=price.index, columns=price.columns)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-5)>>> pf = vbt.Portfolio.from_orders(price, size, fees=0.01, freq='d')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-7)>>> pf.orders.side_buy.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-8)symbol
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-9)a    17
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-10)b    15
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-11)Name: count, dtype: int64
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-13)>>> pf.orders.side_sell.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-14)symbol
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-15)a    24
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-16)b    26
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-1-17)Name: count, dtype: int64
    

## Stats[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#stats "Permanent link")

Hint

See [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats") and [Orders.metrics](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.metrics "vectorbtpro.portfolio.orders.Orders.metrics").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-1)>>> pf.orders['a'].stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-2)Start                  2019-12-31 22:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-3)End                    2020-02-29 22:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-4)Period                          61 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-5)Total Records                                 41
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-6)Side Counts: Buy                              17
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-7)Side Counts: Sell                             24
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-8)Size: Min              0 days 19:33:05.006182372
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-9)Size: Median                     1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-10)Size: Max                        1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-11)Fees: Min              0 days 20:26:25.905776572
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-12)Fees: Median           0 days 22:46:22.693324744
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-13)Fees: Max              1 days 01:04:25.541681491
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-14)Weighted Buy Price                      94.69917
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-15)Weighted Sell Price                    95.742148
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-2-16)Name: a, dtype: object
    

[StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.orders.Orders.stats") also supports (re-)grouping:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-1)>>> pf.orders.stats(group_by=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-2)Start                  2019-12-31 22:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-3)End                    2020-02-29 22:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-4)Period                          61 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-5)Total Records                                 82
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-6)Side Counts: Buy                              32
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-7)Side Counts: Sell                             50
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-8)Size: Min              0 days 19:33:05.006182372
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-9)Size: Median                     1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-10)Size: Max                        1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-11)Fees: Min              0 days 20:26:25.905776572
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-12)Fees: Median           0 days 23:58:29.773897679
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-13)Fees: Max              1 days 02:29:08.904770159
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-14)Weighted Buy Price                     98.804452
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-15)Weighted Sell Price                    99.969934
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-3-16)Name: group, dtype: object
    

## Plots[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#plots "Permanent link")

Hint

See [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots") and [Orders.subplots](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.subplots "vectorbtpro.portfolio.orders.Orders.subplots").

[Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders") class has a single subplot based on [Orders.plot](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.plot "vectorbtpro.portfolio.orders.Orders.plot"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-4-1)>>> pf.orders['a'].plots().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/orders_plots.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/orders_plots.dark.svg#only-dark)

* * *

## fs_orders_attach_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.fs_orders_attach_field_config "Permanent link")

Config of fields to be attached to [FSOrders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders "vectorbtpro.portfolio.orders.FSOrders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-5-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-5-2)    type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-5-3)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-5-4)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-5-5)    stop_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-5-6)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-5-7)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-5-8))
    

* * *

## fs_orders_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.fs_orders_field_config "Permanent link")

Field config for [FSOrders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders "vectorbtpro.portfolio.orders.FSOrders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-5)        ('signal_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-6)        ('creation_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-7)        ('idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-8)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-9)        ('price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-10)        ('fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-11)        ('side', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-12)        ('type', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-13)        ('stop_type', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-14)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-15)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-16)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-17)            title='Fill Index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-18)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-19)        signal_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-20)            title='Signal Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-21)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-22)            noindex=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-23)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-24)        creation_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-25)            title='Creation Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-26)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-27)            noindex=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-28)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-29)        type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-30)            title='Type',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-31)            mapping=OrderTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-32)                Market=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-33)                Limit=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-34)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-35)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-36)        stop_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-37)            title='Stop Type',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-38)            mapping=StopTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-39)                SL=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-40)                TSL=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-41)                TTP=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-42)                TP=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-43)                TD=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-44)                DT=5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-45)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-46)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-47)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-6-48))
    

* * *

## fs_orders_shortcut_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.fs_orders_shortcut_config "Permanent link")

Config of shortcut properties to be attached to [FSOrders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders "vectorbtpro.portfolio.orders.FSOrders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-2)    stop_orders=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-3)    ranges=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-4)    creation_ranges=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-5)    fill_ranges=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-6)    signal_to_creation_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-7)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-8)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-9)    creation_to_fill_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-10)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-11)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-12)    signal_to_fill_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-13)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-14)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-7-15))
    

* * *

## orders_attach_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.orders_attach_field_config "Permanent link")

Config of fields to be attached to [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-8-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-8-2)    side=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-8-3)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-8-4)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-8-5))
    

* * *

## orders_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.orders_field_config "Permanent link")

Field config for [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-5)        ('idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-6)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-7)        ('price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-8)        ('fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-9)        ('side', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-10)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-11)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-12)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-13)            title='Order Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-14)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-15)        idx=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-16)        size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-17)            title='Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-18)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-19)        price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-20)            title='Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-21)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-22)        fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-23)            title='Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-24)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-25)        side=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-26)            title='Side',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-27)            mapping=OrderSideT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-28)                Buy=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-29)                Sell=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-30)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-31)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-32)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-33)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-9-34))
    

* * *

## orders_shortcut_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.orders_shortcut_config "Permanent link")

Config of shortcut properties to be attached to [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-2)    long_view=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-3)    short_view=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-4)    signed_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-5)        obj_type='mapped'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-6)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-7)    value=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-8)        obj_type='mapped'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-9)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-10)    weighted_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-11)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-12)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-13)    price_status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-14)        obj_type='mapped'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-15)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-10-16))
    

* * *

## FSOrders class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L642-L771 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-1)FSOrders(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-11-9))
    

Extends [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders") for working with order records generated from signals.

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
  * [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords "vectorbtpro.generic.price_records.PriceRecords")
  * [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.portfolio.orders.Orders.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.portfolio.orders.Orders.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.portfolio.orders.Orders.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.portfolio.orders.Orders.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.portfolio.orders.Orders.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.portfolio.orders.Orders.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.portfolio.orders.Orders.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.portfolio.orders.Orders.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.portfolio.orders.Orders.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.portfolio.orders.Orders.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.portfolio.orders.Orders.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.portfolio.orders.Orders.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.portfolio.orders.Orders.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.portfolio.orders.Orders.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.portfolio.orders.Orders.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.portfolio.orders.Orders.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.portfolio.orders.Orders.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.portfolio.orders.Orders.prettify")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.portfolio.orders.Orders.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.portfolio.orders.Orders.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.portfolio.orders.Orders.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.portfolio.orders.Orders.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.portfolio.orders.Orders.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.portfolio.orders.Orders.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.portfolio.orders.Orders.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.portfolio.orders.Orders.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.portfolio.orders.Orders.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.portfolio.orders.Orders.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.portfolio.orders.Orders.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.portfolio.orders.Orders.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.portfolio.orders.Orders.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.portfolio.orders.Orders.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.portfolio.orders.Orders.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.portfolio.orders.Orders.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.portfolio.orders.Orders.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.portfolio.orders.Orders.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.portfolio.orders.Orders.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.portfolio.orders.Orders.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.portfolio.orders.Orders.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.portfolio.orders.Orders.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.portfolio.orders.Orders.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.portfolio.orders.Orders.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.portfolio.orders.Orders.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.portfolio.orders.Orders.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.portfolio.orders.Orders.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.portfolio.orders.Orders.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.portfolio.orders.Orders.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.portfolio.orders.Orders.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.portfolio.orders.Orders.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.portfolio.orders.Orders.as_param")
  * [Orders.bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close "vectorbtpro.portfolio.orders.Orders.bar_close")
  * [Orders.bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close_time "vectorbtpro.portfolio.orders.Orders.bar_close_time")
  * [Orders.bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_high "vectorbtpro.portfolio.orders.Orders.bar_high")
  * [Orders.bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_low "vectorbtpro.portfolio.orders.Orders.bar_low")
  * [Orders.bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open "vectorbtpro.portfolio.orders.Orders.bar_open")
  * [Orders.bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open_time "vectorbtpro.portfolio.orders.Orders.bar_open_time")
  * [Orders.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.portfolio.orders.Orders.close")
  * [Orders.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.portfolio.orders.Orders.cls_dir")
  * [Orders.col](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.col "vectorbtpro.portfolio.orders.Orders.col")
  * [Orders.col_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_arr "vectorbtpro.portfolio.orders.Orders.col_arr")
  * [Orders.col_mapper](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_mapper "vectorbtpro.portfolio.orders.Orders.col_mapper")
  * [Orders.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.portfolio.orders.Orders.column_only_select")
  * [Orders.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.portfolio.orders.Orders.config")
  * [Orders.fees](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.fees "vectorbtpro.portfolio.orders.Orders.fees")
  * [Orders.field_names](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.field_names "vectorbtpro.portfolio.orders.Orders.field_names")
  * [Orders.get_long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_long_view "vectorbtpro.portfolio.orders.Orders.get_long_view")
  * [Orders.get_price_status](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_price_status "vectorbtpro.portfolio.orders.Orders.get_price_status")
  * [Orders.get_short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_short_view "vectorbtpro.portfolio.orders.Orders.get_short_view")
  * [Orders.get_signed_size](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_signed_size "vectorbtpro.portfolio.orders.Orders.get_signed_size")
  * [Orders.get_value](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_value "vectorbtpro.portfolio.orders.Orders.get_value")
  * [Orders.get_weighted_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_weighted_price "vectorbtpro.portfolio.orders.Orders.get_weighted_price")
  * [Orders.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.portfolio.orders.Orders.group_select")
  * [Orders.high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.high "vectorbtpro.portfolio.orders.Orders.high")
  * [Orders.id](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.id "vectorbtpro.portfolio.orders.Orders.id")
  * [Orders.id_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.id_arr "vectorbtpro.portfolio.orders.Orders.id_arr")
  * [Orders.idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.idx "vectorbtpro.portfolio.orders.Orders.idx")
  * [Orders.idx_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.idx_arr "vectorbtpro.portfolio.orders.Orders.idx_arr")
  * [Orders.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.portfolio.orders.Orders.iloc")
  * [Orders.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.portfolio.orders.Orders.indexing_kwargs")
  * [Orders.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.portfolio.orders.Orders.loc")
  * [Orders.long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.long_view "vectorbtpro.portfolio.orders.Orders.long_view")
  * [Orders.low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.low "vectorbtpro.portfolio.orders.Orders.low")
  * [Orders.open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.open "vectorbtpro.portfolio.orders.Orders.open")
  * [Orders.pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.pd_mask "vectorbtpro.portfolio.orders.Orders.pd_mask")
  * [Orders.plot](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.plot "vectorbtpro.portfolio.orders.Orders.plot")
  * [Orders.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.plots_defaults "vectorbtpro.portfolio.orders.Orders.plots_defaults")
  * [Orders.price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.price "vectorbtpro.portfolio.orders.Orders.price")
  * [Orders.price_status](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.price_status "vectorbtpro.portfolio.orders.Orders.price_status")
  * [Orders.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.portfolio.orders.Orders.range_only_select")
  * [Orders.readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.readable "vectorbtpro.portfolio.orders.Orders.readable")
  * [Orders.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.portfolio.orders.Orders.rec_state")
  * [Orders.recarray](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.recarray "vectorbtpro.portfolio.orders.Orders.recarray")
  * [Orders.records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records "vectorbtpro.portfolio.orders.Orders.records")
  * [Orders.records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_arr "vectorbtpro.portfolio.orders.Orders.records_arr")
  * [Orders.records_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_readable "vectorbtpro.portfolio.orders.Orders.records_readable")
  * [Orders.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.portfolio.orders.Orders.self_aliases")
  * [Orders.short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.short_view "vectorbtpro.portfolio.orders.Orders.short_view")
  * [Orders.side](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.side "vectorbtpro.portfolio.orders.Orders.side")
  * [Orders.side_buy](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.side_buy "vectorbtpro.portfolio.orders.Orders.side_buy")
  * [Orders.side_sell](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.side_sell "vectorbtpro.portfolio.orders.Orders.side_sell")
  * [Orders.signed_size](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.signed_size "vectorbtpro.portfolio.orders.Orders.signed_size")
  * [Orders.size](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.size "vectorbtpro.portfolio.orders.Orders.size")
  * [Orders.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.stats_defaults "vectorbtpro.portfolio.orders.Orders.stats_defaults")
  * [Orders.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.portfolio.orders.Orders.unwrapped")
  * [Orders.value](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.value "vectorbtpro.portfolio.orders.Orders.value")
  * [Orders.values](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.values "vectorbtpro.portfolio.orders.Orders.values")
  * [Orders.weighted_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.weighted_price "vectorbtpro.portfolio.orders.Orders.weighted_price")
  * [Orders.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.portfolio.orders.Orders.wrapper")
  * [Orders.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.portfolio.orders.Orders.xloc")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.portfolio.orders.Orders.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.portfolio.orders.Orders.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.portfolio.orders.Orders.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.portfolio.orders.Orders.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.portfolio.orders.Orders.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.portfolio.orders.Orders.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.portfolio.orders.Orders.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.portfolio.orders.Orders.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.portfolio.orders.Orders.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.portfolio.orders.Orders.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.portfolio.orders.Orders.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.portfolio.orders.Orders.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.portfolio.orders.Orders.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.portfolio.orders.Orders.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.portfolio.orders.Orders.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.portfolio.orders.Orders.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.portfolio.orders.Orders.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.portfolio.orders.Orders.pprint")
  * [PriceRecords.from_records](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.from_records "vectorbtpro.portfolio.orders.Orders.from_records")
  * [PriceRecords.get_bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close "vectorbtpro.portfolio.orders.Orders.get_bar_close")
  * [PriceRecords.get_bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close_time "vectorbtpro.portfolio.orders.Orders.get_bar_close_time")
  * [PriceRecords.get_bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_high "vectorbtpro.portfolio.orders.Orders.get_bar_high")
  * [PriceRecords.get_bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_low "vectorbtpro.portfolio.orders.Orders.get_bar_low")
  * [PriceRecords.get_bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open "vectorbtpro.portfolio.orders.Orders.get_bar_open")
  * [PriceRecords.get_bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open_time "vectorbtpro.portfolio.orders.Orders.get_bar_open_time")
  * [PriceRecords.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func "vectorbtpro.portfolio.orders.Orders.indexing_func")
  * [PriceRecords.indexing_func_meta](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func_meta "vectorbtpro.portfolio.orders.Orders.indexing_func_meta")
  * [PriceRecords.resample](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resample "vectorbtpro.portfolio.orders.Orders.resample")
  * [PriceRecords.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_column_stack_kwargs "vectorbtpro.portfolio.orders.Orders.resolve_column_stack_kwargs")
  * [PriceRecords.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_row_stack_kwargs "vectorbtpro.portfolio.orders.Orders.resolve_row_stack_kwargs")
  * [Records.apply](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply "vectorbtpro.portfolio.orders.Orders.apply")
  * [Records.apply_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply_mask "vectorbtpro.portfolio.orders.Orders.apply_mask")
  * [Records.build_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.build_field_config_doc "vectorbtpro.portfolio.orders.Orders.build_field_config_doc")
  * [Records.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack "vectorbtpro.portfolio.orders.Orders.column_stack")
  * [Records.column_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack_records_arrs "vectorbtpro.portfolio.orders.Orders.column_stack_records_arrs")
  * [Records.count](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.count "vectorbtpro.portfolio.orders.Orders.count")
  * [Records.coverage_map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.coverage_map "vectorbtpro.portfolio.orders.Orders.coverage_map")
  * [Records.first_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.first_n "vectorbtpro.portfolio.orders.Orders.first_n")
  * [Records.get_apply_mapping_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_arr "vectorbtpro.portfolio.orders.Orders.get_apply_mapping_arr")
  * [Records.get_apply_mapping_str_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_str_arr "vectorbtpro.portfolio.orders.Orders.get_apply_mapping_str_arr")
  * [Records.get_column_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_column_stack_record_indices "vectorbtpro.portfolio.orders.Orders.get_column_stack_record_indices")
  * [Records.get_field_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_arr "vectorbtpro.portfolio.orders.Orders.get_field_arr")
  * [Records.get_field_mapping](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_mapping "vectorbtpro.portfolio.orders.Orders.get_field_mapping")
  * [Records.get_field_name](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_name "vectorbtpro.portfolio.orders.Orders.get_field_name")
  * [Records.get_field_setting](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_setting "vectorbtpro.portfolio.orders.Orders.get_field_setting")
  * [Records.get_field_title](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_title "vectorbtpro.portfolio.orders.Orders.get_field_title")
  * [Records.get_map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field "vectorbtpro.portfolio.orders.Orders.get_map_field")
  * [Records.get_map_field_to_columns](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_columns "vectorbtpro.portfolio.orders.Orders.get_map_field_to_columns")
  * [Records.get_map_field_to_index](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_index "vectorbtpro.portfolio.orders.Orders.get_map_field_to_index")
  * [Records.get_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_pd_mask "vectorbtpro.portfolio.orders.Orders.get_pd_mask")
  * [Records.get_row_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_row_stack_record_indices "vectorbtpro.portfolio.orders.Orders.get_row_stack_record_indices")
  * [Records.has_conflicts](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.has_conflicts "vectorbtpro.portfolio.orders.Orders.has_conflicts")
  * [Records.is_sorted](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.is_sorted "vectorbtpro.portfolio.orders.Orders.is_sorted")
  * [Records.last_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.last_n "vectorbtpro.portfolio.orders.Orders.last_n")
  * [Records.map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map "vectorbtpro.portfolio.orders.Orders.map")
  * [Records.map_array](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_array "vectorbtpro.portfolio.orders.Orders.map_array")
  * [Records.map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_field "vectorbtpro.portfolio.orders.Orders.map_field")
  * [Records.override_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.override_field_config_doc "vectorbtpro.portfolio.orders.Orders.override_field_config_doc")
  * [Records.prepare_customdata](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.prepare_customdata "vectorbtpro.portfolio.orders.Orders.prepare_customdata")
  * [Records.random_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.random_n "vectorbtpro.portfolio.orders.Orders.random_n")
  * [Records.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.replace "vectorbtpro.portfolio.orders.Orders.replace")
  * [Records.resample_meta](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_meta "vectorbtpro.portfolio.orders.Orders.resample_meta")
  * [Records.resample_records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_records_arr "vectorbtpro.portfolio.orders.Orders.resample_records_arr")
  * [Records.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack "vectorbtpro.portfolio.orders.Orders.row_stack")
  * [Records.row_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack_records_arrs "vectorbtpro.portfolio.orders.Orders.row_stack_records_arrs")
  * [Records.select_cols](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.select_cols "vectorbtpro.portfolio.orders.Orders.select_cols")
  * [Records.sort](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.sort "vectorbtpro.portfolio.orders.Orders.sort")
  * [Records.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.to_readable "vectorbtpro.portfolio.orders.Orders.to_readable")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.portfolio.orders.Orders.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.portfolio.orders.Orders.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.portfolio.orders.Orders.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.orders.Orders.stats")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.portfolio.orders.Orders.apply_to_index")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.portfolio.orders.Orders.regroup")
  * [Wrapping.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "vectorbtpro.portfolio.orders.Orders.resolve_self")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.portfolio.orders.Orders.resolve_stack_kwargs")



* * *

### creation_idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.creation_idx "Permanent link")

Mapped array of the field `creation_idx`.

* * *

### creation_ranges cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.creation_ranges "Permanent link")

[FSOrders.get_creation_ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_creation_ranges "vectorbtpro.portfolio.orders.FSOrders.get_creation_ranges") with default arguments.

* * *

### creation_to_fill_duration cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.creation_to_fill_duration "Permanent link")

[FSOrders.get_creation_to_fill_duration](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_creation_to_fill_duration "vectorbtpro.portfolio.orders.FSOrders.get_creation_to_fill_duration") with default arguments.

* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.field_config "Permanent link")

Field config of [FSOrders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders "vectorbtpro.portfolio.orders.FSOrders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-5)        ('signal_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-6)        ('creation_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-7)        ('idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-8)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-9)        ('price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-10)        ('fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-11)        ('side', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-12)        ('type', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-13)        ('stop_type', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-14)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-15)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-16)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-17)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-18)            title='Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-19)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-20)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-21)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-22)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-23)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-24)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-25)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-26)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-27)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-28)            name='idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-29)            title='Fill Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-30)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-31)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-32)        size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-33)            title='Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-34)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-35)        price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-36)            title='Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-37)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-38)        fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-39)            title='Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-40)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-41)        side=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-42)            title='Side',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-43)            mapping=OrderSideT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-44)                Buy=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-45)                Sell=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-46)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-47)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-48)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-49)        signal_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-50)            title='Signal Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-51)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-52)            noindex=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-53)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-54)        creation_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-55)            title='Creation Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-56)            mapping='index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-57)            noindex=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-58)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-59)        type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-60)            title='Type',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-61)            mapping=OrderTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-62)                Market=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-63)                Limit=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-64)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-65)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-66)        stop_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-67)            title='Stop Type',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-68)            mapping=StopTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-69)                SL=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-70)                TSL=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-71)                TTP=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-72)                TP=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-73)                TD=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-74)                DT=5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-75)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-76)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-77)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-12-78))
    

Returns `FSOrders._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `FSOrders._field_config`.

* * *

### fill_ranges cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.fill_ranges "Permanent link")

[FSOrders.get_fill_ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_fill_ranges "vectorbtpro.portfolio.orders.FSOrders.get_fill_ranges") with default arguments.

* * *

### get_creation_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L674-L690 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_creation_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-13-1)FSOrders.get_creation_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-13-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-13-3))
    

Get records of type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for signal-to-creation ranges.

* * *

### get_creation_to_fill_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L715-L718 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_creation_to_fill_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-14-1)FSOrders.get_creation_to_fill_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-14-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-14-3))
    

Get duration between creation and fill.

* * *

### get_fill_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L692-L708 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_fill_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-15-1)FSOrders.get_fill_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-15-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-15-3))
    

Get records of type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for creation-to-fill ranges.

* * *

### get_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L656-L672 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-16-1)FSOrders.get_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-16-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-16-3))
    

Get records of type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for signal-to-fill ranges.

* * *

### get_signal_to_creation_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L710-L713 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_signal_to_creation_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-17-1)FSOrders.get_signal_to_creation_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-17-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-17-3))
    

Get duration between signal and creation.

* * *

### get_signal_to_fill_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L720-L723 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_signal_to_fill_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-18-1)FSOrders.get_signal_to_fill_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-18-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-18-3))
    

Get duration between signal and fill.

* * *

### get_stop_orders method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L652-L654 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_stop_orders "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-19-1)FSOrders.get_stop_orders(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-19-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-19-3))
    

Get stop orders.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.metrics "Permanent link")

Metrics supported by [FSOrders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders "vectorbtpro.portfolio.orders.FSOrders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-4)        calc_func=<function Orders.<lambda> at 0x174d307c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-10)        calc_func=<function Orders.<lambda> at 0x174d30860>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-16)        calc_func=<function Orders.<lambda> at 0x174d30900>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-21)    total_records=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-22)        title='Total Records',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-23)        calc_func='count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-24)        tags='records'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-26)    side_counts=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-27)        title='Side Counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-28)        calc_func='side.value_counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-29)        incl_all_keys=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-30)        post_calc_func=<function Orders.<lambda> at 0x174d309a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-31)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-32)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-33)            'side'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-34)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-35)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-36)    type_counts=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-37)        title='Type Counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-38)        calc_func='type.value_counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-39)        incl_all_keys=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-40)        post_calc_func=<function FSOrders.<lambda> at 0x174d31c60>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-41)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-42)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-43)            'type'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-44)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-45)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-46)    stop_type_counts=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-47)        title='Stop Type Counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-48)        calc_func='stop_type.value_counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-49)        incl_all_keys=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-50)        post_calc_func=<function FSOrders.<lambda> at 0x174d31d00>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-51)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-52)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-53)            'stop_type'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-54)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-55)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-56)    size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-57)        title='Size',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-58)        calc_func='size.describe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-59)        post_calc_func=<function Orders.<lambda> at 0x174d30a40>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-60)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-61)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-62)            'size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-63)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-64)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-65)    fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-66)        title='Fees',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-67)        calc_func='fees.describe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-68)        post_calc_func=<function Orders.<lambda> at 0x174d30ae0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-69)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-70)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-71)            'fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-72)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-73)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-74)    weighted_buy_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-75)        title='Weighted Buy Price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-76)        calc_func='side_buy.get_weighted_price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-77)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-78)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-79)            'buy',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-80)            'price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-81)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-82)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-83)    weighted_sell_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-84)        title='Weighted Sell Price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-85)        calc_func='side_sell.get_weighted_price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-86)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-87)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-88)            'sell',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-89)            'price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-90)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-91)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-92)    avg_signal_to_creation_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-93)        title='Avg Signal-Creation Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-94)        calc_func='signal_to_creation_duration.mean',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-95)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-96)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-97)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-98)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-99)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-100)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-101)    avg_creation_to_fill_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-102)        title='Avg Creation-Fill Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-103)        calc_func='creation_to_fill_duration.mean',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-104)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-105)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-106)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-107)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-108)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-109)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-110)    avg_signal_to_fill_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-111)        title='Avg Signal-Fill Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-112)        calc_func='signal_to_fill_duration.mean',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-113)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-114)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-115)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-116)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-117)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-118)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-20-119))
    

Returns `FSOrders._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `FSOrders._metrics`.

* * *

### ranges cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.ranges "Permanent link")

[FSOrders.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_ranges "vectorbtpro.portfolio.orders.FSOrders.get_ranges") with default arguments.

* * *

### signal_idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.signal_idx "Permanent link")

Mapped array of the field `signal_idx`.

* * *

### signal_to_creation_duration cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.signal_to_creation_duration "Permanent link")

[FSOrders.get_signal_to_creation_duration](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_signal_to_creation_duration "vectorbtpro.portfolio.orders.FSOrders.get_signal_to_creation_duration") with default arguments.

* * *

### signal_to_fill_duration cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.signal_to_fill_duration "Permanent link")

[FSOrders.get_signal_to_fill_duration](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_signal_to_fill_duration "vectorbtpro.portfolio.orders.FSOrders.get_signal_to_fill_duration") with default arguments.

* * *

### stop_orders cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.stop_orders "Permanent link")

[FSOrders.get_stop_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.get_stop_orders "vectorbtpro.portfolio.orders.FSOrders.get_stop_orders") with default arguments.

* * *

### stop_type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.stop_type "Permanent link")

Mapped array of the field `stop_type`.

* * *

### stop_type_dt cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.stop_type_dt "Permanent link")

Records filtered by `stop_type == 5`.

* * *

### stop_type_sl cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.stop_type_sl "Permanent link")

Records filtered by `stop_type == 0`.

* * *

### stop_type_td cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.stop_type_td "Permanent link")

Records filtered by `stop_type == 4`.

* * *

### stop_type_tp cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.stop_type_tp "Permanent link")

Records filtered by `stop_type == 3`.

* * *

### stop_type_tsl cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.stop_type_tsl "Permanent link")

Records filtered by `stop_type == 1`.

* * *

### stop_type_ttp cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.stop_type_ttp "Permanent link")

Records filtered by `stop_type == 2`.

* * *

### type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.type "Permanent link")

Mapped array of the field `type`.

* * *

### type_limit cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.type_limit "Permanent link")

Records filtered by `type == 1`.

* * *

### type_market cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders.type_market "Permanent link")

Records filtered by `type == 0`.

* * *

## Orders class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L194-L556 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-1)Orders(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-21-9))
    

Extends [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords "vectorbtpro.generic.price_records.PriceRecords") for working with order records.

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
  * [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.generic.price_records.PriceRecords.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.generic.price_records.PriceRecords.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.generic.price_records.PriceRecords.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.generic.price_records.PriceRecords.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.generic.price_records.PriceRecords.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.price_records.PriceRecords.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.price_records.PriceRecords.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.price_records.PriceRecords.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.price_records.PriceRecords.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.price_records.PriceRecords.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.price_records.PriceRecords.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.price_records.PriceRecords.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.price_records.PriceRecords.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.price_records.PriceRecords.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.price_records.PriceRecords.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.price_records.PriceRecords.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.price_records.PriceRecords.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.price_records.PriceRecords.prettify")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.price_records.PriceRecords.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.price_records.PriceRecords.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.price_records.PriceRecords.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.price_records.PriceRecords.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.price_records.PriceRecords.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.price_records.PriceRecords.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.price_records.PriceRecords.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.price_records.PriceRecords.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.price_records.PriceRecords.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.price_records.PriceRecords.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.price_records.PriceRecords.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.price_records.PriceRecords.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.price_records.PriceRecords.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.price_records.PriceRecords.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.generic.price_records.PriceRecords.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.generic.price_records.PriceRecords.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.generic.price_records.PriceRecords.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.generic.price_records.PriceRecords.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.generic.price_records.PriceRecords.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.generic.price_records.PriceRecords.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.generic.price_records.PriceRecords.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.generic.price_records.PriceRecords.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.generic.price_records.PriceRecords.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.generic.price_records.PriceRecords.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.generic.price_records.PriceRecords.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.generic.price_records.PriceRecords.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.generic.price_records.PriceRecords.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.generic.price_records.PriceRecords.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.generic.price_records.PriceRecords.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.generic.price_records.PriceRecords.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.generic.price_records.PriceRecords.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.generic.price_records.PriceRecords.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.generic.price_records.PriceRecords.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.price_records.PriceRecords.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.price_records.PriceRecords.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.price_records.PriceRecords.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.price_records.PriceRecords.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.price_records.PriceRecords.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.price_records.PriceRecords.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.price_records.PriceRecords.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.price_records.PriceRecords.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.price_records.PriceRecords.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.price_records.PriceRecords.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.price_records.PriceRecords.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.price_records.PriceRecords.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.generic.price_records.PriceRecords.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.generic.price_records.PriceRecords.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.price_records.PriceRecords.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.generic.price_records.PriceRecords.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.price_records.PriceRecords.pprint")
  * [PriceRecords.bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close "vectorbtpro.generic.price_records.PriceRecords.bar_close")
  * [PriceRecords.bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_close_time "vectorbtpro.generic.price_records.PriceRecords.bar_close_time")
  * [PriceRecords.bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_high "vectorbtpro.generic.price_records.PriceRecords.bar_high")
  * [PriceRecords.bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_low "vectorbtpro.generic.price_records.PriceRecords.bar_low")
  * [PriceRecords.bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open "vectorbtpro.generic.price_records.PriceRecords.bar_open")
  * [PriceRecords.bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.bar_open_time "vectorbtpro.generic.price_records.PriceRecords.bar_open_time")
  * [PriceRecords.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.generic.price_records.PriceRecords.close")
  * [PriceRecords.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.generic.price_records.PriceRecords.cls_dir")
  * [PriceRecords.col_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_arr "vectorbtpro.generic.price_records.PriceRecords.col_arr")
  * [PriceRecords.col_mapper](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.col_mapper "vectorbtpro.generic.price_records.PriceRecords.col_mapper")
  * [PriceRecords.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.generic.price_records.PriceRecords.column_only_select")
  * [PriceRecords.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.price_records.PriceRecords.config")
  * [PriceRecords.field_names](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.field_names "vectorbtpro.generic.price_records.PriceRecords.field_names")
  * [PriceRecords.from_records](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.from_records "vectorbtpro.generic.price_records.PriceRecords.from_records")
  * [PriceRecords.get_bar_close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close "vectorbtpro.generic.price_records.PriceRecords.get_bar_close")
  * [PriceRecords.get_bar_close_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_close_time "vectorbtpro.generic.price_records.PriceRecords.get_bar_close_time")
  * [PriceRecords.get_bar_high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_high "vectorbtpro.generic.price_records.PriceRecords.get_bar_high")
  * [PriceRecords.get_bar_low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_low "vectorbtpro.generic.price_records.PriceRecords.get_bar_low")
  * [PriceRecords.get_bar_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open "vectorbtpro.generic.price_records.PriceRecords.get_bar_open")
  * [PriceRecords.get_bar_open_time](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.get_bar_open_time "vectorbtpro.generic.price_records.PriceRecords.get_bar_open_time")
  * [PriceRecords.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.generic.price_records.PriceRecords.group_select")
  * [PriceRecords.high](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.high "vectorbtpro.generic.price_records.PriceRecords.high")
  * [PriceRecords.id_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.id_arr "vectorbtpro.generic.price_records.PriceRecords.id_arr")
  * [PriceRecords.idx_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.idx_arr "vectorbtpro.generic.price_records.PriceRecords.idx_arr")
  * [PriceRecords.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.generic.price_records.PriceRecords.iloc")
  * [PriceRecords.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func "vectorbtpro.generic.price_records.PriceRecords.indexing_func")
  * [PriceRecords.indexing_func_meta](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func_meta "vectorbtpro.generic.price_records.PriceRecords.indexing_func_meta")
  * [PriceRecords.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.generic.price_records.PriceRecords.indexing_kwargs")
  * [PriceRecords.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.generic.price_records.PriceRecords.loc")
  * [PriceRecords.low](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.low "vectorbtpro.generic.price_records.PriceRecords.low")
  * [PriceRecords.open](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.open "vectorbtpro.generic.price_records.PriceRecords.open")
  * [PriceRecords.pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.pd_mask "vectorbtpro.generic.price_records.PriceRecords.pd_mask")
  * [PriceRecords.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.generic.price_records.PriceRecords.range_only_select")
  * [PriceRecords.readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.readable "vectorbtpro.generic.price_records.PriceRecords.readable")
  * [PriceRecords.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.price_records.PriceRecords.rec_state")
  * [PriceRecords.recarray](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.recarray "vectorbtpro.generic.price_records.PriceRecords.recarray")
  * [PriceRecords.records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records "vectorbtpro.generic.price_records.PriceRecords.records")
  * [PriceRecords.records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_arr "vectorbtpro.generic.price_records.PriceRecords.records_arr")
  * [PriceRecords.records_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_readable "vectorbtpro.generic.price_records.PriceRecords.records_readable")
  * [PriceRecords.resample](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resample "vectorbtpro.generic.price_records.PriceRecords.resample")
  * [PriceRecords.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_column_stack_kwargs "vectorbtpro.generic.price_records.PriceRecords.resolve_column_stack_kwargs")
  * [PriceRecords.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resolve_row_stack_kwargs "vectorbtpro.generic.price_records.PriceRecords.resolve_row_stack_kwargs")
  * [PriceRecords.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.generic.price_records.PriceRecords.self_aliases")
  * [PriceRecords.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.generic.price_records.PriceRecords.unwrapped")
  * [PriceRecords.values](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.values "vectorbtpro.generic.price_records.PriceRecords.values")
  * [PriceRecords.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.generic.price_records.PriceRecords.wrapper")
  * [PriceRecords.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.generic.price_records.PriceRecords.xloc")
  * [Records.apply](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply "vectorbtpro.generic.price_records.PriceRecords.apply")
  * [Records.apply_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.apply_mask "vectorbtpro.generic.price_records.PriceRecords.apply_mask")
  * [Records.build_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.build_field_config_doc "vectorbtpro.generic.price_records.PriceRecords.build_field_config_doc")
  * [Records.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack "vectorbtpro.generic.price_records.PriceRecords.column_stack")
  * [Records.column_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.column_stack_records_arrs "vectorbtpro.generic.price_records.PriceRecords.column_stack_records_arrs")
  * [Records.count](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.count "vectorbtpro.generic.price_records.PriceRecords.count")
  * [Records.coverage_map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.coverage_map "vectorbtpro.generic.price_records.PriceRecords.coverage_map")
  * [Records.first_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.first_n "vectorbtpro.generic.price_records.PriceRecords.first_n")
  * [Records.get_apply_mapping_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_arr "vectorbtpro.generic.price_records.PriceRecords.get_apply_mapping_arr")
  * [Records.get_apply_mapping_str_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_apply_mapping_str_arr "vectorbtpro.generic.price_records.PriceRecords.get_apply_mapping_str_arr")
  * [Records.get_column_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_column_stack_record_indices "vectorbtpro.generic.price_records.PriceRecords.get_column_stack_record_indices")
  * [Records.get_field_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_arr "vectorbtpro.generic.price_records.PriceRecords.get_field_arr")
  * [Records.get_field_mapping](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_mapping "vectorbtpro.generic.price_records.PriceRecords.get_field_mapping")
  * [Records.get_field_name](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_name "vectorbtpro.generic.price_records.PriceRecords.get_field_name")
  * [Records.get_field_setting](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_setting "vectorbtpro.generic.price_records.PriceRecords.get_field_setting")
  * [Records.get_field_title](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_field_title "vectorbtpro.generic.price_records.PriceRecords.get_field_title")
  * [Records.get_map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field "vectorbtpro.generic.price_records.PriceRecords.get_map_field")
  * [Records.get_map_field_to_columns](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_columns "vectorbtpro.generic.price_records.PriceRecords.get_map_field_to_columns")
  * [Records.get_map_field_to_index](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_map_field_to_index "vectorbtpro.generic.price_records.PriceRecords.get_map_field_to_index")
  * [Records.get_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_pd_mask "vectorbtpro.generic.price_records.PriceRecords.get_pd_mask")
  * [Records.get_row_stack_record_indices](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.get_row_stack_record_indices "vectorbtpro.generic.price_records.PriceRecords.get_row_stack_record_indices")
  * [Records.has_conflicts](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.has_conflicts "vectorbtpro.generic.price_records.PriceRecords.has_conflicts")
  * [Records.is_sorted](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.is_sorted "vectorbtpro.generic.price_records.PriceRecords.is_sorted")
  * [Records.last_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.last_n "vectorbtpro.generic.price_records.PriceRecords.last_n")
  * [Records.map](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map "vectorbtpro.generic.price_records.PriceRecords.map")
  * [Records.map_array](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_array "vectorbtpro.generic.price_records.PriceRecords.map_array")
  * [Records.map_field](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.map_field "vectorbtpro.generic.price_records.PriceRecords.map_field")
  * [Records.override_field_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.override_field_config_doc "vectorbtpro.generic.price_records.PriceRecords.override_field_config_doc")
  * [Records.prepare_customdata](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.prepare_customdata "vectorbtpro.generic.price_records.PriceRecords.prepare_customdata")
  * [Records.random_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.random_n "vectorbtpro.generic.price_records.PriceRecords.random_n")
  * [Records.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.replace "vectorbtpro.generic.price_records.PriceRecords.replace")
  * [Records.resample_meta](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_meta "vectorbtpro.generic.price_records.PriceRecords.resample_meta")
  * [Records.resample_records_arr](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.resample_records_arr "vectorbtpro.generic.price_records.PriceRecords.resample_records_arr")
  * [Records.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack "vectorbtpro.generic.price_records.PriceRecords.row_stack")
  * [Records.row_stack_records_arrs](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.row_stack_records_arrs "vectorbtpro.generic.price_records.PriceRecords.row_stack_records_arrs")
  * [Records.select_cols](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.select_cols "vectorbtpro.generic.price_records.PriceRecords.select_cols")
  * [Records.sort](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.sort "vectorbtpro.generic.price_records.PriceRecords.sort")
  * [Records.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.to_readable "vectorbtpro.generic.price_records.PriceRecords.to_readable")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.generic.price_records.PriceRecords.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.generic.price_records.PriceRecords.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.generic.price_records.PriceRecords.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.price_records.PriceRecords.stats")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.generic.price_records.PriceRecords.apply_to_index")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.generic.price_records.PriceRecords.regroup")
  * [Wrapping.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "vectorbtpro.generic.price_records.PriceRecords.resolve_self")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.generic.price_records.PriceRecords.resolve_stack_kwargs")



**Subclasses**

  * [FSOrders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.FSOrders "vectorbtpro.portfolio.orders.FSOrders")



* * *

### col cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.col "Permanent link")

Mapped array of the field `col`.

* * *

### fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.fees "Permanent link")

Mapped array of the field `fees`.

* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.field_config "Permanent link")

Field config of [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-5)        ('idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-6)        ('size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-7)        ('price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-8)        ('fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-9)        ('side', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-10)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-11)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-12)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-13)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-14)            title='Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-15)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-16)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-17)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-18)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-19)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-20)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-21)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-22)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-23)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-24)            name='idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-25)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-26)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-27)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-28)        size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-29)            title='Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-30)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-31)        price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-32)            title='Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-33)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-34)        fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-35)            title='Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-36)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-37)        side=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-38)            title='Side',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-39)            mapping=OrderSideT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-40)                Buy=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-41)                Sell=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-42)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-43)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-44)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-45)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-22-46))
    

Returns `Orders._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `Orders._field_config`.

* * *

### get_long_view method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L206-L223 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_long_view "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-23-1)Orders.get_long_view(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-23-2)    init_position=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-23-3)    init_price=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-23-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-23-5)    chunked=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-23-6))
    

See [get_long_view_orders_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.get_long_view_orders_nb "vectorbtpro.portfolio.nb.records.get_long_view_orders_nb").

* * *

### get_price_status method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L278-L286 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_price_status "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-24-1)Orders.get_price_status(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-24-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-24-3))
    

See [price_status_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.price_status_nb "vectorbtpro.portfolio.nb.records.price_status_nb").

* * *

### get_short_view method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L225-L242 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_short_view "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-25-1)Orders.get_short_view(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-25-2)    init_position=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-25-3)    init_price=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-25-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-25-5)    chunked=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-25-6))
    

See [get_short_view_orders_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/records/#vectorbtpro.portfolio.nb.records.get_short_view_orders_nb "vectorbtpro.portfolio.nb.records.get_short_view_orders_nb").

* * *

### get_signed_size method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L246-L250 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_signed_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-26-1)Orders.get_signed_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-26-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-26-3))
    

Get signed size.

* * *

### get_value method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L252-L254 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_value "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-27-1)Orders.get_value(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-27-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-27-3))
    

Get value.

* * *

### get_weighted_price method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L256-L276 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_weighted_price "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-28-1)Orders.get_weighted_price(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-28-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-28-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-28-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-28-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-28-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-28-7))
    

Get size-weighted price average.

* * *

### id cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.id "Permanent link")

Mapped array of the field `id`.

* * *

### idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.idx "Permanent link")

Mapped array of the field `idx`.

* * *

### long_view cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.long_view "Permanent link")

[Orders.get_long_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_long_view "vectorbtpro.portfolio.orders.Orders.get_long_view") with default arguments.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.metrics "Permanent link")

Metrics supported by [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-4)        calc_func=<function Orders.<lambda> at 0x174d307c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-10)        calc_func=<function Orders.<lambda> at 0x174d30860>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-16)        calc_func=<function Orders.<lambda> at 0x174d30900>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-21)    total_records=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-22)        title='Total Records',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-23)        calc_func='count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-24)        tags='records'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-26)    side_counts=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-27)        title='Side Counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-28)        calc_func='side.value_counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-29)        incl_all_keys=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-30)        post_calc_func=<function Orders.<lambda> at 0x174d309a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-31)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-32)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-33)            'side'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-34)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-35)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-36)    size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-37)        title='Size',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-38)        calc_func='size.describe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-39)        post_calc_func=<function Orders.<lambda> at 0x174d30a40>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-40)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-41)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-42)            'size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-43)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-44)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-45)    fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-46)        title='Fees',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-47)        calc_func='fees.describe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-48)        post_calc_func=<function Orders.<lambda> at 0x174d30ae0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-49)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-50)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-51)            'fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-52)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-53)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-54)    weighted_buy_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-55)        title='Weighted Buy Price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-56)        calc_func='side_buy.get_weighted_price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-57)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-58)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-59)            'buy',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-60)            'price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-61)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-62)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-63)    weighted_sell_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-64)        title='Weighted Sell Price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-65)        calc_func='side_sell.get_weighted_price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-66)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-67)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-68)            'sell',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-69)            'price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-70)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-71)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-29-72))
    

Returns `Orders._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `Orders._metrics`.

* * *

### plot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L368-L528 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.plot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-1)Orders.plot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-3)    plot_ohlc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-4)    plot_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-5)    ohlc_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-6)    ohlc_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-7)    close_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-8)    buy_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-9)    sell_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-10)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-11)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-12)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-30-13))
    

Plot orders.

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
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Orders.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.portfolio.orders.Orders.close").
**`buy_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Buy" markers.
**`sell_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Sell" markers.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-31-1)>>> index = pd.date_range("2020", periods=5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-31-2)>>> price = pd.Series([1., 2., 3., 2., 1.], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-31-3)>>> size = pd.Series([1., 1., 1., 1., -1.], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-31-4)>>> orders = vbt.Portfolio.from_orders(price, size).orders
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-31-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-31-6)>>> orders.plot().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/orders_plot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/orders_plot.dark.svg#only-dark)

* * *

### plots_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L530-L540 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.plots_defaults "Permanent link")

Defaults for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.portfolio.orders.Orders.plots").

Merges [PriceRecords.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.plots_defaults "vectorbtpro.generic.price_records.PriceRecords.plots_defaults") and `plots` from [orders](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.orders "vectorbtpro._settings.orders").

* * *

### price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.price "Permanent link")

Mapped array of the field `price`.

* * *

### price_status cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.price_status "Permanent link")

[Orders.get_price_status](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_price_status "vectorbtpro.portfolio.orders.Orders.get_price_status") with default arguments.

* * *

### short_view cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.short_view "Permanent link")

[Orders.get_short_view](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_short_view "vectorbtpro.portfolio.orders.Orders.get_short_view") with default arguments.

* * *

### side cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.side "Permanent link")

Mapped array of the field `side`.

* * *

### side_buy cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.side_buy "Permanent link")

Records filtered by `side == 0`.

* * *

### side_sell cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.side_sell "Permanent link")

Records filtered by `side == 1`.

* * *

### signed_size cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.signed_size "Permanent link")

[Orders.get_signed_size](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_signed_size "vectorbtpro.portfolio.orders.Orders.get_signed_size") with default arguments.

* * *

### size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.size "Permanent link")

Mapped array of the field `size`.

* * *

### stats_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py#L288-L298 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.stats_defaults "Permanent link")

Defaults for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.orders.Orders.stats").

Merges [PriceRecords.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.stats_defaults "vectorbtpro.generic.price_records.PriceRecords.stats_defaults") and `stats` from [orders](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.orders "vectorbtpro._settings.orders").

* * *

### subplots property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.subplots "Permanent link")

Subplots supported by [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-2)    plot=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-3)        title='Orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-4)        yaxis_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-5)            title='Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-6)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-7)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-8)        plot_func='plot',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-9)        tags='orders'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-10)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#__codelineno-32-11))
    

Returns `Orders._subplots`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `Orders._subplots`.

* * *

### value cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.value "Permanent link")

[Orders.get_value](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_value "vectorbtpro.portfolio.orders.Orders.get_value") with default arguments.

* * *

### weighted_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/orders.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.weighted_price "Permanent link")

[Orders.get_weighted_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders.get_weighted_price "vectorbtpro.portfolio.orders.Orders.get_weighted_price") with default arguments.
