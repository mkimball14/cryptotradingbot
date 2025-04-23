# Indicators[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#indicators "Permanent link")

Question

Learn more in [Indicators documentation](https://vectorbt.pro/pvt_7a467f6b/documentation/indicators/).


# Listing[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#listing "Permanent link")

To list the currently supported indicators, use [IndicatorFactory.list_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_indicators). The returned indicator names can be filtered by location, which can be listed with [IndicatorFactory.list_locations](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_locations), or by evaluating a glob or regex pattern.

List supported indicators and locations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-1)indicator_names = vbt.IF.list_indicators() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-2)indicator_names = vbt.IF.list_indicators("vbt") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-3)indicator_names = vbt.IF.list_indicators("talib") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-4)indicator_names = vbt.IF.list_indicators("RSI*") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-5)indicator_names = vbt.IF.list_indicators("*ma") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-6)indicator_names = vbt.IF.list_indicators("[a-z]+ma$", use_regex=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-7)indicator_names = vbt.IF.list_indicators("*ma", location="pandas_ta") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-0-9)location_names = vbt.IF.list_locations() 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 

Note

Without specifying a location, indicators across all the locations will be parsed, which may take some time. Thus, make sure to not repeatedly call this function; instead, save the results to a variable.


* * *

+


* * *

To get the class of an indicator, use [IndicatorFactory.get_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.get_indicator).

How to get the indicator class
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-1-1)vbt.BBANDS 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-1-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-1-3)BBANDS = vbt.IF.get_indicator("pandas_ta:BBANDS") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-1-4)BBANDS = vbt.indicator("pandas_ta:BBANDS") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-1-5)BBANDS = vbt.IF.from_pandas_ta("BBANDS") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-1-6)BBANDS = vbt.pandas_ta("BBANDS") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-1-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-1-8)RSI = vbt.indicator("RSI") 
 
[/code]

 1. 2. 3. 4. 5. 6. 


* * *

+


* * *

To get familiar with an indicator class, call [phelp](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.phelp) on the `run` class method, which is used to run the indicator. Alternatively, the specification such as input names is also available via various properties to be accessed in a programmable fashion.

How to get the specification of an indicator class
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-2-1)vbt.phelp(vbt.OLS.run) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-2-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-2-3)print(vbt.OLS.input_names) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-2-4)print(vbt.OLS.param_names) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-2-5)print(vbt.OLS.param_defaults) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-2-6)print(vbt.OLS.in_output_names) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-2-7)print(vbt.OLS.output_names) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-2-8)print(vbt.OLS.lazy_output_names) 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 


# Running[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#running "Permanent link")

To run an indicator, call the [IndicatorBase.run](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase.run) class method of its class by manually passing the input arrays (which can be any array-like objects such as Pandas DataFrames and NumPy arrays), parameters (which can be single values and lists for testing multiple parameter combinations), and other arguments expected by the indicator. The result of running the indicator is **an indicator instance** (not the actual arrays!).

How to run an indicator
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-1)bbands = vbt.BBANDS.run(close) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-2)bbands = vbt.BBANDS.run(open) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-3)bbands = vbt.BBANDS.run(close, window=20) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-4)bbands = vbt.BBANDS.run(close, window=vbt.Default(20)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-5)bbands = vbt.BBANDS.run(close, window=20, hide_params=["window"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-6)bbands = vbt.BBANDS.run(close, window=20, hide_params=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-7)bbands = vbt.BBANDS.run(close, window=[10, 20, 30]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-8)bbands = vbt.BBANDS.run(close, window=[10, 20, 30], alpha=[2, 3, 4]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-3-9)bbands = vbt.BBANDS.run(close, window=[10, 20, 30], alpha=[2, 3, 4], param_product=True) 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 

Warning

Testing a wide grid of parameter combinations will produce wide arrays. For example, testing 10000 parameter combinations on one year of daily data would produce an array that takes 30MB of RAM. If the indicator returns three arrays, the RAM consumption would be at least 120MB. One year of minute data would result in staggering 40GB. Thus, for testing wide parameter grids it's recommended to test only a subset of combinations at a time, such as with the use of [parameterization](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization#parameterization) or [chunking](https://vectorbt.pro/pvt_7a467f6b/cookbook/optimization#chunking).


* * *

+


* * *

Often, there's a need to make an indicator skip missing values. For this, use `skipna=True`. This argument not only works for TA-Lib indicators but for any indicators, the only requirement: the jitted loop must be disabled. Also, when a two-dimensional input array is passed, you need to additionally pass `split_columns=True` to split its columns and process one column at once.

Run an indicator on valid values only
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-4-1)bbands = vbt.BBANDS.run(close_1d, skipna=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-4-2)bbands = vbt.BBANDS.run(close_2d, split_columns=True, skipna=True)
 
[/code]


* * *

+


* * *

Another way is to remove missing values altogether.

Remove missing values in an indicator
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-5-1)bbands = bbands.dropna() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-5-2)bbands = bbands.dropna(how="all") 
 
[/code]

 1. 2. 


* * *

+


* * *

To retrieve the output arrays from an indicator instance, either access each as an attribute, or use various unpacking options such as [IndicatorBase.unpack](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase.unpack).

How to retrieve output arrays
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-1)bbands = vbt.talib("BBANDS").run(close)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-2)upperband_df = bbands.upperband 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-3)middleband_df = bbands.middleband
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-4)lowerband_df = bbands.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-5)upperband_df, middleband_df, lowerband_df = bbands.unpack() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-6)output_dict = bbands.to_dict() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-7)output_df = bbands.to_frame() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-9)sma = vbt.talib("SMA").run(close)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-10)sma_df = sma.real 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-11)sma_df = sma.sma 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-12)sma_df = sma.output 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-6-13)sma_df = sma.unpack()
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 


* * *

+


* * *

To keep outputs in the NumPy format and/or omit any shape checks, use `return_raw="outputs"`.

Keep NumPy format
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-7-1)upperband, middleband, lowerband = vbt.talib("BBANDS").run(close, return_raw="outputs")
 
[/code]


* * *

+


* * *

An even simpler way to run indicators is by using [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run), which takes an indicator name or class, identifies what input names the indicator expects, and then runs the indicator while passing all the inputs found in the data instance automatically. This method also allows unpacking and running multiple indicators, which is very useful for feature engineering.

How to run indicators automatically
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-1)bbands = data.run("vbt:BBANDS") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-2)bbands = data.run("vbt:BBANDS", window=20) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-3)upper, middle, lower = data.run("vbt:BBANDS", unpack=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-5)features_df = data.run(["talib:BBANDS", "talib:RSI"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-6)bbands, rsi = data.run(["talib:BBANDS", "talib:RSI"], concat=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-7)features_df = data.run( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-8) ["talib:BBANDS", "talib:RSI"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-9) timeperiod=vbt.run_func_dict(talib_bbands=20, talib_rsi=30),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-10) hide_params=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-11))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-12)features_df = data.run( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-13) ["talib:BBANDS", "vbt:RSI"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-14) talib_bbands=vbt.run_arg_dict(timeperiod=20),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-15) vbt_rsi=vbt.run_arg_dict(window=30),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-16) hide_params=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-17))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-8-18)features_df = data.run("talib_all") 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 


* * *

+


* * *

To quickly run and plot a TA-Lib indicator on a single parameter combination without using the indicator factory, use [talib_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/talib_/#vectorbtpro.indicators.talib.talib_func) and [talib_plot_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/talib_/#vectorbtpro.indicators.talib.talib_plot_func) respectively. In contrast to the official TA-Lib implementation, it can properly handle DataFrames, NaNs, broadcasting, and timeframes. The indicator factory's TA-Lib version is based on these two functions.

Quickly run and plot a TA-Lib indicator
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-9-1)run_bbands = vbt.talib_func("BBANDS")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-9-2)upperband, middleband, lowerband = run_bbands(close, timeperiod=2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-9-3)upperband, middleband, lowerband = data.run("talib_func:BBANDS", timeperiod=2) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-9-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-9-5)plot_bbands = vbt.talib_plot_func("BBANDS")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-9-6)fig = plot_bbands(upperband, middleband, lowerband)
 
[/code]

 1. 


# Parallelization[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#parallelization "Permanent link")

Parameter combinations are processed using [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) such that it's fairly easy to parallelize their execution.

Various parallelization configurations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-1)any_indicator.run(...) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-3)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-5)numba_indicator.run( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-6) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-7) jitted_loop=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-8) jitted_warmup=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-9) execute_kwargs=dict(n_chunks="auto", engine="threadpool")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-10))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-12)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-13)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-14)python_indicator.run( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-15) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-16) execute_kwargs=dict(n_chunks="auto", distribute="chunks", engine="pathos")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-10-17))
 
[/code]

 1. 2. 3. 4. 5. 


# Registration[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#registration "Permanent link")

Custom indicators can be registered by the indicator factory to appear in the list of all indicators. This is convenient to be able to refer to the indicator by its name when running a data instance. Upon registration, you can assign the indicator to a custom location (the default location is "custom"), which acts as a tag or group; this can be used to build arbitrary indicator groups. One indicator can be assigned to multiple locations. Custom indicators have priority over built-in indicators.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-1)vbt.IF.register_custom_indicator(sma_indicator) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-2)vbt.IF.register_custom_indicator(sma_indicator, "SMA") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-3)vbt.IF.register_custom_indicator(sma_indicator, "SMA", location="rolling") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-4)vbt.IF.register_custom_indicator(sma_indicator, "rolling:SMA")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-5)vbt.IF.register_custom_indicator("talib:sma", location="rolling") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-7)vbt.IF.deregister_custom_indicator("SMA", location="rolling") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-8)vbt.IF.deregister_custom_indicator("rolling:SMA")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-9)vbt.IF.deregister_custom_indicator("SMA") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-10)vbt.IF.deregister_custom_indicator(location="rolling") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indicators/#__codelineno-11-11)vbt.IF.deregister_custom_indicator() 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8.