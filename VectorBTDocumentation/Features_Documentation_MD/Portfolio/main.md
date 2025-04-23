# Portfolio[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#portfolio "Permanent link")


# Asset weighting[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#asset-weighting "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_8_20.svg)

 * Asset weighting enables you to fine-tune the influence of individual assets or strategies within your portfolio, providing enhanced control over the overall portfolio's performance. The key advantage: these weights aren't limited to just returns—they are consistently applied across all time series and metrics, including orders, cash flows, and more. This holistic approach ensures that every aspect of your portfolio is precisely aligned.

Maximize Sharpe of a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-1)>>> data = vbt.YFData.pull(["AAPL", "MSFT", "GOOG"], start="2020")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-2)>>> pf = data.run("from_random_signals", n=vbt.Default(50), seed=42, group_by=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-3)>>> pf.get_sharpe_ratio(group_by=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-4)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-5)AAPL 1.401012
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-6)MSFT 0.456162
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-7)GOOG 0.852490
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-8)Name: sharpe_ratio, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-9)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-10)>>> pf.sharpe_ratio 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-11)1.2132857343006869
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-12)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-13)>>> prices = pf.get_value(group_by=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-14)>>> weights = vbt.pypfopt_optimize(prices=prices) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-15)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-16){'AAPL': 0.85232, 'MSFT': 0.0, 'GOOG': 0.14768}
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-18)>>> weighted_pf = pf.apply_weights(weights, rescale=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-19)>>> weighted_pf.weights
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-20)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-21)AAPL 2.55696
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-22)MSFT 0.00000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-23)GOOG 0.44304
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-24)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-25)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-26)>>> weighted_pf.get_sharpe_ratio(group_by=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-0-27)1.426112580298898
 
[/code]

 1. 2. 3. 4. 5. 


# Position views[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#position-views "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/v2024_8_20.svg)

 * Position views enable the analysis of portfolios by focusing specifically on either long or short positions, providing a clear and distinct perspective on each investment strategy.

Separate long and short positions of a basic SMA crossover portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-2)>>> fast_sma = data.run("talib_func:sma", timeperiod=20)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-3)>>> slow_sma = data.run("talib_func:sma", timeperiod=50)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-4)>>> long_entries = fast_sma.vbt.crossed_above(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-5)>>> short_entries = fast_sma.vbt.crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-6)>>> pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-7)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-8)... long_entries=long_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-9)... short_entries=short_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-10)... fees=0.01,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-11)... fixed_fees=1.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-13)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-14)>>> long_pf = pf.long_view
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-15)>>> short_pf = pf.short_view
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-16)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-17)>>> fig = vbt.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-18)>>> fig = long_pf.assets.vbt.plot_against(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-19)... 0, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-20)... trace_kwargs=dict(name="Long position", line_shape="hv", line_color="mediumseagreen"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-21)... other_trace_kwargs=dict(visible=False),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-22)... add_trace_kwargs=dict(row=1, col=1),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-23)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-25)>>> fig = short_pf.assets.vbt.plot_against(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-26)... 0, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-27)... trace_kwargs=dict(name="Short position", line_shape="hv", line_color="coral"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-28)... other_trace_kwargs=dict(visible=False), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-29)... add_trace_kwargs=dict(row=2, col=1),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-30)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-31)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-1-32)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/position_views.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/position_views.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-2-1)>>> long_pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-2-2)0.9185961894435091
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-2-3)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-2-4)>>> short_pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-2-5)0.2760864152147919
 
[/code]


# Index records[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#index-records "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_12_0.svg)

 * How do you backtest time and asset-anchored queries such as "Order X units of asset Y on date Z"? Normally, you'd have to construct a full array and set information manually. But now there's a less stressful way: thanks to the preparers and redesigned smart indexing you can provide all information in a compressed record format! Under the hood, the record array will be translated into a set of [index dictionaries](https://vectorbt.pro/pvt_7a467f6b/features/productivity/#index-dictionaries) \- one per argument.

Define a basic signal strategy using records
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-1)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"], missing_index="drop")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-2)>>> records = [
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-3)... dict(date="2022", symbol="BTC-USD", long_entry=True), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-4)... dict(date="2022", symbol="ETH-USD", short_entry=True),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-5)... dict(row=-1, exit=True),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-6)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-7)>>> pf = vbt.PF.from_signals(data, records=records) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-8)>>> pf.orders.readable
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-9) Order Id Column Signal Index Creation Index 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-10)0 0 BTC-USD 2022-01-01 00:00:00+00:00 2022-01-01 00:00:00+00:00 \
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-11)1 1 BTC-USD 2023-04-25 00:00:00+00:00 2023-04-25 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-12)2 0 ETH-USD 2022-01-01 00:00:00+00:00 2022-01-01 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-13)3 1 ETH-USD 2023-04-25 00:00:00+00:00 2023-04-25 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-15) Fill Index Size Price Fees Side Type 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-16)0 2022-01-01 00:00:00+00:00 0.002097 47686.812500 0.0 Buy Market \
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-17)1 2023-04-25 00:00:00+00:00 0.002097 27534.675781 0.0 Sell Market 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-18)2 2022-01-01 00:00:00+00:00 0.026527 3769.697021 0.0 Sell Market 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-19)3 2023-04-25 00:00:00+00:00 0.026527 1834.759644 0.0 Buy Market 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-20)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-21) Stop Type 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-22)0 None 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-23)1 None 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-24)2 None 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-3-25)3 None 
 
[/code]

 1. 2. 


# Portfolio preparers[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#portfolio-preparers "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_12_0.svg)

 * When you pass an argument to a simulation method such as `Portfolio.from_signals`, it must go through a complex preparation pipeline first to get a format suitable for Numba. Such a pipeline usually involves mapping of enums, broadcasting, data type checks, template substitution, and many other steps. To make VBT more transparent, this pipeline has been outsourced to a separate class so you now have the full control of arguments that are getting passed to the Numba functions! Moreover, you can extend the preparers to automatically prepare arguments for your own simulators.

Get a prepared argument, modify it, and use in a new simulation
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-1)>>> data = vbt.YFData.pull("BTC-USD", end="2017-01")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-2)>>> prep_result = vbt.PF.from_holding(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-3)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-4)... stop_ladder="uniform",
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-5)... tp_stop=vbt.Param([
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-6)... [0.1, 0.2, 0.3, 0.4, 0.5],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-7)... [0.4, 0.5, 0.6],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-8)... ], keys=["tp_ladder_1", "tp_ladder_2"]),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-9)... return_prep_result=True 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-11)>>> prep_result.target_args["tp_stop"] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-12)array([[0.1, 0.4],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-13) [0.2, 0.5],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-14) [0.3, 0.6],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-15) [0.4, nan],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-16) [0.5, nan]])
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-17)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-18)>>> new_tp_stop = prep_result.target_args["tp_stop"] + 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-19)>>> new_prep_result = prep_result.replace(target_args=dict(tp_stop=new_tp_stop), nested_=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-20)>>> new_prep_result.target_args["tp_stop"]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-21)array([[0.2, 0.5],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-22) [0.3, 0.6],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-23) [0.4, 0.7],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-24) [0.5, nan],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-25) [0.6, nan]])
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-26)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-27)>>> pf = vbt.PF.from_signals(new_prep_result) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-28)>>> pf.total_return
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-29)tp_stop
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-30)tp_ladder_1 0.4
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-31)tp_ladder_2 0.6
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-32)Name: total_return, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-33)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-34)>>> sim_out = new_prep_result.target_func(**new_prep_result.target_args) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-35)>>> pf = vbt.PF(order_records=sim_out, **new_prep_result.pf_args)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-36)>>> pf.total_return
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-37)tp_stop
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-38)tp_ladder_1 0.4
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-39)tp_ladder_2 0.6
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-4-40)Name: total_return, dtype: float64
 
[/code]

 1. 2. 3. 4. 5. 


# Stop laddering[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#stop-laddering "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_12_0.svg)

 * Stop laddering is a technique to incrementally move out of a position. Instead of providing a single stop value to close out the position, you can now provide an array of stop values, each removing a certain amount of the position when hit. This amount can be controlled by providing a differnet ladder mode. Furthermore, thanks to a new broadcasting feature that allows arrays to broadcast along just one axis, the stop values don't need to have the same shape as data. You can even provide stop arrays of different shapes as parameters!

Test two TP ladders
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-1)>>> data = vbt.YFData.pull("BTC-USD", end="2017-01")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-2)>>> pf = vbt.PF.from_holding(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-3)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-4)... stop_ladder="uniform",
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-5)... tp_stop=vbt.Param([
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-6)... [0.1, 0.2, 0.3, 0.4, 0.5],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-7)... [0.4, 0.5, 0.6],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-8)... ], keys=["tp_ladder_1", "tp_ladder_2"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-5-10)>>> pf.trades.plot(column="tp_ladder_1").show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/stop_laddering.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/stop_laddering.dark.svg#only-dark)


# Staticization[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#staticization "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_11_0.svg)

 * One of the biggest limitations of Numba is that functions passed as arguments (i.e., callbacks) make the main function uncacheable, such that it has to be re-compiled in each new runtime, over and over again. Especially the performance of simulator functions takes a hit as they usually take up to a minute to compile. Gladly, we've got a new neat trick in our arsenal: "staticization". It works as follows. First, the source code of a function gets annotated with a special syntax. The annotated code then gets extracted (a.k.a. "cutting" ![✂](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2702.svg)), modified into a cacheable version by removing any callbacks from the arguments, and saved to a Python file. Once the function gets called again, the cacheable version gets executed. Sounds complex? See below!

Define the signal function in a Python file, here signal_func_nb.py
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-6-1)from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-6-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-6-3)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-6-4)def signal_func_nb(c, fast_sma, slow_sma): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-6-5) long = vbt.pf_nb.iter_crossed_above_nb(c, fast_sma, slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-6-6) short = vbt.pf_nb.iter_crossed_below_nb(c, fast_sma, slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-6-7) return long, False, short, False
 
[/code]

 1. 

Run a staticized simulation. Running the script again won't re-compile.
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-2)>>> pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-3)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-4)... signal_func_nb="signal_func_nb.py", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-5)... signal_args=(vbt.Rep("fast_sma"), vbt.Rep("slow_sma")),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-6)... broadcast_named_args=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-7)... fast_sma=data.run("sma", 20, hide_params=True, unpack=True), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-8)... slow_sma=data.run("sma", 50, hide_params=True, unpack=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-9)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-10)... staticized=True 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-7-11)... )
 
[/code]

 1. 2. 


# Position info[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#position-info "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_11_0.svg)

 * Dynamic signal functions have now access to the current position information such as (open) P&L.

Enter randomly, exit randomly but only if in profit
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-2)... def signal_func_nb(c, entries, exits):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-3)... is_entry = vbt.pf_nb.select_nb(c, entries)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-4)... is_exit = vbt.pf_nb.select_nb(c, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-5)... if is_entry:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-6)... return True, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-7)... if is_exit:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-8)... pos_info = c.last_pos_info[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-9)... if pos_info["status"] == vbt.pf_enums.TradeStatus.Open:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-10)... if pos_info["pnl"] >= 0:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-11)... return False, True, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-12)... return False, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-13)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-14)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-15)>>> entries, exits = data.run("RANDNX", n=10, unpack=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-16)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-17)... data,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-18)... signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-19)... signal_args=(vbt.Rep("entries"), vbt.Rep("exits")),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-20)... broadcast_named_args=dict(entries=entries, exits=exits),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-21)... jitted=False 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-23)>>> pf.trades.readable[["Entry Index", "Exit Index", "PnL"]]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-24) Entry Index Exit Index PnL
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-25)0 2014-11-01 00:00:00+00:00 2016-01-08 00:00:00+00:00 39.134739
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-26)1 2016-03-27 00:00:00+00:00 2016-09-07 00:00:00+00:00 61.220063
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-27)2 2016-12-24 00:00:00+00:00 2016-12-31 00:00:00+00:00 14.471414
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-28)3 2017-03-16 00:00:00+00:00 2017-08-05 00:00:00+00:00 373.492028
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-29)4 2017-09-12 00:00:00+00:00 2018-05-05 00:00:00+00:00 815.699284
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-30)5 2019-02-15 00:00:00+00:00 2019-11-10 00:00:00+00:00 2107.383227
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-31)6 2019-12-04 00:00:00+00:00 2019-12-10 00:00:00+00:00 12.630214
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-32)7 2020-07-12 00:00:00+00:00 2021-11-14 00:00:00+00:00 21346.035444
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-8-33)8 2022-01-15 00:00:00+00:00 2023-03-06 00:00:00+00:00 -11925.133817
 
[/code]

 1. 


# Time stops[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#time-stops "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_11_0.svg)

 * Joining the ranks of stop orders, time stop orders can close out a position after a period of time or also on a specific date.

Enter randomly, exit before the end of the month
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-1)>>> data = vbt.YFData.pull("BTC-USD", start="2022-01", end="2022-04")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-2)>>> entries = vbt.pd_acc.signals.generate_random(data.symbol_wrapper, n=10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-3)>>> pf = vbt.PF.from_signals(data, entries, dt_stop="M") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-4)>>> pf.orders.readable[["Fill Index", "Side", "Stop Type"]]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-5) Fill Index Side Stop Type
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-6)0 2022-01-19 00:00:00+00:00 Buy None
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-7)1 2022-01-31 00:00:00+00:00 Sell DT
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-8)2 2022-02-25 00:00:00+00:00 Buy None
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-9)3 2022-02-28 00:00:00+00:00 Sell DT
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-10)4 2022-03-11 00:00:00+00:00 Buy None
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-9-11)5 2022-03-31 00:00:00+00:00 Sell DT
 
[/code]

 1. 


# Target size to signals[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#target-size-to-signals "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_10_0.svg)

 * Target size can be translated to signals using a special signal function to gain access to the stop and limit order functionality, for example, when performing a portfolio optimization.

Perform the Mean-Variance Optimization with SL and TP
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-1)>>> data = vbt.YFData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-2)... ["SPY", "TLT", "XLF", "XLE", "XLU", "XLK", "XLB", "XLP", "XLY", "XLI", "XLV"],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-3)... start="2022",
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-4)... end="2023",
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-5)... missing_index="drop"
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-7)>>> pfo = vbt.PFO.from_riskfolio(data.returns, every="M")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-8)>>> pf = pfo.simulate(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-9)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-10)... pf_method="from_signals", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-11)... sl_stop=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-12)... tp_stop=0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-13)... stop_exit_price="close" 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-10-15)>>> pf.plot_allocations().show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/target_size_to_signals.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/target_size_to_signals.dark.svg#only-dark)


# Target price[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#target-price "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_10_0.svg)

 * Limit and stop orders can also be defined using a target price rather than a delta.

Set the SL to the previous low in a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-2)>>> pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-3)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-4)... n=100, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-5)... sl_stop=data.low.vbt.ago(1),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-6)... delta_format="target"
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-8)>>> sl_orders = pf.orders.stop_type_sl
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-9)>>> signal_index = pf.wrapper.index[sl_orders.signal_idx.values]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-10)>>> hit_index = pf.wrapper.index[sl_orders.idx.values]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-11)>>> hit_after = hit_index - signal_index
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-12)>>> hit_after
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-13)TimedeltaIndex([ '7 days', '3 days', '1 days', '5 days', '4 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-14) '1 days', '28 days', '1 days', '1 days', '1 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-15) '1 days', '1 days', '13 days', '10 days', '5 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-16) '1 days', '3 days', '4 days', '1 days', '9 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-17) '5 days', '1 days', '1 days', '2 days', '1 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-18) '1 days', '1 days', '3 days', '1 days', '1 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-19) '1 days', '1 days', '1 days', '2 days', '2 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-20) '1 days', '12 days', '3 days', '1 days', '1 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-21) '1 days', '1 days', '1 days', '3 days', '1 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-22) '1 days', '1 days', '4 days', '1 days', '1 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-23) '2 days', '6 days', '11 days', '1 days', '2 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-24) '1 days', '1 days', '1 days', '1 days', '1 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-25) '4 days', '10 days', '1 days', '1 days', '1 days',
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-26) '2 days', '3 days', '1 days'],
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-11-27) dtype='timedelta64[ns]', name='Date', freq=None)
 
[/code]


# Leverage[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#leverage "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_9_0.svg)

 * Leverage has become an integral part of the portfolio simulation. Supports two different leverage modes: `lazy` (enables leverage only if there's not enough cash available) and `eager` (enables leverage while using only a fraction of the available cash). Allows setting leverage per order. Can also determine an optimal leverage value automatically to satisfy any order requirement! ![🏋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f3cb.svg)

Explore how leverage affects the equity curve in a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-12-1)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2022")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-12-2)>>> pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-12-3)... data, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-12-4)... n=100, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-12-5)... leverage=vbt.Param([0.5, 1, 2, 3]),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-12-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-12-7)>>> pf.value.vbt.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/leverage.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/leverage.dark.svg#only-dark)


# Order delays[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#order-delays "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_4_1.svg)

 * By default, VBT executes every order at the end of the current bar. To delay the execution to the next bar, one had to manually shift all the order-related arrays by one bar, which makes the operation prone to user mistakes. To avoid them, you can now simply specify the number of bars in the past you want the order information to be taken from. Moreover, the price argument has got the new options "nextopen" and "nextclose" for a one-line solution.

Compare orders without and with a delay in a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-1)>>> pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-2)... vbt.YFData.pull("BTC-USD", start="2021-01", end="2021-02"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-3)... n=3, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-4)... price=vbt.Param(["close", "nextopen"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-6)>>> fig = pf.orders["close"].plot(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-7)... buy_trace_kwargs=dict(name="Buy (close)", marker=dict(symbol="triangle-up-open")),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-8)... sell_trace_kwargs=dict(name="Buy (close)", marker=dict(symbol="triangle-down-open"))
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-10)>>> pf.orders["nextopen"].plot(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-11)... plot_ohlc=False,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-12)... plot_close=False,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-13)... buy_trace_kwargs=dict(name="Buy (nextopen)"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-14)... sell_trace_kwargs=dict(name="Sell (nextopen)"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-15)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-13-17)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/order_delays.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/order_delays.dark.svg#only-dark)


# Signal callbacks[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#signal-callbacks "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_4_0.svg)

 * Want to hack into the simulation based on signals, or even generate signals dynamically based on the current backtesting environment? There are two new callbacks that push flexibility of the simulator to the limits: one that lets the user generate or override signals for each asset at the current bar, and another one that lets the user compute any user-defined metrics for the entire group at the end of the bar. Both are taking a so-called "context" that contains the information on the current simulation state based on which trading decisions can be made - very similar to how event-driven backtesters work.

Backtest SMA crossover iteratively
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-1)>>> InOutputs = namedtuple("InOutputs", ["fast_sma", "slow_sma"])
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-3)>>> def initialize_in_outputs(target_shape):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-4)... return InOutputs(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-5)... fast_sma=np.full(target_shape, np.nan),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-6)... slow_sma=np.full(target_shape, np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-8)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-9)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-10)... def signal_func_nb(c, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-11)... fast_sma = c.in_outputs.fast_sma
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-12)... slow_sma = c.in_outputs.slow_sma
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-13)... fast_start_i = c.i - fast_window + 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-14)... slow_start_i = c.i - slow_window + 1
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-15)... if fast_start_i >= 0 and slow_start_i >= 0:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-16)... fast_sma[c.i, c.col] = np.nanmean(c.close[fast_start_i : c.i + 1])
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-17)... slow_sma[c.i, c.col] = np.nanmean(c.close[slow_start_i : c.i + 1])
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-18)... is_entry = vbt.pf_nb.iter_crossed_above_nb(c, fast_sma, slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-19)... is_exit = vbt.pf_nb.iter_crossed_below_nb(c, fast_sma, slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-20)... return is_entry, is_exit, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-21)... return False, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-22)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-23)>>> pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-24)... vbt.YFData.pull("BTC-USD"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-25)... signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-26)... signal_args=(50, 200),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-27)... in_outputs=vbt.RepFunc(initialize_in_outputs),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-28)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-29)>>> fig = pf.get_in_output("fast_sma").vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-30)>>> pf.get_in_output("slow_sma").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-31)>>> pf.orders.plot(plot_ohlc=False, plot_close=False, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-14-32)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/signal_callbacks.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/signal_callbacks.dark.svg#only-dark)


# Limit orders[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#limit-orders "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_4_0.svg)

 * Long-awaited support for limit orders in simulation based on signals! Features time-in-force (TIF) orders, such as DAY, GTC, GTD, LOO, and FOK orders ![⏰](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/23f0.svg) You can also reverse a limit order as well as create it using a delta for easier testing.

Explore how limit delta affects number of orders in a random portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-1)>>> pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-2)... vbt.YFData.pull("BTC-USD"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-3)... n=100, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-4)... order_type="limit", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-5)... limit_delta=vbt.Param(np.arange(0.001, 0.1, 0.001)), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-7)>>> pf.orders.count().vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-8)... xaxis_title="Limit delta", 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-9)... yaxis_title="Order count"
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-15-10)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/limit_delta.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/limit_delta.dark.svg#only-dark)


# Delta formats[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#delta-formats "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_4_0.svg)

 * Previously, stop orders had to be provided strictly as percentages, which works well for single values but may require some transformations for arrays. For example, to set SL to ATR, one would need to know the entry price. Generally, to lock in a specific dollar amount of a trade, you may prefer to utilize a fixed price trailing stop. To address this, VBT has introduced multiple stop value formats (so called "delta formats") to choose from.

Use ATR as SL
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-16-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-16-2)>>> atr = vbt.talib("ATR").run(data.high, data.low, data.close).real
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-16-3)>>> pf = vbt.PF.from_holding(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-16-4)... data.loc["2022-01-01":"2022-01-07"], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-16-5)... sl_stop=atr.loc["2022-01-01":"2022-01-07"], 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-16-6)... delta_format="absolute"
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-16-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-16-8)>>> pf.orders.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/delta_formats.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/delta_formats.dark.svg#only-dark)


# Bar skipping[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#bar-skipping "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_4_0.svg)

 * Simulation based on orders and signals can (partially) skip bars that do not define any orders - a change that often results in noticeable speedups for sparsely distributed orders.

Benchmark bar skipping in a buy-and-hold portfolio
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-17-1)>>> data = vbt.BinanceData.pull("BTCUSDT", start="one month ago UTC", timeframe="minute")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-17-2)>>> size = data.symbol_wrapper.fill(np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-17-3)>>> size[0] = np.inf
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-18-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-18-2)>>> vbt.PF.from_orders(data, size, ffill_val_price=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-18-3)5.92 ms ± 300 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

 1. 

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-19-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-19-2)>>> vbt.PF.from_orders(data, size, ffill_val_price=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-19-3)2.75 ms ± 16 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 
[/code]


# Signal contexts[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#signal-contexts "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_2_3.svg)

 * Signal generation functions have been redesigned from the ground up to operate on contexts. This allows for designing more complex signal strategies with less namespace polution.

Tutorial

Learn more in the [Signal development](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development) tutorial.

Entry at the first bar of the week, exit at the last bar of the week
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-2)... def entry_place_func_nb(c, index): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-3)... for i in range(c.from_i, c.to_i): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-4)... if i == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-5)... return i - c.from_i 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-6)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-7)... index_before = index[i - 1]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-8)... index_now = index[i]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-9)... index_next_week = vbt.dt_nb.future_weekday_nb(index_before, 0)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-10)... if index_now >= index_next_week: 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-11)... return i - c.from_i
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-12)... return -1
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-13)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-14)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-15)... def exit_place_func_nb(c, index): 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-16)... for i in range(c.from_i, c.to_i):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-17)... if i == len(index) - 1:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-18)... return i - c.from_i
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-19)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-20)... index_now = index[i]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-21)... index_after = index[i + 1]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-22)... index_next_week = vbt.dt_nb.future_weekday_nb(index_now, 0)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-23)... if index_after >= index_next_week: 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-24)... return i - c.from_i
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-25)... return -1
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-26)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-27)>>> data = vbt.YFData.pull("BTC-USD", start="2020-01-01", end="2020-01-14")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-28)>>> entries, exits = vbt.pd_acc.signals.generate_both(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-29)... data.symbol_wrapper.shape,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-30)... entry_place_func_nb=entry_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-31)... entry_place_args=(data.index.vbt.to_ns(),),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-32)... exit_place_func_nb=exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-33)... exit_place_args=(data.index.vbt.to_ns(),),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-34)... wrapper=data.symbol_wrapper
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-35)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-36)>>> pd.concat((
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-37)... entries.rename("Entries"), 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-38)... exits.rename("Exits")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-39)... ), axis=1).to_period("W")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-40) Entries Exits
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-41)Date 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-42)2020-01-06/2020-01-12 True False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-43)2020-01-06/2020-01-12 False False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-44)2020-01-06/2020-01-12 False False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-45)2020-01-06/2020-01-12 False False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-46)2020-01-06/2020-01-12 False False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-47)2020-01-06/2020-01-12 False False
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-48)2020-01-06/2020-01-12 False True
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-20-49)2020-01-13/2020-01-19 True False
 
[/code]

 1. 2. 3. 4. 


# Pre-computation[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#pre-computation "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_10.svg)

 * There is a tradeoff between memory consumption and execution speed: a 1000-column dataset is usually processed much faster than a 1-column dataset 1000 times. But the first dataset also requires 1000 times more memory than the second one. That's why during the simulation phase, VBT mainly generates orders while other portfolio attributes such as various balances, equity, and returns are then later reconstructed during the analysis phase if it's needed by the user. For use cases where performance is the main criteria, there are now arguments that allow pre-computing these attributes at the simulation time! ![⏩](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/23e9.svg)

Benchmark a random portfolio with 1000 columns without and with pre-computation
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-21-1)>>> data = vbt.YFData.pull("BTC-USD")
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-22-1)>>> %%timeit 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-22-2)>>> for n in range(1000):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-22-3)... pf = vbt.PF.from_random_signals(data, n=n, save_returns=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-22-4)... pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-22-5)15 s ± 829 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]

 1. 

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-23-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-23-2)>>> pf = vbt.PF.from_random_signals(data, n=np.arange(1000).tolist(), save_returns=False)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-23-3)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-23-4)855 ms ± 6.26 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-24-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-24-2)>>> pf = vbt.PF.from_random_signals(data, n=np.arange(1000).tolist(), save_returns=True)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-24-3)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-24-4)593 ms ± 7.07 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
[/code]


# Cash deposits[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#cash-deposits "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Cash can be deposited and withdrawn at any time.

DCA $10 into Bitcoin each month
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-2)>>> cash_deposits = data.symbol_wrapper.fill(0.0)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-3)>>> month_start_mask = ~data.index.tz_convert(None).to_period("M").duplicated()
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-4)>>> cash_deposits[month_start_mask] = 10
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-5)>>> pf = vbt.PF.from_orders(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-6)... data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-7)... init_cash=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-8)... cash_deposits=cash_deposits
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-11)>>> pf.input_value 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-12)1020.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-13)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-14)>>> pf.final_value
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-25-15)20674.328828315127
 
[/code]

 1. 


# Cash earnings[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#cash-earnings "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Cash can be continuously earned or spent depending on the current position.

Backtest Apple without and with dividend reinvestment
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-1)>>> data = vbt.YFData.pull("AAPL", start="2010")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-2)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-3)>>> pf_kept = vbt.PF.from_holding( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-4)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-5)... cash_dividends=data.get("Dividends")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-7)>>> pf_kept.cash.iloc[-1] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-8)93.9182408043298
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-9)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-10)>>> pf_kept.assets.iloc[-1] 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-11)15.37212731743495
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-12)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-13)>>> pf_reinvested = vbt.PF.from_orders( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-14)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-15)... cash_dividends=data.get("Dividends")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-17)>>> pf_reinvested.cash.iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-18)0.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-19)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-20)>>> pf_reinvested.assets.iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-21)18.203284859405468
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-22)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-23)>>> fig = pf_kept.value.rename("Value (kept)").vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-24)>>> pf_reinvested.value.rename("Value (reinvested)").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-26-25)>>> fig.show()
 
[/code]

 1. 2. 3. 4. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/dividends.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/features/dividends.dark.svg#only-dark)


# In-outputs[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#in-outputs "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Portfolio can now take and return any user-defined arrays filled during the simulation, such as signals. In-output arrays can broadcast together with regular arrays using templates and broadcastable named arguments. Additionally, VBT will (semi-)automatically figure out how to correctly wrap and index each array, for example, whenever you select a column from the entire portfolio.

Track the debt of a random portfolio during the simulation
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-1)>>> data = vbt.YFData.pull(["BTC-USD", "ETH-USD"], missing_index="drop")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-2)>>> size = data.symbol_wrapper.fill(np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-3)>>> rand_indices = np.random.choice(np.arange(len(size)), 10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-4)>>> size.iloc[rand_indices[0::2]] = -np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-5)>>> size.iloc[rand_indices[1::2]] = np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-6)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-7)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-8)... def post_segment_func_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-9)... for col in range(c.from_col, c.to_col):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-10)... col_debt = c.last_debt[col]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-11)... c.in_outputs.debt[c.i, col] = col_debt
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-12)... if col_debt > c.in_outputs.max_debt[col]:
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-13)... c.in_outputs.max_debt[col] = col_debt
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-14)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-15)>>> pf = vbt.PF.from_def_order_func(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-16)... data.close, 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-17)... size=size,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-18)... post_segment_func_nb=post_segment_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-19)... in_outputs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-20)... debt=vbt.RepEval("np.empty_like(close)"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-21)... max_debt=vbt.RepEval("np.full(close.shape[1], 0.)")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-22)... ) 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-23)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-24)>>> pf.get_in_output("debt") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-25)symbol BTC-USD ETH-USD
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-26)Date 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-27)2017-11-09 00:00:00+00:00 0.000000 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-28)2017-11-10 00:00:00+00:00 0.000000 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-29)2017-11-11 00:00:00+00:00 0.000000 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-30)2017-11-12 00:00:00+00:00 0.000000 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-31)2017-11-13 00:00:00+00:00 0.000000 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-32)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-33)2023-02-08 00:00:00+00:00 43.746892 25.054571
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-34)2023-02-09 00:00:00+00:00 43.746892 25.054571
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-35)2023-02-10 00:00:00+00:00 43.746892 25.054571
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-36)2023-02-11 00:00:00+00:00 43.746892 25.054571
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-37)2023-02-12 00:00:00+00:00 43.746892 25.054571
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-38)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-39)[1922 rows x 2 columns]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-40)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-41)>>> pf.get_in_output("max_debt") 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-42)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-43)BTC-USD 75.890464
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-44)ETH-USD 25.926328
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-27-45)Name: max_debt, dtype: float64
 
[/code]

 1. 2. 3. 


# Flexible attributes[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#flexible-attributes "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * Portfolio attributes can now be partly or even entirely computed from user-defined arrays. This allows great control of post-simulation analysis, for example, to override some simulation data, to test hyperparameters without having to re-simulate the entire portfolio, or to avoid repeated reconstruction when caching is disabled.

Compute the net exposure by caching its components
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-2)>>> pf = vbt.PF.from_random_signals(data.close, n=100)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-3)>>> value = pf.get_value() 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-4)>>> long_exposure = vbt.PF.get_gross_exposure( 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-5)... asset_value=pf.get_asset_value(direction="longonly"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-6)... value=value,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-7)... wrapper=pf.wrapper
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-9)>>> short_exposure = vbt.PF.get_gross_exposure(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-10)... asset_value=pf.get_asset_value(direction="shortonly"),
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-11)... value=value,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-12)... wrapper=pf.wrapper
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-14)>>> del value 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-15)>>> net_exposure = vbt.PF.get_net_exposure(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-16)... long_exposure=long_exposure,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-17)... short_exposure=short_exposure,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-18)... wrapper=pf.wrapper
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-19)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-20)>>> del long_exposure
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-21)>>> del short_exposure
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-22)>>> net_exposure
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-23)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-24)2014-09-17 00:00:00+00:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-25)2014-09-18 00:00:00+00:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-26)2014-09-19 00:00:00+00:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-27)2014-09-20 00:00:00+00:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-28)2014-09-21 00:00:00+00:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-29) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-30)2023-02-08 00:00:00+00:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-31)2023-02-09 00:00:00+00:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-32)2023-02-10 00:00:00+00:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-33)2023-02-11 00:00:00+00:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-34)2023-02-12 00:00:00+00:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-28-35)Freq: D, Length: 3071, dtype: float64
 
[/code]

 1. 2. 3. 


# Shortcut properties[¶](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#shortcut-properties "Permanent link")

![](https://vectorbt.pro/pvt_7a467f6b/assets/badges/new-in/1_0_0.svg)

 * [In-output arrays](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#in-outputs) can be used to override regular portfolio attributes. Portfolio will automatically pick the pre-computed array and perform all future calculations using this array, without wasting time on its reconstruction.

Modify the returns from within the simulation
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-1)>>> data = vbt.YFData.pull("BTC-USD")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-2)>>> size = data.symbol_wrapper.fill(np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-3)>>> rand_indices = np.random.choice(np.arange(len(size)), 10)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-4)>>> size.iloc[rand_indices[0::2]] = -np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-5)>>> size.iloc[rand_indices[1::2]] = np.inf
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-6)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-7)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-8)... def post_segment_func_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-9)... for col in range(c.from_col, c.to_col):
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-10)... return_now = c.last_return[col]
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-11)... return_now = 0.5 * return_now if return_now > 0 else return_now
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-12)... c.in_outputs.returns[c.i, col] = return_now
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-13)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-14)>>> pf = vbt.PF.from_def_order_func(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-15)... data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-16)... size=size,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-17)... size_type="targetpercent",
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-18)... post_segment_func_nb=post_segment_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-19)... in_outputs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-20)... returns=vbt.RepEval("np.empty_like(close)")
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-21)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-23)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-24)>>> pf.returns 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-25)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-26)2014-09-17 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-27)2014-09-18 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-28)2014-09-19 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-29)2014-09-20 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-30)2014-09-21 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-31) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-32)2023-02-08 00:00:00+00:00 -0.015227
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-33)2023-02-09 00:00:00+00:00 -0.053320
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-34)2023-02-10 00:00:00+00:00 -0.008439
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-35)2023-02-11 00:00:00+00:00 0.005569 << modified
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-36)2023-02-12 00:00:00+00:00 0.001849 << modified
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-37)Freq: D, Length: 3071, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-38)
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-39)>>> pf.get_returns() 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-40)Date
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-41)2014-09-17 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-42)2014-09-18 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-43)2014-09-19 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-44)2014-09-20 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-45)2014-09-21 00:00:00+00:00 0.000000
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-46) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-47)2023-02-08 00:00:00+00:00 -0.015227
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-48)2023-02-09 00:00:00+00:00 -0.053320
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-49)2023-02-10 00:00:00+00:00 -0.008439
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-50)2023-02-11 00:00:00+00:00 0.011138
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-51)2023-02-12 00:00:00+00:00 0.003697
 [](https://vectorbt.pro/pvt_7a467f6b/features/portfolio/#__codelineno-29-52)Freq: D, Length: 3071, dtype: float64
 
[/code]

 1. 2. 

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/features/portfolio.py.txt)