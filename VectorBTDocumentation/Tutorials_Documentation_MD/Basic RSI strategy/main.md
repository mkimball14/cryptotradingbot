# Basic RSI strategy[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#basic-rsi-strategy "Permanent link")

One of the main powers of vectorbt (PRO) is the ability to create and backtest numerous strategy configurations in the blink of an eye. In this introductory example, we will explore how profitable is the following RSI strategy commonly used by beginners:

> If the RSI is less than 30, it indicates a stock is reaching oversold conditions and may see a trend reversal, or bounceback, towards a higher share price. Once the reversal is confirmed, a buy trade is placed. Conversely, if the RSI is more than 70, it indicates that a stock is reaching an overbought condition and may see a trend reversal, or pullback, in price. After a confirmation of the reversal, a sell trade is placed.

As a bonus, we will gradually expand the analysis towards multiple parameter combinations. Sounds fun? Let's start.


# Single backtest[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#single-backtest "Permanent link")

First, we will take care of data. Using a one-liner, we will download all available daily data for the pair BTC/USDT from Binance:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-0-1)>>> from vectorbtpro import * 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-0-3)>>> data = vbt.BinanceData.pull('BTCUSDT')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-0-4)>>> data
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-0-5)<vectorbtpro.data.custom.binance.BinanceData at 0x7f9c40c59550>
 
[/code]

 1. 

100%

The returned object is of type [BinanceData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/binance/#vectorbtpro.data.custom.binance.BinanceData), which extends [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) to communicate with the Binance API. The class [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) is a vectorbt's in-house container for retrieving, storing, and managing data. Upon receiving a DataFrame, it post-processes and stores the DataFrame inside the dictionary [Data.data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.data) keyed by pair (also referred to as a "symbol" in vectorbt). We can get our DataFrame either from this dictionary, or by using the convenient method [Data.get](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.get), which also allows for specifying one or more columns instead of returning the entire DataFrame at once.

Let's plot the data with [Data.plot](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.plot):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-1-1)>>> data.plot().show() 
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/ohlcv.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/ohlcv.dark.svg#only-dark)

Another way to describe the data is by using the Pandas' [info](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html) method. The tabular format is especially useful for counting null values (which our data apparently doesn't have - good!)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-1)>>> data.data['BTCUSDT'].info()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-2)<class 'pandas.core.frame.DataFrame'>
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-3)DatetimeIndex: 1813 entries, 2017-08-17 00:00:00+00:00 to 2022-08-03 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-4)Freq: D
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-5)Data columns (total 9 columns):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-6) # Column Non-Null Count Dtype 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-7)--- ------ -------------- ----- 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-8) 0 Open 1813 non-null float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-9) 1 High 1813 non-null float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-10) 2 Low 1813 non-null float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-11) 3 Close 1813 non-null float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-12) 4 Volume 1813 non-null float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-13) 5 Quote volume 1813 non-null float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-14) 6 Trade count 1813 non-null int64 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-15) 7 Taker base volume 1813 non-null float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-16) 8 Taker quote volume 1813 non-null float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-17)dtypes: float64(8), int64(1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-2-18)memory usage: 141.6 KB
 
[/code]

In our example, we will generate signals based on the opening price and execute them based on the closing price. We can also place orders a soon as the signal is generated, or at any later time, but we will illustrate how to separate generation of signals from their execution.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-3-1)>>> open_price = data.get('Open')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-3-2)>>> close_price = data.get('Close') 
 
[/code]

 1. 

It's time to run the indicator!

VectorBT® PRO supports 5 (!) different implementations of RSI: one implemented using Numba, and the other four ported from three different technical analysis libraries. Each indicator has been wrapped with the almighty [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory) ![🦾](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f9be.svg)

To list all the available indicators or to search for a specific indicator, we can use [IndicatorFactory.list_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_indicators):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-4-1)>>> vbt.IF.list_indicators("RSI*")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-4-2)['vbt:RSI', 'talib:RSI', 'pandas_ta:RSI', 'ta:RSIIndicator', 'technical:RSI']
 
[/code]

We can then retrieve the actual indicator class as follows:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-5-1)>>> vbt.indicator("talib:RSI")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-5-2)vectorbtpro.indicators.factory.talib.RSI
 
[/code]

Or manually:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-1)>>> vbt.RSI 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-2)vectorbtpro.indicators.custom.RSI
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-4)>>> vbt.talib('RSI') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-5)vectorbtpro.indicators.factory.talib.RSI
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-7)>>> vbt.ta('RSIIndicator') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-8)vectorbtpro.indicators.factory.ta.RSIIndicator
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-10)>>> vbt.pandas_ta('RSI') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-11)vectorbtpro.indicators.factory.pandas_ta.RSI
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-13)>>> vbt.technical('RSI') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-6-14)vectorbtpro.indicators.factory.technical.RSI
 
[/code]

 1. 2. 3. 4. 5. 

Here's a rule of thumb on which implementation to choose:

 1. Use TA-Lib indicators for fastest execution (natively written in C)
 2. Use vectorbt indicators for fast execution and plotting (compiled with Numba)
 3. Use indicators from other libraries in case they provide more options

To run any indicator, use the method `run`. To see what arguments the method accepts, pass it to [phelp](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.phelp):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-1)>>> vbt.phelp(vbt.RSI.run)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-2)RSI.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-3) close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-4) window=Default(value=14),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-5) wtype=Default(value='wilder'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-6) short_name='rsi',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-7) hide_params=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-8) hide_default=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-9) **kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-10)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-11) Run `RSI` indicator.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-13) * Inputs: `close`
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-14) * Parameters: `window`, `wtype`
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-15) * Outputs: `rsi`
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-17) Pass a list of parameter names as `hide_params` to hide their column levels.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-18) Set `hide_default` to False to show the column levels of the parameters with a default value.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-19)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-7-20) Other keyword arguments are passed to `RSI.run_pipeline`.
 
[/code]

As we can see above, we need to at least provide `close`, which can be any numeric time series. Also, by default, the rolling window is 14 bars long and uses the Wilder's smoothed moving average. Since we want to make decisions based on the opening price, we will pass `open_price` as `close`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-8-1)>>> rsi = vbt.RSI.run(open_price)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-8-2)>>> rsi
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-8-3)<vectorbtpro.indicators.custom.RSI at 0x7f9c20921ac8>
 
[/code]

That's all! By executing the method [RSI.run](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/rsi/#vectorbtpro.indicators.custom.rsi.RSI.run), we calculated the RSI values and have received an instance with various methods and properties for their analysis. To retrieve the resulting Pandas object, we need to query the `rsi` attribute (see "Outputs" in the output of `phelp`).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-1)>>> rsi.rsi
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-3)2017-08-17 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-4)2017-08-18 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-5)2017-08-19 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-6)2017-08-20 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-7)2017-08-21 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-8)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-9)2022-07-30 00:00:00+00:00 60.541637
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-10)2022-07-31 00:00:00+00:00 59.503179
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-11)2022-08-01 00:00:00+00:00 56.750576
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-12)2022-08-02 00:00:00+00:00 56.512434
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-13)2022-08-03 00:00:00+00:00 54.177385
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-9-14)Freq: D, Name: Open, Length: 1813, dtype: float64
 
[/code]

Having the RSI array, we now want to generate an entry signal whenever any RSI value crosses below 30 and an exit signal whenever any RSI value crosses above 70:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-1)>>> entries = rsi.rsi.vbt.crossed_below(30) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-2)>>> entries
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-3)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-4)2017-08-17 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-5)2017-08-18 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-6)2017-08-19 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-7)2017-08-20 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-8)2017-08-21 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-9)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-10)2022-07-30 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-11)2022-07-31 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-12)2022-08-01 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-13)2022-08-02 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-14)2022-08-03 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-15)Freq: D, Name: Open, Length: 1813, dtype: bool
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-17)>>> exits = rsi.rsi.vbt.crossed_above(70) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-18)>>> exits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-19)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-20)2017-08-17 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-21)2017-08-18 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-22)2017-08-19 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-23)2017-08-20 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-24)2017-08-21 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-25)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-26)2022-07-30 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-27)2022-07-31 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-28)2022-08-01 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-29)2022-08-02 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-30)2022-08-03 00:00:00+00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-10-31)Freq: D, Name: Open, Length: 1813, dtype: bool
 
[/code]

 1. 2. 

The same can be done using the methods [RSI.rsi_crossed_below](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/rsi/#vectorbtpro.indicators.custom.rsi.RSI.rsi_crossed_below) and [RSI.rsi_crossed_above](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/rsi/#vectorbtpro.indicators.custom.rsi.RSI.rsi_crossed_above) that were auto-generated for the output `rsi` by [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-11-1)>>> entries = rsi.rsi_crossed_below(30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-11-2)>>> exits = rsi.rsi_crossed_above(70)
 
[/code]

Hint

If you are curious what else has been generated, print `dir(rsi)` or look into the [API](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/rsi/#vectorbtpro.indicators.custom.rsi.RSI) generated for the class.

Before we proceed with the portfolio modeling, let's plot the RSI and signals to ensure that we did everything right:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-12-1)>>> def plot_rsi(rsi, entries, exits):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-12-2)... fig = rsi.plot() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-12-3)... entries.vbt.signals.plot_as_entries(rsi.rsi, fig=fig) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-12-4)... exits.vbt.signals.plot_as_exits(rsi.rsi, fig=fig) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-12-5)... return fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-12-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-12-7)>>> plot_rsi(rsi, entries, exits).show()
 
[/code]

 1. 2. 3. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/rsi.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/rsi.dark.svg#only-dark)

The graph looks legit. But notice how there are multiple entries between two exits and vice versa? How does vectorbt handle it? When using [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals), vectorbt will automatically filter out all entry signals if the position has already been entered, and exit signals if the position has already been exited. But to make our analysis cleaner, let's keep each first signal:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-13-1)>>> clean_entries, clean_exits = entries.vbt.signals.clean(exits) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-13-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-13-3)>>> plot_rsi(rsi, clean_entries, clean_exits).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/rsi2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/rsi2.dark.svg#only-dark)

We can immediately see the difference. But what other methods exist to analyze the distribution of signals? How to _quantify_ such analysis? That's what vectorbt is all about. Let's compute various statistics of `clean_entries` and `clean_exits` using [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-1)>>> clean_entries.vbt.signals.total() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-2)8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-4)>>> clean_exits.vbt.signals.total() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-5)7
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-7)>>> ranges = clean_entries.vbt.signals.between_ranges(target=clean_exits) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-8)>>> ranges.duration.mean(wrap_kwargs=dict(to_timedelta=True)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-14-9)Timedelta('86 days 10:17:08.571428572')
 
[/code]

 1. 2. 3. 4. 

We are ready for modeling! We will be using the class method [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals), which will receive the signal arrays, process each signal one by one, and generate orders. It will then create an instance of [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) that can be used to assess the performance of the strategy.

Our experiment is simple: buy $100 of Bitcoin upon an entry signal and close the position upon an exit signal. Start with an infinite capital to not limit our buying power at any time.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-1)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-2)... close=close_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-3)... entries=clean_entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-4)... exits=clean_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-5)... size=100,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-6)... size_type='value',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-7)... init_cash='auto'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-9)>>> pf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-15-10)<vectorbtpro.portfolio.base.Portfolio at 0x7f9c40eea438>
 
[/code]

Info

Running the method above for the first time may take some time as it must be compiled first. Compilation will take place each time a new combination of data types is discovered. But don't worry: Numba caches most compiled functions and re-uses them in each new runtime.

Hint

If you look into the API of [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals), you will find many arguments to be set to None. The value `None` has a special meaning that instructs vectorbt to pull the default value from the global settings. You can discover all the default values for the `Portfolio` class [here](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.portfolio).

Let's print the statistics of our portfolio:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-1)>>> pf.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-2)Start 2017-08-17 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-3)End 2022-08-03 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-4)Period 1813 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-5)Start Value 100.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-6)Min Value 97.185676
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-7)Max Value 203.182943
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-8)End Value 171.335425
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-9)Total Return [%] 71.335425
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-10)Benchmark Return [%] 446.481746
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-11)Total Time Exposure [%] 38.113624
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-12)Max Gross Exposure [%] 100.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-13)Max Drawdown [%] 46.385941
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-14)Max Drawdown Duration 1613 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-15)Total Orders 15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-16)Total Fees Paid 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-17)Total Trades 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-18)Win Rate [%] 71.428571
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-19)Best Trade [%] 54.519055
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-20)Worst Trade [%] -32.078597
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-21)Avg Winning Trade [%] 26.905709
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-22)Avg Losing Trade [%] -19.345383
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-23)Avg Winning Trade Duration 87 days 09:36:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-24)Avg Losing Trade Duration 84 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-25)Profit Factor 3.477019
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-26)Expectancy 13.691111
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-27)Sharpe Ratio 0.505486
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-28)Calmar Ratio 0.246836
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-29)Omega Ratio 1.132505
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-30)Sortino Ratio 0.796701
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-16-31)dtype: object
 
[/code]

Hint

That are lots of statistics, right? If you're looking for the way they are implemented, print `pf.metrics` and look for the `calc_func` argument of the metric of interest. If some function is a lambda, look into the source code to reveal its contents.

Our strategy is not too bad: the portfolio has gained over 71% in profit over the last years, but holding Bitcoin is still better - staggering 450%. Despite the Bitcoin's high volatility, the minimum recorded portfolio value sits at $97 from $100 initially invested. The total time exposure of 38% means that we were in the market 38% of the time. The maximum gross exposure of 100% means that we invested 100% of our available cash balance, each single trade. The maximum drawdown (MDD) of 46% is the maximum distance our portfolio value fell after recording a new high (stop loss to the rescue?). 

The total number of orders matches the total number of (cleaned) signals, but why is the total number of trades suddenly 8 instead of 15? By default, a trade in the vectorbt's universe is a sell order; as soon as an exit order has been filled (by reducing or closing the current position), the profit and loss (PnL) based on the weighted average entry and exit price is calculated. The win rate of 70% means that 70% of the trades (sell orders) generated a profit, with the best trade bringing 54% in profit and the worst one bringing 32% in loss. Since the average winning trade generating more profit than the average losing trade generating loss, we can see various metrics being positive, such as the profit factor and the expectancy.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-17-1)>>> pf.plot(settings=dict(bm_returns=False)).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/pf.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/pf.dark.svg#only-dark)

Hint

A benefit of an interactive plot like above is that you can use tools from the Plotly toolbar to draw a vertical line that connects orders, their P&L, and how they affect the cumulative returns. Try it out!

So, how do we improve from here?


# Multiple backtests[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#multiple-backtests "Permanent link")


# Using for-loop[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#using-for-loop "Permanent link")

Even such a basic strategy as ours has many potential parameters:

 1. Lower threshold (`lower_th`)
 2. Upper threshold (`upper_th`)
 3. Window length (`window`)
 4. Smoothing method (`ewm`)

To make our analysis as flexible as possible, we will write a function that lets us specify all of that information, and return a subset of statistics:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-1)>>> def test_rsi(window=14, wtype="wilder", lower_th=30, upper_th=70):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-2)... rsi = vbt.RSI.run(open_price, window=window, wtype=wtype)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-3)... entries = rsi.rsi_crossed_below(lower_th)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-4)... exits = rsi.rsi_crossed_above(upper_th)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-5)... pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-6)... close=close_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-7)... entries=entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-8)... exits=exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-9)... size=100,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-10)... size_type='value',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-11)... init_cash='auto')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-12)... return pf.stats([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-13)... 'total_return', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-14)... 'total_trades', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-15)... 'win_rate', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-16)... 'expectancy'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-17)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-19)>>> test_rsi()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-20)Total Return [%] 71.335425
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-21)Total Trades 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-22)Win Rate [%] 71.428571
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-23)Expectancy 13.691111
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-24)dtype: object
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-25)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-26)>>> test_rsi(lower_th=20, upper_th=80)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-27)Total Return [%] 6.652287
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-28)Total Trades 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-29)Win Rate [%] 50.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-30)Expectancy 3.737274
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-18-31)dtype: object
 
[/code]

Note

We removed the signal cleaning step because it makes no difference when signals are passed to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) (which cleans the signals automatically anyway).

By raising the upper threshold to 80% and lowering the lower threshold to 20%, the number of trades has decreased to just 2 because it becomes more difficult to cross the thresholds. We can also observe how the total return fell to roughly 7% - not a good sign. But how do we actually know whether this negative result indicates that our strategy is trash and not because of a pure luck? Testing one parameter combination from a huge space usually means making a wild guess.

Let's generate multiple parameter combinations for thresholds, simulate them, and concatenate their statistics for further analysis:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-1)>>> lower_ths = range(20, 31) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-2)>>> upper_ths = range(70, 81) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-3)>>> th_combs = list(product(lower_ths, upper_ths)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-4)>>> len(th_combs)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-5)121
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-7)>>> comb_stats = [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-8)... test_rsi(lower_th=lower_th, upper_th=upper_th)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-9)... for lower_th, upper_th in th_combs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-19-10)... ] 
 
[/code]

 1. 2. 3. 4. 

We just simulated 121 different combinations of the upper and lower threshold and stored their statistics inside a list. In order to analyze this list, we need to convert it to a DataFrame first, with metrics arranged as columns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-1)>>> comb_stats_df = pd.DataFrame(comb_stats)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-2)>>> comb_stats_df
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-3) Total Return [%] Total Trades Win Rate [%] Expectancy
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-4)0 24.369550 3 66.666667 10.606342
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-5)1 37.380341 3 66.666667 16.203667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-6)2 34.560194 3 66.666667 14.981187
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-7)3 31.090080 3 66.666667 13.833710
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-8)4 31.090080 3 66.666667 13.833710
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-9).. ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-10)116 51.074571 6 80.000000 18.978193
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-11)117 62.853840 6 80.000000 21.334047
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-12)118 40.685579 5 75.000000 21.125494
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-13)119 -5.990835 4 66.666667 13.119897
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-14)120 -10.315159 4 66.666667 11.678455
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-20-16)[121 rows x 4 columns]
 
[/code]

But how do we know which row corresponds to which parameter combination? We will build a [MultiIndex](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html) with two levels, `lower_th` and `upper_th`, and make it the index of `comb_stats_df`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-1)>>> comb_stats_df.index = pd.MultiIndex.from_tuples(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-2)... th_combs, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-3)... names=['lower_th', 'upper_th'])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-4)>>> comb_stats_df
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-5) Total Return [%] Total Trades Win Rate [%] Expectancy
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-6)lower_th upper_th 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-7)20 70 24.369550 3 66.666667 10.606342
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-8) 71 37.380341 3 66.666667 16.203667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-9) 72 34.560194 3 66.666667 14.981187
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-10) 73 31.090080 3 66.666667 13.833710
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-11) 74 31.090080 3 66.666667 13.833710
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-12)... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-13)30 76 51.074571 6 80.000000 18.978193
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-14) 77 62.853840 6 80.000000 21.334047
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-15) 78 40.685579 5 75.000000 21.125494
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-16) 79 -5.990835 4 66.666667 13.119897
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-17) 80 -10.315159 4 66.666667 11.678455
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-21-19)[121 rows x 4 columns]
 
[/code]

Much better! We can now analyze every piece of the retrieved information from different angles. Since we have the same number of lower and upper thresholds, let's create a heatmap with the X axis reflecting the lower thresholds, the Y axis reflecting the upper thresholds, and the color bar reflecting the expectancy:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-22-1)>>> comb_stats_df['Expectancy'].vbt.heatmap().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/heatmap.dark.svg#only-dark)

We can explore entire regions of parameter combinations that yield positive or negative results.


# Using columns[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#using-columns "Permanent link")

As you might have read in the documentation, vectorbt loves processing multidimensional data. In particular, it's built around the idea that you can represent each asset, period, parameter combination, and a backtest in general, as a column in a two-dimensional array.

Instead of computing everything in a loop (which isn't too bad but usually executes magnitudes slower than a vectorized solution) we can change our code to accept parameters as arrays. A function that takes such array will automatically convert multiple parameters into multiple columns. A big benefit of this approach is that we don't have to collect our results, put them in a list, and convert into a DataFrame - it's all done by vectorbt!

First, define the parameters that we would like to test:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-23-1)>>> windows = list(range(8, 21))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-23-2)>>> wtypes = ["simple", "exp", "wilder"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-23-3)>>> lower_ths = list(range(20, 31))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-23-4)>>> upper_ths = list(range(70, 81))
 
[/code]

Instead of applying `itertools.product`, we will instruct various parts of our pipeline to build a product instead, so we can observe how each part affects the column hierarchy.

The RSI part is easy: we can pass `param_product=True` to build a product of `windows` and `wtypes` and run the calculation over each column in `open_price`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-1)>>> rsi = vbt.RSI.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-2)... open_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-3)... window=windows, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-4)... wtype=wtypes, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-5)... param_product=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-6)>>> rsi.rsi.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-7)MultiIndex([( 8, 'simple'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-8) ( 8, 'exp'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-9) ( 8, 'wilder'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-10) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-11) (20, 'simple'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-12) (20, 'exp'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-13) (20, 'wilder')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-24-14) names=['rsi_window', 'rsi_wtype'])
 
[/code]

We see that [RSI](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/rsi/#vectorbtpro.indicators.custom.rsi.RSI) appended two levels to the column hierarchy: `rsi_window` and `rsi_wtype`. Those are similar to the ones we created manually for thresholds in [Using for-loop](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#using-for-loop). There are now 39 columns in total, which is just `len(open_price.columns)` x `len(windows)` x `len(wtypes)`.

The next part are crossovers. In contrast to indicators, they are regular functions that take any array-like object, broadcast it to the `rsi` array, and search for crossovers. The broadcasting step is done using [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast), which is a very powerful function for bringing multiple arrays to a single shape (learn more about broadcasting in the documentation).

In our case, we want to build a product of `lower_ths`, `upper_th_index`, and all columns in `rsi`. Since both `rsi_crossed_below` and `rsi_crossed_above` are two different functions, we need to build a product of the threshold values manually and then instruct each crossover function to combine them with every column in `rsi`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-1)>>> lower_ths_prod, upper_ths_prod = zip(*product(lower_ths, upper_ths))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-2)>>> len(lower_ths_prod) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-3)121
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-4)>>> len(upper_ths_prod)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-5)121
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-7)>>> lower_th_index = vbt.Param(lower_ths_prod, name='lower_th') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-8)>>> entries = rsi.rsi_crossed_below(lower_th_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-9)>>> entries.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-10)MultiIndex([(20, 8, 'simple'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-11) (20, 8, 'exp'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-12) (20, 8, 'wilder'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-13) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-14) (30, 20, 'simple'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-15) (30, 20, 'exp'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-16) (30, 20, 'wilder')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-17) names=['lower_th', 'rsi_window', 'rsi_wtype'], length=4719)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-19)>>> upper_th_index = vbt.Param(upper_ths_prod, name='upper_th')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-20)>>> exits = rsi.rsi_crossed_above(upper_th_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-21)>>> exits.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-22)MultiIndex([(70, 8, 'simple'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-23) (70, 8, 'exp'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-24) (70, 8, 'wilder'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-25) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-26) (80, 20, 'simple'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-27) (80, 20, 'exp'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-28) (80, 20, 'wilder')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-25-29) names=['upper_th', 'rsi_window', 'rsi_wtype'], length=4719)
 
[/code]

 1. 2. 

We have produced over 4719 columns - madness! But did you notice that `entries` and `exits` have different columns now? The first one has `lower_th` as one of the column levels, the second one has `upper_th`. How are we supposed to pass differently labeled arrays (including `close_price` with one column) to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals)?

No worries, vectorbt knows exactly how to merge this information. Let's see:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-1)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-2)... close=close_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-3)... entries=entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-4)... exits=exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-5)... size=100,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-6)... size_type='value',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-7)... init_cash='auto'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-9)>>> pf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-10)<vectorbtpro.portfolio.base.Portfolio at 0x7f9c415ed5c0>
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-12)>>> stats_df = pf.stats([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-13)... 'total_return', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-14)... 'total_trades', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-15)... 'win_rate', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-16)... 'expectancy'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-17)... ], agg_func=None) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-18)>>> stats_df
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-19) Total Return [%] Total Trades \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-20)lower_th upper_th rsi_window rsi_wtype 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-21)20 70 8 simple -25.285842 31 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-22) exp -7.939736 29 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-23) wilder 61.979801 11 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-24)... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-25) 20 simple -59.159157 4 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-26) exp -3.331163 8 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-27) wilder 31.479482 3 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-28)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-29) Win Rate [%] Expectancy 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-30)lower_th upper_th rsi_window rsi_wtype 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-31)20 70 8 simple 51.612903 -1.224523 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-32) exp 58.620690 -0.307862 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-33) wilder 72.727273 5.634527 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-34)... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-35) 20 simple 33.333333 -16.159733 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-36) exp 57.142857 7.032204 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-37) wilder 50.000000 38.861607 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-38)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-26-39)[4719 rows x 4 columns]
 
[/code]

 1. 

Congrats! We just backtested 4719 parameter combinations in less than a second ![⚡](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/26a1.svg)

Important

Even though we gained some unreal performance, we need to be careful to not occupy the entire RAM with our wide arrays. We can check the size of any [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable) instance using [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize). For example, to print the total size of our portfolio in a human-readable format:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-27-1)>>> print(pf.getsize())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-27-2)9.4 MB
 
[/code]

Even though the portfolio holds about 10 MB of compressed data, it must generate many arrays, such as the portfolio value, that have the same shape as the number of timestamps x parameter combinations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-28-1)>>> np.product(pf.wrapper.shape) * 8 / 1024 / 1024
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-28-2)65.27364349365234
 
[/code]

We can see that each floating array occupies 65 MB of memory. By creating a dozen of such arrays (which is often the worst case), the memory consumption may jump to 1 GB very quickly.

One option is to use Pandas itself to analyze the produced statistics. For example, calculate the mean expectancy of each `rsi_window`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-1)>>> stats_df['Expectancy'].groupby('rsi_window').mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-2)rsi_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-3)8 0.154425
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-4)9 0.064130
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-5)10 -0.915478
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-6)11 -0.523294
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-7)12 0.742266
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-8)13 3.898482
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-9)14 4.414367
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-10)15 6.916872
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-11)16 8.915225
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-12)17 12.204188
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-13)18 12.897135
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-14)19 14.508950
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-15)20 16.429515
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-29-16)Name: Expectancy, dtype: float64
 
[/code]

The longer is the RSI window, the higher is the mean expectancy.

Display the top 5 parameter combinations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-1)>>> stats_df.sort_values(by='Expectancy', ascending=False).head()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-2) Total Return [%] Total Trades \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-3)lower_th upper_th rsi_window rsi_wtype 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-4)22 80 20 wilder 187.478208 2 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-5)21 80 20 wilder 187.478208 2 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-6)26 80 20 wilder 152.087039 3 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-7)23 80 20 wilder 187.478208 2 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-8)25 80 20 wilder 201.297495 3 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-10) Win Rate [%] Expectancy 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-11)lower_th upper_th rsi_window rsi_wtype 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-12)22 80 20 wilder 100.0 93.739104 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-13)21 80 20 wilder 100.0 93.739104 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-14)26 80 20 wilder 100.0 93.739104 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-15)23 80 20 wilder 100.0 93.739104 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-30-16)25 80 20 wilder 100.0 93.739104 
 
[/code]

To analyze any particular combination using vectorbt, we can select it from the portfolio the same way as we selected a column in a regular Pandas DataFrame. Let's plot the equity of the most successful combination:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-31-1)>>> pf[(22, 80, 20, "wilder")].plot_value().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/value.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/value.dark.svg#only-dark)

Hint

Instead of selecting a column from a portfolio, which will create a new portfolio with only that column, you can also check whether the method you want to call supports the argument `column` and pass your column using this argument. For instance, we could have also used `pf.plot_value(column=(22, 80, 20, "wilder"))`.

Even though, in theory, the best found setting doubles our money, it's still inferior to simply holding Bitcoin - our basic RSI strategy cannot beat the market ![💢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4a2.svg)

But even if it did, there is much more to just searching for right parameters: we need at least to (cross-) validate the strategy. We can also observe how the strategy behaves on other assets. Curious how to do it? Just expand `open_price` and `close_price` to contain multiple assets, and each example would work out-of-the-box!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-32-1)>>> data = vbt.BinanceData.pull(['BTCUSDT', 'ETHUSDT'])
 
[/code]

100%

Your homework is to run the examples on this data.

The final columns should become as follows:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-33-1)MultiIndex([(20, 70, 8, 'simple', 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-33-2) (20, 70, 8, 'simple', 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-33-3) (20, 70, 8, 'exp', 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-33-4) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-33-5) (30, 80, 20, 'exp', 'ETHUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-33-6) (30, 80, 20, 'wilder', 'BTCUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-33-7) (30, 80, 20, 'wilder', 'ETHUSDT')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-33-8) names=['lower_th', 'upper_th', 'rsi_window', 'rsi_wtype', 'symbol'], length=9438)
 
[/code]

We see that the column hierarchy now contains another level - `symbol` \- denoting the asset. Let's visualize the distribution of the expectancy across both assets:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-34-1)>>> eth_mask = stats_df.index.get_level_values('symbol') == 'ETHUSDT'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-34-2)>>> btc_mask = stats_df.index.get_level_values('symbol') == 'BTCUSDT'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-34-3)>>> pd.DataFrame({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-34-4)... 'ETHUSDT': stats_df[eth_mask]['Expectancy'].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-34-5)... 'BTCUSDT': stats_df[btc_mask]['Expectancy'].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#__codelineno-34-6)... }).vbt.histplot(xaxis=dict(title="Expectancy")).show() 
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/histplot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/basic-rsi/histplot.dark.svg#only-dark)

ETH seems to react more aggressively to our strategy on average than BTC, maybe due to the market's higher volatility, a different structure, or just pure randomness.

And here's one of the main takeaways of such analysis: using strategies with simple and explainable mechanics, we can try to explain the mechanics of the market itself. Not only can we use this to improve ourselves and design better indicators, but use this information as an input to ML models, which are better at connecting dots than humans. Possibilities are endless!


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi/#summary "Permanent link")

VectorBT® PRO is a powerful vehicle that enables us to discover uncharted territories faster and analyze them in more detail. Instead of using overused and outdated charts and indicators from books and YouTube videos, we can build our own tools that go hand in hand with the market. We can backtest thousands of strategy configurations to learn how the market reacts to each one of them - in a matter of milliseconds. All it takes is creativity ![💡](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4a1.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/basic-rsi.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/BasicRSI.ipynb)