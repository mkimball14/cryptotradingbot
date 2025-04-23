# Pairs trading[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#pairs-trading "Permanent link")

A pairs trading strategy is a statistical arbitrage and convergence strategy that is based on the historical correlation of two instruments and involves matching a long position with a short position. The two offsetting positions form the basis for a hedging strategy that seeks to benefit from either a positive or negative trend. A high positive correlation (mostly a minimum of 0.8) of both instruments is the primary driver behind the strategy's profits. Whenever the correlation eventually deviates, we would seek to buy the underperforming instrument and sell short the outperforming instrument. If the securities return to their historical correlation (which is what we bet on!), a profit is made from the convergence of the prices. Thus, pairs trading is used to generate profits regardless of any market condition: uptrend, downtrend, or sideways.


# Selection[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#selection "Permanent link")

When designing a pairs trading strategy, it is more important that the pairs are selected based on [cointegration](https://en.wikipedia.org/wiki/Cointegration) rather than just [correlation](https://en.wikipedia.org/wiki/Correlation). Correlated instruments tend to move in a similar way, but over time, the price ratio (or spread) between the two instruments might diverge considerably. Cointegrated instruments, on the other hand, don't necessarily always move in the same direction: the spread between them can on some days increase but the prices usually find themselves being "pulled back together" to the mean, which provides optimal conditions for pairs arbitrage trading.

The two workhorses of finding the cointegration are the Engle-Granger test and the Johansen test. We'll go with the former since its augmented version is implemented in [`statsmodels`](https://www.statsmodels.org/). The idea of Engle-Granger test is simple. We perform a linear regression between the two asset prices and check if the residual is stationary using the [Augmented Dick-Fuller (ADF) test](https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test). If the residual is stationary, then the two asset prices are cointegrated.

But first, let's build a universe of instruments to select our pairs from. For this, we will search for all the available USDT symbols on Binance and download their daily history. Instead of bulk-fetching all of them at once, we will fetch each symbol individually and append it to an HDF file. The reason behind such a separation is that most symbols have a limited history, and we don't want to waste much RAM by prolonging it with NaNs. We will also skip the entire procedure if the file already exists.

Note

Make sure to delete the HDF file if you want to re-fetch.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-3)>>> SYMBOLS = vbt.BinanceData.list_symbols("*USDT") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-4)>>> POOL_FILE = "temp/data_pool.h5"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-5)>>> START = "2018"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-6)>>> END = "2023"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-8)>>> # vbt.remove_dir("temp", with_contents=True, missing_ok=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-9)>>> vbt.make_dir("temp") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-11)>>> if not vbt.file_exists(POOL_FILE):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-12)... with vbt.ProgressBar(total=len(SYMBOLS)) as pbar: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-13)... collected = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-14)... for symbol in SYMBOLS:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-15)... try:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-16)... data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-17)... symbol, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-18)... start=START,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-19)... end=END,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-20)... show_progress=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-21)... silence_warnings=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-23)... data.to_hdf(POOL_FILE) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-24)... collected += 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-25)... except Exception:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-26)... pass
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-27)... pbar.set_prefix(f"{symbol} ({collected})") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-0-28)... pbar.update()
 
[/code]

 1. 2. 3. 4. 5. 

Symbol 423/423

The procedure took a while, but now we've got a file with the data distributed across keys. The great thing about working with HDF files (and VBT in particular!) is that we can import an entire file and join all the contained keys with a single command! 

But we need to do one more decision: which period should we analyze to select the optimal pair? What is really important here is to ensure that we don't use the same date range for both pairs selection and strategy backtesting since we would make ourselves vulnerable to a survivorship bias, thus let's reserve a more recent period of time for the backtesting part.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-1)>>> SELECT_START = "2020"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-2)>>> SELECT_END = "2021"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-4)>>> data = vbt.HDFData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-5)... POOL_FILE, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-6)... start=SELECT_START, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-7)... end=SELECT_END, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-8)... silence_warnings=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-11)>>> print(len(data.symbols))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-1-12)245
 
[/code]

We've imported 245 datasets, but some of these datasets are probably incomplete. In order for our analysis to be as seamless as possible, we should remove them.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-2-1)>>> data = data.select([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-2-2)... k 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-2-3)... for k, v in data.data.items() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-2-4)... if not v.isnull().any().any()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-2-5)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-2-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-2-7)>>> print(len(data.symbols))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-2-8)82
 
[/code]

A big chunk of our data has gone for good!

The next step is finding the pairs that satisfy our cointegration test. The methods for finding viable pairs all live on a spectrum. At the one end, we have some extra knowledge that leads us to believe that the pair is cointegrated, so we go out and test for the presence of cointegration. At the other end of the spectrum, we perform a search through hundreds of different instruments for any viable pairs according to our test. In this case, we may incur a multiple comparisons bias, which is an increased chance to incorrectly generate a significant p-value when many tests are run. For example, if 100 tests are run on a random data, we should expect to see 5 p-values below 0.05. In practice a second verification step would be needed if looking for pairs this way, which we will do later.

The test itself is performed with [`statsmodels.tsa.stattools.coint`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.coint.html). This function returns of tuple, the second element of which is the p-value of interest. But since testing each single pair would require going through `82 * 82` or 6,724 pairs and the `coint` function is not the fastest function of all, we'll parallelize the entire thing using [`pathos`](https://pathos.readthedocs.io/en/latest/index.html) ![⚡](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/26a1.svg)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-1)>>> @vbt.parameterized( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-2)... merge_func="concat", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-3)... engine="pathos",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-4)... distribute="chunks", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-5)... n_chunks="auto" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-7)... def coint_pvalue(close, s1, s2):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-8)... import statsmodels.tsa.stattools as ts 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-9)... import numpy as np
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-10)... return ts.coint(np.log(close[s1]), np.log(close[s2]))[1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-12)>>> COINT_FILE = "temp/coint_pvalues.pickle"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-14)>>> # vbt.remove_file(COINT_FILE, missing_ok=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-15)>>> if not vbt.file_exists(COINT_FILE):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-16)... coint_pvalues = coint_pvalue( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-17)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-18)... vbt.Param(data.symbols, condition="s1 != s2"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-19)... vbt.Param(data.symbols)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-20)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-21)... vbt.save(coint_pvalues, COINT_FILE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-22)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-3-23)... coint_pvalues = vbt.load(COINT_FILE)
 
[/code]

 1. 2. 3. 4. 5. 6. 

Hint

It's OK to analyze raw prices, but log prices are preferable.

The result is a Pandas Series where each pair of two symbols in the index is pointing to its p-value. If the p-value is small, below a critical size (< 0.05), then we can reject the hypothesis that there is no cointegrating relationship. Thus, let's arrange the p-values in increasing order:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-1)>>> coint_pvalues = coint_pvalues.sort_values()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-3)>>> print(coint_pvalues)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-4)s1 s2 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-5)TUSDUSDT BUSDUSDT 6.179128e-17
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-6)USDCUSDT BUSDUSDT 7.703666e-14
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-7)BUSDUSDT USDCUSDT 2.687508e-13
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-8)TUSDUSDT USDCUSDT 2.906244e-12
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-9)BUSDUSDT TUSDUSDT 1.853641e-11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-10) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-11)BTCUSDT XTZUSDT 1.000000e+00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-12) EOSUSDT 1.000000e+00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-13) ENJUSDT 1.000000e+00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-14) NKNUSDT 1.000000e+00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-15)ZILUSDT HBARUSDT 1.000000e+00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-4-16)Length: 6642, dtype: float64
 
[/code]

Coincidence that the most cointegrated pairs are stablecoins? Don't think so.

Remember about the multiple comparisons bias? Let's test the first bunch of pairs by plotting the charts below and ensuring that the difference between each pair of symbols bounces back and forth around its mean. For example, here's the analysis for the pair `(ALGOUSDT, QTUMUSDT)`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-5-1)>>> S1, S2 = "ALGOUSDT", "QTUMUSDT"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-5-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-5-3)>>> data.plot(column="Close", symbol=[S1, S2], base=1).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/rebased_price.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/rebased_price.dark.svg#only-dark)

The prices move together.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-6-1)>>> S1_log = np.log(data.get("Close", S1)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-6-2)>>> S2_log = np.log(data.get("Close", S2))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-6-3)>>> log_diff = (S2_log - S1_log).rename("Log diff")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-6-4)>>> fig = log_diff.vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-6-5)>>> fig.add_hline(y=log_diff.mean(), line_color="yellow", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-6-6)>>> fig.show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/price_log_diff.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/price_log_diff.dark.svg#only-dark)

The linear combination between them varies around the mean.


# Testing[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#testing "Permanent link")

The more data the better: let's re-fetch our pair's history but with a higher granularity.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-1)>>> DATA_FILE = "temp/data.pickle"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-3)>>> # vbt.remove_file(DATA_FILE, missing_ok=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-4)>>> if not vbt.file_exists(DATA_FILE):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-5)... data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-6)... [S1, S2], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-7)... start=SELECT_END, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-8)... end=END, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-9)... timeframe="hourly"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-11)... vbt.save(data, DATA_FILE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-12)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-13)... data = vbt.load(DATA_FILE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-15)>>> print(len(data.index))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-7-16)17507
 
[/code]

 1. 

Note

Make sure that none of the tickers were delisted.

We've got 17,507 data points for each symbol.


# Level: Researcher ![📡](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4e1.svg)[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#level-researcher "Permanent link")

Spread is the relative performance of both instruments. Whenever both instruments drift apart, the spread increases and may reach a certain threshold where we take a long position in the underperformer and a short position in the overachiever. Such a threshold is usually set to a number of standard deviations from the mean. All of that happens in a rolling fashion since the linear combination between both instruments is constantly changing. We'll use the prediction error of the [ordinary least squares (OLS)](https://en.wikipedia.org/wiki/Ordinary_least_squares), that is, the difference between the true and predicted value. Gladly, we have the [OLS](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/ols/#vectorbtpro.indicators.custom.ols.OLS) indicator, which can not only calculate the prediction error but also the z-score of that error:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-1)>>> import scipy.stats as st
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-3)>>> WINDOW = 24 * 30 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-4)>>> UPPER = st.norm.ppf(1 - 0.05 / 2) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-5)>>> LOWER = -st.norm.ppf(1 - 0.05 / 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-7)>>> S1_close = data.get("Close", S1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-8)>>> S2_close = data.get("Close", S2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-9)>>> ols = vbt.OLS.run(S1_close, S2_close, window=vbt.Default(WINDOW))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-10)>>> spread = ols.error.rename("Spread")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-11)>>> zscore = ols.zscore.rename("Z-score")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-12)>>> print(pd.concat((spread, zscore), axis=1))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-13) Spread Z-score
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-14)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-15)2021-01-01 00:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-16)2021-01-01 01:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-17)2021-01-01 02:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-18)2021-01-01 03:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-19)2021-01-01 04:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-20)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-21)2022-12-31 19:00:00+00:00 -0.121450 -1.066809
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-22)2022-12-31 20:00:00+00:00 -0.123244 -1.078957
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-23)2022-12-31 21:00:00+00:00 -0.122595 -1.070667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-24)2022-12-31 22:00:00+00:00 -0.125066 -1.088617
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-25)2022-12-31 23:00:00+00:00 -0.130532 -1.131498
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-26)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-8-27)[17507 rows x 2 columns]
 
[/code]

 1. 2. 

Let's plot the z-score, the two thresholds, and the points where the former crosses the latter:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-1)>>> upper_crossed = zscore.vbt.crossed_above(UPPER)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-2)>>> lower_crossed = zscore.vbt.crossed_below(LOWER)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-4)>>> fig = zscore.vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-5)>>> fig.add_hline(y=UPPER, line_color="orangered", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-6)>>> fig.add_hline(y=0, line_color="yellow", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-7)>>> fig.add_hline(y=LOWER, line_color="limegreen", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-8)>>> upper_crossed.vbt.signals.plot_as_exits(zscore, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-9)>>> lower_crossed.vbt.signals.plot_as_entries(zscore, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-9-10)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/zscore.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/zscore.dark.svg#only-dark)

If we look closely at the chart above, we'll notice many signals of the same type happening one after another. This is because of the price fluctuations that cause the price to repeatedly cross each threshold. This won't cause us any troubles if we use [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) as our simulation method of choice since it ignores any duplicate signals by default.

What's left is the construction of proper signal arrays. Remember that pairs trading involves two opposite positions that should be part of a single portfolio, that is, we need to transform our crossover signals into two arrays, long entries and short entries, with two columns each. Whenever there is an upper-threshold crossover signal, we will issue a short entry signal for the first asset and a long entry signal for the second one. Conversely, whenever there is a lower-threshold crossover signal, we will issue a long entry signal for the first asset and a short entry signal for the second one.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-1)>>> long_entries = data.symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-2)>>> short_entries = data.symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-4)>>> short_entries.loc[upper_crossed, S1] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-5)>>> long_entries.loc[upper_crossed, S2] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-6)>>> long_entries.loc[lower_crossed, S1] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-7)>>> short_entries.loc[lower_crossed, S2] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-9)>>> print(long_entries.sum())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-10)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-11)ALGOUSDT 52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-12)QTUMUSDT 73
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-13)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-14)>>> print(short_entries.sum())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-15)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-16)ALGOUSDT 73
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-17)QTUMUSDT 52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-10-18)dtype: int64
 
[/code]

It's time to simulate our configuration! Position size of the pair should be matched by dollar value rather than by the number of shares; this way a 5% move in one equals a 5% move in the other. To avoid running out of cash, we'll make the position size of each order dependent on the current equity. By the way, you might wonder why we are allowed to use [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) even though it doesn't support target size types? In pairs trading, a position is either opened or reversed (that is, closed out and opened again but with the opposite sign), such that we don't need to use target size types at all - regular size types would suffice.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-1)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-2)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-3)... entries=long_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-4)... short_entries=short_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-5)... size=10, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-6)... size_type="valuepercent100", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-7)... group_by=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-8)... cash_sharing=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-9)... call_seq="auto"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-11-10)... )
 
[/code]

 1. 2. 3. 

The simulation is completed. When working with grouped portfolios that involve some kind of rebalancing, we should always throw a look at the allocations first, for validation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-12-1)>>> fig = pf.plot_allocations()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-12-2)>>> rebalancing_dates = data.index[np.unique(pf.orders.idx.values)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-12-3)>>> for date in rebalancing_dates:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-12-4)... fig.add_vline(x=date, line_color="teal", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-12-5)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/from_signals_allocations.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/from_signals_allocations.dark.svg#only-dark)

The chart makes sense: positions of both symbols are continuously switching as if we're looking at a chess board. Also, the long and short allocations rarely go beyond the specified position size of 10%. Next, we should calculate the portfolio statistics to assess the profitability of our strategy:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-1)>>> pf.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-2)Start 2021-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-3)End 2022-12-31 23:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-4)Period 729 days 11:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-5)Start Value 100.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-6)Min Value 96.401924
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-7)Max Value 127.670782
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-8)End Value 119.930329
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-9)Total Return [%] 19.930329
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-10)Benchmark Return [%] -34.051206
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-11)Total Time Exposure [%] 89.946878
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-12)Max Gross Exposure [%] 12.17734
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-13)Max Drawdown [%] 8.592299
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-14)Max Drawdown Duration 318 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-15)Total Orders 34
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-16)Total Fees Paid 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-17)Total Trades 34
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-18)Win Rate [%] 43.75
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-19)Best Trade [%] 160.511614
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-20)Worst Trade [%] -54.796964
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-21)Avg Winning Trade [%] 41.851493
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-22)Avg Losing Trade [%] -20.499826
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-23)Avg Winning Trade Duration 42 days 22:04:17.142857143
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-24)Avg Losing Trade Duration 33 days 14:43:20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-25)Profit Factor 1.553538
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-26)Expectancy 0.713595
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-27)Sharpe Ratio 0.782316
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-28)Calmar Ratio 1.10712
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-29)Omega Ratio 1.034258
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-30)Sortino Ratio 1.221721
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-13-31)Name: group, dtype: object
 
[/code]

We're up by almost 20% from the initial portfolio value - a comfortable win considering that the benchmark is down by almost 35%. As expected, the amount of time our portfolio was in any position is 90%; the only time we were not in a position is the initial period before the first signal. Also, even though the win rate is below 50%, we made a profit because the average trade brings 50% more profit than loss, which leads us to a long-term profit of $0.70 per trade.

But can we somehow prove that the simulation closely resembles the signals it's based upon? For this, we can reframe our problem into a portfolio optimization problem: we can mark the points where the z-score crosses any of the thresholds as allocation points, and appoint the corresponding weights at these points. All of this is a child's play using [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-1)>>> allocations = data.symbol_wrapper.fill() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-2)>>> allocations.loc[upper_crossed, S1] = -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-3)>>> allocations.loc[upper_crossed, S2] = 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-4)>>> allocations.loc[lower_crossed, S1] = 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-5)>>> allocations.loc[lower_crossed, S2] = -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-6)>>> pfo = vbt.PortfolioOptimizer.from_filled_allocations(allocations)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-8)>>> print(pfo.allocations) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-9)symbol ALGOUSDT QTUMUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-10)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-11)2021-03-15 10:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-12)2021-03-23 03:00:00+00:00 -0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-13)2021-04-17 14:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-14)2021-04-19 00:00:00+00:00 -0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-15)2021-06-03 16:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-16)2021-06-30 22:00:00+00:00 -0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-17)2021-08-19 06:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-18)2021-10-02 21:00:00+00:00 -0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-19)2021-11-12 03:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-20)2022-02-02 09:00:00+00:00 -0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-21)2022-04-28 21:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-22)2022-07-22 02:00:00+00:00 -0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-23)2022-09-04 01:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-24)2022-09-27 03:00:00+00:00 -0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-25)2022-10-13 10:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-26)2022-10-23 19:00:00+00:00 -0.1 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-27)2022-11-08 20:00:00+00:00 0.1 -0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-28)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-14-29)>>> pfo.plot().show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/optimizer.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/optimizer.dark.svg#only-dark)

There's also a handy method to simulate the optimizer:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-15-1)>>> pf = pfo.simulate(data, pf_method="from_signals")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-15-2)>>> pf.total_return
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-15-3)0.19930328736504038
 
[/code]

Info

This method is based on a dynamic signal function that translates target percentages into signals, thus the compilation may take up to a minute (once compiled, it will be ultrafast though). You can also remove the `pf_method` argument to use the cacheable [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) with similar results.

What about parameter optimization? There are several places in the code that can be parameterized. The signal generation part is affected by the parameters `WINDOW`, `UPPER`, and `LOWER`. The simulation part can be tweaked more freely; for example, we can add stops to limit our exposure to unfortunate price movements. Let's do the former part first. 

The main issue that we may come across is the combination of the two parameters `UPPER` and `LOWER`: we cannot just pass them to their respective crossover functions and hope for the best; we need to unify the columns that they produce to combine them later. One trick is to build a meta-indicator that encapsulates other indicators and deals with multiple parameter combinations out of the box:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-1)>>> PTS_expr = """
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-2)... PTS:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-3)... x = @in_close.iloc[:, 0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-4)... y = @in_close.iloc[:, 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-5)... ols = vbt.OLS.run(x, y, window=@p_window, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-6)... upper = st.norm.ppf(1 - @p_upper_alpha / 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-7)... lower = -st.norm.ppf(1 - @p_lower_alpha / 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-8)... upper_crossed = ols.zscore.vbt.crossed_above(upper)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-9)... lower_crossed = ols.zscore.vbt.crossed_below(lower)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-10)... long_entries = wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-11)... short_entries = wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-12)... short_entries.loc[upper_crossed, x.name] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-13)... long_entries.loc[upper_crossed, y.name] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-14)... long_entries.loc[lower_crossed, x.name] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-15)... short_entries.loc[lower_crossed, y.name] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-16)... long_entries, short_entries
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-17)... """
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-19)>>> PTS = vbt.IF.from_expr(PTS_expr, keep_pd=True, st=st) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-20)>>> vbt.phelp(PTS.run) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-21)PTS.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-22) close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-23) window,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-24) upper_alpha,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-25) lower_alpha,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-26) short_name='pts',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-27) hide_params=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-28) hide_default=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-29) **kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-30)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-31) Run `PTS` indicator.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-32)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-33) * Inputs: `close`
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-34) * Parameters: `window`, `upper_alpha`, `lower_alpha`
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-16-35) * Outputs: `long_entries`, `short_entries`
 
[/code]

 1. 2. 

Our goal was to create an indicator that takes an input array with two columns (i.e., assets), executes our pipeline, and returns two signals arrays with two columns each. For this, we have constructed an expression that is a regular Python code but with useful enhancements. For example, we have specified that the variable `close` is an input array by prepending to it the prefix `@in_`. Also, we have annotated the three parameters `window`, `upper_alpha`, and `lower_alpha` by prepending to them the prefix `@p_`. Later, when the expression is run, the indicator factory will replace `@in_close` by our close price and `@p_window`, `@p_upper_alpha`, and `@p_lower_alpha` by our parameter values. Moreover, the factory will recognize the widely-understood variables `vbt` and `wrapper` and replace them by the vectorbt module and the current Pandas wrapper respectively. The last line consists of the variables that we want to return, their names will be used as output names automatically.

Let's run this indicator on a grid of parameter combinations we want to test. But beware of wide parameter grids and potential out-of-memory errors: each parameter combination will build multiple arrays of the same shape as the data, thus use random search to effectively reduce the number of parameter combinations.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-1)>>> WINDOW_SPACE = np.arange(5, 50).tolist() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-2)>>> ALPHA_SPACE = (np.arange(1, 100) / 1000).tolist() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-4)>>> long_entries, short_entries = data.run( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-5)... PTS, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-6)... window=WINDOW_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-7)... upper_alpha=ALPHA_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-8)... lower_alpha=ALPHA_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-9)... param_product=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-10)... random_subset=1000, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-11)... seed=42, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-12)... unpack=True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-14)>>> print(long_entries.columns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-15)MultiIndex([( 5, 0.007, 0.09, 'ALGOUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-16) ( 5, 0.007, 0.09, 'QTUMUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-17) ( 5, 0.009, 0.086, 'ALGOUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-18) ( 5, 0.009, 0.086, 'QTUMUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-19) ( 5, 0.015, 0.082, 'ALGOUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-20) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-21) (49, 0.091, 0.094, 'QTUMUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-22) (49, 0.094, 0.054, 'ALGOUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-23) (49, 0.094, 0.054, 'QTUMUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-24) (49, 0.095, 0.074, 'ALGOUSDT'),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-25) (49, 0.095, 0.074, 'QTUMUSDT')],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-17-26) names=['pts_window', 'pts_upper_alpha', 'pts_lower_alpha', 'symbol'], length=2000)
 
[/code]

 1. 2. 3. 4. 5. 6. 

We took a data instance and told it to introspect the indicator `PTS`, find its input names among the arrays stored in the data instance, and pass the arrays along with the parameters to the indicator. This way, we don't have to deal with input and output names at all ![🎉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f389.svg)

So, which parameter combinations are the most profitable?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-1)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-2)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-3)... entries=long_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-4)... short_entries=short_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-5)... size=10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-6)... size_type="valuepercent100",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-7)... group_by=vbt.ExceptLevel("symbol"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-8)... cash_sharing=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-9)... call_seq="auto"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-12)>>> opt_results = pd.concat((
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-13)... pf.total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-14)... pf.trades.expectancy,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-15)... ), axis=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-16)>>> print(opt_results.sort_values(by="total_return", ascending=False))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-17) total_return expectancy
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-18)pts_window pts_upper_alpha pts_lower_alpha 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-19)41 0.076 0.001 0.503014 0.399218
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-20)15 0.079 0.001 0.489249 2.718049
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-21)16 0.023 0.016 0.474538 0.104986
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-22)6 0.078 0.048 0.445623 0.057574
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-23)41 0.028 0.001 0.441388 0.387182
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-24)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-25)43 0.003 0.004 -0.263967 -0.131984
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-26)15 0.002 0.049 -0.273170 -0.182113
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-27)42 0.002 0.036 -0.316947 -0.110821
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-28)35 0.001 0.008 -0.330056 -0.196462
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-29)41 0.001 0.015 -0.363547 -0.191341
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-18-31)[1000 rows x 2 columns]
 
[/code]

 1. 

Now, let's do the second optimization part by picking one parameter combination from above and testing various stop configurations using [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-1)>>> best_index = opt_results.idxmax()["expectancy"] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-2)>>> best_long_entries = long_entries[best_index]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-3)>>> best_short_entries = short_entries[best_index]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-4)>>> STOP_SPACE = [np.nan] + np.arange(1, 100).tolist() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-6)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-7)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-8)... entries=best_long_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-9)... short_entries=best_short_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-10)... size=10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-11)... size_type="valuepercent100",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-12)... group_by=vbt.ExceptLevel("symbol"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-13)... cash_sharing=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-14)... call_seq="auto",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-15)... sl_stop=vbt.Param(STOP_SPACE), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-16)... tsl_stop=vbt.Param(STOP_SPACE),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-17)... tp_stop=vbt.Param(STOP_SPACE),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-18)... delta_format="percent100", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-19)... stop_exit_price="close", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-20)... broadcast_kwargs=dict(random_subset=1000, seed=42) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-21)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-22)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-23)>>> opt_results = pd.concat((
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-24)... pf.total_return,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-25)... pf.trades.expectancy,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-26)... ), axis=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-27)>>> print(opt_results.sort_values(by="total_return", ascending=False))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-28) total_return expectancy
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-29)sl_stop tsl_stop tp_stop 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-30)86.0 98.0 NaN 0.602834 2.740152
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-31)47.0 62.0 NaN 0.587525 1.632014
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-32)43.0 90.0 NaN 0.579859 1.757150
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-33)16.0 62.0 54.0 0.412477 0.448345
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-34)2.0 95.0 71.0 0.406624 0.125115
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-35)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-36)27.0 41.0 20.0 -0.063945 -0.046337
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-37)52.0 46.0 20.0 -0.065675 -0.067706
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-38)23.0 61.0 22.0 -0.071294 -0.057495
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-39)6.0 57.0 31.0 -0.080679 -0.029232
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-40)23.0 45.0 22.0 -0.090643 -0.073099
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-41)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-19-42)[1000 rows x 2 columns]
 
[/code]

 1. 2. 3. 4. 5. 6. 

We can also observe how the performance degrades with lower SL and TSL, and how the optimizer wants to discourage us from using TP at all. Let's take a closer look how a metric of interest depends on the values of each stop type:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-1)>>> def plot_metric_by_stop(stop_name, metric_name, stat_name, smooth):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-2)... from scipy.signal import savgol_filter
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-3)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-4)... values = pf.deep_getattr(metric_name) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-5)... values = values.vbt.select_levels(stop_name) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-6)... values = getattr(values.groupby(values.index), stat_name)() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-7)... smooth_values = savgol_filter(values, smooth, 1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-8)... smooth_values = values.vbt.wrapper.wrap(smooth_values) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-9)... fig = values.rename(metric_name).vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-10)... smooth_values.rename(f"{metric_name} (smoothed)").vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-11)... trace_kwargs=dict(line=dict(dash="dot", color="yellow")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-12)... fig=fig, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-20-14)... return fig
 
[/code]

 1. 2. 3. 4. 5. 

SLTSLTP
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-21-1)>>> plot_metric_by_stop(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-21-2)... "sl_stop", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-21-3)... "trades.expectancy", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-21-4)... "median",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-21-5)... 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-21-6)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/SL.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/SL.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-22-1)>>> plot_metric_by_stop(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-22-2)... "tsl_stop", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-22-3)... "trades.expectancy", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-22-4)... "median",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-22-5)... 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-22-6)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/TSL.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/TSL.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-23-1)>>> plot_metric_by_stop(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-23-2)... "tp_stop", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-23-3)... "trades.expectancy", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-23-4)... "median",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-23-5)... 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-23-6)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/TP.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/TP.dark.svg#only-dark)

We've got an abstract picture of how stop orders affect the strategy performance.


# Level: Engineer ![🛰](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f6f0.svg)[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#level-engineer "Permanent link")

The approach we followed above works great if we're still in the phase of strategy discovery; Pandas and the vectorbt's high-level API allow us to experiment rapidly and with ease. But as soon as we have finished developing a general framework for our strategy, we should start focusing on optimizing the strategy for best CPU and memory performance in order to be able to test the strategy on more assets, periods, and parameter combinations. Previously, we could test multiple parameter combinations by putting them all into memory; the only reason why we hadn't any issues running them is because we made use of random search. But let's do the parameter search more practical by increasing the speed of our backtests on the one side, and decreasing the memory consumption on the other.

Let's start by rewriting our indicator strictly with Numba:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-1)>>> @njit(nogil=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-2)... def pt_signals_nb(close, window=WINDOW, upper=UPPER, lower=LOWER):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-3)... x = np.expand_dims(close[:, 0], 1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-4)... y = np.expand_dims(close[:, 1], 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-5)... _, _, zscore = vbt.ind_nb.ols_nb(x, y, window) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-6)... zscore_1d = zscore[:, 0] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-7)... upper_ts = np.full_like(zscore_1d, upper, dtype=float_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-8)... lower_ts = np.full_like(zscore_1d, lower, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-9)... upper_crossed = vbt.nb.crossed_above_1d_nb(zscore_1d, upper_ts) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-10)... lower_crossed = vbt.nb.crossed_above_1d_nb(lower_ts, zscore_1d) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-11)... long_entries = np.full_like(close, False, dtype=np.bool_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-12)... short_entries = np.full_like(close, False, dtype=np.bool_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-13)... short_entries[upper_crossed, 0] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-14)... long_entries[upper_crossed, 1] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-15)... long_entries[lower_crossed, 0] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-16)... short_entries[lower_crossed, 1] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-24-17)... return long_entries, short_entries
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 

Below we are ensuring that the indicator produces the same number of signals as previously:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-1)>>> long_entries, short_entries = pt_signals_nb(data.close.values) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-2)>>> long_entries = data.symbol_wrapper.wrap(long_entries) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-3)>>> short_entries = data.symbol_wrapper.wrap(short_entries)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-5)>>> print(long_entries.sum())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-6)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-7)ALGOUSDT 52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-8)QTUMUSDT 73
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-9)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-10)>>> print(short_entries.sum())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-11)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-12)ALGOUSDT 73
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-13)QTUMUSDT 52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-25-14)dtype: int64
 
[/code]

 1. 2. 

Perfect alignment.

Even though this function is faster than the expression-based one, it doesn't address the memory issue because the output arrays it generates must still reside in memory to be later passed to the simulator, especially when multiple parameter combinations should be run. What we can do though is to wrap both the signal generation part and the simulation part into the same pipeline, and make it return lightweight arrays such as the total return. By using a proper chunking approach, we could then run an almost infinite number of parameter combinations! ![🪁](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1fa81.svg)

The next step is rewriting the simulation part with Numba:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-2)... def pt_portfolio_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-3)... open, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-4)... high, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-5)... low, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-6)... close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-7)... long_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-8)... short_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-9)... sl_stop=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-10)... tsl_stop=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-11)... tp_stop=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-12)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-13)... target_shape = close.shape 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-14)... group_lens = np.array([2]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-15)... sim_out = vbt.pf_nb.from_signals_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-16)... target_shape=target_shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-17)... group_lens=group_lens,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-18)... auto_call_seq=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-19)... open=open,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-20)... high=high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-21)... low=low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-22)... close=close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-23)... long_entries=long_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-24)... short_entries=short_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-25)... size=10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-26)... size_type=vbt.pf_enums.SizeType.ValuePercent100, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-27)... sl_stop=sl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-28)... tsl_stop=tsl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-29)... tp_stop=tp_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-30)... delta_format=vbt.pf_enums.DeltaFormat.Percent100,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-31)... stop_exit_price=vbt.pf_enums.StopExitPrice.Close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-32)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-26-33)... return sim_out
 
[/code]

 1. 2. 3. 4. 5. 

Let's run it:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-27-1)>>> sim_out = pt_portfolio_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-27-2)... data.open.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-27-3)... data.high.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-27-4)... data.low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-27-5)... data.close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-27-6)... long_entries.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-27-7)... short_entries.values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-27-8)... )
 
[/code]

The output of this function is an instance of the type [SimulationOutput](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.SimulationOutput), which can be used to construct a new [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) instance for analysis:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-1)>>> pf = vbt.Portfolio(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-2)... data.symbol_wrapper.regroup(group_by=True), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-3)... sim_out, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-4)... open=data.open, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-5)... high=data.high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-6)... low=data.low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-7)... close=data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-8)... cash_sharing=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-9)... init_cash=100 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-12)>>> print(pf.total_return)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-28-13)0.19930328736504038
 
[/code]

 1. 2. 3. 4. 

What's missing is a Numba-compiled version of the analysis part:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-2)... def pt_metrics_nb(close, sim_out):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-3)... target_shape = close.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-4)... group_lens = np.array([2])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-5)... filled_close = vbt.nb.fbfill_nb(close) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-6)... col_map = vbt.rec_nb.col_map_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-7)... col_arr=sim_out.order_records["col"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-8)... n_cols=target_shape[1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-10)... total_profit = vbt.pf_nb.total_profit_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-11)... target_shape=target_shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-12)... close=filled_close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-13)... order_records=sim_out.order_records,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-14)... col_map=col_map
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-16)... total_profit_grouped = vbt.pf_nb.total_profit_grouped_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-17)... total_profit=total_profit,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-18)... group_lens=group_lens,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-19)... )[0] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-20)... total_return = total_profit_grouped / 100 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-21)... trade_records = vbt.pf_nb.get_exit_trades_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-22)... order_records=sim_out.order_records, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-23)... close=filled_close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-24)... col_map=col_map
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-26)... trade_records = trade_records[ 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-27)... trade_records["status"] == vbt.pf_enums.TradeStatus.Closed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-28)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-29)... expectancy = vbt.pf_nb.expectancy_reduce_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-30)... pnl_arr=trade_records["pnl"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-31)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-29-32)... return total_return, expectancy
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 

Don't let this function frighten you! We were able to calculate our metrics based on the close price and order records alone - the process which is also called a "reconstruction". The principle behind it is simple: start with information that you want to gain (a metric, for example) and see which information it requires. Then, find a function that provides that information, and repeat.

Let's run it for validation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-30-1)>>> pt_metrics_nb(data.close.values, sim_out)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-30-2)(0.19930328736504038, 0.7135952049405152)
 
[/code]

100% accuracy.

Finally, we'll put all parts into the same pipeline and benchmark it:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-2)... def pt_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-3)... open, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-4)... high, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-5)... low, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-6)... close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-7)... window=WINDOW, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-8)... upper=UPPER,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-9)... lower=LOWER,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-10)... sl_stop=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-11)... tsl_stop=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-12)... tp_stop=np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-13)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-14)... long_entries, short_entries = pt_signals_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-15)... close, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-16)... window=window, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-17)... upper=upper, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-18)... lower=lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-19)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-20)... sim_out = pt_portfolio_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-21)... open,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-22)... high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-23)... low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-24)... close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-25)... long_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-26)... short_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-27)... sl_stop=sl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-28)... tsl_stop=tsl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-29)... tp_stop=tp_stop
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-30)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-31)... return pt_metrics_nb(close, sim_out)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-32)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-33)>>> pt_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-34)... data.open.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-35)... data.high.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-36)... data.low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-37)... data.close.values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-38)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-39)(0.19930328736504038, 0.7135952049405152)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-40)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-41)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-42)... pt_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-43)... data.open.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-44)... data.high.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-45)... data.low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-46)... data.close.values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-47)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-31-48)5.4 ms ± 13.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 
[/code]

 1. 

Just 5 milliseconds per complete backtest ![🔥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f525.svg)

This kind of performance invites us to try some hard-core parameter optimization. Luckily for us, there are multiple ways we can implement that. The first and the most convenient way is to wrap the pipeline with the [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized) decorator, which takes care of building the parameter grid and calling the pipeline function on each parameter combination from that grid. Also, because each of our Numba functions releases the GIL, we can finally utilize multithreading! Let's test all parameter combinations related to signal generation by dividing them into chunks and distributing the combinations within each chunk, which took me 5 minutes on Apple Silicon:

Important

Remember that `@parameterized` builds the entire parameter grid even if a random subset was specified, which may take a significant amount of time. For example, 6 parameters with 100 values each will build a grid of `100 ** 6`, or one trillion combinations - too many to combine.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-1)>>> param_pt_pipeline = vbt.parameterized( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-2)... pt_pipeline_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-3)... merge_func="concat", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-4)... seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-5)... engine="threadpool", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-6)... chunk_len="auto"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-9)>>> UPPER_SPACE = [st.norm.ppf(1 - x / 2) for x in ALPHA_SPACE] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-10)>>> LOWER_SPACE = [-st.norm.ppf(1 - x / 2) for x in ALPHA_SPACE]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-11)>>> POPT_FILE = "temp/param_opt.pickle"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-13)>>> # vbt.remove_file(POPT_FILE, missing_ok=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-14)>>> if not vbt.file_exists(POPT_FILE):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-15)... param_opt = param_pt_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-16)... data.open.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-17)... data.high.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-18)... data.low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-19)... data.close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-20)... window=vbt.Param(WINDOW_SPACE),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-21)... upper=vbt.Param(UPPER_SPACE),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-22)... lower=vbt.Param(LOWER_SPACE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-23)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-24)... vbt.save(param_opt, POPT_FILE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-25)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-26)... param_opt = vbt.load(POPT_FILE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-27)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-32-28)>>> total_return, expectancy = param_opt 
 
[/code]

 1. 2. 3. 4. 5. 

Chunk 55131/55131

Let's analyze the total return:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-1)>>> print(total_return)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-2)window upper lower 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-3)5 3.290527 -3.290527 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-4) -3.090232 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-5) -2.967738 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-6) -2.878162 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-7) -2.807034 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-8) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-9)49 1.649721 -1.669593 0.196197
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-10) -1.664563 0.192152
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-11) -1.659575 0.190713
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-12) -1.654628 0.201239
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-13) -1.649721 0.204764
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-14)Length: 441045, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-16)>>> grouped_metric = total_return.groupby(level=["upper", "lower"]).mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-17)>>> grouped_metric.vbt.heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-18)... trace_kwargs=dict(colorscale="RdBu", zmid=0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-19)... yaxis=dict(autorange="reversed")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-33-20)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/popt_total_return.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/popt_total_return.dark.svg#only-dark)

The effect of the thresholds seems to be asymmetric: we can register the highest total return for the lowest upper threshold and the lowest lower threshold, such that the neutral range between the two thresholds is basically shifted downwards to the maximum extent.

The `@parameterized` decorator has two major limitations though: it runs only one parameter combination at a time, and it needs to build the parameter grid fully, even when querying a random subset. Why is the former a limitation at all? Because we can parallelize only a bunch of pipeline calls at a time: even though there's a special argument `distribute="chunks"` using which we can parallelize entire chunks, the calls within those chunks happen serially using a regular Python loop - bad for multithreading, which requires the GIL to be released for the **entire** procedure. And if you come to the idea of using multiprocessing: the method will have to serialize all the arguments (including the data) each time the pipeline is called, which is a huge overhead, but it may still result in some speedup compared to the approach above.

To process multiple parameter combinations within each thread, we need to split them into chunks and write a parent Numba function that processes the combinations of each chunk in a loop. We can then parallelize this parent function using multithreading. So, we need to: 1) construct the parameter grid manually, 2) split it into chunks, and 3) iterate over the chunks and pass each one to the parent function for execution. The first step can be done using [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params), which is the ![🫀](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1fac0.svg) of the `@parameterized` decorator. The second and third steps can be done using another decorator - [@chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked), which is specialized in argument chunking. Let's do that! ![💪](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4aa.svg)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-2)... def pt_pipeline_mult_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-3)... n_params: int, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-4)... open: tp.Array2d, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-5)... high: tp.Array2d, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-6)... low: tp.Array2d, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-7)... close: tp.Array2d,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-8)... window: tp.FlexArray1dLike = WINDOW, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-9)... upper: tp.FlexArray1dLike = UPPER,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-10)... lower: tp.FlexArray1dLike = LOWER,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-11)... sl_stop: tp.FlexArray1dLike = np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-12)... tsl_stop: tp.FlexArray1dLike = np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-13)... tp_stop: tp.FlexArray1dLike = np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-14)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-15)... window_ = vbt.to_1d_array_nb(np.asarray(window)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-16)... upper_ = vbt.to_1d_array_nb(np.asarray(upper))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-17)... lower_ = vbt.to_1d_array_nb(np.asarray(lower))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-18)... sl_stop_ = vbt.to_1d_array_nb(np.asarray(sl_stop))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-19)... tsl_stop_ = vbt.to_1d_array_nb(np.asarray(tsl_stop))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-20)... tp_stop_ = vbt.to_1d_array_nb(np.asarray(tp_stop))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-21)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-22)... total_return = np.empty(n_params, dtype=float_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-23)... expectancy = np.empty(n_params, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-24)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-25)... for i in range(n_params): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-26)... total_return[i], expectancy[i] = pt_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-27)... open,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-28)... high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-29)... low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-30)... close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-31)... window=vbt.flex_select_1d_nb(window_, i), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-32)... upper=vbt.flex_select_1d_nb(upper_, i),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-33)... lower=vbt.flex_select_1d_nb(lower_, i),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-34)... sl_stop=vbt.flex_select_1d_nb(sl_stop_, i),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-35)... tsl_stop=vbt.flex_select_1d_nb(tsl_stop_, i),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-36)... tp_stop=vbt.flex_select_1d_nb(tp_stop_, i),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-37)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-34-38)... return total_return, expectancy
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

The magic of the function above is that we don't need to make arrays out of all parameters: thanks to flexible indexing, we can pass some parameters as arrays, and keep some at their defaults. For example, let's test three window combinations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-1)>>> pt_pipeline_mult_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-2)... 3,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-3)... data.open.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-4)... data.high.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-5)... data.low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-6)... data.close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-7)... window=np.array([10, 20, 30])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-9)(array([ 0.11131525, -0.04819178, 0.13124959]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-35-10) array([ 0.01039436, -0.00483853, 0.01756337]))
 
[/code]

Next, we'll wrap the function with the `@chunked` decorator. Not only we need to specify the chunks as we did in `@parameterized`, but we also need to specify where to get the total number of parameter combinations from, and how to split each single argument. To assist us in this matter, vectorbt has its own collection of annotation classes. For instance, we can instruct `@chunked` to take the total number of combinations from the argument `n_params` by annotating this argument with the class [ArgSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer). Then, we can annotate each parameter as a flexible one-dimensional array using the class [FlexArraySlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.FlexArraySlicer): whenever `@chunked` builds a new chunk, it will "slice" the corresponding subset of values from each parameter array.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-1)>>> chunked_pt_pipeline = vbt.chunked(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-2)... pt_pipeline_mult_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-3)... size=vbt.ArgSizer(arg_query="n_params"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-4)... arg_take_spec=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-5)... n_params=vbt.CountAdapter(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-6)... open=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-7)... high=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-8)... low=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-9)... close=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-10)... window=vbt.FlexArraySlicer(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-11)... upper=vbt.FlexArraySlicer(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-12)... lower=vbt.FlexArraySlicer(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-13)... sl_stop=vbt.FlexArraySlicer(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-14)... tsl_stop=vbt.FlexArraySlicer(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-15)... tp_stop=vbt.FlexArraySlicer()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-16)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-17)... chunk_len=1000, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-18)... merge_func="concat", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-19)... execute_kwargs=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-20)... chunk_len="auto",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-21)... engine="threadpool"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-36-23)... )
 
[/code]

 1. 2. 3. 4. 

Here's what happens: whenever we call `chunked_pt_pipeline`, it takes the total number of parameter combinations from the argument `n_params`. It then builds chunks of the length 1,000 and slices each chunk from the parameter arguments; one chunk corresponds to one call of `pt_pipeline_mult_nb`. Then, to parallelize the execution of chunks, we put them into super chunks. Chunks within a super chunk are executed in parallel, while super chunks themselves are executed serially; that's why the progress bar shows the progress of super chunks. 

Let's build the full parameter grid and run our function:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-1)>>> param_product, param_index = vbt.combine_params( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-2)... dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-3)... window=vbt.Param(WINDOW_SPACE), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-4)... upper=vbt.Param(UPPER_SPACE),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-5)... lower=vbt.Param(LOWER_SPACE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-9)>>> COPT_FILE = "temp/chunked_opt.pickle"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-11)>>> # vbt.remove_file(COPT_FILE, missing_ok=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-12)>>> if not vbt.file_exists(COPT_FILE):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-13)... chunked_opt = chunked_pt_pipeline(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-14)... len(param_index), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-15)... data.open.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-16)... data.high.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-17)... data.low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-18)... data.close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-19)... window=param_product["window"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-20)... upper=param_product["upper"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-21)... lower=param_product["lower"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-23)... vbt.save(chunked_opt, COPT_FILE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-24)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-37-25)... chunked_opt = vbt.load(COPT_FILE)
 
[/code]

 1. 2. 3. 

Super chunk 56/56

This runs in 40% less time than previously because the overhead of spawning a thread now weights much less compared to the higher workload in that thread. Also, we don't sacrifice any more RAM for this speedup since still only one parameter combination is processed at a time in `pt_pipeline_mult_nb`.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-38-1)>>> total_return, expectancy = chunked_opt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-38-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-38-3)>>> total_return = pd.Series(total_return, index=param_index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-38-4)>>> expectancy = pd.Series(expectancy, index=param_index)
 
[/code]

 1. 

We have just two limitations left: generating parameter combinations takes a considerable amount of time, and also, if the execution interrupts, all the optimization results will be lost. These issues can be mitigated by creating a while-loop that at each iteration generates a subset of parameter combinations, executes them, and then caches the results to disk. It runs until all the combinations are successfully processed. Another advantage: we can continue from the point where the execution stopped the last time, and even run the optimization procedure until some satisfactory set of parameters is found!

Let's say we want to include the stop parameters as well, but execute just a subset of random parameter combinations. Generating them with [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params) wouldn't be possible:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-39-1)>>> GRID_LEN = len(WINDOW_SPACE) * \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-39-2)... len(UPPER_SPACE) * \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-39-3)... len(LOWER_SPACE) * \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-39-4)... len(STOP_SPACE) ** 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-39-5)>>> print(GRID_LEN)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-39-6)441045000000
 
[/code]

We've got a half of a trillion parameter combinations ![😮‍💨](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f62e-200d-1f4a8.svg)

Instead, let's pick our parameter combinations in a smart way: use a function [pick_from_param_grid](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.pick_from_param_grid) that takes a dictionary of parameter spaces (order matters!) and the position of the parameter combination of interest, and returns the actual parameter combination that corresponds to that position. For example, pick the combination under the index 123,456,789:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-1)>>> GRID = dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-2)... window=WINDOW_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-3)... upper=UPPER_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-4)... lower=LOWER_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-5)... sl_stop=STOP_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-6)... tsl_stop=STOP_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-7)... tp_stop=STOP_SPACE,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-9)>>> vbt.pprint(vbt.pick_from_param_grid(GRID, 123_456_789))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-10)dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-11) window=5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-12) upper=3.090232306167813,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-13) lower=-2.241402727604947,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-14) sl_stop=45.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-15) tsl_stop=67.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-16) tp_stop=89.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-40-17))
 
[/code]

It's exactly the same parameter combination as if we combined all the parameters and did `param_index[123_456_789]`, but with almost zero performance and memory overhead!

We can now construct our while-loop. Let's do a random parameter search until we get at least 100 values with the expectancy of 1 or more!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-1)>>> FOUND_FILE = "temp/found.pickle"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-2)>>> BEST_N = 100 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-3)>>> BEST_TH = 1.0 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-4)>>> CHUNK_LEN = 10_000 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-6)>>> # vbt.remove_file(FOUND_FILE, missing_ok=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-7)>>> if vbt.file_exists(FOUND_FILE):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-8)... found = vbt.load(FOUND_FILE) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-9)>>> else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-10)... found = None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-11)>>> with ( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-12)... vbt.ProgressBar(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-13)... desc="Found", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-14)... initial=0 if found is None else len(found),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-15)... total=BEST_N
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-16)... ) as pbar1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-17)... vbt.ProgressBar(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-18)... desc="Processed"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-19)... ) as pbar2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-20)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-21)... while found is None or len(found) < BEST_N: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-22)... param_df = pd.DataFrame([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-23)... vbt.pick_from_param_grid(GRID) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-24)... for _ in range(CHUNK_LEN)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-25)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-26)... param_index = pd.MultiIndex.from_frame(param_df)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-27)... _, expectancy = chunked_pt_pipeline( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-28)... CHUNK_LEN,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-29)... data.open.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-30)... data.high.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-31)... data.low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-32)... data.close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-33)... window=param_df["window"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-34)... upper=param_df["upper"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-35)... lower=param_df["lower"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-36)... sl_stop=param_df["sl_stop"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-37)... tsl_stop=param_df["tsl_stop"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-38)... tp_stop=param_df["tp_stop"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-39)... _chunk_len=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-40)... _execute_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-41)... chunk_len=None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-42)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-43)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-44)... expectancy = pd.Series(expectancy, index=param_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-45)... best_mask = expectancy >= BEST_TH
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-46)... if best_mask.any(): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-47)... best = expectancy[best_mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-48)... if found is None:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-49)... found = best
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-50)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-51)... found = pd.concat((found, best))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-52)... found = found[~found.index.duplicated(keep="first")]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-53)... vbt.save(found, FOUND_FILE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-54)... pbar1.update_to(len(found))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-55)... pbar1.refresh()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-41-56)... pbar2.update(len(expectancy))
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 

Found 100/100

We can now run the cell above, interrupt it, and continue with the execution at a later time ![📅](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4c5.svg)

By having put similar parameter combinations into the same bucket, we can also aggregate them to derive a single optimal parameter combination:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-1)>>> def get_param_median(param): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-2)... return found.index.get_level_values(param).to_series().median()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-4)>>> pt_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-5)... data.open.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-6)... data.high.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-7)... data.low.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-8)... data.close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-9)... window=int(get_param_median("window")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-10)... upper=get_param_median("upper"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-11)... lower=get_param_median("lower"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-12)... sl_stop=get_param_median("sl_stop"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-13)... tsl_stop=get_param_median("tsl_stop"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-14)... tp_stop=get_param_median("tp_stop")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-42-16)(0.24251123364060986, 1.7316489316495804)
 
[/code]

 1. 

We can see that the median parameter combination satisfies our expectancy condition as well.

But sometimes, there's no need to test for so many parameter combinations, we can just use an established parameter optimization framework like [Optuna](https://optuna.org/). The advantages of this approach are on hand: we can use the original `pt_pipeline_nb` function without any decorators, we don't need to handle large parameter grids, and we can use various statistical approaches to both increase the effectiveness of the search and decrease the number of parameter combinations that we need to test.

Info

Make sure to install Optuna before running the following cell.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-1)>>> import optuna
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-3)>>> optuna.logging.disable_default_handler()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-4)>>> optuna.logging.set_verbosity(optuna.logging.WARNING)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-6)>>> def objective(trial):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-7)... window = trial.suggest_categorical("window", WINDOW_SPACE) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-8)... upper = trial.suggest_categorical("upper", UPPER_SPACE) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-9)... lower = trial.suggest_categorical("lower", LOWER_SPACE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-10)... sl_stop = trial.suggest_categorical("sl_stop", STOP_SPACE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-11)... tsl_stop = trial.suggest_categorical("tsl_stop", STOP_SPACE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-12)... tp_stop = trial.suggest_categorical("tp_stop", STOP_SPACE)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-13)... total_return, expectancy = pt_pipeline_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-14)... data.open.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-15)... data.high.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-16)... data.low.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-17)... data.close.values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-18)... window=window,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-19)... upper=upper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-20)... lower=lower,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-21)... sl_stop=sl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-22)... tsl_stop=tsl_stop,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-23)... tp_stop=tp_stop
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-25)... if np.isnan(total_return):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-26)... raise optuna.TrialPruned() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-27)... if np.isnan(expectancy):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-28)... raise optuna.TrialPruned()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-29)... return total_return, expectancy
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-31)>>> study = optuna.create_study(directions=["maximize", "maximize"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-32)>>> study.optimize(objective, n_trials=1000) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-33)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-34)>>> trials_df = study.trials_dataframe(attrs=["params", "values"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-35)>>> trials_df.set_index([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-36)... "params_window", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-37)... "params_upper", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-38)... "params_lower",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-39)... "params_sl_stop",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-40)... "params_tsl_stop",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-41)... "params_tp_stop"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-42)... ], inplace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-43)>>> trials_df.index.rename([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-44)... "window", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-45)... "upper", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-46)... "lower",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-47)... "sl_stop",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-48)... "tsl_stop",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-49)... "tp_stop"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-50)... ], inplace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-51)>>> trials_df.columns = ["total_return", "expectancy"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-52)>>> trials_df = trials_df[~trials_df.index.duplicated(keep="first")]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-53)>>> print(trials_df.sort_values(by="total_return", ascending=False))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-54) total_return expectancy
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-55)window upper lower sl_stop tsl_stop tp_stop 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-56)44 1.746485 -3.072346 9.0 67.0 55.0 0.558865 0.184924
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-57)42 1.871392 -3.286737 53.0 98.0 55.0 0.500062 0.330489
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-58) 77.0 0.496029 0.334432
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-59)5 1.746485 -1.759648 76.0 94.0 45.0 0.492721 0.043832
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-60)43 1.807618 -3.192280 87.0 36.0 60.0 0.475732 0.229682
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-61)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-62)7 2.639845 -3.072346 80.0 95.0 55.0 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-63)5 3.117886 -3.072346 78.0 90.0 47.0 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-64) 2.769169 -3.072346 78.0 90.0 55.0 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-65)7 3.098951 -3.072346 78.0 95.0 55.0 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-66) 2.607536 -3.072346 78.0 95.0 77.0 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-67)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-43-68)[892 rows x 2 columns]
 
[/code]

 1. 2. 3. 4. 5. 

The only downside to this approach is that we are limited by the picked results and are not able to explore the entire parameter landscape - the ability that vectorbt truly stands for.


# Level: Architect ![🛸](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f6f8.svg)[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#level-architect "Permanent link")

Let's say that we want to have the full control over the execution, for example, to execute at most one rebalancing operation in N days. Furthermore, we want to restrain from pre-calculating arrays and do everything in an event-driven fashion. For the sake of simplicity, let's switch our signaling algorithm from the cointegration with OLS to a basic distance measure: log prices.

We'll implement the strategy as a custom signal function in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals), which is the trickiest approach because the signal function is run per column while we want to make a decision per segment (i.e., just once for both columns). A worthy idea would be doing the calculations under the first column that is being processed at this bar, writing the results to some temporary arrays, and then accessing them under each column to return the signals. A perfect place for storing such arrays is a built-in named tuple `in_outputs`, which can be accessed both during the simulation phase and during the analysis phase.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-1)>>> InOutputs = namedtuple("InOutputs", ["spread", "zscore"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-3)>>> @njit(nogil=True, boundscheck=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-4)... def can_execute_nb(c, wait_days): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-5)... if c.order_counts[c.col] == 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-6)... return True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-7)... last_order = c.order_records[c.order_counts[c.col] - 1, c.col] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-8)... ns_delta = c.index[c.i] - c.index[last_order.idx] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-9)... if ns_delta >= wait_days * vbt.dt_nb.d_ns: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-10)... return True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-11)... return False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-13)>>> @njit(nogil=True, boundscheck=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-14)... def create_signals_nb(c, upper, lower, wait_days): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-15)... _upper = vbt.pf_nb.select_nb(c, upper) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-16)... _lower = vbt.pf_nb.select_nb(c, lower)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-17)... _wait_days = vbt.pf_nb.select_nb(c, wait_days)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-18)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-19)... if c.i > 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-20)... prev_zscore = c.in_outputs.zscore[c.i - 1, c.group]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-21)... zscore = c.in_outputs.zscore[c.i, c.group]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-22)... if prev_zscore < _upper and zscore > _upper: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-23)... if can_execute_nb(c, _wait_days):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-24)... if c.col % 2 == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-25)... return False, False, True, False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-26)... return True, False, False, False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-27)... if prev_zscore > _lower and zscore < _lower:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-28)... if can_execute_nb(c, _wait_days):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-29)... if c.col % 2 == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-30)... return True, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-31)... return False, False, True, False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-32)... return False, False, False, False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-33)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-34)>>> @njit(nogil=True, boundscheck=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-35)... def signal_func_nb(c, window, upper, lower, wait_days): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-36)... _window = vbt.pf_nb.select_nb(c, window)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-37)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-38)... if c.col % 2 == 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-39)... x = vbt.pf_nb.select_nb(c, c.close, col=c.col) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-40)... y = vbt.pf_nb.select_nb(c, c.close, col=c.col + 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-41)... c.in_outputs.spread[c.i, c.group] = np.log(y) - np.log(x) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-42)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-43)... window_start = c.i - _window + 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-44)... window_end = c.i + 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-45)... if window_start >= 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-46)... s = c.in_outputs.spread[window_start : window_end, c.group]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-47)... s_mean = np.nanmean(s)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-48)... s_std = np.nanstd(s)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-49)... c.in_outputs.zscore[c.i, c.group] = (s[-1] - s_mean) / s_std
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-44-50)... return create_signals_nb(c, upper, lower, wait_days)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 17. 18. 19. 20. 21. 

Next, create a pipeline that runs the simulation from the signal function above:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-1)>>> WAIT_DAYS = 30
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-3)>>> def iter_pt_portfolio(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-4)... window=WINDOW, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-5)... upper=UPPER, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-6)... lower=LOWER, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-7)... wait_days=WAIT_DAYS,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-8)... signal_func_nb=signal_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-9)... more_signal_args=(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-10)... **kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-11)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-12)... return vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-13)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-14)... broadcast_named_args=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-15)... window=window,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-16)... upper=upper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-17)... lower=lower,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-18)... wait_days=wait_days
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-19)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-20)... in_outputs=vbt.RepEval("""
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-21)... InOutputs(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-22)... np.full((target_shape[0], target_shape[1] // 2), np.nan), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-23)... np.full((target_shape[0], target_shape[1] // 2), np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-25)... """, context=dict(InOutputs=InOutputs)), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-26)... signal_func_nb=signal_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-27)... signal_args=( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-28)... vbt.Rep("window"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-29)... vbt.Rep("upper"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-30)... vbt.Rep("lower"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-31)... vbt.Rep("wait_days"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-32)... *more_signal_args
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-33)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-34)... size=10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-35)... size_type="valuepercent100",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-36)... group_by=vbt.ExceptLevel("symbol"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-37)... cash_sharing=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-38)... call_seq="auto",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-39)... delta_format="percent100",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-40)... stop_exit_price="close",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-41)... **kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-42)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-43)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-45-44)>>> pf = iter_pt_portfolio()
 
[/code]

 1. 2. 3. 4. 5. 6. 

Let's visually validate our implementation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-1)>>> fig = vbt.make_subplots( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-2)... rows=2, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-3)... cols=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-4)... vertical_spacing=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-5)... shared_xaxes=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-7)>>> zscore = pf.get_in_output("zscore").rename("Z-score") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-8)>>> zscore.vbt.plot( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-9)... add_trace_kwargs=dict(row=1, col=1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-10)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-12)>>> fig.add_hline(row=1, y=UPPER, line_color="orangered", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-13)>>> fig.add_hline(row=1, y=0, line_color="yellow", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-14)>>> fig.add_hline(row=1, y=LOWER, line_color="limegreen", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-15)>>> orders = pf.orders.regroup(group_by=False).iloc[:, 0] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-16)>>> exit_mask = orders.side_sell.get_pd_mask(idx_arr="signal_idx") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-17)>>> entry_mask = orders.side_buy.get_pd_mask(idx_arr="signal_idx") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-18)>>> upper_crossed = zscore.vbt.crossed_above(UPPER)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-19)>>> lower_crossed = zscore.vbt.crossed_below(LOWER)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-20)>>> (upper_crossed & ~exit_mask).vbt.signals.plot_as_exits( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-21)... pf.get_in_output("zscore"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-22)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-23)... name="Exits (ignored)", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-24)... marker=dict(color="lightgray"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-25)... opacity=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-26)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-27)... add_trace_kwargs=dict(row=1, col=1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-28)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-29)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-30)>>> (lower_crossed & ~entry_mask).vbt.signals.plot_as_entries(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-31)... pf.get_in_output("zscore"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-32)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-33)... name="Entries (ignored)", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-34)... marker=dict(color="lightgray"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-35)... opacity=0.5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-36)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-37)... add_trace_kwargs=dict(row=1, col=1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-38)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-39)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-40)>>> exit_mask.vbt.signals.plot_as_exits( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-41)... pf.get_in_output("zscore"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-42)... add_trace_kwargs=dict(row=1, col=1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-43)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-44)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-45)>>> entry_mask.vbt.signals.plot_as_entries(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-46)... pf.get_in_output("zscore"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-47)... add_trace_kwargs=dict(row=1, col=1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-48)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-49)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-50)>>> pf.plot_allocations( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-51)... add_trace_kwargs=dict(row=2, col=1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-52)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-53)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-54)>>> rebalancing_dates = data.index[np.unique(orders.idx.values)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-55)>>> for date in rebalancing_dates:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-56)... fig.add_vline(row=2, x=date, line_color="teal", line_dash="dot")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-57)>>> fig.update_layout(height=600)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-46-58)>>> fig.show()
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/iter_pt_portfolio.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/iter_pt_portfolio.dark.svg#only-dark)

Great, but what about parameter optimization? Thanks to the fact that we have defined our parameters as flexible arrays, we can pass them in a variety of formats, including [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param)! Let's discover how the waiting time affects the number of orders:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-47-1)>>> WAIT_SPACE = np.arange(30, 370, 5).tolist()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-47-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-47-3)>>> pf = iter_pt_portfolio(wait_days=vbt.Param(WAIT_SPACE))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-47-4)>>> pf.orders.count().vbt.scatterplot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-47-5)... xaxis_title="Wait days",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-47-6)... yaxis_title="Order count"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-47-7)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/wait_days.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pairs-trading/wait_days.dark.svg#only-dark)

Note, however, that the optimization approach above is associated with a high RAM usage since the OHLC data will have to be tiled the same number of times as there are parameter combinations; but this is the exactly same consideration as for optimizing `sl_stop` and other built-in parameters. Also, you might have noticed that both the compilation and execution take (much) longer than before: signal functions cannot be cached, thus, not only the entire simulator must be compiled from scratch with each new runtime, but we also must use an entirely different simulation path than the faster path based on signal arrays that we used before. Furthermore, our z-score implementation is quite slow because the mean and standard deviation must be re-computed for each single bar (remember that the previous OLS indicator was based on one of the fastest algorithms out there).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-48-1)>>> with (vbt.Timer() as timer, vbt.MemTracer() as tracer):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-48-2)... iter_pt_portfolio(wait_days=vbt.Param(WAIT_SPACE))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-48-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-48-4)>>> print(timer.elapsed())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-48-5)8.62 seconds
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-48-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-48-7)>>> print(tracer.peak_usage())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-48-8)306.2 MB
 
[/code]

While the compilation time is hard to manipulate, the execution time can be reduced significantly by replacing both the mean and standard deviation operations with a z-score accumulator, which can compute z-scores incrementally without the need for expensive aggregations. Luckily, there's such an accumulator already implemented in vectorbt - [rolling_zscore_acc_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.rolling_zscore_acc_nb). The workings are as follows: provide an input state that holds the information required to process the value for this bar, pass it to the accumulator, and in return, get the output state that contains both the calculated z-score and the new information required by the next bar.

The first question is: which information should we store? Generally, we should store the information that the accumulator changes and then expects to be provided at the next bar. The next question is: how to store such an information? A state is usually comprised of a bunch of single values, but named tuples aren't mutable ![🤔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f914.svg) The trick is to create a [structured NumPy array](https://numpy.org/doc/stable/user/basics.rec.html); you can imagine it being a regular NumPy array that holds mutable named tuples. We'll create a one-dimensional array with one tuple per group:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-1)>>> zscore_state_dt = np.dtype( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-2)... [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-3)... ("cumsum", float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-4)... ("cumsum_sq", float_),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-5)... ("nancnt", int_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-6)... ],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-7)... align=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-10)>>> @njit(nogil=True, boundscheck=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-11)... def stream_signal_func_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-12)... c, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-13)... window, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-14)... upper, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-15)... lower, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-16)... wait_days, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-17)... zscore_state 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-18)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-19)... _window = vbt.pf_nb.select_nb(c, window)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-20)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-21)... if c.col % 2 == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-22)... x = vbt.pf_nb.select_nb(c, c.close, col=c.col)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-23)... y = vbt.pf_nb.select_nb(c, c.close, col=c.col + 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-24)... c.in_outputs.spread[c.i, c.group] = np.log(y) - np.log(x)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-25)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-26)... value = c.in_outputs.spread[c.i, c.group] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-27)... pre_i = c.i - _window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-28)... if pre_i >= 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-29)... pre_window_value = c.in_outputs.spread[pre_i, c.group] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-30)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-31)... pre_window_value = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-32)... zscore_in_state = vbt.enums.RollZScoreAIS( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-33)... i=c.i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-34)... value=value,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-35)... pre_window_value=pre_window_value,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-36)... cumsum=zscore_state["cumsum"][c.group],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-37)... cumsum_sq=zscore_state["cumsum_sq"][c.group],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-38)... nancnt=zscore_state["nancnt"][c.group],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-39)... window=_window,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-40)... minp=_window,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-41)... ddof=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-42)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-43)... zscore_out_state = vbt.nb.rolling_zscore_acc_nb(zscore_in_state) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-44)... c.in_outputs.zscore[c.i, c.group] = zscore_out_state.value 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-45)... zscore_state["cumsum"][c.group] = zscore_out_state.cumsum 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-46)... zscore_state["cumsum_sq"][c.group] = zscore_out_state.cumsum_sq
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-47)... zscore_state["nancnt"][c.group] = zscore_out_state.nancnt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-48)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-49-49)... return create_signals_nb(c, upper, lower, wait_days)
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 

Next, we'll adapt the portfolio function to use our new signal function:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-1)>>> stream_pt_portfolio = partial( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-2)... iter_pt_portfolio,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-3)... signal_func_nb=stream_signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-4)... more_signal_args=( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-5)... vbt.RepEval( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-6)... """
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-7)... n_groups = target_shape[1] // 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-8)... zscore_state = np.empty(n_groups, dtype=zscore_state_dt)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-9)... zscore_state["cumsum"] = 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-10)... zscore_state["cumsum_sq"] = 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-11)... zscore_state["nancnt"] = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-12)... zscore_state
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-13)... """, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-14)... context=dict(zscore_state_dt=zscore_state_dt)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-15)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-50-17)... )
 
[/code]

 1. 2. 3. 

We're ready! Let's build the portfolio and compare to the previous one for validation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-51-1)>>> stream_pf = stream_pt_portfolio()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-51-2)>>> print(stream_pf.total_return)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-51-3)0.15210165047643728
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-51-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-51-5)>>> pf = iter_pt_portfolio()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-51-6)>>> print(pf.total_return)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-51-7)0.15210165047643728
 
[/code]

Finally, let's benchmark the new portfolio on `WAIT_SPACE`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-52-1)>>> with (vbt.Timer() as timer, vbt.MemTracer() as tracer):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-52-2)... stream_pt_portfolio(wait_days=vbt.Param(WAIT_SPACE))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-52-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-52-4)>>> print(timer.elapsed())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-52-5)1.52 seconds
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-52-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-52-7)>>> print(tracer.peak_usage())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-52-8)306.2 MB
 
[/code]

Info

Run this cell at least two times since the simulation may need to compile the first time. This is because the compilation is required whenever a new unique set of argument **types** is discovered. One parameter combination and multiple parameter combinations produce two different sets of argument types!

The final optimization to speed up the simulation of multiple parameter combinations is enabling the in-house chunking. There's one catch though: [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) doesn't know how to chunk any user-defined arrays, thus we need to manually provide the chunking specification for all the arguments in both `signal_args` and `in_outputs`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-1)>>> chunked_stream_pt_portfolio = partial(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-2)... stream_pt_portfolio,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-3)... chunked=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-4)... engine="threadpool",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-5)... arg_take_spec=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-6)... signal_args=vbt.ArgsTaker(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-7)... vbt.flex_array_gl_slicer, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-8)... vbt.flex_array_gl_slicer,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-9)... vbt.flex_array_gl_slicer,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-10)... vbt.flex_array_gl_slicer,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-11)... vbt.ArraySlicer(axis=0) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-12)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-13)... in_outputs=vbt.SequenceTaker([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-14)... vbt.ArraySlicer(axis=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-15)... vbt.ArraySlicer(axis=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-16)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-19)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-20)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-21)>>> with (vbt.Timer() as timer, vbt.MemTracer() as tracer):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-22)... chunked_stream_pt_portfolio(wait_days=vbt.Param(WAIT_SPACE))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-23)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-24)>>> print(timer.elapsed())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-25)520.08 milliseconds
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-26)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-27)>>> print(tracer.peak_usage())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#__codelineno-53-28)306.4 MB
 
[/code]

 1. 2. 3. 4. 

The optimization is now an order of magnitude faster than before ![💨](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4a8.svg)

Hint

To make the execution consume less memory, use the "serial" engine or build super chunks.


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading/#summary "Permanent link")

Pairs trading involves two columns with opposite position signs - an almost perfect use case because of the vectorbt's integrated grouping mechanics. And it gets even better: we can implement most pairs trading strategies by using semi-vectorized, iterative, and even streaming approaches alike. The focus of this tutorial is to showcase how a strategy can be incrementally developed and then optimized for both a high strategy performance and low resource consumption. 

We started the journey with the discovery phase where we designed and implemented the strategy from the ground up using various high-level tools and with no special regard for its performance. Once the framework of the strategy has been established, we moved over to make the execution faster to discover more lucrative configurations in a shorter span of time. Finally, we decided to flip the table and make the strategy iterative to gain complete control over its execution. But even this doesn't have to be the end of the story: if you're curious enough, you can build _your_ simulator and gain unmatched power that others can just dream of ![🦸](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f9b8.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/pairs-trading.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/PairsTrading.ipynb)