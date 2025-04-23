# Splitter[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#splitter "Permanent link")

The manual approach that we did previously can be decomposed into three distinctive steps: splitting the whole period into sub-periods, applying a UDF on each sub-period and merging its outputs, and analyzing the merged outputs using available data science tools. The first and the second step can be well automated; for example, [scikit-learn](https://scikit-learn.org/stable/) has a range of [classes for cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html), each taking an array and performing some job on chunks of that array. The issue with that (otherwise excellent) Python package is that it lacks robust CV schemes for time series data, charting and analysis tools for split distributions, as well as an easy-to-extend interface for custom use cases. It also focuses on machine learning (ML) models that are trained on one data and validated on another by doing predictions (that's why it's called scikit-_learn_ , after all), while rule-based algorithms that aren't predicting but producing a range of scores (one per test rather than data point) aren't receiving enough love.

That's why vectorbt needs to go its own way and implement a functionality cut to the needs of quantitative analysts rather than ML enthusiasts. At the heart of this functionality is the class [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter), whose main responsibility is to produce arbitrary splits and perform operations on those splits. The workings of this class are dead-simple: the user calls one of the class methods with the prefix `from_` (sounds familiar, right?) to generate splits; in return, a splitter instance is returned with splits and their labels being saved in a memory-efficient array format. This instance can be used to analyze the split distribution, to chunk array-like objects, and to run UDFs. Get yourself ready, because this class alone has twice as many lines of code as the entire [backtesting.py](https://github.com/kernc/backtesting.py) library ![😈](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f608.svg)

Let's create a splitter for the schema of our first example:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-0-1)>>> splitter = vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-0-2)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-0-3)... length=360, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-0-4)... split=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-0-5)... set_labels=["IS", "OOS"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-0-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-0-7)>>> splitter.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/splitter.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/splitter.dark.svg#only-dark)

That's it! We've got a splitter that can manipulate the periods (blue and orange boxes on the plot) and the data under those periods to our liking - no more while-loops. But before we dive into the dozens of implemented generation and analysis techniques, let's take a look under the hood and make ourselves comfortable with some basic concepts first.


# Schema[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#schema "Permanent link")

The smallest unit of a splitter is a _range_ , which is a period of time that can be mapped onto data. On the plot above, we can count a total of 18 ranges - 9 blue ones and 9 orange ones. Multiple ranges next to each other and representing a single test are called a _split_ ; there are 9 splits present in the chart, such that we expect one pipeline to be tested on 9 different data ranges. Different range types within each split are called _sets_. Usually, there is either one set, two sets - "training" and "test" (commonly used in backtesting), or three sets - "training", "validation", and "test" (commonly used in ML). The number of sets is fixed throughout all splits.

This schema fits perfectly into the philosophy of vectorbt because we can represent things in an array format where rows are splits, columns are sets, and elements are ranges:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-1)>>> splitter.splits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-2)set IS OOS
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-3)split 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-4)0 slice(0, 180, None) slice(180, 360, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-5)1 slice(180, 360, None) slice(360, 540, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-6)2 slice(360, 540, None) slice(540, 720, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-7)3 slice(540, 720, None) slice(720, 900, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-8)4 slice(720, 900, None) slice(900, 1080, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-9)5 slice(900, 1080, None) slice(1080, 1260, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-10)6 slice(1080, 1260, None) slice(1260, 1440, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-11)7 slice(1260, 1440, None) slice(1440, 1620, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-1-12)8 slice(1440, 1620, None) slice(1620, 1800, None)
 
[/code]

Notice how the index are split labels and columns are set labels: in contrast to other classes in vectorbt, the wrapper of this class doesn't represent time and assets, but splits and sets. Time is being tracked separately as [Splitter.index](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.index) while assets aren't being tracked at all since they have no implications on splitting.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-1)>>> splitter.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-2)DatetimeIndex(['2017-08-17 00:00:00+00:00', '2017-08-18 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-3) '2017-08-19 00:00:00+00:00', '2017-08-20 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-4) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-5) '2022-10-28 00:00:00+00:00', '2022-10-29 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-6) '2022-10-30 00:00:00+00:00', '2022-10-31 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-7) dtype='datetime64[ns, UTC]', name='Open time', length=1902, freq='D')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-9)>>> splitter.wrapper.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-10)RangeIndex(start=0, stop=9, step=1, name='split')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-12)>>> splitter.wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-2-13)Index(['IS', 'OOS'], dtype='object', name='set')
 
[/code]

Such a design has one nice property: we can apply indexing directly on a splitter instance to select specific splits and sets. Let's select the OOS set:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-1)>>> oos_splitter = splitter["OOS"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-2)>>> oos_splitter.splits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-3)split
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-4)0 slice(180, 360, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-5)1 slice(360, 540, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-6)2 slice(540, 720, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-7)3 slice(720, 900, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-8)4 slice(900, 1080, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-9)5 slice(1080, 1260, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-10)6 slice(1260, 1440, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-11)7 slice(1440, 1620, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-12)8 slice(1620, 1800, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-3-13)Name: OOS, dtype: object
 
[/code]

This operation has created a completely new splitter for OOS ranges ![😮](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f62e.svg)

Why bother? Because we can select one set and apply a UDF on it, and then select the next set and apply a completely different UDF on it. Sounds like a prerequisite for CV, right?


# Range format[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#range-format "Permanent link")

So, how do ranges look like? In the first example of this tutorial, we used a start and end date to slice the data using `loc`. But as we also learned that the end date in a `loc` operation should be inclusive, which makes it annoyingly difficult to make sure that neighboring ranges do not overlap. Also, dates cannot be used to slice NumPy arrays, unless they are translated into positions beforehand. That's why the splitter does integer-location based indexing and accepts the following range formats that can be used to slice both Pandas (using [pandas.DataFrame.iloc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html)) and NumPy arrays:

 * A list or array of integers, e.g. `[4, 3, 0]`
 * A slice object with ints, e.g. `slice(1, 7)`
 * A boolean array
 * A callable function with one argument (the calling Series or DataFrame) and that returns valid output for indexing (one of the above)

For example, the slice `slice(1, 7)` covers the indices `[0, 1, 2, 3, 4, 5, 6]`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-1)>>> index = vbt.date_range("2020", periods=14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-2)>>> index[slice(1, 7)] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-3)DatetimeIndex(['2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-4) '2020-01-06', '2020-01-07'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-5) dtype='datetime64[ns]', freq='D')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-7)>>> index[1], index[6]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-8)(Timestamp('2020-01-02 00:00:00', freq='D'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-4-9) Timestamp('2020-01-07 00:00:00', freq='D'))
 
[/code]

 1. 

Having the index and integer-location based ranges kept separately makes designing non-overlapping, bug-free ranges super-easy.


# Relative[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#relative "Permanent link")

The range format introduced above is called "fixed" because ranges do not depend on each other. But there's another range format called "relative" that makes one range depend on the previous range. For example, instead of defining a range between fixed index positions `110` and `150`, we can issue an instruction to create a range that starts `10` points after the end point of the previous range and has the length of `40`. Such an instruction can be created using [RelRange](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.RelRange):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-1)>>> rel_range = vbt.RelRange(offset=10, length=40)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-2)>>> rel_range
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-3)RelRange(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-4) offset=10, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-5) offset_anchor='prev_end', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-6) offset_space='free', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-7) length=40, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-8) length_space='free', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-9) out_of_bounds='warn',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-10) is_gap=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-5-11))
 
[/code]

This instruction will be evaluated later in time by calling [RelRange.to_slice](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.RelRange.to_slice):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-6-1)>>> rel_range.to_slice(total_len=len(splitter.index), prev_end=100) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-6-2)slice(110, 150, None)
 
[/code]

 1. 

Relative ranges are usually converted into fixed ones prior to constructing a splitter instance, but splitter instances can also hold relative ranges in case this is wanted by the user.


# Array format[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#array-format "Permanent link")

But how do we store such range formats efficiently? The most flexible range formats are apparently indices and masks because they allow gaps and can enable a more traditional [k-fold cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html), but they may also produce a huge memory footprint even for simple use cases. For example, consider a range stretching over 1 year of 1-minute data; it would take roughly 4MB of RAM as an integer array and 0.5MB as a mask:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-7-1)>>> index = vbt.date_range("2020", "2021", freq="1min")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-7-2)>>> range_ = np.arange(len(index))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-7-3)>>> range_.nbytes / 1024 / 1024
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-7-4)4.02099609375
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-7-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-7-6)>>> range_ = np.full(len(index), True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-7-7)>>> range_.nbytes / 1024 / 1024
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-7-8)0.50262451171875
 
[/code]

This means that only 100 splits and 2 sets would consume 800MB and 100MB of RAM respectively, and this is only to keep the splitter metadata in memory! Moreover, most "ranges" don't need to be that complex: they have predefined start and end points (that should occupy at most 18 bytes of memory), while being capable of pulling the same exact period of data as their integer and boolean array counterparts. That's why the [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) class tries to convert any array into a slice, by the way.

To make sure that the user can make use of lightweight ranges, complex arrays, and relative ranges using the same API, the array that holds ranges has an object data type:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-8-1)>>> splitter.splits_arr.dtype 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-8-2)dtype('O')
 
[/code]

 1. 

Info

If an element of an array is a complex object, it doesn't mean that the array holds this entire object - it only holds the [reference](https://realpython.com/lessons/object-value-vs-object-identity/) to that object:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-9-1)>>> id(slice(0, 180, None))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-9-2)140627839366784
 
[/code]

The object data type is completely legit; it only becomes a burden once attempted to be passed to Numba, but the splitting functionality is entirely written in Python because the number of ranges (splits x sets) is usually kept relatively low such that the main bottleneck lies in running UDFs and not in iterating over ranges (and no worries, UDFs can still be run in Numba ![😌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f60c.svg)) The other drawback is that the array cannot be numerically processed with NumPy or Pandas anymore, but that's why we have [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) that can extract the meaning out of such an array!

This array format has even more benefits: we can use different range formats across different splits, we can store index arrays of different lengths, and since the `splits` array only stores references, we don't need to duplicate an array if two range values are pointing to the same array object. For example, let's construct a splitter where (differently-sized) ranges are stored as integer-location based arrays:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-1)>>> range_00 = np.arange(0, 5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-2)>>> range_01 = np.arange(5, 15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-3)>>> range_10 = np.arange(15, 30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-4)>>> range_11 = np.arange(30, 50)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-6)>>> ind_splitter = vbt.Splitter.from_splits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-7)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-8)... [[range_00, range_01], [range_10, range_11]],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-9)... fix_ranges=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-11)>>> ind_splitter.splits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-12)set set_0 \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-13)split 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-14)0 FixRange(range_=array([0, 1, 2, 3, 4])) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-15)1 FixRange(range_=array([15, 16, 17, 18, 19, 20,... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-17)set set_1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-18)split 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-19)0 FixRange(range_=array([ 5, 6, 7, 8, 9, 10,... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-20)1 FixRange(range_=array([30, 31, 32, 33, 34, 35,... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-21)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-22)>>> ind_splitter.splits.loc[0, "set_1"] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-23)FixRange(range_=array([20, 21, 22, 23, 24, 25, 26, 27, 28, 29]))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-24)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-25)>>> ind_splitter.splits.loc[0, "set_1"].range_ 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-10-26)array([20, 21, 22, 23, 24, 25, 26, 27, 28, 29])
 
[/code]

 1. 2. 

Hint

Why is the value of [FixRange](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.FixRange) called `range_` and not `range`? Because `range` is a reserved keyword in Python.

As we see, each element of the splits array is... a NumPy array wrapped with [FixRange](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.FixRange), which is perfectly fine. Why are arrays wrapped and slices not? Because sub-arrays would expand the entire array to three dimensions, which are disliked by Pandas.


# Preparation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#preparation "Permanent link")

In a nutshell, a splitter instance keeps track of three objects:

 1. `wrapper` \- Wrapper with split and set labels ([ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper))
 2. `index` \- Data index (mostly [pandas.DatetimeIndex](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html))
 3. `splits` \- Two-dimensional NumPy array with range objects

Although we can prepare these objects manually, there are convenient methods that automate this workflow for us. The base class method that most other class methods are based upon is [Splitter.from_splits](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_splits), which takes a sequence of splits, optionally does some pre-processing on each split, and converts that sequence into a suitable array format. It also prepares the labels and the wrapper. But let's focus on preparing the splits first.


# Splits[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#splits "Permanent link")

Splitting is a process of dividing a bigger range into chunks of smaller ranges, which is implemented by the method [Splitter.split_range](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_range). What it takes is a fixed range `range_` and a split specification `new_split`, and returns a tuple of new fixed ranges. Keep in mind that the returned ranges are always fixed, hence this method is also used to convert relative ranges to fixed. But the main use case of this method is to check whether the provided specification makes any sense and doesn't violate any bounds. Let's generate two ranges: one that takes 75% of space and another that takes the remaining 25%.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-11-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-11-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-11-3)... (vbt.RelRange(length=0.75), vbt.RelRange()), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-11-4)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-11-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-11-6)(slice(0, 1426, None), slice(1426, 1902, None))
 
[/code]

 1. 2. 

Hint

This method is a hybrid method: it can be called both as a class method and instance method. If the latter, we don't need to provide the index since it's already stored:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-12-1)>>> splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-12-2)... slice(None),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-12-3)... (vbt.RelRange(length=0.75), vbt.RelRange())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-12-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-12-5)(slice(0, 1426, None), slice(1426, 1902, None))
 
[/code]

These two slices can then be used to slice the data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-13-1)>>> data[slice(0, 1426, None)] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-13-2)<vectorbtpro.data.custom.binance.BinanceData at 0x7fe12a7df310>
 
[/code]

 1. 

The two relative ranges can be substituted by just one number, which translates into the length reserved for the first range, while the second range gets the remaining space:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-14-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-14-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-14-3)... 0.75, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-14-4)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-14-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-14-6)(slice(0, 1426, None), slice(1426, 1902, None))
 
[/code]

Very often in CV, we want to fix the length of the OOS period and put everything else to the IS period. This can be specified by a negative number, which effectively reverses the processing order. For example, let's set the length of the OOS period to 25%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-15-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-15-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-15-3)... -0.25,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-15-4)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-15-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-15-6)(slice(0, 1427, None), slice(1427, 1902, None))
 
[/code]

Hint

Why are both results not identical? Because of rounding:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-16-1)>>> int(0.75 * len(data.index))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-16-2)1426
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-16-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-16-4)>>> len(data.index) - int(0.25 * len(data.index))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-16-5)1427
 
[/code]

Or manually:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-17-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-17-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-17-3)... (vbt.RelRange(), vbt.RelRange(length=0.25)),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-17-4)... backwards=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-17-5)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-17-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-17-7)(slice(0, 1427, None), slice(1427, 1902, None))
 
[/code]

Relative ranges with just the length defined can be substituted by numbers for more convenience. For example, make the OOS period 30 data points long:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-18-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-18-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-18-3)... (1.0, 30), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-18-4)... backwards=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-18-5)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-18-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-18-7)(slice(0, 1872, None), slice(1872, 1902, None))
 
[/code]

Hint

How does the method decide whether the length is relative or absolute? If the number is between 0 and 1, the length is relative to the surrounding space, otherwise it reflects the number of data points.

When using relative lengths, we can also specify the space the length should be relative to using [RelRange.length_space](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.RelRange.length_space). By default, a length is relative to the remaining space (i.e., from the right-most bound of the previous range to the right-most bound of the whole period), but we can force it to be relative to the entire space instead. For example, let's define three ranges with 40%, 40%, and 20% respectively:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-3)... (
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-4)... vbt.RelRange(length=0.4, length_space="all"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-5)... vbt.RelRange(length=0.4, length_space="all"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-6)... vbt.RelRange()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-7)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-8)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-19-10)(slice(0, 760, None), slice(760, 1520, None), slice(1520, 1902, None))
 
[/code]

To introduce a gap between two ranges, we can use an offset. Similarly to lengths, offsets can be relative or absolute too. Also, offsets have an anchor, which defaults to the right-most bound of the previous range (if any, otherwise 0). Let's require both ranges to have a gap of 1 point:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-20-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-20-2)... slice(None),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-20-3)... (vbt.RelRange(length=0.75), vbt.RelRange(offset=1)),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-20-4)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-20-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-20-6)(slice(0, 1426, None), slice(1427, 1902, None))
 
[/code]

The exact same result can be achieved by placing a relative range of 1 data point between both ranges and enabling [RelRange.is_gap](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.RelRange.is_gap):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-3)... (
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-4)... vbt.RelRange(length=0.75), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-5)... vbt.RelRange(length=1, is_gap=True),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-6)... vbt.RelRange()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-7)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-8)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-21-10)(slice(0, 1426, None), slice(1427, 1902, None))
 
[/code]

This method's power is not only in converting relative ranges into fixed ones, but also in trying to optimize the target ranges for best memory efficiency. Let's make the first range an array without gaps and the second range an array with gaps, and see what happens:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-22-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-22-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-22-3)... (np.array([3, 4, 5]), np.array([6, 8, 10])),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-22-4)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-22-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-22-6)(slice(3, 6, None), array([ 6, 8, 10]))
 
[/code]

We can see that the method was successful in optimizing the first array into a slice, but not the second. If such a conversion is not desired, we can disable it using the argument `range_format`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-23-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-23-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-23-3)... (np.array([3, 4, 5]), np.array([6, 8, 10])),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-23-4)... range_format="indices",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-23-5)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-23-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-23-7)(array([3, 4, 5]), array([ 6, 8, 10]))
 
[/code]

Since [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) uses integer-location and mask based indexing under the hood, we cannot use dates and times to slice arrays. Gladly, [Splitter.split_range](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_range) can take any slices and arrays as `pd.Timestamp`, `np.datetime64`, `datetime.datetime`, and even datetime-looking strings, and convert them into integers for us! It even takes care of the timezone.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-3)... (slice("2020", "2021"), slice("2021", "2022")), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-4)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-6)(slice(867, 1233, None), slice(1233, 1598, None))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-8)>>> data.index[867:1233]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-9)DatetimeIndex(['2020-01-01 00:00:00+00:00', ..., '2020-12-31 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-10) dtype='datetime64[ns, UTC]', name='Open time', length=366, freq='D')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-12)>>> data.index[1233:1598]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-13)DatetimeIndex(['2021-01-01 00:00:00+00:00', ..., '2021-12-31 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-24-14) dtype='datetime64[ns, UTC]', name='Open time', length=365, freq='D')
 
[/code]

 1. 

The same goes for relative ranges where the arguments `offset` and `length` can be provided as `pd.Timedelta`, `np.timedelta64`, `datetime.timedelta`, and timedelta-looking strings:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-1)>>> vbt.Splitter.split_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-2)... slice(None), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-3)... (
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-4)... vbt.RelRange(length="180 days"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-5)... vbt.RelRange(offset="1 day", length="90 days")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-6)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-7)... index=data.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-25-9)(slice(0, 180, None), slice(181, 271, None))
 
[/code]


# Method[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#method "Permanent link")

Back to [Splitter.from_splits](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_splits). We've learned that each split is being prepared by converting a split specification into a sequence of ranges, one per set. By passing multiple of such specifications, we thus get a two-dimensional array available under [Splitter.splits](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.splits). Let's manually generate expanding splits with a OOS set having a fixed length of 25%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-1)>>> manual_splitter = vbt.Splitter.from_splits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-3)... [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-4)... (vbt.RelRange(), vbt.RelRange(offset=0.5, length=0.25, length_space="all")), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-5)... (vbt.RelRange(), vbt.RelRange(offset=0.25, length=0.25, length_space="all")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-6)... (vbt.RelRange(), vbt.RelRange(offset=0, length=0.25, length_space="all")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-7)... ],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-8)... split_range_kwargs=dict(backwards=True), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-9)... set_labels=["IS", "OOS"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-11)>>> manual_splitter.splits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-12)set IS OOS
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-13)split 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-14)0 slice(0, 476, None) slice(476, 951, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-15)1 slice(0, 952, None) slice(952, 1427, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-16)2 slice(0, 1427, None) slice(1427, 1902, None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-26-18)>>> manual_splitter.plot().show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/manual_splitter.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/manual_splitter.dark.svg#only-dark)


# Generation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#generation "Permanent link")

We know how to build a splitter manually, but most CV schemes involve generation through iteration, just like we did with the while-loop in our first example. Moreover, the start point of a split usually depends on the preceding split, which would require us to explicitly call [Splitter.split_range](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_range) on each split to get its boundaries. To reduce the amount of a boilerplate code required to enable this workflow, [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) implements a collection of class methods, such as [Splitter.from_rolling](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_rolling), that can produce a logically-coherent schema from a simple user query.

Most of these methods first divide the entire period into windows (either in advance or iteratively), and then split each sub-period using the argument `split`, which is simply being passed to [Splitter.split_range](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_range) as `new_split`. This way, the split specification becomes relative the sub-period and not the entire period as we did above.

Info

Internally, `slice(None)` (that we used every time previously) is being replaced by the window slice such that `0.5` would split only the window in half, not the entire period.


# Rolling[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#rolling "Permanent link")

The most important method for CV is [Splitter.from_rolling](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_rolling), which deploys a simple while-loop that appends splits until any split exceeds the right bound of the index. If the last split has the length less than the one requested, it gets discarded, such that there is usually some unused space at the end of the backtesting period.

But the most interesting question is: where do we place the next split? By default, if there's only one set, the next split is placed right after the previous one. If there are multiple sets though, the next split is placed right after the first (IS) range in the previous split, such that IS ranges never overlap across splits. And of course, we can control the offset behavior using `offset_anchor_set` (which range in the previous split acts as an anchor?), `offset_anchor` (left or right bound of that range acts as an anchor?), `offset` (positive/negative distance from anchor), and `offset_space` (see [RelRange](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.RelRange)).

One setOne set with a gapOne set with overlapsTwo setsTwo sets without overlaps
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-27-1)>>> vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-27-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-27-3)... length=360, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-27-4)... ).plot().show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling1.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-28-1)>>> vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-28-2)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-28-3)... length=360,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-28-4)... offset=90 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-28-5)... ).plot().show()
 
[/code]

 1. Similarly to a length, an offset can also be a percentage (but relative to `offset_space`) and a duration

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling2.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-29-1)>>> vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-29-2)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-29-3)... length=360,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-29-4)... offset=-0.5 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-29-5)... ).plot().show()
 
[/code]

 1. In contrast to a length, an offset can also be negative (also duration, for example `"-180 days"`). Since `offset_space` defaults to the length of the previous split or anchor range, this will move the next window to the left by 50% of the previous window's length.

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling3.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling3.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-30-1)>>> vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-30-2)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-30-3)... length=360,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-30-4)... split=0.5 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-30-5)... ).plot().show()
 
[/code]

 1. Split instruction passed to [Splitter.split_range](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_range) to split each window. Here, allocate 50% for the first range and the remaining space for the second.

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling4.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling4.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-31-1)>>> vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-31-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-31-3)... length=360,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-31-4)... split=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-31-5)... offset_anchor_set=None 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-31-6)... ).plot().show()
 
[/code]

 1. Use the entire previous split (`set_0 + set_1`) as an anchor. Otherwise, it would use only the first range in that split (`set_0`).

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling5.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_rolling5.dark.svg#only-dark)

Another popular approach is by dividing the entire period into `n` equally-spaced, potentially-overlapping windows, which is implemented by [Splitter.from_n_rolling](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_n_rolling). If the length of the window is `None` (i.e., not provided), it simply calls [Splitter.from_rolling](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_rolling) with the length set to `len(index) // n`. Note that in contrast to the previous method, this one doesn't allow us to control the offset.

Without lengthWith length and without overlapsWith length and with overlaps
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-32-1)>>> vbt.Splitter.from_n_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-32-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-32-3)... n=5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-32-4)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-32-5)... ).plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_rolling1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_rolling1.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-33-1)>>> vbt.Splitter.from_n_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-33-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-33-3)... n=3, 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-33-4)... length=360,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-33-5)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-33-6)... ).plot().show()
 
[/code]

 1. Splits are not overlapping when `n` is small enough

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_rolling2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_rolling2.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-34-1)>>> vbt.Splitter.from_n_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-34-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-34-3)... n=7, 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-34-4)... length=360,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-34-5)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-34-6)... ).plot().show()
 
[/code]

 1. Splits are overlapping when `n` is big enough

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_rolling3.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_rolling3.dark.svg#only-dark)

The windows that we've generated above have all the same length, which makes it easier to conduct fair experiments in backtesting. But sometimes, especially when training ML models, we need every training period to incorporate all the previous history. Such windows are called expanding and can be generated automatically using [Splitter.from_expanding](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_expanding), which works similarly to its rolling counterpart except that the offset controls the number of windows, the offset anchor is always the end of the previous split (window), and there's an argument `min_length` for a minimum window length. There's also a method [Splitter.from_n_expanding](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_n_expanding) that allows us to generate a predefined number of expanding windows.

Using offsetUsing number of windows
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-35-1)>>> vbt.Splitter.from_expanding(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-35-2)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-35-3)... min_length=360, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-35-4)... offset=180, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-35-5)... split=-180 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-35-6)... ).plot().show()
 
[/code]

 1. 2. 3. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_expanding.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_expanding.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-36-1)>>> vbt.Splitter.from_n_expanding(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-36-2)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-36-3)... n=5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-36-4)... min_length=360,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-36-5)... split=-180
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-36-6)... ).plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_expanding.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_expanding.dark.svg#only-dark)


# Anchored[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#anchored "Permanent link")

Let's consider a scenario where we want to generate a set of one-year long splits. Using any of the approaches above, we would get splits that last for one year but most likely start in somewhere in the middle of the year. But what if our requirement was for each split to start exactly at the beginning of the year? Such time anchors are only possible by grouping or resampling. There are two class methods in [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) that enable this behavior: [Splitter.from_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_ranges) and [Splitter.from_grouper](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_grouper).

The first method uses [get_index_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.get_index_ranges) to translate a user query into a set of start and end indices. It allows us to provide custom start and end dates, to resample using a lookback period, to select a time range within each day, and more, - just like resampling but on steroids ![💊](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f48a.svg)

YearlyQuarterly from year startLast month for OOSExpanding with last quarter for OOS
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-37-1)>>> vbt.Splitter.from_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-37-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-37-3)... every="Y", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-37-4)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-37-5)... ).plot().show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_ranges1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_ranges1.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-38-1)>>> vbt.Splitter.from_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-38-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-38-3)... every="Q", 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-38-4)... lookback_period="Y", 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-38-5)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-38-6)... ).plot().show()
 
[/code]

 1. Every quarter start
 2. Look back all the way to to the year start

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_ranges2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_ranges2.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-1)>>> vbt.Splitter.from_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-3)... every="Q",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-4)... lookback_period="Y",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-5)... split=( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-6)... vbt.RepEval("index.month != index.month[-1]"), 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-7)... vbt.RepEval("index.month == index.month[-1]")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-39-9)... ).plot().show()
 
[/code]

 1. Same as above but reserve the last calendar month for the OOS set in each split
 2. Template should return a range (here a mask). Variable `index` in each template will be substituted by the index of the respective split.

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_ranges3.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_ranges3.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-1)>>> def qyear(index): 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-2)... return index.to_period("Q")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-4)>>> vbt.Splitter.from_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-5)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-6)... start=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-7)... fixed_start=True, 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-8)... every="Q",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-9)... closed_end=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-10)... split=(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-11)... lambda index: qyear(index) != qyear(index)[-1], 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-12)... lambda index: qyear(index) == qyear(index)[-1] 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-40-14)... ).plot().show()
 
[/code]

 1. Function to classify each date by quarter
 2. Make each range start from the very first bar
 3. Assign each quarter apart from the last one to the IS set
 4. Assign the last quarter to the IS set

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_ranges4.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_ranges4.dark.svg#only-dark)

The second method takes a grouping or resampling instruction and converts each group into a split. It's based on the method [BaseIDXAccessor.get_grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.get_grouper), and accepts a variety of formats from both vectorbt and Pandas, even [pandas.Grouper](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Grouper.html) and [pandas.Resampler](https://pandas.pydata.org/docs/reference/resampling.html). The only issue that we may encounter are incomplete splits, which can be filtered out using a template provided as `split_check_template` and forwarded down to [Splitter.from_splits](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_splits).

Resampling annuallyRemoving incomplete yearsFormatting labelsUsing grouping
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-41-1)>>> vbt.Splitter.from_grouper(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-41-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-41-3)... by="Y", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-41-4)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-41-5)... ).plot().show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_grouper1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_grouper1.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-1)>>> def is_split_complete(index, split): 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-2)... first_range = split[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-3)... first_index = index[first_range][0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-4)... last_range = split[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-5)... last_index = index[last_range][-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-6)... return first_index.is_year_start and last_index.is_year_end
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-8)>>> vbt.Splitter.from_grouper(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-9)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-10)... by="Y",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-11)... split=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-12)... split_check_template=vbt.RepFunc(is_split_complete) 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-42-13)... ).plot().show()
 
[/code]

 1. Check whether the first day is the year's start and the last day is the year's end. This function will become a template, such that vectorbt will substitute `index` for the **full** index and `split` for the current split. Should return False if the split should be discarded.
 2. Wrap with [RepFunc](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.RepFunc) to make a template out of `is_split_complete`

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_grouper2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_grouper2.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-1)>>> def format_split_labels(index, splits_arr): 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-2)... years = map(lambda x: index[x[0]][0].year, splits_arr) 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-3)... return pd.Index(years, name="split_year")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-5)>>> vbt.Splitter.from_grouper(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-6)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-7)... by="Y",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-8)... split=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-9)... split_check_template=vbt.RepFunc(is_split_complete),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-10)... split_labels=vbt.RepFunc(format_split_labels) 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-43-11)... ).plot().show()
 
[/code]

 1. Extract the year from each split. This function will become a template, such that vectorbt will substitute `index` for the **full** index and `splits_arr` for the splits array. Should return an index-like object.
 2. For each split, get the year of the first timestamp in the first range
 3. Split labels can be an index-like object or a template

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_grouper3.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_grouper3.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-44-1)>>> vbt.Splitter.from_grouper(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-44-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-44-3)... by=data.index.year, 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-44-4)... split=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-44-5)... split_check_template=vbt.RepFunc(is_split_complete) 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-44-6)... ).plot().show()
 
[/code]

 1. Regular Pandas Index with years as values. Each unique value will become a split label.
 2. Still need to check for completeness of splits, but at least labels are already formatted

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_grouper4.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_grouper4.dark.svg#only-dark)


# Random[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#random "Permanent link")

So far, we generated windows based on some pre-defined schema. But there is also a special place for randomness in CV, especially when it comes to [bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping_\(statistics\)) and [block bootstrap](https://en.wikipedia.org/wiki/Bootstrapping_\(statistics\)#Block_bootstrap) in particular. The method [Splitter.from_n_random](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_n_random) draws a predefined number of windows of a (optionally) variable length. At the heart of this method are two callbacks: `length_choice_func` and `start_choice_func`, selecting the next window's length and start point respectively. By default, they are set to [numpy.random.Generator.choice](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.choice.html), which generates a random sample with replacement (i.e., the same window can occur more than once). Another two callbacks, `length_p_func` and `start_p_func`, can control the probabilities of picking each entry (e.g., to select more windows to the right of the period).

Fixed lengthVariable lengthWith probabilities
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-45-1)>>> vbt.Splitter.from_n_random(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-45-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-45-3)... n=50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-45-4)... min_length=360, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-45-5)... seed=42, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-45-6)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-45-7)... ).plot().show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_random1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_random1.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-46-1)>>> vbt.Splitter.from_n_random(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-46-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-46-3)... n=50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-46-4)... min_length=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-46-5)... max_length=300,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-46-6)... seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-46-7)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-46-8)... ).plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_random2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_random2.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-1)>>> def start_p_func(i, indices): 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-2)... return indices / indices.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-4)>>> vbt.Splitter.from_n_random(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-5)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-6)... n=50,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-7)... min_length=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-8)... max_length=300,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-9)... seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-10)... start_p_func=start_p_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-11)... split=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-47-12)... ).plot().show()
 
[/code]

 1. Takes the iteration number and a set of potential start points

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_random3.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_n_random3.dark.svg#only-dark)


# Scikit-learn[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#scikit-learn "Permanent link")

For k-fold and many other standard CV schemes where scikit-learn has an upper hand, there is a method [Splitter.from_sklearn](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_sklearn) that can parse just about every cross-validator that subclasses the scikit-learn's `BaseCrossValidator` class.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-48-1)>>> from sklearn.model_selection import KFold
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-48-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-48-3)>>> vbt.Splitter.from_sklearn(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-48-4)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-48-5)... KFold(n_splits=5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-48-6)... ).plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_sklearn.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_sklearn.dark.svg#only-dark)

Warning

There is a temporal dependency between observations: it makes no sense to use the values from the future to forecast values in the past, thus make sure that the test period always succeeds the training period.


# Dynamic[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#dynamic "Permanent link")

The final and the most flexible generation method involves calling a UDF that takes a context including all the splits generated previously, and returns a new split to be appended. This all happens in an infinite while-loop; to break out of the loop, the UDF must return `None`. Similarly to many other methods in vectorbt that take functions as arguments, this one also makes use of templates to substitute them for information from the context. The context itself includes the appended and resolved splits (`splits`) and the bounds of each range in each split (but only when `fix_ranges=True`), which makes the generation process a child's play.

Roll one-year window each monthTrain one business week, test next
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-1)>>> def split_func(index, prev_start):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-2)... if prev_start is None: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-3)... prev_start = index[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-4)... new_start = prev_start + pd.offsets.MonthBegin(1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-5)... new_end = new_start + pd.DateOffset(years=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-6)... if new_end > index[-1] + index.freq: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-7)... return None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-8)... return [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-9)... slice(new_start, new_start + pd.offsets.MonthBegin(9)), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-10)... slice(new_start + pd.offsets.MonthBegin(9), new_end)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-11)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-13)>>> vbt.Splitter.from_split_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-14)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-15)... split_func=split_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-16)... split_args=(vbt.Rep("index"), vbt.Rep("prev_start")), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-17)... range_bounds_kwargs=dict(index_bounds=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-49-18)... ).plot().show()
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_split_func1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_split_func1.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-1)>>> def get_next_monday(from_date):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-2)... if from_date.weekday == 0 and from_date.ceil("H").hour <= 9: 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-3)... return from_date.floor("D")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-4)... return from_date.floor("D") + pd.offsets.Week(n=0, weekday=0) 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-6)>>> def get_next_business_range(from_date):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-7)... monday_0000 = get_next_monday(from_date)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-8)... monday_0900 = monday_0000 + pd.DateOffset(hours=9) 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-9)... friday_1700 = monday_0900 + pd.DateOffset(days=4, hours=8) 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-10)... return slice(monday_0900, friday_1700)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-12)>>> def split_func(index, bounds):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-13)... if len(bounds) == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-14)... from_date = index[0] 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-15)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-16)... from_date = bounds[-1][1][0] 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-17)... train_range = get_next_business_range(from_date)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-18)... test_range = get_next_business_range(train_range.stop)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-19)... if test_range.stop > index[-1] + index.freq:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-20)... return None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-21)... return train_range, test_range
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-22)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-23)>>> vbt.Splitter.from_split_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-24)... vbt.date_range("2020-01", "2020-03", freq="15min"), 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-25)... split_func=split_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-26)... split_args=(vbt.Rep("index"), vbt.Rep("bounds")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-27)... range_bounds_kwargs=dict(index_bounds=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-50-28)... ).plot().show()
 
[/code]

 1. If `from_date` is a Monday 09:00 or earlier, normalize it to get the Monday 00:00
 2. If not, normalize and find the next Monday 00:00
 3. Add 9 hours to get the Monday 09:00
 4. Add 4 days and 9 hours to get the Friday 17:00
 5. Start from the first date if this is the first split
 6. Use the start date of the previous test set as the start date of the new train set
 7. Generate a 15-minute index for this example

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_split_func2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/from_split_func2.dark.svg#only-dark)


# Validation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#validation "Permanent link")

Consider the following splitter that splits the entire period into years, one per split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-51-1)>>> splitter = vbt.Splitter.from_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-51-2)... data.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-51-3)... every="Y",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-51-4)... closed_end=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-51-5)... split=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-51-6)... set_labels=["IS", "OOS"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-51-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-51-8)>>> splitter.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/flawed_splitter.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/flawed_splitter.dark.svg#only-dark)

By default, `closed_end` is `False` such that any neighboring ranges do not overlap, but we deliberately made a mistake here by setting `closed_end` to `True`, hence we've produced splits that overlap by exactly one bar. How do we detect such a mistake post-factum? The [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) class has various tools exactly for that.


# Bounds[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#bounds "Permanent link")

The first tool involves computing the bounds of each range. The bounds consist of two numbers (`index_bounds=False`) or dates (`index_bounds=True`): the start (always inclusive) and the end (exclusive, but can be inclusive using `right_inclusive=True`). Depending on what the analysis goal is, they can be returned in two different formats. The first format is a three-dimensional NumPy array returned by [Splitter.get_bounds_arr](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_bounds_arr) where the first axis are splits, the second axis are sets, and the third axis are bounds:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-1)>>> bounds_arr = splitter.get_bounds_arr() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-2)>>> bounds_arr.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-3)(4, 2, 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-5)>>> bounds_arr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-6)[[[ 137 320]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-7) [ 320 503]]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-8) [[ 502 685]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-9) [ 685 868]]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-10) [[ 867 1050]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-11) [1050 1234]]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-12) [[1233 1416]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-52-13) [1416 1599]]]
 
[/code]

 1. 

Another, probably a user-friendlier, format is a DataFrame returned by [Splitter.get_bounds](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_bounds) where rows represent ranges and columns represent bounds:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-1)>>> bounds = splitter.get_bounds(index_bounds=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-2)>>> bounds.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-3)(8, 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-5)>>> bounds
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-6)bound start end
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-7)split set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-8)0 IS 2018-01-01 00:00:00+00:00 2018-07-03 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-9) OOS 2018-07-03 00:00:00+00:00 2019-01-02 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-10)1 IS 2019-01-01 00:00:00+00:00 2019-07-03 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-11) OOS 2019-07-03 00:00:00+00:00 2020-01-02 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-12)2 IS 2020-01-01 00:00:00+00:00 2020-07-02 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-13) OOS 2020-07-02 00:00:00+00:00 2021-01-02 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-14)3 IS 2021-01-01 00:00:00+00:00 2021-07-03 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-53-15) OOS 2021-07-03 00:00:00+00:00 2022-01-02 00:00:00+00:00
 
[/code]

 1. 

We can then detect some IS ranges starting before the preceding OOS range ends:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-54-1)>>> bounds.loc[(0, "OOS"), "end"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-54-2)Timestamp('2019-01-02 00:00:00+0000', tz='UTC')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-54-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-54-4)>>> bounds.loc[(1, "IS"), "start"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-54-5)Timestamp('2019-01-01 00:00:00+0000', tz='UTC')
 
[/code]


# Masks[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#masks "Permanent link")

Another tool revolves around range masks. Since the index is the same for each single range, we can translate a range into a mask of the same length as the index and then stack all masks into a single array. Another advantage of masks is that we can combine them, apply logical operators on them, reduce them, and test them for `True` values. The only downside is clearly their memory consumption: as we calculated previously, 100 splits and 2 sets of 1 year of 1-minute data would consume whooping 100MB of RAM. Similarly to bounds, we have two methods that return a three-dimensional NumPy array and a DataFrame respectively: [Splitter.get_mask_arr](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_mask_arr) and [Splitter.get_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_mask). Let's get the mask in the DataFrame format:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-1)>>> mask = splitter.get_mask() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-2)>>> mask.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-3)(1902, 8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-5)>>> mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-6)split 0 1 2 3 \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-7)set IS OOS IS OOS IS OOS IS 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-8)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-9)2017-08-17 00:00:00+00:00 False False False False False False False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-10)2017-08-18 00:00:00+00:00 False False False False False False False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-11)2017-08-19 00:00:00+00:00 False False False False False False False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-12)... ... ... ... ... ... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-13)2022-10-29 00:00:00+00:00 False False False False False False False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-14)2022-10-30 00:00:00+00:00 False False False False False False False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-15)2022-10-31 00:00:00+00:00 False False False False False False False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-17)split 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-18)set OOS 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-19)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-20)2017-08-17 00:00:00+00:00 False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-21)2017-08-18 00:00:00+00:00 False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-22)2017-08-19 00:00:00+00:00 False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-23)... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-24)2022-10-29 00:00:00+00:00 False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-25)2022-10-30 00:00:00+00:00 False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-26)2022-10-31 00:00:00+00:00 False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-27)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-55-28)[1902 rows x 8 columns]
 
[/code]

 1. 

As opposed to bounds, the DataFrame lists split and set labels (i.e., range labels) in columns rather than rows. To demonstrate the power of masks, let's answer the following question: what ranges cover the year 2021?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-1)>>> mask["2021":"2021"].any()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-2)split set
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-3)0 IS False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-4) OOS False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-5)1 IS False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-6) OOS False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-7)2 IS False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-8) OOS True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-9)3 IS True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-10) OOS True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-56-11)dtype: bool
 
[/code]

We can spot the mistake once again: there's an OOS range that clearly overflows into the next year. Here's another question: get the number of dates covered by each set in each year.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-1)>>> mask.resample(vbt.offset("Y")).sum() # (1)!
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-2)split 0 1 2 3 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-3)set IS OOS IS OOS IS OOS IS OOS
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-4)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-5)2017-01-01 00:00:00+00:00 0 0 0 0 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-6)2018-01-01 00:00:00+00:00 183 182 0 0 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-7)2019-01-01 00:00:00+00:00 0 1 183 182 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-8)2020-01-01 00:00:00+00:00 0 0 0 1 183 183 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-9)2021-01-01 00:00:00+00:00 0 0 0 0 0 1 183 182
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-57-10)2022-01-01 00:00:00+00:00 0 0 0 0 0 0 0 1
 
[/code]

To mitigate potential memory issues, there are special approaches that translate only a subset of ranges into a mask at a time. Those approaches are based on two iteration schemas: by split and by set, implemented by [Splitter.get_iter_split_masks](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_iter_split_masks) and [Splitter.get_iter_set_masks](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_iter_set_masks) respectively. Each method returns a [Python generator](https://realpython.com/introduction-to-python-generators/) that can be iterated over in a loop. Let's answer the question above in a memory-friendly manner (if really needed):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-1)>>> results = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-2)>>> for mask in splitter.get_iter_split_masks():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-3)... results.append(mask.resample(vbt.offset("Y")).sum())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-4)>>> pd.concat(results, axis=1, keys=splitter.split_labels)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-5)split 0 1 2 3 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-6)set IS OOS IS OOS IS OOS IS OOS
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-7)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-8)2017-01-01 00:00:00+00:00 0 0 0 0 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-9)2018-01-01 00:00:00+00:00 183 182 0 0 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-10)2019-01-01 00:00:00+00:00 0 1 183 182 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-11)2020-01-01 00:00:00+00:00 0 0 0 1 183 183 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-12)2021-01-01 00:00:00+00:00 0 0 0 0 0 1 183 182
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-58-13)2022-01-01 00:00:00+00:00 0 0 0 0 0 0 0 1
 
[/code]


# Coverage[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#coverage "Permanent link")

Bounds and masks are convenient range formats that enable us to analyze ranges from various perspectives. To not delegate too much work to the user, there are additional methods that automate this analysis. Since we're mostly interested in knowing whether and how much do splits, sets, and ranges overlap, there are 4 methods that provide us with quick insights into that matter: [Splitter.get_split_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_split_coverage) for the coverage by split, [Splitter.get_set_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_set_coverage) for the coverage by set, [Splitter.get_range_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_range_coverage) for the coverage by range, and [Splitter.get_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_coverage) for the coverage by any of the above. For example, the split-relative coverage will return the % of bars in the index covered by each split, while the total coverage will return the % of bars in the index covered by any range.

Warning

Most of the methods below, apart from the plotting method, require the entire mask array to be in memory.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-1)>>> splitter.get_split_coverage() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-2)split
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-3)0 0.192429
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-4)1 0.192429
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-5)2 0.192955
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-6)3 0.192429
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-7)Name: split_coverage, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-9)>>> splitter.get_set_coverage() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-10)set
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-11)IS 0.384858
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-12)OOS 0.385384
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-13)Name: set_coverage, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-15)>>> splitter.get_range_coverage() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-16)split set
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-17)0 IS 0.096215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-18) OOS 0.096215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-19)1 IS 0.096215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-20) OOS 0.096215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-21)2 IS 0.096215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-22) OOS 0.096740
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-23)3 IS 0.096215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-24) OOS 0.096215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-25)Name: range_coverage, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-26)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-27)>>> splitter.get_coverage() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-59-28)0.768664563617245
 
[/code]

 1. 2. 3. 4. 

Note

The default arguments will always return a metric relative to the length of the index.

As we can see above, the first split covers 19.24% of the entire period, while both ranges in that split take 9.62%, or exactly 50% of the split. Both sets cover roughly the same period of time - 38.53% of the entire period. The last metric tells us that 23.14% of the entire period aren't covered by the splitter, which makes sense because the years 2017 and 2022 are incomplete such that no split was produced for either of them. Finally, why do all ranges cover the same period of time except the OOS set in the split `2`? It's because that year was a leap year such that the last months had one day more than the same months in other years:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-60-1)>>> splitter.index_bounds.loc[(2, "OOS"), "start"].is_leap_year
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-60-2)True
 
[/code]

So far, we analyzed coverage in relation to the full index. But is a special argument `relative` that allows us to analyze splits and sets relatively to the total coverage, as well as ranges relatively to the split coverage. For example, let's get the fraction of IS and OOS sets in their respective splits:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-1)>>> splitter.get_range_coverage(relative=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-2)split set
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-3)0 IS 0.500000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-4) OOS 0.500000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-5)1 IS 0.500000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-6) OOS 0.500000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-7)2 IS 0.498638
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-8) OOS 0.501362
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-9)3 IS 0.500000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-10) OOS 0.500000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-61-11)Name: range_coverage, dtype: float64
 
[/code]

Most periods except the leap year have a perfect 50/50 split, as we wanted. We can expand our analysis to answer whether sets in general follow the same 50/50 split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-62-1)>>> splitter.get_set_coverage(relative=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-62-2)set
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-62-3)IS 0.500684
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-62-4)OOS 0.501368
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-62-5)Name: set_coverage, dtype: float64
 
[/code]

Both numbers do not sum to one, which (again) hints at overlapping ranges. By using the argument `overlapping`, we can assess any overlaps of sets within each split, any overlaps of splits within each set, and any overlaps of ranges globally:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-1)>>> splitter.get_split_coverage(overlapping=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-2)split
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-3)0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-4)1 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-5)2 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-6)3 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-7)Name: split_coverage, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-9)>>> splitter.get_set_coverage(overlapping=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-10)set
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-11)IS 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-12)OOS 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-13)Name: set_coverage, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-15)>>> splitter.get_coverage(overlapping=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-63-16)0.002051983584131327
 
[/code]

Ranges neither overlap within each split, nor within each set. But there are still some overlaps of ranges recorded globally, which means they belong to opposite splits and sets. To have a better look, let's visualize the coverage using [Splitter.plot_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.plot_coverage):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-64-1)>>> splitter.plot_coverage().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/plot_coverage.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/plot_coverage.dark.svg#only-dark)

The Y-axis represents the total number of ranges that cover one particular date. We can see that there are three dates covered by two ranges simultaneously.

The last and the most powerful tool in overlap detection are overlap matrices, which compute overlaps either between splits (`by="split"`), sets (`by="set"`), or ranges (`by="range"`). If `normalize` is True, which is the default value, the intersection of two range masks will be normalized by their union. Even though the operation is Numba-compiled, it's still very expensive: 100 splits and 2 sets would require going through all `200 * 200 = 40000` range pairs to build the range overlap matrix. Let's finally shed some light on the overlapping ranges:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-1)>>> splitter.get_overlap_matrix(by="range", normalize=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-2)split 0 1 2 3 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-3)set IS OOS IS OOS IS OOS IS OOS
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-4)split set 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-5)0 IS 183 0 0 0 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-6) OOS 0 183 1 0 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-7)1 IS 0 1 183 0 0 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-8) OOS 0 0 0 183 1 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-9)2 IS 0 0 0 1 183 0 0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-10) OOS 0 0 0 0 0 184 1 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-11)3 IS 0 0 0 0 0 1 183 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-65-12) OOS 0 0 0 0 0 0 0 183
 
[/code]

 1. 


# Grouping[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#grouping "Permanent link")

Each of the methods above (and many others including [Splitter.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.plot)) accept the arguments `split_group_by` and `set_group_by`, which allow grouping splits and sets respectively. Their format is identical to the format of the argument `group_by`, which appears just about everywhere in the vectorbt's codebase. For example, by passing `True`, we can put all ranges into the same bucket and merge them. We can also pass a list of the same length as the number of splits/sets such that the splits/sets under the same unique value will get merged. The actual merging part is being done by the method [Splitter.merge_split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.merge_split).

For example, let's get the bounds of each entire split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-66-1)>>> splitter.get_bounds(index_bounds=True, set_group_by=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-66-2)bound start end
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-66-3)split set_group 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-66-4)0 group 2018-01-01 00:00:00+00:00 2019-01-02 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-66-5)1 group 2019-01-01 00:00:00+00:00 2020-01-02 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-66-6)2 group 2020-01-01 00:00:00+00:00 2021-01-02 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-66-7)3 group 2021-01-01 00:00:00+00:00 2022-01-02 00:00:00+00:00
 
[/code]

This makes certain kinds of analysis much easier ![🪄](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1fa84.svg)


# Manipulation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#manipulation "Permanent link")

We'll end this page with an overview of the methods that can be used to change a splitter. Let's build a splitter that has just one set representing the current year:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-67-1)>>> splitter = vbt.Splitter.from_grouper(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-67-2)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-67-3)... by=data.index.year.rename("split_year") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-67-4)... )
 
[/code]

 1. 

Since the class [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) subclasses the class [Analyzable](https://vectorbt.pro/pvt_7a467f6b/documentation/building-blocks/#analyzing), we can get a quick and nice overview of the most important metrics and plots:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-1)>>> splitter.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-2)Index Start 2017-08-17 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-3)Index End 2022-10-31 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-4)Index Length 1902
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-5)Splits 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-6)Sets 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-7)Coverage [%] 100.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-8)Overlap Coverage [%] 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-9)Name: agg_stats, dtype: object
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-68-11)>>> splitter.plots().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/plots1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/plots1.dark.svg#only-dark)

Info

Since we have only one split, most metrics were hidden from the statistics.

As we already know, we can select specific splits and sets using regular Pandas indexing (which is another great property of [Analyzable](https://vectorbt.pro/pvt_7a467f6b/documentation/building-blocks/#analyzing)). Since we're not interested in incomplete years, let's remove the first and the last split:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-1)>>> splitter = splitter.iloc[1:-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-2)>>> splitter.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-3)Index Start 2017-08-17 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-4)Index End 2022-10-31 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-5)Index Length 1902
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-6)Splits 4 << changed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-7)Sets 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-8)Coverage [%] 76.81388 << changed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-9)Overlap Coverage [%] 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-69-10)Name: agg_stats, dtype: object
 
[/code]

Now, let's split the only set into three: a train set covering the first two quarters, a validation set covering the third one, and a test set covering the last one. This is possible thanks to the method [Splitter.split_set](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_set), which takes the split specification and the labels of the new split as `new_split` and `new_set_labels` respectively. We'll use a function template to divide the set:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-1)>>> def new_split(index): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-2)... return [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-3)... np.isin(index.quarter, [1, 2]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-4)... index.quarter == 3, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-5)... index.quarter == 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-6)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-8)>>> splitter = splitter.split_set(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-9)... vbt.RepFunc(new_split), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-10)... new_set_labels=["train", "valid", "test"] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-70-11)... )
 
[/code]

 1. 2. 3. 4. 

Info

Each operation on a splitter returns a new splitter: no information is changed in place to not mess up with caching and to keep the splitter (as any other vectorbt object) side effect free.

Let's take a look at the new splitter:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-1)>>> splitter.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-2)Index Start 2017-08-17 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-3)Index End 2022-10-31 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-4)Index Length 1902
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-5)Splits 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-6)Sets 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-7)Coverage [%] 76.81388
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-8)Coverage [%]: train 38.117771
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-9)Coverage [%]: valid 19.348055
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-10)Coverage [%]: test 19.348055
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-11)Mean Rel Coverage [%]: train 49.623475
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-12)Mean Rel Coverage [%]: valid 25.188263
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-13)Mean Rel Coverage [%]: test 25.188263
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-14)Overlap Coverage [%] 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-15)Overlap Coverage [%]: train 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-16)Overlap Coverage [%]: valid 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-17)Overlap Coverage [%]: test 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-18)Name: agg_stats, dtype: object
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-19)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation/splitter/#__codelineno-71-20)>>> splitter.plots().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/plots2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/cv/plots2.dark.svg#only-dark)

As you might have guessed, there's also a method that can merge multiple sets - [Splitter.merge_sets](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.merge_sets). Your homework is to merge the "valid" and "test" sets into "test" ![😉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f609.svg)

We did our job perfectly, let's move on to applications! ![✈](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2708.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/cross-validation/splitter.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/CrossValidation.ipynb)