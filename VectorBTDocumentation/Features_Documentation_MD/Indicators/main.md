# Indicators[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#indicators "Permanent link")


# Hurst exponent[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#hurst-exponent "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_6_19.svg)

 * Estimating the Hurst exponent provides a measure of whether the data is a pure white-noise random process or has underlying trends. VectorBT® PRO offers five (!) different implementations.

Plot rolling Hurst exponent by method
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-0-1)>>> data = vbt.YFData.pull("BTC-USD", start="12 months ago")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-0-2)>>> hurst = vbt.HURST.run(data.close, method=["standard", "logrs", "rs", "dma", "dsod"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-0-3)>>> fig = vbt.make_subplots(specs=[[dict(secondary_y=True)]])
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-0-4)>>> data.plot(plot_volume=False, ohlc_trace_kwargs=dict(opacity=0.3), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-0-5)>>> fig = hurst.hurst.vbt.plot(fig=fig, add_trace_kwargs=dict(secondary_y=True))
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-0-6)>>> fig = fig.select_range(start=hurst.param_defaults["window"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-0-7)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/hurst.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/hurst.dark.svg#only-dark)


# Smart Money Concepts[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#smart-money-concepts "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_6_19.svg)

 * VectorBT® PRO integrates most of the indicators from the [Smart Money Concepts (SMC)](https://github.com/joshyattridge/smart-money-concepts) library.

Plot previous high and low
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-1)>>> data = vbt.YFData.pull("BTC-USD", start="6 months ago")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-2)>>> phl = vbt.smc("previous_high_low").run( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-3)... data.open,
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-4)... data.high,
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-5)... data.low,
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-6)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-7)... data.volume,
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-8)... time_frame=vbt.Default("7D")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-10)>>> fig = data.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-11)>>> phl.previous_high.rename("previous_high").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-12)>>> phl.previous_low.rename("previous_low").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-13)>>> (phl.broken_high == 1).rename("broken_high").vbt.signals.plot_as_markers(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-14)... y=phl.previous_high, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-15)... trace_kwargs=dict(marker=dict(color="limegreen")),
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-16)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-18)>>> (phl.broken_low == 1).rename("broken_low").vbt.signals.plot_as_markers(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-19)... y=phl.previous_low, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-20)... trace_kwargs=dict(marker=dict(color="orangered")),
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-21)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-1-23)>>> fig.show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/smc.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/smc.dark.svg#only-dark)


# Signal unraveling[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#signal-unraveling "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_2_22.svg)

 * To backtest each signal in isolation, you can now "unravel" each signal or pair of entry and exit signals into a separate column. This will generate a wide, two-dimensional mask which, when backtested, returns performance metrics for each signal rather than entire column.

For each signal, create a separate position with own stop orders
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-2)>>> fast_sma = data.run("talib_func:sma", timeperiod=20) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-3)>>> slow_sma = data.run("talib_func:sma", timeperiod=50)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-4)>>> entries = fast_sma.vbt.crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-5)>>> exits = fast_sma.vbt.crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-6)>>> entries, exits = entries.vbt.signals.unravel_between(exits, relation="anychain") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-7)>>> pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-8)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-9)... long_entries=entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-10)... short_entries=exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-11)... size=100, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-12)... size_type="value",
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-13)... init_cash="auto", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-14)... tp_stop=0.2, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-15)... sl_stop=0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-16)... group_by=vbt.ExceptLevel("signal"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-17)... cash_sharing=True
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-19)>>> pf.positions.returns.to_pd(ignore_index=True).vbt.barplot(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-20)... trace_kwargs=dict(marker=dict(colorscale="Spectral"))
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-2-21)... ).show() 
 
[/code]

 1. 2. 3. 4. 5. 6. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/signal_unraveling.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/signal_unraveling.dark.svg#only-dark)


# Lightweight TA-Lib[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#lightweight-ta-lib "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_14_0.svg)

 * TA-Lib functions wrapped with the indicator factory are very powerful because in contrast to the official TA-Lib implementation they know how to broadcast, handle DataFrames, skip missing values, and even resample to a different timeframe. Because TA-Lib functions on their own are lightning fast, wrapping them with the indicator factory introduces an overhead. To retain both the speed of TA-Lib and the power of VBT, the added functionality has been outsourced into a separate lightweight function that can be called by the user just like a regular TA-Lib function.

Run and plot an RSI resampled to the monthly timeframe
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-2)>>> run_rsi = vbt.talib_func("rsi")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-3)>>> rsi = run_rsi(data.close, timeperiod=12, timeframe="M") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-4)>>> rsi
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-5)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-6)2014-09-17 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-7)2014-09-18 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-8)2014-09-19 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-9)2014-09-20 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-10)2014-09-21 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-11) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-12)2024-01-18 00:00:00+00:00 64.210811
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-13)2024-01-19 00:00:00+00:00 64.210811
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-14)2024-01-20 00:00:00+00:00 64.210811
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-15)2024-01-21 00:00:00+00:00 64.210811
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-16)2024-01-22 00:00:00+00:00 64.210811
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-17)Freq: D, Name: Close, Length: 3415, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-18)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-19)>>> plot_rsi = vbt.talib_plot_func("rsi")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-3-20)>>> plot_rsi(rsi).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/native_talib.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/native_talib.dark.svg#only-dark)


# Indicator search[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#indicator-search "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_11_1.svg)

 * VectorBT® PRO implements or integrates a total of over 500 indicators, which makes it increasingly difficult to keep an overview. To make them more discoverable, there is a bunch of new methods to globally search for indicators.

List all moving average indicators
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-1)>>> vbt.IF.list_indicators("*ma")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-2)[
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-3) 'vbt:MA',
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-4) 'talib:DEMA',
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-5) 'talib:EMA',
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-6) 'talib:KAMA',
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-7) 'talib:MA',
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-8) ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-9) 'technical:ZEMA',
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-10) 'technical:ZLEMA',
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-11) 'technical:ZLHMA',
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-12) 'technical:ZLMA'
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-13)]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-15)>>> vbt.indicator("technical:ZLMA") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-4-16)vectorbtpro.indicators.factory.technical.ZLMA
 
[/code]

 1. 


# Indicators for ML[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#indicators-for-ml "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_2.svg)

 * Want to feed indicators as features to a machine-learning model? No more need to run them individually: you can instruct VBT to run all indicators of an indicator package on the given data instance; the data instance will recognize input names of each indicator and pass the required data. You can also easily change the defaults of each indicator.

Run all talib indicators on entire BTC-USD history
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-5-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-5-2)>>> features = data.run("talib", mavp=vbt.run_arg_dict(periods=14))
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-5-3)>>> features.shape
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-5-4)(3046, 175)
 
[/code]


# Signal detection[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#signal-detection "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_0.svg)

 * VectorBT® PRO implements an indicator based on a robust peak detection algorithm using z-scores. This indicator can be used to identify outbreaks and outliers in any time-series data.

Detect sudden changes in the bandwidth of a Bollinger Bands indicator
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-6-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-6-2)>>> fig = vbt.make_subplots(rows=2, cols=1, shared_xaxes=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-6-3)>>> bbands = data.run("bbands")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-6-4)>>> bbands.loc["2022"].plot(add_trace_kwargs=dict(row=1, col=1), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-6-5)>>> sigdet = vbt.SIGDET.run(bbands.bandwidth, factor=5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-6-6)>>> sigdet.loc["2022"].plot(add_trace_kwargs=dict(row=2, col=1), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-6-7)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/signal_detection.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/signal_detection.dark.svg#only-dark)


# Pivot detection[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#pivot-detection "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_7_1.svg)

 * Pivot detection indicator is a tool that can be used to find out when the price's trend is reversing. By determining the support and resistance areas, it helps to identify significant changes in price while filtering out short-term fluctuations, thus eliminating the noise. The workings are rather simple: register a peak when the price jumps above one threshold and a valley when the price falls below another threshold. Another advantage: in contrast to the [regular Zig Zag indicator](https://www.investopedia.com/ask/answers/030415/what-zig-zag-indicator-formula-and-how-it-calculated.asp), which tends to look into the future, our indicator returns only the confirmed pivot points and is safe to use in backtesting.

Plot the last pivot value
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-7-1)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2023")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-7-2)>>> fig = data.plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-7-3)>>> pivot_info = data.run("pivotinfo", up_th=1.0, down_th=0.5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-7-4)>>> pivot_info.plot(fig=fig, conf_value_trace_kwargs=dict(visible=False))
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-7-5)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/pivot_detection.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/pivot_detection.dark.svg#only-dark)


# Technical indicators[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#technical-indicators "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_7_0.svg)

 * VectorBT® PRO integrates most of the indicators and consensus classes from the freqtrade's [technical](https://github.com/freqtrade/technical) library.

Compute and plot the summary consensus with a one-liner
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-8-1)>>> vbt.YFData.pull("BTC-USD").run("sumcon", smooth=100).plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/sumcon.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/sumcon.dark.svg#only-dark)


# Renko chart[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#renko-chart "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_7_0.svg)

 * In contrast to regular charts, [Renko chart](https://www.investopedia.com/terms/r/renkochart.asp) is built using price movements. Each "brick" in this chart is created when the price moves a specified price amount. Since the output has irregular time intervals, only one column can be processed at a time. As with everything, the VBT's implementation can translate a huge number of data points very fast thanks to Numba.

Resample closing price into a Renko format
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-9-1)>>> data = vbt.YFData.pull("BTC-USD", start="2021", end="2022")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-9-2)>>> renko_ohlc = data.close.vbt.to_renko_ohlc(1000, reset_index=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-9-3)>>> renko_ohlc.vbt.ohlcv.plot().show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/renko_chart.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/renko_chart.dark.svg#only-dark)


# Rolling OLS[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#rolling-ols "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_3_0.svg)

 * Rolling regressions are one of the models for analyzing changing relationships among variables over time. In VBT, it's implemented as an indicator that takes two time series and returns the slope, intercept, prediction, error, and the z-score of the error at each time step. Not only this indicator can be used for cointegration tests, such as to determine optimal rebalancing timings in pairs trading, but it's also (literally) 1000x faster than the statsmodels' equivalent [RollingOLS](https://www.statsmodels.org/dev/generated/statsmodels.regression.rolling.RollingOLS.html) ![🔥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f525.svg)

Determine the spread between BTC and ETH
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-1)>>> data = vbt.YFData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-2)... ["BTC-USD", "ETH-USD"], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-3)... start="2022", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-4)... end="2023",
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-5)... missing_index="drop"
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-7)>>> ols = vbt.OLS.run(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-8)... data.get("Close", "BTC-USD"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-9)... data.get("Close", "ETH-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-10-11)>>> ols.plot_zscore().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/rolling_ols.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/rolling_ols.dark.svg#only-dark)


# TA-Lib time frames[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#ta-lib-time-frames "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_2_0.svg)

 * Comparing indicators on different time frames involves a lot of nuances. Thankfully, all TA-Lib indicators now support a parameter that resamples the input arrays to a target time frame, calculates the indicator, and then resamples the output arrays back to the original time frame - a parameterized MTF analysis has never been easier!

Tutorial

Learn more in the [MTF analysis](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis) tutorial.

Run SMA on multiple time frames and display the whole thing as a heatmap
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-1)>>> h1_data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-2)... "BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-3)... start="3 months ago UTC", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-4)... timeframe="1h"
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-6)>>> mtf_sma = vbt.talib("SMA").run(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-7)... h1_data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-8)... timeperiod=14, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-9)... timeframe=["1d", "4h", "1h"], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-10)... skipna=True
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-11-12)>>> mtf_sma.real.vbt.ts_heatmap().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/talib_time_frames.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/talib_time_frames.dark.svg#only-dark)


# 1D-native indicators[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#1d-native-indicators "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_10.svg)

 * Previously, own indicators could be created only by accepting two-dimensional input arrays, which forced the user to adapt all functions accordingly. With the new feature, the indicator factory can split each input array along columns and pass one column at once, making it super-easy to design indicators that are meant to be natively run on one-dimensional data (such as TA-Lib!).

Create a TA-Lib powered STOCHRSI indicator
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-1)>>> import talib
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-3)>>> params = dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-4)... rsi_period=14, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-5)... fastk_period=5, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-6)... slowk_period=3, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-7)... slowk_matype=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-8)... slowd_period=3, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-9)... slowd_matype=0
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-11)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-12)>>> def stochrsi_1d(close, *args):
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-13)... rsi = talib.RSI(close, args[0])
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-14)... k, d = talib.STOCH(rsi, rsi, rsi, *args[1:])
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-15)... return rsi, k, d
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-16)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-17)>>> STOCHRSI = vbt.IF(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-18)... input_names=["close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-19)... param_names=list(params.keys()),
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-20)... output_names=["rsi", "k", "d"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-21)... ).with_apply_func(stochrsi_1d, takes_1d=True, **params)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-22)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-23)>>> data = vbt.YFData.pull("BTC-USD", start="2022-01", end="2022-06")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-24)>>> stochrsi = STOCHRSI.run(data.close)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-25)>>> fig = stochrsi.k.rename("%K").vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-26)>>> stochrsi.d.rename("%D").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-12-27)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/stochrsi.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/stochrsi.dark.svg#only-dark)


# Parallelizable indicators[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#parallelizable-indicators "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_10.svg)

 * Processing of parameter combinations by the indicator factory can be distributed over multiple threads, processes, or even in the cloud. This helps immensely when working with slow indicators ![🐌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f40c.svg)

Benchmark a serial and multithreaded rolling min-max indicator
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-2)... def minmax_nb(close, window):
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-3)... return (
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-4)... vbt.nb.rolling_min_nb(close, window),
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-5)... vbt.nb.rolling_max_nb(close, window)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-7)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-8)>>> MINMAX = vbt.IF(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-9)... class_name="MINMAX",
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-10)... input_names=["close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-11)... param_names=["window"], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-12)... output_names=["min", "max"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-13)... ).with_apply_func(minmax_nb, window=14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-13-15)>>> data = vbt.YFData.pull("BTC-USD")
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-14-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-14-2)>>> minmax = MINMAX.run(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-14-3)... data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-14-4)... np.arange(2, 200),
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-14-5)... jitted_loop=True
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-14-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-14-7)420 ms ± 2.05 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-2)>>> minmax = MINMAX.run(
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-3)... data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-4)... np.arange(2, 200),
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-5)... jitted_loop=True,
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-6)... jitted_warmup=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-7)... execute_kwargs=dict(engine="threadpool", n_chunks="auto") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-15-9)120 ms ± 355 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
 
[/code]

 1. 2. 


# TA-Lib plotting[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#ta-lib-plotting "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_9.svg)

 * Every TA-Lib indicator knows how to be plotted - fully automatically based on output flags!

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-16-1)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2021")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-16-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-16-3)>>> vbt.talib("MACD").run(data.close).plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/talib.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/talib.dark.svg#only-dark)


# Indicator expressions[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#indicator-expressions "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_8.svg)

 * Indicators can now be parsed from expressions. An indicator expression is a regular string that represents a Python code enhanced through various extensions. The indicator factory can derive all the required information such as inputs, parameters, outputs, NumPy, VBT, and TA-Lib functions, and even complex indicators thanks to a unique format and a built-in matching mechanism. Designing indicators has never been easier!

Build a MACD indicator from an expression
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-1)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2021")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-3)>>> expr = """
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-4)... MACD:
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-5)... fast_ema = @talib_ema(close, @p_fast_w)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-6)... slow_ema = @talib_ema(close, @p_slow_w)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-7)... macd = fast_ema - slow_ema
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-8)... signal = @talib_ema(macd, @p_signal_w)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-9)... macd, signal
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-10)... """
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-11)>>> MACD = vbt.IF.from_expr(expr, fast_w=12, slow_w=26, signal_w=9) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-12)>>> macd = MACD.run(data.close)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-13)>>> fig = macd.macd.rename("MACD").vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-14)>>> macd.signal.rename("Signal").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-17-15)>>> fig.show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/indicator_expressions.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/indicator_expressions.dark.svg#only-dark)


# WorldQuant Alphas[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#worldquant-alphas "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_8.svg)

 * Each of the [WorldQuant's 101 Formulaic Alphas](https://arxiv.org/pdf/1601.00991.pdf) is now an indicator ![👀](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f440.svg)

Run the first alpha
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-1)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD", "XRP-USD"], missing_index="drop")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-3)>>> vbt.wqa101(1).run(data.close).out
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-4)symbol BTC-USD ETH-USD XRP-USD
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-5)Date 
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-6)2017-11-09 00:00:00+00:00 0.166667 0.166667 0.166667
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-7)2017-11-10 00:00:00+00:00 0.166667 0.166667 0.166667
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-8)2017-11-11 00:00:00+00:00 0.166667 0.166667 0.166667
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-9)2017-11-12 00:00:00+00:00 0.166667 0.166667 0.166667
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-10)2017-11-13 00:00:00+00:00 0.166667 0.166667 0.166667
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-11)... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-12)2023-01-31 00:00:00+00:00 0.166667 0.166667 0.166667
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-13)2023-02-01 00:00:00+00:00 0.000000 0.000000 0.500000
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-14)2023-02-02 00:00:00+00:00 0.000000 0.000000 0.500000
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-15)2023-02-03 00:00:00+00:00 0.000000 0.500000 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-16)2023-02-04 00:00:00+00:00 -0.166667 0.333333 0.333333
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-18-18)[1914 rows x 3 columns]
 
[/code]


# Robust crossovers[¶](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#robust-crossovers "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Crossovers are now robust to NaNs.

Remove a bunch of data points and plot the crossovers
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-1)>>> data = vbt.YFData.pull("BTC-USD", start="2022-01", end="2022-03")
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-2)>>> fast_sma = vbt.talib("SMA").run(data.close, vbt.Default(5)).real
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-3)>>> slow_sma = vbt.talib("SMA").run(data.close, vbt.Default(10)).real
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-4)>>> fast_sma.iloc[np.random.choice(np.arange(len(fast_sma)), 5)] = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-5)>>> slow_sma.iloc[np.random.choice(np.arange(len(slow_sma)), 5)] = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-6)>>> crossed_above = fast_sma.vbt.crossed_above(slow_sma, dropna=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-7)>>> crossed_below = fast_sma.vbt.crossed_below(slow_sma, dropna=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-8)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-9)>>> fig = fast_sma.rename("Fast SMA").vbt.lineplot()
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-10)>>> slow_sma.rename("Slow SMA").vbt.lineplot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-11)>>> crossed_above.vbt.signals.plot_as_entries(fast_sma, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-12)>>> crossed_below.vbt.signals.plot_as_exits(fast_sma, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/indicators/#__codelineno-19-13)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/resilient_crossovers.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/resilient_crossovers.dark.svg#only-dark)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/features/indicators.py.txt)