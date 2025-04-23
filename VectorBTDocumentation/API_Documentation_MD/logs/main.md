logs records

#  logs module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs "Permanent link")

Base class for working with log records.

Order records capture information on simulation logs. Logs are populated when simulating a portfolio and can be accessed as [Portfolio.logs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.logs "vectorbtpro.portfolio.base.Portfolio.logs").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-3)>>> np.random.seed(42)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-4)>>> price = pd.DataFrame({
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-5)...     'a': np.random.uniform(1, 2, size=100),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-6)...     'b': np.random.uniform(1, 2, size=100)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-7)... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-8)>>> size = pd.DataFrame({
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-9)...     'a': np.random.uniform(-100, 100, size=100),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-10)...     'b': np.random.uniform(-100, 100, size=100),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-11)... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-12)>>> pf = vbt.Portfolio.from_orders(price, size, fees=0.01, freq='d', log=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-13)>>> logs = pf.logs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-15)>>> logs.filled.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-16)a    88
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-17)b    99
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-18)Name: count, dtype: int64
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-19)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-20)>>> logs.ignored.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-21)a    0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-22)b    0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-23)Name: count, dtype: int64
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-24)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-25)>>> logs.rejected.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-26)a    12
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-27)b     1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-0-28)Name: count, dtype: int64
    

## Stats[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#stats "Permanent link")

Hint

See [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats") and [Logs.metrics](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.metrics "vectorbtpro.portfolio.logs.Logs.metrics").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-1)>>> logs['a'].stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-2)Start                             2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-3)End                               2020-04-09 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-4)Period                              100 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-5)Total Records                                     100
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-6)Status Counts: None                                 0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-7)Status Counts: Filled                              88
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-8)Status Counts: Ignored                              0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-9)Status Counts: Rejected                            12
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-10)Status Info Counts: None                           88
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-11)Status Info Counts: NoCashLong                     12
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-1-12)Name: a, dtype: object
    

[StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.logs.Logs.stats") also supports (re-)grouping:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-1)>>> logs.stats(group_by=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-2)Start                             2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-3)End                               2020-04-09 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-4)Period                              100 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-5)Total Records                                     200
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-6)Status Counts: None                                 0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-7)Status Counts: Filled                             187
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-8)Status Counts: Ignored                              0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-9)Status Counts: Rejected                            13
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-10)Status Info Counts: None                          187
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-11)Status Info Counts: NoCashLong                     13
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-2-12)Name: group, dtype: object
    

## Plots[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#plots "Permanent link")

Hint

See [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots") and [Logs.subplots](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.subplots "vectorbtpro.portfolio.logs.Logs.subplots").

This class does not have any subplots.

* * *

## logs_attach_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.logs_attach_field_config "Permanent link")

Config of fields to be attached to [Logs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs "vectorbtpro.portfolio.logs.Logs").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-2)    res_side=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-3)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-4)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-5)    res_status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-6)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-8)    res_status_info=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-9)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-10)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-3-11))
    

* * *

## logs_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.logs_field_config "Permanent link")

Field config for [Logs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs "vectorbtpro.portfolio.logs.Logs").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-4)        ('group', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-5)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-6)        ('idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-7)        ('price_area_open', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-8)        ('price_area_high', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-9)        ('price_area_low', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-10)        ('price_area_close', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-11)        ('st0_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-12)        ('st0_position', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-13)        ('st0_debt', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-14)        ('st0_locked_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-15)        ('st0_free_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-16)        ('st0_val_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-17)        ('st0_value', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-18)        ('req_size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-19)        ('req_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-20)        ('req_size_type', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-21)        ('req_direction', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-22)        ('req_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-23)        ('req_fixed_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-24)        ('req_slippage', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-25)        ('req_min_size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-26)        ('req_max_size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-27)        ('req_size_granularity', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-28)        ('req_leverage', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-29)        ('req_leverage_mode', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-30)        ('req_reject_prob', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-31)        ('req_price_area_vio_mode', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-32)        ('req_allow_partial', 'bool'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-33)        ('req_raise_reject', 'bool'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-34)        ('req_log', 'bool'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-35)        ('res_size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-36)        ('res_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-37)        ('res_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-38)        ('res_side', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-39)        ('res_status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-40)        ('res_status_info', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-41)        ('st1_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-42)        ('st1_position', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-43)        ('st1_debt', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-44)        ('st1_locked_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-45)        ('st1_free_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-46)        ('st1_val_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-47)        ('st1_value', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-48)        ('order_id', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-49)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-50)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-51)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-52)            title='Log Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-53)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-54)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-55)            title='Column'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-56)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-57)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-58)            title='Index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-59)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-60)        group=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-61)            title='Group'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-62)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-63)        price_area_open=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-64)            title='[PA] Open'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-65)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-66)        price_area_high=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-67)            title='[PA] High'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-68)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-69)        price_area_low=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-70)            title='[PA] Low'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-71)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-72)        price_area_close=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-73)            title='[PA] Close'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-74)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-75)        st0_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-76)            title='[ST0] Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-77)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-78)        st0_position=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-79)            title='[ST0] Position'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-80)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-81)        st0_debt=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-82)            title='[ST0] Debt'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-83)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-84)        st0_locked_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-85)            title='[ST0] Locked Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-86)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-87)        st0_free_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-88)            title='[ST0] Free Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-89)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-90)        st0_val_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-91)            title='[ST0] Valuation Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-92)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-93)        st0_value=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-94)            title='[ST0] Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-95)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-96)        req_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-97)            title='[REQ] Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-98)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-99)        req_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-100)            title='[REQ] Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-101)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-102)        req_size_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-103)            title='[REQ] Size Type',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-104)            mapping=SizeTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-105)                Amount=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-106)                Value=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-107)                Percent=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-108)                Percent100=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-109)                ValuePercent=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-110)                ValuePercent100=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-111)                TargetAmount=6,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-112)                TargetValue=7,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-113)                TargetPercent=8,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-114)                TargetPercent100=9
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-115)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-116)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-117)        req_direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-118)            title='[REQ] Direction',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-119)            mapping=DirectionT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-120)                LongOnly=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-121)                ShortOnly=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-122)                Both=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-123)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-124)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-125)        req_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-126)            title='[REQ] Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-127)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-128)        req_fixed_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-129)            title='[REQ] Fixed Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-130)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-131)        req_slippage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-132)            title='[REQ] Slippage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-133)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-134)        req_min_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-135)            title='[REQ] Min Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-136)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-137)        req_max_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-138)            title='[REQ] Max Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-139)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-140)        req_size_granularity=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-141)            title='[REQ] Size Granularity'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-142)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-143)        req_leverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-144)            title='[REQ] Leverage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-145)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-146)        req_leverage_mode=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-147)            title='[REQ] Leverage Mode',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-148)            mapping=LeverageModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-149)                Lazy=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-150)                Eager=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-151)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-152)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-153)        req_reject_prob=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-154)            title='[REQ] Rejection Prob'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-155)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-156)        req_price_area_vio_mode=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-157)            title='[REQ] Price Area Violation Mode',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-158)            mapping=PriceAreaVioModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-159)                Ignore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-160)                Cap=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-161)                Error=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-162)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-163)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-164)        req_allow_partial=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-165)            title='[REQ] Allow Partial'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-166)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-167)        req_raise_reject=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-168)            title='[REQ] Raise Rejection'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-169)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-170)        req_log=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-171)            title='[REQ] Log'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-172)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-173)        res_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-174)            title='[RES] Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-175)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-176)        res_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-177)            title='[RES] Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-178)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-179)        res_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-180)            title='[RES] Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-181)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-182)        res_side=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-183)            title='[RES] Side',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-184)            mapping=OrderSideT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-185)                Buy=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-186)                Sell=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-187)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-188)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-189)        res_status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-190)            title='[RES] Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-191)            mapping=OrderStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-192)                Filled=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-193)                Ignored=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-194)                Rejected=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-195)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-196)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-197)        res_status_info=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-198)            title='[RES] Status Info',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-199)            mapping=OrderStatusInfoT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-200)                SizeNaN=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-201)                PriceNaN=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-202)                ValPriceNaN=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-203)                ValueNaN=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-204)                ValueZeroNeg=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-205)                SizeZero=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-206)                NoCash=6,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-207)                NoOpenPosition=7,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-208)                MaxSizeExceeded=8,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-209)                RandomEvent=9,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-210)                CantCoverFees=10,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-211)                MinSizeNotReached=11,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-212)                PartialFill=12
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-213)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-214)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-215)        st1_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-216)            title='[ST1] Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-217)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-218)        st1_position=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-219)            title='[ST1] Position'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-220)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-221)        st1_debt=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-222)            title='[ST1] Debt'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-223)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-224)        st1_locked_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-225)            title='[ST1] Locked Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-226)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-227)        st1_free_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-228)            title='[ST1] Free Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-229)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-230)        st1_val_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-231)            title='[ST1] Valuation Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-232)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-233)        st1_value=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-234)            title='[ST1] Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-235)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-236)        order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-237)            title='Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-238)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-239)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-240)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-4-241))
    

* * *

## Logs class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py#L201-L282 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-1)Logs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-5-9))
    

Extends [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords "vectorbtpro.generic.price_records.PriceRecords") for working with log records.

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



* * *

### col cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.col "Permanent link")

Mapped array of the field `col`.

* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.field_config "Permanent link")

Field config of [Logs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs "vectorbtpro.portfolio.logs.Logs").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-4)        ('group', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-5)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-6)        ('idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-7)        ('price_area_open', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-8)        ('price_area_high', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-9)        ('price_area_low', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-10)        ('price_area_close', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-11)        ('st0_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-12)        ('st0_position', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-13)        ('st0_debt', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-14)        ('st0_locked_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-15)        ('st0_free_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-16)        ('st0_val_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-17)        ('st0_value', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-18)        ('req_size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-19)        ('req_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-20)        ('req_size_type', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-21)        ('req_direction', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-22)        ('req_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-23)        ('req_fixed_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-24)        ('req_slippage', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-25)        ('req_min_size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-26)        ('req_max_size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-27)        ('req_size_granularity', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-28)        ('req_leverage', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-29)        ('req_leverage_mode', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-30)        ('req_reject_prob', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-31)        ('req_price_area_vio_mode', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-32)        ('req_allow_partial', 'bool'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-33)        ('req_raise_reject', 'bool'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-34)        ('req_log', 'bool'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-35)        ('res_size', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-36)        ('res_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-37)        ('res_fees', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-38)        ('res_side', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-39)        ('res_status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-40)        ('res_status_info', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-41)        ('st1_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-42)        ('st1_position', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-43)        ('st1_debt', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-44)        ('st1_locked_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-45)        ('st1_free_cash', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-46)        ('st1_val_price', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-47)        ('st1_value', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-48)        ('order_id', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-49)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-50)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-51)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-52)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-53)            title='Log Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-54)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-55)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-56)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-57)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-58)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-59)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-60)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-61)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-62)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-63)            name='idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-64)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-65)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-66)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-67)        group=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-68)            title='Group'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-69)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-70)        price_area_open=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-71)            title='[PA] Open'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-72)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-73)        price_area_high=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-74)            title='[PA] High'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-75)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-76)        price_area_low=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-77)            title='[PA] Low'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-78)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-79)        price_area_close=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-80)            title='[PA] Close'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-81)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-82)        st0_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-83)            title='[ST0] Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-84)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-85)        st0_position=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-86)            title='[ST0] Position'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-87)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-88)        st0_debt=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-89)            title='[ST0] Debt'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-90)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-91)        st0_locked_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-92)            title='[ST0] Locked Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-93)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-94)        st0_free_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-95)            title='[ST0] Free Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-96)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-97)        st0_val_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-98)            title='[ST0] Valuation Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-99)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-100)        st0_value=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-101)            title='[ST0] Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-102)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-103)        req_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-104)            title='[REQ] Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-105)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-106)        req_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-107)            title='[REQ] Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-108)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-109)        req_size_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-110)            title='[REQ] Size Type',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-111)            mapping=SizeTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-112)                Amount=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-113)                Value=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-114)                Percent=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-115)                Percent100=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-116)                ValuePercent=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-117)                ValuePercent100=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-118)                TargetAmount=6,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-119)                TargetValue=7,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-120)                TargetPercent=8,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-121)                TargetPercent100=9
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-122)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-123)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-124)        req_direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-125)            title='[REQ] Direction',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-126)            mapping=DirectionT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-127)                LongOnly=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-128)                ShortOnly=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-129)                Both=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-130)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-131)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-132)        req_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-133)            title='[REQ] Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-134)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-135)        req_fixed_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-136)            title='[REQ] Fixed Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-137)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-138)        req_slippage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-139)            title='[REQ] Slippage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-140)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-141)        req_min_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-142)            title='[REQ] Min Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-143)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-144)        req_max_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-145)            title='[REQ] Max Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-146)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-147)        req_size_granularity=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-148)            title='[REQ] Size Granularity'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-149)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-150)        req_leverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-151)            title='[REQ] Leverage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-152)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-153)        req_leverage_mode=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-154)            title='[REQ] Leverage Mode',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-155)            mapping=LeverageModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-156)                Lazy=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-157)                Eager=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-158)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-159)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-160)        req_reject_prob=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-161)            title='[REQ] Rejection Prob'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-162)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-163)        req_price_area_vio_mode=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-164)            title='[REQ] Price Area Violation Mode',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-165)            mapping=PriceAreaVioModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-166)                Ignore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-167)                Cap=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-168)                Error=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-169)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-170)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-171)        req_allow_partial=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-172)            title='[REQ] Allow Partial'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-173)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-174)        req_raise_reject=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-175)            title='[REQ] Raise Rejection'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-176)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-177)        req_log=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-178)            title='[REQ] Log'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-179)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-180)        res_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-181)            title='[RES] Size'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-182)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-183)        res_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-184)            title='[RES] Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-185)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-186)        res_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-187)            title='[RES] Fees'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-188)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-189)        res_side=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-190)            title='[RES] Side',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-191)            mapping=OrderSideT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-192)                Buy=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-193)                Sell=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-194)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-195)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-196)        res_status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-197)            title='[RES] Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-198)            mapping=OrderStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-199)                Filled=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-200)                Ignored=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-201)                Rejected=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-202)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-203)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-204)        res_status_info=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-205)            title='[RES] Status Info',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-206)            mapping=OrderStatusInfoT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-207)                SizeNaN=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-208)                PriceNaN=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-209)                ValPriceNaN=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-210)                ValueNaN=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-211)                ValueZeroNeg=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-212)                SizeZero=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-213)                NoCash=6,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-214)                NoOpenPosition=7,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-215)                MaxSizeExceeded=8,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-216)                RandomEvent=9,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-217)                CantCoverFees=10,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-218)                MinSizeNotReached=11,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-219)                PartialFill=12
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-220)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-221)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-222)        st1_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-223)            title='[ST1] Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-224)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-225)        st1_position=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-226)            title='[ST1] Position'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-227)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-228)        st1_debt=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-229)            title='[ST1] Debt'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-230)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-231)        st1_locked_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-232)            title='[ST1] Locked Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-233)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-234)        st1_free_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-235)            title='[ST1] Free Cash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-236)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-237)        st1_val_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-238)            title='[ST1] Valuation Price'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-239)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-240)        st1_value=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-241)            title='[ST1] Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-242)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-243)        order_id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-244)            title='Order Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-245)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-246)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-247)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-6-248))
    

Returns `Logs._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `Logs._field_config`.

* * *

### group cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.group "Permanent link")

Mapped array of the field `group`.

* * *

### id cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.id "Permanent link")

Mapped array of the field `id`.

* * *

### idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.idx "Permanent link")

Mapped array of the field `idx`.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.metrics "Permanent link")

Metrics supported by [Logs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs "vectorbtpro.portfolio.logs.Logs").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-4)        calc_func=<function Logs.<lambda> at 0x174d11260>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-10)        calc_func=<function Logs.<lambda> at 0x174d11300>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-16)        calc_func=<function Logs.<lambda> at 0x174d113a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-21)    total_records=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-22)        title='Total Records',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-23)        calc_func='count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-24)        tags='records'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-26)    res_status_counts=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-27)        title='Status Counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-28)        calc_func='res_status.value_counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-29)        incl_all_keys=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-30)        post_calc_func=<function Logs.<lambda> at 0x174d11440>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-31)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-32)            'logs',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-33)            'res_status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-34)            'value_counts'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-35)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-36)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-37)    res_status_info_counts=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-38)        title='Status Info Counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-39)        calc_func='res_status_info.value_counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-40)        post_calc_func=<function Logs.<lambda> at 0x174d114e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-41)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-42)            'logs',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-43)            'res_status_info',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-44)            'value_counts'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-45)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-46)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-7-47))
    

Returns `Logs._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `Logs._metrics`.

* * *

### order_id cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.order_id "Permanent link")

Mapped array of the field `order_id`.

* * *

### plots_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py#L268-L278 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.plots_defaults "Permanent link")

Defaults for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.portfolio.logs.Logs.plots").

Merges [PriceRecords.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.plots_defaults "vectorbtpro.generic.price_records.PriceRecords.plots_defaults") and `plots` from [logs](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.logs "vectorbtpro._settings.logs").

* * *

### price_area_close cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.price_area_close "Permanent link")

Mapped array of the field `price_area_close`.

* * *

### price_area_high cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.price_area_high "Permanent link")

Mapped array of the field `price_area_high`.

* * *

### price_area_low cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.price_area_low "Permanent link")

Mapped array of the field `price_area_low`.

* * *

### price_area_open cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.price_area_open "Permanent link")

Mapped array of the field `price_area_open`.

* * *

### req_allow_partial cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_allow_partial "Permanent link")

Mapped array of the field `req_allow_partial`.

* * *

### req_direction cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_direction "Permanent link")

Mapped array of the field `req_direction`.

* * *

### req_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_fees "Permanent link")

Mapped array of the field `req_fees`.

* * *

### req_fixed_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_fixed_fees "Permanent link")

Mapped array of the field `req_fixed_fees`.

* * *

### req_leverage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_leverage "Permanent link")

Mapped array of the field `req_leverage`.

* * *

### req_leverage_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_leverage_mode "Permanent link")

Mapped array of the field `req_leverage_mode`.

* * *

### req_log cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_log "Permanent link")

Mapped array of the field `req_log`.

* * *

### req_max_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_max_size "Permanent link")

Mapped array of the field `req_max_size`.

* * *

### req_min_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_min_size "Permanent link")

Mapped array of the field `req_min_size`.

* * *

### req_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_price "Permanent link")

Mapped array of the field `req_price`.

* * *

### req_price_area_vio_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_price_area_vio_mode "Permanent link")

Mapped array of the field `req_price_area_vio_mode`.

* * *

### req_raise_reject cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_raise_reject "Permanent link")

Mapped array of the field `req_raise_reject`.

* * *

### req_reject_prob cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_reject_prob "Permanent link")

Mapped array of the field `req_reject_prob`.

* * *

### req_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_size "Permanent link")

Mapped array of the field `req_size`.

* * *

### req_size_granularity cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_size_granularity "Permanent link")

Mapped array of the field `req_size_granularity`.

* * *

### req_size_type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_size_type "Permanent link")

Mapped array of the field `req_size_type`.

* * *

### req_slippage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.req_slippage "Permanent link")

Mapped array of the field `req_slippage`.

* * *

### res_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_fees "Permanent link")

Mapped array of the field `res_fees`.

* * *

### res_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_price "Permanent link")

Mapped array of the field `res_price`.

* * *

### res_side cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_side "Permanent link")

Mapped array of the field `res_side`.

* * *

### res_side_buy cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_side_buy "Permanent link")

Records filtered by `res_side == 0`.

* * *

### res_side_sell cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_side_sell "Permanent link")

Records filtered by `res_side == 1`.

* * *

### res_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_size "Permanent link")

Mapped array of the field `res_size`.

* * *

### res_status cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status "Permanent link")

Mapped array of the field `res_status`.

* * *

### res_status_filled cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_filled "Permanent link")

Records filtered by `res_status == 0`.

* * *

### res_status_ignored cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_ignored "Permanent link")

Records filtered by `res_status == 1`.

* * *

### res_status_info cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info "Permanent link")

Mapped array of the field `res_status_info`.

* * *

### res_status_info_cant_cover_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_cant_cover_fees "Permanent link")

Records filtered by `res_status_info == 10`.

* * *

### res_status_info_max_size_exceeded cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_max_size_exceeded "Permanent link")

Records filtered by `res_status_info == 8`.

* * *

### res_status_info_min_size_not_reached cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_min_size_not_reached "Permanent link")

Records filtered by `res_status_info == 11`.

* * *

### res_status_info_no_cash cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_no_cash "Permanent link")

Records filtered by `res_status_info == 6`.

* * *

### res_status_info_no_open_position cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_no_open_position "Permanent link")

Records filtered by `res_status_info == 7`.

* * *

### res_status_info_partial_fill cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_partial_fill "Permanent link")

Records filtered by `res_status_info == 12`.

* * *

### res_status_info_price_nan cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_price_nan "Permanent link")

Records filtered by `res_status_info == 1`.

* * *

### res_status_info_random_event cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_random_event "Permanent link")

Records filtered by `res_status_info == 9`.

* * *

### res_status_info_size_nan cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_size_nan "Permanent link")

Records filtered by `res_status_info == 0`.

* * *

### res_status_info_size_zero cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_size_zero "Permanent link")

Records filtered by `res_status_info == 5`.

* * *

### res_status_info_val_price_nan cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_val_price_nan "Permanent link")

Records filtered by `res_status_info == 2`.

* * *

### res_status_info_value_nan cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_value_nan "Permanent link")

Records filtered by `res_status_info == 3`.

* * *

### res_status_info_value_zero_neg cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_info_value_zero_neg "Permanent link")

Records filtered by `res_status_info == 4`.

* * *

### res_status_rejected cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.res_status_rejected "Permanent link")

Records filtered by `res_status == 2`.

* * *

### st0_cash cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st0_cash "Permanent link")

Mapped array of the field `st0_cash`.

* * *

### st0_debt cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st0_debt "Permanent link")

Mapped array of the field `st0_debt`.

* * *

### st0_free_cash cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st0_free_cash "Permanent link")

Mapped array of the field `st0_free_cash`.

* * *

### st0_locked_cash cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st0_locked_cash "Permanent link")

Mapped array of the field `st0_locked_cash`.

* * *

### st0_position cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st0_position "Permanent link")

Mapped array of the field `st0_position`.

* * *

### st0_val_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st0_val_price "Permanent link")

Mapped array of the field `st0_val_price`.

* * *

### st0_value cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st0_value "Permanent link")

Mapped array of the field `st0_value`.

* * *

### st1_cash cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st1_cash "Permanent link")

Mapped array of the field `st1_cash`.

* * *

### st1_debt cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st1_debt "Permanent link")

Mapped array of the field `st1_debt`.

* * *

### st1_free_cash cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st1_free_cash "Permanent link")

Mapped array of the field `st1_free_cash`.

* * *

### st1_locked_cash cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st1_locked_cash "Permanent link")

Mapped array of the field `st1_locked_cash`.

* * *

### st1_position cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st1_position "Permanent link")

Mapped array of the field `st1_position`.

* * *

### st1_val_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st1_val_price "Permanent link")

Mapped array of the field `st1_val_price`.

* * *

### st1_value cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.st1_value "Permanent link")

Mapped array of the field `st1_value`.

* * *

### stats_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py#L212-L222 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.stats_defaults "Permanent link")

Defaults for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.portfolio.logs.Logs.stats").

Merges [PriceRecords.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.stats_defaults "vectorbtpro.generic.price_records.PriceRecords.stats_defaults") and `stats` from [logs](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.logs "vectorbtpro._settings.logs").

* * *

### subplots property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/logs.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs.subplots "Permanent link")

Subplots supported by [Logs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs "vectorbtpro.portfolio.logs.Logs").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#__codelineno-8-1)HybridConfig()
    

Returns `Logs._subplots`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `Logs._subplots`.
