# Projections[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#projections "Permanent link")

Given a set of detected patterns, how do we assess whether they provide us with an edge? One idea would be to backtest them using signals and analyze the produced trades, but the performance of each trade would also depend on the selected backtesting parameters and the performance of all the trades preceding it. What we need though are distilled statistics that do not depend on anything other than the development of the price after each pattern. Here's a simplified workflow: capture the price development (a.k.a. a projection) for a number of bars after each pattern, save them into a single array (a.k.a. projections), and run various statistics on that array. The main idea is that if the pattern works, the price will mostly rise or fall depending on the pattern's bullishness or bearishness. Here, "mostly" is the median return, and it's just one of the many statistics that can be analyzed.

Projections capture the price development during a pre-defined period of time. Since time periods are best represented using range records of the type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges), we can easily map each range into a projection. The Numba-compiled function that does this is [map_ranges_to_projections_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.map_ranges_to_projections_nb), which takes the close price (or any other price), information on each range, and returns a two-dimensional NumPy array where each _row_ is a single projection. Before we put our hands onto this function, let's find all the ranges where the price increased by 20% in a matter of 7 days. We will allow this requirement to deviate by a maximum of 1%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-2)... [1, 1.2], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-3)... window=7, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-4)... rescale_mode="rebase", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-5)... max_error=0.01,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-6)... max_error_interp_mode="discrete", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-7)... max_error_strict=True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-9)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-0-10)3
 
[/code]

 1. 2. 3. 


# Pattern projections[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#pattern-projections "Permanent link")

Let's call the Numba-compiled function on the pattern ranges we generated above. This operation will build projections from the price **inside** each range, that is, they all should be highly similar to our pattern:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-1)>>> range_idxs, raw_projections = vbt.nb.map_ranges_to_projections_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-2)... vbt.to_2d_array(price), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-3)... pattern_ranges.get_field_arr("col"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-4)... pattern_ranges.get_field_arr("start_idx"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-5)... pattern_ranges.get_field_arr("end_idx"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-6)... pattern_ranges.get_field_arr("status")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-8)>>> range_idxs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-9)array([0, 1, 2])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-11)>>> raw_projections
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-12)array([[1. , 1.00936136, 1.0528197 , 1.11080047, 1.12247632,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-13) 1.13616486, 1.18824968, 1.16303367],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-14) [1. , 1.03041164, 1.07854881, 1.08766541, 1.14380648,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-15) 1.17483528, 1.20173755, 1.11737666],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-16) [1. , 1.02418635, 1.10605106, 1.12944688, 1.17161711,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-1-17) 1.17323145, 1.20239992, 1.22269832]])
 
[/code]

 1. 2. 

Here's what happened: the function iterated through each range, selected the corresponding price subset within that range, and stored that price subset in the output array. By default, it has also rebased all projections to `1` to make them comparable. Additionally, it returned an array with indices that link the passed ranges to the returned projections.

To avoid manually preparing the input and output data, there is an extra-convenient method [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections) that returns a Series/DataFrame with projections laid out as _columns_ and labeled accordingly:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-1)>>> projections = pattern_ranges.get_projections()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-2)>>> projections
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-3)range_id 0 1 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-4)2022-05-31 00:00:00+00:00 1.000000 1.000000 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-5)2022-06-01 00:00:00+00:00 1.009361 1.030412 1.024186
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-6)2022-06-02 00:00:00+00:00 1.052820 1.078549 1.106051
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-7)2022-06-03 00:00:00+00:00 1.110800 1.087665 1.129447
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-8)2022-06-04 00:00:00+00:00 1.122476 1.143806 1.171617
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-9)2022-06-05 00:00:00+00:00 1.136165 1.174835 1.173231
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-10)2022-06-06 00:00:00+00:00 1.188250 1.201738 1.202400
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-2-11)2022-06-07 00:00:00+00:00 1.163034 1.117377 1.222698
 
[/code]

If we throw a look at the index of the DataFrame above, we will notice that it starts with the last index in the price. This is because projections are meant to be _projected_ into the future. We will also notice that there are 8 elements even though we ordered our patterns to be 7 bars long:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-3-1)>>> pattern_ranges.duration.values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-3-2)array([7, 7, 7])
 
[/code]

This is because the first element (`1`) is considered the base of each projection and isn't taken into account when it comes to the number of projected entries, which is the duration of the range by default. In a case where we want to analyze exclusively the duration of the range, we can disable this behavior by setting `incl_end_idx` to `False`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-1)>>> projections = pattern_ranges.get_projections(incl_end_idx=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-2)>>> projections
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-3)range_id 0 1 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-4)2022-05-31 00:00:00+00:00 1.000000 1.000000 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-5)2022-06-01 00:00:00+00:00 1.009361 1.030412 1.024186
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-6)2022-06-02 00:00:00+00:00 1.052820 1.078549 1.106051
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-7)2022-06-03 00:00:00+00:00 1.110800 1.087665 1.129447
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-8)2022-06-04 00:00:00+00:00 1.122476 1.143806 1.171617
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-9)2022-06-05 00:00:00+00:00 1.136165 1.174835 1.173231
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-4-10)2022-06-06 00:00:00+00:00 1.188250 1.201738 1.202400
 
[/code]

We can finally observe the cumulative returns of each price range fitting our pattern. This data format allows us to apply many data analysis techniques to assess the quality of the pattern itself. For example, let's get the total return of each range:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-5-1)>>> projections.iloc[-1] / projections.iloc[0] - 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-5-2)range_id
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-5-3)0 0.188250
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-5-4)1 0.201738
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-5-5)2 0.202400
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-5-6)dtype: float64
 
[/code]

Info

You might wonder why the first return is 18.8% even though the maximum error requires it to be within 19% and 21%? The 1% requirement is not defined relative to the total return, but relative to the percentage change between the price and the pattern at the respective point.

And here's the visualization:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-6-1)>>> projections.vbt.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/pattern_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/pattern_projections.dark.svg#only-dark)

As we can see, each price range fits the pattern quite well.


# Delta projections[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#delta-projections "Permanent link")

But the main use case of projections is not debugging patterns, but analyzing their impact on the price to determine whether they carry alpha and consistently beat randomness (even slightly). Since projections are extracted from between the start and end row of each range, we need to shift the range of each detected pattern to start with the last point and have a specific duration (= delta) that we want to analyze. This procedure is implemented by the class method [Ranges.from_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta) and instance method [Ranges.with_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.with_delta), which is based on the former. Let's construct new ranges that start at the last point in each pattern range and end after a duration of 4 bars, that is, we want to analyze the impact of our pattern 4 bars in the future:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-7-1)>>> delta_ranges = pattern_ranges.with_delta(4) 
 
[/code]

 1. 

To better understand how the newly created ranges relate to the pattern ranges they were generated from, let's visualize both range types between January and March 2021:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-1)>>> fig = pattern_ranges.loc["2021-01":"2021-03"].plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-2)>>> delta_ranges.loc["2021-01":"2021-03"].plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-3)... plot_ohlc=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-4)... plot_close=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-5)... plot_markers=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-6)... closed_shape_kwargs=dict(fillcolor="DeepSkyBlue"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-7)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-8-9)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/delta_ranges.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/delta_ranges.dark.svg#only-dark)

We see that the "DeepSkyBlue"-colored ranges start from the last point in the pattern range and last 4 bars. Why not letting them start from the last point in the range to avoid overlaps? Remember that the first point in each projection is the base point (`1`) from which the actual projections propagate, thus this base point should be the last pattern point. Let's generate projections once again:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-9-1)>>> projections = delta_ranges.get_projections()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-9-2)>>> projections
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-9-3)range_id 0 1 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-9-4)2022-05-31 00:00:00+00:00 1.000000 1.000000 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-9-5)2022-06-01 00:00:00+00:00 0.978779 0.929801 1.016882
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-9-6)2022-06-02 00:00:00+00:00 1.108145 0.864097 0.992104
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-9-7)2022-06-03 00:00:00+00:00 1.178824 0.864522 0.963215
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-9-8)2022-06-04 00:00:00+00:00 1.147739 0.851382 0.941327
 
[/code]

Those three columns contain the price development for 4 bars after their respective pattern and are now perfectly analyzable. For example, we can derive the mean total return of that development:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-10-1)>>> np.mean(projections.iloc[-1] / projections.iloc[0] - 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-10-2)-0.01985064245106242
 
[/code]

We see that whenever the price rises by 20% in a matter of 7 bars, after 4 bars it tends to fall by 2% on average. If you have at least a bit of experience in statistics, you'd quickly point at the low number of observations to derive any meaningful statistics. Thus, let's search for a 20% price increase in windows ranging from 7 to 30 bars with overlaps allowed, and perform our analysis again, but now on both assets:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-1)>>> pattern_ranges = mult_price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-2)... [1, 1.2], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-3)... window=7, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-4)... max_window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-5)... rescale_mode="rebase",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-6)... max_error=0.01,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-7)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-8)... max_error_strict=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-9)... overlap_mode="allow"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-11)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-12)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-13)BTCUSDT 48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-14)ETHUSDT 64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-15)Name: count, dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-17)>>> delta_ranges = pattern_ranges.with_delta(4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-18)>>> projections = delta_ranges.get_projections()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-19)>>> (projections.iloc[-1] / projections.iloc[0] - 1).describe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-20)count 112.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-21)mean 0.010467
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-22)std 0.079566
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-23)min -0.203760
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-24)25% -0.044565
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-25)50% 0.014051
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-26)75% 0.055390
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-27)max 0.270107
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-11-28)dtype: float64
 
[/code]

Half the time, the total return after 4 bars is at least 1.4%. 

Since projection columns are sorted by time (the pattern ranges are sorted by the end index, the delta ranges are thus sorted by the start index), we can even visualize this metric against time to observe how it evolves. We just need to split this operation by symbol since projections of multiple symbols are stacked block-wise as columns. We also need to generate projections once again but now with the argument `id_level` set to "end_idx" to replace the column level "range_id" by the actual time of the total return:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-1)>>> projections = delta_ranges.get_projections(id_level="end_idx")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-2)>>> projections.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-3)MultiIndex([('BTCUSDT', '2020-08-03 00:00:00+00:00'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-4) ('BTCUSDT', '2020-08-04 00:00:00+00:00'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-5) ('BTCUSDT', '2020-08-05 00:00:00+00:00'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-6) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-7) ('ETHUSDT', '2022-04-07 00:00:00+00:00'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-8) ('ETHUSDT', '2022-04-08 00:00:00+00:00'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-9) ('ETHUSDT', '2022-04-09 00:00:00+00:00')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-10) names=['symbol', 'end_idx'], length=112)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-12)>>> btc_projections = projections.xs("BTCUSDT", level="symbol", axis=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-13)>>> total_proj_return = btc_projections.iloc[-1] / btc_projections.iloc[0] - 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-14)>>> total_proj_return.vbt.scatterplot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-15)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-16)... marker=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-17)... color=total_proj_return.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-18)... colorscale="Temps_r",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-19)... cmid=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-20)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-21)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-12-22)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/total_proj_return.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/total_proj_return.dark.svg#only-dark)

We can confirm that after a 20% increase, the price mostly keeps on growing the next 4 bars.


# Plotting[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#plotting "Permanent link")

But what about plotting projections themselves? As all the projections in our array share the same index, we can plot them as regular lines. But instead of doing it manually and wasting our precious time, there is an accessor method [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections) specialized in projection visualization:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-13-1)>>> btc_projections.vbt.plot_projections(plot_bands=False).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/plot_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/plot_projections.dark.svg#only-dark)

We can see the price development after each detected pattern plotted as a line.


# Colorization[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#colorization "Permanent link")

Each line is colorized according to the projection's performance. By default, the color represents the median value of the projection relative to other projections. Here, for example, is the first projection in the array:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-1)>>> btc_projections["2020-08-03"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-2)2022-05-31 00:00:00+00:00 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-3)2022-06-01 00:00:00+00:00 1.019300
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-4)2022-06-02 00:00:00+00:00 1.053823
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-5)2022-06-03 00:00:00+00:00 1.018510
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-6)2022-06-04 00:00:00+00:00 1.015957
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-7)Freq: D, Name: 2020-08-03 00:00:00+00:00, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-9)>>> btc_projections["2020-08-03"].median()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-14-10)1.018510232892989
 
[/code]

Why the median and not the final value? Imagine that the projection is 90% of time above the baseline (`1`) but then falls below the baseline abruptly, should it be classified as a positive or negative performing projection? There are two components that drive the impact of an event on the price: the impact's delay and the impact's duration. Some events cause an immediate reaction of the price, other events are more long-term and take some time for the reaction to unfold. Mostly, events last only a limited amount of time and their effect gradually diminishes with time. That's why valuating projections by their last value is risky and strongly depends on the chosen projection duration, while taking the median is not affected by the duration.

But in a case where we're interested in the final or any other value, we can use the argument `colorize`, which accepts various modes ("median", "mean", and "last") but also a custom function that takes a Series/DataFrame and returns a number per column. Let's colorize the projections by their volatility:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-15-1)>>> btc_projections.vbt.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-15-2)... plot_bands=False, colorize=np.std
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-15-3)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/colorize_std.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/colorize_std.dark.svg#only-dark)

Hint

For the fans of fifty shades of grey, pass `colorize=False`.


# Bands[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#bands "Permanent link")

Seeing such an amount of projections doesn't give us many clues about the overall performance of the pattern. What we need though is a way to distill the most important price changes and present them in a human-readable format. If we take another look at the array with the projections, we would quickly realize that not only we can reduce that array along rows, but also along columns! This would reduce all the projections into a single projection, where each value is a statistic derived from all the projections at that bar. Let's, for example, compute the median projection for one and multiple symbols:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-1)>>> projections.xs("ETHUSDT", level="symbol", axis=1).median(axis=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-2)2022-05-31 00:00:00+00:00 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-3)2022-06-01 00:00:00+00:00 1.005677
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-4)2022-06-02 00:00:00+00:00 1.014560
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-5)2022-06-03 00:00:00+00:00 1.017341
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-6)2022-06-04 00:00:00+00:00 1.019444
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-7)Freq: D, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-9)>>> projections.groupby("symbol", axis=1).median() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-10)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-11)2022-05-31 00:00:00+00:00 1.000000 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-12)2022-06-01 00:00:00+00:00 1.003365 1.005677
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-13)2022-06-02 00:00:00+00:00 1.001214 1.014560
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-14)2022-06-03 00:00:00+00:00 1.010576 1.017341
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-15)2022-06-04 00:00:00+00:00 1.009568 1.019444
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-17)>>> projections.median(axis=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-18)2022-05-31 00:00:00+00:00 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-19)2022-06-01 00:00:00+00:00 1.004447
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-20)2022-06-02 00:00:00+00:00 1.006168
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-21)2022-06-03 00:00:00+00:00 1.014375
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-22)2022-06-04 00:00:00+00:00 1.014051
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-16-23)Freq: D, dtype: float64
 
[/code]

 1. 2. 3. 

If we can build one projection out of many, then we can also construct so-called confidence bands within which a certain percentage of projections are moving. Such bands are displayed automatically when calling [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-17-1)>>> btc_projections.vbt.plot_projections().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/bands.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/bands.dark.svg#only-dark)

The method generated four bands: the projections' 20% quantile, 50% quantile (median), 80% quantile, and mean. Whenever quantiles are plotted, their trace name gets prepended with `Q=`. So, what do those quantiles mean? Quantiles are values that split sorted data into equal parts. In our case, the quantiles are calculated across all projections at each time step (`axis=1`, remember?). For example, the 20% quantile means that there are 20% of values that are below that threshold. The 50% quantile is probably the most important quantile because it tells us the value below which there are 50% values and above which there are also 50% values. So, if the median is zero, predicting the market movement direction is no better than flipping a coin. Conversely, if the median is not zero, there are more projections that have a positive/negative return than the other way around, which is already worth investigating.

Quantiles are great to explore because they not only tell us how many values are below a certain band, but we can also derive the number of values that are located between bands. For example, in our chart above, `80% - 20% = 60%` of values are between the upper and lower band. This also means that only `100% - 80% = 20%` of values are located above the upper band, so the probability of hitting a return of more than 7% (see below) is not greater than one to five:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-18-1)>>> btc_projections.iloc[-1].quantile(0.8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-18-2)1.0702371602730685
 
[/code]

Since we can now approximate the probability of certain market reactions to our events, such an analysis can be beneficiary in determining optimal stop loss and take profit levels. For instance, depending on our risk aversion, we can set the stop loss at the lowest point of the 20% quantile band. If the 30% quantile fits our trading style better, we can plot it as the lower band by overriding the argument `plot_lower`. We can also plot it as the middle band while hiding other bands:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-19-1)>>> btc_projections.vbt.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-19-2)... plot_lower=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-19-3)... plot_middle="30%", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-19-4)... plot_upper=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-19-5)... plot_aux_middle=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-19-6)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/bands_30.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/bands_30.dark.svg#only-dark)

There are 30% projections below (or 70% above) that band.

The middle band as any other band argument allows an entire collection of formats to be provided. For instance, instead of using quantiles, we can use significance levels and [z-scores](https://en.wikipedia.org/wiki/Standard_score). Standard scores assume that the distribution of the projection values at any point approaches a normal distribution, which isn't necessarily the case, but might be, especially for smaller timeframes. To see whether any set of values is distributed normally, we can display a QQ plot:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-20-1)>>> btc_projections.iloc[-1].vbt.qqplot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/qqplot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/qqplot.dark.svg#only-dark)

Apart from a couple of outliers, most points lie on the red line, thus the distribution of all the projection values at the last bar is roughly normal. Given this, we can instruct the projection plotting method to display the bands based on a certain significance level. For example, similarly to the 10% quantile, providing a (one-tailed) significance level of 10% would mark where 10% of the lowest data points would be contained. This percentage can be provided using the percentage format `P=X%` or the floating format `P=0.X`, and is internally translated into a z-score using [scipy.stats.norm.ppf](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html). The z-score, or standard score, is the number of standard deviations from the mean. If the significance level is 95%, the z-score would be `1.96`, or almost twice the volatility. To provide a z-score instead of a significance level, use the format `Z=X`. 

Let's plot the significance levels of 20% and 80%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-21-1)>>> btc_projections.vbt.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-21-2)... plot_lower="P=20%",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-21-3)... plot_middle="P=50%", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-21-4)... plot_upper="P=80%", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-21-5)... plot_aux_middle=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-21-6)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/significance_levels.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/significance_levels.dark.svg#only-dark)

If the true distribution of the projection values at each bar is normal, the probability of each new projection to be between the low and upper band would be 60%. But what about custom bands? Similarly to the `colorize` argument, we can provide a UDF here. Let's highlight two actual projections: the one that finishes better than 20% of projections, and the one that finishes better than 80% of projections.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-1)>>> def finishes_at_quantile(df, q):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-2)... nth_element = int(np.ceil(q * (df.shape[1] - 1))) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-3)... nth_index = np.argsort(df.iloc[-1])[nth_element] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-4)... return df.iloc[:, nth_index] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-6)>>> btc_projections.vbt.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-7)... plot_lower=partial(finishes_at_quantile, q=0.2), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-8)... plot_middle=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-9)... plot_upper=partial(finishes_at_quantile, q=0.8), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-22-10)... ).show()
 
[/code]

 1. 2. 3. 4. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/custom_bands.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/custom_bands.dark.svg#only-dark)

And that's why the final (or any other) performance isn't necessarily representative of the overall performance: even though the upper band finished in the top 20% of projections by their final value, it spent most of the time below the baseline.


# Filtering[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#filtering "Permanent link")

Not always we want to analyze the entire projection array. What if we're interested only in the projections that cross a certain threshold during a certain period of time? Let's filter and display both `BTCUSDT` and `ETHUSDT` projections that crossed a 5% return threshold at any time during the first two bars:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-1)>>> crossed_mask = projections.expanding().max().iloc[1] >= 1.05 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-2)>>> filt_projections = projections.loc[:, crossed_mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-3)>>> filt_projections.iloc[-1].describe() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-4)count 8.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-5)mean 1.095870
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-6)std 0.084343
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-7)min 0.955078
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-8)25% 1.059109
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-9)50% 1.092623
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-10)75% 1.139190
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-11)max 1.214039
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-12)Name: 2022-06-04 00:00:00+00:00, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-23-14)>>> filt_projections.loc[:, crossed_mask].vbt.plot_projections().show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/filtering.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/filtering.dark.svg#only-dark)

If the price increased by 5% during the first 2 bars after our pattern, 80% of the found occurrences stayed above that 5% mark, 50% of the occurrences crossed the 9% mark, and every fourth occurrence even crossed the 14% mark after 4 bars.


# Latest projections[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#latest-projections "Permanent link")

So far, we've covered projection analysis of patterns and a period of time after them, but there is a use case that requires a special treatment: patterns based on the latest price. The idea is to search for similar occurrences of the latest price development such that we can project them into the future to make predictions. Let's select the latest date range of 7 bars from our `BTCUSDT` data that we want to use for prediction. We'll manually provide search configs and use rescaling through rebasing to search for occurrences that match our pattern in both shape and magnitude:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-24-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-24-2)... pattern=data.close.iloc[-7:],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-24-3)... rescale_mode="rebase",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-24-4)... overlap_mode="allow"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-24-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-24-6)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-24-7)5
 
[/code]

The algorithm has found a total of 5 occurrences with the similarity score of more than 85%. One of those occurrences is marked as an open range and have the score of 100% (see `pattern_ranges.records_readable`) since they exactly match the latest price as the prototype of our pattern. Let's exclude it and plot the pattern projections:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-25-1)>>> pattern_ranges = pattern_ranges.status_closed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-25-2)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-25-3)4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-25-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-25-5)>>> projections = pattern_ranges.get_projections()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-25-6)>>> projections.vbt.plot_projections(plot_bands=False).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/latest_pattern_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/latest_pattern_projections.dark.svg#only-dark)

We've got a pretty accurate pattern ranges, but what we need are delta ranges that come after the pattern ranges. Let's project 7 bars into the future and visualize the projections as possible continuations of the latest price:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-26-1)>>> delta_ranges = pattern_ranges.with_delta(7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-26-2)>>> projections = delta_ranges.get_projections(start_value=-1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-26-3)>>> fig = data.iloc[-7:].plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-26-4)>>> projections.vbt.plot_projections(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-26-5)>>> fig.show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/latest_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/latest_projections.dark.svg#only-dark)

As we can see, both the median and the mean band are rising, which gives us hope that the price might rise in the future. Let's quantify this observation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-1)>>> projections.mean(axis=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-2)2022-05-31 00:00:00+00:00 31801.040000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-3)2022-06-01 00:00:00+00:00 31955.412346
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-4)2022-06-02 00:00:00+00:00 32950.202299
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-5)2022-06-03 00:00:00+00:00 33227.236565
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-6)2022-06-04 00:00:00+00:00 35188.975154
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-7)2022-06-05 00:00:00+00:00 35928.715257
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-8)2022-06-06 00:00:00+00:00 35916.453055
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-9)2022-06-07 00:00:00+00:00 36003.074673
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-27-10)Freq: D, dtype: float64
 
[/code]

Our data is defined between `2020-06-01` and `2022-06-01`, let's fetch the next 7 bars to see how that prediction played out:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-1)>>> next_data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-2)... "BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-3)... start="2022-05-31", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-4)... end="2022-06-08"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-6)>>> next_data.close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-7)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-8)2022-05-31 00:00:00+00:00 31801.04
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-9)2022-06-01 00:00:00+00:00 29805.83
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-10)2022-06-02 00:00:00+00:00 30452.62
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-11)2022-06-03 00:00:00+00:00 29700.21
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-12)2022-06-04 00:00:00+00:00 29864.04
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-13)2022-06-05 00:00:00+00:00 29919.21
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-14)2022-06-06 00:00:00+00:00 31373.10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-15)2022-06-07 00:00:00+00:00 31125.33
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-28-16)Freq: D, Name: Close, dtype: float64
 
[/code]

Even though we've got three out of four projections that predicted the price to be highly above the baseline, the actual price development is less rosy. And this is a very important concept to grasp: there is no guarantee that the future will unfold the same way as projected. What matters though is the number of projections driving up the statistical significance (a sample of 4 projections is way to too small), and the consistency of predictions (the one comparison above is way too few to be representative of the pattern's prediction power). To have both the first and the second number in a range of hundreds, we need more data (higher frequency or/and number of assets) and cross-validation.


# Quick plotting[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#quick-plotting "Permanent link")

Manually building and visualizing projections might be useful when the main objective is statistical analysis, but might be cumbersome for quickly plotting things. In fact, there is a method [Ranges.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections) that combines both parts: generation and visualization of projections. The first part is done by calling [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections). The second part is done by calling [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections). That's why it takes all the arguments accepted by those two methods, and more. It also allows us to plot projection lines as continuations of the price line, which is quite handy for making predictions:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-29-1)>>> delta_ranges.plot_projections().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/ranges_plot_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/ranges_plot_projections.dark.svg#only-dark)

Hint

To plot OHLC, pass `open`, `high`, `low`, and `close` to any method that creates ranges, such as [Ranges.with_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.with_delta).


# Non-uniform projections[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#non-uniform-projections "Permanent link")

The impact of patterns on the price is very easy to project since such projections usually have the same duration (delta). But sometimes, projections should be generated from ranges that are not uniform, for instance, ranges that span between entry and exit signals and have a varying duration. Let's analyze a slightly more advanced use case: moving average crossovers! 

We'll generate a number of window combinations, and check whether the price development after entry signals differs from the price development after exit signals. Below, we're generating entry and exit signals from crossovers based on 136 different window combinations, with a minimum difference of 5 between a fast and slow window to reduce noisy crossovers.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-1)>>> windows = np.arange(10, 31)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-2)>>> window_tuples = combinations(windows, 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-3)>>> window_tuples = filter(lambda x: abs(x[0] - x[1]) >= 5, window_tuples)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-4)>>> fast_windows, slow_windows = zip(*window_tuples)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-5)>>> fast_sma = data.run("sma", fast_windows, short_name="fast_sma")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-6)>>> slow_sma = data.run("sma", slow_windows, short_name="slow_sma")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-7)>>> entries = fast_sma.real_crossed_above(slow_sma.real)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-8)>>> exits = fast_sma.real_crossed_below(slow_sma.real)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-10)>>> entries.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-30-11)(730, 136)
 
[/code]

First, let's check whether the generated entry and exit signals have different delta projections. For this, we'll use the accessor method [SignalsAccessor.delta_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.delta_ranges), which builds delta ranges directly from signals. The only parameter we have to specify here is the delta, which will be 30 bars. To avoid using incomplete data, we'll query the closed ranges only:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-1)>>> entry_ranges = entries.vbt.signals.delta_ranges(30, close=data.close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-2)>>> entry_ranges = entry_ranges.status_closed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-3)>>> entry_ranges.count().sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-4)2233
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-6)>>> exit_ranges = exits.vbt.signals.delta_ranges(30, close=data.close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-7)>>> exit_ranges = exit_ranges.status_closed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-8)>>> exit_ranges.count().sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-31-9)2233
 
[/code]

Second, we'll extract the price projections within those ranges:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-32-1)>>> entry_projections = entry_ranges.get_projections()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-32-2)>>> entry_projections.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-32-3)(31, 2233)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-32-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-32-5)>>> exit_projections = exit_ranges.get_projections()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-32-6)>>> exit_projections.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-32-7)(31, 2233)
 
[/code]

Remember how we worked with just 4 projections? We now have 4.5k! 

Finally, let's plot the bands of both datasets on a single chart:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-1)>>> fig = entry_projections.vbt.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-2)... plot_projections=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-3)... plot_aux_middle=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-4)... plot_fill=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-5)... lower_trace_kwargs=dict(name="Lower (entry)", line_color="green"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-6)... middle_trace_kwargs=dict(name="Middle (entry)", line_color="green"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-7)... upper_trace_kwargs=dict(name="Upper (entry)", line_color="green"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-9)>>> fig = exit_projections.vbt.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-10)... plot_projections=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-11)... plot_aux_middle=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-12)... plot_fill=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-13)... lower_trace_kwargs=dict(name="Lower (exit)", line_color="orangered"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-14)... middle_trace_kwargs=dict(name="Middle (exit)", line_color="orangered"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-15)... upper_trace_kwargs=dict(name="Upper (exit)", line_color="orangered"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-16)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-33-18)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/entry_exit_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/entry_exit_projections.dark.svg#only-dark)

Surprised? Exits seem to consistently outperform entries right after the event, but ultimately lose to them big-time in the long term. Of course this analysis can be further decomposed by window length or difference, but this is left as an exercise for the reader.

The projections we've generated above are still uniform because they all have the same length and can be easily managed. But what if our projections had varying lengths? Let's generate a projection from the price located between each consecutive entry and exit pair for long trades, and vice versa for short trades. This format has the benefit of closely matching the performance of the trades that would be otherwise produced by passing the signal arrays to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals). To represet each pair of signals as a range, we can use the accessor method [SignalsAccessor.between_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_ranges):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-1)>>> entry_ranges = entries.vbt.signals.between_ranges(exits, close=data.close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-2)>>> entry_ranges = entry_ranges.status_closed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-3)>>> entry_ranges.count().sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-4)2240
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-6)>>> exit_ranges = exits.vbt.signals.between_ranges(entries, close=data.close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-7)>>> exit_ranges = exit_ranges.status_closed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-8)>>> exit_ranges.count().sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-9)2118
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-11)>>> entry_projections = entry_ranges.get_projections()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-12)>>> entry_projections.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-13)(124, 2240)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-15)>>> exit_projections = exit_ranges.get_projections()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-16)>>> exit_projections.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-34-17)(83, 2118)
 
[/code]

We can see right away that both arrays have a different number of rows now. Not only that: projections themselves have different lengths and are padded at the end by NaNs. If we attempted to plot any of the arrays, it would take an eternity to create thousands of scatter traces. Whenever we cannot plot something because of its size, we should select a subset of elements (columns in our case) randomly:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-35-1)>>> rand_cols = np.random.choice(entry_projections.shape[1], 100)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-35-2)>>> entry_projections.iloc[:, rand_cols].vbt.plot_projections(plot_bands=False).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/rand_entry_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/rand_entry_projections.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-36-1)>>> rand_cols = np.random.choice(exit_projections.shape[1], 100)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-36-2)>>> exit_projections.iloc[:, rand_cols].vbt.plot_projections(plot_bands=False).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/rand_exit_projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/rand_exit_projections.dark.svg#only-dark)

There a lot shorter projections and a few longer ones. What's interesting is that, on a larger scale, entries are followed exclusively by bull runs and exits by bear runs.


# Shrinking[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#shrinking "Permanent link")

What's problematic though is building the confidence bands since the first points will have much more observations (non-NaN values) than the last ones. In case we want to "shrink" the projection period, we can either keep bigger projections and cut them afterwards using Pandas, or use the `proj_period` argument in [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections), which can be provided either as an integer (= number of rows) or a timedelta. Let's reduce our projections to 30 days:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-37-1)>>> entry_projections = entry_ranges.get_projections(proj_period="30d")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-37-2)>>> entry_projections.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-37-3)(31, 2240)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-37-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-37-5)>>> exit_projections = exit_ranges.get_projections(proj_period="30d")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-37-6)>>> exit_projections.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-37-7)(31, 2118)
 
[/code]

There are now 31 rows in each array, one baseline row and 30 projection rows. Let's plot the generated projections:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-38-1)>>> rand_cols = np.random.choice(entry_projections.shape[1], 100)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-38-2)>>> entry_projections.iloc[:, rand_cols].vbt.plot_projections().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/entry_proj_period.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/entry_proj_period.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-39-1)>>> rand_cols = np.random.choice(exit_projections.shape[1], 100)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-39-2)>>> exit_projections.iloc[:, rand_cols].vbt.plot_projections().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/exit_proj_period.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/exit_proj_period.dark.svg#only-dark)

We are now more confident that a combination of above-crossovers as entry trades and below-crossovers as exit trades mostly generated positive returns, especially in the long term. Those two graphs alone are worth more than dozens of crossover heatmaps because we can analyze the impact of arbitrary events across the time dimension. Selecting projections randomly as we did above is also a form of validation: we can assess the consistency of our findings by plotting random projections multiple times.


# Stretching[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#stretching "Permanent link")

There is also a way to bring non-uniform projections to a uniform format: by using the argument `extend` we can "extend" shorter projections to the period of the biggest projection (or `proj_period`) by including the price that comes after the projection's end. This is effectively the same as generating delta ranges. Let's shrink our signal projections to 30 days and then extend smaller projections to bring all projections to the same length:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-1)>>> entry_projections = entry_ranges.get_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-2)... proj_period="30d", extend=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-4)>>> entry_projections.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-5)(31, 2240)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-7)>>> exit_projections = exit_ranges.get_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-8)... proj_period="30d", extend=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-10)>>> exit_projections.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-11)(31, 2118)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-13)>>> rand_cols = np.random.choice(entry_projections.shape[1], 100)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-40-14)>>> entry_projections.iloc[:, rand_cols].vbt.plot_projections().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/entry_extend.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/entry_extend.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-41-1)>>> rand_cols = np.random.choice(exit_projections.shape[1], 100)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-41-2)>>> exit_projections.iloc[:, rand_cols].vbt.plot_projections().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/exit_extend.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/exit_extend.dark.svg#only-dark)

Stretching has extended each projection beyond its opposite signal, making it redundant. By looking at the chart, we can clearly see that without the opposite signal the advantage of using crossovers vanishes, thus this analysis has once again underlined the importance of properly timing the exit.


# Quick plotting[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#quick-plotting_1 "Permanent link")

Similarly to how we combined generation and visualization of projections before, we can combine all the steps above using [Ranges.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections). The only difference is that this method allows only one column to be plotted. We can also use various arguments to filter the ranges: for example, we can use `min_duration` and `max_duration` to filter out short and long ranges respectively before generating projections, or select a number of the most recent ranges using the argument `last_n`. Let's select the 10 most recent ranges:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-1)>>> entry_ranges.wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-2)MultiIndex([(10, 15),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-3) (10, 16),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-4) (10, 17),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-5) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-6) (24, 29),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-7) (24, 30),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-8) (25, 30)],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-9) names=['fast_sma_timeperiod', 'slow_sma_timeperiod'], length=136)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-11)>>> entry_ranges.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-12)... column=(25, 30),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-13)... last_n=10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-14)... proj_period="30d", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-15)... extend=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-16)... plot_lower=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-17)... plot_upper=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-18)... plot_aux_middle=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-19)... projection_trace_kwargs=dict(opacity=0.3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-42-20)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/plot_projections_25_30.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/plot_projections_25_30.dark.svg#only-dark)

The above graph can be read like this: "How the price would probably react if we saw an upward crossover of the 25 and 30 SMA today?".

Hint

You can disable plotting of the price by setting `plot_close` to `False`.


# Open projections[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#open-projections "Permanent link")

Another use case is when the latest range (or trade) is not closed. Applied to the crossover scenario above, it means that the latest entry has no exit (or vice versa), and so we would be primarily interested in projections that do not start from the signal, but continue from the point we are currently at. Let's regenerate our ranges but with open ranges allowed. Since most of the recent crossovers were exits, we'll apply our analysis to the exit signals. Suppose that we've opened a short trade at the latest exit signal, and we're looking for the further price development to decide whether the trade should be closed before the next entry:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-43-1)>>> exit_ranges = exits.vbt.signals.between_ranges(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-43-2)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-43-3)... incl_open=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-43-4)... close=data.close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-43-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-43-6)>>> exit_ranges.count().sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-43-7)2240
 
[/code]

What are the columns where the last exit has no entry?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-44-1)>>> exit_ranges.wrapper.columns[exit_ranges.status_open.col_arr]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-44-2)MultiIndex([(10, 17),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-44-3) (10, 18),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-44-4) (10, 19),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-44-5) (24, 29),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-44-6) (24, 30),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-44-7) (25, 30)],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-44-8) names=['fast_sma_timeperiod', 'slow_sma_timeperiod'], length=122)
 
[/code]

Let's call the method [Ranges.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections) on the **closed** ranges of the column `(20, 30)`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-45-1)>>> exit_ranges.status_closed.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-45-2)... column=(20, 30), plot_bands=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-45-3)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/open_projections_closed.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/open_projections_closed.dark.svg#only-dark)

And now with the open range included:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-46-1)>>> exit_ranges.plot_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-46-2)... column=(20, 30), plot_bands=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-46-3)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/open_projections_all.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/open_projections_all.dark.svg#only-dark)

What happened? The method noticed that the last range is open (i.e., last signal has no opposite signal), and so it instructed the [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections) to generate projections starting at the signal point. This behavior is controlled by the argument `proj_start`, which has the value `current_or_0` by default. Whenever there is an open range, it uses the signal point as the start, otherwise the first point. The other argument that controls the plotting period of the price - `plot_past_period` \- has the default value `current_or_proj_period`, which plots the close from the signal point if there is an open range, otherwise it's set to the projection period.

To better illustrate this, let's plot all projections from the signal point:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-1)>>> column = (20, 30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-2)>>> signal_index = data.wrapper.index[np.flatnonzero(exits[column])[-1]]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-3)>>> plot_start_index = signal_index - pd.Timedelta(days=10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-4)>>> sub_close = data.close[plot_start_index:]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-5)>>> sub_exits = exits.loc[plot_start_index:, column]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-7)>>> fig = sub_close.vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-8)>>> sub_exits.vbt.signals.plot_as_exits(sub_close, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-9)>>> projections = exit_ranges[column].status_closed.get_projections(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-10)... start_value=sub_close.loc[signal_index],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-11)... start_index=signal_index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-13)>>> projections.vbt.plot_projections(plot_bands=False, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#__codelineno-47-14)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/open_projections_sub.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/open_projections_sub.dark.svg#only-dark)

As we can see, by the end of the price there are only two projections left, and that's why other projections were disregarded by the previous plot.


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/projections/#summary "Permanent link")

We learned how to recognize patterns in any time series and evaluate their impact on price development using projections without a single bit of backtesting. Doing so allows us to analyze arbitrary events without having to deal with numerous culprits of backtesting, such as setting a proper initial capital, position sizing, and performance accumulation. By taking into consideration the price and only the price, we're setting up a perfectly fair experiment that can give us clues about how our trading strategy would have performed if we entered a position at one point and exited it at another. But still, having a pool of several projections is not enough: as with everything in statistics, we need a sample of events big enough to derive their impact with a certain confidence. Otherwise, we can easily get fooled by astonishing results.

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/patterns-and-projections/projections.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/PatternsProjections.ipynb)