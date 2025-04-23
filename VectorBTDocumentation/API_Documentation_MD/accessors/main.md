accessors signals

#  accessors module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors "Permanent link")

Custom Pandas accessors for signals.

Methods can be accessed as follows:

  * [SignalsSRAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsSRAccessor "vectorbtpro.signals.accessors.SignalsSRAccessor") -> `pd.Series.vbt.signals.*`
  * [SignalsDFAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsDFAccessor "vectorbtpro.signals.accessors.SignalsDFAccessor") -> `pd.DataFrame.vbt.signals.*`


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-3)>>> # vectorbtpro.signals.accessors.SignalsAccessor.pos_rank
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-4)>>> pd.Series([False, True, True, True, False]).vbt.signals.pos_rank()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-5)0   -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-6)1    0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-7)2    1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-8)3    2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-9)4   -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-0-10)dtype: int64
    

The accessors extend [vectorbtpro.generic.accessors](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/ "vectorbtpro.generic.accessors").

Note

The underlying Series/DataFrame must already be a signal series and have boolean data type.

Grouping is only supported by the methods that accept the `group_by` argument.

Accessors do not utilize caching.

**Run for the examples below**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-1)>>> mask = pd.DataFrame({
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-2)...     'a': [True, False, False, False, False],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-3)...     'b': [True, False, True, False, True],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-4)...     'c': [True, True, True, False, False]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-5)... }, index=pd.date_range("2020", periods=5))
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-6)>>> mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-7)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-8)2020-01-01   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-9)2020-01-02  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-10)2020-01-03  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-11)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-1-12)2020-01-05  False   True  False
    

## Stats[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#stats "Permanent link")

Hint

See [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats") and [SignalsAccessor.metrics](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.metrics "vectorbtpro.signals.accessors.SignalsAccessor.metrics").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-1)>>> mask.vbt.signals.stats(column='a')
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-2)Start                         2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-3)End                           2020-01-05 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-4)Period                            5 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-5)Total                                           1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-6)Rate [%]                                     20.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-7)First Index                   2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-8)Last Index                    2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-9)Norm Avg Index [-1, 1]                       -1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-10)Distance: Min                                 NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-11)Distance: Median                              NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-12)Distance: Max                                 NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-13)Total Partitions                                1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-14)Partition Rate [%]                          100.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-15)Partition Length: Min             1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-16)Partition Length: Median          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-17)Partition Length: Max             1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-18)Partition Distance: Min                       NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-19)Partition Distance: Median                    NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-20)Partition Distance: Max                       NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-2-21)Name: a, dtype: object
    

We can pass another signal array to compare this array with:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-1)>>> mask.vbt.signals.stats(column='a', settings=dict(target=mask['b']))
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-3)Start                         2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-4)End                           2020-01-05 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-5)Period                            5 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-6)Total                                           1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-7)Rate [%]                                     20.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-8)Total Overlapping                               1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-9)Overlapping Rate [%]                    33.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-10)First Index                   2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-11)Last Index                    2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-12)Norm Avg Index [-1, 1]                       -1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-13)Distance -> Target: Min           0 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-14)Distance -> Target: Median        2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-15)Distance -> Target: Max           4 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-16)Total Partitions                                1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-17)Partition Rate [%]                          100.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-18)Partition Length: Min             1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-19)Partition Length: Median          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-20)Partition Length: Max             1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-21)Partition Distance: Min                       NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-22)Partition Distance: Median                    NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-23)Partition Distance: Max                       NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-3-24)Name: a, dtype: object
    

We can also return duration as a floating number rather than a timedelta:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-1)>>> mask.vbt.signals.stats(column='a', settings=dict(to_timedelta=False))
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-2)Start                         2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-3)End                           2020-01-05 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-4)Period                                          5
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-5)Total                                           1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-6)Rate [%]                                     20.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-7)First Index                   2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-8)Last Index                    2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-9)Norm Avg Index [-1, 1]                       -1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-10)Distance: Min                                 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-11)Distance: Median                              NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-12)Distance: Max                                 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-13)Total Partitions                                1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-14)Partition Rate [%]                          100.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-15)Partition Length: Min                         1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-16)Partition Length: Median                      1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-17)Partition Length: Max                         1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-18)Partition Distance: Min                       NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-19)Partition Distance: Median                    NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-20)Partition Distance: Max                       NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-4-21)Name: a, dtype: object
    

[StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.signals.accessors.SignalsAccessor.stats") also supports (re-)grouping:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-1)>>> mask.vbt.signals.stats(column=0, group_by=[0, 0, 1])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-2)Start                         2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-3)End                           2020-01-05 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-4)Period                            5 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-5)Total                                           4
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-6)Rate [%]                                     40.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-7)First Index                   2020-01-01 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-8)Last Index                    2020-01-05 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-9)Norm Avg Index [-1, 1]                      -0.25
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-10)Distance: Min                     2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-11)Distance: Median                  2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-12)Distance: Max                     2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-13)Total Partitions                                4
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-14)Partition Rate [%]                          100.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-15)Partition Length: Min             1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-16)Partition Length: Median          1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-17)Partition Length: Max             1 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-18)Partition Distance: Min           2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-19)Partition Distance: Median        2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-20)Partition Distance: Max           2 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-5-21)Name: 0, dtype: object
    

## Plots[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#plots "Permanent link")

Hint

See [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots") and [SignalsAccessor.subplots](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.subplots "vectorbtpro.signals.accessors.SignalsAccessor.subplots").

This class inherits subplots from [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor "vectorbtpro.generic.accessors.GenericAccessor").

* * *

## SignalsAccessor class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L211-L2959 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-6-1)SignalsAccessor(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-6-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-6-3)    obj=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-6-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-6-5))
    

Accessor on top of signal series. For both, Series and DataFrames.

Accessible via `pd.Series.vbt.signals` and `pd.DataFrame.vbt.signals`.

**Superclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [BaseAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor "vectorbtpro.base.accessors.BaseAccessor")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor "vectorbtpro.generic.accessors.GenericAccessor")
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
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.generic.accessors.GenericAccessor.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.generic.accessors.GenericAccessor.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.generic.accessors.GenericAccessor.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.generic.accessors.GenericAccessor.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.generic.accessors.GenericAccessor.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.accessors.GenericAccessor.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.accessors.GenericAccessor.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.accessors.GenericAccessor.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.accessors.GenericAccessor.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.accessors.GenericAccessor.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.accessors.GenericAccessor.find_messages")
  * [BaseAccessor.align](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.align "vectorbtpro.generic.accessors.GenericAccessor.align")
  * [BaseAccessor.align_to](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.align_to "vectorbtpro.generic.accessors.GenericAccessor.align_to")
  * [BaseAccessor.apply](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply "vectorbtpro.generic.accessors.GenericAccessor.apply")
  * [BaseAccessor.apply_and_concat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply_and_concat "vectorbtpro.generic.accessors.GenericAccessor.apply_and_concat")
  * [BaseAccessor.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply_to_index "vectorbtpro.generic.accessors.GenericAccessor.apply_to_index")
  * [BaseAccessor.broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast "vectorbtpro.generic.accessors.GenericAccessor.broadcast")
  * [BaseAccessor.broadcast_combs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast_combs "vectorbtpro.generic.accessors.GenericAccessor.broadcast_combs")
  * [BaseAccessor.broadcast_to](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast_to "vectorbtpro.generic.accessors.GenericAccessor.broadcast_to")
  * [BaseAccessor.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.column_stack "vectorbtpro.generic.accessors.GenericAccessor.column_stack")
  * [BaseAccessor.combine](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.combine "vectorbtpro.generic.accessors.GenericAccessor.combine")
  * [BaseAccessor.concat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.concat "vectorbtpro.generic.accessors.GenericAccessor.concat")
  * [BaseAccessor.cross](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.cross "vectorbtpro.generic.accessors.GenericAccessor.cross")
  * [BaseAccessor.cross](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.x "vectorbtpro.generic.accessors.GenericAccessor.x")
  * [BaseAccessor.cross_with](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.cross_with "vectorbtpro.generic.accessors.GenericAccessor.cross_with")
  * [BaseAccessor.eval](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.eval "vectorbtpro.generic.accessors.GenericAccessor.eval")
  * [BaseAccessor.get](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.get "vectorbtpro.generic.accessors.GenericAccessor.get")
  * [BaseAccessor.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.indexing_func "vectorbtpro.generic.accessors.GenericAccessor.indexing_func")
  * [BaseAccessor.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.indexing_setter_func "vectorbtpro.generic.accessors.GenericAccessor.indexing_setter_func")
  * [BaseAccessor.is_frame](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.is_frame "vectorbtpro.generic.accessors.GenericAccessor.is_frame")
  * [BaseAccessor.is_series](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.is_series "vectorbtpro.generic.accessors.GenericAccessor.is_series")
  * [BaseAccessor.make_symmetric](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.make_symmetric "vectorbtpro.generic.accessors.GenericAccessor.make_symmetric")
  * [BaseAccessor.repeat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.repeat "vectorbtpro.generic.accessors.GenericAccessor.repeat")
  * [BaseAccessor.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_column_stack_kwargs "vectorbtpro.generic.accessors.GenericAccessor.resolve_column_stack_kwargs")
  * [BaseAccessor.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_row_stack_kwargs "vectorbtpro.generic.accessors.GenericAccessor.resolve_row_stack_kwargs")
  * [BaseAccessor.resolve_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_shape "vectorbtpro.generic.accessors.GenericAccessor.resolve_shape")
  * [BaseAccessor.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.row_stack "vectorbtpro.generic.accessors.GenericAccessor.row_stack")
  * [BaseAccessor.set](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set "vectorbtpro.generic.accessors.GenericAccessor.set")
  * [BaseAccessor.set_between](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set_between "vectorbtpro.generic.accessors.GenericAccessor.set_between")
  * [BaseAccessor.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.generic.accessors.GenericAccessor.should_wrap")
  * [BaseAccessor.tile](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.tile "vectorbtpro.generic.accessors.GenericAccessor.tile")
  * [BaseAccessor.to_1d_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_1d_array "vectorbtpro.generic.accessors.GenericAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_2d_array "vectorbtpro.generic.accessors.GenericAccessor.to_2d_array")
  * [BaseAccessor.to_data](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_data "vectorbtpro.generic.accessors.GenericAccessor.to_data")
  * [BaseAccessor.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_dict "vectorbtpro.generic.accessors.GenericAccessor.to_dict")
  * [BaseAccessor.unstack_to_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.unstack_to_array "vectorbtpro.generic.accessors.GenericAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.unstack_to_df "vectorbtpro.generic.accessors.GenericAccessor.unstack_to_df")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.accessors.GenericAccessor.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.accessors.GenericAccessor.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.accessors.GenericAccessor.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.accessors.GenericAccessor.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.accessors.GenericAccessor.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.accessors.GenericAccessor.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.accessors.GenericAccessor.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.generic.accessors.GenericAccessor.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.accessors.GenericAccessor.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.accessors.GenericAccessor.update_config")
  * [GenericAccessor.ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ago "vectorbtpro.generic.accessors.GenericAccessor.ago")
  * [GenericAccessor.all_ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.all_ago "vectorbtpro.generic.accessors.GenericAccessor.all_ago")
  * [GenericAccessor.any_ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.any_ago "vectorbtpro.generic.accessors.GenericAccessor.any_ago")
  * [GenericAccessor.apply_along_axis](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_along_axis "vectorbtpro.generic.accessors.GenericAccessor.apply_along_axis")
  * [GenericAccessor.apply_and_reduce](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_and_reduce "vectorbtpro.generic.accessors.GenericAccessor.apply_and_reduce")
  * [GenericAccessor.apply_mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_mapping "vectorbtpro.generic.accessors.GenericAccessor.apply_mapping")
  * [GenericAccessor.areaplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.areaplot "vectorbtpro.generic.accessors.GenericAccessor.areaplot")
  * [GenericAccessor.barplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.barplot "vectorbtpro.generic.accessors.GenericAccessor.barplot")
  * [GenericAccessor.bfill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.bfill "vectorbtpro.generic.accessors.GenericAccessor.bfill")
  * [GenericAccessor.binarize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.binarize "vectorbtpro.generic.accessors.GenericAccessor.binarize")
  * [GenericAccessor.boxplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.boxplot "vectorbtpro.generic.accessors.GenericAccessor.boxplot")
  * [GenericAccessor.bshift](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.bshift "vectorbtpro.generic.accessors.GenericAccessor.bshift")
  * [GenericAccessor.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.generic.accessors.GenericAccessor.cls_dir")
  * [GenericAccessor.column_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.column_apply "vectorbtpro.generic.accessors.GenericAccessor.column_apply")
  * [GenericAccessor.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.generic.accessors.GenericAccessor.column_only_select")
  * [GenericAccessor.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.accessors.GenericAccessor.config")
  * [GenericAccessor.corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.corr "vectorbtpro.generic.accessors.GenericAccessor.corr")
  * [GenericAccessor.count](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.count "vectorbtpro.generic.accessors.GenericAccessor.count")
  * [GenericAccessor.cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cov "vectorbtpro.generic.accessors.GenericAccessor.cov")
  * [GenericAccessor.crossed_above](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_above "vectorbtpro.generic.accessors.GenericAccessor.crossed_above")
  * [GenericAccessor.crossed_below](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_below "vectorbtpro.generic.accessors.GenericAccessor.crossed_below")
  * [GenericAccessor.cumprod](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cumprod "vectorbtpro.generic.accessors.GenericAccessor.cumprod")
  * [GenericAccessor.cumsum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cumsum "vectorbtpro.generic.accessors.GenericAccessor.cumsum")
  * [GenericAccessor.demean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.demean "vectorbtpro.generic.accessors.GenericAccessor.demean")
  * [GenericAccessor.describe](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.describe "vectorbtpro.generic.accessors.GenericAccessor.describe")
  * [GenericAccessor.df_accessor_cls](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.df_accessor_cls "vectorbtpro.generic.accessors.GenericAccessor.df_accessor_cls")
  * [GenericAccessor.diff](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.diff "vectorbtpro.generic.accessors.GenericAccessor.diff")
  * [GenericAccessor.digitize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.digitize "vectorbtpro.generic.accessors.GenericAccessor.digitize")
  * [GenericAccessor.drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.drawdown "vectorbtpro.generic.accessors.GenericAccessor.drawdown")
  * [GenericAccessor.drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.drawdowns "vectorbtpro.generic.accessors.GenericAccessor.drawdowns")
  * [GenericAccessor.ewm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ewm_mean "vectorbtpro.generic.accessors.GenericAccessor.ewm_mean")
  * [GenericAccessor.ewm_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ewm_std "vectorbtpro.generic.accessors.GenericAccessor.ewm_std")
  * [GenericAccessor.expanding_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_apply "vectorbtpro.generic.accessors.GenericAccessor.expanding_apply")
  * [GenericAccessor.expanding_corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_corr "vectorbtpro.generic.accessors.GenericAccessor.expanding_corr")
  * [GenericAccessor.expanding_cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_cov "vectorbtpro.generic.accessors.GenericAccessor.expanding_cov")
  * [GenericAccessor.expanding_idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_idxmax "vectorbtpro.generic.accessors.GenericAccessor.expanding_idxmax")
  * [GenericAccessor.expanding_idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_idxmin "vectorbtpro.generic.accessors.GenericAccessor.expanding_idxmin")
  * [GenericAccessor.expanding_max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_max "vectorbtpro.generic.accessors.GenericAccessor.expanding_max")
  * [GenericAccessor.expanding_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_mean "vectorbtpro.generic.accessors.GenericAccessor.expanding_mean")
  * [GenericAccessor.expanding_min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_min "vectorbtpro.generic.accessors.GenericAccessor.expanding_min")
  * [GenericAccessor.expanding_ols](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_ols "vectorbtpro.generic.accessors.GenericAccessor.expanding_ols")
  * [GenericAccessor.expanding_rank](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_rank "vectorbtpro.generic.accessors.GenericAccessor.expanding_rank")
  * [GenericAccessor.expanding_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_std "vectorbtpro.generic.accessors.GenericAccessor.expanding_std")
  * [GenericAccessor.expanding_zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_zscore "vectorbtpro.generic.accessors.GenericAccessor.expanding_zscore")
  * [GenericAccessor.fbfill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fbfill "vectorbtpro.generic.accessors.GenericAccessor.fbfill")
  * [GenericAccessor.ffill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ffill "vectorbtpro.generic.accessors.GenericAccessor.ffill")
  * [GenericAccessor.fillna](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fillna "vectorbtpro.generic.accessors.GenericAccessor.fillna")
  * [GenericAccessor.find_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.find_pattern "vectorbtpro.generic.accessors.GenericAccessor.find_pattern")
  * [GenericAccessor.flatten_grouped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.flatten_grouped "vectorbtpro.generic.accessors.GenericAccessor.flatten_grouped")
  * [GenericAccessor.fshift](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fshift "vectorbtpro.generic.accessors.GenericAccessor.fshift")
  * [GenericAccessor.get_drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.get_drawdowns "vectorbtpro.generic.accessors.GenericAccessor.get_drawdowns")
  * [GenericAccessor.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.get_ranges "vectorbtpro.generic.accessors.GenericAccessor.get_ranges")
  * [GenericAccessor.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.generic.accessors.GenericAccessor.group_select")
  * [GenericAccessor.groupby_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_apply "vectorbtpro.generic.accessors.GenericAccessor.groupby_apply")
  * [GenericAccessor.groupby_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_transform "vectorbtpro.generic.accessors.GenericAccessor.groupby_transform")
  * [GenericAccessor.heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.heatmap "vectorbtpro.generic.accessors.GenericAccessor.heatmap")
  * [GenericAccessor.histplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.histplot "vectorbtpro.generic.accessors.GenericAccessor.histplot")
  * [GenericAccessor.idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.idxmax "vectorbtpro.generic.accessors.GenericAccessor.idxmax")
  * [GenericAccessor.idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.idxmin "vectorbtpro.generic.accessors.GenericAccessor.idxmin")
  * [GenericAccessor.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.generic.accessors.GenericAccessor.iloc")
  * [GenericAccessor.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.generic.accessors.GenericAccessor.indexing_kwargs")
  * [GenericAccessor.lineplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.lineplot "vectorbtpro.generic.accessors.GenericAccessor.lineplot")
  * [GenericAccessor.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.generic.accessors.GenericAccessor.loc")
  * [GenericAccessor.ma](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ma "vectorbtpro.generic.accessors.GenericAccessor.ma")
  * [GenericAccessor.map](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.map "vectorbtpro.generic.accessors.GenericAccessor.map")
  * [GenericAccessor.mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.mapping "vectorbtpro.generic.accessors.GenericAccessor.mapping")
  * [GenericAccessor.max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.max "vectorbtpro.generic.accessors.GenericAccessor.max")
  * [GenericAccessor.maxabs_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.maxabs_scale "vectorbtpro.generic.accessors.GenericAccessor.maxabs_scale")
  * [GenericAccessor.mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.mean "vectorbtpro.generic.accessors.GenericAccessor.mean")
  * [GenericAccessor.median](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.median "vectorbtpro.generic.accessors.GenericAccessor.median")
  * [GenericAccessor.min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.min "vectorbtpro.generic.accessors.GenericAccessor.min")
  * [GenericAccessor.minmax_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.minmax_scale "vectorbtpro.generic.accessors.GenericAccessor.minmax_scale")
  * [GenericAccessor.msd](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.msd "vectorbtpro.generic.accessors.GenericAccessor.msd")
  * [GenericAccessor.ndim](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.ndim "vectorbtpro.generic.accessors.GenericAccessor.ndim")
  * [GenericAccessor.normalize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.normalize "vectorbtpro.generic.accessors.GenericAccessor.normalize")
  * [GenericAccessor.obj](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.obj "vectorbtpro.generic.accessors.GenericAccessor.obj")
  * [GenericAccessor.overlay_with_heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.overlay_with_heatmap "vectorbtpro.generic.accessors.GenericAccessor.overlay_with_heatmap")
  * [GenericAccessor.pct_change](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.pct_change "vectorbtpro.generic.accessors.GenericAccessor.pct_change")
  * [GenericAccessor.plot_against](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot_against "vectorbtpro.generic.accessors.GenericAccessor.plot_against")
  * [GenericAccessor.plot_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot_pattern "vectorbtpro.generic.accessors.GenericAccessor.plot_pattern")
  * [GenericAccessor.power_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.power_transform "vectorbtpro.generic.accessors.GenericAccessor.power_transform")
  * [GenericAccessor.product](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.product "vectorbtpro.generic.accessors.GenericAccessor.product")
  * [GenericAccessor.proximity_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.proximity_apply "vectorbtpro.generic.accessors.GenericAccessor.proximity_apply")
  * [GenericAccessor.qqplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.qqplot "vectorbtpro.generic.accessors.GenericAccessor.qqplot")
  * [GenericAccessor.quantile_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.quantile_transform "vectorbtpro.generic.accessors.GenericAccessor.quantile_transform")
  * [GenericAccessor.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.generic.accessors.GenericAccessor.range_only_select")
  * [GenericAccessor.ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ranges "vectorbtpro.generic.accessors.GenericAccessor.ranges")
  * [GenericAccessor.realign](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign "vectorbtpro.generic.accessors.GenericAccessor.realign")
  * [GenericAccessor.realign_closing](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_closing "vectorbtpro.generic.accessors.GenericAccessor.realign_closing")
  * [GenericAccessor.realign_opening](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_opening "vectorbtpro.generic.accessors.GenericAccessor.realign_opening")
  * [GenericAccessor.rebase](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rebase "vectorbtpro.generic.accessors.GenericAccessor.rebase")
  * [GenericAccessor.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.accessors.GenericAccessor.rec_state")
  * [GenericAccessor.reduce](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.reduce "vectorbtpro.generic.accessors.GenericAccessor.reduce")
  * [GenericAccessor.resample_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_apply "vectorbtpro.generic.accessors.GenericAccessor.resample_apply")
  * [GenericAccessor.resample_between_bounds](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_between_bounds "vectorbtpro.generic.accessors.GenericAccessor.resample_between_bounds")
  * [GenericAccessor.resample_to_index](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_to_index "vectorbtpro.generic.accessors.GenericAccessor.resample_to_index")
  * [GenericAccessor.resolve_mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resolve_mapping "vectorbtpro.generic.accessors.GenericAccessor.resolve_mapping")
  * [GenericAccessor.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resolve_self "vectorbtpro.generic.accessors.GenericAccessor.resolve_self")
  * [GenericAccessor.robust_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.robust_scale "vectorbtpro.generic.accessors.GenericAccessor.robust_scale")
  * [GenericAccessor.rolling_all](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_all "vectorbtpro.generic.accessors.GenericAccessor.rolling_all")
  * [GenericAccessor.rolling_any](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_any "vectorbtpro.generic.accessors.GenericAccessor.rolling_any")
  * [GenericAccessor.rolling_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_apply "vectorbtpro.generic.accessors.GenericAccessor.rolling_apply")
  * [GenericAccessor.rolling_corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_corr "vectorbtpro.generic.accessors.GenericAccessor.rolling_corr")
  * [GenericAccessor.rolling_cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_cov "vectorbtpro.generic.accessors.GenericAccessor.rolling_cov")
  * [GenericAccessor.rolling_idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_idxmax "vectorbtpro.generic.accessors.GenericAccessor.rolling_idxmax")
  * [GenericAccessor.rolling_idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_idxmin "vectorbtpro.generic.accessors.GenericAccessor.rolling_idxmin")
  * [GenericAccessor.rolling_max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_max "vectorbtpro.generic.accessors.GenericAccessor.rolling_max")
  * [GenericAccessor.rolling_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_mean "vectorbtpro.generic.accessors.GenericAccessor.rolling_mean")
  * [GenericAccessor.rolling_min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_min "vectorbtpro.generic.accessors.GenericAccessor.rolling_min")
  * [GenericAccessor.rolling_ols](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_ols "vectorbtpro.generic.accessors.GenericAccessor.rolling_ols")
  * [GenericAccessor.rolling_pattern_similarity](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_pattern_similarity "vectorbtpro.generic.accessors.GenericAccessor.rolling_pattern_similarity")
  * [GenericAccessor.rolling_prod](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_prod "vectorbtpro.generic.accessors.GenericAccessor.rolling_prod")
  * [GenericAccessor.rolling_rank](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_rank "vectorbtpro.generic.accessors.GenericAccessor.rolling_rank")
  * [GenericAccessor.rolling_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_std "vectorbtpro.generic.accessors.GenericAccessor.rolling_std")
  * [GenericAccessor.rolling_sum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_sum "vectorbtpro.generic.accessors.GenericAccessor.rolling_sum")
  * [GenericAccessor.rolling_zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_zscore "vectorbtpro.generic.accessors.GenericAccessor.rolling_zscore")
  * [GenericAccessor.row_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.row_apply "vectorbtpro.generic.accessors.GenericAccessor.row_apply")
  * [GenericAccessor.scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.scale "vectorbtpro.generic.accessors.GenericAccessor.scale")
  * [GenericAccessor.scatterplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.scatterplot "vectorbtpro.generic.accessors.GenericAccessor.scatterplot")
  * [GenericAccessor.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.generic.accessors.GenericAccessor.self_aliases")
  * [GenericAccessor.shuffle](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.shuffle "vectorbtpro.generic.accessors.GenericAccessor.shuffle")
  * [GenericAccessor.squeeze_grouped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.squeeze_grouped "vectorbtpro.generic.accessors.GenericAccessor.squeeze_grouped")
  * [GenericAccessor.sr_accessor_cls](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.sr_accessor_cls "vectorbtpro.generic.accessors.GenericAccessor.sr_accessor_cls")
  * [GenericAccessor.std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.std "vectorbtpro.generic.accessors.GenericAccessor.std")
  * [GenericAccessor.sum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.sum "vectorbtpro.generic.accessors.GenericAccessor.sum")
  * [GenericAccessor.to_daily_log_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_daily_log_returns "vectorbtpro.generic.accessors.GenericAccessor.to_daily_log_returns")
  * [GenericAccessor.to_daily_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_daily_returns "vectorbtpro.generic.accessors.GenericAccessor.to_daily_returns")
  * [GenericAccessor.to_log_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_log_returns "vectorbtpro.generic.accessors.GenericAccessor.to_log_returns")
  * [GenericAccessor.to_mapped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_mapped "vectorbtpro.generic.accessors.GenericAccessor.to_mapped")
  * [GenericAccessor.to_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_returns "vectorbtpro.generic.accessors.GenericAccessor.to_returns")
  * [GenericAccessor.transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.transform "vectorbtpro.generic.accessors.GenericAccessor.transform")
  * [GenericAccessor.ts_heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ts_heatmap "vectorbtpro.generic.accessors.GenericAccessor.ts_heatmap")
  * [GenericAccessor.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.generic.accessors.GenericAccessor.unwrapped")
  * [GenericAccessor.value_counts](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.value_counts "vectorbtpro.generic.accessors.GenericAccessor.value_counts")
  * [GenericAccessor.vidya](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.vidya "vectorbtpro.generic.accessors.GenericAccessor.vidya")
  * [GenericAccessor.volume](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.volume "vectorbtpro.generic.accessors.GenericAccessor.volume")
  * [GenericAccessor.wm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wm_mean "vectorbtpro.generic.accessors.GenericAccessor.wm_mean")
  * [GenericAccessor.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.generic.accessors.GenericAccessor.wrapper")
  * [GenericAccessor.wwm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wwm_mean "vectorbtpro.generic.accessors.GenericAccessor.wwm_mean")
  * [GenericAccessor.wwm_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wwm_std "vectorbtpro.generic.accessors.GenericAccessor.wwm_std")
  * [GenericAccessor.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.generic.accessors.GenericAccessor.xloc")
  * [GenericAccessor.zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.zscore "vectorbtpro.generic.accessors.GenericAccessor.zscore")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.accessors.GenericAccessor.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.accessors.GenericAccessor.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.accessors.GenericAccessor.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.accessors.GenericAccessor.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.accessors.GenericAccessor.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.accessors.GenericAccessor.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.accessors.GenericAccessor.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.accessors.GenericAccessor.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.accessors.GenericAccessor.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.accessors.GenericAccessor.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.accessors.GenericAccessor.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.accessors.GenericAccessor.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.generic.accessors.GenericAccessor.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.generic.accessors.GenericAccessor.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.generic.accessors.GenericAccessor.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.generic.accessors.GenericAccessor.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.generic.accessors.GenericAccessor.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.generic.accessors.GenericAccessor.select_col_from_obj")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.generic.accessors.GenericAccessor.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.generic.accessors.GenericAccessor.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.generic.accessors.GenericAccessor.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.generic.accessors.GenericAccessor.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.generic.accessors.GenericAccessor.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.generic.accessors.GenericAccessor.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.generic.accessors.GenericAccessor.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.generic.accessors.GenericAccessor.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.generic.accessors.GenericAccessor.select_levels")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.generic.accessors.GenericAccessor.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.generic.accessors.GenericAccessor.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.accessors.GenericAccessor.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.accessors.GenericAccessor.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.accessors.GenericAccessor.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.accessors.GenericAccessor.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.accessors.GenericAccessor.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.accessors.GenericAccessor.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.accessors.GenericAccessor.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.accessors.GenericAccessor.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.accessors.GenericAccessor.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.accessors.GenericAccessor.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.accessors.GenericAccessor.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.accessors.GenericAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.generic.accessors.GenericAccessor.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.generic.accessors.GenericAccessor.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.accessors.GenericAccessor.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.generic.accessors.GenericAccessor.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.accessors.GenericAccessor.pprint")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.generic.accessors.GenericAccessor.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.generic.accessors.GenericAccessor.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.generic.accessors.GenericAccessor.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.accessors.GenericAccessor.stats")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.generic.accessors.GenericAccessor.regroup")
  * [Wrapping.resample](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resample "vectorbtpro.generic.accessors.GenericAccessor.resample")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.generic.accessors.GenericAccessor.resolve_stack_kwargs")



**Subclasses**

  * [SignalsDFAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsDFAccessor "vectorbtpro.signals.accessors.SignalsDFAccessor")
  * [SignalsSRAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsSRAccessor "vectorbtpro.signals.accessors.SignalsSRAccessor")



* * *

### between_partition_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2096-L2119 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_partition_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-7-1)SignalsAccessor.between_partition_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-7-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-7-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-7-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-7-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-7-6))
    

Wrap the result of [between_partition_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_partition_ranges_nb "vectorbtpro.signals.nb.between_partition_ranges_nb") with [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-8-1)>>> mask_sr = pd.Series([True, False, False, True, False, True, True])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-8-2)>>> mask_sr.vbt.signals.between_partition_ranges().readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-8-3)   Range Id  Column  Start Timestamp  End Timestamp  Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-8-4)0         0       0                0              3  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-8-5)1         1       0                3              5  Closed
    

* * *

### between_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1966-L2066 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-1)SignalsAccessor.between_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-2)    target=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-3)    relation='onemany',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-4)    incl_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-5)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-6)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-7)    attach_target=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-8)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-9)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-10)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-9-11))
    

Wrap the result of [between_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_ranges_nb "vectorbtpro.signals.nb.between_ranges_nb") with [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").

If `target` specified, see [between_two_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_two_ranges_nb "vectorbtpro.signals.nb.between_two_ranges_nb"). Both will broadcast using [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "vectorbtpro.base.reshaping.broadcast") and `broadcast_kwargs`.

**Usage**

  * One array:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-1)>>> mask_sr = pd.Series([True, False, False, True, False, True, True])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-2)>>> ranges = mask_sr.vbt.signals.between_ranges()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-3)>>> ranges
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-4)<vectorbtpro.generic.ranges.Ranges at 0x7ff29ea7c7b8>
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-6)>>> ranges.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-7)   Range Id  Column  Start Index  End Index  Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-8)0         0       0            0          3  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-9)1         1       0            3          5  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-10)2         2       0            5          6  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-12)>>> ranges.duration.values
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-10-13)array([3, 2, 1])
    

  * Two arrays, traversing the signals of the first array:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-1)>>> mask_sr1 = pd.Series([True, True, True, False, False])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-2)>>> mask_sr2 = pd.Series([False, False, True, False, True])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-3)>>> ranges = mask_sr1.vbt.signals.between_ranges(target=mask_sr2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-4)>>> ranges
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-5)<vectorbtpro.generic.ranges.Ranges at 0x7ff29e3b80f0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-7)>>> ranges.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-8)   Range Id  Column  Start Index  End Index  Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-9)0         0       0            2          2  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-10)1         1       0            2          4  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-12)>>> ranges.duration.values
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-11-13)array([0, 2])
    

  * Two arrays, traversing the signals of the second array:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-1)>>> ranges = mask_sr1.vbt.signals.between_ranges(target=mask_sr2, relation="manyone")
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-2)>>> ranges
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-3)<vectorbtpro.generic.ranges.Ranges at 0x7ff29eccbd68>
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-5)>>> ranges.readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-6)   Range Id  Column  Start Index  End Index  Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-7)0         0       0            0          2  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-8)1         1       0            1          2  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-9)2         2       0            2          2  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-11)>>> ranges.duration.values
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-12-12)array([0, 2])
    

* * *

### clean class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L579-L627 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.clean "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-1)SignalsAccessor.clean(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-3)    force_first=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-4)    keep_conflicts=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-5)    reverse_order=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-6)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-7)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-8)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-9)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-13-10))
    

Clean signals.

If one array is passed, see [SignalsAccessor.first](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first "vectorbtpro.signals.accessors.SignalsAccessor.first"). If two arrays passed, entries and exits, see [clean_enex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.clean_enex_nb "vectorbtpro.signals.nb.clean_enex_nb").

* * *

### delta_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1956-L1964 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.delta_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-14-1)SignalsAccessor.delta_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-14-2)    delta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-14-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-14-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-14-5))
    

Build a record array of the type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges") from a delta applied after each signal (or before if delta is negative).

* * *

### distance_from_last method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1877-L1914 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.distance_from_last "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-15-1)SignalsAccessor.distance_from_last(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-15-2)    nth=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-15-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-15-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-15-5)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-15-6))
    

See [distance_from_last_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.distance_from_last_nb "vectorbtpro.signals.nb.distance_from_last_nb").

**Usage**

  * Get the distance to the last signal:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-16-1)>>> mask.vbt.signals.distance_from_last()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-16-2)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-16-3)2020-01-01 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-16-4)2020-01-02  1  1  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-16-5)2020-01-03  2  2  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-16-6)2020-01-04  3  1  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-16-7)2020-01-05  4  2  2
    

  * Get the distance to the second last signal:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-17-1)>>> mask.vbt.signals.distance_from_last(nth=2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-17-2)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-17-3)2020-01-01 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-17-4)2020-01-02 -1 -1  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-17-5)2020-01-03 -1  2  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-17-6)2020-01-04 -1  3  2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-17-7)2020-01-05 -1  2  3
    

* * *

### empty class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L239-L242 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.empty "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-18-1)SignalsAccessor.empty(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-18-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-18-3)    fill_value=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-18-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-18-5))
    

[BaseAccessor.empty](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.empty "vectorbtpro.base.accessors.BaseAccessor.empty") with `fill_value=False`.

* * *

### empty_like class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L244-L247 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.empty_like "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-19-1)SignalsAccessor.empty_like(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-19-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-19-3)    fill_value=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-19-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-19-5))
    

[BaseAccessor.empty_like](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.empty_like "vectorbtpro.base.accessors.BaseAccessor.empty_like") with `fill_value=False`.

* * *

### first method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1765-L1774 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-20-1)SignalsAccessor.first(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-20-2)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-20-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-20-4))
    

Select signals that satisfy the condition `pos_rank == 0`.

Uses [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank").

* * *

### first_after method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1776-L1786 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first_after "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-21-1)SignalsAccessor.first_after(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-21-2)    reset_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-21-3)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-21-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-21-5))
    

Select signals that satisfy the condition `pos_rank == 0`.

Uses [SignalsAccessor.pos_rank_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after").

* * *

### from_nth method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1813-L1823 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.from_nth "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-22-1)SignalsAccessor.from_nth(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-22-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-22-3)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-22-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-22-5))
    

Select signals that satisfy the condition `pos_rank >= n`.

Uses [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank").

* * *

### from_nth_after method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1825-L1836 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.from_nth_after "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-23-1)SignalsAccessor.from_nth_after(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-23-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-23-3)    reset_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-23-4)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-23-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-23-6))
    

Select signals that satisfy the condition `pos_rank >= n`.

Uses [SignalsAccessor.pos_rank_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after").

* * *

### generate class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L256-L343 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-1)SignalsAccessor.generate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-3)    place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-4)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-5)    place_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-6)    only_once=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-7)    wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-8)    broadcast_named_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-9)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-10)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-11)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-12)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-13)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-14)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-24-15))
    

See [generate_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_nb "vectorbtpro.signals.nb.generate_nb").

`shape` can be a shape-like tuple or an instance of [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") (will be used as `wrapper`).

Arguments to `place_func_nb` can be passed either as `*args` or `place_args` (but not both!).

**Usage**

  * Generate random signals manually:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-1)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-2)... def place_func_nb(c):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-3)...     i = np.random.choice(len(c.out))
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-4)...     c.out[i] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-5)...     return i
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-7)>>> vbt.pd_acc.signals.generate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-8)...     (5, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-9)...     place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-10)...     wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-11)...         index=mask.index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-12)...         columns=mask.columns
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-13)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-14)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-15)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-16)2020-01-01   True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-17)2020-01-02  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-18)2020-01-03  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-19)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-25-20)2020-01-05  False  False  False
    

* * *

### generate_both class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L345-L498 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_both "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-1)SignalsAccessor.generate_both(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-3)    entry_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-4)    exit_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-5)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-6)    entry_place_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-7)    exit_place_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-8)    entry_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-9)    exit_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-10)    broadcast_named_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-11)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-12)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-13)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-14)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-15)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-16)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-26-17))
    

See [generate_enex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_enex_nb "vectorbtpro.signals.nb.generate_enex_nb").

`shape` can be a shape-like tuple or an instance of [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") (will be used as `wrapper`).

Arguments to `entry_place_func_nb` can be passed either as `*args` or `entry_place_args` while arguments to `exit_place_func_nb` can be passed either as `*args` or `exit_place_args` (but not both!).

**Usage**

  * Generate entry and exit signals one after another:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-1)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-2)... def place_func_nb(c):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-3)...     c.out[0] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-4)...     return 0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-6)>>> en, ex = vbt.pd_acc.signals.generate_both(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-7)...     (5, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-8)...     entry_place_func_nb=place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-9)...     exit_place_func_nb=place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-10)...     wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-11)...         index=mask.index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-12)...         columns=mask.columns
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-13)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-14)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-15)>>> en
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-16)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-17)2020-01-01   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-18)2020-01-02  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-19)2020-01-03   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-20)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-21)2020-01-05   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-22)>>> ex
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-23)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-24)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-25)2020-01-02   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-26)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-27)2020-01-04   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-27-28)2020-01-05  False  False  False
    

  * Generate three entries and one exit one after another:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-1)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-2)... def entry_place_func_nb(c, n):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-3)...     c.out[:n] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-4)...     return n - 1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-6)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-7)... def exit_place_func_nb(c, n):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-8)...     c.out[:n] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-9)...     return n - 1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-11)>>> en, ex = vbt.pd_acc.signals.generate_both(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-12)...     (5, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-13)...     entry_place_func_nb=entry_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-14)...     entry_place_args=(3,),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-15)...     exit_place_func_nb=exit_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-16)...     exit_place_args=(1,),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-17)...     wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-18)...         index=mask.index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-19)...         columns=mask.columns
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-20)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-21)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-22)>>> en
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-23)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-24)2020-01-01   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-25)2020-01-02   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-26)2020-01-03   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-27)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-28)2020-01-05   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-29)>>> ex
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-30)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-31)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-32)2020-01-02  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-33)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-34)2020-01-04   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-28-35)2020-01-05  False  False  False
    

* * *

### generate_exits method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L500-L575 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_exits "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-1)SignalsAccessor.generate_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-2)    exit_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-4)    exit_place_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-5)    wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-6)    until_next=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-7)    skip_until_exit=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-8)    broadcast_named_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-9)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-10)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-11)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-12)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-13)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-29-14))
    

See [generate_ex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_ex_nb "vectorbtpro.signals.nb.generate_ex_nb").

**Usage**

  * Generate an exit just before the next entry:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-1)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-2)... def exit_place_func_nb(c):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-3)...     c.out[-1] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-4)...     return len(c.out) - 1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-6)>>> mask.vbt.signals.generate_exits(exit_place_func_nb)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-7)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-8)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-9)2020-01-02  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-10)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-11)2020-01-04  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-30-12)2020-01-05   True  False   True
    

* * *

### generate_ohlc_stop_exits method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1182-L1552 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-1)SignalsAccessor.generate_ohlc_stop_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-2)    entry_price,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-3)    open=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-4)    high=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-5)    low=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-6)    close=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-7)    sl_stop=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-8)    tsl_th=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-9)    tsl_stop=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-10)    tp_stop=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-11)    reverse=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-12)    is_entry_open=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-13)    out_dict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-14)    entry_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-15)    exit_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-16)    until_next=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-17)    skip_until_exit=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-18)    chain=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-19)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-20)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-21)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-22)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-23)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-31-24))
    

Generate exits based on when the price hits (trailing) stop loss or take profit.

Use `out_dict` as a dict to pass `stop_price` and `stop_type` arrays. You can also set `out_dict` to {} to produce these arrays automatically and still have access to them.

For arguments, see [ohlc_stop_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.ohlc_stop_place_nb "vectorbtpro.signals.nb.ohlc_stop_place_nb"). If `chain` is True, uses [SignalsAccessor.generate_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_both "vectorbtpro.signals.accessors.SignalsAccessor.generate_both"). Otherwise, uses [SignalsAccessor.generate_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_exits").

All array-like arguments including stops and `out_dict` will broadcast using [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "vectorbtpro.base.reshaping.broadcast") and `broadcast_kwargs`.

For arguments, see [ohlc_stop_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.ohlc_stop_place_nb "vectorbtpro.signals.nb.ohlc_stop_place_nb").

Hint

Default arguments will generate an exit signal strictly between two entry signals. If both entry signals are too close to each other, no exit will be generated.

To ignore all entries that come between an entry and its exit, set `until_next` to False and `skip_until_exit` to True.

To remove all entries that come between an entry and its exit, set `chain` to True. This will return two arrays: new entries and exits.

**Usage**

  * Generate exits for TSL and TP of 10%:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-1)>>> price = pd.DataFrame({
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-2)...     'open': [10, 11, 12, 11, 10],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-3)...     'high': [11, 12, 13, 12, 11],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-4)...     'low': [9, 10, 11, 10, 9],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-5)...     'close': [10, 11, 12, 11, 10]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-6)... })
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-7)>>> out_dict = {}
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-8)>>> exits = mask.vbt.signals.generate_ohlc_stop_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-9)...     price["open"],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-10)...     price['open'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-11)...     price['high'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-12)...     price['low'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-13)...     price['close'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-14)...     tsl_stop=0.1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-15)...     tp_stop=0.1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-16)...     is_entry_open=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-17)...     out_dict=out_dict,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-18)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-19)>>> exits
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-20)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-21)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-22)2020-01-02   True   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-23)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-24)2020-01-04  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-25)2020-01-05  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-27)>>> out_dict['stop_price']
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-28)               a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-29)2020-01-01   NaN   NaN   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-30)2020-01-02  11.0  11.0   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-31)2020-01-03   NaN   NaN   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-32)2020-01-04   NaN  10.8  10.8
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-33)2020-01-05   NaN   NaN   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-34)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-35)>>> out_dict['stop_type'].vbt(mapping=vbt.sig_enums.StopType).apply_mapping()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-36)               a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-37)2020-01-01  None  None  None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-38)2020-01-02    TP    TP  None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-39)2020-01-03  None  None  None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-40)2020-01-04  None   TSL   TSL
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-32-41)2020-01-05  None  None  None
    

Notice how the first two entry signals in the third column have no exit signal - there is no room between them for an exit signal.

  * To find an exit for the first entry and ignore all entries that are in-between them, we can pass `until_next=False` and `skip_until_exit=True`:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-1)>>> out_dict = {}
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-2)>>> exits = mask.vbt.signals.generate_ohlc_stop_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-3)...     price['open'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-4)...     price['open'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-5)...     price['high'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-6)...     price['low'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-7)...     price['close'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-8)...     tsl_stop=0.1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-9)...     tp_stop=0.1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-10)...     is_entry_open=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-11)...     out_dict=out_dict,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-12)...     until_next=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-13)...     skip_until_exit=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-14)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-15)>>> exits
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-16)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-17)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-18)2020-01-02   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-19)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-20)2020-01-04  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-21)2020-01-05  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-22)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-23)>>> out_dict['stop_price']
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-24)               a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-25)2020-01-01   NaN   NaN   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-26)2020-01-02  11.0  11.0  11.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-27)2020-01-03   NaN   NaN   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-28)2020-01-04   NaN  10.8  10.8
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-29)2020-01-05   NaN   NaN   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-30)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-31)>>> out_dict['stop_type'].vbt(mapping=vbt.sig_enums.StopType).apply_mapping()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-32)               a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-33)2020-01-01  None  None  None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-34)2020-01-02    TP    TP    TP
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-35)2020-01-03  None  None  None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-36)2020-01-04  None   TSL   TSL
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-33-37)2020-01-05  None  None  None
    

Now, the first signal in the third column gets executed regardless of the entries that come next, which is very similar to the logic that is implemented in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals "vectorbtpro.portfolio.base.Portfolio.from_signals").

  * To automatically remove all ignored entry signals, pass `chain=True`. This will return a new entries array:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-1)>>> out_dict = {}
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-2)>>> new_entries, exits = mask.vbt.signals.generate_ohlc_stop_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-3)...     price['open'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-4)...     price['open'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-5)...     price['high'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-6)...     price['low'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-7)...     price['close'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-8)...     tsl_stop=0.1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-9)...     tp_stop=0.1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-10)...     is_entry_open=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-11)...     out_dict=out_dict,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-12)...     chain=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-13)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-14)>>> new_entries
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-15)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-16)2020-01-01   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-17)2020-01-02  False  False  False  << removed entry in the third column
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-18)2020-01-03  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-19)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-20)2020-01-05  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-21)>>> exits
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-22)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-23)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-24)2020-01-02   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-25)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-26)2020-01-04  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-34-27)2020-01-05  False  False  False
    

Warning

The last two examples above make entries dependent upon exits - this makes only sense if you have no other exit arrays to combine this stop exit array with.

  * Test multiple parameter combinations:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-1)>>> exits = mask.vbt.signals.generate_ohlc_stop_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-2)...     price['open'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-3)...     price['open'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-4)...     price['high'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-5)...     price['low'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-6)...     price['close'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-7)...     sl_stop=vbt.Param([False, 0.1]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-8)...     tsl_stop=vbt.Param([False, 0.1]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-9)...     is_entry_open=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-10)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-11)>>> exits
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-12)sl_stop     False                                       0.1                \
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-13)tsl_stop    False                  0.1                False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-14)                a      b      c      a      b      c      a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-15)2020-01-01  False  False  False  False  False  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-16)2020-01-02  False  False  False  False  False  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-17)2020-01-03  False  False  False  False  False  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-18)2020-01-04  False  False  False   True   True   True  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-19)2020-01-05  False  False  False  False  False  False   True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-21)sl_stop
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-22)tsl_stop      0.1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-23)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-24)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-25)2020-01-02  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-26)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-27)2020-01-04   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-35-28)2020-01-05  False  False  False
    

* * *

### generate_random class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L631-L749 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-1)SignalsAccessor.generate_random(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-3)    n=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-4)    prob=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-5)    pick_first=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-6)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-7)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-8)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-9)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-36-10))
    

Generate signals randomly.

`shape` can be a shape-like tuple or an instance of [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") (will be used as `wrapper`).

If `n` is set, uses [rand_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rand_place_nb "vectorbtpro.signals.nb.rand_place_nb"). If `prob` is set, uses [rand_by_prob_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rand_by_prob_place_nb "vectorbtpro.signals.nb.rand_by_prob_place_nb").

For arguments, see [SignalsAccessor.generate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate "vectorbtpro.signals.accessors.SignalsAccessor.generate").

`n` must be either a scalar or an array that will broadcast to the number of columns. `prob` must be either a single number or an array that will broadcast to match `shape`.

Specify `seed` to make output deterministic.

**Usage**

  * For each column, generate a variable number of signals:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-1)>>> vbt.pd_acc.signals.generate_random(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-2)...     (5, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-3)...     n=[0, 1, 2],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-4)...     seed=42,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-5)...     wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-6)...         index=mask.index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-7)...         columns=mask.columns
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-8)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-9)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-10)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-11)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-12)2020-01-02  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-13)2020-01-03  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-14)2020-01-04  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-37-15)2020-01-05  False  False   True
    

  * For each column and time step, pick a signal with 50% probability:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-1)>>> vbt.pd_acc.signals.generate_random(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-2)...     (5, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-3)...     prob=0.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-4)...     seed=42,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-5)...     wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-6)...         index=mask.index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-7)...         columns=mask.columns
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-8)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-9)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-10)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-11)2020-01-01   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-12)2020-01-02  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-13)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-14)2020-01-04  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-38-15)2020-01-05   True  False   True
    

* * *

### generate_random_both class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L751-L883 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random_both "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-1)SignalsAccessor.generate_random_both(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-3)    n=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-4)    entry_prob=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-5)    exit_prob=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-6)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-7)    entry_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-8)    exit_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-9)    entry_pick_first=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-10)    exit_pick_first=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-11)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-12)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-13)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-14)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-39-15))
    

Generate chain of entry and exit signals randomly.

`shape` can be a shape-like tuple or an instance of [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") (will be used as `wrapper`).

If `n` is set, uses [generate_rand_enex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_rand_enex_nb "vectorbtpro.signals.nb.generate_rand_enex_nb"). If `entry_prob` and `exit_prob` are set, uses [SignalsAccessor.generate_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_both "vectorbtpro.signals.accessors.SignalsAccessor.generate_both") with [rand_by_prob_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rand_by_prob_place_nb "vectorbtpro.signals.nb.rand_by_prob_place_nb").

**Usage**

  * For each column, generate two entries and exits randomly:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-1)>>> en, ex = vbt.pd_acc.signals.generate_random_both(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-2)...     (5, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-3)...     n=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-4)...     seed=42,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-5)...     wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-6)...         index=mask.index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-7)...         columns=mask.columns
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-8)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-9)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-10)>>> en
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-11)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-12)2020-01-01  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-13)2020-01-02   True   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-14)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-15)2020-01-04   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-16)2020-01-05  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-17)>>> ex
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-18)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-19)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-20)2020-01-02  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-21)2020-01-03   True   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-22)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-40-23)2020-01-05   True   True   True
    

  * For each column and time step, pick entry with 50% probability and exit right after:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-1)>>> en, ex = vbt.pd_acc.signals.generate_random_both(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-2)...     (5, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-3)...     entry_prob=0.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-4)...     exit_prob=1.,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-5)...     seed=42,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-6)...     wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-7)...         index=mask.index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-8)...         columns=mask.columns
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-9)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-10)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-11)>>> en
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-12)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-13)2020-01-01   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-14)2020-01-02  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-15)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-16)2020-01-04  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-17)2020-01-05   True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-18)>>> ex
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-19)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-20)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-21)2020-01-02   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-22)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-23)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-41-24)2020-01-05  False  False   True
    

* * *

### generate_random_exits method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L885-L985 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random_exits "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-1)SignalsAccessor.generate_random_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-2)    prob=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-3)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-4)    wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-5)    until_next=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-6)    skip_until_exit=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-7)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-8)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-9)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-10)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-11)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-42-12))
    

Generate exit signals randomly.

If `prob` is None, uses [rand_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rand_place_nb "vectorbtpro.signals.nb.rand_place_nb"). Otherwise, uses [rand_by_prob_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rand_by_prob_place_nb "vectorbtpro.signals.nb.rand_by_prob_place_nb").

Uses [SignalsAccessor.generate_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_exits").

Specify `seed` to make output deterministic.

**Usage**

  * After each entry in `mask`, generate exactly one exit:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-43-1)>>> mask.vbt.signals.generate_random_exits(seed=42)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-43-2)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-43-3)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-43-4)2020-01-02  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-43-5)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-43-6)2020-01-04   True   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-43-7)2020-01-05  False  False   True
    

  * After each entry in `mask` and at each time step, generate exit with 50% probability:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-44-1)>>> mask.vbt.signals.generate_random_exits(prob=0.5, seed=42)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-44-2)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-44-3)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-44-4)2020-01-02   True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-44-5)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-44-6)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-44-7)2020-01-05  False  False   True
    

* * *

### generate_stop_exits method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L989-L1180 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_stop_exits "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-1)SignalsAccessor.generate_stop_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-2)    entry_ts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-3)    ts=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-4)    follow_ts=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-5)    stop=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-6)    trailing=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-7)    out_dict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-8)    entry_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-9)    exit_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-10)    until_next=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-11)    skip_until_exit=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-12)    chain=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-13)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-14)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-15)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-16)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-17)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-45-18))
    

Generate exits based on when `ts` hits the stop.

For arguments, see [stop_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.stop_place_nb "vectorbtpro.signals.nb.stop_place_nb"). If `chain` is True, uses [SignalsAccessor.generate_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_both "vectorbtpro.signals.accessors.SignalsAccessor.generate_both"). Otherwise, uses [SignalsAccessor.generate_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_exits").

Use `out_dict` as a dict to pass `stop_ts` array. You can also set `out_dict` to {} to produce this array automatically and still have access to it.

All array-like arguments including stops and `out_dict` will broadcast using [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "vectorbtpro.base.reshaping.broadcast") and `broadcast_kwargs`.

Hint

Default arguments will generate an exit signal strictly between two entry signals. If both entry signals are too close to each other, no exit will be generated.

To ignore all entries that come between an entry and its exit, set `until_next` to False and `skip_until_exit` to True.

To remove all entries that come between an entry and its exit, set `chain` to True. This will return two arrays: new entries and exits.

**Usage**

  * Regular stop loss:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-1)>>> ts = pd.Series([1, 2, 3, 2, 1])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-3)>>> mask.vbt.signals.generate_stop_exits(ts, stop=-0.1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-4)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-5)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-6)2020-01-02  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-7)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-8)2020-01-04  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-46-9)2020-01-05  False  False  False
    

  * Trailing stop loss:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-47-1)>>> mask.vbt.signals.generate_stop_exits(ts, stop=-0.1, trailing=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-47-2)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-47-3)2020-01-01  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-47-4)2020-01-02  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-47-5)2020-01-03  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-47-6)2020-01-04   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-47-7)2020-01-05  False  False  False
    

  * Testing multiple take profit stops:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-48-1)>>> mask.vbt.signals.generate_stop_exits(ts, stop=vbt.Param([1.0, 1.5]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-48-2)stop                        1.0                  1.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-48-3)                a      b      c      a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-48-4)2020-01-01  False  False  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-48-5)2020-01-02   True   True  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-48-6)2020-01-03  False  False  False   True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-48-7)2020-01-04  False  False  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-48-8)2020-01-05  False  False  False  False  False  False
    

* * *

### get_relation_str method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1940-L1952 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.get_relation_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-49-1)SignalsAccessor.get_relation_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-49-2)    relation
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-49-3))
    

Get direction string for `relation`.

* * *

### index_from_unravel class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2123-L2141 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.index_from_unravel "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-50-1)SignalsAccessor.index_from_unravel(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-50-2)    range_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-50-3)    row_idxs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-50-4)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-50-5)    signal_index_type='range',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-50-6)    signal_index_name='signal'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-50-7))
    

Get index from an unraveling operation.

* * *

### index_mapped method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2539-L2549 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.index_mapped "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-51-1)SignalsAccessor.index_mapped(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-51-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-51-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-51-4))
    

Get a mapped array of indices.

See [GenericAccessor.to_mapped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_mapped "vectorbtpro.generic.accessors.GenericAccessor.to_mapped").

Only True values will be considered.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.metrics "Permanent link")

Metrics supported by [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor "vectorbtpro.signals.accessors.SignalsAccessor").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-4)        calc_func=<function SignalsAccessor.<lambda> at 0x17798ff60>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-10)        calc_func=<function SignalsAccessor.<lambda> at 0x1779b4040>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-16)        calc_func=<function SignalsAccessor.<lambda> at 0x1779b40e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-21)    total=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-22)        title='Total',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-23)        calc_func='total',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-24)        tags='signals'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-26)    rate=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-27)        title='Rate [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-28)        calc_func='rate',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-29)        post_calc_func=<function SignalsAccessor.<lambda> at 0x1779b4180>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-30)        tags='signals'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-31)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-32)    total_overlapping=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-33)        title='Total Overlapping',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-34)        calc_func=<function SignalsAccessor.<lambda> at 0x1779b4220>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-35)        check_silent_has_target=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-36)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-37)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-38)            'target'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-39)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-40)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-41)    overlapping_rate=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-42)        title='Overlapping Rate [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-43)        calc_func=<function SignalsAccessor.<lambda> at 0x1779b42c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-44)        post_calc_func=<function SignalsAccessor.<lambda> at 0x1779b4360>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-45)        check_silent_has_target=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-46)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-47)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-48)            'target'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-49)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-50)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-51)    first_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-52)        title='First Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-53)        calc_func='nth_index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-54)        n=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-55)        wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-56)            to_index=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-57)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-58)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-59)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-60)            'index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-61)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-62)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-63)    last_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-64)        title='Last Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-65)        calc_func='nth_index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-66)        n=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-67)        wrap_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-68)            to_index=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-69)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-70)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-71)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-72)            'index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-73)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-74)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-75)    norm_avg_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-76)        title='Norm Avg Index [-1, 1]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-77)        calc_func='norm_avg_index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-78)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-79)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-80)            'index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-81)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-82)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-83)    distance=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-84)        title=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-85)            template="f'Distance {self.get_relation_str(relation)} {target_name}' if target is not None else 'Distance'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-86)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-87)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-88)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-89)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-90)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-91)        calc_func='between_ranges.duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-92)        post_calc_func=<function SignalsAccessor.<lambda> at 0x1779b4400>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-93)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-94)        tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-95)            template="['signals', 'distance', 'target'] if target is not None else ['signals', 'distance']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-96)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-97)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-98)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-99)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-100)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-101)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-102)    total_partitions=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-103)        title='Total Partitions',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-104)        calc_func='total_partitions',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-105)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-106)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-107)            'partitions'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-108)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-109)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-110)    partition_rate=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-111)        title='Partition Rate [%]',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-112)        calc_func='partition_rate',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-113)        post_calc_func=<function SignalsAccessor.<lambda> at 0x1779b44a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-114)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-115)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-116)            'partitions'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-117)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-118)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-119)    partition_len=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-120)        title='Partition Length',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-121)        calc_func='partition_ranges.duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-122)        post_calc_func=<function SignalsAccessor.<lambda> at 0x1779b4540>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-123)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-124)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-125)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-126)            'partitions',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-127)            'distance'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-128)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-129)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-130)    partition_distance=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-131)        title='Partition Distance',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-132)        calc_func='between_partition_ranges.duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-133)        post_calc_func=<function SignalsAccessor.<lambda> at 0x1779b45e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-134)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-135)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-136)            'signals',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-137)            'partitions',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-138)            'distance'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-139)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-140)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-52-141))
    

Returns `SignalsAccessor._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `SignalsAccessor._metrics`.

* * *

### norm_avg_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2495-L2537 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.norm_avg_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-53-1)SignalsAccessor.norm_avg_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-53-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-53-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-53-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-53-5)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-53-6))
    

See [norm_avg_index_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.norm_avg_index_nb "vectorbtpro.signals.nb.norm_avg_index_nb").

Normalized average index measures the average signal location relative to the middle of the column. This way, we can quickly see where the majority of signals are located.

Common values are:

  * -1.0: only the first signal is set
  * 1.0: only the last signal is set
  * 0.0: symmetric distribution around the middle
  * [-1.0, 0.0): average signal is on the left
  * (0.0, 1.0]: average signal is on the right



**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-54-1)>>> pd.Series([True, False, False, False]).vbt.signals.norm_avg_index()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-54-2)-1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-54-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-54-4)>>> pd.Series([False, False, False, True]).vbt.signals.norm_avg_index()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-54-5)1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-54-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-54-7)>>> pd.Series([True, False, False, True]).vbt.signals.norm_avg_index()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-54-8)0.0
    

* * *

### nth method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1788-L1798 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-55-1)SignalsAccessor.nth(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-55-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-55-3)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-55-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-55-5))
    

Select signals that satisfy the condition `pos_rank == n`.

Uses [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank").

* * *

### nth_after method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1800-L1811 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth_after "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-56-1)SignalsAccessor.nth_after(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-56-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-56-3)    reset_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-56-4)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-56-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-56-6))
    

Select signals that satisfy the condition `pos_rank == n`.

Uses [SignalsAccessor.pos_rank_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after").

* * *

### nth_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2445-L2493 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-57-1)SignalsAccessor.nth_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-57-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-57-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-57-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-57-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-57-6)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-57-7))
    

See [nth_index_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.nth_index_nb "vectorbtpro.signals.nb.nth_index_nb").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-1)>>> mask.vbt.signals.nth_index(0)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-2)a   2020-01-01
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-3)b   2020-01-01
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-4)c   2020-01-01
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-5)Name: nth_index, dtype: datetime64[ns]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-7)>>> mask.vbt.signals.nth_index(2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-8)a          NaT
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-9)b   2020-01-05
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-10)c   2020-01-03
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-11)Name: nth_index, dtype: datetime64[ns]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-13)>>> mask.vbt.signals.nth_index(-1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-14)a   2020-01-01
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-15)b   2020-01-05
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-16)c   2020-01-03
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-17)Name: nth_index, dtype: datetime64[ns]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-18)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-19)>>> mask.vbt.signals.nth_index(-1, group_by=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-58-20)Timestamp('2020-01-05 00:00:00')
    

* * *

### partition_pos_rank method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1715-L1759 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-59-1)SignalsAccessor.partition_pos_rank(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-59-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-59-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-59-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-59-5))
    

Get partition position ranks.

Uses [SignalsAccessor.rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rank "vectorbtpro.signals.accessors.SignalsAccessor.rank") with [part_pos_rank_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.part_pos_rank_nb "vectorbtpro.signals.nb.part_pos_rank_nb").

**Usage**

  * Rank each partition of True values in `mask`:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-1)>>> mask.vbt.signals.partition_pos_rank()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-2)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-3)2020-01-01  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-4)2020-01-02 -1 -1  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-5)2020-01-03 -1  1  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-6)2020-01-04 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-7)2020-01-05 -1  2 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-9)>>> mask.vbt.signals.partition_pos_rank(after_false=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-10)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-11)2020-01-01 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-12)2020-01-02 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-13)2020-01-03 -1  0 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-14)2020-01-04 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-15)2020-01-05 -1  1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-16)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-17)>>> mask.vbt.signals.partition_pos_rank(reset_by=mask)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-18)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-19)2020-01-01  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-20)2020-01-02 -1 -1  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-21)2020-01-03 -1  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-22)2020-01-04 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-60-23)2020-01-05 -1  0 -1
    

* * *

### partition_pos_rank_after method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1761-L1763 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_after "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-61-1)SignalsAccessor.partition_pos_rank_after(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-61-2)    reset_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-61-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-61-4))
    

Get partition position ranks after each signal in `reset_by`.

* * *

### partition_pos_rank_mapped method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1869-L1873 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_mapped "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-62-1)SignalsAccessor.partition_pos_rank_mapped(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-62-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-62-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-62-4))
    

Get a mapped array of partition position ranks.

Uses [SignalsAccessor.partition_pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank").

* * *

### partition_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2068-L2094 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-63-1)SignalsAccessor.partition_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-63-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-63-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-63-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-63-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-63-6))
    

Wrap the result of [partition_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.partition_ranges_nb "vectorbtpro.signals.nb.partition_ranges_nb") with [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").

If `use_end_idxs` is True, uses the index of the last signal in each partition as `idx_arr`. Otherwise, uses the index of the first signal.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-64-1)>>> mask_sr = pd.Series([True, True, True, False, True, True])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-64-2)>>> mask_sr.vbt.signals.partition_ranges().readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-64-3)   Range Id  Column  Start Timestamp  End Timestamp  Status
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-64-4)0         0       0                0              3  Closed
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-64-5)1         1       0                4              5    Open
    

* * *

### partition_rate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2573-L2583 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_rate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-65-1)SignalsAccessor.partition_rate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-65-2)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-65-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-65-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-65-5))
    

[SignalsAccessor.total_partitions](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total_partitions "vectorbtpro.signals.accessors.SignalsAccessor.total_partitions") divided by [SignalsAccessor.total](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total "vectorbtpro.signals.accessors.SignalsAccessor.total") in each column/group.

* * *

### plot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2711-L2738 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-66-1)SignalsAccessor.plot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-66-2)    yref='y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-66-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-66-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-66-5))
    

Plot signals.

**Args**

**`yref`** : `str`
    Y coordinate axis.
**`column`** : `hashable`
    Column to plot.
**`**kwargs`**
    Keyword arguments passed to [GenericAccessor.lineplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.lineplot "vectorbtpro.generic.accessors.GenericAccessor.lineplot").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-67-1)>>> mask[['a', 'c']].vbt.signals.plot().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/signals_df_plot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/signals_df_plot.dark.svg#only-dark)

* * *

### plot_as_entries method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2813-L2842 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entries "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-68-1)SignalsAccessor.plot_as_entries(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-68-2)    y=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-68-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-68-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-68-5))
    

Plot signals as entry markers.

See [SignalsAccessor.plot_as_markers](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers "vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_markers").

* * *

### plot_as_entry_marks method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2875-L2908 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entry_marks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-69-1)SignalsAccessor.plot_as_entry_marks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-69-2)    y=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-69-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-69-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-69-5))
    

Plot signals as marked entry markers.

See [SignalsAccessor.plot_as_markers](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers "vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_markers").

* * *

### plot_as_exit_marks method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2910-L2943 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exit_marks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-70-1)SignalsAccessor.plot_as_exit_marks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-70-2)    y=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-70-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-70-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-70-5))
    

Plot signals as marked exit markers.

See [SignalsAccessor.plot_as_markers](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers "vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_markers").

* * *

### plot_as_exits method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2844-L2873 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exits "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-71-1)SignalsAccessor.plot_as_exits(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-71-2)    y=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-71-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-71-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-71-5))
    

Plot signals as exit markers.

See [SignalsAccessor.plot_as_markers](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers "vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_markers").

* * *

### plot_as_markers method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2740-L2811 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-72-1)SignalsAccessor.plot_as_markers(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-72-2)    y=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-72-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-72-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-72-5))
    

Plot Series as markers.

**Args**

**`y`** : `array_like`
    Y-axis values to plot markers on.
**`column`** : `hashable`
    Column to plot.
**`**kwargs`**
    Keyword arguments passed to [GenericAccessor.scatterplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.scatterplot "vectorbtpro.generic.accessors.GenericAccessor.scatterplot").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-73-1)>>> ts = pd.Series([1, 2, 3, 2, 1], index=mask.index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-73-2)>>> fig = ts.vbt.lineplot()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-73-3)>>> mask['b'].vbt.signals.plot_as_entries(y=ts, fig=fig)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-73-4)>>> (~mask['b']).vbt.signals.plot_as_exits(y=ts, fig=fig).show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/signals_plot_as_markers.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/signals_plot_as_markers.dark.svg#only-dark)

* * *

### plots_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2945-L2955 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plots_defaults "Permanent link")

Defaults for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.signals.accessors.SignalsAccessor.plots").

Merges [GenericAccessor.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plots_defaults "vectorbtpro.generic.accessors.GenericAccessor.plots_defaults") and `plots` from [signals](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.signals "vectorbtpro._settings.signals").

* * *

### pos_rank method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1638-L1700 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-74-1)SignalsAccessor.pos_rank(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-74-2)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-74-3)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-74-4)    allow_gaps=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-74-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-74-6))
    

Get signal position ranks.

Uses [SignalsAccessor.rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rank "vectorbtpro.signals.accessors.SignalsAccessor.rank") with [sig_pos_rank_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.sig_pos_rank_nb "vectorbtpro.signals.nb.sig_pos_rank_nb").

**Usage**

  * Rank each True value in each partition in `mask`:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-1)>>> mask.vbt.signals.pos_rank()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-2)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-3)2020-01-01  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-4)2020-01-02 -1 -1  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-5)2020-01-03 -1  0  2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-6)2020-01-04 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-7)2020-01-05 -1  0 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-9)>>> mask.vbt.signals.pos_rank(after_false=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-10)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-11)2020-01-01 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-12)2020-01-02 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-13)2020-01-03 -1  0 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-14)2020-01-04 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-15)2020-01-05 -1  0 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-16)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-17)>>> mask.vbt.signals.pos_rank(allow_gaps=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-18)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-19)2020-01-01  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-20)2020-01-02 -1 -1  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-21)2020-01-03 -1  1  2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-22)2020-01-04 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-23)2020-01-05 -1  2 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-24)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-25)>>> mask.vbt.signals.pos_rank(reset_by=~mask, allow_gaps=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-26)            a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-27)2020-01-01  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-28)2020-01-02 -1 -1  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-29)2020-01-03 -1  0  2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-30)2020-01-04 -1 -1 -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-75-31)2020-01-05 -1  0 -1
    

* * *

### pos_rank_after method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1702-L1713 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-76-1)SignalsAccessor.pos_rank_after(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-76-2)    reset_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-76-3)    after_reset=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-76-4)    allow_gaps=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-76-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-76-6))
    

Get signal position ranks after each signal in `reset_by`.

Note

`allow_gaps` is enabled by default.

* * *

### pos_rank_mapped method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1863-L1867 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_mapped "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-77-1)SignalsAccessor.pos_rank_mapped(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-77-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-77-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-77-4))
    

Get a mapped array of signal position ranks.

Uses [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank").

* * *

### rank method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1556-L1636 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rank "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-1)SignalsAccessor.rank(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-2)    rank_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-4)    rank_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-5)    reset_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-6)    after_false=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-7)    after_reset=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-8)    reset_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-9)    as_mapped=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-10)    broadcast_named_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-11)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-12)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-13)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-14)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-15)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-16)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-78-17))
    

See [rank_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rank_nb "vectorbtpro.signals.nb.rank_nb").

Arguments to `rank_func_nb` can be passed either as `*args` or `rank_args` (but not both!).

Will broadcast with `reset_by` using [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "vectorbtpro.base.reshaping.broadcast") and `broadcast_kwargs`.

Set `as_mapped` to True to return an instance of [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray").

* * *

### rate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2556-L2561 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-79-1)SignalsAccessor.rate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-79-2)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-79-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-79-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-79-5))
    

[SignalsAccessor.total](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total "vectorbtpro.signals.accessors.SignalsAccessor.total") divided by the total index length in each column/group.

* * *

### ravel method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2412-L2441 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.ravel "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-80-1)SignalsAccessor.ravel(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-80-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-80-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-80-4)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-80-5))
    

Ravel signals.

See [ravel_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.ravel_nb "vectorbtpro.signals.nb.ravel_nb").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-1)>>> unravel_mask = mask.vbt.signals.unravel()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-2)>>> original_mask = unravel_mask.vbt.signals.ravel(group_by=vbt.ExceptLevel("signal"))
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-3)>>> original_mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-4)                a      b      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-5)2020-01-01   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-6)2020-01-02  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-7)2020-01-03  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-8)2020-01-04  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-81-9)2020-01-05  False   True  False
    

* * *

### stats_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2587-L2597 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.stats_defaults "Permanent link")

Defaults for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.signals.accessors.SignalsAccessor.stats").

Merges [GenericAccessor.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.stats_defaults "vectorbtpro.generic.accessors.GenericAccessor.stats_defaults") and `stats` from [signals](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.signals "vectorbtpro._settings.signals").

* * *

### subplots property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.subplots "Permanent link")

Subplots supported by [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor "vectorbtpro.signals.accessors.SignalsAccessor").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-82-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-82-2)    plot=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-82-3)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-82-4)        plot_func='plot',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-82-5)        pass_trace_names=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-82-6)        tags='generic'
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-82-7)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-82-8))
    

Returns `SignalsAccessor._subplots`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `SignalsAccessor._subplots`.

* * *

### to_nth method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1838-L1848 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-83-1)SignalsAccessor.to_nth(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-83-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-83-3)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-83-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-83-5))
    

Select signals that satisfy the condition `pos_rank < n`.

Uses [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank").

* * *

### to_nth_after method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L1850-L1861 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth_after "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-84-1)SignalsAccessor.to_nth_after(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-84-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-84-3)    reset_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-84-4)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-84-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-84-6))
    

Select signals that satisfy the condition `pos_rank < n`.

Uses [SignalsAccessor.pos_rank_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after").

* * *

### total method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2551-L2554 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-85-1)SignalsAccessor.total(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-85-2)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-85-3)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-85-4))
    

Total number of True values in each column/group.

* * *

### total_partitions method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2563-L2571 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total_partitions "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-86-1)SignalsAccessor.total_partitions(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-86-2)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-86-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-86-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-86-5))
    

Total number of partitions of True values in each column/group.

* * *

### unravel method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2143-L2194 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.unravel "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-1)SignalsAccessor.unravel(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-2)    incl_empty_cols=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-3)    force_signal_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-4)    signal_index_type='range',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-5)    signal_index_name='signal',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-6)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-7)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-8)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-87-9))
    

Unravel signals.

See [unravel_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.unravel_nb "vectorbtpro.signals.nb.unravel_nb").

Argument `signal_index_type` takes the following values:

  * "range": Basic signal counter in a column
  * "position(s)": Integer position (row) of signal in a column
  * "label(s)": Label of signal in a column



**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-88-1)>>> mask.vbt.signals.unravel()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-88-2)signal          0      0      1      2      0      1      2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-88-3)                a      b      b      b      c      c      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-88-4)2020-01-01   True   True  False  False   True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-88-5)2020-01-02  False  False  False  False  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-88-6)2020-01-03  False  False   True  False  False  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-88-7)2020-01-04  False  False  False  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-88-8)2020-01-05  False  False  False   True  False  False  False
    

* * *

### unravel_between class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2196-L2410 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.unravel_between "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-1)SignalsAccessor.unravel_between(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-3)    relation='onemany',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-4)    incl_open_source=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-5)    incl_open_target=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-6)    incl_empty_cols=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-7)    broadcast_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-8)    force_signal_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-9)    signal_index_type='pair_range',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-10)    signal_index_name='signal',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-11)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-12)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-13)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-89-14))
    

Unravel signal pairs.

If one array is passed, see [unravel_between_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.unravel_between_nb "vectorbtpro.signals.nb.unravel_between_nb"). If two arrays are passed, see [unravel_between_two_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.unravel_between_two_nb "vectorbtpro.signals.nb.unravel_between_two_nb").

Argument `signal_index_type` takes the following values:

  * "pair_range": Basic pair counter in a column
  * "range": Basic signal counter in a column
  * "source_range": Basic signal counter in a source column
  * "target_range": Basic signal counter in a target column
  * "position(s)": Integer position (row) of signal in a column
  * "source_position(s)": Integer position (row) of signal in a source column
  * "target_position(s)": Integer position (row) of signal in a target column
  * "label(s)": Label of signal in a column
  * "source_label(s)": Label of signal in a source column
  * "target_label(s)": Label of signal in a target column



**Usage**

  * One mask:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-1)>>> mask.vbt.signals.unravel_between()
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-2)signal         -1      0      1      0      1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-3)                a      b      b      c      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-4)2020-01-01  False   True  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-5)2020-01-02  False  False  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-6)2020-01-03  False   True   True  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-7)2020-01-04  False  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-8)2020-01-05  False  False   True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-10)>>> mask.vbt.signals.unravel_between(signal_index_type="position")
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-11)source_signal     -1      0      2      0      1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-12)target_signal     -1      2      4      1      2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-13)                   a      b      b      c      c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-14)2020-01-01     False   True  False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-15)2020-01-02     False  False  False   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-16)2020-01-03     False   True   True  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-17)2020-01-04     False  False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-90-18)2020-01-05     False  False   True  False  False
    

  * Two masks:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-1)>>> source_mask = pd.Series([True, True, False, False, True, True])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-2)>>> target_mask = pd.Series([False, False, True, True, False, False])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-3)>>> new_source_mask, new_target_mask = vbt.pd_acc.signals.unravel_between(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-4)...     source_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-5)...     target_mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-7)>>> new_source_mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-8)signal      0      1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-9)0       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-10)1        True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-11)2       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-12)3       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-13)4       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-14)5       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-15)>>> new_target_mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-16)signal      0      1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-17)0       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-18)1       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-19)2        True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-20)3       False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-21)4       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-22)5       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-23)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-24)>>> new_source_mask, new_target_mask = vbt.pd_acc.signals.unravel_between(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-25)...     source_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-26)...     target_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-27)...     relation="chain"
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-28)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-29)>>> new_source_mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-30)signal      0      1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-31)0        True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-32)1       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-33)2       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-34)3       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-35)4       False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-36)5       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-37)>>> new_target_mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-38)signal      0      1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-39)0       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-40)1       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-41)2        True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-42)3       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-43)4       False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-91-44)5       False  False
    

* * *

## SignalsDFAccessor class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2985-L3001 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsDFAccessor "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-92-1)SignalsDFAccessor(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-92-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-92-3)    obj=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-92-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-92-5))
    

Accessor on top of signal series. For DataFrames only.

Accessible via `pd.DataFrame.vbt.signals`.

**Superclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [BaseAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor "vectorbtpro.base.accessors.BaseAccessor")
  * [BaseDFAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseDFAccessor "vectorbtpro.base.accessors.BaseDFAccessor")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor "vectorbtpro.generic.accessors.GenericAccessor")
  * [GenericDFAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor "vectorbtpro.generic.accessors.GenericDFAccessor")
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
  * [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor "vectorbtpro.signals.accessors.SignalsAccessor")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.signals.accessors.SignalsAccessor.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.signals.accessors.SignalsAccessor.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.signals.accessors.SignalsAccessor.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.signals.accessors.SignalsAccessor.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.signals.accessors.SignalsAccessor.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.signals.accessors.SignalsAccessor.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.signals.accessors.SignalsAccessor.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.signals.accessors.SignalsAccessor.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.signals.accessors.SignalsAccessor.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.signals.accessors.SignalsAccessor.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.signals.accessors.SignalsAccessor.find_messages")
  * [BaseAccessor.align](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.align "vectorbtpro.signals.accessors.SignalsAccessor.align")
  * [BaseAccessor.align_to](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.align_to "vectorbtpro.signals.accessors.SignalsAccessor.align_to")
  * [BaseAccessor.apply](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply "vectorbtpro.signals.accessors.SignalsAccessor.apply")
  * [BaseAccessor.apply_and_concat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply_and_concat "vectorbtpro.signals.accessors.SignalsAccessor.apply_and_concat")
  * [BaseAccessor.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply_to_index "vectorbtpro.signals.accessors.SignalsAccessor.apply_to_index")
  * [BaseAccessor.broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast "vectorbtpro.signals.accessors.SignalsAccessor.broadcast")
  * [BaseAccessor.broadcast_combs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast_combs "vectorbtpro.signals.accessors.SignalsAccessor.broadcast_combs")
  * [BaseAccessor.broadcast_to](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast_to "vectorbtpro.signals.accessors.SignalsAccessor.broadcast_to")
  * [BaseAccessor.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.column_stack "vectorbtpro.signals.accessors.SignalsAccessor.column_stack")
  * [BaseAccessor.combine](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.combine "vectorbtpro.signals.accessors.SignalsAccessor.combine")
  * [BaseAccessor.concat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.concat "vectorbtpro.signals.accessors.SignalsAccessor.concat")
  * [BaseAccessor.cross](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.cross "vectorbtpro.signals.accessors.SignalsAccessor.cross")
  * [BaseAccessor.cross](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.x "vectorbtpro.signals.accessors.SignalsAccessor.x")
  * [BaseAccessor.cross_with](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.cross_with "vectorbtpro.signals.accessors.SignalsAccessor.cross_with")
  * [BaseAccessor.eval](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.eval "vectorbtpro.signals.accessors.SignalsAccessor.eval")
  * [BaseAccessor.get](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.get "vectorbtpro.signals.accessors.SignalsAccessor.get")
  * [BaseAccessor.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.indexing_func "vectorbtpro.signals.accessors.SignalsAccessor.indexing_func")
  * [BaseAccessor.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.indexing_setter_func "vectorbtpro.signals.accessors.SignalsAccessor.indexing_setter_func")
  * [BaseAccessor.is_frame](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.is_frame "vectorbtpro.signals.accessors.SignalsAccessor.is_frame")
  * [BaseAccessor.is_series](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.is_series "vectorbtpro.signals.accessors.SignalsAccessor.is_series")
  * [BaseAccessor.make_symmetric](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.make_symmetric "vectorbtpro.signals.accessors.SignalsAccessor.make_symmetric")
  * [BaseAccessor.repeat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.repeat "vectorbtpro.signals.accessors.SignalsAccessor.repeat")
  * [BaseAccessor.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_column_stack_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.resolve_column_stack_kwargs")
  * [BaseAccessor.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_row_stack_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.resolve_row_stack_kwargs")
  * [BaseAccessor.resolve_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_shape "vectorbtpro.signals.accessors.SignalsAccessor.resolve_shape")
  * [BaseAccessor.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.row_stack "vectorbtpro.signals.accessors.SignalsAccessor.row_stack")
  * [BaseAccessor.set](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set "vectorbtpro.signals.accessors.SignalsAccessor.set")
  * [BaseAccessor.set_between](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set_between "vectorbtpro.signals.accessors.SignalsAccessor.set_between")
  * [BaseAccessor.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.signals.accessors.SignalsAccessor.should_wrap")
  * [BaseAccessor.tile](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.tile "vectorbtpro.signals.accessors.SignalsAccessor.tile")
  * [BaseAccessor.to_1d_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_1d_array "vectorbtpro.signals.accessors.SignalsAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_2d_array "vectorbtpro.signals.accessors.SignalsAccessor.to_2d_array")
  * [BaseAccessor.to_data](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_data "vectorbtpro.signals.accessors.SignalsAccessor.to_data")
  * [BaseAccessor.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_dict "vectorbtpro.signals.accessors.SignalsAccessor.to_dict")
  * [BaseAccessor.unstack_to_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.unstack_to_array "vectorbtpro.signals.accessors.SignalsAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.unstack_to_df "vectorbtpro.signals.accessors.SignalsAccessor.unstack_to_df")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.signals.accessors.SignalsAccessor.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.signals.accessors.SignalsAccessor.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.signals.accessors.SignalsAccessor.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.signals.accessors.SignalsAccessor.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.signals.accessors.SignalsAccessor.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.signals.accessors.SignalsAccessor.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.signals.accessors.SignalsAccessor.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.signals.accessors.SignalsAccessor.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.signals.accessors.SignalsAccessor.update_config")
  * [GenericAccessor.ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ago "vectorbtpro.generic.accessors.GenericDFAccessor.ago")
  * [GenericAccessor.all_ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.all_ago "vectorbtpro.signals.accessors.SignalsAccessor.all_ago")
  * [GenericAccessor.any_ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.any_ago "vectorbtpro.signals.accessors.SignalsAccessor.any_ago")
  * [GenericAccessor.apply_along_axis](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_along_axis "vectorbtpro.signals.accessors.SignalsAccessor.apply_along_axis")
  * [GenericAccessor.apply_and_reduce](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_and_reduce "vectorbtpro.signals.accessors.SignalsAccessor.apply_and_reduce")
  * [GenericAccessor.apply_mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_mapping "vectorbtpro.signals.accessors.SignalsAccessor.apply_mapping")
  * [GenericAccessor.areaplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.areaplot "vectorbtpro.signals.accessors.SignalsAccessor.areaplot")
  * [GenericAccessor.barplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.barplot "vectorbtpro.signals.accessors.SignalsAccessor.barplot")
  * [GenericAccessor.bfill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.bfill "vectorbtpro.signals.accessors.SignalsAccessor.bfill")
  * [GenericAccessor.binarize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.binarize "vectorbtpro.signals.accessors.SignalsAccessor.binarize")
  * [GenericAccessor.boxplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.boxplot "vectorbtpro.signals.accessors.SignalsAccessor.boxplot")
  * [GenericAccessor.bshift](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.bshift "vectorbtpro.generic.accessors.GenericDFAccessor.bshift")
  * [GenericAccessor.column_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.column_apply "vectorbtpro.signals.accessors.SignalsAccessor.column_apply")
  * [GenericAccessor.corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.corr "vectorbtpro.signals.accessors.SignalsAccessor.corr")
  * [GenericAccessor.count](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.count "vectorbtpro.signals.accessors.SignalsAccessor.count")
  * [GenericAccessor.cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cov "vectorbtpro.signals.accessors.SignalsAccessor.cov")
  * [GenericAccessor.crossed_above](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_above "vectorbtpro.signals.accessors.SignalsAccessor.crossed_above")
  * [GenericAccessor.crossed_below](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_below "vectorbtpro.signals.accessors.SignalsAccessor.crossed_below")
  * [GenericAccessor.cumprod](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cumprod "vectorbtpro.signals.accessors.SignalsAccessor.cumprod")
  * [GenericAccessor.cumsum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cumsum "vectorbtpro.signals.accessors.SignalsAccessor.cumsum")
  * [GenericAccessor.demean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.demean "vectorbtpro.signals.accessors.SignalsAccessor.demean")
  * [GenericAccessor.describe](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.describe "vectorbtpro.signals.accessors.SignalsAccessor.describe")
  * [GenericAccessor.diff](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.diff "vectorbtpro.signals.accessors.SignalsAccessor.diff")
  * [GenericAccessor.digitize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.digitize "vectorbtpro.signals.accessors.SignalsAccessor.digitize")
  * [GenericAccessor.drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.drawdown "vectorbtpro.signals.accessors.SignalsAccessor.drawdown")
  * [GenericAccessor.ewm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ewm_mean "vectorbtpro.signals.accessors.SignalsAccessor.ewm_mean")
  * [GenericAccessor.ewm_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ewm_std "vectorbtpro.signals.accessors.SignalsAccessor.ewm_std")
  * [GenericAccessor.expanding_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_apply "vectorbtpro.signals.accessors.SignalsAccessor.expanding_apply")
  * [GenericAccessor.expanding_corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_corr "vectorbtpro.signals.accessors.SignalsAccessor.expanding_corr")
  * [GenericAccessor.expanding_cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_cov "vectorbtpro.signals.accessors.SignalsAccessor.expanding_cov")
  * [GenericAccessor.expanding_idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_idxmax "vectorbtpro.signals.accessors.SignalsAccessor.expanding_idxmax")
  * [GenericAccessor.expanding_idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_idxmin "vectorbtpro.signals.accessors.SignalsAccessor.expanding_idxmin")
  * [GenericAccessor.expanding_max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_max "vectorbtpro.signals.accessors.SignalsAccessor.expanding_max")
  * [GenericAccessor.expanding_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_mean "vectorbtpro.signals.accessors.SignalsAccessor.expanding_mean")
  * [GenericAccessor.expanding_min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_min "vectorbtpro.signals.accessors.SignalsAccessor.expanding_min")
  * [GenericAccessor.expanding_ols](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_ols "vectorbtpro.signals.accessors.SignalsAccessor.expanding_ols")
  * [GenericAccessor.expanding_rank](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_rank "vectorbtpro.signals.accessors.SignalsAccessor.expanding_rank")
  * [GenericAccessor.expanding_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_std "vectorbtpro.signals.accessors.SignalsAccessor.expanding_std")
  * [GenericAccessor.expanding_zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_zscore "vectorbtpro.signals.accessors.SignalsAccessor.expanding_zscore")
  * [GenericAccessor.fbfill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fbfill "vectorbtpro.signals.accessors.SignalsAccessor.fbfill")
  * [GenericAccessor.ffill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ffill "vectorbtpro.signals.accessors.SignalsAccessor.ffill")
  * [GenericAccessor.fillna](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fillna "vectorbtpro.signals.accessors.SignalsAccessor.fillna")
  * [GenericAccessor.find_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.find_pattern "vectorbtpro.signals.accessors.SignalsAccessor.find_pattern")
  * [GenericAccessor.flatten_grouped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.flatten_grouped "vectorbtpro.signals.accessors.SignalsAccessor.flatten_grouped")
  * [GenericAccessor.fshift](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fshift "vectorbtpro.generic.accessors.GenericDFAccessor.fshift")
  * [GenericAccessor.get_drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.get_drawdowns "vectorbtpro.signals.accessors.SignalsAccessor.get_drawdowns")
  * [GenericAccessor.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.get_ranges "vectorbtpro.signals.accessors.SignalsAccessor.get_ranges")
  * [GenericAccessor.groupby_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_apply "vectorbtpro.signals.accessors.SignalsAccessor.groupby_apply")
  * [GenericAccessor.groupby_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_transform "vectorbtpro.signals.accessors.SignalsAccessor.groupby_transform")
  * [GenericAccessor.heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.heatmap "vectorbtpro.signals.accessors.SignalsAccessor.heatmap")
  * [GenericAccessor.histplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.histplot "vectorbtpro.signals.accessors.SignalsAccessor.histplot")
  * [GenericAccessor.idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.idxmax "vectorbtpro.signals.accessors.SignalsAccessor.idxmax")
  * [GenericAccessor.idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.idxmin "vectorbtpro.signals.accessors.SignalsAccessor.idxmin")
  * [GenericAccessor.lineplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.lineplot "vectorbtpro.signals.accessors.SignalsAccessor.lineplot")
  * [GenericAccessor.ma](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ma "vectorbtpro.signals.accessors.SignalsAccessor.ma")
  * [GenericAccessor.map](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.map "vectorbtpro.signals.accessors.SignalsAccessor.map")
  * [GenericAccessor.max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.max "vectorbtpro.signals.accessors.SignalsAccessor.max")
  * [GenericAccessor.maxabs_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.maxabs_scale "vectorbtpro.signals.accessors.SignalsAccessor.maxabs_scale")
  * [GenericAccessor.mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.mean "vectorbtpro.signals.accessors.SignalsAccessor.mean")
  * [GenericAccessor.median](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.median "vectorbtpro.signals.accessors.SignalsAccessor.median")
  * [GenericAccessor.min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.min "vectorbtpro.signals.accessors.SignalsAccessor.min")
  * [GenericAccessor.minmax_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.minmax_scale "vectorbtpro.signals.accessors.SignalsAccessor.minmax_scale")
  * [GenericAccessor.msd](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.msd "vectorbtpro.signals.accessors.SignalsAccessor.msd")
  * [GenericAccessor.normalize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.normalize "vectorbtpro.signals.accessors.SignalsAccessor.normalize")
  * [GenericAccessor.overlay_with_heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.overlay_with_heatmap "vectorbtpro.signals.accessors.SignalsAccessor.overlay_with_heatmap")
  * [GenericAccessor.pct_change](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.pct_change "vectorbtpro.signals.accessors.SignalsAccessor.pct_change")
  * [GenericAccessor.plot_against](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot_against "vectorbtpro.signals.accessors.SignalsAccessor.plot_against")
  * [GenericAccessor.plot_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot_pattern "vectorbtpro.signals.accessors.SignalsAccessor.plot_pattern")
  * [GenericAccessor.power_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.power_transform "vectorbtpro.signals.accessors.SignalsAccessor.power_transform")
  * [GenericAccessor.product](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.product "vectorbtpro.signals.accessors.SignalsAccessor.product")
  * [GenericAccessor.proximity_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.proximity_apply "vectorbtpro.signals.accessors.SignalsAccessor.proximity_apply")
  * [GenericAccessor.qqplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.qqplot "vectorbtpro.signals.accessors.SignalsAccessor.qqplot")
  * [GenericAccessor.quantile_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.quantile_transform "vectorbtpro.signals.accessors.SignalsAccessor.quantile_transform")
  * [GenericAccessor.realign](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign "vectorbtpro.generic.accessors.GenericDFAccessor.realign")
  * [GenericAccessor.realign_closing](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_closing "vectorbtpro.signals.accessors.SignalsAccessor.realign_closing")
  * [GenericAccessor.realign_opening](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_opening "vectorbtpro.signals.accessors.SignalsAccessor.realign_opening")
  * [GenericAccessor.rebase](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rebase "vectorbtpro.signals.accessors.SignalsAccessor.rebase")
  * [GenericAccessor.reduce](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.reduce "vectorbtpro.signals.accessors.SignalsAccessor.reduce")
  * [GenericAccessor.resample_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_apply "vectorbtpro.signals.accessors.SignalsAccessor.resample_apply")
  * [GenericAccessor.resample_between_bounds](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_between_bounds "vectorbtpro.signals.accessors.SignalsAccessor.resample_between_bounds")
  * [GenericAccessor.resample_to_index](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_to_index "vectorbtpro.signals.accessors.SignalsAccessor.resample_to_index")
  * [GenericAccessor.resolve_mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resolve_mapping "vectorbtpro.signals.accessors.SignalsAccessor.resolve_mapping")
  * [GenericAccessor.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resolve_self "vectorbtpro.signals.accessors.SignalsAccessor.resolve_self")
  * [GenericAccessor.robust_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.robust_scale "vectorbtpro.signals.accessors.SignalsAccessor.robust_scale")
  * [GenericAccessor.rolling_all](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_all "vectorbtpro.signals.accessors.SignalsAccessor.rolling_all")
  * [GenericAccessor.rolling_any](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_any "vectorbtpro.signals.accessors.SignalsAccessor.rolling_any")
  * [GenericAccessor.rolling_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_apply "vectorbtpro.signals.accessors.SignalsAccessor.rolling_apply")
  * [GenericAccessor.rolling_corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_corr "vectorbtpro.signals.accessors.SignalsAccessor.rolling_corr")
  * [GenericAccessor.rolling_cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_cov "vectorbtpro.signals.accessors.SignalsAccessor.rolling_cov")
  * [GenericAccessor.rolling_idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_idxmax "vectorbtpro.signals.accessors.SignalsAccessor.rolling_idxmax")
  * [GenericAccessor.rolling_idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_idxmin "vectorbtpro.signals.accessors.SignalsAccessor.rolling_idxmin")
  * [GenericAccessor.rolling_max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_max "vectorbtpro.signals.accessors.SignalsAccessor.rolling_max")
  * [GenericAccessor.rolling_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_mean "vectorbtpro.signals.accessors.SignalsAccessor.rolling_mean")
  * [GenericAccessor.rolling_min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_min "vectorbtpro.signals.accessors.SignalsAccessor.rolling_min")
  * [GenericAccessor.rolling_ols](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_ols "vectorbtpro.signals.accessors.SignalsAccessor.rolling_ols")
  * [GenericAccessor.rolling_pattern_similarity](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_pattern_similarity "vectorbtpro.signals.accessors.SignalsAccessor.rolling_pattern_similarity")
  * [GenericAccessor.rolling_prod](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_prod "vectorbtpro.signals.accessors.SignalsAccessor.rolling_prod")
  * [GenericAccessor.rolling_rank](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_rank "vectorbtpro.signals.accessors.SignalsAccessor.rolling_rank")
  * [GenericAccessor.rolling_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_std "vectorbtpro.signals.accessors.SignalsAccessor.rolling_std")
  * [GenericAccessor.rolling_sum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_sum "vectorbtpro.signals.accessors.SignalsAccessor.rolling_sum")
  * [GenericAccessor.rolling_zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_zscore "vectorbtpro.signals.accessors.SignalsAccessor.rolling_zscore")
  * [GenericAccessor.row_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.row_apply "vectorbtpro.signals.accessors.SignalsAccessor.row_apply")
  * [GenericAccessor.scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.scale "vectorbtpro.signals.accessors.SignalsAccessor.scale")
  * [GenericAccessor.scatterplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.scatterplot "vectorbtpro.signals.accessors.SignalsAccessor.scatterplot")
  * [GenericAccessor.shuffle](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.shuffle "vectorbtpro.signals.accessors.SignalsAccessor.shuffle")
  * [GenericAccessor.squeeze_grouped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.squeeze_grouped "vectorbtpro.signals.accessors.SignalsAccessor.squeeze_grouped")
  * [GenericAccessor.std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.std "vectorbtpro.signals.accessors.SignalsAccessor.std")
  * [GenericAccessor.sum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.sum "vectorbtpro.signals.accessors.SignalsAccessor.sum")
  * [GenericAccessor.to_daily_log_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_daily_log_returns "vectorbtpro.signals.accessors.SignalsAccessor.to_daily_log_returns")
  * [GenericAccessor.to_daily_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_daily_returns "vectorbtpro.signals.accessors.SignalsAccessor.to_daily_returns")
  * [GenericAccessor.to_log_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_log_returns "vectorbtpro.signals.accessors.SignalsAccessor.to_log_returns")
  * [GenericAccessor.to_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_returns "vectorbtpro.signals.accessors.SignalsAccessor.to_returns")
  * [GenericAccessor.transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.transform "vectorbtpro.signals.accessors.SignalsAccessor.transform")
  * [GenericAccessor.ts_heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ts_heatmap "vectorbtpro.signals.accessors.SignalsAccessor.ts_heatmap")
  * [GenericAccessor.value_counts](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.value_counts "vectorbtpro.signals.accessors.SignalsAccessor.value_counts")
  * [GenericAccessor.vidya](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.vidya "vectorbtpro.signals.accessors.SignalsAccessor.vidya")
  * [GenericAccessor.volume](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.volume "vectorbtpro.signals.accessors.SignalsAccessor.volume")
  * [GenericAccessor.wm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wm_mean "vectorbtpro.signals.accessors.SignalsAccessor.wm_mean")
  * [GenericAccessor.wwm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wwm_mean "vectorbtpro.signals.accessors.SignalsAccessor.wwm_mean")
  * [GenericAccessor.wwm_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wwm_std "vectorbtpro.signals.accessors.SignalsAccessor.wwm_std")
  * [GenericAccessor.zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.zscore "vectorbtpro.signals.accessors.SignalsAccessor.zscore")
  * [GenericDFAccessor.band](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.band "vectorbtpro.generic.accessors.GenericDFAccessor.band")
  * [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections "vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.signals.accessors.SignalsAccessor.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.signals.accessors.SignalsAccessor.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.signals.accessors.SignalsAccessor.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.signals.accessors.SignalsAccessor.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.signals.accessors.SignalsAccessor.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.signals.accessors.SignalsAccessor.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.signals.accessors.SignalsAccessor.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.signals.accessors.SignalsAccessor.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.signals.accessors.SignalsAccessor.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.signals.accessors.SignalsAccessor.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.signals.accessors.SignalsAccessor.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.signals.accessors.SignalsAccessor.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.signals.accessors.SignalsAccessor.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.signals.accessors.SignalsAccessor.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.signals.accessors.SignalsAccessor.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.signals.accessors.SignalsAccessor.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.signals.accessors.SignalsAccessor.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.signals.accessors.SignalsAccessor.select_col_from_obj")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.signals.accessors.SignalsAccessor.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.signals.accessors.SignalsAccessor.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.signals.accessors.SignalsAccessor.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.signals.accessors.SignalsAccessor.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.signals.accessors.SignalsAccessor.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.signals.accessors.SignalsAccessor.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.signals.accessors.SignalsAccessor.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.signals.accessors.SignalsAccessor.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.signals.accessors.SignalsAccessor.select_levels")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.signals.accessors.SignalsAccessor.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.signals.accessors.SignalsAccessor.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.signals.accessors.SignalsAccessor.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.signals.accessors.SignalsAccessor.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.signals.accessors.SignalsAccessor.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.signals.accessors.SignalsAccessor.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.signals.accessors.SignalsAccessor.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.signals.accessors.SignalsAccessor.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.signals.accessors.SignalsAccessor.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.signals.accessors.SignalsAccessor.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.signals.accessors.SignalsAccessor.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.signals.accessors.SignalsAccessor.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.signals.accessors.SignalsAccessor.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.signals.accessors.SignalsAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.signals.accessors.SignalsAccessor.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.signals.accessors.SignalsAccessor.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.signals.accessors.SignalsAccessor.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.signals.accessors.SignalsAccessor.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.signals.accessors.SignalsAccessor.pprint")
  * [SignalsAccessor.between_partition_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_partition_ranges "vectorbtpro.signals.accessors.SignalsAccessor.between_partition_ranges")
  * [SignalsAccessor.between_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_ranges "vectorbtpro.signals.accessors.SignalsAccessor.between_ranges")
  * [SignalsAccessor.clean](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.clean "vectorbtpro.signals.accessors.SignalsAccessor.clean")
  * [SignalsAccessor.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.signals.accessors.SignalsAccessor.cls_dir")
  * [SignalsAccessor.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.signals.accessors.SignalsAccessor.column_only_select")
  * [SignalsAccessor.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.signals.accessors.SignalsAccessor.config")
  * [SignalsAccessor.delta_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.delta_ranges "vectorbtpro.signals.accessors.SignalsAccessor.delta_ranges")
  * [SignalsAccessor.df_accessor_cls](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.df_accessor_cls "vectorbtpro.signals.accessors.SignalsAccessor.df_accessor_cls")
  * [SignalsAccessor.distance_from_last](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.distance_from_last "vectorbtpro.signals.accessors.SignalsAccessor.distance_from_last")
  * [SignalsAccessor.drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.drawdowns "vectorbtpro.signals.accessors.SignalsAccessor.drawdowns")
  * [SignalsAccessor.empty](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.empty "vectorbtpro.signals.accessors.SignalsAccessor.empty")
  * [SignalsAccessor.empty_like](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.empty_like "vectorbtpro.signals.accessors.SignalsAccessor.empty_like")
  * [SignalsAccessor.first](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first "vectorbtpro.signals.accessors.SignalsAccessor.first")
  * [SignalsAccessor.first_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first_after "vectorbtpro.signals.accessors.SignalsAccessor.first_after")
  * [SignalsAccessor.from_nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.from_nth "vectorbtpro.signals.accessors.SignalsAccessor.from_nth")
  * [SignalsAccessor.from_nth_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.from_nth_after "vectorbtpro.signals.accessors.SignalsAccessor.from_nth_after")
  * [SignalsAccessor.generate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate "vectorbtpro.signals.accessors.SignalsAccessor.generate")
  * [SignalsAccessor.generate_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_both "vectorbtpro.signals.accessors.SignalsAccessor.generate_both")
  * [SignalsAccessor.generate_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_exits")
  * [SignalsAccessor.generate_ohlc_stop_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits")
  * [SignalsAccessor.generate_random](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random "vectorbtpro.signals.accessors.SignalsAccessor.generate_random")
  * [SignalsAccessor.generate_random_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random_both "vectorbtpro.signals.accessors.SignalsAccessor.generate_random_both")
  * [SignalsAccessor.generate_random_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_random_exits")
  * [SignalsAccessor.generate_stop_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_stop_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_stop_exits")
  * [SignalsAccessor.get_relation_str](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.get_relation_str "vectorbtpro.signals.accessors.SignalsAccessor.get_relation_str")
  * [SignalsAccessor.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.signals.accessors.SignalsAccessor.group_select")
  * [SignalsAccessor.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.signals.accessors.SignalsAccessor.iloc")
  * [SignalsAccessor.index_from_unravel](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.index_from_unravel "vectorbtpro.signals.accessors.SignalsAccessor.index_from_unravel")
  * [SignalsAccessor.index_mapped](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.index_mapped "vectorbtpro.signals.accessors.SignalsAccessor.index_mapped")
  * [SignalsAccessor.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.indexing_kwargs")
  * [SignalsAccessor.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.signals.accessors.SignalsAccessor.loc")
  * [SignalsAccessor.mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.mapping "vectorbtpro.signals.accessors.SignalsAccessor.mapping")
  * [SignalsAccessor.ndim](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.ndim "vectorbtpro.signals.accessors.SignalsAccessor.ndim")
  * [SignalsAccessor.norm_avg_index](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.norm_avg_index "vectorbtpro.signals.accessors.SignalsAccessor.norm_avg_index")
  * [SignalsAccessor.nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth "vectorbtpro.signals.accessors.SignalsAccessor.nth")
  * [SignalsAccessor.nth_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth_after "vectorbtpro.signals.accessors.SignalsAccessor.nth_after")
  * [SignalsAccessor.nth_index](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth_index "vectorbtpro.signals.accessors.SignalsAccessor.nth_index")
  * [SignalsAccessor.obj](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.obj "vectorbtpro.signals.accessors.SignalsAccessor.obj")
  * [SignalsAccessor.partition_pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank")
  * [SignalsAccessor.partition_pos_rank_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_after "vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_after")
  * [SignalsAccessor.partition_pos_rank_mapped](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_mapped "vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_mapped")
  * [SignalsAccessor.partition_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_ranges "vectorbtpro.signals.accessors.SignalsAccessor.partition_ranges")
  * [SignalsAccessor.partition_rate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_rate "vectorbtpro.signals.accessors.SignalsAccessor.partition_rate")
  * [SignalsAccessor.plot](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot "vectorbtpro.signals.accessors.SignalsAccessor.plot")
  * [SignalsAccessor.plot_as_entries](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entries "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entries")
  * [SignalsAccessor.plot_as_entry_marks](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entry_marks "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entry_marks")
  * [SignalsAccessor.plot_as_exit_marks](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exit_marks "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exit_marks")
  * [SignalsAccessor.plot_as_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exits "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exits")
  * [SignalsAccessor.plot_as_markers](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers")
  * [SignalsAccessor.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plots_defaults "vectorbtpro.signals.accessors.SignalsAccessor.plots_defaults")
  * [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank")
  * [SignalsAccessor.pos_rank_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after")
  * [SignalsAccessor.pos_rank_mapped](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_mapped "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_mapped")
  * [SignalsAccessor.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.signals.accessors.SignalsAccessor.range_only_select")
  * [SignalsAccessor.ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ranges "vectorbtpro.signals.accessors.SignalsAccessor.ranges")
  * [SignalsAccessor.rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rank "vectorbtpro.signals.accessors.SignalsAccessor.rank")
  * [SignalsAccessor.rate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rate "vectorbtpro.signals.accessors.SignalsAccessor.rate")
  * [SignalsAccessor.ravel](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.ravel "vectorbtpro.signals.accessors.SignalsAccessor.ravel")
  * [SignalsAccessor.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.signals.accessors.SignalsAccessor.rec_state")
  * [SignalsAccessor.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.signals.accessors.SignalsAccessor.self_aliases")
  * [SignalsAccessor.sr_accessor_cls](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.sr_accessor_cls "vectorbtpro.signals.accessors.SignalsAccessor.sr_accessor_cls")
  * [SignalsAccessor.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.stats_defaults "vectorbtpro.signals.accessors.SignalsAccessor.stats_defaults")
  * [SignalsAccessor.to_mapped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_mapped "vectorbtpro.signals.accessors.SignalsAccessor.to_mapped")
  * [SignalsAccessor.to_nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth "vectorbtpro.signals.accessors.SignalsAccessor.to_nth")
  * [SignalsAccessor.to_nth_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth_after "vectorbtpro.signals.accessors.SignalsAccessor.to_nth_after")
  * [SignalsAccessor.total](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total "vectorbtpro.signals.accessors.SignalsAccessor.total")
  * [SignalsAccessor.total_partitions](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total_partitions "vectorbtpro.signals.accessors.SignalsAccessor.total_partitions")
  * [SignalsAccessor.unravel](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.unravel "vectorbtpro.signals.accessors.SignalsAccessor.unravel")
  * [SignalsAccessor.unravel_between](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.unravel_between "vectorbtpro.signals.accessors.SignalsAccessor.unravel_between")
  * [SignalsAccessor.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.signals.accessors.SignalsAccessor.unwrapped")
  * [SignalsAccessor.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.signals.accessors.SignalsAccessor.wrapper")
  * [SignalsAccessor.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.signals.accessors.SignalsAccessor.xloc")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.signals.accessors.SignalsAccessor.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.signals.accessors.SignalsAccessor.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.signals.accessors.SignalsAccessor.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.signals.accessors.SignalsAccessor.stats")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.signals.accessors.SignalsAccessor.regroup")
  * [Wrapping.resample](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resample "vectorbtpro.signals.accessors.SignalsAccessor.resample")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.resolve_stack_kwargs")



* * *

## SignalsSRAccessor class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/accessors.py#L2966-L2982 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsSRAccessor "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-93-1)SignalsSRAccessor(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-93-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-93-3)    obj=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-93-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#__codelineno-93-5))
    

Accessor on top of signal series. For Series only.

Accessible via `pd.Series.vbt.signals`.

**Superclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [BaseAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor "vectorbtpro.base.accessors.BaseAccessor")
  * [BaseSRAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseSRAccessor "vectorbtpro.base.accessors.BaseSRAccessor")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor "vectorbtpro.generic.accessors.GenericAccessor")
  * [GenericSRAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor "vectorbtpro.generic.accessors.GenericSRAccessor")
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
  * [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor "vectorbtpro.signals.accessors.SignalsAccessor")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.signals.accessors.SignalsAccessor.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.signals.accessors.SignalsAccessor.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.signals.accessors.SignalsAccessor.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.signals.accessors.SignalsAccessor.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.signals.accessors.SignalsAccessor.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.signals.accessors.SignalsAccessor.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.signals.accessors.SignalsAccessor.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.signals.accessors.SignalsAccessor.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.signals.accessors.SignalsAccessor.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.signals.accessors.SignalsAccessor.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.signals.accessors.SignalsAccessor.find_messages")
  * [BaseAccessor.align](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.align "vectorbtpro.signals.accessors.SignalsAccessor.align")
  * [BaseAccessor.align_to](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.align_to "vectorbtpro.signals.accessors.SignalsAccessor.align_to")
  * [BaseAccessor.apply](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply "vectorbtpro.signals.accessors.SignalsAccessor.apply")
  * [BaseAccessor.apply_and_concat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply_and_concat "vectorbtpro.signals.accessors.SignalsAccessor.apply_and_concat")
  * [BaseAccessor.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.apply_to_index "vectorbtpro.signals.accessors.SignalsAccessor.apply_to_index")
  * [BaseAccessor.broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast "vectorbtpro.signals.accessors.SignalsAccessor.broadcast")
  * [BaseAccessor.broadcast_combs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast_combs "vectorbtpro.signals.accessors.SignalsAccessor.broadcast_combs")
  * [BaseAccessor.broadcast_to](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.broadcast_to "vectorbtpro.signals.accessors.SignalsAccessor.broadcast_to")
  * [BaseAccessor.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.column_stack "vectorbtpro.signals.accessors.SignalsAccessor.column_stack")
  * [BaseAccessor.combine](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.combine "vectorbtpro.signals.accessors.SignalsAccessor.combine")
  * [BaseAccessor.concat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.concat "vectorbtpro.signals.accessors.SignalsAccessor.concat")
  * [BaseAccessor.cross](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.cross "vectorbtpro.signals.accessors.SignalsAccessor.cross")
  * [BaseAccessor.cross](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.x "vectorbtpro.signals.accessors.SignalsAccessor.x")
  * [BaseAccessor.cross_with](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.cross_with "vectorbtpro.signals.accessors.SignalsAccessor.cross_with")
  * [BaseAccessor.eval](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.eval "vectorbtpro.signals.accessors.SignalsAccessor.eval")
  * [BaseAccessor.get](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.get "vectorbtpro.signals.accessors.SignalsAccessor.get")
  * [BaseAccessor.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.indexing_func "vectorbtpro.signals.accessors.SignalsAccessor.indexing_func")
  * [BaseAccessor.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.indexing_setter_func "vectorbtpro.signals.accessors.SignalsAccessor.indexing_setter_func")
  * [BaseAccessor.is_frame](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.is_frame "vectorbtpro.signals.accessors.SignalsAccessor.is_frame")
  * [BaseAccessor.is_series](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.is_series "vectorbtpro.signals.accessors.SignalsAccessor.is_series")
  * [BaseAccessor.make_symmetric](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.make_symmetric "vectorbtpro.signals.accessors.SignalsAccessor.make_symmetric")
  * [BaseAccessor.repeat](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.repeat "vectorbtpro.signals.accessors.SignalsAccessor.repeat")
  * [BaseAccessor.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_column_stack_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.resolve_column_stack_kwargs")
  * [BaseAccessor.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_row_stack_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.resolve_row_stack_kwargs")
  * [BaseAccessor.resolve_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.resolve_shape "vectorbtpro.signals.accessors.SignalsAccessor.resolve_shape")
  * [BaseAccessor.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.row_stack "vectorbtpro.signals.accessors.SignalsAccessor.row_stack")
  * [BaseAccessor.set](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set "vectorbtpro.signals.accessors.SignalsAccessor.set")
  * [BaseAccessor.set_between](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set_between "vectorbtpro.signals.accessors.SignalsAccessor.set_between")
  * [BaseAccessor.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.signals.accessors.SignalsAccessor.should_wrap")
  * [BaseAccessor.tile](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.tile "vectorbtpro.signals.accessors.SignalsAccessor.tile")
  * [BaseAccessor.to_1d_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_1d_array "vectorbtpro.signals.accessors.SignalsAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_2d_array "vectorbtpro.signals.accessors.SignalsAccessor.to_2d_array")
  * [BaseAccessor.to_data](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_data "vectorbtpro.signals.accessors.SignalsAccessor.to_data")
  * [BaseAccessor.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.to_dict "vectorbtpro.signals.accessors.SignalsAccessor.to_dict")
  * [BaseAccessor.unstack_to_array](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.unstack_to_array "vectorbtpro.signals.accessors.SignalsAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.unstack_to_df "vectorbtpro.signals.accessors.SignalsAccessor.unstack_to_df")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.signals.accessors.SignalsAccessor.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.signals.accessors.SignalsAccessor.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.signals.accessors.SignalsAccessor.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.signals.accessors.SignalsAccessor.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.signals.accessors.SignalsAccessor.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.signals.accessors.SignalsAccessor.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.signals.accessors.SignalsAccessor.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.signals.accessors.SignalsAccessor.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.signals.accessors.SignalsAccessor.update_config")
  * [GenericAccessor.ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ago "vectorbtpro.generic.accessors.GenericSRAccessor.ago")
  * [GenericAccessor.all_ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.all_ago "vectorbtpro.signals.accessors.SignalsAccessor.all_ago")
  * [GenericAccessor.any_ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.any_ago "vectorbtpro.signals.accessors.SignalsAccessor.any_ago")
  * [GenericAccessor.apply_along_axis](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_along_axis "vectorbtpro.signals.accessors.SignalsAccessor.apply_along_axis")
  * [GenericAccessor.apply_and_reduce](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_and_reduce "vectorbtpro.signals.accessors.SignalsAccessor.apply_and_reduce")
  * [GenericAccessor.apply_mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.apply_mapping "vectorbtpro.signals.accessors.SignalsAccessor.apply_mapping")
  * [GenericAccessor.areaplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.areaplot "vectorbtpro.signals.accessors.SignalsAccessor.areaplot")
  * [GenericAccessor.barplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.barplot "vectorbtpro.signals.accessors.SignalsAccessor.barplot")
  * [GenericAccessor.bfill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.bfill "vectorbtpro.signals.accessors.SignalsAccessor.bfill")
  * [GenericAccessor.binarize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.binarize "vectorbtpro.signals.accessors.SignalsAccessor.binarize")
  * [GenericAccessor.boxplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.boxplot "vectorbtpro.signals.accessors.SignalsAccessor.boxplot")
  * [GenericAccessor.bshift](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.bshift "vectorbtpro.generic.accessors.GenericSRAccessor.bshift")
  * [GenericAccessor.column_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.column_apply "vectorbtpro.signals.accessors.SignalsAccessor.column_apply")
  * [GenericAccessor.corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.corr "vectorbtpro.signals.accessors.SignalsAccessor.corr")
  * [GenericAccessor.count](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.count "vectorbtpro.signals.accessors.SignalsAccessor.count")
  * [GenericAccessor.cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cov "vectorbtpro.signals.accessors.SignalsAccessor.cov")
  * [GenericAccessor.crossed_above](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_above "vectorbtpro.signals.accessors.SignalsAccessor.crossed_above")
  * [GenericAccessor.crossed_below](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_below "vectorbtpro.signals.accessors.SignalsAccessor.crossed_below")
  * [GenericAccessor.cumprod](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cumprod "vectorbtpro.signals.accessors.SignalsAccessor.cumprod")
  * [GenericAccessor.cumsum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.cumsum "vectorbtpro.signals.accessors.SignalsAccessor.cumsum")
  * [GenericAccessor.demean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.demean "vectorbtpro.signals.accessors.SignalsAccessor.demean")
  * [GenericAccessor.describe](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.describe "vectorbtpro.signals.accessors.SignalsAccessor.describe")
  * [GenericAccessor.diff](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.diff "vectorbtpro.signals.accessors.SignalsAccessor.diff")
  * [GenericAccessor.digitize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.digitize "vectorbtpro.signals.accessors.SignalsAccessor.digitize")
  * [GenericAccessor.drawdown](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.drawdown "vectorbtpro.signals.accessors.SignalsAccessor.drawdown")
  * [GenericAccessor.ewm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ewm_mean "vectorbtpro.signals.accessors.SignalsAccessor.ewm_mean")
  * [GenericAccessor.ewm_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ewm_std "vectorbtpro.signals.accessors.SignalsAccessor.ewm_std")
  * [GenericAccessor.expanding_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_apply "vectorbtpro.signals.accessors.SignalsAccessor.expanding_apply")
  * [GenericAccessor.expanding_corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_corr "vectorbtpro.signals.accessors.SignalsAccessor.expanding_corr")
  * [GenericAccessor.expanding_cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_cov "vectorbtpro.signals.accessors.SignalsAccessor.expanding_cov")
  * [GenericAccessor.expanding_idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_idxmax "vectorbtpro.signals.accessors.SignalsAccessor.expanding_idxmax")
  * [GenericAccessor.expanding_idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_idxmin "vectorbtpro.signals.accessors.SignalsAccessor.expanding_idxmin")
  * [GenericAccessor.expanding_max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_max "vectorbtpro.signals.accessors.SignalsAccessor.expanding_max")
  * [GenericAccessor.expanding_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_mean "vectorbtpro.signals.accessors.SignalsAccessor.expanding_mean")
  * [GenericAccessor.expanding_min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_min "vectorbtpro.signals.accessors.SignalsAccessor.expanding_min")
  * [GenericAccessor.expanding_ols](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_ols "vectorbtpro.signals.accessors.SignalsAccessor.expanding_ols")
  * [GenericAccessor.expanding_rank](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_rank "vectorbtpro.signals.accessors.SignalsAccessor.expanding_rank")
  * [GenericAccessor.expanding_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_std "vectorbtpro.signals.accessors.SignalsAccessor.expanding_std")
  * [GenericAccessor.expanding_zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.expanding_zscore "vectorbtpro.signals.accessors.SignalsAccessor.expanding_zscore")
  * [GenericAccessor.fbfill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fbfill "vectorbtpro.signals.accessors.SignalsAccessor.fbfill")
  * [GenericAccessor.ffill](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ffill "vectorbtpro.signals.accessors.SignalsAccessor.ffill")
  * [GenericAccessor.fillna](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fillna "vectorbtpro.signals.accessors.SignalsAccessor.fillna")
  * [GenericAccessor.find_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.find_pattern "vectorbtpro.signals.accessors.SignalsAccessor.find_pattern")
  * [GenericAccessor.flatten_grouped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.flatten_grouped "vectorbtpro.signals.accessors.SignalsAccessor.flatten_grouped")
  * [GenericAccessor.fshift](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fshift "vectorbtpro.generic.accessors.GenericSRAccessor.fshift")
  * [GenericAccessor.get_drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.get_drawdowns "vectorbtpro.signals.accessors.SignalsAccessor.get_drawdowns")
  * [GenericAccessor.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.get_ranges "vectorbtpro.signals.accessors.SignalsAccessor.get_ranges")
  * [GenericAccessor.groupby_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_apply "vectorbtpro.signals.accessors.SignalsAccessor.groupby_apply")
  * [GenericAccessor.groupby_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_transform "vectorbtpro.signals.accessors.SignalsAccessor.groupby_transform")
  * [GenericAccessor.heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.heatmap "vectorbtpro.signals.accessors.SignalsAccessor.heatmap")
  * [GenericAccessor.histplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.histplot "vectorbtpro.signals.accessors.SignalsAccessor.histplot")
  * [GenericAccessor.idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.idxmax "vectorbtpro.signals.accessors.SignalsAccessor.idxmax")
  * [GenericAccessor.idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.idxmin "vectorbtpro.signals.accessors.SignalsAccessor.idxmin")
  * [GenericAccessor.lineplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.lineplot "vectorbtpro.signals.accessors.SignalsAccessor.lineplot")
  * [GenericAccessor.ma](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ma "vectorbtpro.signals.accessors.SignalsAccessor.ma")
  * [GenericAccessor.map](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.map "vectorbtpro.signals.accessors.SignalsAccessor.map")
  * [GenericAccessor.max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.max "vectorbtpro.signals.accessors.SignalsAccessor.max")
  * [GenericAccessor.maxabs_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.maxabs_scale "vectorbtpro.signals.accessors.SignalsAccessor.maxabs_scale")
  * [GenericAccessor.mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.mean "vectorbtpro.signals.accessors.SignalsAccessor.mean")
  * [GenericAccessor.median](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.median "vectorbtpro.signals.accessors.SignalsAccessor.median")
  * [GenericAccessor.min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.min "vectorbtpro.signals.accessors.SignalsAccessor.min")
  * [GenericAccessor.minmax_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.minmax_scale "vectorbtpro.signals.accessors.SignalsAccessor.minmax_scale")
  * [GenericAccessor.msd](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.msd "vectorbtpro.signals.accessors.SignalsAccessor.msd")
  * [GenericAccessor.normalize](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.normalize "vectorbtpro.signals.accessors.SignalsAccessor.normalize")
  * [GenericAccessor.overlay_with_heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.overlay_with_heatmap "vectorbtpro.signals.accessors.SignalsAccessor.overlay_with_heatmap")
  * [GenericAccessor.pct_change](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.pct_change "vectorbtpro.signals.accessors.SignalsAccessor.pct_change")
  * [GenericAccessor.plot_against](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot_against "vectorbtpro.signals.accessors.SignalsAccessor.plot_against")
  * [GenericAccessor.plot_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot_pattern "vectorbtpro.signals.accessors.SignalsAccessor.plot_pattern")
  * [GenericAccessor.power_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.power_transform "vectorbtpro.signals.accessors.SignalsAccessor.power_transform")
  * [GenericAccessor.product](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.product "vectorbtpro.signals.accessors.SignalsAccessor.product")
  * [GenericAccessor.proximity_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.proximity_apply "vectorbtpro.signals.accessors.SignalsAccessor.proximity_apply")
  * [GenericAccessor.qqplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.qqplot "vectorbtpro.signals.accessors.SignalsAccessor.qqplot")
  * [GenericAccessor.quantile_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.quantile_transform "vectorbtpro.signals.accessors.SignalsAccessor.quantile_transform")
  * [GenericAccessor.realign](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign "vectorbtpro.generic.accessors.GenericSRAccessor.realign")
  * [GenericAccessor.realign_closing](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_closing "vectorbtpro.signals.accessors.SignalsAccessor.realign_closing")
  * [GenericAccessor.realign_opening](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_opening "vectorbtpro.signals.accessors.SignalsAccessor.realign_opening")
  * [GenericAccessor.rebase](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rebase "vectorbtpro.signals.accessors.SignalsAccessor.rebase")
  * [GenericAccessor.reduce](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.reduce "vectorbtpro.signals.accessors.SignalsAccessor.reduce")
  * [GenericAccessor.resample_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_apply "vectorbtpro.signals.accessors.SignalsAccessor.resample_apply")
  * [GenericAccessor.resample_between_bounds](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_between_bounds "vectorbtpro.signals.accessors.SignalsAccessor.resample_between_bounds")
  * [GenericAccessor.resample_to_index](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_to_index "vectorbtpro.signals.accessors.SignalsAccessor.resample_to_index")
  * [GenericAccessor.resolve_mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resolve_mapping "vectorbtpro.signals.accessors.SignalsAccessor.resolve_mapping")
  * [GenericAccessor.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resolve_self "vectorbtpro.signals.accessors.SignalsAccessor.resolve_self")
  * [GenericAccessor.robust_scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.robust_scale "vectorbtpro.signals.accessors.SignalsAccessor.robust_scale")
  * [GenericAccessor.rolling_all](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_all "vectorbtpro.signals.accessors.SignalsAccessor.rolling_all")
  * [GenericAccessor.rolling_any](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_any "vectorbtpro.signals.accessors.SignalsAccessor.rolling_any")
  * [GenericAccessor.rolling_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_apply "vectorbtpro.signals.accessors.SignalsAccessor.rolling_apply")
  * [GenericAccessor.rolling_corr](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_corr "vectorbtpro.signals.accessors.SignalsAccessor.rolling_corr")
  * [GenericAccessor.rolling_cov](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_cov "vectorbtpro.signals.accessors.SignalsAccessor.rolling_cov")
  * [GenericAccessor.rolling_idxmax](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_idxmax "vectorbtpro.signals.accessors.SignalsAccessor.rolling_idxmax")
  * [GenericAccessor.rolling_idxmin](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_idxmin "vectorbtpro.signals.accessors.SignalsAccessor.rolling_idxmin")
  * [GenericAccessor.rolling_max](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_max "vectorbtpro.signals.accessors.SignalsAccessor.rolling_max")
  * [GenericAccessor.rolling_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_mean "vectorbtpro.signals.accessors.SignalsAccessor.rolling_mean")
  * [GenericAccessor.rolling_min](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_min "vectorbtpro.signals.accessors.SignalsAccessor.rolling_min")
  * [GenericAccessor.rolling_ols](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_ols "vectorbtpro.signals.accessors.SignalsAccessor.rolling_ols")
  * [GenericAccessor.rolling_pattern_similarity](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_pattern_similarity "vectorbtpro.signals.accessors.SignalsAccessor.rolling_pattern_similarity")
  * [GenericAccessor.rolling_prod](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_prod "vectorbtpro.signals.accessors.SignalsAccessor.rolling_prod")
  * [GenericAccessor.rolling_rank](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_rank "vectorbtpro.signals.accessors.SignalsAccessor.rolling_rank")
  * [GenericAccessor.rolling_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_std "vectorbtpro.signals.accessors.SignalsAccessor.rolling_std")
  * [GenericAccessor.rolling_sum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_sum "vectorbtpro.signals.accessors.SignalsAccessor.rolling_sum")
  * [GenericAccessor.rolling_zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_zscore "vectorbtpro.signals.accessors.SignalsAccessor.rolling_zscore")
  * [GenericAccessor.row_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.row_apply "vectorbtpro.signals.accessors.SignalsAccessor.row_apply")
  * [GenericAccessor.scale](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.scale "vectorbtpro.signals.accessors.SignalsAccessor.scale")
  * [GenericAccessor.scatterplot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.scatterplot "vectorbtpro.signals.accessors.SignalsAccessor.scatterplot")
  * [GenericAccessor.shuffle](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.shuffle "vectorbtpro.signals.accessors.SignalsAccessor.shuffle")
  * [GenericAccessor.squeeze_grouped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.squeeze_grouped "vectorbtpro.signals.accessors.SignalsAccessor.squeeze_grouped")
  * [GenericAccessor.std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.std "vectorbtpro.signals.accessors.SignalsAccessor.std")
  * [GenericAccessor.sum](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.sum "vectorbtpro.signals.accessors.SignalsAccessor.sum")
  * [GenericAccessor.to_daily_log_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_daily_log_returns "vectorbtpro.signals.accessors.SignalsAccessor.to_daily_log_returns")
  * [GenericAccessor.to_daily_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_daily_returns "vectorbtpro.signals.accessors.SignalsAccessor.to_daily_returns")
  * [GenericAccessor.to_log_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_log_returns "vectorbtpro.signals.accessors.SignalsAccessor.to_log_returns")
  * [GenericAccessor.to_returns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_returns "vectorbtpro.signals.accessors.SignalsAccessor.to_returns")
  * [GenericAccessor.transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.transform "vectorbtpro.signals.accessors.SignalsAccessor.transform")
  * [GenericAccessor.ts_heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ts_heatmap "vectorbtpro.signals.accessors.SignalsAccessor.ts_heatmap")
  * [GenericAccessor.value_counts](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.value_counts "vectorbtpro.signals.accessors.SignalsAccessor.value_counts")
  * [GenericAccessor.vidya](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.vidya "vectorbtpro.signals.accessors.SignalsAccessor.vidya")
  * [GenericAccessor.volume](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.volume "vectorbtpro.signals.accessors.SignalsAccessor.volume")
  * [GenericAccessor.wm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wm_mean "vectorbtpro.signals.accessors.SignalsAccessor.wm_mean")
  * [GenericAccessor.wwm_mean](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wwm_mean "vectorbtpro.signals.accessors.SignalsAccessor.wwm_mean")
  * [GenericAccessor.wwm_std](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.wwm_std "vectorbtpro.signals.accessors.SignalsAccessor.wwm_std")
  * [GenericAccessor.zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.zscore "vectorbtpro.signals.accessors.SignalsAccessor.zscore")
  * [GenericSRAccessor.fit_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.fit_pattern "vectorbtpro.generic.accessors.GenericSRAccessor.fit_pattern")
  * [GenericSRAccessor.to_renko](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.to_renko "vectorbtpro.generic.accessors.GenericSRAccessor.to_renko")
  * [GenericSRAccessor.to_renko_ohlc](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.to_renko_ohlc "vectorbtpro.generic.accessors.GenericSRAccessor.to_renko_ohlc")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.signals.accessors.SignalsAccessor.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.signals.accessors.SignalsAccessor.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.signals.accessors.SignalsAccessor.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.signals.accessors.SignalsAccessor.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.signals.accessors.SignalsAccessor.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.signals.accessors.SignalsAccessor.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.signals.accessors.SignalsAccessor.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.signals.accessors.SignalsAccessor.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.signals.accessors.SignalsAccessor.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.signals.accessors.SignalsAccessor.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.signals.accessors.SignalsAccessor.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.signals.accessors.SignalsAccessor.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.signals.accessors.SignalsAccessor.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.signals.accessors.SignalsAccessor.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.signals.accessors.SignalsAccessor.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.signals.accessors.SignalsAccessor.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.signals.accessors.SignalsAccessor.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.signals.accessors.SignalsAccessor.select_col_from_obj")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.signals.accessors.SignalsAccessor.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.signals.accessors.SignalsAccessor.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.signals.accessors.SignalsAccessor.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.signals.accessors.SignalsAccessor.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.signals.accessors.SignalsAccessor.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.signals.accessors.SignalsAccessor.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.signals.accessors.SignalsAccessor.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.signals.accessors.SignalsAccessor.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.signals.accessors.SignalsAccessor.select_levels")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.signals.accessors.SignalsAccessor.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.signals.accessors.SignalsAccessor.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.signals.accessors.SignalsAccessor.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.signals.accessors.SignalsAccessor.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.signals.accessors.SignalsAccessor.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.signals.accessors.SignalsAccessor.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.signals.accessors.SignalsAccessor.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.signals.accessors.SignalsAccessor.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.signals.accessors.SignalsAccessor.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.signals.accessors.SignalsAccessor.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.signals.accessors.SignalsAccessor.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.signals.accessors.SignalsAccessor.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.signals.accessors.SignalsAccessor.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.signals.accessors.SignalsAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.signals.accessors.SignalsAccessor.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.signals.accessors.SignalsAccessor.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.signals.accessors.SignalsAccessor.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.signals.accessors.SignalsAccessor.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.signals.accessors.SignalsAccessor.pprint")
  * [SignalsAccessor.between_partition_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_partition_ranges "vectorbtpro.signals.accessors.SignalsAccessor.between_partition_ranges")
  * [SignalsAccessor.between_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_ranges "vectorbtpro.signals.accessors.SignalsAccessor.between_ranges")
  * [SignalsAccessor.clean](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.clean "vectorbtpro.signals.accessors.SignalsAccessor.clean")
  * [SignalsAccessor.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.signals.accessors.SignalsAccessor.cls_dir")
  * [SignalsAccessor.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.signals.accessors.SignalsAccessor.column_only_select")
  * [SignalsAccessor.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.signals.accessors.SignalsAccessor.config")
  * [SignalsAccessor.delta_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.delta_ranges "vectorbtpro.signals.accessors.SignalsAccessor.delta_ranges")
  * [SignalsAccessor.df_accessor_cls](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.df_accessor_cls "vectorbtpro.signals.accessors.SignalsAccessor.df_accessor_cls")
  * [SignalsAccessor.distance_from_last](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.distance_from_last "vectorbtpro.signals.accessors.SignalsAccessor.distance_from_last")
  * [SignalsAccessor.drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.drawdowns "vectorbtpro.signals.accessors.SignalsAccessor.drawdowns")
  * [SignalsAccessor.empty](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.empty "vectorbtpro.signals.accessors.SignalsAccessor.empty")
  * [SignalsAccessor.empty_like](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.empty_like "vectorbtpro.signals.accessors.SignalsAccessor.empty_like")
  * [SignalsAccessor.first](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first "vectorbtpro.signals.accessors.SignalsAccessor.first")
  * [SignalsAccessor.first_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first_after "vectorbtpro.signals.accessors.SignalsAccessor.first_after")
  * [SignalsAccessor.from_nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.from_nth "vectorbtpro.signals.accessors.SignalsAccessor.from_nth")
  * [SignalsAccessor.from_nth_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.from_nth_after "vectorbtpro.signals.accessors.SignalsAccessor.from_nth_after")
  * [SignalsAccessor.generate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate "vectorbtpro.signals.accessors.SignalsAccessor.generate")
  * [SignalsAccessor.generate_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_both "vectorbtpro.signals.accessors.SignalsAccessor.generate_both")
  * [SignalsAccessor.generate_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_exits")
  * [SignalsAccessor.generate_ohlc_stop_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits")
  * [SignalsAccessor.generate_random](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random "vectorbtpro.signals.accessors.SignalsAccessor.generate_random")
  * [SignalsAccessor.generate_random_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random_both "vectorbtpro.signals.accessors.SignalsAccessor.generate_random_both")
  * [SignalsAccessor.generate_random_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_random_exits")
  * [SignalsAccessor.generate_stop_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_stop_exits "vectorbtpro.signals.accessors.SignalsAccessor.generate_stop_exits")
  * [SignalsAccessor.get_relation_str](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.get_relation_str "vectorbtpro.signals.accessors.SignalsAccessor.get_relation_str")
  * [SignalsAccessor.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.signals.accessors.SignalsAccessor.group_select")
  * [SignalsAccessor.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.signals.accessors.SignalsAccessor.iloc")
  * [SignalsAccessor.index_from_unravel](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.index_from_unravel "vectorbtpro.signals.accessors.SignalsAccessor.index_from_unravel")
  * [SignalsAccessor.index_mapped](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.index_mapped "vectorbtpro.signals.accessors.SignalsAccessor.index_mapped")
  * [SignalsAccessor.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.indexing_kwargs")
  * [SignalsAccessor.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.signals.accessors.SignalsAccessor.loc")
  * [SignalsAccessor.mapping](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.mapping "vectorbtpro.signals.accessors.SignalsAccessor.mapping")
  * [SignalsAccessor.ndim](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.ndim "vectorbtpro.signals.accessors.SignalsAccessor.ndim")
  * [SignalsAccessor.norm_avg_index](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.norm_avg_index "vectorbtpro.signals.accessors.SignalsAccessor.norm_avg_index")
  * [SignalsAccessor.nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth "vectorbtpro.signals.accessors.SignalsAccessor.nth")
  * [SignalsAccessor.nth_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth_after "vectorbtpro.signals.accessors.SignalsAccessor.nth_after")
  * [SignalsAccessor.nth_index](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth_index "vectorbtpro.signals.accessors.SignalsAccessor.nth_index")
  * [SignalsAccessor.obj](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.obj "vectorbtpro.signals.accessors.SignalsAccessor.obj")
  * [SignalsAccessor.partition_pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank")
  * [SignalsAccessor.partition_pos_rank_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_after "vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_after")
  * [SignalsAccessor.partition_pos_rank_mapped](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_mapped "vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank_mapped")
  * [SignalsAccessor.partition_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_ranges "vectorbtpro.signals.accessors.SignalsAccessor.partition_ranges")
  * [SignalsAccessor.partition_rate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_rate "vectorbtpro.signals.accessors.SignalsAccessor.partition_rate")
  * [SignalsAccessor.plot](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot "vectorbtpro.signals.accessors.SignalsAccessor.plot")
  * [SignalsAccessor.plot_as_entries](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entries "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entries")
  * [SignalsAccessor.plot_as_entry_marks](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entry_marks "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_entry_marks")
  * [SignalsAccessor.plot_as_exit_marks](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exit_marks "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exit_marks")
  * [SignalsAccessor.plot_as_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exits "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_exits")
  * [SignalsAccessor.plot_as_markers](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers "vectorbtpro.signals.accessors.SignalsAccessor.plot_as_markers")
  * [SignalsAccessor.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.plots_defaults "vectorbtpro.signals.accessors.SignalsAccessor.plots_defaults")
  * [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank")
  * [SignalsAccessor.pos_rank_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_after")
  * [SignalsAccessor.pos_rank_mapped](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_mapped "vectorbtpro.signals.accessors.SignalsAccessor.pos_rank_mapped")
  * [SignalsAccessor.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.signals.accessors.SignalsAccessor.range_only_select")
  * [SignalsAccessor.ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ranges "vectorbtpro.signals.accessors.SignalsAccessor.ranges")
  * [SignalsAccessor.rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rank "vectorbtpro.signals.accessors.SignalsAccessor.rank")
  * [SignalsAccessor.rate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rate "vectorbtpro.signals.accessors.SignalsAccessor.rate")
  * [SignalsAccessor.ravel](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.ravel "vectorbtpro.signals.accessors.SignalsAccessor.ravel")
  * [SignalsAccessor.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.signals.accessors.SignalsAccessor.rec_state")
  * [SignalsAccessor.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.signals.accessors.SignalsAccessor.self_aliases")
  * [SignalsAccessor.sr_accessor_cls](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.sr_accessor_cls "vectorbtpro.signals.accessors.SignalsAccessor.sr_accessor_cls")
  * [SignalsAccessor.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.stats_defaults "vectorbtpro.signals.accessors.SignalsAccessor.stats_defaults")
  * [SignalsAccessor.to_mapped](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.to_mapped "vectorbtpro.signals.accessors.SignalsAccessor.to_mapped")
  * [SignalsAccessor.to_nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth "vectorbtpro.signals.accessors.SignalsAccessor.to_nth")
  * [SignalsAccessor.to_nth_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth_after "vectorbtpro.signals.accessors.SignalsAccessor.to_nth_after")
  * [SignalsAccessor.total](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total "vectorbtpro.signals.accessors.SignalsAccessor.total")
  * [SignalsAccessor.total_partitions](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.total_partitions "vectorbtpro.signals.accessors.SignalsAccessor.total_partitions")
  * [SignalsAccessor.unravel](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.unravel "vectorbtpro.signals.accessors.SignalsAccessor.unravel")
  * [SignalsAccessor.unravel_between](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.unravel_between "vectorbtpro.signals.accessors.SignalsAccessor.unravel_between")
  * [SignalsAccessor.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.signals.accessors.SignalsAccessor.unwrapped")
  * [SignalsAccessor.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.signals.accessors.SignalsAccessor.wrapper")
  * [SignalsAccessor.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.signals.accessors.SignalsAccessor.xloc")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.signals.accessors.SignalsAccessor.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.signals.accessors.SignalsAccessor.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.signals.accessors.SignalsAccessor.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.signals.accessors.SignalsAccessor.stats")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.signals.accessors.SignalsAccessor.regroup")
  * [Wrapping.resample](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resample "vectorbtpro.signals.accessors.SignalsAccessor.resample")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.signals.accessors.SignalsAccessor.resolve_stack_kwargs")


