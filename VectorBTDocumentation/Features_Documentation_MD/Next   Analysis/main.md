# Analysis[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#analysis "Permanent link")


# Simulation ranges[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#simulation-ranges "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_5_15.svg)

 * Each simulation begins and ends at specific points, typically corresponding to the first and last rows of your data. You can define a different simulation range beforehand, and now, you can also adjust this range during the simulation. This flexibility allows you to halt the simulation when further processing is unnecessary. Additionally, the date range is stored in the portfolio object, ensuring all metrics and subplots are aware of it. Processing only the relevant dates enhances execution speed and introduces a new dimension for analysis—isolated time windows ![🔬](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f52c.svg)

Example 1: Simulate a quick liquidation scenario
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-2)... def post_segment_func_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-3)... value = vbt.pf_nb.get_group_value_nb(c, c.group)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-4)... if value <= 0:
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-5)... vbt.pf_nb.stop_group_sim_nb(c, c.group) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-6)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-7)>>> pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-8)... "BTC-USD", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-9)... n=10, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-10)... seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-11)... sim_start="auto", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-12)... post_segment_func_nb=post_segment_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-13)... leverage=10,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-0-15)>>> pf.plot_value() 
 
[/code]

 1. 2. 3. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/liquidation.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/liquidation.dark.svg#only-dark)

Example 2: Analyze a date range of an already simulated portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-1)>>> pf = vbt.PF.from_random_signals("BTC-USD", n=10, seed=42)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-3)>>> pf.get_sharpe_ratio(sim_start="2023", sim_end="2024") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-4)1.7846214408154346
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-6)>>> pf.get_sharpe_ratio(sim_start="2023", sim_end="2024", rec_sim_range=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-7)1.8377982089422782
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-8)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-9)>>> pf.returns_stats(settings=dict(sim_start="2023", sim_end="2024")) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-10)Start Index 2023-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-11)End Index 2023-12-31 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-12)Total Duration 365 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-13)Total Return [%] 84.715081
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-14)Benchmark Return [%] 155.417419
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-15)Annualized Return [%] 84.715081
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-16)Annualized Volatility [%] 38.49976
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-17)Max Drawdown [%] 20.057773
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-18)Max Drawdown Duration 102 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-19)Sharpe Ratio 1.784621
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-20)Calmar Ratio 4.223554
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-21)Omega Ratio 1.378076
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-22)Sortino Ratio 3.059933
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-23)Skew -0.39136
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-24)Kurtosis 13.607937
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-25)Tail Ratio 1.323376
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-26)Common Sense Ratio 1.823713
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-27)Value at Risk -0.028314
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-28)Alpha -0.103145
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-29)Beta 0.770428
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-1-30)dtype: object
 
[/code]

 1. 2. 3. 


# Expanding trade metrics[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#expanding-trade-metrics "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_11_0.svg)

 * Regular metrics such as MAE and MFE represent only the final point of each trade, but what if we would like to see their development during each trade? You can now analyze expanding trade metrics as DataFrames!

Visualize the expanding MFE using projections
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-2-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-2-2)>>> pf = vbt.PF.from_random_signals(data, n=50, tp_stop=0.5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-2-3)>>> pf.trades.plot_expanding_mfe_returns().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/expanding_mfe_returns.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/expanding_mfe_returns.dark.svg#only-dark)


# Trade signals[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#trade-signals "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_2.svg)

 * New method for plotting trades that categorizes entry and exit trades into long entries, long exits, short entries, and short exits. Supports different styles for positions.

Plot trade signals of a Bollinger Bands strategy
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-2)>>> bb = data.run("bbands")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-3)>>> long_entries = data.hlc3.vbt.crossed_above(bb.upper) & (bb.bandwidth < 0.1)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-4)>>> long_exits = data.hlc3.vbt.crossed_below(bb.upper) & (bb.bandwidth > 0.5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-5)>>> short_entries = data.hlc3.vbt.crossed_below(bb.lower) & (bb.bandwidth < 0.1)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-6)>>> short_exits = data.hlc3.vbt.crossed_above(bb.lower) & (bb.bandwidth > 0.5)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-7)>>> pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-8)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-9)... long_entries=long_entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-10)... long_exits=long_exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-11)... short_entries=short_entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-12)... short_exits=short_exits
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-3-14)>>> pf.plot_trade_signals().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/trade_signals.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/trade_signals.dark.svg#only-dark)


# Edge ratio[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#edge-ratio "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_1.svg)

 * [Edge ratio](https://www.buildalpha.com/eratio/) is a unique way to quantify entry profitability. Unlike most performance metrics, the edge ratio takes both open profits and losses into account. This can help you determine optimal trade exits.

Compare the edge ratio of an EMA crossover to a random strategy
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-2)>>> fast_ema = data.run("ema", 10, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-3)>>> slow_ema = data.run("ema", 20, hide_params=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-4)>>> entries = fast_ema.real_crossed_above(slow_ema)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-5)>>> exits = fast_ema.real_crossed_below(slow_ema)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-6)>>> pf = vbt.PF.from_signals(data, entries, exits, direction="both")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-7)>>> rand_pf = vbt.PF.from_random_signals(data, n=pf.orders.count() // 2) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-8)>>> fig = pf.trades.plot_running_edge_ratio(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-9)... trace_kwargs=dict(line_color="limegreen", name="Edge Ratio (S)")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-11)>>> fig = rand_pf.trades.plot_running_edge_ratio(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-12)... trace_kwargs=dict(line_color="mediumslateblue", name="Edge Ratio (R)"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-13)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-4-15)>>> fig.show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/running_edge_ratio.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/running_edge_ratio.dark.svg#only-dark)


# Trade history[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#trade-history "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_8_1.svg)

 * Trade history is a human-readable DataFrame that lists orders and extends them with valuable information on entry trades, exit trades, and positions.

Get the trade history of a random portfolio with one signal
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-1)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"], missing_index="drop")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-2)>>> pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-3)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-4)... n=1,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-5)... run_kwargs=dict(hide_params=True),
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-6)... tp_stop=0.5, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-7)... sl_stop=0.1
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-9)>>> pf.trade_history
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-10) Order Id Column Signal Index Creation Index \
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-11)0 0 BTC-USD 2016-02-20 00:00:00+00:00 2016-02-20 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-12)1 1 BTC-USD 2016-02-20 00:00:00+00:00 2016-06-12 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-13)2 0 ETH-USD 2019-05-25 00:00:00+00:00 2019-05-25 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-14)3 1 ETH-USD 2019-05-25 00:00:00+00:00 2019-07-15 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-15)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-16) Fill Index Side Type Stop Type Size Price \
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-17)0 2016-02-20 00:00:00+00:00 Buy Market None 0.228747 437.164001 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-18)1 2016-06-12 00:00:00+00:00 Sell Market TP 0.228747 655.746002 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-19)2 2019-05-25 00:00:00+00:00 Buy Market None 0.397204 251.759872 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-20)3 2019-07-15 00:00:00+00:00 Sell Market SL 0.397204 226.583885 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-21)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-22) Fees PnL Return Direction Status Entry Trade Id Exit Trade Id \
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-23)0 0.0 50.0 0.5 Long Closed 0 -1 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-24)1 0.0 50.0 0.5 Long Closed -1 0 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-25)2 0.0 -10.0 -0.1 Long Closed 0 -1 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-26)3 0.0 -10.0 -0.1 Long Closed -1 0 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-27)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-28) Position Id 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-29)0 0 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-30)1 0 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-31)2 0 
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-5-32)3 0 
 
[/code]


# Patterns[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#patterns "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_5_0.svg)

 * Patterns are the distinctive formations created by the movements of security prices on a chart and are the foundation of technical analysis. There are new designated functions and classes for detecting patterns of any complexity in any time series data. The concept is simple: fit a pattern to match the scale and period of the selected data window, and compute their element-wise distance to each other to derive a single similarity score. You can then tweak the threshold for this score above which a data window should be marked as "matched". Thanks to Numba, this operation can be done hundreds of thousands of times per second! ![🔎](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f50e.svg)

Tutorial

Learn more in the [Patterns and projections](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections) tutorial.

Find and plot a descending triangle pattern
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-6-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-6-2)>>> data.hlc3.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-6-3)... pattern=[5, 1, 3, 1, 2, 1],
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-6-4)... window=100,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-6-5)... max_window=700,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-6-6)... ).loc["2017":"2019"].plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/patterns.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/patterns.dark.svg#only-dark)


# Projections[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#projections "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_5_0.svg)

 * There are more clean ways of analyzing events and their impact on the price than conventional backtesting. Meet projections! ![👋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f44b.svg) Not only they can allow you to assess the performance of events visually and quantitatively, but they also can enable you to project events into the future for assistance in trading. That is possible by extracting the price range after each event, putting all the price ranges into a multidimensional array, and deriving the confidence intervals and other meaningful statistics from that array. Combined with patterns, these are a quantitative analyst's dream tools! ![🌠](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f320.svg)

Tutorial

Learn more in the [Patterns and projections](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections) tutorial.

Find occurrences of the price moving similarly to the last week and project them
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-1)>>> data = vbt.YFData.pull("ETH-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-2)>>> pattern_ranges = data.hlc3.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-3)... pattern=data.close.iloc[-7:],
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-4)... rescale_mode="rebase"
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-6)>>> delta_ranges = pattern_ranges.with_delta(7)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-7)>>> fig = data.iloc[-7:].plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-8)>>> delta_ranges.plot_projections(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-7-9)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/projections.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/projections.dark.svg#only-dark)


# MAE and MFE[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#mae-and-mfe "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_3_0.svg)

 * [Maximum Adverse Excursion (MAE)](https://analyzingalpha.com/maximum-adverse-excursion) helps you to identify what the maximum loss was during a trade. This is also known as maximum drawdown of the position. [Maximum Favorable Excursion (MFE)](https://analyzingalpha.com/maximum-favorable-excursion), on the other hand, shows you what the highest profit was during a trade. Analyzing MAE and MFE statistics can help you optimize your exit strategies.

Analyze the MAE of a random portfolio without SL
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-8-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-8-2)>>> pf = vbt.PF.from_random_signals(data, n=50)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-8-3)>>> pf.trades.plot_mae_returns().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/mae_without_sl.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/mae_without_sl.dark.svg#only-dark)

Analyze the MAE of a random portfolio with SL
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-9-1)>>> pf = vbt.PF.from_random_signals(data, n=50, sl_stop=0.1)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-9-2)>>> pf.trades.plot_mae_returns().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/mae_with_sl.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/mae_with_sl.dark.svg#only-dark)


# OHLC-native classes[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#ohlc-native-classes "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_3_0.svg)

 * Previously, OHLC was used for simulation but only the close price was used for analysis purposes. With this update, most classes will allow you to keep track of the entire OHLC data for a more accurate quantitative and qualitative analysis.

Plot trades of a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-1)>>> data = vbt.YFData.pull("BTC-USD", start="2020-01", end="2020-03")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-2)>>> pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-3)... open=data.open,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-4)... high=data.high,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-5)... low=data.low,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-6)... close=data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-7)... n=10
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-10-9)>>> pf.trades.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/ohlc_native_classes.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/ohlc_native_classes.dark.svg#only-dark)


# Benchmark[¶](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#benchmark "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_4.svg)

 * Benchmark can be easily set for the entire portfolio.

Compare Microsoft to S&P 500
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-11-1)>>> data = vbt.YFData.pull(["SPY", "MSFT"], start="2010", missing_columns="drop")
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-11-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-11-3)>>> pf = vbt.PF.from_holding(
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-11-4)... close=data.data["MSFT"]["Close"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-11-5)... bm_close=data.data["SPY"]["Close"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-11-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/analysis/#__codelineno-11-7)>>> pf.plot_cumulative_returns().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/benchmark.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/benchmark.dark.svg#only-dark)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/features/analysis.py.txt)