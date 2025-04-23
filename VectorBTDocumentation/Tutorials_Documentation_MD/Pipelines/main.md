# Pipelines[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#pipelines "Permanent link")

Most of the time, we not only care about the performance of all the deployed indicators, but about the health of the entire backtesting pipeline in general - having an ultrafast indicator brings nothing if the main bottleneck is the portfolio simulator itself.

Let's build a simple pipeline that takes the input data and strategy parameters, and returns the Sharpe ratio per symbol and parameter combination:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-1)>>> def pipeline(data, period=7, multiplier=3):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-2)... high = data.get('High')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-3)... low = data.get('Low')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-4)... close = data.get('Close')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-5)... st = SuperTrend.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-6)... high, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-7)... low, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-8)... close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-9)... period=period, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-10)... multiplier=multiplier
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-12)... entries = (~st.superl.isnull()).vbt.signals.fshift()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-13)... exits = (~st.supers.isnull()).vbt.signals.fshift()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-14)... pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-15)... close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-16)... entries=entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-17)... exits=exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-18)... fees=0.001,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-19)... save_returns=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-20)... max_order_records=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-21)... freq='1h'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-23)... return pf.sharpe_ratio 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-24)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-25)>>> pipeline(data)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-26)st_period st_multiplier symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-27)7 3 BTCUSDT 1.521221
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-28) ETHUSDT 2.258501
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-29)Name: sharpe_ratio, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-31)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-32)>>> pipeline(data)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-0-33)32.5 ms ± 1.12 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
 
[/code]

 1. 2. 3. 

The indicator takes roughly 3 milliseconds for both columns, or 10% of the total execution time. The other 90% are spent to select the data, create `entries` and `exits`, perform the simulation, and calculate the Sharpe values. 

As you might have guessed, the simulation is the place where the most of the processing takes place: vectorbt has to update the cash balance, group value, and other metrics at every single time step to keep the trading environment intact. Finally, after finishing the simulation, it has to go over the data one to multiple times to reconstruct the attributes required for computing various statistics, usually including the cash flow, cash, asset flow, assets, asset value, portfolio value, and finally, returns. If we were to populate and keep all of this information during the simulation, we would run out of memory. But luckily for us, we can avoid the reconstruction phase entirely by pre-computing the returns, as we did above.

Now, guess what will be the execution time when running the same pipeline 336 times? You say 10 seconds? 
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-1-1)>>> op_tree = (product, periods, multipliers)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-1-2)>>> period_product, multiplier_product = vbt.generate_param_combs(op_tree) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-1-3)>>> period_product = np.asarray(period_product)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-1-4)>>> multiplier_product = np.asarray(multiplier_product)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-1-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-1-6)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-1-7)>>> pipeline(data, period_product, multiplier_product)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-1-8)2.38 s ± 142 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

 1. 

Only 1/5 of that. This is because vectorbt knows how to process wide arrays efficiently. But as soon as you start testing thousands of parameter combinations, the performance will begin to suffer. Generally, stacking a lot of columns at once consumes much more memory than doing it in a loop, and as soon as you have used all the available memory, depending upon the system, the process switches to the swap memory, which is much slower to access than RAM. How do we tackle this?


# Chunked pipeline[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#chunked-pipeline "Permanent link")

To avoid memory problems, let's make our pipeline chunkable. Chunking in vectorbt allows for splitting arguments (in our case, parameter combinations) such that only one bunch of the argument values is passed to the pipeline function at a time. This is done using the [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked) decorator:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-1)>>> chunked_pipeline = vbt.chunked(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-2)... size=vbt.LenSizer(arg_query='period', single_type=int), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-3)... arg_take_spec=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-4)... data=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-5)... period=vbt.ChunkSlicer(), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-6)... multiplier=vbt.ChunkSlicer()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-7)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-8)... merge_func=lambda x: pd.concat(x).sort_index() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-2-9)... )(pipeline)
 
[/code]

 1. 2. 3. 4. 5. 

The returned `chunked_pipeline` function has the signature (i.e., accepted arguments and the order they come in) identical to that of the `pipeline`, but now it can internally split all arguments thanks to the chunking specification that we provided. It measures the number of elements in `period` and, by default, generates the same number of chunks as we have cores in our system. Each chunk contains the same input data passed as `data` (only a reference, not a copy!), and a slice of the values in `period` and `multiplier`. After all chunks have been processed, it merges their results using Pandas, such that we get the same result as if we had processed all parameter combinations at once. Incredible, right?

Let's test the chunked pipeline on one combination:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-3-1)st_period st_multiplier symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-3-2)7 3 BTCUSDT 1.521221
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-3-3) ETHUSDT 2.258501
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-3-4)Name: sharpe_ratio, dtype: float64
 
[/code]

We're getting the same results as by using `pipeline`, which isn't much surprising. How about multiple combinations? Let's execute `chunked_pipeline` on 4 combinations split into 2 chunks while also showing the progress bar:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-4-1)>>> chunked_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-4-2)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-4-3)... period_product[:4], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-4-4)... multiplier_product[:4],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-4-5)... _n_chunks=2, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-4-6)... )
 
[/code]

 1. 

Chunk 2/2
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-1)st_period st_multiplier symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-2)4 2.0 BTCUSDT 0.451699
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-3) ETHUSDT 1.391032
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-4) 2.1 BTCUSDT 0.495387
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-5) ETHUSDT 1.134741
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-6) 2.2 BTCUSDT 0.985946
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-7) ETHUSDT 0.955616
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-8) 2.3 BTCUSDT 1.193179
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-9) ETHUSDT 1.307505
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-5-10)Name: sharpe_ratio, dtype: float64
 
[/code]

How do we know whether the passed arguments were split correctly?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-1)>>> chunk_meta, tasks = chunked_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-2)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-3)... period_product[:4], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-4)... multiplier_product[:4],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-5)... _n_chunks=2,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-6)... _return_raw_chunks=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-9)>>> chunk_meta 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-10)[ChunkMeta(uuid='0882b000-52ab-4694-bb7c-341a9370937b', idx=0, start=0, end=2, indices=None),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-11) ChunkMeta(uuid='1d5a74d9-d517-437d-a20a-4580f601a280', idx=1, start=2, end=4, indices=None)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-13)>>> list(tasks) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-14)[(<function __main__.pipeline(data, period=7, multiplier=3)>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-15) (<vectorbtpro.data.custom.hdf.HDFData at 0x7f7b30509a60>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-16) array([4, 4]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-17) array([2., 2.1])),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-18) {}),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-19) (<function __main__.pipeline(data, period=7, multiplier=3)>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-20) (<vectorbtpro.data.custom.hdf.HDFData at 0x7f7b30509a60>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-21) array([4, 4]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-22) array([2.2, 2.3])),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-6-23) {})]
 
[/code]

 1. 2. 

The first chunk contains the combinations `(4, 2.0)` and `(4, 2.1)`, the second chunk contains the combinations `(4, 2.2)` and `(4, 2.3)`.

And here's how long does it take to run all combinations of parameters:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-7-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-7-2)>>> chunked_pipeline(data, period_product, multiplier_product)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-7-3)2.33 s ± 50.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

We don't observe any increase in performance because there is no multiprocessing or multithreading taking place, but splitting into chunks is all about memory and keeping its health at maximum. But don't overdo! Looping over all parameter combinations and processing only one combination at a time is much slower because now vectorbt can't take advantage of multidimensionality:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-8-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-8-2)>>> chunked_pipeline(data, period_product, multiplier_product, _chunk_len=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-8-3)11.4 s ± 965 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

What's better? Something in-between. Usually, the default values are good enough.


# Numba pipeline[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#numba-pipeline "Permanent link")

Wouldn't it be great if we could parallelize our pipeline the same way as we did with the indicator? Unfortunately, our Python code wouldn't make the concurrency possible since it holds the GIL. But remember how Numba can release the GIL to enable multithreading? If only we could write the entire pipeline in Numba... Let's do this!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-2)... def pipeline_nb(high, low, close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-3)... periods=np.asarray([7]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-4)... multipliers=np.asarray([3]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-5)... ann_factor=365):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-6)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-7)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-8)... sharpe = np.empty(periods.size * close.shape[1], dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-9)... long_entries = np.empty(close.shape, dtype=np.bool_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-10)... long_exits = np.empty(close.shape, dtype=np.bool_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-11)... group_lens = np.full(close.shape[1], 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-12)... init_cash = 100.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-13)... fees = 0.001
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-14)... k = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-15)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-16)... for i in range(periods.size):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-17)... for col in range(close.shape[1]):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-18)... _, _, superl, supers = superfast_supertrend_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-19)... high[:, col], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-20)... low[:, col], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-21)... close[:, col], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-22)... periods[i], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-23)... multipliers[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-25)... long_entries[:, col] = vbt.nb.fshift_1d_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-26)... ~np.isnan(superl), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-27)... fill_value=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-28)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-29)... long_exits[:, col] = vbt.nb.fshift_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-30)... ~np.isnan(supers), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-31)... fill_value=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-32)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-33)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-34)... sim_out = vbt.pf_nb.from_signals_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-35)... target_shape=close.shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-36)... group_lens=group_lens,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-37)... init_cash=init_cash,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-38)... high=high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-39)... low=low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-40)... close=close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-41)... long_entries=long_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-42)... long_exits=long_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-43)... fees=fees,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-44)... save_returns=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-45)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-46)... returns = sim_out.in_outputs.returns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-47)... _sharpe = vbt.ret_nb.sharpe_ratio_nb(returns, ann_factor, ddof=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-48)... sharpe[k:k + close.shape[1]] = _sharpe 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-49)... k += close.shape[1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-50)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-9-51)... return sharpe
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

Running this pipeline on one parameter combination yields two (already familiar to us) Sharpe values, one per column in `high`, `low`, and `close`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-1)>>> ann_factor = vbt.pd_acc.returns.get_ann_factor(freq='1h') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-2)>>> pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-3)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-4)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-5)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-6)... ann_factor=ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-8)array([1.521221, 2.25850084])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-10)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-11)>>> pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-12)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-13)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-14)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-15)... ann_factor=ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-10-17)3.13 ms ± 544 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 
[/code]

 1. 

One iteration of `pipeline_nb` is already 10x faster than one iteration of `pipeline`.

The next step is creation of a chunked pipeline. Since the returned values aren't Pandas Series anymore, we can't simply join them and hope for the best: we need to manually concatenate them and build a multi-level index for later analysis.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-1)>>> def merge_func(arrs, ann_args, input_columns): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-2)... arr = np.concatenate(arrs)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-3)... param_index = vbt.stack_indexes(( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-4)... pd.Index(ann_args['periods']['value'], name='st_period'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-5)... pd.Index(ann_args['multipliers']['value'], name='st_multiplier')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-6)... ))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-7)... index = vbt.combine_indexes(( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-8)... param_index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-9)... input_columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-10)... ))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-11)... return pd.Series(arr, index=index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-13)>>> nb_chunked = vbt.chunked(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-14)... size=vbt.ArraySizer(arg_query='periods', axis=0), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-15)... arg_take_spec=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-16)... high=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-17)... low=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-18)... close=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-19)... periods=vbt.ArraySlicer(axis=0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-20)... multipliers=vbt.ArraySlicer(axis=0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-21)... ann_factor=None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-22)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-23)... merge_func=merge_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-24)... merge_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-25)... ann_args=vbt.Rep("ann_args")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-27)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-11-28)>>> chunked_pipeline_nb = nb_chunked(pipeline_nb)
 
[/code]

 1. 2. 3. 4. 5. 6. 

Let's test the pipeline on four parameter combinations as we did with the previous pipeline:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-1)>>> chunked_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-2)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-3)... low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-4)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-5)... periods=period_product[:4], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-6)... multipliers=multiplier_product[:4],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-7)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-8)... _n_chunks=2,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-9)... _merge_kwargs=dict(input_columns=close.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-12-10)... )
 
[/code]

Chunk 2/2
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-1)st_period st_multiplier symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-2)4 2.0 BTCUSDT 0.451699
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-3) ETHUSDT 1.391032
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-4) 2.1 BTCUSDT 0.495387
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-5) ETHUSDT 1.134741
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-6) 2.2 BTCUSDT 0.985946
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-7) ETHUSDT 0.955616
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-8) 2.3 BTCUSDT 1.193179
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-9) ETHUSDT 1.307505
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-13-10)dtype: float64
 
[/code]

We can instantly recognize the values produced by the previous pipeline. Moreover, if you run the code, you'll also notice that `chunked_pipeline_nb` has the average iteration speed of 50 per second as compared to 15 per second of `chunked_pipeline` \- a remarkable jump in performance. But that's not all: let's benchmark this pipeline without and with parallelization enabled.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-2)>>> chunked_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-3)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-4)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-5)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-6)... periods=period_product, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-7)... multipliers=multiplier_product,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-8)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-9)... _merge_kwargs=dict(input_columns=close.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-11)894 ms ± 14.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-13)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-14)>>> chunked_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-15)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-16)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-17)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-18)... periods=period_product, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-19)... multipliers=multiplier_product,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-20)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-21)... _execute_kwargs=dict(engine="dask"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-22)... _merge_kwargs=dict(input_columns=close.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-23)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-14-24)217 ms ± 4.67 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

We just processed 12 million data points in 217 milliseconds, and that's in Python! ![😎](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f60e.svg)


# Contextualized pipeline[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#contextualized-pipeline "Permanent link")

But it's not always about performance. Consider a scenario where we need to know the Sharpe ratio at each single time step to drive our trading decisions. This isn't possible using the pipelines we wrote above because we have introduced a path dependency: the current Sharpe now directly depends upon the previous Sharpe. 

Exactly for such situations vectorbt designed a concept of a custom order function - a regular callback that can be executed at any time during the simulation. It takes a surrounding simulation context such as the running cash balance and makes a decision on whether to issue an order or not. Order functions are not the only callback inhabitants in vectorbt: there is an entire zoo of callbacks that can be called at specific checkpoints during the runtime. Using such callbacks is usually associated with a noticeable performance hit (still very fast though), but they make the event-driven backtesting possible in a package otherwise focused on manipulating arrays.

To make the simulation as fast as possible, we'll calculate both the SuperTrend and the Sharpe ratio in a single pass. This way, not only we will know those two values at each time step, but we will also retain the full control over their calculation.


# Streaming Sharpe[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#streaming-sharpe "Permanent link")

We've already designed a streaming SuperTrend indicator, but what about Sharpe? Making it a one-pass algorithm requires implementing an accumulator, which is a fairly easy task because the Sharpe ratio essentially depends on the rolling mean and the standard deviation. Thus, we'll make an accumulator by simply combining other two accumulators: [rolling_mean_acc_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.rolling_mean_acc_nb) and [rolling_std_acc_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.rolling_std_acc_nb). If you followed me through the implementation of the streaming SuperTrend, you would have no difficulties understanding the following code:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-1)>>> class RollSharpeAIS(tp.NamedTuple):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-2)... i: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-3)... ret: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-4)... pre_window_ret: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-5)... cumsum: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-6)... cumsum_sq: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-7)... nancnt: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-8)... window: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-9)... minp: tp.Optional[int]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-10)... ddof: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-11)... ann_factor: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-13)>>> class RollSharpeAOS(tp.NamedTuple):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-14)... cumsum: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-15)... cumsum_sq: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-16)... nancnt: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-17)... value: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-19)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-20)... def rolling_sharpe_acc_nb(in_state):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-21)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-22)... mean_in_state = vbt.nb.RollMeanAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-23)... i=in_state.i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-24)... value=in_state.ret,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-25)... pre_window_value=in_state.pre_window_ret,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-26)... cumsum=in_state.cumsum,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-27)... nancnt=in_state.nancnt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-28)... window=in_state.window,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-29)... minp=in_state.minp
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-30)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-31)... mean_out_state = vbt.nb.rolling_mean_acc_nb(mean_in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-32)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-33)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-34)... std_in_state = vbt.nb.RollStdAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-35)... i=in_state.i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-36)... value=in_state.ret,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-37)... pre_window_value=in_state.pre_window_ret,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-38)... cumsum=in_state.cumsum,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-39)... cumsum_sq=in_state.cumsum_sq,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-40)... nancnt=in_state.nancnt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-41)... window=in_state.window,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-42)... minp=in_state.minp,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-43)... ddof=in_state.ddof
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-44)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-45)... std_out_state = vbt.nb.rolling_std_acc_nb(std_in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-46)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-47)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-48)... mean = mean_out_state.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-49)... std = std_out_state.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-50)... if std == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-51)... sharpe = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-52)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-53)... sharpe = mean / std * np.sqrt(in_state.ann_factor)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-54)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-55)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-56)... return RollSharpeAOS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-57)... cumsum=std_out_state.cumsum,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-58)... cumsum_sq=std_out_state.cumsum_sq,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-59)... nancnt=std_out_state.nancnt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-60)... value=sharpe
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-15-61)... )
 
[/code]

 1. 2. 3. 4. 

To make sure that the calculation procedure above is correct, let's create a simple function `rolling_sharpe_ratio_nb` that computes the rolling Sharpe ratio using our accumulator, and compare its output to the output of another function with a totally different implementation - [ReturnsAccessor.rolling_sharpe_ratio](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor.rolling_sharpe_ratio).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-2)... def rolling_sharpe_ratio_nb(returns, window, minp=None, ddof=0, ann_factor=365):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-3)... if window is None:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-4)... window = returns.shape[0] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-5)... if minp is None:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-6)... minp = window 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-7)... out = np.empty(returns.shape, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-8)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-9)... if returns.shape[0] == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-10)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-11)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-12)... cumsum = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-13)... cumsum_sq = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-14)... nancnt = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-15)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-16)... for i in range(returns.shape[0]):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-17)... in_state = RollSharpeAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-18)... i=i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-19)... ret=returns[i],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-20)... pre_window_ret=returns[i - window] if i - window >= 0 else np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-21)... cumsum=cumsum,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-22)... cumsum_sq=cumsum_sq,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-23)... nancnt=nancnt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-24)... window=window,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-25)... minp=minp,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-26)... ddof=ddof,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-27)... ann_factor=ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-28)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-29)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-30)... out_state = rolling_sharpe_acc_nb(in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-31)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-32)... cumsum = out_state.cumsum
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-33)... cumsum_sq = out_state.cumsum_sq
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-34)... nancnt = out_state.nancnt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-35)... out[i] = out_state.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-36)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-37)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-38)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-39)>>> ann_factor = vbt.pd_acc.returns.get_ann_factor(freq='1h') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-40)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-41)>>> returns = close['BTCUSDT'].vbt.to_returns() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-42)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-43)>>> np.testing.assert_allclose(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-44)... rolling_sharpe_ratio_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-45)... returns=returns.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-46)... window=10, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-47)... ddof=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-48)... ann_factor=ann_factor),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-49)... returns.vbt.returns(freq='1h').rolling_sharpe_ratio(10).values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-16-50)... )
 
[/code]

 1. 2. 3. 4. 5. 

We're good - both functions return identical arrays!


# Callbacks[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#callbacks "Permanent link")

In a contextualized simulation using [from_order_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/from_order_func/#vectorbtpro.portfolio.nb.from_order_func.from_order_func_nb), there is a number of callbacks we can use to define our logic in. The simulator takes a shape `target_shape` and iterates over columns and rows of this shape in a specific fashion. You can imagine this shape being a two-dimensional array where columns are assets (denoted as `col`) and rows are time steps (denoted as `i`). For each element of this shape, we call an order function. This is similar to how we trade in the real world: 1 trade on BTC and 0 trades on ETH yesterday, 0 trades on BTC and 0 trades on ETH today, etc.

Date | BTCUSDT (`col=0`) | ETHUSDT (`col=1`) 
---|---|--- 
2020-01-01 (`i=0`) | 1 | 0 
2020-01-02 (`i=1`) | 0 | 1 
... | ... | ... 
today (`i=n`) | 1 | 1 
 
Since the simulator suddenly works on multiple columns, the information we need to manage to run the streaming SuperTrend such as `cumsum` and `cumsum_sq` should be defined per column. This means we're scratching scalars in favor of one-dimensional arrays. Why arrays and not lists, dicts, or tuples? Because arrays are faster than lists and dicts, can be modified in contrast to tuples, and they are native data structures in Numba, which makes them more than suited to hold and modify data. 

In traditional backtesting, we usually store our own variables such as arrays on the instance we're working on. But during simulation with vectorbt, we don't have classes and instances (well, Numba has a concept of jitted classes, but they are too heavy-weight): the only way to pass any information around is by letting a callback return them as a tuple to be consumed by other callbacks down the execution stack. As you can imagine, managing large tuples is not quite intuitive. The best way is to create a named tuple, which acts as a container (also called "memory") and is perfectly acceptable by Numba. We can then access any array conveniently by its name.

So, where do we define this memory? Whenever the simulator starts a new simulation, it first calls the `pre_sim_func_nb` callback, which is just a regular pre-processing function called prior to the main simulation procedure. Whatever this function returns gets passed to other callbacks. Sounds like a perfect place, right?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-1)>>> class Memory(tp.NamedTuple): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-2)... nobs: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-3)... old_wt: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-4)... weighted_avg: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-5)... prev_upper: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-6)... prev_lower: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-7)... prev_dir_: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-8)... cumsum: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-9)... cumsum_sq: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-10)... nancnt: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-11)... was_entry: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-12)... was_exit: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-14)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-15)... def pre_sim_func_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-16)... memory = Memory( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-17)... nobs=np.full(c.target_shape[1], 0, dtype=int_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-18)... old_wt=np.full(c.target_shape[1], 1., dtype=float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-19)... weighted_avg=np.full(c.target_shape[1], np.nan, dtype=float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-20)... prev_upper=np.full(c.target_shape[1], np.nan, dtype=float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-21)... prev_lower=np.full(c.target_shape[1], np.nan, dtype=float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-22)... prev_dir_=np.full(c.target_shape[1], np.nan, dtype=float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-23)... cumsum=np.full(c.target_shape[1], 0., dtype=float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-24)... cumsum_sq=np.full(c.target_shape[1], 0., dtype=float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-25)... nancnt=np.full(c.target_shape[1], 0, dtype=int_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-26)... was_entry=np.full(c.target_shape[1], False, dtype=np.bool_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-27)... was_exit=np.full(c.target_shape[1], False, dtype=np.bool_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-28)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-17-29)... return (memory,)
 
[/code]

 1. 2. 

The memory returned by the simulation pre-processing function gets automatically prepended to the arguments of every other callback, unless some callbacks higher in the call hierarchy decide not to do so and limit exposure to the memory. Let's write the main part of our simulation - the order function, which takes the surrounding context, the memory, and the parameter values passed by the user, calculates the current SuperTrend values, and finally, uses them to decide whether to enter or exit the position. This signal gets stored in the memory and gets only executed at the next time step (this was our initial requirement):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-2)... def order_func_nb(c, memory, period, multiplier):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-3)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-4)... is_entry = memory.was_entry[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-5)... is_exit = memory.was_exit[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-6)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-7)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-8)... in_state = SuperTrendAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-9)... i=c.i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-10)... high=c.high[c.i, c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-11)... low=c.low[c.i, c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-12)... close=c.close[c.i, c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-13)... prev_close=c.close[c.i - 1, c.col] if c.i > 0 else np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-14)... prev_upper=memory.prev_upper[c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-15)... prev_lower=memory.prev_lower[c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-16)... prev_dir_=memory.prev_dir_[c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-17)... nobs=memory.nobs[c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-18)... weighted_avg=memory.weighted_avg[c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-19)... old_wt=memory.old_wt[c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-20)... period=period,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-21)... multiplier=multiplier
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-23)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-24)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-25)... out_state = superfast_supertrend_acc_nb(in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-26)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-27)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-28)... memory.nobs[c.col] = out_state.nobs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-29)... memory.weighted_avg[c.col] = out_state.weighted_avg
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-30)... memory.old_wt[c.col] = out_state.old_wt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-31)... memory.prev_upper[c.col] = out_state.upper
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-32)... memory.prev_lower[c.col] = out_state.lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-33)... memory.prev_dir_[c.col] = out_state.dir_
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-34)... memory.was_entry[c.col] = not np.isnan(out_state.long)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-35)... memory.was_exit[c.col] = not np.isnan(out_state.short)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-36)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-37)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-38)... in_position = c.position_now > 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-39)... if is_entry and not in_position:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-40)... size = np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-41)... elif is_exit and in_position:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-42)... size = -np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-43)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-44)... size = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-45)... return vbt.pf_nb.order_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-46)... size=size, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-47)... direction=vbt.pf_enums.Direction.LongOnly,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-48)... fees=0.001
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-18-49)... )
 
[/code]

 1. 2. 3. 4. 5. 

Hint

If the execution time has to be shifted by more than one tick, consider creating a full array for `long` and `short` values returned by `superfast_supertrend_acc_nb` and access any previous element in those arrays to generate a signal.

If an order decision (such as `is_entry`) is based on an information from an array (such as `memory.was_entry`), temporarily store the element in a const variable - Numba loves it.

The last callback is the segment post-processing function. A segment is simply a group of columns at a single time step, mostly for managing orders of assets that share the same capital or are connected by any other means. Since our portfolio isn't grouped, every column (`BTCUSDT` and `ETHUSDT`) has its own group, and thus each segment contains only one column. After all columns in a segment have been processed, the simulator updates the current group value and the return. The latter is used by our callback to calculate the Sharpe ratio:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-2)... def post_segment_func_nb(c, memory, ann_factor):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-3)... for col in range(c.from_col, c.to_col): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-4)... in_state = RollSharpeAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-5)... i=c.i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-6)... ret=c.last_return[col], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-7)... pre_window_ret=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-8)... cumsum=memory.cumsum[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-9)... cumsum_sq=memory.cumsum_sq[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-10)... nancnt=memory.nancnt[col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-11)... window=c.i + 1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-12)... minp=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-13)... ddof=1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-14)... ann_factor=ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-16)... out_state = rolling_sharpe_acc_nb(in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-17)... memory.cumsum[col] = out_state.cumsum
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-18)... memory.cumsum_sq[col] = out_state.cumsum_sq
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-19)... memory.nancnt[col] = out_state.nancnt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-19-20)... c.in_outputs.sharpe[col] = out_state.value 
 
[/code]

 1. 2. 3. 4. 

Here's a short illustration of what calls what:

(Reload the page if the diagram doesn't show up)

Info

The operation flow within the rectangle is executed at each time step.


# Pipeline[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#pipeline "Permanent link")

Let's put all the parts together and define our super-flexible pipeline:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-1)>>> class InOutputs(tp.NamedTuple): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-2)... sharpe: tp.Array1d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-4)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-5)... def ctx_pipeline_nb(high, low, close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-6)... periods=np.asarray([7]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-7)... multipliers=np.asarray([3]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-8)... ann_factor=365):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-9)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-10)... in_outputs = InOutputs(sharpe=np.empty(close.shape[1], dtype=float_))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-11)... sharpe = np.empty(periods.size * close.shape[1], dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-12)... group_lens = np.full(close.shape[1], 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-13)... init_cash = 100.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-14)... k = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-15)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-16)... for i in range(periods.size):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-17)... sim_out = vbt.pf_nb.from_order_func_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-18)... target_shape=close.shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-19)... group_lens=group_lens,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-20)... cash_sharing=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-21)... init_cash=init_cash,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-22)... pre_sim_func_nb=pre_sim_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-23)... order_func_nb=order_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-24)... order_args=(periods[i], multipliers[i]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-25)... post_segment_func_nb=post_segment_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-26)... post_segment_args=(ann_factor,),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-27)... high=high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-28)... low=low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-29)... close=close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-30)... in_outputs=in_outputs,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-31)... fill_pos_info=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-32)... max_order_records=0 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-33)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-34)... sharpe[k:k + close.shape[1]] = in_outputs.sharpe
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-35)... k += close.shape[1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-36)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-20-37)... return sharpe
 
[/code]

 1. 2. 3. 

The function has the same signature as `pipeline_nb`, and gladly, produces the same results!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-1)>>> ctx_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-2)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-3)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-4)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-5)... ann_factor=ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-7)array([1.521221, 2.25850084])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-9)>>> chunked_ctx_pipeline_nb = nb_chunked(ctx_pipeline_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-10)>>> chunked_ctx_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-11)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-12)... low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-13)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-14)... periods=period_product[:4], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-15)... multipliers=multiplier_product[:4],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-16)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-17)... _n_chunks=2,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-18)... _merge_kwargs=dict(input_columns=close.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-21-19)... )
 
[/code]

Chunk 2/2
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-1)st_period st_multiplier symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-2)4 2.0 BTCUSDT 0.451699
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-3) ETHUSDT 1.391032
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-4) 2.1 BTCUSDT 0.495387
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-5) ETHUSDT 1.134741
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-6) 2.2 BTCUSDT 0.985946
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-7) ETHUSDT 0.955616
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-8) 2.3 BTCUSDT 1.193179
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-9) ETHUSDT 1.307505
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-22-10)dtype: float64
 
[/code]

But in contrast to the previous pipeline, it's several times slower:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-2)>>> chunked_ctx_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-3)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-4)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-5)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-6)... periods=period_product, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-7)... multipliers=multiplier_product,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-8)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-9)... _merge_kwargs=dict(input_columns=close.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-11)6.4 s ± 45.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-13)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-14)>>> chunked_ctx_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-15)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-16)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-17)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-18)... periods=period_product, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-19)... multipliers=multiplier_product,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-20)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-21)... _execute_kwargs=dict(engine="dask"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-22)... _merge_kwargs=dict(input_columns=close.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-23)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-23-24)1.38 s ± 26.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

We traded in a bit of performance for full flexibility. But even in this constellation, event-driven backtesting of a **full grid** of parameter combinations with vectorbt is on par with a **single** SuperTrend calculation with Pandas ![😅](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f605.svg)


# Bonus: Own simulator[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#bonus-own-simulator "Permanent link")

If all you care is the best possible performance, you have a perfect streaming algorithm, and you know exactly how to calculate the metrics of interest on the fly, you probably can drop the simulation with the [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) class entirely and define the entire logic in a collection of primitive but purified and hyperfast Numba-compiled for-loops. In this case, you can directly use the vectorbt's core functionality for order execution:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-2)... def raw_pipeline_nb(high, low, close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-3)... periods=np.array([7]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-4)... multipliers=np.array([3]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-5)... ann_factor=365):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-6)... out = np.empty(periods.size * close.shape[1], dtype=float_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-7)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-8)... if close.shape[0] == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-9)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-10)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-11)... for k in range(len(periods)): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-12)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-13)... for col in range(close.shape[1]): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-14)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-15)... nobs = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-16)... old_wt = 1.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-17)... weighted_avg = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-18)... prev_close_ = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-19)... prev_upper = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-20)... prev_lower = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-21)... prev_dir_ = 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-22)... cumsum = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-23)... cumsum_sq = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-24)... nancnt = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-25)... was_entry = False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-26)... was_exit = False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-27)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-28)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-29)... init_cash = 100.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-30)... cash = init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-31)... position = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-32)... debt = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-33)... locked_cash = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-34)... free_cash = init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-35)... val_price = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-36)... value = init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-37)... prev_value = init_cash
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-38)... return_ = 0.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-39)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-40)... for i in range(close.shape[0]): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-41)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-42)... is_entry = was_entry
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-43)... is_exit = was_exit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-44)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-45)... st_in_state = SuperTrendAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-46)... i=i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-47)... high=high[i, col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-48)... low=low[i, col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-49)... close=close[i, col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-50)... prev_close=prev_close_,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-51)... prev_upper=prev_upper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-52)... prev_lower=prev_lower,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-53)... prev_dir_=prev_dir_,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-54)... nobs=nobs,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-55)... weighted_avg=weighted_avg,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-56)... old_wt=old_wt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-57)... period=periods[k],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-58)... multiplier=multipliers[k]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-59)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-60)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-61)... st_out_state = superfast_supertrend_acc_nb(st_in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-62)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-63)... nobs = st_out_state.nobs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-64)... weighted_avg = st_out_state.weighted_avg
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-65)... old_wt = st_out_state.old_wt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-66)... prev_close_ = close[i, col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-67)... prev_upper = st_out_state.upper
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-68)... prev_lower = st_out_state.lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-69)... prev_dir_ = st_out_state.dir_
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-70)... was_entry = not np.isnan(st_out_state.long)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-71)... was_exit = not np.isnan(st_out_state.short)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-72)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-73)... if is_entry and position == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-74)... size = np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-75)... elif is_exit and position > 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-76)... size = -np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-77)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-78)... size = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-79)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-80)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-81)... val_price = close[i, col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-82)... value = cash + position * val_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-83)... if not np.isnan(size):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-84)... exec_state = vbt.pf_enums.ExecState( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-85)... cash=cash,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-86)... position=position,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-87)... debt=debt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-88)... locked_cash=locked_cash,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-89)... free_cash=free_cash,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-90)... val_price=val_price,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-91)... value=value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-92)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-93)... price_area = vbt.pf_enums.PriceArea( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-94)... open=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-95)... high=high[i, col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-96)... low=low[i, col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-97)... close=close[i, col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-98)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-99)... order = vbt.pf_nb.order_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-100)... size=size, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-101)... direction=vbt.pf_enums.Direction.LongOnly,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-102)... fees=0.001
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-103)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-104)... _, new_exec_state = vbt.pf_nb.execute_order_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-105)... exec_state, order, price_area)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-106)... cash, position, debt, locked_cash, free_cash, val_price, value = new_exec_state
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-107)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-108)... value = cash + position * val_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-109)... return_ = vbt.ret_nb.get_return_nb(prev_value, value) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-110)... prev_value = value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-111)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-112)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-113)... sharpe_in_state = RollSharpeAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-114)... i=i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-115)... ret=return_,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-116)... pre_window_ret=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-117)... cumsum=cumsum,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-118)... cumsum_sq=cumsum_sq,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-119)... nancnt=nancnt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-120)... window=i + 1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-121)... minp=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-122)... ddof=1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-123)... ann_factor=ann_factor
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-124)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-125)... sharpe_out_state = rolling_sharpe_acc_nb(sharpe_in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-126)... cumsum = sharpe_out_state.cumsum
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-127)... cumsum_sq = sharpe_out_state.cumsum_sq
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-128)... nancnt = sharpe_out_state.nancnt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-129)... sharpe = sharpe_out_state.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-130)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-131)... out[k * close.shape[1] + col] = sharpe 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-132)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-24-133)... return out
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 

We just created our own simulator optimized for one particular task, and as you might have guessed, its speed is something unreal! ![🤯](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f92f.svg)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-1)>>> chunked_raw_pipeline_nb = nb_chunked(raw_pipeline_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-3)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-4)>>> chunked_raw_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-5)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-6)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-7)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-8)... periods=period_product, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-9)... multipliers=multiplier_product,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-10)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-11)... _merge_kwargs=dict(input_columns=close.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-13)225 ms ± 464 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-15)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-16)>>> chunked_raw_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-17)... high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-18)... low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-19)... close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-20)... periods=period_product, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-21)... multipliers=multiplier_product,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-22)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-23)... _execute_kwargs=dict(engine="dask"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-24)... _merge_kwargs=dict(input_columns=close.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-25-26)54 ms ± 1.13 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
 
[/code]

The reason why we see a 20x jump in performance compared to the latest pipeline even though it also processed the data in a streaming fashion, is because vectorbt has to prepare the contexts for all callbacks (even those that do nothing by default) and calculate all possible metrics that the user may need. Additionally, Numba hates complex relationships between objects that are shared or passed back and forth between multiple functions, so designing an efficient order function may not be the easiest challenge.

The best in the pipeline above is that it's very memory efficient. Let's roll 100 one-year periods over the entire period (1,752,000 input data points in total), backtest the full parameter grid on each one, and animate the whole thing as a GIF - in 15 seconds!

First, we need to split the entire period into sub-periods:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-1)>>> range_len = int(vbt.timedelta('365d') / vbt.timedelta('1h')) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-2)>>> splitter = vbt.Splitter.from_n_rolling( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-3)... high.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-4)... n=100, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-5)... length=range_len
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-8)>>> roll_high = splitter.take(high, into="reset_stacked") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-9)>>> roll_low = splitter.take(low, into="reset_stacked")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-10)>>> roll_close = splitter.take(close, into="reset_stacked")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-11)>>> roll_close.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-12)MultiIndex([( 0, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-13) ( 0, 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-14) ( 1, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-15) ( 1, 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-16) ( 2, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-17) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-18) (97, 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-19) (98, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-20) (98, 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-21) (99, 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-22) (99, 'ETHUSDT')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-23) names=['split', 'symbol'], length=200)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-24)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-25)>>> range_indexes = splitter.take(high.index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-26)>>> range_indexes[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-27)DatetimeIndex(['2020-01-01 00:00:00+00:00', '2020-01-01 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-28) '2020-01-01 02:00:00+00:00', '2020-01-01 03:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-29) '2020-01-01 04:00:00+00:00', '2020-01-01 05:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-30) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-31) '2020-12-31 12:00:00+00:00', '2020-12-31 13:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-32) '2020-12-31 14:00:00+00:00', '2020-12-31 15:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-33) '2020-12-31 16:00:00+00:00', '2020-12-31 17:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-26-34) dtype='datetime64[ns, UTC]', name='split_0', length=8760, freq=None)
 
[/code]

 1. 2. 3. 4. 

Next, generate the Sharpe values:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-1)>>> sharpe_ratios = chunked_raw_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-2)... roll_high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-3)... roll_low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-4)... roll_close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-5)... periods=period_product, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-6)... multipliers=multiplier_product,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-7)... ann_factor=ann_factor,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-8)... _execute_kwargs=dict(engine="dask"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-9)... _merge_kwargs=dict(input_columns=roll_close.columns) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-12)>>> sharpe_ratios
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-13)st_period st_multiplier split symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-14)4 2.0 0 BTCUSDT 1.751331
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-15) ETHUSDT 2.479750
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-16) 1 BTCUSDT 1.847095
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-17) ETHUSDT 2.736193
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-18) 2 BTCUSDT 1.739149
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-19) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-20)19 4.0 97 ETHUSDT 1.503001
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-21) 98 BTCUSDT 0.954932
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-22) ETHUSDT 1.204134
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-23) 99 BTCUSDT 0.818209
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-24) ETHUSDT 1.191223
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-27-25)Length: 67200, dtype: float64
 
[/code]

 1. 

67,200 backtests in one second ![💨](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4a8.svg)

When plotting a heatmap for each sub-period, we will use the Sharpe ratio of holding during that period as a mid-point of the colorscale, such that any blue-tinted point indicates that the parameter combination performed better than the market, and any red-tinted point indicates that the combination performed less well. For this, we need the Sharpe of holding:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-1)>>> pf_hold = vbt.Portfolio.from_holding(roll_close, freq='1h')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-2)>>> sharpe_ratios_hold = pf_hold.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-4)>>> sharpe_ratios_hold
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-5)split symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-6)0 BTCUSDT 2.229122
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-7) ETHUSDT 2.370132
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-8)1 BTCUSDT 2.298050
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-9) ETHUSDT 2.611722
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-10)2 BTCUSDT 2.351417
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-11) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-12)97 ETHUSDT 2.315863
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-13)98 BTCUSDT 1.124489
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-14) ETHUSDT 2.114297
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-15)99 BTCUSDT 0.975638
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-16) ETHUSDT 2.008839
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-28-17)Name: sharpe_ratio, Length: 200, dtype: float64
 
[/code]

Info

Notice how this multi-index lists no parameter combinations: the performance of holding isn't dependent on our indicator in any way.

Next, let's create a function that plots a sub-period:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-1)>>> def plot_subperiod_sharpe(index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-2)... sharpe_ratios, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-3)... sharpe_ratios_hold, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-4)... range_indexes, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-5)... symbol):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-6)... split = index[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-7)... sharpe_ratios = sharpe_ratios.xs( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-8)... symbol, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-9)... level='symbol', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-10)... drop_level=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-11)... sharpe_ratios = sharpe_ratios.xs( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-12)... split, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-13)... level='split', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-14)... drop_level=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-15)... start_date = range_indexes[split][0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-16)... end_date = range_indexes[split][-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-17)... return sharpe_ratios.vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-18)... x_level='st_period', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-19)... y_level='st_multiplier',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-20)... title="{} - {}".format( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-21)... start_date.strftime("%d %b, %Y %H:%M:%S"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-22)... end_date.strftime("%d %b, %Y %H:%M:%S")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-23)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-24)... trace_kwargs=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-25)... zmin=sharpe_ratios.min(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-26)... zmid=sharpe_ratios_hold[(split, symbol)],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-27)... zmax=sharpe_ratios.max(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-28)... colorscale='Spectral'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-29)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-29-30)... )
 
[/code]

 1. 2. 3. 4. 

Finally, use [save_animation](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#vectorbtpro.utils.image_.save_animation) to iterate over each split index, plot the heatmap of the sub-period, and append it as a PNG image to the GIF file:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-1)>>> fname = 'raw_pipeline.gif'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-2)>>> level_idx = sharpe_ratios.index.names.index('split')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-3)>>> split_indices = sharpe_ratios.index.levels[level_idx]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-5)>>> vbt.save_animation(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-6)... fname,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-7)... split_indices, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-8)... plot_subperiod_sharpe, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-9)... sharpe_ratios, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-10)... sharpe_ratios_hold,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-11)... range_indexes,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-12)... 'BTCUSDT',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-13)... delta=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-14)... fps=7,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-15)... writer_kwargs=dict(loop=0) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-30-16)... )
 
[/code]

 1. 2. 3. 4. 

Heatmap 100/100
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-31-1)>>> from IPython.display import Image, display
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-31-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-31-3)>>> with open(fname,'rb') as f:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#__codelineno-31-4)... display(Image(data=f.read(), format='png'))
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/raw_pipeline.light.gif#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/supertrend/raw_pipeline.dark.gif#only-dark)

Everything bluer than yellow beats the market. Just don't pick any value at the bottom ![😉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f609.svg)


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/pipelines/#summary "Permanent link")

We covered a lot of territories, let's digest what we have learned so far. 

A pipeline is a process that takes data and transforms it into insights. Such a process can be realized through a set of totally different pipeline designs, and you can always count on vectorbt during the development of each one. 

The easiest-to-use class of pipelines in vectorbt deploys two main components: indicator (such as `SuperTrend`) and simulator (such as [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals)); both can be developed, tweaked, and run independently of each other. This modular design yields the highest flexibility when signals and order execution aren't path-dependent. The only drawback is a high memory consumption, which can only be mitigated by chunking - splitting data and/or parameters into bunches that are processed sequentially (loop) or in parallel. Chunking also enables other two perks to utilize all cores: multiprocessing and multithreading. But the latter can only work when the entire pipeline is Numba-compiled and can release the GIL. Luckily for us, vectorbt offers a lot of utilities that can be used from within Numba, thus don't be afraid of writing the entire pipeline with Numba - it's easier than it seems!

But once signals become dependent upon trades made previously, both components must be merged into a monolithic workflow. Such workflows are possible using contextualized simulation, such as with [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func), which lets us inject our custom trading logic into the simulator itself using callbacks and contexts. This approach is very similar to the event-driven backtesting approach used by many backtesting frameworks, such as backtrader. The only difference lies in storing and managing information, which is done using named tuples and arrays, as opposed to classes and variables. Such pipelines offer the greatest flexibility but are considerably slower than the modular ones (although they would still leave most other backtesting software in the dust). To dramatically increase performance, you can switch to a lower-level API and implement the simulator by yourself. Sounds scary? It shouldn't because every simulator is just a bunch of regular for-loops and order management commands.

At the end of the day, you should pick the design that best suits your needs. There is no reason to spend days designing a perfect pipeline if all it does is save you 5 minutes, right? But at least you will learn how to design efficient algorithms in Python that can compete with top-notch algo-trading systems written in Java.

As always, happy coding ![❤](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2764.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/superfast-supertrend/pipelines.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/SuperTrend.ipynb)