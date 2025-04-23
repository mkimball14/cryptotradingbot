# Aggregation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#aggregation "Permanent link")

Aggregation plays a central role in downsampling. Consider a use case where we want to know the maximum drawdown (MDD) of each month of data. Let's do this using various different techniques available in vectorbt. The first approach involves resampling the data and then manipulating it:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-1)>>> ms_data = h1_data.resample("M") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-2)>>> ms_data.get("Low") / ms_data.get("High") - 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-3)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-4)2020-01-01 00:00:00+00:00 -0.282623
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-5)2020-02-01 00:00:00+00:00 -0.195714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-6)2020-03-01 00:00:00+00:00 -0.588362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-7)2020-04-01 00:00:00+00:00 -0.349883
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-8)2020-05-01 00:00:00+00:00 -0.193702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-9)2020-06-01 00:00:00+00:00 -0.149037
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-10)2020-07-01 00:00:00+00:00 -0.222909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-11)2020-08-01 00:00:00+00:00 -0.156360
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-12)2020-09-01 00:00:00+00:00 -0.184705
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-13)2020-10-01 00:00:00+00:00 -0.264255
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-14)2020-11-01 00:00:00+00:00 -0.335702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-15)2020-12-01 00:00:00+00:00 -0.400262
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-0-16)Freq: MS, dtype: float64
 
[/code]

 1. 

The same can be done by resampling only the arrays that are needed for the calculation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-1)>>> h1_high = h1_data.get("High")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-2)>>> h1_low = h1_data.get("Low")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-3)>>> ms_high = h1_high.resample(vbt.offset("M")).max()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-4)>>> ms_low = h1_low.resample(vbt.offset("M")).min()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-5)>>> ms_low / ms_high - 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-6)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-7)2020-01-01 00:00:00+00:00 -0.282623
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-8)2020-02-01 00:00:00+00:00 -0.195714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-9)2020-03-01 00:00:00+00:00 -0.588362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-10)2020-04-01 00:00:00+00:00 -0.349883
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-11)2020-05-01 00:00:00+00:00 -0.193702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-12)2020-06-01 00:00:00+00:00 -0.149037
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-13)2020-07-01 00:00:00+00:00 -0.222909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-14)2020-08-01 00:00:00+00:00 -0.156360
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-15)2020-09-01 00:00:00+00:00 -0.184705
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-16)2020-10-01 00:00:00+00:00 -0.264255
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-17)2020-11-01 00:00:00+00:00 -0.335702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-18)2020-12-01 00:00:00+00:00 -0.400262
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-1-19)Freq: MS, dtype: float64
 
[/code]

And now using the vectorbt's superfast [GenericAccessor.resample_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_apply), which uses Numba:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-1)>>> ms_high = h1_high.vbt.resample_apply("M", vbt.nb.max_reduce_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-2)>>> ms_low = h1_low.vbt.resample_apply("M", vbt.nb.min_reduce_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-3)>>> ms_low / ms_high - 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-4)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-5)2020-01-01 00:00:00+00:00 -0.282623
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-6)2020-02-01 00:00:00+00:00 -0.195714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-7)2020-03-01 00:00:00+00:00 -0.588362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-8)2020-04-01 00:00:00+00:00 -0.349883
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-9)2020-05-01 00:00:00+00:00 -0.193702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-10)2020-06-01 00:00:00+00:00 -0.149037
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-11)2020-07-01 00:00:00+00:00 -0.222909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-12)2020-08-01 00:00:00+00:00 -0.156360
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-13)2020-09-01 00:00:00+00:00 -0.184705
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-14)2020-10-01 00:00:00+00:00 -0.264255
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-15)2020-11-01 00:00:00+00:00 -0.335702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-16)2020-12-01 00:00:00+00:00 -0.400262
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-2-17)Freq: MS, dtype: float64
 
[/code]

Hint

See available reduce functions ending with `reduce_nb` in [nb.apply_reduce](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/apply_reduce/). If you cannot find some function, you can always write it yourself ![😉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f609.svg)


# Custom index[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#custom-index "Permanent link")

Using rules such as `"M"` is very convenient but still not enough for many use cases. Consider a scenario where we already have a target index we would want to resample to: none of Pandas functions allow for such flexibility, unless we can somehow express the operation using [pandas.DataFrame.groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html). Luckily, vectorbt allows for a variety of inputs and options to make this possible.


# Using target index[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#using-target-index "Permanent link")

The method [GenericAccessor.resample_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_apply) has two different modes: the one that uses the target index (see [GenericAccessor.resample_to_index](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_to_index)), and the one that uses a Pandas resampler and vectorbt's grouping mechanism (see [GenericAccessor.groupby_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_apply)). The first one is the default mode: it's very fast but requires careful handling of bounds. The second one is guaranteed to produce the same results as Pandas but is (considerably) slower, and can be enabled by passing `use_groupby_apply=True` to [GenericAccessor.resample_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_apply).

Talking about the first mode, it actually works in a similar fashion to [GenericAccessor.realign](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign) by taking the source and target index, and aggregating all the array elements located between each two timestamps in the target index. This is done in one pass for best efficiency. And also similar to `realign`, we can pass a [Resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler) instance and so provide our own custom index, even a numeric one. But in contrast to `realign`, there is no argument to specify frequencies or bounds - the left/right bound is always the previous/next element in the target index (or infinity). This is best illustrated in the following example:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-1)>>> target_index = pd.Index([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-2)... "2020-01-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-3)... "2020-02-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-4)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-5)>>> h1_high.vbt.resample_to_index(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-6)... target_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-7)... vbt.nb.max_reduce_nb
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-9)2020-01-01 9578.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-10)2020-02-01 29300.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-3-11)Name: High, dtype: float64
 
[/code]

Info

You should only think about this whenever passing a custom index. Passing a frequency like `"M"` will produce results identical to that of Pandas with default arguments.

We see that the second value takes the maximum out of all values coming after `2020-02-01`, which is not intended since we want the aggregation to be performed strictly per month. To solve this, let's add another index value that will act as the rightmost bound:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-1)>>> target_rbound_index = vbt.Resampler.get_rbound_index( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-2)... target_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-3)... pd.offsets.MonthBegin(1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-5)>>> h1_high.vbt.resample_to_index(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-6)... target_index.append(target_rbound_index[[-1]]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-7)... vbt.nb.max_reduce_nb
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-8)... ).iloc[:-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-9)2020-01-01 9578.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-10)2020-02-01 10500.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-11)Name: High, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-13)>>> h1_high[:"2020-03-01"].resample(vbt.offset("M")).max().iloc[:-1] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-14)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-15)2020-01-01 00:00:00+00:00 9578.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-16)2020-02-01 00:00:00+00:00 10500.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-4-17)Freq: MS, Name: High, dtype: float64
 
[/code]

 1. 2. 


# Using group-by[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#using-group-by "Permanent link")

The second mode has a completely different implementation: it creates or takes a [Pandas Resampler](https://pandas.pydata.org/docs/reference/resampling.html) or a [Pandas Grouper](https://pandas.pydata.org/docs/reference/api/pandas.Grouper.html), and parses them to build a [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/#vectorbtpro.base.grouping.base.Grouper) instance. The grouper stores a map linking each group of elements in the source index to the respective elements in the target index. This map is then passed to a Numba-compiled function for aggregation per group.

Enough theory! Let's perform our resampling procedure using the grouping mechanism:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-1)>>> pd_resampler = h1_high.resample(vbt.offset("M"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-2)>>> ms_high = h1_high.vbt.groupby_apply(pd_resampler, vbt.nb.max_reduce_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-3)>>> ms_low = h1_low.vbt.groupby_apply(pd_resampler, vbt.nb.min_reduce_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-4)>>> ms_low / ms_high - 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-5)2020-01-01 00:00:00+00:00 -0.282623
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-6)2020-02-01 00:00:00+00:00 -0.195714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-7)2020-03-01 00:00:00+00:00 -0.588362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-8)2020-04-01 00:00:00+00:00 -0.349883
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-9)2020-05-01 00:00:00+00:00 -0.193702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-10)2020-06-01 00:00:00+00:00 -0.149037
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-11)2020-07-01 00:00:00+00:00 -0.222909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-12)2020-08-01 00:00:00+00:00 -0.156360
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-13)2020-09-01 00:00:00+00:00 -0.184705
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-14)2020-10-01 00:00:00+00:00 -0.264255
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-15)2020-11-01 00:00:00+00:00 -0.335702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-16)2020-12-01 00:00:00+00:00 -0.400262
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-5-17)dtype: float64
 
[/code]

But since parsing a resampler or grouper object from Pandas is kinda slow, we can provide our own grouper that can considerably speed the things up. Here we have two options: either providing any `group_by` object, such as a Pandas Index, a NumPy array, or a level name in a multi-index level, or a [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/#vectorbtpro.base.grouping.base.Grouper) instance itself.

Below, we will aggregate the data by month index:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-1)>>> h1_high.vbt.groupby_apply(h1_high.index.month, vbt.nb.max_reduce_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-3)1 9578.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-4)2 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-5)3 9188.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-6)4 9460.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-7)5 10067.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-8)6 10380.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-9)7 11444.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-10)8 12468.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-11)9 12050.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-12)10 14100.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-13)11 19863.16
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-14)12 29300.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-6-15)Name: High, dtype: float64
 
[/code]

Which is similar to calling [pandas.DataFrame.groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-1)>>> h1_high.groupby(h1_high.index.month).max()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-3)1 9578.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-4)2 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-5)3 9188.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-6)4 9460.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-7)5 10067.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-8)6 10380.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-9)7 11444.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-10)8 12468.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-11)9 12050.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-12)10 14100.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-13)11 19863.16
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-14)12 29300.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-7-15)Name: High, dtype: float64
 
[/code]

Hint

Using built-in functions such as `max` when using Pandas resampling and grouping are already optimized and are on par with vectorbt regarding performance. Consider using vectorbt's functions mainly when you have a custom function and you are forced to use `apply` \- that's where vectorbt really shines ![☀](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2600.svg)


# Using bounds[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#using-bounds "Permanent link")

We've just learned that [GenericAccessor.resample_to_index](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_to_index) aggregates all the array values that come after/before each element in the target index, while [GenericAccessor.groupby_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_apply) aggregates all the array values that map to the same target index by binning. But the first method doesn't allow gaps and custom bounds, while the second method doesn't allow overlapping groups. Both of these limitations are solved by [GenericAccessor.resample_between_bounds](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_between_bounds)!

This method takes the left and the right bound of the target index, and aggregates all the array values that fall in between those two bounds:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-1)>>> target_lbound_index = pd.Index([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-2)... "2020-01-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-3)... "2020-02-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-4)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-5)>>> target_rbound_index = pd.Index([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-6)... "2020-02-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-7)... "2020-03-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-8)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-9)>>> h1_high.vbt.resample_between_bounds( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-10)... target_lbound_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-11)... target_rbound_index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-12)... vbt.nb.max_reduce_nb
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-14)2020-01-01 9578.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-15)2020-02-01 10500.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-8-16)Name: High, dtype: float64
 
[/code]

 1. 

This opens some very interesting possibilities, such as custom-sized expanding windows. Let's calculate the highest high up to the beginning of each month:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-1)>>> h1_high.vbt.resample_between_bounds(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-2)... "2020-01-01", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-3)... vbt.date_range("2020-01-02", "2021-01-01", freq="M", inclusive="both"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-4)... vbt.nb.max_reduce_nb
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-5)... ) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-6)2020-02-01 9578.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-7)2020-03-01 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-8)2020-04-01 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-9)2020-05-01 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-10)2020-06-01 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-11)2020-07-01 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-12)2020-08-01 11444.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-13)2020-09-01 12468.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-14)2020-10-01 12468.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-15)2020-11-01 14100.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-16)2020-12-01 19863.16
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-17)2021-01-01 29300.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-9-18)Freq: MS, Name: High, dtype: float64
 
[/code]

 1. 

Let's validate the output:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-1)>>> h1_high.expanding().max().resample(vbt.offset("M")).max()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-3)2020-01-01 00:00:00+00:00 9578.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-4)2020-02-01 00:00:00+00:00 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-5)2020-03-01 00:00:00+00:00 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-6)2020-04-01 00:00:00+00:00 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-7)2020-05-01 00:00:00+00:00 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-8)2020-06-01 00:00:00+00:00 10500.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-9)2020-07-01 00:00:00+00:00 11444.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-10)2020-08-01 00:00:00+00:00 12468.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-11)2020-09-01 00:00:00+00:00 12468.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-12)2020-10-01 00:00:00+00:00 14100.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-13)2020-11-01 00:00:00+00:00 19863.16
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-14)2020-12-01 00:00:00+00:00 29300.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-10-15)Freq: MS, Name: High, dtype: float64
 
[/code]


# Meta methods[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#meta-methods "Permanent link")

All the methods introduced above are great when the primary operation should be performed on **one** array. But as soon as the operation involves multiple arrays (like `h1_high` and `h1_low` in our example), we need to perform multiple resampling operations and make sure that the results align nicely. A cleaner approach would be to do a resampling operation that does the entire calculation in one single pass, which is best for performance and consistency. Such operations can be performed using meta methods. 

Meta methods are class methods that aren't bound to any particular array and that can take, broadcast, and combine more than one array of data. And the good thing is: most of the methods we used above are also available as meta methods! Let's calculate the MDD using a single resampling operation with [GenericAccessor.resample_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_apply):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-1)>>> @njit 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-2)... def mdd_nb(from_i, to_i, col, high, low): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-3)... highest = np.nanmax(high[from_i:to_i, col]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-4)... lowest = np.nanmin(low[from_i:to_i, col])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-5)... return lowest / highest - 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-7)>>> vbt.pd_acc.resample_apply( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-8)... 'MS',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-9)... mdd_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-10)... vbt.Rep('high'), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-11)... vbt.Rep('low'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-12)... broadcast_named_args=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-13)... high=h1_high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-14)... low=h1_low
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-17)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-18)2020-01-01 00:00:00+00:00 -0.282623
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-19)2020-02-01 00:00:00+00:00 -0.195714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-20)2020-03-01 00:00:00+00:00 -0.588362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-21)2020-04-01 00:00:00+00:00 -0.349883
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-22)2020-05-01 00:00:00+00:00 -0.193702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-23)2020-06-01 00:00:00+00:00 -0.149037
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-24)2020-07-01 00:00:00+00:00 -0.222909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-25)2020-08-01 00:00:00+00:00 -0.156360
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-26)2020-09-01 00:00:00+00:00 -0.184705
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-27)2020-10-01 00:00:00+00:00 -0.264255
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-28)2020-11-01 00:00:00+00:00 -0.335702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-29)2020-12-01 00:00:00+00:00 -0.400262
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-11-30)Freq: MS, dtype: float64
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

You can think of meta methods as flexible siblings of regular methods: they act as micro-pipelines that take an arbitrary number of arrays and allow us to select the elements of those array as we wish. If we place a print statement in `mdd_nb` to print out `from_i`, `to_i`, and `col`, we would get:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-1)0 744 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-2)744 1434 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-3)1434 2177 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-4)2177 2895 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-5)2895 3639 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-6)3639 4356 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-7)4356 5100 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-8)5100 5844 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-9)5844 6564 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-10)6564 7308 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-11)7308 8027 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-12-12)8027 8767 0
 
[/code]

Each of those lines is a separate `mdd_nb` call, while the first two indices in each line denote the absolute start and end index we should select from data. Since we used `MS` as a target frequency, `from_i` and `to_i` denote the start and end of the month respectively. We can actually prove this:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-1)>>> h1_high.iloc[0:744] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-3)2020-01-01 00:00:00+00:00 7196.25
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-4)2020-01-01 01:00:00+00:00 7230.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-5)2020-01-01 02:00:00+00:00 7244.87
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-6)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-7)2020-01-31 21:00:00+00:00 9373.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-8)2020-01-31 22:00:00+00:00 9430.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-9)2020-01-31 23:00:00+00:00 9419.96
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-10)Name: High, Length: 744, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-12)>>> h1_low.iloc[0:744].min() / h1_high.iloc[0:744].max() - 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-13-13)-0.28262267696805177
 
[/code]

 1. 

The same example using [GenericAccessor.resample_between_bounds](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_between_bounds):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-1)>>> target_lbound_index = vbt.date_range("2020-01-01", "2020-12-01", freq="M", tz="UTC", inclusive="both")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-2)>>> target_rbound_index = vbt.date_range("2020-02-01", "2021-01-01", freq="M", tz="UTC", inclusive="both")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-3)>>> vbt.pd_acc.resample_between_bounds(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-4)... target_lbound_index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-5)... target_rbound_index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-6)... mdd_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-7)... vbt.Rep('high'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-8)... vbt.Rep('low'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-9)... broadcast_named_args=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-10)... high=h1_high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-11)... low=h1_low
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-14)2020-01-01 00:00:00+00:00 -0.282623
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-15)2020-02-01 00:00:00+00:00 -0.195714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-16)2020-03-01 00:00:00+00:00 -0.588362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-17)2020-04-01 00:00:00+00:00 -0.349883
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-18)2020-05-01 00:00:00+00:00 -0.193702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-19)2020-06-01 00:00:00+00:00 -0.149037
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-20)2020-07-01 00:00:00+00:00 -0.222909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-21)2020-08-01 00:00:00+00:00 -0.156360
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-22)2020-09-01 00:00:00+00:00 -0.184705
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-23)2020-10-01 00:00:00+00:00 -0.264255
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-24)2020-11-01 00:00:00+00:00 -0.335702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-25)2020-12-01 00:00:00+00:00 -0.400262
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-14-26)Freq: MS, dtype: float64
 
[/code]

Sky is the limit when it comes to possibilities that vectorbt enables for analysis ![🌌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f30c.svg)


# Numba[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#numba "Permanent link")

90% of functionality in vectorbt is compiled with Numba. To avoid using the high-level API and dive deep into the world of Numba, just look up in the documentation the Numba-compiled function used by the accessor function you want to use. For example, [GenericAccessor.resample_between_bounds](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_between_bounds) first generates index ranges using [map_bounds_to_source_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/nb/#vectorbtpro.base.resampling.nb.map_bounds_to_source_ranges_nb) and then uses [reduce_index_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/resample/#vectorbtpro.generic.nb.apply_reduce.reduce_index_ranges_nb) for generic calls and [reduce_index_ranges_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/resample/#vectorbtpro.generic.nb.apply_reduce.reduce_index_ranges_meta_nb) for meta calls. Let's run the same meta function as above:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-1)>>> from vectorbtpro.base.resampling.nb import map_bounds_to_source_ranges_nb
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-3)>>> range_starts, range_ends = map_bounds_to_source_ranges_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-4)... source_index=h1_high.index.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-5)... target_lbound_index=target_lbound_index.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-6)... target_rbound_index=target_rbound_index.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-7)... closed_lbound=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-8)... closed_rbound=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-10)>>> np.column_stack((range_starts, range_ends)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-11)array([[ 0, 744],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-12) [ 744, 1434],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-13) [1434, 2177],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-14) [2177, 2895],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-15) [2895, 3639],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-16) [3639, 4356],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-17) [4356, 5100],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-18) [5100, 5844],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-19) [5844, 6564],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-20) [6564, 7308],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-21) [7308, 8027],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-22) [8027, 8767]])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-23)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-24)>>> ms_mdd_arr = vbt.nb.reduce_index_ranges_meta_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-25)... 1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-26)... range_starts,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-27)... range_ends,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-28)... mdd_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-29)... vbt.to_2d_array(h1_high), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-30)... vbt.to_2d_array(h1_low)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-31)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-32)>>> ms_mdd_arr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-33)array([[-0.28262268],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-34) [-0.19571429],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-35) [-0.58836199],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-36) [-0.34988266],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-37) [-0.1937022 ],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-38) [-0.14903661],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-39) [-0.22290895],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-40) [-0.15636028],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-41) [-0.18470481],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-42) [-0.26425532],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-43) [-0.33570238],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-15-44) [-0.40026177]])
 
[/code]

 1. 2. 3. 4. 5. 

That's the fastest execution we can get. We can then wrap the array as follows:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-1)>>> pd.Series(ms_mdd_arr[:, 0], index=target_lbound_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-2)2020-01-01 00:00:00+00:00 -0.282623
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-3)2020-02-01 00:00:00+00:00 -0.195714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-4)2020-03-01 00:00:00+00:00 -0.588362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-5)2020-04-01 00:00:00+00:00 -0.349883
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-6)2020-05-01 00:00:00+00:00 -0.193702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-7)2020-06-01 00:00:00+00:00 -0.149037
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-8)2020-07-01 00:00:00+00:00 -0.222909
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-9)2020-08-01 00:00:00+00:00 -0.156360
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-10)2020-09-01 00:00:00+00:00 -0.184705
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-11)2020-10-01 00:00:00+00:00 -0.264255
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-12)2020-11-01 00:00:00+00:00 -0.335702
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-13)2020-12-01 00:00:00+00:00 -0.400262
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-16-14)Freq: MS, dtype: float64
 
[/code]


# Caveats[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#caveats "Permanent link")

As we already discussed in [Alignment](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment), each timestamp is the open time and information at that timestamp happens somewhere between this timestamp and the next one. We shouldn't worry about this if we downsample to a frequency that is an integer multiplier of the source frequency. For example, consider downsampling two days of `H4` data to `D1` time frame:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-1)>>> h4_close_2d = h4_close.iloc[:12]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-2)>>> h4_close_2d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-3)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-4)2020-01-01 00:00:00+00:00 7225.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-5)2020-01-01 04:00:00+00:00 7209.83
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-6)2020-01-01 08:00:00+00:00 7197.20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-7)2020-01-01 12:00:00+00:00 7234.19
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-8)2020-01-01 16:00:00+00:00 7229.48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-9)2020-01-01 20:00:00+00:00 7200.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-10)2020-01-02 00:00:00+00:00 7129.61
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-11)2020-01-02 04:00:00+00:00 7110.57
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-12)2020-01-02 08:00:00+00:00 7139.79
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-13)2020-01-02 12:00:00+00:00 7130.98
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-14)2020-01-02 16:00:00+00:00 6983.27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-15)2020-01-02 20:00:00+00:00 6965.71
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-16)Freq: 4H, Name: Close, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-18)>>> h4_close_2d.resample("1d").last()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-19)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-20)2020-01-01 00:00:00+00:00 7200.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-21)2020-01-02 00:00:00+00:00 6965.71
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-17-22)Freq: D, Name: Close, dtype: float64
 
[/code]

This operation is correct: `7200.85` is the last value of `2020-01-01` and `6965.71` is the last value of `2020-01-02`. But what happens if we change `H4` to `H5`? Nothing good:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-1)>>> h5_close = h1_close.resample("5h").last()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-2)>>> h5_close_2d = h5_close.iloc[:10]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-3)>>> h5_close_2d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-4)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-5)2020-01-01 00:00:00+00:00 7217.27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-6)2020-01-01 05:00:00+00:00 7188.77
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-7)2020-01-01 10:00:00+00:00 7221.43
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-8)2020-01-01 15:00:00+00:00 7229.48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-9)2020-01-01 20:00:00+00:00 7211.02
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-10)2020-01-02 01:00:00+00:00 7138.93
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-11)2020-01-02 06:00:00+00:00 7161.83
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-12)2020-01-02 11:00:00+00:00 7130.98
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-13)2020-01-02 16:00:00+00:00 6948.49
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-14)2020-01-02 21:00:00+00:00 6888.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-15)Freq: 5H, Name: Close, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-17)>>> h5_close_2d.resample("1d").last()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-18)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-19)2020-01-01 00:00:00+00:00 7211.02
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-20)2020-01-02 00:00:00+00:00 6888.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-18-21)Freq: D, Name: Close, dtype: float64
 
[/code]

Try spotting the issue and come back once you found it (or not)...

Pandas resampler thinks that information at each timestamp happens exactly at that timestamp, and so it chose the latest value of the first day to be at the latest timestamp of that day - `2020-01-01 20:00:00`. But this is a no-go for us! The timestamp `2020-01-01 20:00:00` holds the close price, which happens right before the next timestamp, or `2020-01-02 01:00:00` on the next day. This value is still unavailable at the end of the first day. Using this information that early means looking into the future, and producing unreliable backtesting results.

This happens only when the target frequency cannot be divided by the source frequency without a leftover:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-19-1)>>> vbt.timedelta("1d") % vbt.timedelta("1h") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-19-2)Timedelta('0 days 00:00:00')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-19-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-19-4)>>> vbt.timedelta("1d") % vbt.timedelta("4h") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-19-5)Timedelta('0 days 00:00:00')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-19-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-19-7)>>> vbt.timedelta("1d") % vbt.timedelta("5h") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-19-8)Timedelta('0 days 04:00:00')
 
[/code]

 1. 2. 3. 

But the solution is rather simple: make each timestamp be the close time instead of the open time. Logically, the close time is just the next timestamp minus one nanosecond (the smallest timedelta possible):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-1)>>> h5_close_time = h5_close_2d.index.shift("5h") - pd.Timedelta(nanoseconds=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-2)>>> h5_close_time.name = "Close time"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-3)>>> h5_close_2d.index = h5_close_time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-4)>>> h5_close_2d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-5)Close time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-6)2020-01-01 04:59:59.999999999+00:00 7217.27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-7)2020-01-01 09:59:59.999999999+00:00 7188.77
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-8)2020-01-01 14:59:59.999999999+00:00 7221.43
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-9)2020-01-01 19:59:59.999999999+00:00 7229.48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-10)2020-01-02 00:59:59.999999999+00:00 7211.02
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-11)2020-01-02 05:59:59.999999999+00:00 7138.93
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-12)2020-01-02 10:59:59.999999999+00:00 7161.83
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-13)2020-01-02 15:59:59.999999999+00:00 7130.98
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-14)2020-01-02 20:59:59.999999999+00:00 6948.49
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-15)2020-01-03 01:59:59.999999999+00:00 6888.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-20-16)Freq: 5H, Name: Close, dtype: float64
 
[/code]

Each timestamp is now guaranteed to produce a correct resampling operation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-21-1)>>> h5_close_2d.resample("1d").last()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-21-2)Close time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-21-3)2020-01-01 00:00:00+00:00 7229.48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-21-4)2020-01-02 00:00:00+00:00 6948.49
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-21-5)2020-01-03 00:00:00+00:00 6888.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-21-6)Freq: D, Name: Close, dtype: float64
 
[/code]

Note

Whenever using the close time, don't specify the right bound when resampling with vectorbt methods. For instance, instead of using [GenericAccessor.realign_closing](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_closing), you're now safe to use [GenericAccessor.realign_opening](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_opening).


# Portfolio[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#portfolio "Permanent link")

Whenever working with portfolios, we must distinguish between two time frames: the one used during simulation and the one used during analysis (or reconstruction). By default, both time frames are equal. But using a special command, we can execute the trading strategy using a more granular data and then downsample the simulated data for analysis. This brings two key advantages:

 1. Using a shorter time frame during simulation, we can place a lot more orders more precisely
 2. Using a longer time frame during analysis, we can cut down memory consumption and processing time

Let's simulate a simple crossover strategy on `H1` data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-22-1)>>> fast_sma = vbt.talib("SMA").run(h1_close, timeperiod=vbt.Default(10))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-22-2)>>> slow_sma = vbt.talib("SMA").run(h1_close, timeperiod=vbt.Default(20))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-22-3)>>> entries = fast_sma.real_crossed_above(slow_sma.real)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-22-4)>>> exits = fast_sma.real_crossed_below(slow_sma.real)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-22-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-22-6)>>> pf = vbt.Portfolio.from_signals(h1_close, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-22-7)>>> pf.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/h1_pf.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/h1_pf.dark.svg#only-dark)

Computing the returns of a portfolio involves reconstructing many attributes, including the cash flow, cash, asset flow, asset value, value, and finally returns. This cascade of reconstructions may become a bottleneck if the input data, such as tick data, is too granular. Luckily, there is a brandnew method [Wrapping.resample](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resample), which allows us to resample vectorbt objects of arbitrary complexity (as long as resampling is possible and logically justifiable). Here, we are resampling the portfolio to the start of each month:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-23-1)>>> ms_pf = pf.resample("M")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-23-2)>>> ms_pf.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/ms_pf.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/ms_pf.dark.svg#only-dark)

The main artifacts of a simulation are the close price, order records, and additional inputs such as cash deposits and earnings. Whenever we trigger a resampling job, the close price and those additional inputs are resampled pretty easily using a bunch of `last` and `sum` operations. 

The order records, on the other hand, are more complex in nature: they are structured NumPy arrays (similar to a Pandas DataFrame) that hold order information at each row. The timestamp of each order is stored in a separate column of that array, such that we can have multiple orders at the same timestamp. This means that we can resample such records simply by re-indexing their timestamp column to the target index, which is done using [Resampler.map_to_target_index](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.map_to_target_index).

After resampling the artifacts, a new [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) instance is created, and the attributes such as returns are reconstructed on the new data. This is a perfect example of why vectorbt reconstructs all attributes after the simulation and not during the simulation like many conventional backtesters do. 

To prove that we can trust the results:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-24-1)>>> pf.total_return
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-24-2)2.735083772113918
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-24-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-24-4)>>> ms_pf.total_return
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-24-5)2.735083772113918
 
[/code]

Or by comparing the resampled returns of the original portfolio to the returns of the resampled portfolio:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-1)>>> (1 + pf.returns).resample(vbt.offset("M")).apply(lambda x: x.prod() - 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-3)2020-01-01 00:00:00+00:00 0.150774
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-4)2020-02-01 00:00:00+00:00 0.057471
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-5)2020-03-01 00:00:00+00:00 -0.005920
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-6)2020-04-01 00:00:00+00:00 0.144156
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-7)2020-05-01 00:00:00+00:00 0.165367
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-8)2020-06-01 00:00:00+00:00 -0.015025
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-9)2020-07-01 00:00:00+00:00 0.179079
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-10)2020-08-01 00:00:00+00:00 0.084451
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-11)2020-09-01 00:00:00+00:00 -0.018819
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-12)2020-10-01 00:00:00+00:00 0.064898
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-13)2020-11-01 00:00:00+00:00 0.322020
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-14)2020-12-01 00:00:00+00:00 0.331068
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-15)Freq: MS, Name: Close, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-17)>>> ms_pf.returns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-18)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-19)2020-01-01 00:00:00+00:00 0.150774
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-20)2020-02-01 00:00:00+00:00 0.057471
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-21)2020-03-01 00:00:00+00:00 -0.005920
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-22)2020-04-01 00:00:00+00:00 0.144156
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-23)2020-05-01 00:00:00+00:00 0.165367
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-24)2020-06-01 00:00:00+00:00 -0.015025
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-25)2020-07-01 00:00:00+00:00 0.179079
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-26)2020-08-01 00:00:00+00:00 0.084451
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-27)2020-09-01 00:00:00+00:00 -0.018819
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-28)2020-10-01 00:00:00+00:00 0.064898
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-29)2020-11-01 00:00:00+00:00 0.322020
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-30)2020-12-01 00:00:00+00:00 0.331068
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-25-31)Freq: MS, Name: Close, dtype: float64
 
[/code]

Hint

Actually, since returns are reconstructed all the way up from order records and involve so many other attributes, having identical results like this shows that the entire implementation of vectorbt is algorithmically correct ![😏](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f60f.svg)

BTW If you're wondering how to aggregate those P&L values on the graph, do the following:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-1)>>> ms_pf.trades.pnl.to_pd(reduce_func_nb="sum") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-3)2020-01-01 00:00:00+00:00 15.077357
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-4)2020-02-01 00:00:00+00:00 6.613564
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-5)2020-03-01 00:00:00+00:00 -0.113362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-6)2020-04-01 00:00:00+00:00 16.831599
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-7)2020-05-01 00:00:00+00:00 22.888280
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-8)2020-06-01 00:00:00+00:00 -2.502485
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-9)2020-07-01 00:00:00+00:00 26.603047
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-10)2020-08-01 00:00:00+00:00 18.804921
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-11)2020-09-01 00:00:00+00:00 -6.180621
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-12)2020-10-01 00:00:00+00:00 10.133302
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-13)2020-11-01 00:00:00+00:00 35.891558
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-14)2020-12-01 00:00:00+00:00 129.461217
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#__codelineno-26-15)Freq: MS, Name: Close, dtype: float64
 
[/code]

 1. 


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/aggregation/#summary "Permanent link")

We should keep in mind that when working with bars, any information stored under a timestamp doesn't usually happen exactly at that point in time - it happens somewhere in between this timestamp and the next one. This may sound very basic, but this fact changes the resampling logic drastically since now we have to be very careful to not catch the look-ahead bias when aligning multiple time frames. Gladly, vectorbt implements a range of highly-optimized functions that can take this into account and make our lives easier!

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/mtf-analysis/aggregation.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/MTFAnalysis.ipynb)