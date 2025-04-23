# Multithreading[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#multithreading "Permanent link")

Having a purely Numba-compiled indicator function has one major benefit - multithreading support. So, what exactly is multithreading and how it compares to multiprocessing?

Multithreading means having the same process run multiple threads **concurrently** , sharing the same CPU and memory. However, because of the [GIL](https://realpython.com/python-gil/) in Python, not all tasks can be executed faster by using multithreading. In fact, GIL allows only one thread to execute at a time even in a multi-threaded architecture with more than one CPU core, meaning only when one thread is idly waiting, another thread can start executing code.

To circumvent this limitation of the GIL, the most popular way is to use a multiprocessing approach where you use multiple processes instead of threads. Each Python process gets its own Python interpreter and memory space. And here's the catch: you cannot share the same array between two processes (you can, but it's tricky), and processes are (much) heavier than threads. For instance, vectorbt takes 2-3 seconds to be imported - are you willing to spend this much time in every single process? Such waiting time feels like eternity compared to our superfast streaming function.

But don't lose your faith just yet. Fortunately, compiled code called by the Python interpreter can release the GIL and execute on multiple threads at the same time. Libraries like NumPy and Pandas release the GIL automatically, while Numba requires the `nogil=True` flag to be set (as we luckily did above).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-1)>>> SuperTrend = vbt.IF(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-2)... class_name='SuperTrend',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-3)... short_name='st',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-4)... input_names=['high', 'low', 'close'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-5)... param_names=['period', 'multiplier'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-6)... output_names=['supert', 'superd', 'superl', 'supers']
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-7)... ).with_apply_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-8)... superfast_supertrend_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-9)... takes_1d=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-10)... period=7, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-11)... multiplier=3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-0-12)... )
 
[/code]

The indicator factory recognizes that `superfast_supertrend_nb` is Numba-compiled and dynamically generates another Numba-compiled function that selects one parameter combination at each time step and calls our `superfast_supertrend_nb`. By default, it also forces this selection function to release the GIL.

Let's benchmark this indicator on 336 parameter combinations per symbol:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-2)>>> SuperTrend.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-3)... high, low, close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-4)... period=periods, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-5)... multiplier=multipliers,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-6)... param_product=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-7)... execute_kwargs=dict(show_progress=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-1-9)269 ms ± 72.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

We see that each iteration takes around 270 / 336 / 2 = 400 microseconds, which is 2x slower than `superfast_supertrend_nb` itself. This is due to the fact that the indicator also has to concatenate all the generated columns of each output into a single array - apparently a costly operation.

Let's repeat the same test but now with multithreading enabled:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-2)>>> SuperTrend.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-3)... high, low, close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-4)... period=periods, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-5)... multiplier=multipliers,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-6)... param_product=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-7)... execute_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-8)... engine='dask', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-9)... chunk_len='auto', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-10)... show_progress=False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/multithreading/#__codelineno-2-13)147 ms ± 10.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

 1. 2. 3. 

What the command did is the following: it divided all the parameter combinations into chunks. Each chunk has the same number of combinations as we have cores, such that each of the combinations in that chunk can be executed concurrently. The chunks themselves are executed sequentially though. This way, we are always running at most `n` combinations and do not create more threads than needed. 

As we can see, this strategy has paid out with a 2x speedup.

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/superfast-supertrend/multithreading.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/SuperTrend.ipynb)