# Benchmarking[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#benchmarking "Permanent link")

To measure execution time of a code block by running it **only once** , use [Timer](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.Timer).

Measure execution time by running once
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-0-1)with vbt.Timer() as timer:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-0-2) my_pipeline()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-0-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-0-4)print(timer.elapsed())
 
[/code]

Note

The code block may depend on Numba functions that need to be compiled first. To exclude any compilation time from the estimate (recommended since a compilation may take up to a minute while the code block may execute in milliseconds), dry-run the code block.


* * *

+


* * *

Another way is to repeatedly run a code block and assess some statistic, such as the shortest average execution time, which is easily doable with the help of the [timeit](https://docs.python.org/3/library/timeit.html) module and the corresponding vectorbtpro's function that returns the number in a human-readable format. The advantage of this approach is that any compilation overhead is effectively ignored.

Measure execution time by running multiple times
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-1-1)print(vbt.timeit(my_pipeline))
 
[/code]


* * *

+


* * *

There's also a profiling tool for peak memory usage - [MemTracer](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.MemTracer), which helps to determine an approximate size of all objects that are generated when running a code block.

Measure peak memory usage by running once
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-2-1)with vbt.MemTracer() as tracer:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-2-2) my_pipeline()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-2-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/benchmarking/#__codelineno-2-4)print(tracer.peak_usage())
 
[/code]