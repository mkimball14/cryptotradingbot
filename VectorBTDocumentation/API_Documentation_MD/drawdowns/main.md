drawdowns records

#  drawdowns module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns "Permanent link")

Base class for working with drawdown records.

Drawdown records capture information on drawdowns. Since drawdowns are ranges, they subclass [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").

Warning

[Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns") return both recovered AND active drawdowns, which may skew your performance results. To only consider recovered drawdowns, you should explicitly query `status_recovered` attribute.

Using [Drawdowns.from_price](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.from_price "vectorbtpro.generic.drawdowns.Drawdowns.from_price"), you can generate drawdown records for any time series and analyze them right away.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-0-3)>>> price = vbt.YFData.pull(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-0-4)...     "BTC-USD",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-0-5)...     start="2019-10 UTC",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-0-6)...     end="2020-01 UTC"
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-0-7)... ).get('Close')
    

100%
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-1)>>> price = price.rename(None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-3)>>> drawdowns = vbt.Drawdowns.from_price(price, wrapper_kwargs=dict(freq='d'))
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-5)>>> drawdowns.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-6)   Drawdown Id  Column               Start Index              Valley Index  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-7)0            0       0 2019-10-02 00:00:00+00:00 2019-10-06 00:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-8)1            1       0 2019-10-09 00:00:00+00:00 2019-10-24 00:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-9)2            2       0 2019-10-27 00:00:00+00:00 2019-12-17 00:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-11)                  End Index   Peak Value  Valley Value    End Value     Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-12)0 2019-10-09 00:00:00+00:00  8393.041992   7988.155762  8595.740234  Recovered
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-13)1 2019-10-25 00:00:00+00:00  8595.740234   7493.488770  8660.700195  Recovered
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-14)2 2019-12-31 00:00:00+00:00  9551.714844   6640.515137  7193.599121     Active
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-16)>>> drawdowns.duration.max(wrap_kwargs=dict(to_timedelta=True))
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-1-17)Timedelta('66 days 00:00:00')
    

## From accessors[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#from-accessors "Permanent link")

Moreover, all generic accessors have a property `drawdowns` and a method `get_drawdowns`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-2-1)>>> # vectorbtpro.generic.accessors.GenericAccessor.drawdowns.coverage
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-2-2)>>> price.vbt.drawdowns.coverage
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-2-3)0.967391304347826
    

## Stats[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#stats "Permanent link")

Hint

See [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats") and [Drawdowns.metrics](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.metrics "vectorbtpro.generic.drawdowns.Drawdowns.metrics").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-1)>>> df = pd.DataFrame({
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-2)...     'a': [1, 2, 1, 3, 2],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-3)...     'b': [2, 3, 1, 2, 1]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-4)... })
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-6)>>> drawdowns = df.vbt(freq='d').drawdowns
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-8)>>> drawdowns['a'].stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-9)Start                                        0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-10)End                                          4
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-11)Period                         5 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-12)Coverage [%]                              80.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-13)Total Records                                2
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-14)Total Recovered Drawdowns                    1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-15)Total Active Drawdowns                       1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-16)Active Drawdown [%]                  33.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-17)Active Duration                2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-18)Active Recovery [%]                        0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-19)Active Recovery Return [%]                 0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-20)Active Recovery Duration       0 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-21)Max Drawdown [%]                          50.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-22)Avg Drawdown [%]                          50.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-23)Max Drawdown Duration          2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-24)Avg Drawdown Duration          2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-25)Max Recovery Return [%]                  200.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-26)Avg Recovery Return [%]                  200.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-27)Max Recovery Duration          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-28)Avg Recovery Duration          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-29)Avg Recovery Duration Ratio                1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-3-30)Name: a, dtype: object
    

By default, the metrics `max_dd`, `avg_dd`, `max_dd_duration`, and `avg_dd_duration` do not include active drawdowns. To change that, pass `incl_active=True`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-1)>>> drawdowns['a'].stats(settings=dict(incl_active=True))
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-2)Start                                        0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-3)End                                          4
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-4)Period                         5 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-5)Coverage [%]                              80.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-6)Total Records                                2
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-7)Total Recovered Drawdowns                    1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-8)Total Active Drawdowns                       1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-9)Active Drawdown [%]                  33.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-10)Active Duration                2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-11)Active Recovery [%]                        0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-12)Active Recovery Return [%]                 0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-13)Active Recovery Duration       0 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-14)Max Drawdown [%]                          50.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-15)Avg Drawdown [%]                     41.666667
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-16)Max Drawdown Duration          2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-17)Avg Drawdown Duration          2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-18)Max Recovery Return [%]                  200.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-19)Avg Recovery Return [%]                  200.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-20)Max Recovery Duration          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-21)Avg Recovery Duration          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-22)Avg Recovery Duration Ratio                1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-4-23)Name: a, dtype: object
    

[StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.drawdowns.Drawdowns.stats") also supports (re-)grouping:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-1)>>> drawdowns['a'].stats(group_by=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-2)UserWarning: Metric 'active_dd' does not support grouped data
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-3)UserWarning: Metric 'active_duration' does not support grouped data
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-4)UserWarning: Metric 'active_recovery' does not support grouped data
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-5)UserWarning: Metric 'active_recovery_return' does not support grouped data
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-6)UserWarning: Metric 'active_recovery_duration' does not support grouped data
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-8)Start                                        0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-9)End                                          4
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-10)Period                         5 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-11)Coverage [%]                              80.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-12)Total Records                                2
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-13)Total Recovered Drawdowns                    1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-14)Total Active Drawdowns                       1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-15)Max Drawdown [%]                          50.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-16)Avg Drawdown [%]                          50.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-17)Max Drawdown Duration          2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-18)Avg Drawdown Duration          2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-19)Max Recovery Return [%]                  200.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-20)Avg Recovery Return [%]                  200.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-21)Max Recovery Duration          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-22)Avg Recovery Duration          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-23)Avg Recovery Duration Ratio                1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-5-24)Name: group, dtype: object
    

## Plots[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#plots "Permanent link")

Hint

See [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots") and [Drawdowns.subplots](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.subplots "vectorbtpro.generic.drawdowns.Drawdowns.subplots").

[Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns") class has a single subplot based on [Drawdowns.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.plot "vectorbtpro.generic.drawdowns.Drawdowns.plot"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-6-1)>>> drawdowns['a'].plots().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/drawdowns_plots.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/drawdowns_plots.dark.svg#only-dark)

* * *

## dd_attach_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.dd_attach_field_config "Permanent link")

Config of fields to be attached to [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-7-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-7-2)    status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-7-3)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-7-4)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-7-5))
    

* * *

## dd_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.dd_field_config "Permanent link")

Field config for [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-5)        ('start_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-6)        ('valley_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-7)        ('end_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-8)        ('start_val', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-9)        ('valley_val', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-10)        ('end_val', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-11)        ('status', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-12)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-13)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-14)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-15)            title='Drawdown Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-16)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-17)        valley_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-18)            title='Valley Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-19)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-20)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-21)        start_val=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-22)            title='Start Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-23)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-24)        valley_val=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-25)            title='Valley Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-26)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-27)        end_val=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-28)            title='End Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-29)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-30)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-31)            mapping=DrawdownStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-32)                Active=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-33)                Recovered=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-34)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-35)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-36)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-8-37))
    

* * *

## dd_shortcut_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.dd_shortcut_config "Permanent link")

Config of shortcut properties to be attached to [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-2)    ranges=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-3)    decline_ranges=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-4)    recovery_ranges=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-5)    drawdown=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-6)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-8)    avg_drawdown=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-9)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-10)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-11)    max_drawdown=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-12)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-14)    recovery_return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-15)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-16)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-17)    avg_recovery_return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-18)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-19)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-20)    max_recovery_return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-21)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-22)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-23)    decline_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-24)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-26)    recovery_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-27)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-28)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-29)    recovery_duration_ratio=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-30)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-31)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-32)    active_drawdown=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-33)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-35)    active_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-36)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-37)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-38)    active_recovery=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-39)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-40)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-41)    active_recovery_return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-42)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-43)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-44)    active_recovery_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-45)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-46)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-9-47))
    

* * *

## Drawdowns class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L275-L1183 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-1)Drawdowns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-10-9))
    

Extends [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for working with drawdown records.

Requires `records_arr` to have all fields defined in [drawdown_dt](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.drawdown_dt "vectorbtpro.generic.enums.drawdown_dt").

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



* * *

### active_drawdown cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.active_drawdown "Permanent link")

[Drawdowns.get_active_drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_drawdown "vectorbtpro.generic.drawdowns.Drawdowns.get_active_drawdown") with default arguments.

* * *

### active_duration cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.active_duration "Permanent link")

[Drawdowns.get_active_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_duration "vectorbtpro.generic.drawdowns.Drawdowns.get_active_duration") with default arguments.

* * *

### active_recovery cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.active_recovery "Permanent link")

[Drawdowns.get_active_recovery](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery "vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery") with default arguments.

* * *

### active_recovery_duration cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.active_recovery_duration "Permanent link")

[Drawdowns.get_active_recovery_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery_duration "vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery_duration") with default arguments.

* * *

### active_recovery_return cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.active_recovery_return "Permanent link")

[Drawdowns.get_active_recovery_return](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery_return "vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery_return") with default arguments.

* * *

### avg_drawdown cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.avg_drawdown "Permanent link")

[Drawdowns.get_avg_drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_avg_drawdown "vectorbtpro.generic.drawdowns.Drawdowns.get_avg_drawdown") with default arguments.

* * *

### avg_recovery_return cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.avg_recovery_return "Permanent link")

[Drawdowns.get_avg_recovery_return](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_avg_recovery_return "vectorbtpro.generic.drawdowns.Drawdowns.get_avg_recovery_return") with default arguments.

* * *

### decline_duration cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.decline_duration "Permanent link")

[Drawdowns.get_decline_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_decline_duration "vectorbtpro.generic.drawdowns.Drawdowns.get_decline_duration") with default arguments.

* * *

### decline_ranges cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.decline_ranges "Permanent link")

[Drawdowns.get_decline_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_decline_ranges "vectorbtpro.generic.drawdowns.Drawdowns.get_decline_ranges") with default arguments.

* * *

### drawdown cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.drawdown "Permanent link")

[Drawdowns.get_drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_drawdown "vectorbtpro.generic.drawdowns.Drawdowns.get_drawdown") with default arguments.

* * *

### end_val cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.end_val "Permanent link")

Mapped array of the field `end_val`.

* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.field_config "Permanent link")

Field config of [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-5)        ('start_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-6)        ('valley_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-7)        ('end_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-8)        ('start_val', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-9)        ('valley_val', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-10)        ('end_val', 'float64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-11)        ('status', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-12)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-13)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-14)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-15)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-16)            title='Drawdown Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-17)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-18)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-19)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-20)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-21)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-22)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-23)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-24)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-25)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-26)            name='end_idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-27)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-28)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-29)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-30)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-31)            title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-32)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-33)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-34)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-35)            title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-36)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-37)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-38)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-39)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-40)            mapping=DrawdownStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-41)                Active=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-42)                Recovered=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-43)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-44)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-45)        valley_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-46)            title='Valley Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-47)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-48)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-49)        start_val=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-50)            title='Start Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-51)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-52)        valley_val=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-53)            title='Valley Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-54)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-55)        end_val=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-56)            title='End Value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-57)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-58)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-11-59))
    

Returns `Drawdowns._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `Drawdowns._field_config`.

* * *

### from_price class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L287-L337 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.from_price "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-1)Drawdowns.from_price(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-2)    close,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-3)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-7)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-8)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-9)    attach_data=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-10)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-11)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-12)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-13)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-14)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-12-15))
    

Build [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns") from price.

`**kwargs` will be passed to [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns").

* * *

### get_active_drawdown method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L540-L557 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_drawdown "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-13-1)Drawdowns.get_active_drawdown(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-13-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-13-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-13-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-13-5)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-13-6))
    

Get drawdown of the last active drawdown only.

Does not support grouping.

* * *

### get_active_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L559-L580 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-14-1)Drawdowns.get_active_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-14-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-14-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-14-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-14-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-14-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-14-7))
    

Get duration of the last active drawdown only.

Does not support grouping.

* * *

### get_active_recovery method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L582-L600 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-15-1)Drawdowns.get_active_recovery(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-15-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-15-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-15-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-15-5)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-15-6))
    

Get recovery of the last active drawdown only.

Does not support grouping.

* * *

### get_active_recovery_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L625-L646 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-16-1)Drawdowns.get_active_recovery_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-16-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-16-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-16-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-16-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-16-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-16-7))
    

Get recovery duration of the last active drawdown only.

Does not support grouping.

* * *

### get_active_recovery_return method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L602-L623 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_active_recovery_return "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-17-1)Drawdowns.get_active_recovery_return(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-17-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-17-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-17-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-17-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-17-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-17-7))
    

Get recovery return of the last active drawdown only.

Does not support grouping.

* * *

### get_avg_drawdown method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L404-L416 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_avg_drawdown "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-18-1)Drawdowns.get_avg_drawdown(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-18-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-18-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-18-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-18-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-18-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-18-7))
    

Get average drawdown (ADD).

Based on [Drawdowns.drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.drawdown "vectorbtpro.generic.drawdowns.Drawdowns.drawdown").

* * *

### get_avg_recovery_return method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L448-L466 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_avg_recovery_return "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-19-1)Drawdowns.get_avg_recovery_return(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-19-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-19-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-19-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-19-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-19-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-19-7))
    

Get average recovery return.

Based on [Drawdowns.recovery_return](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.recovery_return "vectorbtpro.generic.drawdowns.Drawdowns.recovery_return").

* * *

### get_decline_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L490-L502 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_decline_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-20-1)Drawdowns.get_decline_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-20-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-20-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-20-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-20-5))
    

See [dd_decline_duration_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.dd_decline_duration_nb "vectorbtpro.generic.nb.records.dd_decline_duration_nb").

Takes into account both recovered and active drawdowns.

* * *

### get_decline_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L357-L373 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_decline_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-21-1)Drawdowns.get_decline_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-21-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-21-3))
    

Get records of type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for peak-to-valley ranges.

* * *

### get_drawdown method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L395-L402 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_drawdown "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-22-1)Drawdowns.get_drawdown(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-22-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-22-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-22-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-22-5))
    

See [dd_drawdown_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.dd_drawdown_nb "vectorbtpro.generic.nb.records.dd_drawdown_nb").

Takes into account both recovered and active drawdowns.

* * *

### get_max_drawdown method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L418-L430 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_max_drawdown "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-23-1)Drawdowns.get_max_drawdown(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-23-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-23-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-23-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-23-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-23-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-23-7))
    

Get maximum drawdown (MDD).

Based on [Drawdowns.drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.drawdown "vectorbtpro.generic.drawdowns.Drawdowns.drawdown").

* * *

### get_max_recovery_return method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L468-L486 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_max_recovery_return "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-24-1)Drawdowns.get_max_recovery_return(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-24-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-24-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-24-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-24-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-24-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-24-7))
    

Get maximum recovery return.

Based on [Drawdowns.recovery_return](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.recovery_return "vectorbtpro.generic.drawdowns.Drawdowns.recovery_return").

* * *

### get_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L339-L355 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-25-1)Drawdowns.get_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-25-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-25-3))
    

Get records of type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for peak-to-end ranges.

* * *

### get_recovery_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L504-L518 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-26-1)Drawdowns.get_recovery_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-26-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-26-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-26-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-26-5))
    

See [dd_recovery_duration_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.dd_recovery_duration_nb "vectorbtpro.generic.nb.records.dd_recovery_duration_nb").

A value higher than 1 means the recovery was slower than the decline.

Takes into account both recovered and active drawdowns.

* * *

### get_recovery_duration_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L520-L536 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_duration_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-27-1)Drawdowns.get_recovery_duration_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-27-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-27-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-27-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-27-5))
    

See [dd_recovery_duration_ratio_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.dd_recovery_duration_ratio_nb "vectorbtpro.generic.nb.records.dd_recovery_duration_ratio_nb").

Takes into account both recovered and active drawdowns.

* * *

### get_recovery_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L375-L391 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-28-1)Drawdowns.get_recovery_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-28-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-28-3))
    

Get records of type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for valley-to-end ranges.

* * *

### get_recovery_return method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L434-L446 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_return "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-29-1)Drawdowns.get_recovery_return(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-29-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-29-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-29-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-29-5))
    

See [dd_recovery_return_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.dd_recovery_return_nb "vectorbtpro.generic.nb.records.dd_recovery_return_nb").

Takes into account both recovered and active drawdowns.

* * *

### max_drawdown cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.max_drawdown "Permanent link")

[Drawdowns.get_max_drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_max_drawdown "vectorbtpro.generic.drawdowns.Drawdowns.get_max_drawdown") with default arguments.

* * *

### max_recovery_return cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.max_recovery_return "Permanent link")

[Drawdowns.get_max_recovery_return](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_max_recovery_return "vectorbtpro.generic.drawdowns.Drawdowns.get_max_recovery_return") with default arguments.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.metrics "Permanent link")

Metrics supported by [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-4)        calc_func=<function Drawdowns.<lambda> at 0x11e2a7240>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-10)        calc_func=<function Drawdowns.<lambda> at 0x11e2a72e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-16)        calc_func=<function Drawdowns.<lambda> at 0x11e2a7380>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-21)    coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-22)        title='Coverage [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-23)        calc_func='coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-24)        post_calc_func=<function Drawdowns.<lambda> at 0x11e2a7420>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-25)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-26)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-27)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-28)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-29)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-30)    total_records=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-31)        title='Total Records',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-32)        calc_func='count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-33)        tags='records'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-35)    total_recovered=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-36)        title='Total Recovered Drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-37)        calc_func='status_recovered.count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-38)        tags='drawdowns'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-39)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-40)    total_active=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-41)        title='Total Active Drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-42)        calc_func='status_active.count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-43)        tags='drawdowns'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-44)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-45)    active_dd=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-46)        title='Active Drawdown [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-47)        calc_func='active_drawdown',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-48)        post_calc_func=<function Drawdowns.<lambda> at 0x11e2a74c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-49)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-50)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-51)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-52)            'active'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-53)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-54)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-55)    active_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-56)        title='Active Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-57)        calc_func='active_duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-58)        fill_wrap_kwargs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-59)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-60)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-61)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-62)            'active',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-63)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-64)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-65)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-66)    active_recovery=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-67)        title='Active Recovery [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-68)        calc_func='active_recovery',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-69)        post_calc_func=<function Drawdowns.<lambda> at 0x11e2a7560>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-70)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-71)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-72)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-73)            'active'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-74)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-75)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-76)    active_recovery_return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-77)        title='Active Recovery Return [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-78)        calc_func='active_recovery_return',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-79)        post_calc_func=<function Drawdowns.<lambda> at 0x11e2a7600>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-80)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-81)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-82)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-83)            'active'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-84)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-85)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-86)    active_recovery_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-87)        title='Active Recovery Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-88)        calc_func='active_recovery_duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-89)        fill_wrap_kwargs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-90)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-91)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-92)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-93)            'active',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-94)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-95)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-96)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-97)    max_dd=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-98)        title='Max Drawdown [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-99)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-100)            template="'max_drawdown' if incl_active else 'status_recovered.get_max_drawdown'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-101)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-102)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-103)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-104)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-105)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-106)        post_calc_func=<function Drawdowns.<lambda> at 0x11e2a76a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-107)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-108)            template="['drawdowns'] if incl_active else ['drawdowns', 'recovered']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-109)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-110)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-111)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-112)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-113)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-114)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-115)    avg_dd=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-116)        title='Avg Drawdown [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-117)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-118)            template="'avg_drawdown' if incl_active else 'status_recovered.get_avg_drawdown'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-119)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-120)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-121)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-122)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-123)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-124)        post_calc_func=<function Drawdowns.<lambda> at 0x11e2a7740>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-125)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-126)            template="['drawdowns'] if incl_active else ['drawdowns', 'recovered']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-127)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-128)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-129)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-130)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-131)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-132)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-133)    max_dd_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-134)        title='Max Drawdown Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-135)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-136)            template="'max_duration' if incl_active else 'status_recovered.get_max_duration'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-137)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-138)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-139)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-140)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-141)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-142)        fill_wrap_kwargs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-143)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-144)            template="['drawdowns', 'duration'] if incl_active else ['drawdowns', 'recovered', 'duration']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-145)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-146)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-147)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-148)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-149)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-150)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-151)    avg_dd_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-152)        title='Avg Drawdown Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-153)        calc_func=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-154)            template="'avg_duration' if incl_active else 'status_recovered.get_avg_duration'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-155)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-156)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-157)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-158)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-159)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-160)        fill_wrap_kwargs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-161)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-162)            template="['drawdowns', 'duration'] if incl_active else ['drawdowns', 'recovered', 'duration']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-163)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-164)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-165)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-166)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-167)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-168)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-169)    max_return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-170)        title='Max Recovery Return [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-171)        calc_func='status_recovered.recovery_return.max',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-172)        post_calc_func=<function Drawdowns.<lambda> at 0x11e2a77e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-173)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-174)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-175)            'recovered'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-176)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-177)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-178)    avg_return=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-179)        title='Avg Recovery Return [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-180)        calc_func='status_recovered.recovery_return.mean',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-181)        post_calc_func=<function Drawdowns.<lambda> at 0x11e2a7880>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-182)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-183)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-184)            'recovered'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-185)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-186)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-187)    max_recovery_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-188)        title='Max Recovery Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-189)        calc_func='status_recovered.recovery_duration.max',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-190)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-191)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-192)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-193)            'recovered',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-194)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-195)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-196)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-197)    avg_recovery_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-198)        title='Avg Recovery Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-199)        calc_func='status_recovered.recovery_duration.mean',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-200)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-201)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-202)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-203)            'recovered',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-204)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-205)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-206)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-207)    recovery_duration_ratio=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-208)        title='Avg Recovery Duration Ratio',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-209)        calc_func='status_recovered.recovery_duration_ratio.mean',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-210)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-211)            'drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-212)            'recovered'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-213)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-214)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-30-215))
    

Returns `Drawdowns._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `Drawdowns._metrics`.

* * *

### plot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L793-L1156 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.plot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-1)Drawdowns.plot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-3)    top_n=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-4)    plot_ohlc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-5)    plot_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-6)    plot_markers=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-7)    plot_zones=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-8)    ohlc_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-9)    ohlc_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-10)    close_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-11)    peak_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-12)    valley_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-13)    recovery_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-14)    active_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-15)    decline_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-16)    recovery_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-17)    active_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-18)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-19)    xref='x',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-20)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-21)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-22)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-31-23))
    

Plot drawdowns.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`top_n`** : `int`
    Filter top N drawdown records by maximum drawdown.
**`plot_ohlc`** : `bool`
    Whether to plot OHLC.
**`plot_close`** : `bool`
    Whether to plot close.
**`plot_markers`** : `bool`
    Whether to plot markers.
**`plot_zones`** : `bool`
    Whether to plot zones.
**`ohlc_type`**
    

Either 'OHLC', 'Candlestick' or Plotly trace.

Pass None to use the default.

**`ohlc_trace_kwargs`** : `dict`
    Keyword arguments passed to `ohlc_type`.
**`close_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Drawdowns.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.generic.drawdowns.Drawdowns.close").
**`peak_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for peak values.
**`valley_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for valley values.
**`recovery_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for recovery values.
**`active_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for active recovery values.
**`decline_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for decline zones.
**`recovery_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for recovery zones.
**`active_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for active recovery zones.
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
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-32-1)>>> index = pd.date_range("2020", periods=8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-32-2)>>> price = pd.Series([1, 2, 1, 2, 3, 2, 1, 2], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-32-3)>>> vbt.Drawdowns.from_price(price, wrapper_kwargs=dict(freq='1 day')).plot().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/drawdowns_plot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/drawdowns_plot.dark.svg#only-dark)

* * *

### plots_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L1158-L1168 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.plots_defaults "Permanent link")

Defaults for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.drawdowns.Drawdowns.plots").

Merges [Ranges.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plots_defaults "vectorbtpro.generic.ranges.Ranges.plots_defaults") and `plots` from [drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.drawdowns "vectorbtpro._settings.drawdowns").

* * *

### ranges cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.ranges "Permanent link")

[Drawdowns.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_ranges "vectorbtpro.generic.drawdowns.Drawdowns.get_ranges") with default arguments.

* * *

### recovery_duration cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.recovery_duration "Permanent link")

[Drawdowns.get_recovery_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_duration "vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_duration") with default arguments.

* * *

### recovery_duration_ratio cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.recovery_duration_ratio "Permanent link")

[Drawdowns.get_recovery_duration_ratio](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_duration_ratio "vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_duration_ratio") with default arguments.

* * *

### recovery_ranges cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.recovery_ranges "Permanent link")

[Drawdowns.get_recovery_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_ranges "vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_ranges") with default arguments.

* * *

### recovery_return cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.recovery_return "Permanent link")

[Drawdowns.get_recovery_return](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_return "vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_return") with default arguments.

* * *

### start_val cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.start_val "Permanent link")

Mapped array of the field `start_val`.

* * *

### stats_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py#L650-L660 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.stats_defaults "Permanent link")

Defaults for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.drawdowns.Drawdowns.stats").

Merges [Ranges.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.stats_defaults "vectorbtpro.generic.ranges.Ranges.stats_defaults") and `stats` from [drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.drawdowns "vectorbtpro._settings.drawdowns").

* * *

### status_active cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.status_active "Permanent link")

Records filtered by `status == 0`.

* * *

### status_recovered cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.status_recovered "Permanent link")

Records filtered by `status == 1`.

* * *

### subplots property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.subplots "Permanent link")

Subplots supported by [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-33-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-33-2)    plot=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-33-3)        title='Drawdowns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-33-4)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-33-5)        plot_func='plot',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-33-6)        tags='drawdowns'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-33-7)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#__codelineno-33-8))
    

Returns `Drawdowns._subplots`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `Drawdowns._subplots`.

* * *

### valley_idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.valley_idx "Permanent link")

Mapped array of the field `valley_idx`.

* * *

### valley_val cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/drawdowns.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.valley_val "Permanent link")

Mapped array of the field `valley_val`.
