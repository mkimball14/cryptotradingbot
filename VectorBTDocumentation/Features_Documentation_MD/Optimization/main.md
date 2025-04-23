# Optimization[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#optimization "Permanent link")


# Purged CV[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#purged-cv "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_4_1.svg)

 * Added support for walk-forward cross-validation (CV) with purging and combinatorial CV with purging and embargoing, as inspired by the Marcos Lopez de Prado's [Advances in Financial Machine Learning](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086).

Create and plot a combinatorial splitter with purging and embargoing
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-0-1)>>> splitter = vbt.Splitter.from_purged_kfold(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-0-2)... vbt.date_range("2024", "2025"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-0-3)... n_folds=10,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-0-4)... n_test_folds=2, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-0-5)... purge_td="3 days",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-0-6)... embargo_td="3 days"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-0-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-0-8)>>> splitter.plots().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/purged_cv.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/purged_cv.dark.svg#only-dark)


# Paramables[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#paramables "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_4_1.svg)

 * Each analyzable VBT object (such as data, indicator, or portfolio) can now be split into items - multiple objects of the same type with only one column/group. This enables using VBT objects as standalone parameters and processing only a subset of information, such as symbol in a data instance or parameter combination in an indicator, at a time.

Combine outputs of a SMA indicator combinatorially
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-1)>>> @vbt.parameterized(merge_func="column_stack")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-2)... def get_signals(fast_sma, slow_sma): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-3)... entries = fast_sma.crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-4)... exits = fast_sma.crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-5)... return entries, exits
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-6)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-7)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-8)>>> sma = data.run("talib:sma", timeperiod=range(20, 50, 2)) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-9)>>> fast_sma = sma.rename_levels({"sma_timeperiod": "fast"}) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-10)>>> slow_sma = sma.rename_levels({"sma_timeperiod": "slow"})
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-11)>>> entries, exits = get_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-12)... vbt.Param(fast_sma, condition="__fast__ < __slow__"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-13)... vbt.Param(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-15)>>> entries.columns
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-16)MultiIndex([(20, 22, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-17) (20, 22, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-18) (20, 24, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-19) (20, 24, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-20) (20, 26, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-21) (20, 26, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-22) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-23) (44, 46, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-24) (44, 46, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-25) (44, 48, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-26) (44, 48, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-27) (46, 48, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-28) (46, 48, 'ETH-USD')],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-1-29) names=['fast', 'slow', 'symbol'], length=210)
 
[/code]

 1. 2. 3. 4. 


# Lazy parameter grids[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#lazy-parameter-grids "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2023_12_23.svg)

 * [Parameterized decorator](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#parameterized-decorator) no longer necessarily materializes parameter grids if you're only interested in a subset of all parameter combinations. Consequently, this enables the generation of random parameter combinations to be almost instant, regardless of the total number of all possible parameter combinations.

Test a random subset of a huge number of parameter combinations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-1)>>> @vbt.parameterized(merge_func="concat")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-2)... def test_combination(data, n, sl_stop, tsl_stop, tp_stop):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-3)... return data.run(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-4)... "from_random_signals", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-5)... n=n, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-6)... sl_stop=sl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-7)... tsl_stop=tsl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-8)... tp_stop=tp_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-9)... ).total_return
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-11)>>> n = np.arange(10, 100)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-12)>>> sl_stop = np.arange(1, 1000) / 1000
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-13)>>> tsl_stop = np.arange(1, 1000) / 1000
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-14)>>> tp_stop = np.arange(1, 1000) / 1000
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-15)>>> len(n) * len(sl_stop) * len(tsl_stop) * len(tp_stop)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-16)89730269910
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-18)>>> test_combination(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-19)... vbt.YFData.pull("BTC-USD"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-20)... n=vbt.Param(n),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-21)... sl_stop=vbt.Param(sl_stop),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-22)... tsl_stop=vbt.Param(tsl_stop),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-23)... tp_stop=vbt.Param(tp_stop),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-24)... _random_subset=10
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-26)n sl_stop tsl_stop tp_stop
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-27)34 0.188 0.916 0.749 6.869901
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-28)44 0.176 0.734 0.550 6.186478
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-29)50 0.421 0.245 0.253 0.540188
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-30)51 0.033 0.951 0.344 6.514647
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-31) 0.915 0.461 0.322 2.915987
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-32)73 0.057 0.690 0.008 -0.204080
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-33)74 0.368 0.360 0.935 14.207262
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-34)76 0.771 0.342 0.187 -0.278499
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-35)83 0.796 0.788 0.730 6.450076
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-36)96 0.873 0.429 0.815 18.670965
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-2-37)dtype: float64
 
[/code]


# Mono-chunks[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#mono-chunks "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_13_0.svg)

 * [Parameterized decorator](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#parameterized-decorator) has been extended to split parameter combinations into so-called "mono-chunks", merge the parameter values within each chunk into a single value, and execute the entire chunk with a single function call. This way, you are not limited by only one parameter combination being processed at a time anymore ![🌪](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f32a.svg) Just note: you must adapt the function to take multiple parameter values and change the merging function as appropriate.

Test 100 combinations of SL and TP values per thread
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-1)>>> @vbt.parameterized(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-2)... merge_func="concat", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-3)... mono_chunk_len=100, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-4)... chunk_len="auto", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-5)... engine="threadpool", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-6)... warmup=True 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-7)... ) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-8)... @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-9)... def test_stops_nb(close, entries, exits, sl_stop, tp_stop):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-10)... sim_out = vbt.pf_nb.from_signals_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-11)... target_shape=(close.shape[0], sl_stop.shape[1]),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-12)... group_lens=np.full(sl_stop.shape[1], 1),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-13)... close=close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-14)... long_entries=entries,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-15)... short_entries=exits,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-16)... sl_stop=sl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-17)... tp_stop=tp_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-18)... save_returns=True
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-19)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-20)... return vbt.ret_nb.total_return_nb(sim_out.in_outputs.returns)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-21)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-22)>>> data = vbt.YFData.pull("BTC-USD", start="2020") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-23)>>> entries, exits = data.run("randnx", n=10, hide_params=True, unpack=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-24)>>> sharpe_ratios = test_stops_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-25)... vbt.to_2d_array(data.close),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-26)... vbt.to_2d_array(entries),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-27)... vbt.to_2d_array(exits),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-28)... sl_stop=vbt.Param(np.arange(0.01, 1.0, 0.01), mono_merge_func=np.column_stack), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-29)... tp_stop=vbt.Param(np.arange(0.01, 1.0, 0.01), mono_merge_func=np.column_stack)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-30)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-3-31)>>> sharpe_ratios.vbt.heatmap().show()
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/chunked_params.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/chunked_params.dark.svg#only-dark)


# CV decorator[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#cv-decorator "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_1.svg)

 * Most cross-validation tasks involve testing a grid of parameter combinations on the training data, selecting the best parameter combination, and validating it on the test data. This procedure needs to be repeated on each split. The cross-validation decorator combines the parameterized and split decorators to automate such a task.

Tutorial

Learn more in the [Cross-validation](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation) tutorial.

Cross-validate a SMA crossover using random search
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-1)>>> @vbt.cv_split(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-2)... splitter="from_rolling", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-3)... splitter_kwargs=dict(length=365, split=0.5, set_labels=["train", "test"]),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-4)... takeable_args=["data"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-5)... parameterized_kwargs=dict(random_subset=100),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-6)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-8)... def sma_crossover_cv(data, fast_period, slow_period, metric):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-9)... fast_sma = data.run("sma", fast_period, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-10)... slow_sma = data.run("sma", slow_period, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-11)... entries = fast_sma.real_crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-12)... exits = fast_sma.real_crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-13)... pf = vbt.PF.from_signals(data, entries, exits, direction="both")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-14)... return pf.deep_getattr(metric)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-15)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-16)>>> sma_crossover_cv(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-17)... vbt.YFData.pull("BTC-USD", start="4 years ago"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-18)... vbt.Param(np.arange(20, 50), condition="x < slow_period"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-19)... vbt.Param(np.arange(20, 50)),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-20)... "trades.expectancy"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-4-21)... )
 
[/code]

Split 7/7
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-1)split set fast_period slow_period
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-2)0 train 20 25 8.015725
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-3) test 20 23 0.573465
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-4)1 train 40 48 -4.356317
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-5) test 39 40 5.666271
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-6)2 train 24 45 18.253340
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-7) test 22 36 111.202831
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-8)3 train 20 31 54.626024
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-9) test 20 25 -1.596945
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-10)4 train 25 48 41.328588
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-11) test 25 30 6.620254
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-12)5 train 26 32 7.178085
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-13) test 24 29 4.087456
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-14)6 train 22 23 -0.581255
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-15) test 22 31 -2.494519
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-5-16)dtype: float64
 
[/code]


# Split decorator[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#split-decorator "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_1.svg)

 * Normally, to run a function on each split, you need to build a splitter specifically targeted at the input data passed to the function. That is, each time the input data changes, you need to rebuild the splitter. This process is automated by the split decorator, which wraps a function and thus gets access to all the arguments the function receives to do various splitting decisions. Basically, it can "infect" any Python function with splitting functionality ![🦠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f9a0.svg)

Tutorial

Learn more in the [Cross-validation](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation) tutorial.

Get total return from holding in each quarter
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-1)>>> @vbt.split(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-2)... splitter="from_grouper", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-3)... splitter_kwargs=dict(by="Q"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-4)... takeable_args=["data"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-5)... merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-7)... def get_quarter_return(data):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-8)... return data.returns.vbt.returns.total()
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-9)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-10)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-11)>>> get_quarter_return(data.loc["2021"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-12)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-13)2021Q1 1.005805
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-14)2021Q2 -0.407050
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-15)2021Q3 0.304383
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-16)2021Q4 -0.037627
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-17)Freq: Q-DEC, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-18)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-19)>>> get_quarter_return(data.loc["2022"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-20)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-21)2022Q1 -0.045047
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-22)2022Q2 -0.572515
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-23)2022Q3 0.008429
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-24)2022Q4 -0.143154
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-6-25)Freq: Q-DEC, dtype: float64
 
[/code]


# Conditional parameters[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#conditional-parameters "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_1.svg)

 * Parameters can depend on each other. For instance, when testing a crossover of moving averages, it makes no sense to test a fast window that has a bigger length than the slow window. By filtering such cases out, you only need to evaluate half as many parameter combinations.

Test slow windows being longer than fast windows by at least 5
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-1)>>> @vbt.parameterized(merge_func="column_stack")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-2)... def ma_crossover_signals(data, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-3)... fast_sma = data.run("sma", fast_window, short_name="fast_sma")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-4)... slow_sma = data.run("sma", slow_window, short_name="slow_sma")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-5)... entries = fast_sma.real_crossed_above(slow_sma.real)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-6)... exits = fast_sma.real_crossed_below(slow_sma.real)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-7)... return entries, exits
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-8)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-9)>>> entries, exits = ma_crossover_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-10)... vbt.YFData.pull("BTC-USD", start="one year ago UTC"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-11)... vbt.Param(np.arange(5, 50), condition="slow_window - fast_window >= 5"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-12)... vbt.Param(np.arange(5, 50))
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-14)>>> entries.columns
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-15)MultiIndex([( 5, 10),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-16) ( 5, 11),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-17) ( 5, 12),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-18) ( 5, 13),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-19) ( 5, 14),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-20) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-21) (42, 48),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-22) (42, 49),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-23) (43, 48),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-24) (43, 49),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-25) (44, 49)],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-7-26) names=['fast_window', 'slow_window'], length=820)
 
[/code]


# Splitter[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#splitter "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_0.svg)

 * Splitters in [scikit-learn](https://scikit-learn.org/stable/) are a poor fit for validating ML-based and rule-based trading strategies; VBT has a juggernaut class that supports various splitting schemes safe for backtesting, including rolling windows, expanding windows, time-anchored windows, random windows for block bootstraps, and even Pandas-native `groupby` and `resample` instructions such as "M" for monthly frequency. As the cherry on the cake, the produced splits can be easily analyzed and visualized too! For example, you can detect any split or set overlaps, convert all the splits into a single boolean mask for custom analysis, group splits and sets, and analyze their distribution relative to each other. The class has more lines of code than the entire [backtesting.py](https://github.com/kernc/backtesting.py) package, don't underestimate the new king in town! ![🦏](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f98f.svg)

Tutorial

Learn more in the [Cross-validation](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation) tutorial.

Roll a 360-day window and split it equally into train and test sets
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-1)>>> data = vbt.YFData.pull("BTC-USD", start="4 years ago")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-2)>>> splitter = vbt.Splitter.from_rolling(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-3)... data.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-4)... length="360 days",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-5)... split=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-6)... set_labels=["train", "test"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-7)... freq="daily"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-8-9)>>> splitter.plots().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/splitter.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/splitter.dark.svg#only-dark)


# Random search[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#random-search "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_7_0.svg)

 * While grid search looks at every possible combination of hyperparameters, random search only selects and tests a random combination of hyperparameters. This is especially useful when the number of parameter combinations is huge. Also, random search has shown to find equal or better values than grid search within fewer function evaluations. The indicator factory, parameterized decorator, and any method that does broadcasting now supports random search out of the box.

Test a random subset of SL, TSL, and TP combinations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-1)>>> data = vbt.YFData.pull("BTC-USD", start="2020")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-2)>>> stop_values = np.arange(1, 100) / 100 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-3)>>> pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-4)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-5)... n=100, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-6)... sl_stop=vbt.Param(stop_values),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-7)... tsl_stop=vbt.Param(stop_values),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-8)... tp_stop=vbt.Param(stop_values),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-9)... broadcast_kwargs=dict(random_subset=1000) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-11)>>> pf.total_return.sort_values(ascending=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-12)sl_stop tsl_stop tp_stop
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-13)0.06 0.85 0.43 2.291260
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-14) 0.74 0.40 2.222212
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-15) 0.97 0.22 2.149849
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-16)0.40 0.10 0.23 2.082935
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-17)0.47 0.09 0.25 2.030105
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-18) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-19)0.51 0.36 0.01 -0.618805
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-20)0.53 0.37 0.01 -0.624761
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-21)0.35 0.60 0.02 -0.662992
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-22)0.29 0.13 0.02 -0.671376
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-23)0.46 0.72 0.02 -0.720024
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-9-24)Name: total_return, Length: 1000, dtype: float64
 
[/code]

 1. 2. 


# Parameterized decorator[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#parameterized-decorator "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_7_0.svg)

 * There is a special decorator that can make any Python function accept multiple parameter combinations, even if the function itself can handle only one! The decorator wraps the function, thus getting access to its arguments; it then identifies all the arguments that act as parameters, builds a grid of them, and calls the underlying function on each parameter combination from that grid. The execution part can be easily parallelized. After all the outputs are ready, it merges them into a single object. Use cases are endless: from running indicators that cannot be wrapped with the indicator factory, to parameterizing entire pipelines! ![🪄](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1fa84.svg)

Example 1: Parameterize a simple SMA indicator without Indicator Factory
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-10-1)>>> @vbt.parameterized(merge_func="column_stack") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-10-2)... def sma(close, window):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-10-3)... return close.rolling(window).mean()
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-10-4)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-10-5)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-10-6)>>> sma(data.close, vbt.Param(range(20, 50)))
 
[/code]

 1. 

Combination 30/30
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-1)window 20 21 22 \
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-2)Date 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-3)2014-09-17 00:00:00+00:00 NaN NaN NaN 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-4)2014-09-18 00:00:00+00:00 NaN NaN NaN 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-5)2014-09-19 00:00:00+00:00 NaN NaN NaN 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-6)... ... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-7)2024-03-07 00:00:00+00:00 57657.135156 57395.376488 57147.339134 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-8)2024-03-08 00:00:00+00:00 58488.990039 58163.942708 57891.045455 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-9)2024-03-09 00:00:00+00:00 59297.836523 58956.156064 58624.648793 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-11)...
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-12)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-13)window 48 49 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-14)Date 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-15)2014-09-17 00:00:00+00:00 NaN NaN 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-16)2014-09-18 00:00:00+00:00 NaN NaN 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-17)2014-09-19 00:00:00+00:00 NaN NaN 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-18)... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-19)2024-03-07 00:00:00+00:00 49928.186686 49758.599330 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-20)2024-03-08 00:00:00+00:00 50483.072266 50303.123565 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-21)2024-03-09 00:00:00+00:00 51040.440837 50846.672353 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-22)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-11-23)[3462 rows x 30 columns]
 
[/code]

Example 2: Parameterize an entire Bollinger Bands pipeline
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-1)>>> @vbt.parameterized(merge_func="concat") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-2)... def bbands_sharpe(data, timeperiod=14, nbdevup=2, nbdevdn=2, thup=0.3, thdn=0.1):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-3)... bb = data.run(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-4)... "talib_bbands", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-5)... timeperiod=timeperiod, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-6)... nbdevup=nbdevup, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-7)... nbdevdn=nbdevdn
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-9)... bandwidth = (bb.upperband - bb.lowerband) / bb.middleband
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-10)... cond1 = data.low < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-11)... cond2 = bandwidth > thup
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-12)... cond3 = data.high > bb.upperband
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-13)... cond4 = bandwidth < thdn
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-14)... entries = (cond1 & cond2) | (cond3 & cond4)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-15)... exits = (cond1 & cond4) | (cond3 & cond2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-16)... pf = vbt.PF.from_signals(data, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-17)... return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-18)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-19)>>> bbands_sharpe(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-20)... vbt.YFData.pull("BTC-USD"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-21)... nbdevup=vbt.Param([1, 2]), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-22)... nbdevdn=vbt.Param([1, 2]),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-23)... thup=vbt.Param([0.4, 0.5]),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-24)... thdn=vbt.Param([0.1, 0.2])
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-12-25)... )
 
[/code]

 1. 2. 

Combination 16/16
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-1)nbdevup nbdevdn thup thdn
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-2)1 1 0.4 0.1 1.681532
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-3) 0.2 1.617400
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-4) 0.5 0.1 1.424175
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-5) 0.2 1.563520
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-6) 2 0.4 0.1 1.218554
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-7) 0.2 1.520852
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-8) 0.5 0.1 1.242523
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-9) 0.2 1.317883
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-10)2 1 0.4 0.1 1.174562
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-11) 0.2 1.469828
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-12) 0.5 0.1 1.427940
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-13) 0.2 1.460635
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-14) 2 0.4 0.1 1.000210
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-15) 0.2 1.378108
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-16) 0.5 0.1 1.196087
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-17) 0.2 1.782502
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-13-18)dtype: float64
 
[/code]


# Riskfolio-Lib[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#riskfolio-lib "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_7_0.svg)

 * [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib) is another increasingly popular library for portfolio optimization that has been integrated into VBT. The integration was done by automating typical workflows inside Riskfolio-Lib and putting them into a single function, such that many portfolio optimization problems can be expressed using a single set of keyword arguments and thus parameterized easily.

Tutorial

Learn more in the [Portfolio optimization](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization) tutorial.

Run Nested Clustered Optimization (NCO) on a monthly basis
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-1)>>> data = vbt.YFData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-2)... ["SPY", "TLT", "XLF", "XLE", "XLU", "XLK", "XLB", "XLP", "XLY", "XLI", "XLV"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-3)... start="2020",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-4)... end="2023",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-5)... missing_index="drop"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-7)>>> pfo = vbt.PFO.from_riskfolio(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-8)... returns=data.close.vbt.to_returns(),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-9)... port_cls="hc",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-10)... every="M"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-14-12)>>> pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/riskfolio_lib.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/riskfolio_lib.dark.svg#only-dark)


# Array-like parameters[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#array-like-parameters "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_5_0.svg)

 * Broadcasting mechanism has been completely refactored and now supports parameters. Many parameters in VBT, such as SL and TP, are array-like and can be provided per row, column, and even element. Internally, even a scalar is treated like a regular time series and broadcasted along other proper time series. Thus, to test multiple parameter combinations, one had to tile other time series such that all shapes perfectly match. With this feature, the tiling procedure is performed automatically!

Write a steep slope indicator without indicator factory
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-1)>>> def steep_slope(close, up_th):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-2)... r = vbt.broadcast(dict(close=close, up_th=up_th))
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-3)... return r["close"].pct_change() >= r["up_th"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-4)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-5)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2022")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-6)>>> fig = data.plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-7)>>> sma = vbt.talib("SMA").run(data.close, timeperiod=50).real
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-8)>>> sma.rename("SMA").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-9)>>> mask = steep_slope(sma, vbt.Param([0.005, 0.01, 0.015])) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-11)>>> def plot_mask_ranges(column, color):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-12)... mask.vbt.ranges.plot_shapes(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-13)... column=column, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-14)... plot_close=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-15)... shape_kwargs=dict(fillcolor=color),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-16)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-18)>>> plot_mask_ranges(0.005, "orangered")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-19)>>> plot_mask_ranges(0.010, "orange")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-20)>>> plot_mask_ranges(0.015, "yellow")
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-21)>>> fig.update_xaxes(showgrid=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-22)>>> fig.update_yaxes(showgrid=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-15-23)>>> fig.show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/steep_slope.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/steep_slope.dark.svg#only-dark)


# Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#parameters "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_5_0.svg)

 * There is a new module addition for working with parameters.

Generate 10,000 random parameter combinations for MACD
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-1)>>> from itertools import combinations
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-3)>>> window_space = np.arange(100)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-4)>>> fastk_windows, slowk_windows = list(zip(*combinations(window_space, 2))) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-5)>>> window_type_space = list(vbt.enums.WType)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-6)>>> param_product = vbt.combine_params(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-7)... dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-8)... fast_window=vbt.Param(fastk_windows, level=0), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-9)... slow_window=vbt.Param(slowk_windows, level=0),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-10)... signal_window=vbt.Param(window_space, level=1),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-11)... macd_wtype=vbt.Param(window_type_space, level=2), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-12)... signal_wtype=vbt.Param(window_type_space, level=2),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-13)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-14)... random_subset=10_000,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-15)... build_index=False
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-17)>>> pd.DataFrame(param_product)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-18) fast_window slow_window signal_window macd_wtype signal_wtype
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-19)0 0 1 47 3 3
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-20)1 0 2 21 2 2
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-21)2 0 2 33 1 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-22)3 0 2 42 1 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-23)4 0 3 52 1 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-24)... ... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-25)9995 97 99 19 1 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-26)9996 97 99 92 4 4
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-27)9997 98 99 2 2 2
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-28)9998 98 99 12 1 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-29)9999 98 99 81 2 2
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-30)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-16-31)[10000 rows x 5 columns]
 
[/code]

 1. 2. 3. 


# Portfolio optimization[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#portfolio-optimization "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_2_0.svg)

 * Portfolio optimization is the process of creating a portfolio of assets, for which your investment has the maximum return and minimum risk. Usually, this process is performed periodically and involves generating new weights to rebalance an existing portfolio. As most things in VBT, the weight generation step is implemented as a callback by the user while the optimizer calls that callback periodically. The final result is a collection of the returned weight allocations that can be analyzed, visualized, and used in an actual simulation ![🥧](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f967.svg)

Tutorial

Learn more in the [Portfolio optimization](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization) tutorial.

Allocate assets inversely to their total return in the last month
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-1)>>> def regime_change_optimize_func(data):
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-2)... returns = data.returns
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-3)... total_return = returns.vbt.returns.total()
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-4)... weights = data.symbol_wrapper.fill_reduced(0)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-5)... pos_mask = total_return > 0
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-6)... if pos_mask.any():
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-7)... weights[pos_mask] = total_return[pos_mask] / total_return.abs().sum()
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-8)... neg_mask = total_return < 0
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-9)... if neg_mask.any():
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-10)... weights[neg_mask] = total_return[neg_mask] / total_return.abs().sum()
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-11)... return -1 * weights
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-12)
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-13)>>> data = vbt.YFData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-14)... ["SPY", "TLT", "XLF", "XLE", "XLU", "XLK", "XLB", "XLP", "XLY", "XLI", "XLV"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-15)... start="2020",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-16)... end="2023",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-17)... missing_index="drop"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-19)>>> pfo = vbt.PFO.from_optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-20)... data.symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-21)... regime_change_optimize_func,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-22)... vbt.RepEval("data[index_slice]", context=dict(data=data)),
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-23)... every="M"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-17-25)>>> pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/portfolio_optimization.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/portfolio_optimization.dark.svg#only-dark)


# PyPortfolioOpt[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#pyportfolioopt "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_2_0.svg)

 * [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) is a popular financial portfolio optimization package that includes both classical methods (Markowitz 1952 and Black-Litterman), suggested best practices (e.g covariance shrinkage), along with many recent developments and novel features, like L2 regularisation, shrunk covariance, and hierarchical risk parity.

Tutorial

Learn more in the [Portfolio optimization](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization) tutorial.

Run Nested Clustered Optimization (NCO) on a monthly basis
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-1)>>> data = vbt.YFData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-2)... ["SPY", "TLT", "XLF", "XLE", "XLU", "XLK", "XLB", "XLP", "XLY", "XLI", "XLV"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-3)... start="2020",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-4)... end="2023",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-5)... missing_index="drop"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-7)>>> pfo = vbt.PFO.from_pypfopt(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-8)... returns=data.returns,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-9)... optimizer="hrp",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-10)... target="optimize",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-11)... every="M"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-18-13)>>> pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/pyportfolioopt.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/pyportfolioopt.dark.svg#only-dark)


# Universal Portfolios[¶](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#universal-portfolios "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_2_0.svg)

 * [Universal Portfolios](https://github.com/Marigold/universal-portfolios) is a package putting together different Online Portfolio Selection (OLPS) algorithms.

Tutorial

Learn more in the [Portfolio optimization](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization) tutorial.

Simulate an online minumum-variance portfolio on a weekly time frame
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-1)>>> data = vbt.YFData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-2)... ["SPY", "TLT", "XLF", "XLE", "XLU", "XLK", "XLB", "XLP", "XLY", "XLI", "XLV"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-3)... start="2020",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-4)... end="2023",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-5)... missing_index="drop"
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-7)>>> pfo = vbt.PFO.from_universal_algo(
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-8)... "MPT",
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-9)... data.resample("W").close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-10)... window=52, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-11)... min_history=4, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-12)... mu_estimator='historical', 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-13)... cov_estimator='empirical', 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-14)... method='mpt', 
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-15)... q=0
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#__codelineno-19-17)>>> pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/universal_portfolios.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/universal_portfolios.dark.svg#only-dark)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/features/optimization.py.txt)