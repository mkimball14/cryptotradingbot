ranges records

#  ranges module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges "Permanent link")

Base class for working with range records.

Range records capture information on ranges. They are useful for analyzing duration of processes, such as drawdowns, trades, and positions. They also come in handy when analyzing distance between events, such as entry and exit signals.

Each range has a starting point and an ending point. For example, the points for `range(20)` are 0 and 20 (not 19!) respectively.

Note

Be aware that if a range hasn't ended in a column, its `end_idx` will point at the latest index. Make sure to account for this when computing custom metrics involving duration.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-0-3)>>> start = '2019-01-01 UTC'  # crypto is in UTC
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-0-4)>>> end = '2020-01-01 UTC'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-0-5)>>> price = vbt.YFData.pull('BTC-USD', start=start, end=end).get('Close')
    

100%
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-1)>>> fast_ma = vbt.MA.run(price, 10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-2)>>> slow_ma = vbt.MA.run(price, 50)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-3)>>> fast_below_slow = fast_ma.ma_above(slow_ma)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-5)>>> ranges = vbt.Ranges.from_array(fast_below_slow, wrapper_kwargs=dict(freq='d'))
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-7)>>> ranges.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-8)   Range Id  Column           Start Timestamp             End Timestamp  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-9)0         0       0 2019-02-19 00:00:00+00:00 2019-07-25 00:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-10)1         1       0 2019-08-08 00:00:00+00:00 2019-08-19 00:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-11)2         2       0 2019-11-01 00:00:00+00:00 2019-11-20 00:00:00+00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-13)   Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-14)0  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-15)1  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-16)2  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-17)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-18)>>> ranges.duration.max(wrap_kwargs=dict(to_timedelta=True))
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-1-19)Timedelta('156 days 00:00:00')
    

## From accessors[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#from-accessors "Permanent link")

Moreover, all generic accessors have a property `ranges` and a method `get_ranges`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-2-1)>>> # vectorbtpro.generic.accessors.GenericAccessor.ranges.coverage
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-2-2)>>> fast_below_slow.vbt.ranges.coverage
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-2-3)0.5081967213114754
    

## Stats[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#stats "Permanent link")

Hint

See [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats") and [Ranges.metrics](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.metrics "vectorbtpro.generic.ranges.Ranges.metrics").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-1)>>> df = pd.DataFrame({
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-2)...     'a': [1, 2, np.nan, np.nan, 5, 6],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-3)...     'b': [np.nan, 2, np.nan, 4, np.nan, 6]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-4)... })
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-5)>>> ranges = df.vbt(freq='d').ranges
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-7)>>> ranges['a'].stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-8)Start                             0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-9)End                               5
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-10)Period              6 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-11)Total Records                     2
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-12)Coverage                   0.666667
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-13)Overlap Coverage                0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-14)Duration: Min       2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-15)Duration: Median    2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-16)Duration: Max       2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-3-17)Name: a, dtype: object
    

[StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.ranges.Ranges.stats") also supports (re-)grouping:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-1)>>> ranges.stats(group_by=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-2)Start                                       0
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-3)End                                         5
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-4)Period                        6 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-5)Total Records                               5
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-6)Coverage                             0.416667
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-7)Overlap Coverage                          0.4
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-8)Duration: Min                 1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-9)Duration: Median              1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-10)Duration: Max                 2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-4-11)Name: group, dtype: object
    

## Plots[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#plots "Permanent link")

Hint

See [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots") and [Ranges.subplots](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.subplots "vectorbtpro.generic.ranges.Ranges.subplots").

[Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") class has a single subplot based on [Ranges.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot "vectorbtpro.generic.ranges.Ranges.plot"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-5-1)>>> ranges['a'].plots().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/ranges_plots.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/ranges_plots.dark.svg#only-dark)

* * *

## pattern_ranges_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.pattern_ranges_field_config "Permanent link")

Field config for [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-5)        ('start_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-6)        ('end_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-7)        ('status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-8)        ('similarity', 'float64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-9)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-10)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-11)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-12)            title='Pattern Range Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-13)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-14)        similarity=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-15)            title='Similarity'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-16)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-17)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-6-18))
    

* * *

## ranges_attach_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.ranges_attach_field_config "Permanent link")

Config of fields to be attached to [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-7-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-7-2)    status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-7-3)        attach_filters=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-7-4)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-7-5))
    

* * *

## ranges_field_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.ranges_field_config "Permanent link")

Field config for [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-5)        ('start_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-6)        ('end_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-7)        ('status', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-8)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-9)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-10)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-11)            title='Range Id'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-12)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-13)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-14)            name='end_idx'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-15)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-16)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-17)            title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-18)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-19)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-20)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-21)            title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-22)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-23)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-24)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-25)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-26)            mapping=RangeStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-27)                Open=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-28)                Closed=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-29)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-30)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-31)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-8-32))
    

* * *

## ranges_shortcut_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.ranges_shortcut_config "Permanent link")

Config of shortcut properties to be attached to [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-2)    valid=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-3)    invalid=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-4)    first_pd_mask=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-5)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-6)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-7)    last_pd_mask=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-8)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-9)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-10)    ranges_pd_mask=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-11)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-12)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-13)    first_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-14)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-15)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-16)    last_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-17)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-18)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-19)    duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-20)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-21)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-22)    real_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-23)        obj_type='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-24)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-25)    avg_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-26)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-27)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-28)    max_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-29)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-30)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-31)    coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-32)        obj_type='red_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-33)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-34)    overlap_coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-35)        method_name='get_coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-36)        obj_type='red_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-37)        method_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-38)            overlapping=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-39)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-40)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-41)    projections=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-42)        obj_type='array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-43)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-9-44))
    

* * *

## PSC class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1547-L1685 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-10-1)PSC(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-10-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-10-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-10-4))
    

Class that represents a pattern search config.

Every field will be resolved into the format suitable for Numba.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.attr_.DefineMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.attr_.DefineMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.attr_.DefineMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.attr_.DefineMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.attr_.DefineMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.attr_.DefineMixin.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.attr_.DefineMixin.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing")
  * [DefineMixin.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.attr_.DefineMixin.fields")
  * [DefineMixin.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.attr_.DefineMixin.fields_dict")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.attr_.DefineMixin.get_field")
  * [DefineMixin.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.attr_.DefineMixin.hash")
  * [DefineMixin.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.attr_.DefineMixin.hash_key")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.attr_.DefineMixin.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.attr_.DefineMixin.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.attr_.DefineMixin.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.attr_.DefineMixin.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.attr_.DefineMixin.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.attr_.DefineMixin.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.attr_.DefineMixin.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### distance_measure field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.distance_measure "Permanent link")

Distance measure. See [DistanceMeasure](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.DistanceMeasure "vectorbtpro.generic.enums.DistanceMeasure").

* * *

### error_type field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.error_type "Permanent link")

Error type. See [ErrorType](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.ErrorType "vectorbtpro.generic.enums.ErrorType").

* * *

### interp_mode field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.interp_mode "Permanent link")

Interpolation mode. See [InterpMode](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.InterpMode "vectorbtpro.generic.enums.InterpMode").

* * *

### invert field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.invert "Permanent link")

Whether to invert the pattern vertically.

* * *

### max_error field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error "Permanent link")

Maximum error at each point. Can be provided as a flexible array.

If `max_error` is an array, it must be of the same size as the pattern array. It also should be provided within the same scale as the pattern.

* * *

### max_error_as_maxdist field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error_as_maxdist "Permanent link")

Whether [PSC.max_error](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error "vectorbtpro.generic.ranges.PSC.max_error") should be used as the maximum distance at each point.

If False, crossing [PSC.max_error](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error "vectorbtpro.generic.ranges.PSC.max_error") will set the distance to the maximum distance based on [PSC.pmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pmin "vectorbtpro.generic.ranges.PSC.pmin"), [PSC.pmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pmax "vectorbtpro.generic.ranges.PSC.pmax"), and the pattern value at that point.

If True and any of the points in a window is `np.nan`, the point will be skipped.

* * *

### max_error_interp_mode field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error_interp_mode "Permanent link")

Interpolation mode for [PSC.max_error](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error "vectorbtpro.generic.ranges.PSC.max_error"). See [InterpMode](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.InterpMode "vectorbtpro.generic.enums.InterpMode").

If None, defaults to [PSC.interp_mode](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.interp_mode "vectorbtpro.generic.ranges.PSC.interp_mode").

* * *

### max_error_strict field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error_strict "Permanent link")

Whether crossing [PSC.max_error](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error "vectorbtpro.generic.ranges.PSC.max_error") even once should yield the similarity of `np.nan`.

* * *

### max_pct_change field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_pct_change "Permanent link")

Maximum percentage change of the window to stay a candidate for search.

If any window crosses this mark, its similarity becomes `np.nan`.

* * *

### max_records field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_records "Permanent link")

Maximum number of records expected to be filled.

Set to avoid creating empty arrays larger than needed.

* * *

### max_window field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_window "Permanent link")

Maximum window (including).

* * *

### min_pct_change field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.min_pct_change "Permanent link")

Minimum percentage change of the window to stay a candidate for search.

If any window doesn't cross this mark, its similarity becomes `np.nan`.

* * *

### min_similarity field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.min_similarity "Permanent link")

Minimum similarity.

If any window doesn't cross this mark, its similarity becomes `np.nan`.

* * *

### minp field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.minp "Permanent link")

Minimum number of observations in price window required to have a value.

* * *

### name field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.name "Permanent link")

Name of the config.

* * *

### overlap_mode field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.overlap_mode "Permanent link")

Overlapping mode. See [OverlapMode](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.OverlapMode "vectorbtpro.generic.enums.OverlapMode").

* * *

### pattern field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pattern "Permanent link")

Flexible pattern array.

Can be smaller or bigger than the source array; in such a case, the values of the smaller array will be "stretched" by interpolation of the type in [PSC.interp_mode](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.interp_mode "vectorbtpro.generic.ranges.PSC.interp_mode").

* * *

### pmax field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pmax "Permanent link")

Value to be considered as the maximum of [PSC.pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pattern "vectorbtpro.generic.ranges.PSC.pattern").

Used in rescaling using `RescaleMode.MinMax` and calculating the maximum distance at each point if [PSC.max_error_as_maxdist](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error_as_maxdist "vectorbtpro.generic.ranges.PSC.max_error_as_maxdist") is disabled.

If `np.nan`, gets calculated dynamically.

* * *

### pmin field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pmin "Permanent link")

Value to be considered as the minimum of [PSC.pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pattern "vectorbtpro.generic.ranges.PSC.pattern").

Used in rescaling using `RescaleMode.MinMax` and calculating the maximum distance at each point if [PSC.max_error_as_maxdist](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error_as_maxdist "vectorbtpro.generic.ranges.PSC.max_error_as_maxdist") is disabled.

If `np.nan`, gets calculated dynamically.

* * *

### rescale_mode field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.rescale_mode "Permanent link")

Rescaling mode. See [RescaleMode](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.RescaleMode "vectorbtpro.generic.enums.RescaleMode").

* * *

### roll_forward field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.roll_forward "Permanent link")

Whether to roll windows to the left of the current row, otherwise to the right.

* * *

### row_select_prob field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.row_select_prob "Permanent link")

Row selection probability.

* * *

### vmax field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.vmax "Permanent link")

Maximum value of any window. Should only be used when the array has fixed bounds.

Used in rescaling using `RescaleMode.MinMax` and checking against [PSC.min_pct_change](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.min_pct_change "vectorbtpro.generic.ranges.PSC.min_pct_change") and [PSC.max_pct_change](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_pct_change "vectorbtpro.generic.ranges.PSC.max_pct_change").

If `np.nan`, gets calculated dynamically.

* * *

### vmin field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.vmin "Permanent link")

Minimum value of any window. Should only be used when the array has fixed bounds.

Used in rescaling using `RescaleMode.MinMax` and checking against [PSC.min_pct_change](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.min_pct_change "vectorbtpro.generic.ranges.PSC.min_pct_change") and [PSC.max_pct_change](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_pct_change "vectorbtpro.generic.ranges.PSC.max_pct_change").

If `np.nan`, gets calculated dynamically.

* * *

### window field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.window "Permanent link")

Minimum window.

Defaults to the length of [PSC.pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pattern "vectorbtpro.generic.ranges.PSC.pattern").

* * *

### window_select_prob field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.window_select_prob "Permanent link")

Window selection probability.

* * *

## PatternRanges class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1709-L2258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-11-1)PatternRanges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-11-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-11-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-11-4)    search_configs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-11-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-11-6))
    

Extends [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") for working with range records generated from pattern search.

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
  * [PriceRecords.indexing_func_meta](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.indexing_func_meta "vectorbtpro.generic.ranges.Ranges.indexing_func_meta")
  * [PriceRecords.resample](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.resample "vectorbtpro.generic.ranges.Ranges.resample")
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
  * [Ranges.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plots_defaults "vectorbtpro.generic.ranges.Ranges.plots_defaults")
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
  * [Ranges.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.stats_defaults "vectorbtpro.generic.ranges.Ranges.stats_defaults")
  * [Ranges.status](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status "vectorbtpro.generic.ranges.Ranges.status")
  * [Ranges.status_closed](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_closed "vectorbtpro.generic.ranges.Ranges.status_closed")
  * [Ranges.status_open](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_open "vectorbtpro.generic.ranges.Ranges.status_open")
  * [Ranges.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.generic.ranges.Ranges.unwrapped")
  * [Ranges.valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.valid "vectorbtpro.generic.ranges.Ranges.valid")
  * [Ranges.values](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.values "vectorbtpro.generic.ranges.Ranges.values")
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

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.field_config "Permanent link")

Field config of [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-5)        ('start_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-6)        ('end_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-7)        ('status', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-8)        ('similarity', 'float64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-9)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-10)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-11)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-12)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-13)            title='Pattern Range Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-14)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-15)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-16)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-17)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-18)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-19)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-20)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-21)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-22)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-23)            name='end_idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-24)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-25)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-26)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-27)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-28)            title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-29)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-30)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-31)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-32)            title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-33)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-34)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-35)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-36)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-37)            mapping=RangeStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-38)                Open=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-39)                Closed=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-40)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-41)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-42)        similarity=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-43)            title='Similarity'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-44)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-45)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-12-46))
    

Returns `PatternRanges._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `PatternRanges._field_config`.

* * *

### from_pattern_search class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1760-L1982 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.from_pattern_search "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-1)PatternRanges.from_pattern_search(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-3)    pattern=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-4)    window=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-5)    max_window=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-6)    row_select_prob=1.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-7)    window_select_prob=1.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-8)    roll_forward=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-9)    interp_mode='mixed',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-10)    rescale_mode='minmax',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-11)    vmin=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-12)    vmax=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-13)    pmin=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-14)    pmax=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-15)    invert=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-16)    error_type='absolute',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-17)    distance_measure='mae',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-18)    max_error=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-19)    max_error_interp_mode=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-20)    max_error_as_maxdist=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-21)    max_error_strict=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-22)    min_pct_change=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-23)    max_pct_change=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-24)    min_similarity=0.85,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-25)    minp=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-26)    overlap_mode='disallow',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-27)    max_records=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-28)    random_subset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-29)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-30)    search_configs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-31)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-32)    execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-33)    attach_as_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-34)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-35)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-36)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-13-37))
    

Build [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges") from all occurrences of a pattern in an array.

Searches for parameters of the type [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param"), and if found, broadcasts and combines them using [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params"). Then, converts them into a list of search configurations. If none of such parameters was found among the passed arguments, builds one search configuration using the passed arguments. If `search_configs` is not None, uses it instead. In all cases, it uses the defaults defined in the signature of this method to augment search configurations. For example, passing `min_similarity` of 95% will use it in all search configurations except where it was explicitly overridden.

Argument `search_configs` must be provided as a sequence of [PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC "vectorbtpro.generic.ranges.PSC") instances. If any element is a list of [PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC "vectorbtpro.generic.ranges.PSC") instances itself, it will be used per column in `arr`, otherwise per entire `arr`. Each configuration will be resolved using [PatternRanges.resolve_search_config](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.resolve_search_config "vectorbtpro.generic.ranges.PatternRanges.resolve_search_config") to prepare arguments for the use in Numba.

After all the search configurations have been resolved, uses [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute "vectorbtpro.utils.execution.execute") to loop over each configuration and execute it using [find_pattern_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.find_pattern_1d_nb "vectorbtpro.generic.nb.records.find_pattern_1d_nb"). The results are then concatenated into a single records array and wrapped with [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges").

If `attach_as_close` is True, will attach `arr` as `close`.

`**kwargs` will be passed to [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges").

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L2051-L2070 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-14-1)PatternRanges.indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-14-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-14-3)    ranges_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-14-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-14-5))
    

Perform indexing on [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges").

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.metrics "Permanent link")

Metrics supported by [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-4)        calc_func=<function Ranges.<lambda> at 0x11e2a44a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-10)        calc_func=<function Ranges.<lambda> at 0x11e2a4540>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-16)        calc_func=<function Ranges.<lambda> at 0x11e2a45e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-21)    total_records=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-22)        title='Total Records',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-23)        calc_func='count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-24)        tags='records'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-26)    coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-27)        title='Coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-28)        calc_func='coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-29)        overlapping=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-30)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-31)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-32)            'coverage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-33)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-35)    overlap_coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-36)        title='Overlap Coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-37)        calc_func='coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-38)        overlapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-39)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-40)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-41)            'coverage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-42)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-43)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-44)    duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-45)        title='Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-46)        calc_func='duration.describe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-47)        post_calc_func=<function Ranges.<lambda> at 0x11e2a4680>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-48)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-49)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-50)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-51)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-52)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-53)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-54)    similarity=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-55)        title='Similarity',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-56)        calc_func='similarity.describe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-57)        post_calc_func=<function PatternRanges.<lambda> at 0x11e2a6200>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-58)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-59)            'pattern_ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-60)            'similarity'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-61)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-62)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-15-63))
    

Returns `PatternRanges._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `PatternRanges._metrics`.

* * *

### plot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L2101-L2258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.plot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-1)PatternRanges.plot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-3)    top_n=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-4)    fit_ranges=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-5)    plot_patterns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-6)    plot_max_error=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-7)    fill_distance=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-8)    pattern_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-9)    lower_max_error_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-10)    upper_max_error_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-11)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-12)    xref='x',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-13)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-14)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-15)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-16-16))
    

Plot pattern ranges.

Based on [Ranges.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot "vectorbtpro.generic.ranges.Ranges.plot") and [GenericAccessor.plot_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot_pattern "vectorbtpro.generic.accessors.GenericSRAccessor.plot_pattern").

**Args**

**`column`** : `str`
    Name of the column to plot.
**`top_n`** : `int`
    Filter top N range records by maximum duration.
**`fit_ranges`** : `bool`, `int`, `or sequence` of `int`
    

Whether or which range records to fit.

True to fit to all range records, integer or a sequence of such to fit to specific range records.

**`plot_patterns`** : `bool` or `array_like`
    Whether to plot [PSC.pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.pattern "vectorbtpro.generic.ranges.PSC.pattern").
**`plot_max_error`** : `array_like`
    Whether to plot [PSC.max_error](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC.max_error "vectorbtpro.generic.ranges.PSC.max_error").
**`fill_distance`** : `bool`
    

Whether to fill the space between close and pattern.

Visible for every interpolation mode except discrete.

**`pattern_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for pattern.
**`lower_max_error_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for lower max error.
**`upper_max_error_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for upper max error.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`xref`** : `str`
    X coordinate axis.
**`yref`** : `str`
    Y coordinate axis.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**kwargs`**
    Keyword arguments passed to [Ranges.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot "vectorbtpro.generic.ranges.Ranges.plot").

* * *

### resolve_column_stack_kwargs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L2016-L2032 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.resolve_column_stack_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-17-1)PatternRanges.resolve_column_stack_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-17-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-17-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-17-4))
    

Resolve keyword arguments for initializing [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges") after stacking along columns.

* * *

### resolve_row_stack_kwargs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1990-L2014 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.resolve_row_stack_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-18-1)PatternRanges.resolve_row_stack_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-18-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-18-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-18-4))
    

Resolve keyword arguments for initializing [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges") after stacking along columns.

* * *

### resolve_search_config class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1718-L1758 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.resolve_search_config "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-19-1)PatternRanges.resolve_search_config(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-19-2)    search_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-19-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-19-4))
    

Resolve search config for [PatternRanges.from_pattern_search](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.from_pattern_search "vectorbtpro.generic.ranges.PatternRanges.from_pattern_search").

Converts array-like objects into arrays and enums into integers.

* * *

### search_configs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L2072-L2075 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.search_configs "Permanent link")

List of [PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC "vectorbtpro.generic.ranges.PSC") instances, one per column.

* * *

### similarity cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.similarity "Permanent link")

Mapped array of the field `similarity`.

* * *

### with_delta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1984-L1988 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.with_delta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-20-1)PatternRanges.with_delta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-20-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-20-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-20-4))
    

Pass self to [Ranges.from_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta "vectorbtpro.generic.ranges.Ranges.from_delta") but with the index set to the last index.

* * *

## Ranges class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L225-L1534 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-1)Ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-3)    records_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-4)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-5)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-6)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-7)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-21-9))
    

Extends [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords "vectorbtpro.generic.price_records.PriceRecords") for working with range records.

Requires `records_arr` to have all fields defined in [range_dt](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.range_dt "vectorbtpro.generic.enums.range_dt").

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

  * [AllocRanges](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/records/#vectorbtpro.portfolio.pfopt.records.AllocRanges "vectorbtpro.portfolio.pfopt.records.AllocRanges")
  * [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns")
  * [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges "vectorbtpro.generic.ranges.PatternRanges")
  * [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades")



* * *

### avg_duration cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.avg_duration "Permanent link")

[Ranges.get_avg_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_avg_duration "vectorbtpro.generic.ranges.Ranges.get_avg_duration") with default arguments.

* * *

### col cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.col "Permanent link")

Mapped array of the field `col`.

* * *

### coverage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.coverage "Permanent link")

[Ranges.get_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_coverage "vectorbtpro.generic.ranges.Ranges.get_coverage") with default arguments.

* * *

### crop method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L354-L358 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.crop "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-22-1)Ranges.crop()
    

Remove any data outside the minimum start index and the maximum end index.

* * *

### duration cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.duration "Permanent link")

[Ranges.get_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_duration "vectorbtpro.generic.ranges.Ranges.get_duration") with default arguments.

* * *

### end_idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.end_idx "Permanent link")

Mapped array of the field `end_idx`.

* * *

### field_config property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.field_config "Permanent link")

Field config of [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-2)    dtype=np.dtype([
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-3)        ('id', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-4)        ('col', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-5)        ('start_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-6)        ('end_idx', 'int64'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-7)        ('status', 'int64')
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-8)    ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-9)    settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-10)        id=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-11)            name='id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-12)            title='Range Id',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-13)            mapping='ids'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-14)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-15)        col=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-16)            name='col',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-17)            title='Column',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-18)            mapping='columns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-19)            as_customdata=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-20)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-21)        idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-22)            name='end_idx',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-23)            title='Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-24)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-25)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-26)        start_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-27)            title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-28)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-29)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-30)        end_idx=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-31)            title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-32)            mapping='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-33)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-34)        status=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-35)            title='Status',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-36)            mapping=RangeStatusT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-37)                Open=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-38)                Closed=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-39)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-40)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-41)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-23-42))
    

Returns `Ranges._field_config`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change fields, you can either change the config in-place, override this property, or overwrite the instance variable `Ranges._field_config`.

* * *

### filter_max_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L376-L388 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_max_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-24-1)Ranges.filter_max_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-24-2)    max_duration,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-24-3)    real=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-24-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-24-5))
    

Filter out ranges that last more than a maximum duration.

* * *

### filter_min_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L362-L374 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.filter_min_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-25-1)Ranges.filter_min_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-25-2)    min_duration,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-25-3)    real=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-25-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-25-5))
    

Filter out ranges that last less than a minimum duration.

* * *

### first_idx cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_idx "Permanent link")

[Ranges.get_first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_idx "vectorbtpro.generic.ranges.Ranges.get_first_idx") with default arguments.

* * *

### first_pd_mask cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.first_pd_mask "Permanent link")

[Ranges.get_first_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_pd_mask "vectorbtpro.generic.ranges.Ranges.get_first_pd_mask") with default arguments.

* * *

### from_array class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L237-L276 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-1)Ranges.from_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-3)    gap_value=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-4)    attach_as_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-5)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-6)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-7)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-26-9))
    

Build [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") from an array.

Searches for sequences of

  * True values in boolean data (False acts as a gap),
  * positive values in integer data (-1 acts as a gap), and
  * non-NaN values in any other data (NaN acts as a gap).



If `attach_as_close` is True, will attach `arr` as `close`.

`**kwargs` will be passed to [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").

* * *

### from_delta class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L278-L348 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-1)Ranges.from_delta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-2)    records_or_mapped,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-3)    delta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-4)    shift=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-5)    idx_field_or_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-6)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-7)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-27-9))
    

Build [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") from a record/mapped array with a timedelta applied on its index field.

See [get_ranges_from_delta_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.get_ranges_from_delta_nb "vectorbtpro.generic.nb.records.get_ranges_from_delta_nb").

Set `delta` to an integer to wait a certain amount of rows. Set it to anything else to wait a timedelta. The conversion is done using [to_timedelta64](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timedelta64 "vectorbtpro.utils.datetime_.to_timedelta64"). The second option requires the index to be datetime-like, or at least the frequency to be set.

`**kwargs` will be passed to [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").

* * *

### get_avg_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L484-L501 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_avg_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-28-1)Ranges.get_avg_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-28-2)    real=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-28-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-28-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-28-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-28-6)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-28-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-28-8))
    

Get average range duration (as timedelta).

* * *

### get_coverage method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L522-L548 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_coverage "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-29-1)Ranges.get_coverage(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-29-2)    overlapping=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-29-3)    normalize=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-29-4)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-29-5)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-29-6)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-29-7)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-29-8))
    

Get coverage, that is, the number of steps that are covered by all ranges.

See [range_coverage_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.range_coverage_nb "vectorbtpro.generic.nb.records.range_coverage_nb").

* * *

### get_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L450-L465 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-30-1)Ranges.get_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-30-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-30-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-30-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-30-5))
    

Get the effective duration of each range in integer format.

* * *

### get_first_idx method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L439-L441 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_idx "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-31-1)Ranges.get_first_idx(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-31-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-31-3))
    

Get the first index in each range.

* * *

### get_first_pd_mask method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L392-L394 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_pd_mask "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-32-1)Ranges.get_first_pd_mask(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-32-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-32-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-32-4))
    

Get mask from [Ranges.get_first_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_first_idx "vectorbtpro.generic.ranges.Ranges.get_first_idx").

* * *

### get_invalid method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L432-L437 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_invalid "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-33-1)Ranges.get_invalid(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-33-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-33-3))
    

Get invalid ranges.

An invalid range has the start and/or end index set to -1.

* * *

### get_last_idx method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L443-L448 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_idx "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-34-1)Ranges.get_last_idx(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-34-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-34-3))
    

Get the last index in each range.

* * *

### get_last_pd_mask method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L396-L399 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_pd_mask "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-35-1)Ranges.get_last_pd_mask(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-35-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-35-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-35-4))
    

Get mask from [Ranges.get_last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_idx "vectorbtpro.generic.ranges.Ranges.get_last_idx").

* * *

### get_max_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L503-L520 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_max_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-36-1)Ranges.get_max_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-36-2)    real=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-36-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-36-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-36-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-36-6)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-36-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-36-8))
    

Get maximum range duration (as timedelta).

* * *

### get_projections method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L550-L684 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-1)Ranges.get_projections(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-2)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-3)    proj_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-4)    proj_period=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-5)    incl_end_idx=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-6)    extend=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-7)    rebase=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-8)    start_value=1.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-9)    ffill=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-10)    remove_empty=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-11)    return_raw=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-12)    start_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-13)    id_level=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-14)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-15)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-16)    clean_index_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-37-17))
    

Generate a projection for each range record.

See [map_ranges_to_projections_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.map_ranges_to_projections_nb "vectorbtpro.generic.nb.records.map_ranges_to_projections_nb").

Set `proj_start` to an integer to generate a projection after a certain row after the start row. Set it to anything else to wait a timedelta. The conversion is done using [to_timedelta64](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timedelta64 "vectorbtpro.utils.datetime_.to_timedelta64"). The second option requires the index to be datetime-like, or at least the frequency to be set.

Set `proj_period` the same way as `proj_start` to generate a projection of a certain length. Unless `extend` is True, it still respects the duration of the range.

Set `extend` to True to extend the projection even after the end of the range. The extending period is taken from the longest range duration if `proj_period` is None, and from the longest `proj_period` if it's not None.

Set `rebase` to True to make each projection start with 1, otherwise, each projection will consist of original `close` values during the projected period. Use `start_value` to replace 1 with another start value. It can also be a flexible array with elements per column. If `start_value` is -1, will set it to the latest row in `close`.

Set `ffill` to True to forward fill NaN values, even if they are NaN in `close` itself.

Set `remove_empty` to True to remove projections that are either NaN or with only one element. The index of each projection is still being tracked and will appear in the multi-index of the returned DataFrame.

Note

As opposed to the Numba-compiled function, the returned DataFrame will have projections stacked along columns rather than rows. Set `return_raw` to True to return them in the original format.

* * *

### get_ranges_pd_mask method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L401-L421 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_ranges_pd_mask "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-38-1)Ranges.get_ranges_pd_mask(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-38-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-38-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-38-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-38-5)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-38-6))
    

Get mask from ranges.

See [ranges_to_mask_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.ranges_to_mask_nb "vectorbtpro.generic.nb.records.ranges_to_mask_nb").

* * *

### get_real_duration method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L467-L482 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_real_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-39-1)Ranges.get_real_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-39-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-39-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-39-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-39-5))
    

Get the real duration of each range in timedelta format.

* * *

### get_valid method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L425-L430 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_valid "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-40-1)Ranges.get_valid(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-40-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-40-3))
    

Get valid ranges.

A valid range doesn't have the start and end index set to -1.

* * *

### id cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.id "Permanent link")

Mapped array of the field `id`.

* * *

### invalid cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.invalid "Permanent link")

[Ranges.get_invalid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_invalid "vectorbtpro.generic.ranges.Ranges.get_invalid") with default arguments.

* * *

### last_idx cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_idx "Permanent link")

[Ranges.get_last_idx](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_idx "vectorbtpro.generic.ranges.Ranges.get_last_idx") with default arguments.

* * *

### last_pd_mask cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.last_pd_mask "Permanent link")

[Ranges.get_last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_last_pd_mask "vectorbtpro.generic.ranges.Ranges.get_last_pd_mask") with default arguments.

* * *

### max_duration cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.max_duration "Permanent link")

[Ranges.get_max_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_max_duration "vectorbtpro.generic.ranges.Ranges.get_max_duration") with default arguments.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.metrics "Permanent link")

Metrics supported by [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-4)        calc_func=<function Ranges.<lambda> at 0x11e2a44a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-10)        calc_func=<function Ranges.<lambda> at 0x11e2a4540>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-16)        calc_func=<function Ranges.<lambda> at 0x11e2a45e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-21)    total_records=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-22)        title='Total Records',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-23)        calc_func='count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-24)        tags='records'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-26)    coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-27)        title='Coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-28)        calc_func='coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-29)        overlapping=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-30)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-31)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-32)            'coverage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-33)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-35)    overlap_coverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-36)        title='Overlap Coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-37)        calc_func='coverage',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-38)        overlapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-39)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-40)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-41)            'coverage'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-42)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-43)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-44)    duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-45)        title='Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-46)        calc_func='duration.describe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-47)        post_calc_func=<function Ranges.<lambda> at 0x11e2a4680>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-48)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-49)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-50)            'ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-51)            'duration'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-52)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-53)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-41-54))
    

Returns `Ranges._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `Ranges._metrics`.

* * *

### overlap_coverage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.overlap_coverage "Permanent link")

[Ranges.get_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_coverage "vectorbtpro.generic.ranges.Ranges.get_coverage") with arguments `{'overlapping': True}`.

* * *

### plot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1237-L1507 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-1)Ranges.plot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-3)    top_n=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-4)    plot_ohlc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-5)    plot_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-6)    plot_markers=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-7)    plot_zones=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-8)    ohlc_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-9)    ohlc_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-10)    close_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-11)    start_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-12)    end_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-13)    open_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-14)    closed_shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-15)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-16)    xref='x',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-17)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-18)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-19)    return_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-20)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-42-21))
    

Plot ranges.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`top_n`** : `int`
    Filter top N range records by maximum duration.
**`plot_ohlc`** : `bool` or `DataFrame`
    Whether to plot OHLC.
**`plot_close`** : `bool` or `Series`
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
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Ranges.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.generic.ranges.Ranges.close").
**`start_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for start values.
**`end_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for end values.
**`open_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for open zones.
**`closed_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for closed zones.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`xref`** : `str`
    X coordinate axis.
**`yref`** : `str`
    Y coordinate axis.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`return_close`** : `bool`
    Whether to return the close series along with the figure.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-43-1)>>> price = pd.Series(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-43-2)...     [1, 2, 1, 2, 3, 2, 1, 2, 3],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-43-3)...     index=pd.date_range("2020", periods=9),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-43-4)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-43-5)>>> vbt.Ranges.from_array(price >= 2).plot().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/ranges_plot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/ranges_plot.dark.svg#only-dark)

* * *

### plot_projections method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L752-L1063 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-1)Ranges.plot_projections(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-3)    min_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-4)    max_duration=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-5)    last_n=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-6)    top_n=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-7)    random_n=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-8)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-9)    proj_start='current_or_0',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-10)    proj_period='max',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-11)    incl_end_idx=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-12)    extend=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-13)    ffill=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-14)    plot_past_period='current_or_proj_period',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-15)    plot_ohlc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-16)    plot_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-17)    plot_projections=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-18)    plot_bands=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-19)    plot_lower=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-20)    plot_middle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-21)    plot_upper=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-22)    plot_aux_middle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-23)    plot_fill=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-24)    colorize=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-25)    ohlc_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-26)    ohlc_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-27)    close_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-28)    projection_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-29)    lower_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-30)    middle_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-31)    upper_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-32)    aux_middle_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-33)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-34)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-35)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-44-36))
    

Plot projections.

Combines generation of projections using [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.generic.ranges.Ranges.get_projections") and their plotting using [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").

**Args**

**`column`** : `str`
    Name of the column to plot.
**`min_duration`** : `str`, `int`, `or frequency_like`
    Filter range records by minimum duration.
**`max_duration`** : `str`, `int`, `or frequency_like`
    Filter range records by maximum duration.
**`last_n`** : `int`
    Select last N range records.
**`top_n`** : `int`
    Select top N range records by maximum duration.
**`random_n`** : `int`
    Select N range records randomly.
**`seed`** : `int`
    Seed to make output deterministic.
**`proj_start`** : `str`, `int`, `or frequency_like`
    

See [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.generic.ranges.Ranges.get_projections").

Allows an additional option "current_or_{value}", which sets `proj_start` to the duration of the current open range, and to the specified value if there is no open range.

**`proj_period`** : `str`, `int`, `or frequency_like`
    

See [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.generic.ranges.Ranges.get_projections").

Allows additional options "current_or_{option}", "mean", "min", "max", "median", or a percentage such as "50%" representing a quantile. All of those options are based on the duration of all the closed ranges filtered by the arguments above.

**`incl_end_idx`** : `bool`
    See [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.generic.ranges.Ranges.get_projections").
**`extend`** : `bool`
    See [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.generic.ranges.Ranges.get_projections").
**`ffill`** : `bool`
    See [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.generic.ranges.Ranges.get_projections").
**`plot_past_period`** : `str`, `int`, `or frequency_like`
    

Past period to plot.

Allows the same options as `proj_period` plus "proj_period" and "current_or_proj_period".

**`plot_ohlc`** : `bool` or `DataFrame`
    Whether to plot OHLC.
**`plot_close`** : `bool` or `Series`
    Whether to plot close.
**`plot_projections`** : `bool`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`plot_bands`** : `bool`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`plot_lower`** : `bool`, `str`, `or callable`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`plot_middle`** : `bool`, `str`, `or callable`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`plot_upper`** : `bool`, `str`, `or callable`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`plot_aux_middle`** : `bool`, `str`, `or callable`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`plot_fill`** : `bool`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`colorize`** : `bool`, `str`, `or callable`
    See [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections").
**`ohlc_type`**
    

Either 'OHLC', 'Candlestick' or Plotly trace.

Pass None to use the default.

**`ohlc_trace_kwargs`** : `dict`
    Keyword arguments passed to `ohlc_type`.
**`close_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Ranges.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.generic.ranges.Ranges.close").
**`projection_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for projections.
**`lower_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.plotly.graph_objects.Scatter` for lower band.
**`middle_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for middle band.
**`upper_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for upper band.
**`aux_middle_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for auxiliary middle band.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-1)>>> price = pd.Series(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-2)...     [11, 12, 13, 14, 11, 12, 13, 12, 11, 12],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-3)...     index=pd.date_range("2020", periods=10),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-4)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-5)>>> vbt.Ranges.from_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-6)...     price >= 12,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-7)...     attach_as_close=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-8)...     close=price,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-9)... ).plot_projections(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-10)...     proj_start=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-11)...     proj_period=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-12)...     extend=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-13)...     plot_past_period=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-45-14)... ).show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/ranges_plot_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/ranges_plot_projections.dark.svg#only-dark)

* * *

### plot_shapes method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1065-L1235 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_shapes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-1)Ranges.plot_shapes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-3)    plot_ohlc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-4)    plot_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-5)    ohlc_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-6)    ohlc_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-7)    close_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-8)    shape_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-9)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-10)    xref='x',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-11)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-12)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-13)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-46-14))
    

Plot range shapes.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`plot_ohlc`** : `bool` or `DataFrame`
    Whether to plot OHLC.
**`plot_close`** : `bool` or `Series`
    Whether to plot close.
**`ohlc_type`**
    

Either 'OHLC', 'Candlestick' or Plotly trace.

Pass None to use the default.

**`ohlc_trace_kwargs`** : `dict`
    Keyword arguments passed to `ohlc_type`.
**`close_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Ranges.close](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords.close "vectorbtpro.generic.ranges.Ranges.close").
**`shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for shapes.
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

  * Plot zones colored by duration:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-1)>>> price = pd.Series(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-2)...     [1, 2, 1, 2, 3, 2, 1, 2, 3],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-3)...     index=pd.date_range("2020", periods=9),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-4)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-6)>>> def get_opacity(self_col, i):
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-7)...     real_duration = self_col.get_real_duration().values
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-8)...     return real_duration[i] / real_duration.max() * 0.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-10)>>> vbt.Ranges.from_array(price >= 2).plot_shapes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-11)...     shape_kwargs=dict(fillcolor="teal", opacity=vbt.RepFunc(get_opacity))
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-47-12)... ).show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/ranges_plot_shapes.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/ranges_plot_shapes.dark.svg#only-dark)

* * *

### plots_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L1509-L1519 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plots_defaults "Permanent link")

Defaults for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.ranges.Ranges.plots").

Merges [Records.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.plots_defaults "vectorbtpro.records.base.Records.plots_defaults") and `plots` from [ranges](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.ranges "vectorbtpro._settings.ranges").

* * *

### projections cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.projections "Permanent link")

[Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections "vectorbtpro.generic.ranges.Ranges.get_projections") with default arguments.

* * *

### ranges_pd_mask cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.ranges_pd_mask "Permanent link")

[Ranges.get_ranges_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_ranges_pd_mask "vectorbtpro.generic.ranges.Ranges.get_ranges_pd_mask") with default arguments.

* * *

### real_duration cacheable_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.real_duration "Permanent link")

[Ranges.get_real_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_real_duration "vectorbtpro.generic.ranges.Ranges.get_real_duration") with default arguments.

* * *

### start_idx cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.start_idx "Permanent link")

Mapped array of the field `start_idx`.

* * *

### stats_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L686-L696 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.stats_defaults "Permanent link")

Defaults for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.ranges.Ranges.stats").

Merges [Records.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.stats_defaults "vectorbtpro.records.base.Records.stats_defaults") and `stats` from [ranges](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.ranges "vectorbtpro._settings.ranges").

* * *

### status cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status "Permanent link")

Mapped array of the field `status`.

* * *

### status_closed cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_closed "Permanent link")

Records filtered by `status == 1`.

* * *

### status_open cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.status_open "Permanent link")

Records filtered by `status == 0`.

* * *

### subplots property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.subplots "Permanent link")

Subplots supported by [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-48-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-48-2)    plot=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-48-3)        title='Ranges',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-48-4)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-48-5)        plot_func='plot',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-48-6)        tags='ranges'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-48-7)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-48-8))
    

Returns `Ranges._subplots`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `Ranges._subplots`.

* * *

### valid cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.valid "Permanent link")

[Ranges.get_valid](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_valid "vectorbtpro.generic.ranges.Ranges.get_valid") with default arguments.

* * *

### with_delta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/ranges.py#L350-L352 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.with_delta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-49-1)Ranges.with_delta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-49-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-49-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#__codelineno-49-4))
    

Pass self to [Ranges.from_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta "vectorbtpro.generic.ranges.Ranges.from_delta").
