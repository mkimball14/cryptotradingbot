# Performance[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#performance "Permanent link")


# Chunk caching[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#chunk-caching "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_5_15.svg)

 * Most workflows using the VBT’s execution framework—such as data pulling, chunking, parameterization, splitting, and optimization—can now offload intermediate results to disk and reload them if the workflow crashes and restarts. You can confidently test billions of parameter combinations on cloud instances without worrying about losing your data!

Execute a basic range with random fallouts while caching successful attempts
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-1)>>> @vbt.parameterized(cache_chunks=True, chunk_len=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-2)... def basic_iterator(i):
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-3)... print("i:", i)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-4)... rand_number = np.random.uniform()
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-5)... if rand_number < 0.2:
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-6)... print("failed ⛔")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-7)... raise ValueError
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-8)... return i
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-9)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-10)>>> attempt = 0
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-11)>>> while True:
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-12)... attempt += 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-13)... print("attempt", attempt)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-14)... try:
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-15)... basic_iterator(vbt.Param(np.arange(10)))
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-16)... print("completed 🎉")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-17)... break
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-18)... except ValueError:
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-19)... pass
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-20)attempt 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-21)i: 0
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-22)i: 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-23)failed ⛔
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-24)attempt 2
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-25)i: 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-26)i: 2
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-27)i: 3
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-28)i: 4
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-29)failed ⛔
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-30)attempt 3
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-31)i: 4
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-32)i: 5
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-33)i: 6
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-34)i: 7
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-35)i: 8
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-36)i: 9
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-0-37)completed 🎉
 
[/code]

 1. 


# Accumulators[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#accumulators "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_10.svg)

 * Most rolling indicators implemented with Pandas and NumPy require running over data more than once. For example, a simple sum of three arrays involves at least two passes over data. Moreover, if you want to calculate such an indicator iterativelly (i.e., bar by bar), you either need to pre-calculate it entirely and store in memory, or re-calculate each window, which may dramatically hit performance. [Accumulators](https://theboostcpplibraries.com/boost.accumulators), on the other hand, keep an internal state that allows you to calculate an indicator value every time a new data point arrives, leading to the best performance possible.

Design a one-pass rolling z-score
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-2)... def fastest_rolling_zscore_1d_nb(arr, window, minp=None, ddof=1):
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-3)... if minp is None:
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-4)... minp = window
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-5)... out = np.full(arr.shape, np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-6)... cumsum = 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-7)... cumsum_sq = 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-8)... nancnt = 0
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-9)... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-10)... for i in range(len(arr)):
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-11)... pre_window_value = arr[i - window] if i - window >= 0 else np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-12)... mean_in_state = vbt.nb.RollMeanAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-13)... i, arr[i], pre_window_value, cumsum, nancnt, window, minp
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-15)... mean_out_state = vbt.nb.rolling_mean_acc_nb(mean_in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-16)... _, _, _, mean = mean_out_state
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-17)... std_in_state = vbt.nb.RollStdAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-18)... i, arr[i], pre_window_value, cumsum, cumsum_sq, nancnt, window, minp, ddof
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-19)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-20)... std_out_state = vbt.nb.rolling_std_acc_nb(std_in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-21)... cumsum, cumsum_sq, nancnt, _, std = std_out_state
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-22)... out[i] = (arr[i] - mean) / std
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-23)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-24)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-25)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-26)>>> rolling_zscore = fastest_rolling_zscore_1d_nb(data.returns.values, 14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-27)>>> data.symbol_wrapper.wrap(rolling_zscore)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-28)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-29)2014-09-17 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-30)2014-09-18 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-31)2014-09-19 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-32) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-33)2023-02-01 00:00:00+00:00 0.582381
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-34)2023-02-02 00:00:00+00:00 -0.705441
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-35)2023-02-03 00:00:00+00:00 -0.217880
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-36)Freq: D, Name: BTC-USD, Length: 3062, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-37)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-38)>>> (data.returns - data.returns.rolling(14).mean()) / data.returns.rolling(14).std()
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-39)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-40)2014-09-17 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-41)2014-09-18 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-42)2014-09-19 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-43) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-44)2023-02-01 00:00:00+00:00 0.582381
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-45)2023-02-02 00:00:00+00:00 -0.705441
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-46)2023-02-03 00:00:00+00:00 -0.217880
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-1-47)Freq: D, Name: Close, Length: 3062, dtype: float64
 
[/code]


# Chunking[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#chunking "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * An innovative new chunking mechanism that takes a specification of how arguments should be chunked, automatically splits array-like arguments, passes each chunk to the function for execution, and merges back the results. This way, you can split large arrays and run any function in a distributed manner! Additionally, VBT implements a central registry and provides the chunking specification for all arguments of most Numba-compiled functions, including the simulation functions. Chunking can be enabled by a single command. No more out-of-memory errors! ![🎉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f389.svg)

Backtest at most 100 parameter combinations at once
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-1)>>> @vbt.chunked(
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-2)... chunk_len=100,
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-3)... merge_func="concat", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-4)... execute_kwargs=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-5)... clear_cache=True,
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-6)... collect_garbage=True
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-9)... def backtest(data, fast_windows, slow_windows): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-10)... fast_ma = vbt.MA.run(data.close, fast_windows, short_name="fast")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-11)... slow_ma = vbt.MA.run(data.close, slow_windows, short_name="slow")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-12)... entries = fast_ma.ma_crossed_above(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-13)... exits = fast_ma.ma_crossed_below(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-14)... pf = vbt.PF.from_signals(data.close, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-15)... return pf.total_return
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-16)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-17)>>> param_product = vbt.combine_params( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-18)... dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-19)... fast_window=vbt.Param(range(2, 100), condition="fast_window < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-20)... slow_window=vbt.Param(range(2, 100)),
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-21)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-22)... build_index=False
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-23)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-24)>>> backtest(
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-25)... vbt.YFData.pull(["BTC-USD", "ETH-USD"]), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-26)... vbt.Chunked(param_product["fast_window"]), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-27)... vbt.Chunked(param_product["slow_window"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-2-28)... )
 
[/code]

 1. 2. 3. 4. 5. 6. 

Chunk 48/48
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-1)fast_window slow_window symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-2)2 3 BTC-USD 193.124482
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-3) ETH-USD 12.247315
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-4) 4 BTC-USD 159.600953
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-5) ETH-USD 15.825041
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-6) 5 BTC-USD 124.703676
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-7) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-8)97 98 ETH-USD 3.947346
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-9) 99 BTC-USD 25.551881
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-10) ETH-USD 3.442949
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-11)98 99 BTC-USD 27.943574
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-12) ETH-USD 3.540720
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-3-13)Name: total_return, Length: 9506, dtype: float64
 
[/code]


# Parallel Numba[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#parallel-numba "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Most Numba-compiled functions were rewritten to process columns in parallel using [automatic parallelization with `@jit`](https://numba.readthedocs.io/en/stable/user/parallel.html), which can be enabled by a single command. Best suited for lightweight functions applied on wide arrays.

Benchmark the rolling mean without and with parallelization
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-1)>>> df = pd.DataFrame(np.random.uniform(size=(1000, 1000)))
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-3)>>> %timeit df.rolling(10).mean() 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-4)45.6 ms ± 138 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-6)>>> %timeit df.vbt.rolling_mean(10) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-7)5.33 ms ± 302 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-8)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-9)>>> %timeit df.vbt.rolling_mean(10, jitted=dict(parallel=True)) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-4-10)1.82 ms ± 5.21 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
 
[/code]

 1. 2. 3. 


# Multithreading[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#multithreading "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Integration of [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor) from `concurrent.futures`, [ThreadPool](https://pathos.readthedocs.io/en/latest/pathos.html#pathos.pools.ThreadPool) from `pathos`, and [Dask](https://dask.org/) backend for running multiple chunks across multiple threads. Best suited for accelerating heavyweight functions that release GIL, such as Numba and C functions. Multithreading + Chunking + Numba = ![💪](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4aa.svg)

Benchmark 1000 random portfolios without and with multithreading
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-5-1)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-5-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-5-3)>>> %timeit vbt.PF.from_random_signals(data.close, n=[100] * 1000)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-5-4)613 ms ± 37.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-5-5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-5-6)>>> %timeit vbt.PF.from_random_signals(data.close, n=[100] * 1000, chunked="threadpool")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-5-7)294 ms ± 8.91 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]


# Multiprocessing[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#multiprocessing "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Integration of [ProcessPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor) from `concurrent.futures`, [ProcessPool](https://pathos.readthedocs.io/en/latest/pathos.html#pathos.pools.ProcessPool) and [ParallelPool](https://pathos.readthedocs.io/en/latest/pathos.html#pathos.pools.ParallelPool) from `pathos`, [WorkerPool](https://sybrenjansen.github.io/mpire/usage/workerpool/index.html) from `mpire`, and [Ray](https://www.ray.io/) backend for running multiple chunks across multiple processes. Best suited for accelerating heavyweight functions that do not release GIL, such as regular Python functions, and accept leightweight arguments that are easy to serialize. Ever wanted to test billions of hyperparameter combinations in a matter of minutes? This is now possible by scaling functions and entire applications up in the cloud using [Ray clusters](https://docs.ray.io/en/latest/cluster/getting-started.html) ![👀](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f440.svg)

Benchmark running a slow function on each column without and with multiprocessing
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-1)>>> @vbt.chunked(
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-2)... size=vbt.ArraySizer(arg_query="items", axis=1),
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-3)... arg_take_spec=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-4)... items=vbt.ArraySelector(axis=1)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-5)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-6)... merge_func=np.column_stack
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-8)... def bubble_sort(items):
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-9)... items = items.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-10)... for i in range(len(items)):
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-11)... for j in range(len(items) - 1 - i):
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-12)... if items[j] > items[j + 1]:
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-13)... items[j], items[j + 1] = items[j + 1], items[j]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-14)... return items
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-15)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-16)>>> items = np.random.uniform(size=(1000, 3))
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-18)>>> %timeit bubble_sort(items)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-19)456 ms ± 1.36 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-20)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-21)>>> %timeit bubble_sort(items, _execute_kwargs=dict(engine="pathos"))
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-6-22)165 ms ± 1.51 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]


# Jitting[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#jitting "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Jitting means just-in-time compiling. In the VBT universe though, jitting simply means accelerating. Although Numba remains the primary jitter, VBT now enables implementation of custom jitter classes, such as that for vectorized NumPy and even [JAX](https://github.com/google/jax) with GPU support. Every jitted function is registered globally, so you can switch between different implementations or even disable jitting entirely using a single command.

Run different implementations of the cumulative sum
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-1)>>> data = vbt.YFData.pull("BTC-USD", start="7 days ago")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-2)>>> log_returns = np.log1p(data.close.pct_change())
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-3)>>> log_returns.vbt.cumsum() 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-4)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-5)2023-01-31 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-6)2023-02-01 00:00:00+00:00 0.024946
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-7)2023-02-02 00:00:00+00:00 0.014271
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-8)2023-02-03 00:00:00+00:00 0.013310
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-9)2023-02-04 00:00:00+00:00 0.008288
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-10)2023-02-05 00:00:00+00:00 -0.007967
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-11)2023-02-06 00:00:00+00:00 -0.010087
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-12)Freq: D, Name: Close, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-13)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-14)>>> log_returns.vbt.cumsum(jitted=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-15)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-16)2023-01-31 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-17)2023-02-01 00:00:00+00:00 0.024946
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-18)2023-02-02 00:00:00+00:00 0.014271
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-19)2023-02-03 00:00:00+00:00 0.013310
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-20)2023-02-04 00:00:00+00:00 0.008288
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-21)2023-02-05 00:00:00+00:00 -0.007967
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-22)2023-02-06 00:00:00+00:00 -0.010087
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-23)Freq: D, Name: Close, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-24)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-25)>>> @vbt.register_jitted(task_id_or_func=vbt.nb.nancumsum_nb) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-26)... def nancumsum_np(arr):
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-27)... return np.nancumsum(arr, axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-28)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-29)>>> log_returns.vbt.cumsum(jitted="np") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-30)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-31)2023-01-31 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-32)2023-02-01 00:00:00+00:00 0.024946
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-33)2023-02-02 00:00:00+00:00 0.014271
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-34)2023-02-03 00:00:00+00:00 0.013310
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-35)2023-02-04 00:00:00+00:00 0.008288
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-36)2023-02-05 00:00:00+00:00 -0.007967
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-37)2023-02-06 00:00:00+00:00 -0.010087
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-7-38)Freq: D, Name: Close, dtype: float64
 
[/code]

 1. 2. 3. 4. 


# Caching[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#caching "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Caching has been reimplemented from the ground up, and now it's being managed by a central registry. This allows for tracking useful statistics of all cacheable parts of VBT, such as to display the total cached size in MB. Full control and transparency ![🪟](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1fa9f.svg)

Get the cache statistics after computing the statistics of a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-2)>>> pf = vbt.PF.from_random_signals(data.close, n=5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-3)>>> _ = pf.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-4)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-5)>>> pf.get_ca_setup().get_status_overview(
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-6)... filter_func=lambda setup: setup.caching_enabled,
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-7)... include=["hits", "misses", "total_size"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-9) hits misses total_size
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-10)object 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-11)portfolio:0.drawdowns 0 1 70.9 kB
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-12)portfolio:0.exit_trades 0 1 70.5 kB
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-13)portfolio:0.filled_close 6 1 24.3 kB
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-14)portfolio:0.init_cash 3 1 32 Bytes
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-15)portfolio:0.init_position 0 1 32 Bytes
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-16)portfolio:0.init_position_value 0 1 32 Bytes
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-17)portfolio:0.init_value 5 1 32 Bytes
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-18)portfolio:0.input_value 1 1 32 Bytes
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-19)portfolio:0.orders 9 1 69.7 kB
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-20)portfolio:0.total_profit 1 1 32 Bytes
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-8-21)portfolio:0.trades 0 1 70.5 kB
 
[/code]


# Hyperfast rolling metrics[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#hyperfast-rolling-metrics "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Rolling metrics based on returns were optimized for best performance - up to 1000x speedup!

Benchmark the rolling Sortino ratio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-1)>>> import quantstats as qs
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-3)>>> index = vbt.date_range("2020", periods=100000, freq="1min")
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-4)>>> returns = pd.Series(np.random.normal(0, 0.001, size=len(index)), index=index)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-6)>>> %timeit qs.stats.rolling_sortino(returns, rolling_period=10) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-7)2.79 s ± 24.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-8)
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-9)>>> %timeit returns.vbt.returns.rolling_sortino_ratio(window=10) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/performance/#__codelineno-9-10)8.12 ms ± 199 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

 1. 2. 


# And many more...[¶](https://vectorbt.pro/pvt_7a467f6b/features/performance/#and-many-more "Permanent link")

 * Expect more killer features to be added on a weekly basis!

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/features/performance.py.txt)