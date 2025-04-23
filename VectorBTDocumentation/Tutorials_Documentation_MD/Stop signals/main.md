# Stop signals[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#stop-signals "Permanent link")

Our goal is to utilize large-scale backtesting to compare the performance of trading with and without stop loss (SL), trailing stop (TS), and take profit (TP) signals. To make this attempt representative, we will run a huge number of experiments across three different dimensions: instruments, time, and parameters.

First, we will pick 10 cryptocurrencies by market capitalization (except stablecoins such as USDT) and fetch 3 years of their daily pricing data. In particular, we aim at backtesting the time period from 2018 to 2021 as it contains periods of sharp price drops (e.g., corrections due to ATH in December 2017 and coronavirus in March 2020) as well as surges (ATH in December 2020) — this keeps things balanced. For each instrument, we will split this time period into 400 smaller (and overlapping) time windows, each 6 months long. We will run our tests on each of these windows to account for different market regimes. For each instrument and time window, we will then generate an entry signal at the very first bar and find an exit signal according to the stop configuration. We will test 100 stop values with a 1% increment and compare the performance of each one to that of trading randomly and holding within this particular time window. In total, we will conduct 2,000,000 tests.

Important

Make sure that you have at least 16 GB of free RAM available, or memory swapping enabled.


# Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#parameters "Permanent link")

The first step is to define the parameters of the analysis pipeline. As discussed above, we will backtest 3 years of pricing data, 400 time windows, 10 cryptocurrencies, and 100 stop values. We will also set fees and slippage both to 0.25% and initial capital to $100 (the amount per se doesn't matter, but it must be the same for all assets to be comparable). Feel free to change any parameter of interest.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-2)>>> import ipywidgets
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-4)>>> seed = 42
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-5)>>> symbols = [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-6)... "BTC-USD", "ETH-USD", "XRP-USD", "BCH-USD", "LTC-USD", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-7)... "BNB-USD", "EOS-USD", "XLM-USD", "XMR-USD", "ADA-USD"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-8)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-9)>>> start_date = vbt.utc_timestamp("2018-01-01")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-10)>>> end_date = vbt.utc_timestamp("2021-01-01")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-11)>>> time_delta = end_date - start_date
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-12)>>> window_len = vbt.timedelta("180d")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-13)>>> window_cnt = 400
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-14)>>> exit_types = ["SL", "TS", "TP", "Random", "Holding"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-15)>>> step = 0.01 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-16)>>> stops = np.arange(step, 1 + step, step)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-18)>>> vbt.settings.wrapping["freq"] = "d"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-19)>>> vbt.settings.plotting["layout"]["template"] = "vbt_dark"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-20)>>> vbt.settings.portfolio["init_cash"] = 100. 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-21)>>> vbt.settings.portfolio["fees"] = 0.0025 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-22)>>> vbt.settings.portfolio["slippage"] = 0.0025 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-23)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-24)>>> pd.Series({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-25)... "Start date": start_date,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-26)... "End date": end_date,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-27)... "Time period (days)": time_delta.days,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-28)... "Assets": len(symbols),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-29)... "Window length": window_len,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-30)... "Windows": window_cnt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-31)... "Exit types": len(exit_types),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-32)... "Stop values": len(stops),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-33)... "Tests per asset": window_cnt * len(stops) * len(exit_types),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-34)... "Tests per window": len(symbols) * len(stops) * len(exit_types),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-35)... "Tests per exit type": len(symbols) * window_cnt * len(stops),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-36)... "Tests per stop type and value": len(symbols) * window_cnt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-37)... "Tests total": len(symbols) * window_cnt * len(stops) * len(exit_types)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-38)... })
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-39)Start date 2018-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-40)End date 2021-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-41)Time period (days) 1096
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-42)Assets 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-43)Window length 180 days, 0:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-44)Windows 400
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-45)Exit types 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-46)Stop values 100
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-47)Tests per asset 200000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-48)Tests per window 5000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-49)Tests per exit type 400000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-50)Tests per stop type and value 4000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-51)Tests total 2000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-0-52)dtype: object
 
[/code]

 1. 2. 3. 4. 

Our configuration yields sample sizes with enough statistical power to analyze four variables: assets (200k tests per asset), time (5k tests per time window), exit types (400k tests per exit type), and stop values (4k tests per stop type and value). Similar to how Tableau handles dimensions and measures, we will be able to group our performance by each of these variables, but we will mainly focus on 5 exit types: SL exits, TS exits, TP exits, random exits, and holding exits (placed at the last bar).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-1-1)>>> cols = ["Open", "Low", "High", "Close", "Volume"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-1-2)>>> yfdata = vbt.YFData.pull(symbols, start=start_date, end=end_date)
 
[/code]

Symbol 10/10
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-2-1)>>> yfdata.data.keys()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-2-2)dict_keys(['BTC-USD', 'ETH-USD', 'XRP-USD', 'BCH-USD', 'LTC-USD', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-2-3) 'BNB-USD', 'EOS-USD', 'XLM-USD', 'XMR-USD', 'ADA-USD'])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-2-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-2-5)>>> yfdata.data["BTC-USD"].shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-2-6)(1096, 7)
 
[/code]

The data instance `yfdata` contains a dictionary with the OHLCV data by cryptocurrency name. Each DataFrame has 1096 rows (days) and 5 columns (O, H, L, C, and V). You can plot the DataFrame as follows:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-3-1)>>> yfdata.plot(symbol="BTC-USD").show() 
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/yfdata.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/yfdata.dark.svg#only-dark)

Since assets are one of the dimensions we want to analyze, vectorbt expects us to pack them as columns into a single DataFrame and label them accordingly. To do so, we simply swap assets and features to get a dictionary of DataFrames (with assets now as columns) keyed by feature name, such as "Open".
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-4-1)>>> ohlcv = yfdata.concat()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-4-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-4-3)>>> ohlcv.keys()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-4-4)dict_keys(['Open', 'High', 'Low', 'Close', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-4-5) 'Volume', 'Dividends', 'Stock Splits'])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-4-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-4-7)>>> ohlcv['Open'].shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-4-8)(1096, 10)
 
[/code]


# Time windows[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#time-windows "Permanent link")

Next, we will move a 6-month sliding window over the whole time period and take 400 "snapshots" of each price DataFrame within this window. Each snapshot will correspond to a subset of data that should be independently backtested. As with assets and other variables, snapshots also need to be stacked horizontally as columns. As a result, we will get 180 rows (window length in days) and 4000 columns (10 assets x 400 windows); that is, one column will correspond to the price of one asset within one particular time window.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-1)>>> splitter = vbt.Splitter.from_n_rolling( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-2)... ohlcv["Open"].index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-3)... n=window_cnt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-4)... length=window_len.days
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-7)>>> split_ohlcv = {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-8)>>> for k, v in ohlcv.items(): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-9)... split_ohlcv[k] = splitter.take(v, into="reset_stacked") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-10)>>> print(split_ohlcv["Open"].shape)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-11)(180, 4000)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-13)>>> split_indexes = splitter.take(ohlcv["Open"].index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-14)>>> print(split_indexes)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-15)split
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-16)0 DatetimeIndex(['2018-01-01 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-17)1 DatetimeIndex(['2018-01-03 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-18)2 DatetimeIndex(['2018-01-06 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-19)3 DatetimeIndex(['2018-01-08 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-20)4 DatetimeIndex(['2018-01-10 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-21) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-22)395 DatetimeIndex(['2020-06-26 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-23)396 DatetimeIndex(['2020-06-28 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-24)397 DatetimeIndex(['2020-06-30 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-25)398 DatetimeIndex(['2020-07-03 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-26)399 DatetimeIndex(['2020-07-05 00:00:00+00:00', '2...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-27)Length: 400, dtype: object
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-28)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-29)>>> print(split_indexes[10]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-30)DatetimeIndex(['2018-01-24 00:00:00+00:00', '2018-01-25 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-31) '2018-01-26 00:00:00+00:00', '2018-01-27 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-32) '2018-01-28 00:00:00+00:00', '2018-01-29 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-33) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-34) '2018-07-17 00:00:00+00:00', '2018-07-18 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-35) '2018-07-19 00:00:00+00:00', '2018-07-20 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-36) '2018-07-21 00:00:00+00:00', '2018-07-22 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-5-37) dtype='datetime64[ns, UTC]', name='Date', length=180, freq='D')
 
[/code]

 1. 2. 3. 4. 5. 

A nice feature of vectorbt is that it makes use of [hierarchical indexing](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html) to store valuable information on each backtest. It also ensures that this column hierarchy is preserved across the whole backtesting pipeline — from signal generation to performance modeling — and can be extended easily. Currently, our columns have the following hierarchy:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-1)>>> split_ohlcv["Open"].columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-2)MultiIndex([( 0, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-3) ( 0, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-4) ( 0, 'XRP-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-5) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-6) (399, 'XLM-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-7) (399, 'XMR-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-8) (399, 'ADA-USD')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-6-9) names=['split', 'symbol'], length=4000)
 
[/code]

This multi-index captures three parameters: the symbol, the start date of the time window, and its end date. Later, we will extend this multi-index with exit types and stop values such that each of the 2 million tests has its own price series.


# Entry signals[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#entry-signals "Permanent link")

In contrast to most other backtesting libraries, signals are not stored as a signed integer array, but they are split into two boolean arrays: entries and exits, which makes manipulation a lot easier. At the beginning of each time window, let's generate an entry signal indicating a buy order. The data frame will have the same shape, index, and columns as that of price so that vectorbt can link their elements together.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-7-1)>>> entries = pd.DataFrame.vbt.signals.empty_like(split_ohlcv["Open"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-7-2)>>> entries.iloc[0, :] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-7-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-7-4)>>> entries.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-7-5)(180, 4000)
 
[/code]


# Exit signals[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#exit-signals "Permanent link")

For each of the entry signals we generated, we will find an exit signal according to our 5 exit types: SL, TS, TP, random, and holding. We will also concatenate their DataFrames into a single (huge) DataFrame with 180 rows and 2,000,000 columns, each representing a separate backtest. Since exit signals are boolean, their memory footprint is tolerable.

Let's generate exit signals according to stop conditions first. We want to test 100 different stop values with a 1% increment, starting from 1% and ending with 100% (i.e., find a timestamp where the price exceeds the entry price by 100%). When OHLC data is checked against such conditions, the position is closed at (or shortly after) the time of hitting the particular stop.

Hint

We use [OHLCSTX](https://vectorbt.pro/pvt_7a467f6b/api/signals/generators/ohlcstx/#vectorbtpro.signals.generators.ohlcstx.OHLCSTX) instead of built-in stop-loss in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) because we want to analyze signals before simulation. Also, it's easier to construct param grids. For reality check, run the same setup using [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) alone.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-1)>>> sl_ohlcstx = vbt.OHLCSTX.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-2)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-3)... entry_price=split_ohlcv["Close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-4)... open=split_ohlcv["Open"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-5)... high=split_ohlcv["High"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-6)... low=split_ohlcv["Low"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-7)... close=split_ohlcv["Close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-8)... sl_stop=list(stops), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-9)... stop_type=None 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-11)>>> sl_exits = sl_ohlcstx.exits.copy() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-12)>>> sl_price = sl_ohlcstx.close.copy() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-13)>>> sl_price[sl_exits] = sl_ohlcstx.stop_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-14)>>> del sl_ohlcstx 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-16)>>> sl_exits.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-17)(180, 400000)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-19)>>> tsl_ohlcstx = vbt.OHLCSTX.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-20)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-21)... entry_price=split_ohlcv["Close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-22)... open=split_ohlcv["Open"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-23)... high=split_ohlcv["High"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-24)... low=split_ohlcv["Low"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-25)... close=split_ohlcv["Close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-26)... tsl_stop=list(stops),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-27)... stop_type=None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-28)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-29)>>> tsl_exits = tsl_ohlcstx.exits.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-30)>>> tsl_price = tsl_ohlcstx.close.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-31)>>> tsl_price[tsl_exits] = tsl_ohlcstx.stop_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-32)>>> del tsl_ohlcstx
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-33)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-34)>>> tsl_exits.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-35)(180, 400000)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-36)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-37)>>> tp_ohlcstx = vbt.OHLCSTX.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-38)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-39)... entry_price=split_ohlcv["Close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-40)... open=split_ohlcv["Open"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-41)... high=split_ohlcv["High"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-42)... low=split_ohlcv["Low"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-43)... close=split_ohlcv["Close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-44)... tp_stop=list(stops),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-45)... stop_type=None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-46)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-47)>>> tp_exits = tp_ohlcstx.exits.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-48)>>> tp_price = tp_ohlcstx.close.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-49)>>> tp_price[tp_exits] = tp_ohlcstx.stop_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-50)>>> del tp_ohlcstx
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-51)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-52)>>> tp_exits.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-8-53)(180, 400000)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

This also extended our column hierarchy with a new column level indicating the stop value, we only have to make it consistent across all DataFrames:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-1)>>> def rename_stop_level(df):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-2)... return df.vbt.rename_levels({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-3)... "ohlcstx_sl_stop": "stop_value",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-4)... "ohlcstx_tsl_stop": "stop_value",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-5)... "ohlcstx_tp_stop": "stop_value"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-6)... }, strict=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-8)>>> sl_exits = rename_stop_level(sl_exits)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-9)>>> tsl_exits = rename_stop_level(tsl_exits)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-10)>>> tp_exits = rename_stop_level(tp_exits)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-12)>>> sl_price = rename_stop_level(sl_price)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-13)>>> tsl_price = rename_stop_level(tsl_price)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-14)>>> tp_price = rename_stop_level(tp_price)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-16)>>> sl_exits.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-17)MultiIndex([(0.01, 0, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-18) (0.01, 0, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-19) (0.01, 0, 'XRP-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-20) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-21) ( 1.0, 399, 'XLM-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-22) ( 1.0, 399, 'XMR-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-23) ( 1.0, 399, 'ADA-USD')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-9-24) names=['stop_value', 'split', 'symbol'], length=400000)
 
[/code]

One major feature of vectorbt is that it places a strong focus on data science, and so it allows us to apply popular analysis tools to almost any part of the backtesting pipeline. For example, let's explore how the number of exit signals depends upon the stop type and value:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-1)>>> pd.Series({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-2)... "SL": sl_exits.vbt.signals.total().mean(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-3)... "TS": tsl_exits.vbt.signals.total().mean(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-4)... "TP": tp_exits.vbt.signals.total().mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-5)... }, name="avg_num_signals")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-6)SL 0.428585
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-7)TS 0.587100
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-8)TP 0.520042
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-9)Name: avg_num_signals, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-11)>>> def groupby_stop_value(df):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-12)... return df.vbt.signals.total().groupby("stop_value").mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-14)>>> pd.DataFrame({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-15)... "Stop Loss": groupby_stop_value(sl_exits),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-16)... "Trailing Stop": groupby_stop_value(tsl_exits),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-17)... "Take Profit": groupby_stop_value(tp_exits)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-18)... }).vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-19)... xaxis_title="Stop value", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-20)... yaxis_title="Avg number of signals"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-10-21)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/avg_num_signals.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/avg_num_signals.dark.svg#only-dark)

We see that TS is by far the most occurring exit signal. The SL and TP curves come hand in hand up to the stop value of 50% and then diverge in favor of TP. While it might seem that bulls are mostly in charge, especially for bigger price movements, remember that it is much easier to post a 50% profit than a 50% loss because the latter requires a 100% profit to recover; thus, negative downward spikes seem to dominate small to medium price movements (and shake out weak hands potentially). These are well-known cryptocurrency dynamics.

To simplify the analysis that follows, we should ensure that each column has at least one exit signal to close the position, which means that if a column has no exit signal now, it should get one at the last timestamp. This is done by combining the stop exits with the last-bar exit using the _OR_ rule and selecting the one that comes first:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-1)>>> sl_exits.iloc[-1, :] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-2)>>> tsl_exits.iloc[-1, :] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-3)>>> tp_exits.iloc[-1, :] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-5)>>> sl_exits = sl_exits.vbt.signals.first_after(entries) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-6)>>> tsl_exits = tsl_exits.vbt.signals.first_after(entries)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-7)>>> tp_exits = tp_exits.vbt.signals.first_after(entries)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-9)>>> pd.Series({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-10)... "SL": sl_exits.vbt.signals.total().mean(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-11)... "TS": tsl_exits.vbt.signals.total().mean(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-12)... "TP": tp_exits.vbt.signals.total().mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-13)... }, name="avg_num_signals")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-14)SL 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-15)TS 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-16)TP 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-11-17)Name: avg_num_signals, dtype: float64
 
[/code]

 1. 

Next, we will generate signals of the two remaining exit types: random and holding — they will act as benchmarks to compare SL, TS, and TP against.

"Holding" exit signals are signals placed at the very last bar of each time series. On most occasions, we shouldn't bother ourselves with placing them, since we can simply assess open positions. The reason we do it anyway is consistency — we want to ensure that each column has (exactly) one signal. The other consideration is shape and columns: they should match that of stop signals, so we can concatenate all DataFrames later.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-12-1)>>> hold_exits = pd.DataFrame.vbt.signals.empty_like(sl_exits)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-12-2)>>> hold_exits.iloc[-1, :] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-12-3)>>> hold_price = vbt.broadcast_to(split_ohlcv["Close"], sl_price)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-12-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-12-5)>>> hold_exits.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-12-6)(180, 400000)
 
[/code]

To generate random exit signals, just shuffle any signal array. The only requirement is that each column should contain exactly one signal.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-13-1)>>> rand_exits = hold_exits.vbt.shuffle(seed=seed) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-13-2)>>> rand_price = hold_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-13-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-13-4)>>> rand_exits.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-13-5)(180, 400000)
 
[/code]

 1. 

The last step is the concatenation of all DataFrames along the column axis and labeling them using a new column level `exit_type`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-1)>>> exits = pd.DataFrame.vbt.concat(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-2)... sl_exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-3)... tsl_exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-4)... tp_exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-5)... rand_exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-6)... hold_exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-7)... keys=pd.Index(exit_types, name="exit_type")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-9)>>> del sl_exits 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-10)>>> del tsl_exits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-11)>>> del tp_exits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-12)>>> del rand_exits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-13)>>> del hold_exits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-15)>>> exits.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-16)(180, 2000000)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-18)>>> price = pd.DataFrame.vbt.concat(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-19)... sl_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-20)... tsl_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-21)... tp_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-22)... rand_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-23)... hold_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-24)... keys=pd.Index(exit_types, name="exit_type")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-26)>>> del sl_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-27)>>> del tsl_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-28)>>> del tp_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-29)>>> del rand_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-30)>>> del hold_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-31)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-14-32)>>> price.shape
 
[/code]

 1. 

The `exits` array now contains 2,000,000 columns — one per backtest. The column hierarchy is also complete — one tuple of parameters per backtest.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-1)>>> exits.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-2)MultiIndex([( 'SL', 0.01, 0, 'BTC-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-3) ( 'SL', 0.01, 0, 'ETH-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-4) ( 'SL', 0.01, 0, 'XRP-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-5) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-6) ('Holding', 1.0, 399, 'XLM-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-7) ('Holding', 1.0, 399, 'XMR-USD'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-8) ('Holding', 1.0, 399, 'ADA-USD')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-9) names=['exit_type', 'stop_value', 'split', 'symbol'], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-15-10) length=2000000)
 
[/code]

Warning

One boolean array takes roughly 400 MB of RAM:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-16-1)>>> print(exits.vbt.getsize())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-16-2)390.0 MB
 
[/code]

One floating array takes roughly 3 GB of RAM:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-17-1)>>> print(price.vbt.getsize())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-17-2)2.9 GB
 
[/code]

This allows us to group signals by one or multiple levels and conveniently analyze them in one go. For example, let's compare different exit types and stop values by an average distance of exit signal to entry signal (in days):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-1)>>> avg_distance = entries.vbt.signals.between_ranges(target=exits)\ 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-2)... .duration.mean()\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-3)... .groupby(["exit_type", "stop_value"])\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-4)... .mean()\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-5)... .unstack(level="exit_type")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-7)>>> avg_distance.mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-8)exit_type
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-9)Holding 179.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-10)Random 89.432010
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-11)SL 124.686960
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-12)TP 113.887502
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-13)TS 104.159855
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-14)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-16)>>> avg_distance[exit_types].vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-17)... xaxis_title="Stop value", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-18)... yaxis_title="Avg distance to entry"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-18-19)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/avg_distance.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/avg_distance.dark.svg#only-dark)

This scatterplot gives us a more detailed view of the distribution of exit signals. As expected, exit signals of plain holding have an exact distance of 179 days after entry (maximum possible), while random exit signals are evenly distributed over the time window and are not dependent upon any stop value. But we are more interested in stop curves, which are flat and thus hint at high volatility of price movements within our timeframe — the lower the curve, the higher is the chance of hitting a stop. To give an example, a TS of 20% is hit after just 30 days on average, while it would take 72 days for SL and 81 days for TP. But does an early exit any good?


# Simulation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#simulation "Permanent link")

Here comes the actual backtesting part:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-1)>>> %%time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-2)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-3)... split_ohlcv["Close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-4)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-5)... exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-6)... price=price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-9)>>> len(pf.orders)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-10)3995570
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-11)CPU times: user 21.2 s, sys: 9.11 s, total: 30.3 s
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-19-12)Wall time: 51.5 s
 
[/code]

 1. 

Fairly easy, right?

The simulation took roughly 50 seconds on my Apple M1 to finish and generated in total 3,995,570 orders that are ready to be analyzed (should be 4 million, but some price data points seem to be missing). Notice, however, that any floating array produced by the portfolio object of the same shape as our exit signals, such as portfolio value or returns, requires 8 * 180 * 2000000 bytes or almost 3GB of RAM. We can analyze anything from trades to Sharpe ratio, but given the amount of data, we will stick to a fast-to-calculate metric — total return.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-20-1)>>> total_return = pf.total_return
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-20-2)>>> del pf 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-20-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-20-4)>>> total_return.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-20-5)(2000000,)
 
[/code]

 1. 

If your computer takes a substantial amount of time to simulate, you have several options:

 * Use [Google Colab](https://colab.research.google.com/)
 * Reduce the parameter space (e.g., lower the stop value granularity from 1% to 2%)
 * Use random search (e.g., pick a subset of columns randomly)
 * Cast to `np.float32` or even below (if supported)
 * Split the exit signal array into chunks and simulate per chunk. Just make sure each chunk has a shape compatible with that of the price and entries (remember to delete the previous portfolio if simulated):

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-1)>>> total_returns = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-2)>>> for i in vbt.ProgressBar(range(len(exit_types))): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-3)... exit_type_columns = exits.columns.get_level_values("exit_type")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-4)... chunk_mask = exit_type_columns == exit_types[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-5)... chunk_pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-6)... split_ohlcv["Close"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-7)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-8)... exits.loc[:, chunk_mask], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-9)... price=price.loc[:, chunk_mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-11)... total_returns.append(chunk_pf.total_return)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-12)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-13)... del chunk_pf
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-14)... vbt.flush() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-16)>>> total_return = pd.concat(total_returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-21-18)>>> total_return.shape
 
[/code]

 1. 2. 3. 

Chunk 5/5
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-22-1)>>> total_return = pd.concat(total_returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-22-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-22-3)>>> total_return.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-22-4)(2000000,)
 
[/code]

This approach has a similar execution time but is much healthier for memory.


# Performance[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#performance "Permanent link")

The first step is always taking a look at the distribution of the baseline:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-1)>>> return_by_type = total_return.unstack(level="exit_type")[exit_types]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-3)>>> return_by_type["Holding"].describe(percentiles=[])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-4)count 400000.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-5)mean 0.096940
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-6)std 0.833088
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-7)min -0.909251
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-8)50% -0.130475
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-9)max 6.565380
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-10)Name: Holding, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-12)>>> purple_color = vbt.settings["plotting"]["color_schema"]["purple"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-13)>>> return_by_type["Holding"].vbt.histplot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-14)... xaxis_title="Total return",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-15)... xaxis_tickformat=".2%",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-16)... yaxis_title="Count",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-17)... trace_kwargs=dict(marker_color=purple_color)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-23-18)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/holding_histplot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/holding_histplot.dark.svg#only-dark)

The distribution of holding performance across time windows is highly left-skewed. On the one hand, this indicates prolonged sideways and bearish regimes within our timeframe. On the other hand, the price of any asset can climb to infinity but is limited by 0 — making the distribution denser on the left and more sparse on the right by nature. Every second return is a loss of more than 6%, but thanks to bull runs the strategy still manages to post an average profit of 9%.

Let's include other strategies into the analysis:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-1)>>> pd.DataFrame({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-2)... "Mean": return_by_type.mean(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-3)... "Median": return_by_type.median(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-4)... "Std": return_by_type.std(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-5)... })
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-6) Mean Median Std
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-7)exit_type 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-8)SL 0.064957 -0.150000 0.771851
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-9)TS 0.068242 -0.084071 0.699093
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-10)TP 0.047264 0.088279 0.470234
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-11)Random 0.035533 -0.064302 0.581179
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-12)Holding 0.096940 -0.130475 0.833088
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-14)>>> return_by_type.vbt.boxplot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-15)... trace_kwargs=dict(boxpoints=False), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-16)... yaxis_title="Total return",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-17)... yaxis_tickformat=".2%"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-24-18)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/return_by_type.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/return_by_type.dark.svg#only-dark)

None of the strategies beat the average return of the baseline. The TP strategy is the most consistent one though — although it introduces an upper bound that limits huge profits (see missing outliers), its trade returns are less volatile and mostly positive. The reason why SL and TS are unbounded at the top is that some stops haven't been hit, and so their columns fall back to plain holding. The random strategy is also interesting: while it's inferior in terms of average return, it finishes second after TP in terms of median return and returns volatility.

To confirm the picture above, let's calculate the win rate of each strategy:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-25-1)>>> (return_by_type > 0).mean().rename("win_rate")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-25-2)exit_type
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-25-3)SL 0.311065
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-25-4)TS 0.375567
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-25-5)TP 0.598395
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-25-6)Random 0.417915
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-25-7)Holding 0.410250
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-25-8)Name: win_rate, dtype: float64
 
[/code]

Almost 60% of trades with TP are profitable — a high contrast to other strategies. But having a high win ratio doesn't necessarily guarantee longer-term trading success if your winning trades are often much smaller than your losing trades. Thus, let's aggregate by stop type and value and compute the [expectancy](https://www.icmarkets.com/blog/reward-to-risk-win-ratio-and-expectancy/):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-1)>>> init_cash = vbt.settings.portfolio["init_cash"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-3)>>> def get_expectancy(return_by_type, level_name):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-4)... grouped = return_by_type.groupby(level_name, axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-5)... win_rate = grouped.apply(lambda x: (x > 0).mean())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-6)... avg_win = grouped.apply(lambda x: init_cash * x[x > 0].mean())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-7)... avg_win = avg_win.fillna(0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-8)... avg_loss = grouped.apply(lambda x: init_cash * x[x < 0].mean())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-9)... avg_loss = avg_loss.fillna(0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-10)... return win_rate * avg_win - (1 - win_rate) * np.abs(avg_loss)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-12)>>> expectancy_by_stop = get_expectancy(return_by_type, "stop_value")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-14)>>> expectancy_by_stop.mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-15)exit_type
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-16)SL 6.495740
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-17)TS 6.824201
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-18)TP 4.726418
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-19)Random 3.388083
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-20)Holding 9.693974
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-21)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-22)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-23)>>> expectancy_by_stop.vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-24)... xaxis_title="Stop value", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-25)... yaxis_title="Expectancy"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-26-26)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/expectancy_by_stop.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/expectancy_by_stop.dark.svg#only-dark)

Each strategy is able to add gradually to our account in the long run, with the holding strategy being the clear winner here — we can expect to add to our account an average of almost $9 out of $100 invested after every 6 months of holding. The only configuration that beats the baseline is TS with stop values ranging from 20% to 40%. The worst-performing configuration is SL and TS with stop values around 45% and 60% respectively; both seem to get triggered once most corrections find the bottom, which is even worse than exiting randomly. The TP strategy, on the other hand, beats the random exit strategy after the stop value of 30%. Generally, waiting seems to pay off for cryptocurrencies.

Finally, let’s take a look at how our strategies perform under different market conditions. We will consider a simplified form of regime classification that divides holding returns into 20 bins and calculates the expectancy of each strategy within the boundaries of each bin (we leave out the latest bin for the sake of chart readability). Note that due to the highly skewed distribution of holding returns, we need to take into account the density of observations and make bins equally-sized.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-1)>>> return_values = np.sort(return_by_type["Holding"].values)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-2)>>> idxs = np.ceil(np.linspace(0, len(return_values) - 1, 21)).astype(int)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-3)>>> bins = return_values[idxs][:-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-5)>>> def bin_return(return_by_type):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-6)... classes = pd.cut(return_by_type["Holding"], bins=bins, right=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-7)... new_level = np.array(classes.apply(lambda x: x.right))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-8)... new_level = pd.Index(new_level, name="bin_right")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-9)... return return_by_type.vbt.add_levels(new_level, axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-11)>>> binned_return_by_type = bin_return(return_by_type)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-13)>>> expectancy_by_bin = get_expectancy(binned_return_by_type, "bin_right")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-15)>>> expectancy_by_bin.vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-16)... trace_kwargs=dict(mode="lines"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-17)... xaxis_title="Total return of holding",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-18)... xaxis_tickformat=".2%",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-19)... yaxis_title="Expectancy"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-27-20)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/expectancy_by_bin.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/stop-signals/expectancy_by_bin.dark.svg#only-dark)

The chart above confirms the general intuition behind the behavior of stop orders: SL and TS limit the trader’s loss during downtrends, TP is beneficial for short-term traders interested in profiting from a quick bump in price, and holding performs best in top-growth markets. Surprisingly, while random exits perform poorly in sideways and bull markets, they match and often outperform stop exits in bear markets.


# Bonus: Dashboard[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#bonus-dashboard "Permanent link")

Dashboards can be a really powerful way of interacting with the data.

First, let’s define the components of our dashboard. We have two types of components: controls, such as asset dropdown, and graphs. Controls define parameters and trigger updates for graphs.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-1)>>> range_starts = pd.DatetimeIndex(list(map(lambda x: x[0], split_indexes)))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-2)>>> range_ends = pd.DatetimeIndex(list(map(lambda x: x[-1], split_indexes)))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-4)>>> symbol_lvl = return_by_type.index.get_level_values("symbol")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-5)>>> split_lvl = return_by_type.index.get_level_values("split")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-6)>>> range_start_lvl = range_starts[split_lvl]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-7)>>> range_end_lvl = range_ends[split_lvl]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-9)>>> asset_multi_select = ipywidgets.SelectMultiple(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-10)... options=symbols,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-11)... value=symbols,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-12)... rows=len(symbols),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-13)... description="Symbols"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-15)>>> dates = np.unique(yfdata.wrapper.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-16)>>> date_range_slider = ipywidgets.SelectionRangeSlider(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-17)... options=dates,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-18)... index=(0, len(dates)-1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-19)... orientation="horizontal",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-20)... readout=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-21)... continuous_update=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-23)>>> range_start_label = ipywidgets.Label()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-24)>>> range_end_label = ipywidgets.Label()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-25)>>> metric_dropdown = ipywidgets.Dropdown(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-26)... options=["Mean", "Median", "Win Rate", "Expectancy"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-27)... value="Expectancy"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-28)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-29)>>> stop_scatter = vbt.Scatter(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-30)... trace_names=exit_types,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-31)... x_labels=stops, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-32)... xaxis_title="Stop value", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-33)... yaxis_title="Expectancy"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-34)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-35)>>> stop_scatter_img = ipywidgets.Image(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-36)... format="png",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-37)... width=stop_scatter.fig.layout.width,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-38)... height=stop_scatter.fig.layout.height
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-39)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-40)>>> bin_scatter = vbt.Scatter(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-41)... trace_names=exit_types,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-42)... x_labels=expectancy_by_bin.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-43)... trace_kwargs=dict(mode="lines"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-44)... xaxis_title="Total return of holding",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-45)... xaxis_tickformat="%",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-46)... yaxis_title="Expectancy"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-47)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-48)>>> bin_scatter_img = ipywidgets.Image(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-49)... format="png",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-50)... width=bin_scatter.fig.layout.width,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-51)... height=bin_scatter.fig.layout.height
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-28-52)... )
 
[/code]

The second step is the definition of the update function, which is triggered once any control has been changed. We also manually call this function to initialize the graphs with default parameters.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-1)>>> def update_scatter(*args, **kwargs):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-2)... _symbols = asset_multi_select.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-3)... _from = date_range_slider.value[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-4)... _to = date_range_slider.value[1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-5)... _metric_name = metric_dropdown.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-6)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-7)... range_mask = (range_start_lvl >= _from) & (range_end_lvl <= _to)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-8)... asset_mask = symbol_lvl.isin(_symbols)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-9)... filt = return_by_type[range_mask & asset_mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-10)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-11)... filt_binned = bin_return(filt)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-12)... if _metric_name == "Mean":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-13)... filt_metric = filt.groupby("stop_value").mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-14)... filt_bin_metric = filt_binned.groupby("bin_right").mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-15)... elif _metric_name == "Median":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-16)... filt_metric = filt.groupby("stop_value").median()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-17)... filt_bin_metric = filt_binned.groupby("bin_right").median()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-18)... elif _metric_name == "Win Rate":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-19)... filt_metric = (filt > 0).groupby("stop_value").mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-20)... filt_bin_metric = (filt_binned > 0).groupby("bin_right").mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-21)... elif _metric_name == "Expectancy":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-22)... filt_metric = get_expectancy(filt, "stop_value")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-23)... filt_bin_metric = get_expectancy(filt_binned, "bin_right")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-24)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-25)... stop_scatter.fig.update_layout(yaxis_title=_metric_name)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-26)... stop_scatter.update(filt_metric)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-27)... stop_scatter_img.value = stop_scatter.fig.to_image(format="png")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-28)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-29)... bin_scatter.fig.update_layout(yaxis_title=_metric_name)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-30)... bin_scatter.update(filt_bin_metric)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-31)... bin_scatter_img.value = bin_scatter.fig.to_image(format="png")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-32)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-33)... range_start_label.value = np.datetime_as_string(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-34)... _from.to_datetime64(), unit="D")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-35)... range_end_label.value = np.datetime_as_string(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-36)... _to.to_datetime64(), unit="D")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-37)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-38)>>> asset_multi_select.observe(update_scatter, names="value")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-39)>>> date_range_slider.observe(update_scatter, names="value")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-40)>>> metric_dropdown.observe(update_scatter, names="value")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-29-41)>>> update_scatter()
 
[/code]

In the last step, we will define the layout of the dashboard and finally run it:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-1)>>> dashboard = ipywidgets.VBox([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-2)... asset_multi_select,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-3)... ipywidgets.HBox([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-4)... range_start_label,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-5)... date_range_slider,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-6)... range_end_label
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-7)... ]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-8)... metric_dropdown,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-9)... stop_scatter_img,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-10)... bin_scatter_img
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-11)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#__codelineno-30-12)>>> dashboard
 
[/code]

 * **Dashboard**


* * *

Run the notebook to view the dashboard!


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals/#summary "Permanent link")

The use of large-scale backtesting is not limited to hyperparameter optimization, but when properly utilized, it gives us a vehicle to explore complex phenomena related to trading. Especially utilization of multidimensional arrays, dynamic compilation, and integration with pandas, as done by vectorbt, allows us to quickly get new insights by applying popular data science tools to each component of a backtesting pipeline.

In this particular example, we conducted 2 million tests to observe how different stop values impact the performance of stop signals and how different stop signals compare to holding and trading randomly. On the one hand, the findings confirm what we already know about the behavior of stop signals under various market conditions. On the other hand, they reveal optimal configurations that might have worked well for the last couple of years of trading cryptocurrencies.

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/stop-signals.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/StopSignals.ipynb)