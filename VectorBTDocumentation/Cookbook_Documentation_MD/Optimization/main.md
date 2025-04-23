# Optimization[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#optimization "Permanent link")

Optimization involves executing a function on a set of various configurations with an aim to optimize the performance of a strategy, and/or to optimize the CPU or RAM performance of a pipeline.

Question

Learn more in [Pairs trading tutorial](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/).


# Parameterization[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#parameterization "Permanent link")

The first and easiest approach revolves around testing a single parameter combination at a time, which utilizes as little RAM as possible but may take longer to run if the function isn't written in pure Numba and has a fixed overhead (e.g., conversion from Pandas to NumPy and back) that adds to the total execution time with each run. For this, create a pipeline function that runs a set of single values and decorate it with [`@vbt.parameterized`](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized). To test multiple parameters, wrap each parameter argument with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param). 

Example

See an example in [Parameterized decorator](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#parameterized-decorator).


# Decoration[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#decoration "Permanent link")

To parameterize any function, we have to decorate (or wrap) it with `@vbt.parameterized`. This will return a new function with the same name and arguments as the original one. The only difference: this new function will process passed arguments, build parameter combinations, call the original function on each parameter combination, and merge the results of all combinations.

Process only one parameter combination at a time
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-1)@vbt.parameterized
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-2)def my_pipeline(data, fast_window, slow_window): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-4) return result 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-6)results = my_pipeline( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-7) data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-8) vbt.Param(fast_windows), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-9) vbt.Param(slow_windows)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-0-10))
 
[/code]

 1. 2. 3. 4. 


* * *

+


* * *

To keep the original function separate from the decorated one, we can decorate it after it has been defined and give the decorated function another name.

Decorate a function later
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-1-1)def my_pipeline(data, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-1-2) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-1-3) return result
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-1-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-1-5)my_param_pipeline = vbt.parameterized(my_pipeline)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-1-6)results = my_param_pipeline(...)
 
[/code]


# Merging[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#merging "Permanent link")

The code above returns a list of results, one per parameter combination. To return the grid of parameter combinations as well, pass `return_param_index=True` to the decorator. Alternatively, let VBT merge the results into one or more Pandas objects and attach the grid to their index or columns by specifying the merging function (see [resolve_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.merging.resolve_merge_func)).

Various merging configurations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-1)@vbt.parameterized(return_param_index=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-2)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-4) return result
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-6)results, param_index = my_pipeline(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-8)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-10)@vbt.parameterized(merge_func="concat") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-11)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-12) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-13) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-15)sharpe_ratio = my_pipeline(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-17)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-18)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-19)@vbt.parameterized(merge_func="concat")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-20)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-21) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-22) return pf.sharpe_ratio, pf.win_rate
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-24)sharpe_ratio, win_rate = my_pipeline(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-25)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-26)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-27)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-28)@vbt.parameterized(merge_func="column_stack") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-29)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-30) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-31) return entries, exits
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-32)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-33)entries, exits = my_pipeline(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-34)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-35)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-36)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-37)@vbt.parameterized(merge_func="row_stack") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-38)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-39) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-40) return pf.value
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-41)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-42)value = my_pipeline(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-43)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-44)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-45)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-46)@vbt.parameterized(merge_func=("concat", "column_stack")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-47)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-48) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-49) return pf.sharpe_ratio, pf.value
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-50)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-51)sharpe_ratio, value = my_pipeline(...)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-52)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-53)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-54)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-55)def merge_func(results, param_index):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-56) return pd.Series(results, index=param_index)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-57)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-58)@vbt.parameterized(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-59) merge_func=merge_func, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-60) merge_kwargs=dict(param_index=vbt.Rep("param_index")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-61))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-62)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-63) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-64) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-65)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-2-66)sharpe_ratio = my_pipeline(...)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 


* * *

+


* * *

We can also use annotations to specify the merging function(s).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-1)@vbt.parameterized
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-2)def my_pipeline(...) -> "concat": 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-4) return result
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-6)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-8)@vbt.parameterized
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-9)def my_pipeline(...) -> ("concat", "column_stack"): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-10) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-11) return result1, result2
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-13)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-15)@vbt.parameterized
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-16)def my_pipeline(...) -> ( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-17) vbt.MergeFunc("concat", wrap=False), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-18) vbt.MergeFunc("column_stack", wrap=False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-19)):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-20) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-3-21) return result1, result2
 
[/code]

 1. 2. 3. 


# Generation[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#generation "Permanent link")

The grid of parameter combinations can be controlled by individual parameters. By default, vectorbtpro will build a Cartesian product of all parameters. To avoid building the product between some parameters, they can be assigned to the same product `level`. To filter out unwanted parameter configurations, specify the `condition` as a boolean expression where variables are parameter names. Such a condition will be evaluated on each parameter combination, and if it returns True, the combination will be kept. To change the appearance of a parameter in the parameter index, `keys` with human-readable strings can be provided. A parameter can also be hidden entirely by setting `hide=True`.

Various parameter configurations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-1)sma_crossover( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-2) data=data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-3) fast_window=vbt.Param(windows, condition="fast_window < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-4) slow_window=vbt.Param(windows),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-5))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-7)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-9)sma_crossover( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-10) data=vbt.Param(data),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-11) fast_window=vbt.Param(windows, condition="fast_window < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-12) slow_window=vbt.Param(windows),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-13))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-15)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-17)from itertools import combinations
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-18)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-19)fast_windows, slow_windows = zip(*combinations(windows, 2)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-20)sma_crossover(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-21) data=vbt.Param(data, level=0),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-22) fast_window=vbt.Param(fast_windows, level=1),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-23) slow_window=vbt.Param(slow_windows, level=1),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-24))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-25)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-26)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-27)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-28)bbands_indicator( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-29) data=data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-30) timeperiod=vbt.Param(timeperiods, level=0),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-31) upper_threshold=vbt.Param(thresholds, level=1, keys=pd.Index(thresholds, name="threshold")),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-32) lower_threshold=vbt.Param(thresholds, level=1, hide=True),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-33) _random_subset=1_000 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-4-34))
 
[/code]

 1. 2. 3. 4. 5. 

Example

See an example in [Conditional parameters](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#conditional-parameters).

Warning

Testing 6 parameters with only 10 values each would generate staggering 1 million parameter combinations, thus make sure that your grids are not too wide, otherwise the generation part alone will take forever to run. This warning doesn't apply when you use `random_subset` though; in this case, VBT won't build the full grid but select random combinations dynamically. See an example in [Lazy parameter grids](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#lazy-parameter-grids).


* * *

+


* * *

We can also use annotations to specify which arguments are parameters and their default configuration.

Calculate the SMA crossover for one parameter combination at a time
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-1)@vbt.parameterized
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-2)def sma_crossover(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-3) data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-4) fast_window: vbt.Param(condition="fast_window < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-5) slow_window: vbt.Param,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-6)) -> "column_stack":
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-7) fast_sma = data.run("talib:sma", fast_window, unpack=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-8) slow_sma = data.run("talib:sma", slow_window, unpack=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-9) upper_crossover = fast_sma.vbt.crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-10) lower_crossover = fast_sma.vbt.crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-11) signals = upper_crossover | lower_crossover
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-12) return signals
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-5-14)signals = sma_crossover(data, fast_windows, slow_windows)
 
[/code]


# Pre-generation[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#pre-generation "Permanent link")

To get the generated parameter combinations before (or without) calling the `@vbt.parameterized` decorator, we can pass the same parameters to [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params).

Pre-generate parameter combinations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-1)param_product, param_index = vbt.combine_params(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-2) dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-3) fast_window=vbt.Param(windows, condition="fast_window < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-4) slow_window=vbt.Param(windows),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-5) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-6))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-8)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-10)param_product = vbt.combine_params(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-11) dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-12) fast_window=vbt.Param(windows, condition="fast_window < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-13) slow_window=vbt.Param(windows),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-14) ),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-15) build_index=False 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-6-16))
 
[/code]

 1. 


# Execution[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#execution "Permanent link")

Each parameter combination involves one call of the pipeline function. To perform multiple calls in parallel, pass a dictionary named `execute_kwargs` with keyword arguments that should be forwarded to the function [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute), which takes care of chunking and executing the function calls.

Various execution configurations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-1)@vbt.parameterized 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-2)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-5)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-7)@vbt.parameterized(execute_kwargs=dict(chunk_len="auto", engine="threadpool")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-8)@njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-9)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-10) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-12)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-14)@vbt.parameterized(execute_kwargs=dict(n_chunks="auto", distribute="chunks", engine="pathos")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-15)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-16) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-18)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-19)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-20)@vbt.parameterized 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-21)@njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-22)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-23) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-24)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-25)my_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-26) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-27) _execute_kwargs=dict(chunk_len="auto", engine="threadpool")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-28))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-29)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-30)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-31)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-32)@vbt.parameterized(execute_kwargs=dict(show_progress=False)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-33)@njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-34)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-35) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-36)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-37)my_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-38) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-39) _execute_kwargs=dict(chunk_len="auto", engine="threadpool") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-40))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-41)my_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-42) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-43) _execute_kwargs=vbt.atomic_dict(chunk_len="auto", engine="threadpool") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-7-44))
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

Note

Threads are easier and faster to spawn than processes. Also, to execute a function in its own process, all the passed inputs and parameters need to be serialized and then deserialized, which takes time. Thus, multithreading is preferred, but it requires the function to release the GIL, which means either compiling the function with Numba and setting the `nogil` flag to True, or using exclusively NumPy.

If this isn't possible, use multiprocessing but make sure that the function either doesn't take large arrays, or that one parameter combination takes a considerable amount of time to run. Otherwise, you may find parallelization making the execution even slower.


* * *

+


* * *

To run a code before/after the entire processing or even before/after each individual chunk, [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) offers a number of callbacks.

Clear cache and collect garbage once in 3 chunks
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-1)def post_chunk_func(chunk_idx, flush_every):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-2) if (chunk_idx + 1) % flush_every == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-3) vbt.flush()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-5)@vbt.parameterized(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-6) post_chunk_func=post_chunk_func,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-7) post_chunk_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-8) chunk_idx=vbt.Rep("chunk_idx", eval_id="post_chunk_kwargs"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-9) flush_every=3
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-10) ),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-11) chunk_len=10 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-12)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-13)def my_pipeline(...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-8-14) ...
 
[/code]

 1. 

Tip

This works not only with `@vbt.parameterized` but also with other functions that use [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) with chunking!


# Total or partial?[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#total-or-partial "Permanent link")

Often, you should make a decision whether your pipeline should be parameterized totally or partially. Total parameterization means running the entire pipeline on each parameter combination, which is the easiest but also the most suitable approach if you have parameters being applied across multiple components of the pipeline, and/or if you want to trade in faster processing for lower memory consumption.

Parameterize an entire MA crossover pipeline
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-1)@vbt.parameterized(merge_func="concat") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-2)def ma_crossover_sharpe(data, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-3) fast_ma = data.run("vbt:ma", window=fast_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-4) slow_ma = data.run("vbt:ma", window=slow_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-5) entries = fast_ma.ma_crossed_above(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-6) exits = fast_ma.ma_crossed_below(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-7) pf = vbt.PF.from_signals(data, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-8) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-10)ma_crossover_sharpe(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-11) data, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-12) vbt.Param(fast_windows, condition="fast_window < slow_window"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-13) vbt.Param(slow_windows)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-9-14))
 
[/code]


* * *

+


* * *

Partial parameterization, on the other hand, is appropriate if you have only a few components in the pipeline where parameters are being applied, and if the remaining components of the pipeline know how to work with the results from the parameterized components. This may lead to a faster execution but also a higher memory consumption.

Parameterize only the signal part of a MA crossover pipeline
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-1)@vbt.parameterized(merge_func="column_stack") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-2)def ma_crossover_signals(data, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-3) fast_ma = data.run("vbt:ma", window=fast_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-4) slow_ma = data.run("vbt:ma", window=slow_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-5) entries = fast_ma.ma_crossed_above(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-6) exits = fast_ma.ma_crossed_below(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-7) return entries, exits
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-9)def ma_crossover_sharpe(data, fast_windows, slow_windows):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-10) entries, exits = ma_crossover_signals(data, fast_windows, slow_windows) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-11) pf = vbt.PF.from_signals(data, entries, exits) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-12) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-14)ma_crossover_sharpe(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-15) data, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-16) vbt.Param(fast_windows, condition="fast_window < slow_window"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-17) vbt.Param(slow_windows)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-10-18))
 
[/code]

 1. 2. 


# Flat or nested?[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#flat-or-nested "Permanent link")

Another decision you should make is whether to handle all parameters by one decorator (flat parameterization) or distribute parameters across multiple decorators to implement a specific parameter hierarchy (nested parameterization). The former approach should be used if you want to treat all of your parameters equally and put them into the same bucket for generation and processing. In this case, the order of the parameters in combinations is defined by the order the parameters are passed to the function. For example, while the values of the first parameter will be processed strictly from the first to the last value, the values of any other parameter will be rotated.

Process all parameters at the same time in a MA crossover pipeline
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-1)@vbt.parameterized(merge_func="concat") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-2)def ma_crossover_sharpe(data, symbol, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-3) symbol_data = data.select(symbol) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-4) fast_ma = symbol_data.run("vbt:ma", window=fast_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-5) slow_ma = symbol_data.run("vbt:ma", window=slow_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-6) entries = fast_ma.ma_crossed_above(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-7) exits = fast_ma.ma_crossed_below(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-8) pf = vbt.PF.from_signals(symbol_data, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-9) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-11)ma_crossover_sharpe(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-12) data, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-13) vbt.Param(data.symbols), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-14) vbt.Param(fast_windows, condition="fast_window < slow_window"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-15) vbt.Param(slow_windows),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-11-16))
 
[/code]

 1. 


* * *

+


* * *

The latter approach should be used if you want to define your own custom parameter hierarchy. For example, you may want to execute (such as parallelize) certain parameters differently, or you may want to reduce the number of invocations of certain parameters, or you may want to introduce special preprocessing and/or postprocessing to certain parameters.

First process symbols and then windows in a MA crossover pipeline
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-1)@vbt.parameterized(merge_func="concat", eval_id="inner") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-2)def symbol_ma_crossover_sharpe(symbol_data, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-3) fast_ma = symbol_data.run("vbt:ma", window=fast_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-4) slow_ma = symbol_data.run("vbt:ma", window=slow_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-5) entries = fast_ma.ma_crossed_above(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-6) exits = fast_ma.ma_crossed_below(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-7) pf = vbt.PF.from_signals(symbol_data, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-8) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-10)@vbt.parameterized(merge_func="concat", eval_id="outer") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-11)def ma_crossover_sharpe(data, symbol, fast_windows, slow_windows):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-12) symbol_data = data.select(symbol) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-13) return symbol_ma_crossover_sharpe(symbol_data, fast_windows, slow_windows) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-15)ma_crossover_sharpe( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-16) data, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-17) vbt.Param(data.symbols, eval_id="outer"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-18) vbt.Param(fast_windows, eval_id="inner", condition="fast_window < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-19) vbt.Param(slow_windows, eval_id="inner")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-20))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-21)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-22)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-24)@vbt.parameterized(merge_func="concat", eval_id="outer")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-25)@vbt.parameterized(merge_func="concat", eval_id="inner")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-26)def ma_crossover_sharpe(data, fast_window, slow_window): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-27) fast_ma = data.run("vbt:ma", window=fast_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-28) slow_ma = data.run("vbt:ma", window=slow_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-29) entries = fast_ma.ma_crossed_above(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-30) exits = fast_ma.ma_crossed_below(slow_ma)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-31) pf = vbt.PF.from_signals(data, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-32) return pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-33)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-34)ma_crossover_sharpe(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-35) vbt.Param(data, eval_id="outer"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-36) vbt.Param(fast_windows, eval_id="inner", condition="fast_window < slow_window"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-37) vbt.Param(slow_windows, eval_id="inner")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-12-38))
 
[/code]

 1. 2. 3. 4. 5. 6. 


# Skipping[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#skipping "Permanent link")

Parameter combinations can be skipped dynamically by returning [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.NoResult) instead of the actual result.

Skip the parameter combination if an error occurred
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-1)@vbt.parameterized
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-2)def my_pipeline(data, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-3) try:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-4) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-5) return result
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-6) except Exception:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-7) return vbt.NoResult
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-9)results = my_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-10) data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-11) vbt.Param(fast_windows),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-12) vbt.Param(slow_windows)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-13-13))
 
[/code]


# Hybrid (mono-chunks)[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#hybrid-mono-chunks "Permanent link")

The approach above calls the original function on each single parameter combination, which makes it slow when dealing with a large number of combinations, especially when each function call is associated with an overhead, such as when NumPy array gets converted to a Pandas object. Remember that 1 millisecond of an overhead translates into 17 minutes of additional execution time for one million of combinations. 

There's nothing (apart from parallelization) we can do to speed up functions that take only one combination at a time. But if the function can be adapted to accept multiple combinations, where each parameter argument becomes an array instead of a single value, we can instruct `@vbt.parameterized` to merge all combinations into chunks and call the function on each chunk. This way, we can reduce the number of function calls significantly.

Test a grid of parameters using mono-chunks
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-1)@vbt.parameterized(mono_n_chunks=?, mono_chunk_len=?, mono_chunk_meta=?) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-2)def my_pipeline(data, fast_windows, slow_windows): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-4) return result 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-6)results = my_pipeline( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-7) data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-8) vbt.Param(fast_windows),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-9) vbt.Param(slow_windows)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-10))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-12)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-14)@vbt.parameterized(mono_n_chunks="auto") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-15)...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-17)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-18)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-19)@vbt.parameterized(mono_chunk_len=100) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-14-20)...
 
[/code]

 1. 2. 3. 4. 5. 6. 


* * *

+


* * *

By default, parameter values are passed as lists to the original function. To pass them as arrays or in any other format instead, set a merging function `mono_merge_func` for each parameter.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-15-1)my_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-15-2) param_a=vbt.Param(param_a), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-15-3) param_b=vbt.Param(param_b, mono_reduce=True), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-15-4) param_c=vbt.Param(param_c, mono_merge_func="concat"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-15-5) param_d=vbt.Param(param_d, mono_merge_func="row_stack"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-15-6) param_e=vbt.Param(param_e, mono_merge_func="column_stack"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-15-7) param_f=vbt.Param(param_f, mono_merge_func=vbt.MergeFunc(...)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-15-8))
 
[/code]

 1. 2. 3. 4. 5. 6. 

Execution is done in the same way as in [Parameterization](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#parameterization) and chunks can be easily parallelized, just keep an eye on RAM consumption since now multiple parameter combinations are executed at the same time.

Example

See an example in [Mono-chunks](https://vectorbt.pro/pvt_7a467f6b/features/optimization/#mono-chunks).


# Chunking[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#chunking "Permanent link")

Chunking revolves around splitting a value (such as an array) of one or more arguments into many parts (or chunks), calling the function on each part, and then merging all parts together. This way, we can instruct VBT to process only a subset of data at a time, which is helpful in both reducing RAM consumption and increasing performance by utilizing parallelization. Chunking is also highly convenient: usually, you don't have to change your function in any way, and you'll get the same results regardless of whether chunking was enabled or disabled. To use chunking, create a pipeline function, decorate it with [`@vbt.chunked`](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked), and specify how exactly arguments should be chunked and results should be merged.

Example

See an example in [Chunking](https://vectorbt.pro/pvt_7a467f6b/features/performance/#chunking).


# Decoration[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#decoration_1 "Permanent link")

To make any function chunkable, we have to decorate (or wrap) it with `@vbt.chunked`. This will return a new function with the same name and arguments as the original one. The only difference: this new function will process passed arguments, chunk the arguments, call the original function on each chunk of the arguments, and merge the results of all chunks.

Process only a subset of values at a time
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-1)@vbt.chunked
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-2)def my_pipeline(data, fast_windows, slow_windows): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-4) return result 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-6)results = my_pipeline( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-7) data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-8) vbt.Chunked(fast_windows), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-9) vbt.Chunked(slow_windows)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-16-10))
 
[/code]

 1. 2. 3. 4. 


* * *

+


* * *

To keep the original function separate from the decorated one, we can decorate it after it has been defined and give the decorated function another name.

Decorate a function later
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-17-1)def my_pipeline(data, fast_windows, slow_windows):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-17-2) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-17-3) return result
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-17-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-17-5)my_chunked_pipeline = vbt.chunked(my_pipeline)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-17-6)results = my_chunked_pipeline(...)
 
[/code]


# Specification[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#specification "Permanent link")

To chunk an argument, we must provide a chunking specification for that argument. There are three main ways on how to provide such a specification.

Approach 1: Pass a dictionary `arg_take_spec` to the decorator. The most capable approach as it allows chunking of any nested objects of arbitrary depths, such as lists inside lists.

Specify chunking rules via arg_take_spec
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-1)@vbt.chunked(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-2) arg_take_spec=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-3) array1=vbt.ChunkedArray(axis=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-4) array2=vbt.ChunkedArray(axis=1),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-5) combine_func=vbt.NotChunked 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-6) ),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-7) size=vbt.ArraySizer(arg_query="array1", axis=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-8) merge_func="column_stack" 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-9))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-10)def combine_arrays(array1, array2, combine_func):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-11) return combine_func(array1, array2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-18-13)new_array = combine_arrays(array1, array2, np.add)
 
[/code]

 1. 2. 3. 4. 5. 


* * *

+


* * *

Approach 2: Annotate the function. The most convenient approach as you can specify chunking rules next to their respective arguments directly in the function definition.

Specify chunking rules via annotations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-1)@vbt.chunked
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-2)def combine_arrays(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-3) array1: vbt.ChunkedArray(axis=1) | vbt.ArraySizer(axis=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-4) array2: vbt.ChunkedArray(axis=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-5) combine_func
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-6)) -> "column_stack":
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-7) return combine_func(array1, array2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-19-9)new_array = combine_arrays(array1, array2, np.add)
 
[/code]

 1. 


* * *

+


* * *

Approach 3: Wrap argument values directly. Allows switching chunking rules on the fly.

Specify chunking rules via argument values
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-1)@vbt.chunked
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-2)def combine_arrays(array1, array2, combine_func):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-3) return combine_func(array1, array2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-5)new_array = combine_arrays( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-6) vbt.ChunkedArray(array1), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-7) vbt.ChunkedArray(array2), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-8) np.add,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-9) _size=len(array1), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-10) _merge_func="concat"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-11))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-12)new_array = combine_arrays( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-13) vbt.ChunkedArray(array1, axis=0), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-14) vbt.ChunkedArray(array2, axis=0), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-15) np.add,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-16) _size=array1.shape[0],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-17) _merge_func="row_stack"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-18))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-19)new_array = combine_arrays( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-20) vbt.ChunkedArray(array1, axis=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-21) vbt.ChunkedArray(array2, axis=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-22) np.add,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-23) _size=array1.shape[1],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-24) _merge_func="column_stack"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-20-25))
 
[/code]

 1. 2. 3. 4. 

Merging and execution are done in the same way as in [Parameterization](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#parameterization).


# Hybrid (super-chunks)[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#hybrid-super-chunks "Permanent link")

[Parameterized decorator](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#parameterization) and chunked decorator can be combined to process only a subset of parameter combinations at a time without the need of changing the function's design as in [Hybrid (mono-chunks)](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#hybrid-mono-chunks). Even though super-chunking may not be as fast as mono-chunking, it's still beneficiary when you want to process only a subset of parameter combinations at a time (but not all, otherwise, you should just use `distribute="chunks"` in the parameterized decorator without a chunked decorator) to keep RAM consumption in check, or when you want do some preprocessing and/or postprocessing such as flushing per bunch of parameter combinations.

Execute at most n parameter combinations per process
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-1)@vbt.parameterized
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-2)def my_pipeline(data, fast_window, slow_window): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-4) return result
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-6)@vbt.chunked(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-7) chunk_len=?, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-8) execute_kwargs=dict(chunk_len="auto", engine="pathos") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-9))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-10)def chunked_pipeline(data, fast_windows, slow_windows): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-11) return my_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-12) data, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-13) vbt.Param(fast_windows, level=0), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-14) vbt.Param(slow_windows, level=0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-15) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-17)param_product = vbt.combine_params( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-18) dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-19) fast_windows=fast_windows,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-20) slow_windows=slow_windows,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-21) ),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-22) build_index=False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-23))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-24)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-25)chunked_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-26) data,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-27) vbt.Chunked(param_product["fast_windows"]), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-28) vbt.Chunked(param_product["slow_windows"])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-21-29))
 
[/code]

 1. 2. 3. 4. 5. 


# Raw execution[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#raw-execution "Permanent link")

Whenever VBT needs to execute one function on multiple sets of arguments, it uses the function [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute), which takes a list of tasks (functions and their arguments) and executes them with an engine selected by the user. This function takes all the same arguments that you usually pass inside `execute_kwargs`.

Execute multiple indicator configurations in parallel
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-1)sma_func = vbt.talib_func("sma")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-2)ema_func = vbt.talib_func("ema")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-3)tasks = [
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-4) vbt.Task(sma_func, arr, 10), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-5) vbt.Task(sma_func, arr, 20),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-6) vbt.Task(ema_func, arr, 10),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-7) vbt.Task(ema_func, arr, 20),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-8)]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-9)keys = pd.MultiIndex.from_tuples([ 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-10) ("sma", 10),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-11) ("sma", 20),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-12) ("ema", 10),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-13) ("ema", 20),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-14)], names=["indicator", "timeperiod"])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-15)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-16)indicators_df = vbt.execute( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-17) tasks, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-18) keys=keys, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-19) merge_func="column_stack",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-20) engine="threadpool"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-22-21))
 
[/code]

 1. 2. 3. 


* * *

+


* * *

If you want to parallelize a workflow within a for-loop, put it into a function and decorate that function with [iterated](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.iterated). Then, when executing the decorated function, pass a total number of iterations or a range in place of the argument where you expect the iteration variable.

Execute a regular for-loop in parallel
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-1)# ______________________________ FROM ______________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-3)results = []
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-4)keys = []
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-5)for timeperiod in range(20, 50, 5):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-6) result = sma_func(arr, timeperiod)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-7) results.append(result)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-8) keys.append(timeperiod)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-9)keys = pd.Index(keys, name="timeperiod")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-10)sma_df = pd.concat(map(pd.Series, results), axis=1, keys=keys)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-12)# ______________________________ TO ______________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-14)@vbt.iterated(over_arg="timeperiod", merge_func="column_stack", engine="threadpool")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-15)def sma(arr, timeperiod):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-16) return sma_func(arr, timeperiod)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-18)sma = vbt.iterated( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-19) sma_func, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-20) over_arg="timeperiod", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-21) engine="threadpool", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-22) merge_func="column_stack"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-23))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-24)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-23-25)sma_df = sma(arr, range(20, 50, 5))
 
[/code]

 1. 

Execute a nested for-loop in parallel
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-1)# ______________________________ FROM ______________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-3)results = []
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-4)keys = []
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-5)for fast_window in range(20, 50, 5):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-6) for slow_window in range(20, 50, 5):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-7) if fast_window < slow_window:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-8) fast_sma = sma_func(arr, fast_window)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-9) slow_sma = sma_func(arr, slow_window)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-10) result = fast_sma - slow_sma
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-11) results.append(result)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-12) keys.append((fast_window, slow_window))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-13)keys = pd.MultiIndex.from_tuples(keys, names=["fast_window", "slow_window"])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-14)sma_diff_df = pd.concat(map(pd.Series, results), axis=1, keys=keys)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-15)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-16)# ______________________________ TO ______________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-18)@vbt.iterated(over_arg="fast_window", merge_func="column_stack", engine="pathos") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-19)@vbt.iterated(over_arg="slow_window", merge_func="column_stack", raise_no_results=False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-20)def sma_diff(arr, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-21) if fast_window >= slow_window:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-22) return vbt.NoResult
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-23) fast_sma = sma_func(arr, fast_window)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-24) slow_sma = sma_func(arr, slow_window)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-25) return fast_sma - slow_sma
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-26)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization/#__codelineno-24-27)sma_diff_df = sma_diff(arr, range(20, 50, 5), range(20, 50, 5))
 
[/code]

 1.