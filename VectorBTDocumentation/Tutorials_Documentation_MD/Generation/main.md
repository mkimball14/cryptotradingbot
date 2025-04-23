# Generation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#generation "Permanent link")

Signals are an additional level of abstraction added on top of orders: instead of specifying every bit of information on what needs to be ordered at each timestamp, we can first decide on what a typical order should look like, and then choose the timing of issuing such an order. The latter decision process can be realized through signals, which in the vectorbt's world are represented by a boolean mask where `True` means "order" and `False` means "no order". Additionally, we can change the meaning of each signal statically, or dynamically based on the current simulation state; for example, we can instruct the simulator to ignore an "order" signal if we're already in the market, which cannot be done by using the "from-orders" method alone. Finally, vectorbt loves data science, and so comparing multiple strategies with the same trading conditions but different signal permutations (i.e., order timings and directions) is much easier, less error-prone, and generally leads to fairer experiments.

Since we constantly buy and sell things, the ideal scenario would be to incorporate an order direction into each signal as well. But we cannot represent three states ("order to buy", "order to sell", and "no order") by using booleans - a data type with just two values. Thus, signals are usually distributed across two or more boolean arrays, where each array represents a different decision dimension. The most popular way to define signals is by using two direction-unaware arrays: ![1⃣](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/31-20e3.svg) entries and ![2⃣](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/32-20e3.svg) exits. Those two arrays have a different meaning based on the direction specified using a separate variable. For instance, when only the long direction is enabled, an entry signal opens a new long position and an exit signal closes it; when both directions are enabled, an entry signal opens a new long position and an exit signal reverses it to open a short one. To better control the decision on whether to reverse the current position or just close it out, we can define four direction-aware arrays: ![1⃣](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/31-20e3.svg) long entries, ![2⃣](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/32-20e3.svg) long exits, ![3⃣](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/33-20e3.svg) short entries, and ![4⃣](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/34-20e3.svg) short exits, which guarantees the most flexibility.

For example, to open a long position, close it, open a short position, and reverse it, the signals would look like this:

Long entry | Long exit | Short entry | Short exit 
---|---|---|--- 
True | False | False | False 
False | True | False | False 
False | False | True | False 
True | False | False | False 
 
The same strategy can be also defined using an entry signal, an exit signal, and a direction:

Entry | Exit | Direction 
---|---|--- 
True | False | Long only 
False | True | Long only 
True/False | False/True | Short only/Both 
True | False | Long only/Both 
 
Info

Direction-unaware signals can be easily translated into direction-aware signals:

 * True, True, Long only True, True, False, False
 * True, True, Short only False, False, True, True
 * True, True, Both True, False, True, False

But direction-aware signals cannot be translated into direction-unaware signals if both directions are enabled and there is an exit signal present:

 * False, True, False, True ![❓](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2753.svg)

Thus, we need to evaluate in detail which conditions we're interested in before generating signals.

But why not choosing an integer data type where a positive number means "order to buy", negative number means "order to sell", and zero means "no order", like done in backtrader, for example? Boolean arrays are much easier to generate and maintain by the user, but also, a boolean NumPy array requires 8x less memory than a 64-bit signed integer NumPy array. Furthermore, it's so much more convenient to combine and analyze masks than integer arrays! For example, we can use the _logical OR_ (`|` in NumPy) operation to combine two masks, or sum the elements in a mask to get the number of signals since booleans are a subtype of integers and behave just like regular integers in most math expressions.


# Comparison[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#comparison "Permanent link")

Generating signals properly can sometimes be orders of magnitude more difficult than simulating them. This is because we have to take into account not only their distribution, but also how they interact across multiple boolean arrays. For example, setting both an entry and an exit at the same timestamp will effectively eliminate both. That's why vectorbt deploys numerous functions and techniques to support us in this regard.

Signal generation usually starts with comparing two or more numeric arrays. Remember that by comparing entire arrays, we're iterating over each row and column (= element) in a vectorized manner, and compare their scalar values at that one element. So, essentially, we're just running the same comparison operation on each single element across all the arrays that are being compared together. Let's start our first example with Bollinger Bands run on two separate assets. At each timestamp, we'll place a signal whenever the low price is below the lower band, with an expectation that the price will reverse back to its rolling mean:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-3)>>> data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-4)... ["BTCUSDT", "ETHUSDT"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-5)... start="2021-01-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-6)... end="2022-01-01"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-8)>>> data.get("Low")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-9)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-10)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-11)2021-01-01 00:00:00+00:00 28624.57 714.29
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-12)2021-01-02 00:00:00+00:00 28946.53 714.91
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-13)2021-01-03 00:00:00+00:00 31962.99 768.71
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-14)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-15)2021-12-29 00:00:00+00:00 46096.99 3604.20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-16)2021-12-30 00:00:00+00:00 45900.00 3585.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-17)2021-12-31 00:00:00+00:00 45678.00 3622.29
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-19)[365 rows x 2 columns]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-20)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-21)>>> bb = vbt.talib("BBANDS").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-22)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-23)... timeperiod=vbt.Default(14), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-24)... nbdevup=vbt.Default(2),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-25)... nbdevdn=vbt.Default(2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-27)>>> bb.lowerband 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-28)symbol BTC-USD ETH-USD
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-29)Date 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-30)2021-04-23 00:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-31)2021-04-24 00:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-32)2021-04-25 00:00:00+00:00 NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-33)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-34)2022-04-21 00:00:00+00:00 38987.326323 2912.894415
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-35)2022-04-22 00:00:00+00:00 38874.059308 2898.681307
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-36)2022-04-23 00:00:00+00:00 38915.417003 2903.756905
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-37)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-38)[366 rows x 2 columns]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-39)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-40)>>> mask = data.get("Low") < bb.lowerband 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-41)>>> mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-42)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-43)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-44)2021-01-01 00:00:00+00:00 False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-45)2021-01-02 00:00:00+00:00 False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-46)2021-01-03 00:00:00+00:00 False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-47)... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-48)2021-12-29 00:00:00+00:00 False True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-49)2021-12-30 00:00:00+00:00 False True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-50)2021-12-31 00:00:00+00:00 False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-51)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-52)[365 rows x 2 columns]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-53)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-54)>>> mask.sum() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-55)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-56)BTCUSDT 36
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-57)ETHUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-0-58)dtype: int64
 
[/code]

 1. 2. 3. 4. 

This operation has generated a mask that has a true value whenever the low price dips below the lower band. Such an array can already be used in simulation! But let's see what happens when we try to compare the lower band that has been generated for multiple combinations of the (upper and lower) multiplier:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-1-1)>>> bb_mult = vbt.talib("BBANDS").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-1-2)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-1-3)... timeperiod=vbt.Default(14),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-1-4)... nbdevup=[2, 3],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-1-5)... nbdevdn=[2, 3] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-1-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-1-7)>>> mask = data.get("Low") < bb_mult.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-1-8)ValueError: Can only compare identically-labeled DataFrame objects
 
[/code]

 1. 

The problem lies in Pandas being unable to compare DataFrames with different columns - the left DataFrame contains the columns `BTCUSDT` and `ETHUSDT` while the right DataFrame coming from the Bollinger Bands indicator now contains the columns `(2, 2, BTCUSDT)`, `(2, 2, ETHUSDT)`, `(3, 3, BTCUSDT)`, and `(3, 3, ETHUSDT)`. So, what's the solution? Right - vectorbt! By appending `vbt` to the _left_ operand, we are comparing the accessor object of type [BaseAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor) instead of the DataFrame itself. This will trigger the so-called [magic method](https://rszalski.github.io/magicmethods/) `__lt__` of that accessor, which takes the DataFrame under the accessor and the DataFrame on the right, and combines them with [BaseAccessor.combine](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.combine) and [numpy.less](https://numpy.org/doc/stable/reference/generated/numpy.less.html) as `combine_func`. This, in turn, will broadcast the shapes and indexes of both DataFrames using the vectorbt's powerful broadcasting mechanism, effectively circumventing the limitation of Pandas.

As the result, vectorbt will compare `(2, 2, BTCUSDT)` and `(3, 3, BTCUSDT)` only with `BTCUSDT` and `(2, 2, ETHSDT)` and `(3, 3, ETHSDT)` only with `ETHSDT`, and this using NumPy - faster!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-1)>>> mask = data.get("Low").vbt < bb_mult.lowerband 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-2)>>> mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-3)bbands_nbdevup 2 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-4)bbands_nbdevdn 2 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-5)symbol BTCUSDT ETHUSDT BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-6)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-7)2021-01-01 00:00:00+00:00 False False False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-8)2021-01-02 00:00:00+00:00 False False False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-9)2021-01-03 00:00:00+00:00 False False False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-10)... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-11)2021-12-29 00:00:00+00:00 False True False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-12)2021-12-30 00:00:00+00:00 False True False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-13)2021-12-31 00:00:00+00:00 False False False False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-15)[365 rows x 4 columns]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-17)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-18)bbands_nbdevup bbands_nbdevdn symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-19)2 2 BTCUSDT 53
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-20) ETHUSDT 48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-21)3 3 BTCUSDT 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-22) ETHUSDT 9
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-2-23)dtype: int64
 
[/code]

 1. 

Note

For vectorbt to be able to compare shapes that are not broadcastable, both DataFrames must have at least one column level in common, such as `symbol` that we had above.

As you might have recalled from the documentation on indicators, each indicator attaches a couple of helper methods for comparison - `{name}_above`, `{name}_equal`, and `{name}_below`, which do basically the same as we did above:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-3-1)>>> mask = bb_mult.lowerband_above(data.get("Low")) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-3-2)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-3-3)bbands_nbdevup bbands_nbdevdn symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-3-4)2 2 BTCUSDT 53
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-3-5) ETHUSDT 48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-3-6)3 3 BTCUSDT 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-3-7) ETHUSDT 9
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-3-8)dtype: int64
 
[/code]

 1. 


# Thresholds[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#thresholds "Permanent link")

To compare a numeric array against two or more scalar thresholds (making them parameter combinations), we can use the same approach by either appending `vbt`, or by calling the method [BaseAccessor.combine](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.combine). Let's calculate the bandwidth of our single-combination indicator, which is the upper band minus the lower band divided by the middle band, and check whether it's higher than two different thresholds:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-1)>>> bandwidth = (bb.upperband - bb.lowerband) / bb.middleband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-3)>>> mask = bandwidth.vbt > vbt.Param([0.15, 0.3], name="threshold") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-4)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-5)threshold symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-6)0.15 BTCUSDT 253
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-7) ETHUSDT 316
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-8)0.30 BTCUSDT 65
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-9) ETHUSDT 136
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-10)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-12)>>> mask = bandwidth.vbt.combine(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-13)... [0.15, 0.3], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-14)... combine_func=np.greater, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-15)... keys=pd.Index([0.15, 0.3], name="threshold") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-17)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-18)threshold symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-19)0.15 BTCUSDT 253
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-20) ETHUSDT 316
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-21)0.30 BTCUSDT 65
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-22) ETHUSDT 136
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-4-23)dtype: int64
 
[/code]

 1. 2. 3. 

The latest example works also on arrays instead of scalars. Or, we can use [pandas.concat](https://pandas.pydata.org/docs/reference/api/pandas.concat.html) to manually stack the results of any comparison to treat them as separate combinations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-1)>>> mask = pd.concat(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-2)... (bandwidth > 0.15, bandwidth > 0.3), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-3)... keys=pd.Index([0.15, 0.3], name="threshold"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-4)... axis=1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-6)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-7)threshold symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-8)0.15 BTCUSDT 253
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-9) ETHUSDT 316
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-10)0.30 BTCUSDT 65
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-11) ETHUSDT 136
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-5-12)dtype: int64
 
[/code]


# Crossovers[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#crossovers "Permanent link")

So far we have touched basic vectorized comparison operations, but there is one operation that comes disproportionally often in technical analysis: crossovers. A crossover refers to a situation where two time series cross each other. There are two ways of finding the crossovers: naive and native. The naive approach compares both time series in a vectorized manner and then selects the first `True` value out of each "partition" of `True` values. A partition in the vectorbt's vocabulary for signal processing is just a bulk of consecutive `True` values produced by the comparison. While we already know how to do the first operation, the second one can be achieved with the help of the accessor for signals - [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor), accessible via the attribute `vbt.signals` on any Pandas object.

In particular, we will be using the method [SignalsAccessor.first](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first), which takes a mask, assigns a rank to each `True` value in each partition using [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank) (enumerated from 0 to the length of the respective partition), and then keeps only those `True` values that have the rank 0. Let's get the crossovers of the lower price dipping below the lower band:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-6-1)>>> low_below_lband = data.get("Low") < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-6-2)>>> mask = low_below_lband.vbt.signals.first()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-6-3)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-6-4)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-6-5)BTCUSDT 21
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-6-6)ETHUSDT 20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-6-7)dtype: int64
 
[/code]

To make sure that the operation was successful, let's plot the `BTCUSDT` column of both time series using [GenericAccessor.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot) and the generated signals using [SignalsSRAccessor.plot_as_markers](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_markers):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-1)>>> btc_low = data.get("Low", "BTCUSDT").rename("Low") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-2)>>> btc_lowerband = bb.lowerband["BTCUSDT"].rename("Lower Band")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-3)>>> btc_mask = mask["BTCUSDT"].rename("Signals")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-5)>>> fig = btc_low.vbt.plot() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-6)>>> btc_lowerband.vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-7)>>> btc_mask.vbt.signals.plot_as_markers(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-8)... y=btc_low, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-9)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-10)... marker=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-11)... color="#DFFF00"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-13)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-14)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-15)... ) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-7-16)>>> fig.show()
 
[/code]

 1. 2. 3. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/crossovers.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/crossovers.dark.svg#only-dark)

Hint

To wait for a confirmation, use [SignalsAccessor.nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth) to select the n-th signal in each partition.

But here's the catch: if the first low value is already below the first lower band value, it will also yield a crossover signal. To fix that, we need to pass `after_false=True`, which will discard the first partition if there is no `False` value before it.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-8-1)>>> mask = low_below_lband.vbt.signals.first(after_false=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-8-2)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-8-3)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-8-4)BTCUSDT 21
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-8-5)ETHUSDT 20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-8-6)dtype: int64
 
[/code]

And here's another catch: if the first bunch of values in the indicator are NaN, which results in `False` values in the mask, and the first value after the last NaN yields `True`, then the `after_false` argument becomes ineffective. To account for this, we need to manually set those values in the mask to `True`. Let's illustrate this issue on sample data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-1)>>> sample_low = pd.Series([10, 9, 8, 9, 8])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-2)>>> sample_lband = pd.Series([np.nan, np.nan, 9, 8, 9])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-3)>>> sample_mask = sample_low < sample_lband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-4)>>> sample_mask.vbt.signals.first(after_false=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-5)0 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-6)1 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-7)2 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-8)3 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-9)4 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-10)dtype: bool
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-12)>>> sample_mask[sample_lband.ffill().isnull()] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-13)>>> sample_mask.vbt.signals.first(after_false=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-14)0 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-15)1 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-16)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-17)3 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-18)4 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-9-19)dtype: bool
 
[/code]

 1. 2. 

Or, we can remove the buffer, do the operation, and then add the buffer back:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-1)>>> buffer = sample_lband.ffill().isnull().sum(axis=0).max() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-2)>>> buffer
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-3)2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-5)>>> sample_buf_mask = sample_low.iloc[buffer:] < sample_lband.iloc[buffer:]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-6)>>> sample_buf_mask = sample_buf_mask.vbt.signals.first(after_false=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-7)>>> sample_mask = sample_low.vbt.wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-8)>>> sample_mask.loc[sample_buf_mask.index] = sample_buf_mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-9)>>> sample_mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-10)0 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-11)1 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-12)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-13)3 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-14)4 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-10-15)dtype: bool
 
[/code]

 1. 

Info

We can apply the buffer-exclusive approach introduced above to basically any operation in vectorbt.

But here comes another issue: what happens if our data contains gaps and we encounter a NaN in the middle of a partition? We should make the second part of the partition `False` as forward-filling that NaN value would make waiting for a confirmation problematic. But also, doing so many operations on bigger arrays just for getting the crossovers is quite resource-expensive. Gladly, vectorbt deploys its own Numba-compiled function [crossed_above_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/base/#vectorbtpro.generic.nb.base.crossed_above_nb) for finding the crossovers in an iterative manner, which is the second, native way. To use this function, we can use the methods [GenericAccessor.crossed_above](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_above) and [GenericAccessor.crossed_below](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_below), accessible via the attribute `vbt` on any Pandas object:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-11-1)>>> mask = data.get("Low").vbt.crossed_below(bb.lowerband, wait=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-11-2)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-11-3)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-11-4)BTCUSDT 15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-11-5)ETHUSDT 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-11-6)dtype: int64
 
[/code]

 1. 

Info

If the time series crosses back during the confirmation period `wait`, the signal won't be set. To set the signal anyway, use forward shifting.

As with other comparison methods, each indicator has the helper methods `{name}_crossed_above` and `{name}_crossed_below` for generating the crossover masks:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-12-1)>>> mask = bb.lowerband_crossed_above(data.get("Low"), wait=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-12-2)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-12-3)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-12-4)BTCUSDT 15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-12-5)ETHUSDT 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-12-6)dtype: int64
 
[/code]


# Logical operators[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#logical-operators "Permanent link")

Once we've generated two or more masks (conditions), we can combine them into a single mask using logical operators. Common logical operators include 

 * _AND_ (`&` or [numpy.logical_and](https://numpy.org/doc/stable/reference/generated/numpy.logical_and.html)): for each element, returns True whenever all the conditions are True
 * _OR_ (`|` or [numpy.logical_or](https://numpy.org/doc/stable/reference/generated/numpy.logical_or.html)): for each element, returns True whenever any of the conditions are True
 * _NOT_ (`~` or [numpy.logical_not](https://numpy.org/doc/stable/reference/generated/numpy.logical_not.html)): for each element, returns True whenever the condition is False
 * _XOR_ (`^` or [numpy.logical_xor](https://numpy.org/doc/stable/reference/generated/numpy.logical_xor.html)): for each element, returns True whenever only one of the conditions is True

Note

Do not use `and`, `or`, or `not` on arrays - they only work on single boolean values! For example, instead of `mask1 and mask2` use `mask1 & mask2`, instead of `mask1 or mask2` use `mask1 | mask2`, and instead of `not mask` use `~mask`.

For example, let's combine four conditions for a signal: the low price dips below the lower band _AND_ the bandwidth is above some threshold (= a downward breakout while expanding), _OR_ , the high price rises above the upper band _AND_ the bandwidth is below some threshold (= an upward breakout while squeezing):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-1)>>> cond1 = data.get("Low") < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-2)>>> cond2 = bandwidth > 0.3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-3)>>> cond3 = data.get("High") > bb.upperband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-4)>>> cond4 = bandwidth < 0.15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-6)>>> mask = (cond1 & cond2) | (cond3 & cond4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-7)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-8)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-9)BTCUSDT 25
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-10)ETHUSDT 13
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-13-11)dtype: int64
 
[/code]

To test multiple thresholds and to broadcast exclusively using vectorbt:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-1)>>> cond1 = data.get("Low").vbt < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-2)>>> cond2 = bandwidth.vbt > vbt.Param([0.3, 0.3, 0.4, 0.4], name="cond2_th") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-3)>>> cond3 = data.get("High").vbt > bb.upperband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-4)>>> cond4 = bandwidth.vbt < vbt.Param([0.1, 0.2, 0.1, 0.2], name="cond4_th") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-6)>>> mask = (cond1.vbt & cond2).vbt | (cond3.vbt & cond4) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-7)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-8)cond2_th cond4_th symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-9)0.3 0.1 BTCUSDT 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-10) ETHUSDT 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-11) 0.2 BTCUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-12) ETHUSDT 27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-13)0.4 0.1 BTCUSDT 9
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-14) ETHUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-15) 0.2 BTCUSDT 26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-16) ETHUSDT 22
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-14-17)dtype: int64
 
[/code]

 1. 2. 3. 


# Cartesian product[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#cartesian-product "Permanent link")

Combining two or more arrays using a Cartesian product is a bit more complex since every array has the column level `symbol` that shouldn't be combined with itself. But here's the trick. First, convert the columns of each array into their integer positions. Then, split each position array into "blocks" (smaller arrays). Blocks will be combined with each other, but the positions within each block won't; that is, each block acts as a parameter combination. Combine then all blocks using a combinatorial function of choice (see [itertools](https://docs.python.org/3/library/itertools.html) for various options, or [generate_param_combs](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.generate_param_combs)), and finally, flatten each array with blocks and use it for column selection. Sounds complex? Yes. Difficult to implement? No!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-1)>>> cond1 = data.get("Low").vbt < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-2)>>> cond2 = bandwidth.vbt > vbt.Param([0.3, 0.4], name="cond2_th") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-3)>>> cond3 = data.get("High").vbt > bb.upperband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-4)>>> cond4 = bandwidth.vbt < vbt.Param([0.1, 0.2], name="cond4_th")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-6)>>> i1 = np.split(np.arange(len(cond1.columns)), len(cond1.columns) // 2) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-7)>>> i2 = np.split(np.arange(len(cond2.columns)), len(cond2.columns) // 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-8)>>> i3 = np.split(np.arange(len(cond3.columns)), len(cond3.columns) // 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-9)>>> i4 = np.split(np.arange(len(cond4.columns)), len(cond4.columns) // 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-11)>>> i1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-12)[array([0, 1])]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-13)>>> i2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-14)[array([0, 1]), array([2, 3])]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-15)>>> i3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-16)[array([0, 1])]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-17)>>> i4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-18)[array([0, 1]), array([2, 3])]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-19)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-20)>>> i1, i2, i3, i4 = zip(*product(i1, i2, i3, i4)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-21)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-22)>>> i1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-23)(array([0, 1]), array([0, 1]), array([0, 1]), array([0, 1]))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-24)>>> i2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-25)(array([0, 1]), array([0, 1]), array([2, 3]), array([2, 3]))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-26)>>> i3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-27)(array([0, 1]), array([0, 1]), array([0, 1]), array([0, 1]))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-28)>>> i4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-29)(array([0, 1]), array([2, 3]), array([0, 1]), array([2, 3]))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-31)>>> i1 = np.asarray(i1).flatten() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-32)>>> i2 = np.asarray(i2).flatten()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-33)>>> i3 = np.asarray(i3).flatten()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-34)>>> i4 = np.asarray(i4).flatten()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-35)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-36)>>> i1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-37)[0 1 0 1 0 1 0 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-38)>>> i2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-39)[0 1 0 1 2 3 2 3]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-40)>>> i3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-41)[0 1 0 1 0 1 0 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-42)>>> i4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-43)[0 1 2 3 0 1 2 3]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-44)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-45)>>> cond1 = cond1.iloc[:, i1] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-46)>>> cond2 = cond2.iloc[:, i2]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-47)>>> cond3 = cond3.iloc[:, i3]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-48)>>> cond4 = cond4.iloc[:, i4]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-49)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-50)>>> mask = (cond1.vbt & cond2).vbt | (cond3.vbt & cond4) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-51)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-52)cond2_th cond4_th symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-53)0.3 0.1 BTCUSDT 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-54) ETHUSDT 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-55) 0.2 BTCUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-56) ETHUSDT 27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-57)0.4 0.1 BTCUSDT 9
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-58) ETHUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-59) 0.2 BTCUSDT 26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-60) ETHUSDT 22
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-15-61)dtype: int64
 
[/code]

 1. 2. 3. 4. 5. 6. 

In newer versions of VBT the same effect can be achieved with a single call of [BaseAccessor.cross](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.cross):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-16-1)>>> cond1 = data.get("Low").vbt < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-16-2)>>> cond2 = bandwidth.vbt > vbt.Param([0.3, 0.4], name="cond2_th")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-16-3)>>> cond3 = data.get("High").vbt > bb.upperband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-16-4)>>> cond4 = bandwidth.vbt < vbt.Param([0.1, 0.2], name="cond4_th")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-16-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-16-6)>>> cond1, cond2, cond3, cond4 = vbt.pd_acc.x(cond1, cond2, cond3, cond4) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-16-7)>>> mask = (cond1.vbt & cond2).vbt | (cond3.vbt & cond4)
 
[/code]

 1. 

But probably an easier and less error-prone approach would be to build an indicator that would handle parameter combinations for us ![😁](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f601.svg)

For this, we will write an indicator expression similar to the code we wrote for a single parameter combination, and use [IndicatorFactory.from_expr](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_expr) to auto-build an indicator by parsing that expression. The entire logic including the specification of all inputs, parameters, and outputs is encapsulated in the expression itself. We'll use the annotation `@res_talib_bbands` to resolve the specification of the inputs and parameters expected by the TA-Lib's `BBANDS` indicator and "copy" them over to our indicator by also prepending the prefix `talib` to the parameter names. Then, we will perform our usual signal generation logic by substituting the custom parameters `cond2_th` and `cond4_th` with their single values, and return the whole thing as an output `mask` annotated accordingly.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-1)>>> MaskGenerator = vbt.IF.from_expr("""
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-2)... upperband, middleband, lowerband = @res_talib_bbands
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-3)... bandwidth = (upperband - lowerband) / middleband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-4)... cond1 = low < lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-5)... cond2 = bandwidth > @p_cond2_th
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-6)... cond3 = high > upperband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-7)... cond4 = bandwidth < @p_cond4_th
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-8)... @out_mask:(cond1 & cond2) | (cond3 & cond4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-9)... """)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-11)>>> vbt.phelp(MaskGenerator.run, incl_doc=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-12)Indicator.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-13) high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-14) low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-15) close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-16) cond2_th,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-17) cond4_th,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-18) bbands_timeperiod=Default(value=5),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-19) bbands_nbdevup=Default(value=2),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-20) bbands_nbdevdn=Default(value=2),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-21) bbands_matype=Default(value=0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-22) bbands_timeframe=Default(value=None),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-23) short_name='custom',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-24) hide_params=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-25) hide_default=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-26) **kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-27))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-28)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-29)>>> mask_generator = MaskGenerator.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-30)... high=data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-31)... low=data.get("Low"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-32)... close=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-33)... cond2_th=[0.3, 0.4],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-34)... cond4_th=[0.1, 0.2],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-35)... bbands_timeperiod=vbt.Default(14),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-36)... param_product=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-37)... ) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-38)>>> mask_generator.mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-39)custom_cond2_th custom_cond4_th symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-40)0.3 0.1 BTCUSDT 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-41) ETHUSDT 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-42) 0.2 BTCUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-43) ETHUSDT 27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-44)0.4 0.1 BTCUSDT 9
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-45) ETHUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-46) 0.2 BTCUSDT 26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-47) ETHUSDT 22
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-17-48)dtype: int64
 
[/code]

 1. 2. 

Info

Even though the indicator factory has "indicator" in its name, we can use it to generate signals just as well. This is because signals are just boolean arrays that also guarantee to be of the input shape.


# Shifting[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#shifting "Permanent link")

To compare the current value to any previous (not future!) value, we can use forward shifting. Also, we can use it to shift the final mask to postpone the order execution. For example, let's generate a signal whenever the low price dips below the lower band _AND_ the bandwidth change (i.e., the difference between the current and the previous bandwidth) is positive:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-1)>>> cond1 = data.get("Low") < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-2)>>> cond2 = bandwidth > bandwidth.shift(1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-4)>>> mask = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-5)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-6)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-7)BTCUSDT 42
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-8)ETHUSDT 39
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-18-9)dtype: int64
 
[/code]

 1. 

Important

Never attempt to shift backwards to avoid the look-ahead bias! Use either a positive number in [DataFrame.shift](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html), or the vectorbt's accessor method [GenericAccessor.fshift](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.fshift).

Another way to shift observations is by selecting the first observation in a rolling window. This is particularly useful when the rolling window has a variable size, for example, based on a frequency. Let's do the same as above but determine the change in the bandwidth in relation to one week ago instead of yesterday:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-19-1)>>> cond2 = bandwidth > bandwidth.rolling("7d").apply(lambda x: x[0])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-19-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-19-3)>>> mask = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-19-4)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-19-5)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-19-6)BTCUSDT 33
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-19-7)ETHUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-19-8)dtype: int64
 
[/code]

Hint

Using variable windows instead of fixed ones should be preferred if your data has gaps.

The approach above is a move in the right direction, but it introduces two potential issues: all windows will be either 6 days long or less, while the performance of rolling and applying such a custom Python function using Pandas is not satisfactory, to say the least. The first issue can be solved by rolling a window of 8 days, and checking the timestamp of the first observation being exactly 7 days behind the current timestamp:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-1)>>> def exactly_ago(sr): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-2)... if sr.index[0] == sr.index[-1] - vbt.timedelta("7d"):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-3)... return sr.iloc[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-4)... return np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-6)>>> cond_7d_ago = bandwidth.rolling("8d").apply(exactly_ago, raw=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-7)>>> cond2 = bandwidth > cond_7d_ago
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-9)>>> mask = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-10)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-11)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-12)BTCUSDT 29
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-13)ETHUSDT 26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-20-14)dtype: int64
 
[/code]

 1. 

The second issue can be solved by looping with Numba. However, the main challenge lies in solving those two issues simultaneously because we want to access the timestamp of the first observation, which requires us to work on a Pandas Series instead of a NumPy array, and Numba cannot work on Pandas Series ![😑](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f611.svg)

Thus, we will use the vectorbt's accessor method [GenericAccessor.rolling_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_apply), which offers two modes: regular and meta. The regular mode rolls over the data of a Pandas object just like Pandas does it, and does not give us any information about the current window ![🙅](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f645.svg) The meta mode rolls over the **metadata** of a Pandas object, so we can easily select the data from any array corresponding to the current window ![👌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f44c.svg)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-2)... def exactly_ago_meta_nb(from_i, to_i, col, index, freq, arr): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-3)... if index[from_i] == index[to_i - 1] - freq: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-4)... return arr[from_i, col] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-5)... return np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-7)>>> cond_7d_ago = vbt.pd_acc.rolling_apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-8)... "8d",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-9)... exactly_ago_meta_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-10)... bandwidth.index.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-11)... vbt.timedelta("7d").to_timedelta64(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-12)... vbt.to_2d_array(bandwidth),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-13)... wrapper=bandwidth.vbt.wrapper 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-15)>>> cond2 = bandwidth > cond_7d_ago
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-17)>>> mask = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-18)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-19)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-20)BTCUSDT 29
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-21)ETHUSDT 26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-21-22)dtype: int64
 
[/code]

 1. 2. 3. 4. 5. 

And if this approach (rightfully) intimidates you, there is a dead simple method [GenericAccessor.ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ago), which is capable of forward-shifting the array using any delta:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-1)>>> cond2 = bandwidth > bandwidth.vbt.ago("7d")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-3)>>> mask = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-4)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-5)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-6)BTCUSDT 29
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-7)ETHUSDT 26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-8)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-10)>>> bandwidth.iloc[-8]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-11)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-12)BTCUSDT 0.125477
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-13)ETHUSDT 0.096458
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-14)Name: 2021-12-24 00:00:00+00:00, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-16)>>> bandwidth.vbt.ago("7d").iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-17)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-18)BTCUSDT 0.125477
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-19)ETHUSDT 0.096458
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-22-20)Name: 2021-12-31 00:00:00+00:00, dtype: float64
 
[/code]

Hint

This method returns exact matches. In a case where the is no exact match, the value will be NaN. To return the previous index value instead, pass `method="ffill"`. The method also accepts a sequence of deltas that will be applied on the per-element basis.


# Truth value testing[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#truth-value-testing "Permanent link")

But what if we want to test whether a certain condition was met during a certain period of time in the past? For this, we need to create an expanding or a rolling window, and do truth value testing using [numpy.any](https://numpy.org/doc/stable/reference/generated/numpy.any.html) or [numpy.all](https://numpy.org/doc/stable/reference/generated/numpy.all.html) within this window. But since Pandas doesn't implement the rolling aggregation using `any` and `all`, we need to be more creative and treat booleans as integers: use `max` for a logical _OR_ and `min` for a logical _AND_. Also, don't forget to cast the resulting array to a boolean data type to generate a valid mask.

Let's place a signal whenever the low price goes below the lower band _AND_ there was a downward crossover of the close price with the middle band in the past 5 candles:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-1)>>> cond2 = data.get("Close").vbt.crossed_below(bb.middleband)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-2)>>> cond2 = cond2.rolling(5, min_periods=1).max().astype(bool)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-4)>>> mask = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-5)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-6)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-7)BTCUSDT 36
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-8)ETHUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-23-9)dtype: int64
 
[/code]

Note

Be cautious when setting `min_periods` to a higher number and converting to a boolean data type: each NaN will become `True`. Thus, at least replace NaNs with zeros before casting.

If the window size is fixed, we can also use [GenericAccessor.rolling_any](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_any) and [GenericAccessor.rolling_all](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_all), which are tailored for computing rolling truth testing operations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-1)>>> cond2 = data.get("Close").vbt.crossed_below(bb.middleband)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-2)>>> cond2 = cond2.vbt.rolling_any(5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-4)>>> mask = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-5)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-6)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-7)BTCUSDT 36
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-8)ETHUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-24-9)dtype: int64
 
[/code]

Another way of doing the same rolling operations is by using the accessor method [GenericAccessor.rolling_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_apply) and specifying `reduce_func_nb` as "any" or "all" string. We should use the argument `wrap_kwargs` to instruct vectorbt to fill NaNs with `False` and change the data type. This method allows flexible windows to be passed. Again, let's roll a window of 5 days:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-1)>>> cond2 = data.get("Close").vbt.crossed_below(bb.middleband)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-2)>>> cond2 = cond2.vbt.rolling_apply(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-3)... "5d", "any", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-4)... minp=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-5)... wrap_kwargs=dict(fillna=0, dtype=bool)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-8)>>> mask = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-9)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-10)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-11)BTCUSDT 36
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-12)ETHUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-25-13)dtype: int64
 
[/code]

 1. 

Let's do something more complex: check whether the bandwidth contracted to 10% or less at any point during a month using an expanding window, and reset the window at the beginning of the next month; this way, we make the first timestamp of the month a time anchor for our condition. For this, we'll overload the vectorbt's resampling logic, which allows aggregating values by mapping any source index (anchor points in our example) to any target index (our index).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-1)>>> anchor_points = data.wrapper.get_index_points( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-2)... every="M", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-3)... start=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-4)... exact_start=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-6)>>> anchor_points
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-7)array([ 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-9)>>> left_bound = np.full(len(data.wrapper.index), np.nan) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-10)>>> left_bound[anchor_points] = anchor_points
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-11)>>> left_bound = vbt.nb.ffill_1d_nb(left_bound).astype(int_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-12)>>> left_bound = bandwidth.index[left_bound]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-13)>>> left_bound
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-14)DatetimeIndex(['2021-01-01 00:00:00+00:00', '2021-01-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-15) '2021-01-01 00:00:00+00:00', '2021-01-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-16) '2021-01-01 00:00:00+00:00', '2021-01-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-17) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-18) '2021-12-01 00:00:00+00:00', '2021-12-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-19) '2021-12-01 00:00:00+00:00', '2021-12-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-20) '2021-12-01 00:00:00+00:00', '2021-12-01 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-21) dtype='datetime64[ns, UTC]', ...)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-22)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-23)>>> right_bound = data.wrapper.index 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-24)>>> right_bound
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-25)DatetimeIndex(['2021-01-01 00:00:00+00:00', '2021-01-02 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-26) '2021-01-03 00:00:00+00:00', '2021-01-04 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-27) '2021-01-05 00:00:00+00:00', '2021-01-06 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-28) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-29) '2021-12-26 00:00:00+00:00', '2021-12-27 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-30) '2021-12-28 00:00:00+00:00', '2021-12-29 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-31) '2021-12-30 00:00:00+00:00', '2021-12-31 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-32) dtype='datetime64[ns, UTC]', ...)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-33)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-34)>>> mask = (bandwidth <= 0.1).vbt.resample_between_bounds( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-35)... left_bound, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-36)... right_bound,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-37)... "any",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-38)... closed_lbound=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-39)... closed_rbound=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-40)... wrap_kwargs=dict(fillna=0, dtype=bool)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-41)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-42)>>> mask.index = right_bound
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-26-43)>>> mask.astype(int).vbt.ts_heatmap().show()
 
[/code]

 1. 2. 3. 4. 5. 6. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ts_heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ts_heatmap.dark.svg#only-dark)

We can observe how the signal for the bandwidth touching the 10% mark propagates through each month, and then the calculation gets reset and repeated.


# Periodically[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#periodically "Permanent link")

To set signals periodically, such as at 18:00 of each Tuesday, we have multiple options. The first approach involves comparing various attributes of the source and target datetime. For example, to get the timestamps that correspond to each Tuesday, we can compare [pandas.DatetimeIndex.weekday](https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.weekday.html#pandas.DatetimeIndex.weekday) to 1 (Monday is 0 and Sunday is 6):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-1)>>> min_data = vbt.BinanceData.pull( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-2)... ["BTCUSDT", "ETHUSDT"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-3)... start="2021-01-01 UTC", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-4)... end="2021-02-01 UTC",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-5)... timeframe="1h"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-7)>>> index = min_data.wrapper.index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-8)>>> tuesday_index = index[index.weekday == 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-9)>>> tuesday_index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-10)DatetimeIndex(['2021-01-05 00:00:00+00:00', '2021-01-05 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-11) '2021-01-05 02:00:00+00:00', '2021-01-05 03:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-12) '2021-01-05 04:00:00+00:00', '2021-01-05 05:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-13) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-14) '2021-01-26 18:00:00+00:00', '2021-01-26 19:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-15) '2021-01-26 20:00:00+00:00', '2021-01-26 21:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-16) '2021-01-26 22:00:00+00:00', '2021-01-26 23:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-27-17) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 2. 

Now, we need to select only those timestamps that happen at one specific time:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-28-1)>>> tuesday_1800_index = tuesday_index[tuesday_index.hour == 18]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-28-2)>>> tuesday_1800_index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-28-3)DatetimeIndex(['2021-01-05 18:00:00+00:00', '2021-01-12 18:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-28-4) '2021-01-19 18:00:00+00:00', '2021-01-26 18:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-28-5) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

Since each attribute comparison produces a mask, we can get our signals by pure logical operations. Let's get the timestamps that correspond to each Tuesday 17:30 by comparing the weekday of each timestamp to Tuesday _AND_ the hour of each timestamp to 17 _AND_ the minute of each timestamp to 30:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-29-1)>>> tuesday_1730_index = index[
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-29-2)... (index.weekday == 1) & 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-29-3)... (index.hour == 17) & 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-29-4)... (index.minute == 30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-29-5)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-29-6)>>> tuesday_1730_index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-29-7)DatetimeIndex([], dtype='datetime64[ns, UTC]', name='Open time', freq='H')
 
[/code]

As we see, both conditions combined produced no exact matches because our index is hourly. But what if we wanted to get the previous or next timestamp if there was no exact match? Clearly, the approach above wouldn't work. Instead, we'll use the function [pandas.Index.get_indexer](https://pandas.pydata.org/docs/reference/api/pandas.Index.get_indexer.html), which takes an array with index labels, and searches for their corresponding positions in the index. For example, let's get the position of August 7th in our index:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-30-1)>>> index.get_indexer([vbt.timestamp("2021-01-07", tz=index.tz)]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-30-2)array([144])
 
[/code]

 1. 

But looking for an index that doesn't exist will return `-1`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-31-1)>>> index.get_indexer([vbt.timestamp("2021-01-07 17:30:00", tz=index.tz)]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-31-2)array([-1])
 
[/code]

Warning

Do not pass the result for indexing if there is a possibility of no match. For example, if any of the returned positions is `-1` and it's used in timestamp selection, the position will be replaced by the latest timestamp in the index.

To get either the exact match or the previous one, we can pass `method='ffill'`. Conversely, to get the next one, we can pass `method='bfill'`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-1)>>> index[index.get_indexer(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-2)... [vbt.timestamp("2021-01-07 17:30:00", tz=index.tz)],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-3)... method="ffill"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-4)... )]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-5)DatetimeIndex(['2021-01-07 17:00:00+00:00'], ...)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-7)>>> index[index.get_indexer(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-8)... [vbt.timestamp("2021-01-07 17:30:00", tz=index.tz)],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-9)... method="bfill"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-10)... )]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-32-11)DatetimeIndex(['2021-01-07 18:00:00+00:00'], ...)
 
[/code]

Returning to our example, we need first to generate the target index for our query, which we're about to search in the source index: use the function [pandas.date_range](https://pandas.pydata.org/docs/reference/api/pandas.date_range.html) to get the timestamp of each Tuesday midnight, and then add a timedelta of 17 hours and 30 minutes. Next, transform the target index into positions (row indices) at which our signals will be placed. Then, we extract the Pandas symbol wrapper from our data instance and use it to fill a new mask that has the same number of columns as we have symbols. Finally, set `True` at the generated positions of that mask:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-1)>>> each_tuesday = vbt.date_range(index[0], index[-1], freq="tuesday") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-2)>>> each_tuesday_1730 = each_tuesday + pd.Timedelta(hours=17, minutes=30) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-3)>>> each_tuesday_1730
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-4)DatetimeIndex(['2021-01-05 17:30:00+00:00', '2021-01-12 17:30:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-5) '2021-01-19 17:30:00+00:00', '2021-01-26 17:30:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-6) dtype='datetime64[ns, UTC]', freq=None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-8)>>> positions = index.get_indexer(each_tuesday_1730, method="bfill")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-10)>>> min_symbol_wrapper = min_data.get_symbol_wrapper() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-11)>>> mask = min_symbol_wrapper.fill(False) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-12)>>> mask.iloc[positions] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-13)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-14)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-15)BTCUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-16)ETHUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-33-17)dtype: int64
 
[/code]

 1. 2. 3. 4. 5. 

Let's make sure that all signals match 18:00 on Tuesday, which is the first date after the requested 17:30 on Tuesday in an hourly index:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-34-1)>>> mask[mask.any(axis=1)].index.strftime("%A %T") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-34-2)Index(['Tuesday 18:00:00', 'Tuesday 18:00:00', 'Tuesday 18:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-34-3) 'Tuesday 18:00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-34-4) dtype='object', name='Open time')
 
[/code]

 1. 

The above solution is only required when only a single time boundary is known. For example, if we want 17:30 on Tuesday or later, we know only the left boundary while the right boundary is infinity (or we might get no data point after this datetime at all). When both time boundaries are known, we can easily use the first approach and combine it with the vectorbt's signal selection mechanism. For example, let's place a signal at 17:00 on Tuesday or later, but not later than 17:00 on Wednesday. This would require us placing signals from the left boundary all the way to the right boundary, and then selecting the first signal out of that partition:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-1)>>> tuesday_after_1700 = (index.weekday == 1) & (index.hour >= 17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-2)>>> wednesday_before_1700 = (index.weekday == 2) & (index.hour < 17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-3)>>> main_cond = tuesday_after_1700 | wednesday_before_1700
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-4)>>> mask = min_symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-5)>>> mask[main_cond] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-6)>>> mask = mask.vbt.signals.first()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-7)>>> mask[mask.any(axis=1)].index.strftime("%A %T")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-8)Index(['Tuesday 17:00:00', 'Tuesday 17:00:00', 'Tuesday 17:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-9) 'Tuesday 17:00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-35-10) dtype='object', name='Open time')
 
[/code]

The third and final approach is the vectorbt's one ![❤️‍🔥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2764-fe0f-200d-1f525.svg)

It's relying on the two accessor methods [BaseAccessor.set](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set) and [BaseAccessor.set_between](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set_between), which allow us to conditionally set elements of an array in a more intuitive manner.

Place a signal at 17:30 each Tuesday or later:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-1)>>> mask = min_symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-2)>>> mask.vbt.set(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-3)... True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-4)... every="tuesday", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-5)... at_time="17:30", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-6)... inplace=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-8)>>> mask[mask.any(axis=1)].index.strftime("%A %T")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-9)Index(['Tuesday 18:00:00', 'Tuesday 18:00:00', 'Tuesday 18:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-10) 'Tuesday 18:00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-36-11) dtype='object', name='Open time')
 
[/code]

Place a signal after 18:00 each Tuesday (exclusive):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-1)>>> mask = min_symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-2)>>> mask.vbt.set(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-3)... True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-4)... every="tuesday", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-5)... at_time="18:00", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-6)... add_delta=pd.Timedelta(nanoseconds=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-7)... inplace=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-9)>>> mask[mask.any(axis=1)].index.strftime("%A %T")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-10)Index(['Tuesday 19:00:00', 'Tuesday 19:00:00', 'Tuesday 19:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-11) 'Tuesday 19:00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-37-12) dtype='object', name='Open time')
 
[/code]

 1. 

Fill signals between 12:00 each Monday and 17:00 each Tuesday:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-1)>>> mask = min_symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-2)>>> mask.vbt.set_between(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-3)... True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-4)... every="monday", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-5)... start_time="12:00", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-6)... end_time="17:00", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-7)... add_end_delta=pd.Timedelta(days=1), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-8)... inplace=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-10)>>> mask[mask.any(axis=1)].index.strftime("%A %T")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-11)Index(['Monday 12:00:00', 'Monday 13:00:00', 'Monday 14:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-12) 'Monday 15:00:00', 'Monday 16:00:00', 'Monday 17:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-13) 'Monday 18:00:00', 'Monday 19:00:00', 'Monday 20:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-14) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-15) 'Tuesday 10:00:00', 'Tuesday 11:00:00', 'Tuesday 12:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-16) 'Tuesday 13:00:00', 'Tuesday 14:00:00', 'Tuesday 15:00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-17) 'Tuesday 16:00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-38-18) dtype='object', name='Open time', length=116)
 
[/code]

 1. 

Place a signal exactly at the midnight of January 7th, 2021:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-1)>>> mask = min_symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-2)>>> mask.vbt.set(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-3)... True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-4)... on="January 7th 2021 UTC", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-5)... indexer_method=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-6)... inplace=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-8)>>> mask[mask.any(axis=1)].index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-39-9)DatetimeIndex(['2021-01-07 00:00:00+00:00'], ...)
 
[/code]

 1. 2. 

Fill signals between 12:00 on January 1st/7th and 12:00 on January 2nd/8th, 2021:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-1)>>> mask = min_symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-2)>>> mask.vbt.set_between(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-3)... True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-4)... start=["2021-01-01 12:00:00", "2021-01-07 12:00:00"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-5)... end=["2021-01-02 12:00:00", "2021-01-08 12:00:00"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-6)... inplace=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-8)>>> mask[mask.any(axis=1)].index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-9)DatetimeIndex(['2021-01-01 12:00:00+00:00', '2021-01-01 13:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-10) '2021-01-01 14:00:00+00:00', '2021-01-01 15:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-11) '2021-01-01 16:00:00+00:00', '2021-01-01 17:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-12) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-13) '2021-01-08 06:00:00+00:00', '2021-01-08 07:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-14) '2021-01-08 08:00:00+00:00', '2021-01-08 09:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-15) '2021-01-08 10:00:00+00:00', '2021-01-08 11:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-40-16) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 

Fill signals in the first 2 hours of each week:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-1)>>> mask = min_symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-2)>>> mask.vbt.set_between(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-3)... True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-4)... every="monday",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-5)... split_every=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-6)... add_end_delta="2h",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-7)... inplace=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-9)>>> mask[mask.any(axis=1)].index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-10)DatetimeIndex(['2021-01-04 00:00:00+00:00', '2021-01-04 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-11) '2021-01-11 00:00:00+00:00', '2021-01-11 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-12) '2021-01-18 00:00:00+00:00', '2021-01-18 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-13) '2021-01-25 00:00:00+00:00', '2021-01-25 01:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-41-14) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 

See the API documentation for more examples.


# Iteratively[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#iteratively "Permanent link")

With Numba, we can write an iterative logic that performs just as well as its vectorized counterparts. But which approach is better? There is no clear winner, although using vectors is an overall more effective and user-friendlier approach because it abstracts away looping over data and automates various mechanisms associated with index and columns. Just think about how powerful the concept of broadcasting is, and how many more lines of code it would require implementing something similar iteratively. Numba also doesn't allow us to work with labels and complex data types, only with numeric data, which requires skills and creativity in designing (efficient!) algorithms. 

Moreover, most vectorized and also non-vectorized but compiled functions are specifically tailored at one specific task and perform it reliably, while writing an own loop makes **you** responsible to implement every bit of the logic correctly. Vectors are like Lego bricks that require almost zero effort to construct even the most breathtaking castles, while custom loops require learning how to design each Lego brick first ![🧱](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f9f1.svg)

Nevertheless, the most functionality in vectorbt is powered by loops, not vectors - we should rename vectorbt to loopbt, really ![😬](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f62c.svg) The main reason is plain and simple: most of the operations cannot be realized through vectors because they either introduce path dependencies, require complex data structures, use intermediate calculations or data buffers, periodically need to call a third-party function, or all of these together. Another reason is certainly efficiency: we can design algorithms that loop of the data [only once](https://en.wikipedia.org/wiki/One-pass_algorithm), while performing the same logic using vectors would read the whole data sometimes a dozen of times. The same goes for memory consumption! Finally, defining and running a strategy at each time step is exactly how we would proceed in the real world (and in any other backtesting framework too), and we as traders should strive to mimic the real world as closely as possible.

Enough talking! Let's implement the first example from [Logical operators](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#logical-operators) using a custom loop. Unless our signals are based on multiple assets or some other column grouping, we should always start with one column only:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-1)>>> @njit 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-2)... def generate_mask_1d_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-3)... high, low, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-4)... uband, mband, lband, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-5)... cond2_th, cond4_th 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-6)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-7)... out = np.full(high.shape, False) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-8)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-9)... for i in range(high.shape[0]): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-10)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-11)... bandwidth = (uband[i] - lband[i]) / mband[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-12)... cond1 = low[i] < lband[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-13)... cond2 = bandwidth > cond2_th
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-14)... cond3 = high[i] > uband[i]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-15)... cond4 = bandwidth < cond4_th
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-16)... signal = (cond1 and cond2) or (cond3 and cond4) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-17)... out[i] = signal 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-18)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-19)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-20)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-21)>>> mask = generate_mask_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-22)... data.get("High")["BTCUSDT"].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-23)... data.get("Low")["BTCUSDT"].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-24)... bb.upperband["BTCUSDT"].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-25)... bb.middleband["BTCUSDT"].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-26)... bb.lowerband["BTCUSDT"].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-27)... 0.30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-28)... 0.15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-29)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-30)>>> symbol_wrapper = data.get_symbol_wrapper()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-31)>>> mask = symbol_wrapper["BTCUSDT"].wrap(mask) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-32)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-42-33)25
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 

We've got the same number of signals as previously - magic!

To make the function work on multiple columns, we can then write another Numba-compiled function that iterates over columns and calls `generate_mask_1d_nb` on each:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-2)... def generate_mask_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-3)... high, low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-4)... uband, mband, lband,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-5)... cond2_th, cond4_th
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-6)... ):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-7)... out = np.empty(high.shape, dtype=np.bool_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-8)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-9)... for col in range(high.shape[1]): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-10)... out[:, col] = generate_mask_1d_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-11)... high[:, col], low[:, col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-12)... uband[:, col], mband[:, col], lband[:, col],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-13)... cond2_th, cond4_th
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-15)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-16)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-18)>>> mask = generate_mask_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-19)... vbt.to_2d_array(data.get("High")), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-20)... vbt.to_2d_array(data.get("Low")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-21)... vbt.to_2d_array(bb.upperband),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-22)... vbt.to_2d_array(bb.middleband),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-23)... vbt.to_2d_array(bb.lowerband),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-24)... 0.30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-25)... 0.15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-27)>>> mask = symbol_wrapper.wrap(mask)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-28)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-29)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-30)BTCUSDT 25
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-31)ETHUSDT 13
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-43-32)dtype: int64
 
[/code]

 1. 2. 3. 4. 5. 

Probably a more "vectorbtonic" way is to create a stand-alone indicator where we can specify the function and what data it expects and returns, and the indicator factory will take care of everything else for us!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-1)>>> MaskGenerator = vbt.IF( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-2)... input_names=["high", "low", "uband", "mband", "lband"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-3)... param_names=["cond2_th", "cond4_th"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-4)... output_names=["mask"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-5)... ).with_apply_func(generate_mask_1d_nb, takes_1d=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-6)>>> mask_generator = MaskGenerator.run( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-7)... data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-8)... data.get("Low"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-9)... bb.upperband,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-10)... bb.middleband,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-11)... bb.lowerband,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-12)... [0.3, 0.4],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-13)... [0.1, 0.2],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-14)... param_product=True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-16)>>> mask_generator.mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-17)custom_cond2_th custom_cond4_th symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-18)0.3 0.1 BTCUSDT 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-19) ETHUSDT 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-20) 0.2 BTCUSDT 28
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-21) ETHUSDT 27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-22)0.4 0.1 BTCUSDT 9
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-23) ETHUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-24) 0.2 BTCUSDT 26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-25) ETHUSDT 22
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-44-26)dtype: int64
 
[/code]

 1. 2. 3. 4. 

But what about shifting and truth value testing? Simple use cases such as fixed shifts and windows can be implemented quite easily. Below, we're comparing the current value to the value some number of ticks before:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-2)... def value_ago_1d_nb(arr, ago):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-3)... out = np.empty(arr.shape, dtype=float_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-4)... for i in range(out.shape[0]):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-5)... if i - ago >= 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-6)... out[i] = arr[i - ago]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-7)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-8)... out[i] = np.nan 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-9)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-11)>>> arr = np.array([1, 2, 3])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-12)>>> value_ago_1d_nb(arr, 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-45-13)array([nan, 1., 2.])
 
[/code]

 1. 2. 3. 

Important

Don't forget to check whether the element you query is within the bounds of the array. Unless you turned on the `NUMBA_BOUNDSCHECK` mode, Numba won't raise an error if you accessed an element that does not exist. Instead, it will quietly proceed with the calculation, and at some point your kernel will probably die. In such a case, just restart the kernel, disable Numba or enable the bounds check, and re-run the function to identify the bug.

And here's how to test if any condition was true inside a fixed window (= variable time interval):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-2)... def any_in_window_1d_nb(arr, window):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-3)... out = np.empty(arr.shape, dtype=np.bool_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-4)... for i in range(out.shape[0]):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-5)... from_i = max(0, i + 1 - window) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-6)... to_i = i + 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-7)... out[i] = np.any(arr[from_i:to_i]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-8)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-10)>>> arr = np.array([False, True, True, False, False])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-11)>>> any_in_window_1d_nb(arr, 2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-46-12)array([False, True, True, True, False])
 
[/code]

 1. 2. 3. 4. 

As soon as dates and time are involved, such as to compare the current value to the value exactly 5 days ago, a better approach is to pre-calculate as many intermediate steps as possible. But there is also a possibility to work with a datetime-like index in Numba directly. Here's how to test if any condition was true inside a variable window (= fixed time interval):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-2)... def any_in_var_window_1d_nb(arr, index, freq): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-3)... out = np.empty(arr.shape, dtype=np.bool_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-4)... from_i = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-5)... for i in range(out.shape[0]):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-6)... if index[from_i] <= index[i] - freq: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-7)... for j in range(from_i + 1, index.shape[0]): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-8)... if index[j] > index[i] - freq:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-9)... from_i = j
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-10)... break 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-11)... to_i = i + 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-12)... out[i] = np.any(arr[from_i:to_i])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-13)... return out
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-15)>>> arr = np.array([False, True, True, False, False])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-16)>>> index = vbt.date_range("2020", freq="5min", periods=len(arr)).values 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-17)>>> freq = vbt.timedelta("10min").to_timedelta64() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-18)>>> any_in_var_window_1d_nb(arr, index, freq)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-47-19)array([False, True, True, True, False])
 
[/code]

 1. 2. 3. 4. 5. 6. 

Hint

Generally, it's easier to design iterative functions using regular Python and only compile them with Numba if they were sufficiently tested, because it's easier to debug things in Python than in Numba.

Remember that Numba (and thus vectorbt) has far more features for processing numeric data than datetime/timedelta data. But gladly, datetime/timedelta data can be safely converted into integer data outside Numba, and many functions will continue to work just as before:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-48-1)>>> any_in_var_window_1d_nb(arr, vbt.dt.to_ns(index), vbt.dt.to_ns(freq))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-48-2)array([False, True, True, True, False])
 
[/code]

Why so? By converting a datetime/timedelta into an integer, we're extracting the total number of nanoseconds representing that object. For a datetime, the integer value becomes the number of nanoseconds after the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time), which is 00:00:00 UTC on 1 January 1970:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-1)>>> vbt.dt.to_ns(index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-2)array([1577836800000000000, 1577837100000000000, 1577837400000000000,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-3) 1577837700000000000, 1577838000000000000])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-5)>>> vbt.dt.to_ns(index - np.datetime64(0, "ns")) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-6)array([1577836800000000000, 1577837100000000000, 1577837400000000000,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-7) 1577837700000000000, 1577838000000000000])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-9)>>> vbt.dt.to_ns(freq) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-10)600000000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-12)>>> vbt.dt.to_ns(freq) / 1000 / 1000 / 1000 / 60 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-49-13)10.0
 
[/code]

 1. 2. 3. 4. 


# Generators[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#generators "Permanent link")

Writing own loops is powerful and makes fun, but even here vectorbt has functions that may make our life easier, especially for generating signals. The most flexible out of all helper functions is the Numba-compiled function [generate_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_nb) and its accessor class method [SignalsAccessor.generate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate), which takes a target shape, initializes a boolean output array of that shape and fills it with `False`values, then iterates over the columns, and for each column, it calls a so-called "placement function" - a regular UDF that changes the mask in place. After the change, the placement function should return either the position of the last placed signal or `-1` for no signal.

All the information about the current iteration is being passed via a context of the type [GenEnContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext), which contains the current segment of the output mask that can be modified in place, the range start (inclusive) that corresponds to that segment, the range end (exclusive), column, but also the full output mask for the user to be able to make patches wherever they want. This way, vectorbt abstracts away both preparing the array and looping over the columns, and assists the user in selecting the right subset of the output data to modify.

Let's place a signal at 17:00 (UTC) of each Tuesday:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-2)... def place_func_nb(c, index): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-3)... last_i = -1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-4)... for out_i in range(len(c.out)): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-5)... i = c.from_i + out_i 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-6)... weekday = vbt.dt_nb.weekday_nb(index[i]) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-7)... hour = vbt.dt_nb.hour_nb(index[i])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-8)... if weekday == 1 and hour == 17: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-9)... c.out[out_i] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-10)... last_i = out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-11)... return last_i 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-13)>>> mask = vbt.pd_acc.signals.generate( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-14)... symbol_wrapper.shape, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-15)... place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-16)... vbt.dt.to_ns(symbol_wrapper.index), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-17)... wrapper=symbol_wrapper 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-19)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-20)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-21)BTCUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-22)ETHUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-50-23)dtype: int64
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 

Info

Segments in [generate_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_nb) are always the entire columns.

But our index is a daily index, thus there can't be any signal. Instead, let's place a signal at the next possible timestamp:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-2)... def place_func_nb(c, index):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-3)... last_i = -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-4)... for out_i in range(len(c.out)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-5)... i = c.from_i + out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-6)... weekday = vbt.dt_nb.weekday_nb(index[i])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-7)... hour = vbt.dt_nb.hour_nb(index[i])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-8)... if weekday == 1 and hour == 17:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-9)... c.out[out_i] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-10)... last_i = out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-11)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-12)... past_target_midnight = vbt.dt_nb.past_weekday_nb(index[i], 1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-13)... past_target = past_target_midnight + 17 * vbt.dt_nb.h_ns 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-14)... if (i > 0 and index[i - 1] < past_target) and \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-15)... index[i] > past_target: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-16)... c.out[out_i] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-17)... last_i = out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-18)... return last_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-19)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-20)>>> mask = vbt.pd_acc.signals.generate(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-21)... symbol_wrapper.shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-22)... place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-23)... vbt.dt.to_ns(symbol_wrapper.index),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-24)... wrapper=symbol_wrapper
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-26)>>> mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-27)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-28)BTCUSDT 52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-29)ETHUSDT 52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-30)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-31)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-32)>>> mask.index[mask.any(axis=1)].strftime('%A %m/%d/%Y') 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-33)Index(['Thursday 01/07/2021', ..., 'Thursday 12/30/2021'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-51-34) dtype='object', name='Open time')
 
[/code]

 1. 2. 3. 4. 

The most fascinating part about the snippet above is that the entire datetime logic is being performed using just regular integers!

Important

When being converted into the integer format, the timezone of each datetime object is effectively converted to UTC, thus make sure that any value compared to the UTC timestamp is also in UTC.

But what about multiple parameter combinations? We cannot pass the function above to the indicator factory because it doesn't look like an apply function. But vectorbt's got our back! There is an entire subclass of the indicator factory tailed at signal generation - [SignalFactory](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#vectorbtpro.signals.factory.SignalFactory). This class supports multiple generation modes that can be specified using the argument `mode` of the type [FactoryMode](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.FactoryMode). In our case, the mode is `FactoryMode.Entries` because our function generates signals based on the target shape only, and not based on other signal arrays. Furthermore, the signal factory accepts any additional inputs, parameters, and in-outputs to build the skeleton of our future indicator class.

The signal factory has the class method [SignalFactory.with_place_func](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#vectorbtpro.signals.factory.SignalFactory.with_place_func) comparable to `from_apply_func` we've got used to. In fact, it takes a placement function and generates a custom function that does all the pre- and post-processing around [generate_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_nb) (note that other modes have other generation functions). This custom function, for example, prepares the arguments and assigns them to their correct positions in the placement function call. It's then forwarded down to [IndicatorFactory.with_custom_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.with_custom_func). As a result, we receive an indicator class with a `run` method that can be applied on any user-defined shape and any grid of parameter combinations. Sounds handy, right?

Let's parametrize our exact-match placement function with two parameters: weekday and hour.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-2)... def place_func_nb(c, weekday, hour, index): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-3)... last_i = -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-4)... for out_i in range(len(c.out)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-5)... i = c.from_i + out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-6)... weekday_now = vbt.dt_nb.weekday_nb(index[i])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-7)... hour_now = vbt.dt_nb.hour_nb(index[i])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-8)... if weekday_now == weekday and hour_now == hour:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-9)... c.out[out_i] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-10)... last_i = out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-11)... return last_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-13)>>> EntryGenerator = vbt.SignalFactory(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-14)... mode="entries",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-15)... param_names=["weekday", "hour"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-16)... ).with_place_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-17)... entry_place_func_nb=place_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-18)... entry_settings=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-19)... pass_params=["weekday", "hour"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-20)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-21)... var_args=True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-23)>>> entry_generator = EntryGenerator.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-24)... symbol_wrapper.shape, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-25)... 1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-26)... [0, 17], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-27)... vbt.dt.to_ns(symbol_wrapper.index), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-28)... input_index=symbol_wrapper.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-29)... input_columns=symbol_wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-30)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-31)>>> entry_generator.entries.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-32)custom_weekday custom_hour symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-33)2 0 BTCUSDT 52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-34) ETHUSDT 52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-35) 17 BTCUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-36) ETHUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-52-37)dtype: int64
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 

Note

The mode `FactoryMode.Entries` doesn't mean that we are forced to generate signals that must strictly act as entries during the simulation - we can generate any mask, also exits if they don't depend on entries.

The indicator function was able to match all midnight times but none afternoon times, which makes sense because our index is daily and thus contains midnight times only. We can easily plot the indicator using the attached `plot` method, which knows how to visualize each mode:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-53-1)>>> entry_generator.plot(column=(1, 0, "BTCUSDT")).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/signal_factory.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/signal_factory.dark.svg#only-dark)


# Exits[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#exits "Permanent link")

After populating the position entry mask, we should decide on the position exit mask. When exits do not rely on entries, we can use the generator introduced above. In other cases though, we might have a logic that makes an exit signal fully depend on the entry signal. For example, an exit signal representing a stop loss exists solely because of the entry signal that defined that stop loss condition. There is also no guarantee that an exit can be found for an entry at all. Thus, this mode should only be used for cases where entries do not depend on exits, but exits depend on entries. The generation is then done using the Numba-compiled function [generate_ex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_ex_nb) and its accessor instance method [SignalsAccessor.generate_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_exits). The passed context is now of the type [GenExContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext) and also includes the input mask and various generator-related arguments.

The generator takes an entry mask array, and in each column, it visits each entry signal and calls a UDF to place one or more exit signals succeeding it. Do you recall how we had to accept `from_i` and `to_i` in the placement functions above? The previous mode always passed `0` as `from_i` and `len(index)` as `to_i` because we had all the freedom to define our signals across the entire column. Here, the passed `from_i` will usually be the next index after the previous entry, while the passed `to_i` will usually be the index of the next entry, thus effectively limiting our decision field to the space between each pair of entries.

Warning

Beware that knowing the position of the next entry signal may introduce the look-ahead bias. Thus, use it only for iteration purposes, and never set data based on `to_i`!

Let's generate an entry each quarter and an exit at the next date:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-2)... def exit_place_func_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-3)... c.out[0] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-4)... return 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-6)>>> entries = symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-7)>>> entries.vbt.set(True, every="Q", inplace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-8)>>> entries.index[entries.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-9)DatetimeIndex(['2021-03-31 00:00:00+00:00', '2021-06-30 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-10) '2021-09-30 00:00:00+00:00', '2021-12-31 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-11) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-13)>>> exits = entries.vbt.signals.generate_exits(exit_place_func_nb) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-14)>>> exits.index[exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-15)DatetimeIndex(['2021-04-01 00:00:00+00:00', '2021-07-01 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-16) '2021-10-01 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-54-17) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 2. 

We can control the distance to the entry signal using `wait`, which defaults to 1. Let's instruct vectorbt to start each segment at the same timestamp as the entry:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-55-1)>>> exits = entries.vbt.signals.generate_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-55-2)... exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-55-3)... wait=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-55-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-55-5)>>> exits.index[exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-55-6)DatetimeIndex(['2021-03-31 00:00:00+00:00', '2021-06-30 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-55-7) '2021-09-30 00:00:00+00:00', '2021-12-31 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-55-8) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

And below is how to implement a variable waiting time based on a frequency. Let's wait exactly 7 days before placing an exit:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-2)... def exit_place_func_nb(c, index, wait_td):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-3)... for out_i in range(len(c.out)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-4)... i = c.from_i + out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-5)... if index[i] >= index[c.from_i] + wait_td: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-6)... return out_i 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-7)... return -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-9)>>> exits = entries.vbt.signals.generate_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-10)... exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-11)... vbt.dt.to_ns(entries.index), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-12)... vbt.dt.to_ns(vbt.timedelta("7d")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-13)... wait=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-15)>>> exits.index[exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-16)DatetimeIndex(['2021-04-07 00:00:00+00:00', '2021-07-07 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-17) '2021-10-07 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-56-18) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 2. 3. 

But what happens with the exit condition for the previous entry if the next entry is less than 7 days away? Will the exit still be placed? No!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-1)>>> entries = symbol_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-2)>>> entries.vbt.set(True, every="5d", inplace=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-3)>>> exits = entries.vbt.signals.generate_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-4)... exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-5)... vbt.dt.to_ns(entries.index),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-6)... vbt.dt.to_ns(vbt.timedelta("7d")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-7)... wait=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-9)>>> exits.index[exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-57-10)DatetimeIndex([], dtype='datetime64[ns, UTC]', name='Open time', freq='D')
 
[/code]

By default, each segment is limited by the two entries surrounding it. To make it infinite, we can disable `until_next`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-1)>>> exits = entries.vbt.signals.generate_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-2)... exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-3)... vbt.dt.to_ns(entries.index),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-4)... vbt.dt.to_ns(vbt.timedelta("7d")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-5)... wait=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-6)... until_next=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-8)>>> exits.index[exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-9)DatetimeIndex(['2021-01-08 00:00:00+00:00', '2021-01-13 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-10) '2021-01-18 00:00:00+00:00', '2021-01-23 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-11) '2021-01-28 00:00:00+00:00', '2021-02-02 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-12) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-13) '2021-12-04 00:00:00+00:00', '2021-12-09 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-14) '2021-12-14 00:00:00+00:00', '2021-12-19 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-15) '2021-12-24 00:00:00+00:00', '2021-12-29 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-58-16) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

Note

In such a case, we might be unable to identify which exit belongs to which entry. Moreover, two or more entries may generate an exit at the same timestamp, so beware!

In the case above, the generated signals follow the following schema: `entry1`, `entry2`, `exit1`, `entry3`, `exit2`, and so on. Whenever those signals are passed to the simulator, it will execute `entry1` and ignore `entry2` because there was no exit prior to it - we're still in the market. It will then rightfully execute `exit1`. But then, it will open a new position with `entry3` and close it with `exit2` right after, which was originally designed for `entry2` (that has been ignored). To avoid this mistake, we should enable `skip_until_exit` to avoid processing any future entry signal that comes before an exit for any past entry signal. This would match the simulation order.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-1)>>> exits = entries.vbt.signals.generate_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-2)... exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-3)... vbt.dt.to_ns(entries.index),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-4)... vbt.dt.to_ns(vbt.timedelta("7d")),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-5)... wait=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-6)... until_next=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-7)... skip_until_exit=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-9)>>> exits.index[exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-10)DatetimeIndex(['2021-01-08 00:00:00+00:00', '2021-01-18 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-11) '2021-01-28 00:00:00+00:00', '2021-02-07 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-12) '2021-02-17 00:00:00+00:00', '2021-02-27 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-13) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-14) '2021-11-04 00:00:00+00:00', '2021-11-14 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-15) '2021-11-24 00:00:00+00:00', '2021-12-04 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-16) '2021-12-14 00:00:00+00:00', '2021-12-24 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-59-17) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

Note

Make sure to use `skip_until_exit` always in conjunction with disabled `until_next`.

Finally, to make the thing parametrizable, we should use the mode `FactoryMode.Exits` and provide any supporting information with the prefix `exit`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-2)... def exit_place_func_nb(c, wait_td, index): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-3)... for out_i in range(len(c.out)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-4)... i = c.from_i + out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-5)... if index[i] >= index[c.from_i] + wait_td:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-6)... return out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-7)... return -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-9)>>> ExitGenerator = vbt.SignalFactory(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-10)... mode="exits",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-11)... param_names=["wait_td"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-12)... ).with_place_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-13)... exit_place_func_nb=exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-14)... exit_settings=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-15)... pass_params=["wait_td"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-16)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-17)... var_args=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-18)... wait=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-19)... until_next=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-20)... skip_until_exit=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-21)... param_settings=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-22)... wait_td=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-23)... post_index_func=lambda x: x.map(lambda y: str(vbt.timedelta(y)))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-25)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-27)>>> exit_generator = ExitGenerator.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-28)... entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-29)... [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-30)... vbt.timedelta("3d").to_timedelta64(), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-31)... vbt.timedelta("7d").to_timedelta64()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-32)... ],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-33)... symbol_wrapper.index.values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-34)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-35)>>> exit_generator.exits.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-36)custom_wait_td symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-37)3 days 00:00:00 BTCUSDT 73
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-38) ETHUSDT 73
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-39)7 days 00:00:00 BTCUSDT 36
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-40) ETHUSDT 36
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-60-41)dtype: int64
 
[/code]

 1. 2. 3. 4. 5. 

We can then remove redundant entries if wanted:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-1)>>> new_entries = exit_generator.entries.vbt.signals.first( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-2)... reset_by=exit_generator.exits, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-3)... allow_gaps=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-5)>>> new_entries.index[new_entries[("7 days 00:00:00", "BTCUSDT")]]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-6)DatetimeIndex(['2021-01-01 00:00:00+00:00', '2021-01-11 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-7) '2021-01-21 00:00:00+00:00', '2021-01-31 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-8) '2021-02-10 00:00:00+00:00', '2021-02-20 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-9) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-10) '2021-11-17 00:00:00+00:00', '2021-11-27 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-11) '2021-12-07 00:00:00+00:00', '2021-12-17 00:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-12) '2021-12-27 00:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-61-13) dtype='datetime64[ns, UTC]', name='Open time', freq=None)
 
[/code]

 1. 2. 3. 

After that, each exit is guaranteed to come after the entry it was generated for.


# Both[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#both "Permanent link")

Instead of dividing the entry and exit signal generation parts, we can merge them. This is particularly well-suited for a scenario where an exit depends on an entry but also an entry depends on an exit. This kind of logic can be realized through the Numba-compiled function [generate_enex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_enex_nb) and its accessor class method [SignalsAccessor.generate_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_both). The generation proceeds as follows. First, two empty output masks are created: entries and exits. Then, for each column, the entry placement function is called to place one or more entry signals. The generator then searches for the position of the last generated entry signal, and calls the exit placement function on the segment right after that entry signal. Then, it's the entry placement function's turn again. This process repeats until the column has been traversed completely. The passed context is of the type [GenEnExContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext) and contains all the interesting information related to the current turn and iteration.

Let's demonstrate the full power of this method by placing an entry once the price dips below one threshold, and an exit once the price tops another threshold. The signals will be generated strictly one after another, and the entry/exit price will be the close price.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-2)... def entry_place_func_nb(c, low, close, th):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-3)... if c.from_i == 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-4)... c.out[0] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-5)... return 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-6)... exit_i = c.from_i - c.wait 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-7)... exit_price = close[exit_i, c.col] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-8)... hit_price = exit_price * (1 - th)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-9)... for out_i in range(len(c.out)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-10)... i = c.from_i + out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-11)... if low[i, c.col] <= hit_price: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-12)... return out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-13)... return -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-15)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-16)... def exit_place_func_nb(c, high, close, th): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-17)... entry_i = c.from_i - c.wait
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-18)... entry_price = close[entry_i, c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-19)... hit_price = entry_price * (1 + th)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-20)... for out_i in range(len(c.out)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-21)... i = c.from_i + out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-22)... if high[i, c.col] >= hit_price:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-23)... return out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-24)... return -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-25)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-26)>>> entries, exits = vbt.pd_acc.signals.generate_both( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-27)... symbol_wrapper.shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-28)... entry_place_func_nb=entry_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-29)... entry_place_args=(vbt.Rep("low"), vbt.Rep("close"), 0.1), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-30)... exit_place_func_nb=exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-31)... exit_place_args=(vbt.Rep("high"), vbt.Rep("close"), 0.2),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-32)... wrapper=symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-33)... broadcast_named_args=dict( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-34)... high=data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-35)... low=data.get("Low"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-36)... close=data.get("Close")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-37)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-38)... broadcast_kwargs=dict(post_func=np.asarray) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-39)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-40)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-41)>>> fig = data.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-42)... symbol="BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-43)... ohlc_trace_kwargs=dict(opacity=0.5), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-44)... plot_volume=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-45)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-46)>>> entries["BTCUSDT"].vbt.signals.plot_as_entries(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-47)... y=data.get("Close", "BTCUSDT"), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-48)>>> exits["BTCUSDT"].vbt.signals.plot_as_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-49)... y=data.get("Close", "BTCUSDT"), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-62-50)>>> fig.show() 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/both.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/both.dark.svg#only-dark)

To parametrize this logic, we need to use the mode `FactoryMode.Both`. And because our functions require input arrays that broadcast against the input shape, vectorbt won't ask us to provide the input shape but rather determine it from the input arrays automatically:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-1)>>> BothGenerator = vbt.SignalFactory(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-2)... mode="both",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-3)... input_names=["high", "low", "close"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-4)... param_names=["entry_th", "exit_th"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-5)... ).with_place_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-6)... entry_place_func_nb=entry_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-7)... entry_settings=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-8)... pass_inputs=["low", "close"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-9)... pass_params=["entry_th"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-10)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-11)... exit_place_func_nb=exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-12)... exit_settings=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-13)... pass_inputs=["high", "close"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-14)... pass_params=["exit_th"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-17)>>> both_generator = BothGenerator.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-18)... data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-19)... data.get("Low"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-20)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-21)... [0.1, 0.2],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-22)... [0.2, 0.3],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-23)... param_product=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-25)>>> fig = data.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-26)... symbol="BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-27)... ohlc_trace_kwargs=dict(opacity=0.5), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-28)... plot_volume=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-29)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-30)>>> both_generator.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-31)... column=(0.1, 0.3, "BTCUSDT"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-32)... entry_y=data.get("Close", "BTCUSDT"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-33)... exit_y=data.get("Close", "BTCUSDT"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-34)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-35)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-63-36)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/both2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/both2.dark.svg#only-dark)


# Chained exits[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#chained-exits "Permanent link")

A chain in the vectorbt's vocabulary is a special ordering of entry and exit signals where each exit comes after exactly one entry and each entry (apart from the first one) comes after exactly one exit. Thus, we can easily identify which exit belongs to which entry and vice versa. The example above is actually a perfect example of a chain because each signal from crossing a threshold is based solely on the latest opposite signal. Now, imagine that we have already generated an array with entries, and each of those entries should exist only if there was an exit before, otherwise it should be ignored. This use case is very similar to `FactoryMode.Exits` with enabled `skip_until_exit` and disabled `until_next`.

But what the mode `FactoryMode.Chain` proposes is the following: use the generator [generate_enex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_enex_nb) with the entry placement function [first_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.first_place_nb) to select only the first entry signal after each exit, and any user-defined exit placement function. In the end, we will get two arrays: cleaned entries (often `new_entries`) and exits (`exits`).

What we should always keep in mind is that entries and exits during the generation phase aren't forced to be used as entries and exits respectively during the simulation. Let's generate entry signals from a moving average crossover each mimicing a limit order, and use an exit placement function to generate signals for executing those limit orders. As a result, we can use those newly generated signals as actual entries during the simulation! If any new "entry" signal comes before the previous "exit" signal, it will be ignored. We'll also track the fill price with another array.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-2)... def exit_place_func_nb(c, low, request_price, fill_price_out):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-3)... entry_req_price = request_price[c.from_i - c.wait, c.col] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-4)... for out_i in range(len(c.out)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-5)... i = c.from_i + out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-6)... if low[i, c.col] <= entry_req_price: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-7)... fill_price_out[i, c.col] = entry_req_price
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-8)... return out_i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-9)... return -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-11)>>> ChainGenerator = vbt.SignalFactory(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-12)... mode="chain",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-13)... input_names=["low", "request_price"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-14)... in_output_names=["fill_price_out"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-15)... ).with_place_func( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-16)... exit_place_func_nb=exit_place_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-17)... exit_settings=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-18)... pass_inputs=["low", "request_price"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-19)... pass_in_outputs=["fill_price_out"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-20)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-21)... fill_price_out=np.nan 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-22)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-23)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-24)>>> fast_ma = vbt.talib("SMA").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-25)... data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-26)... vbt.Default(10), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-27)... short_name="fast_ma"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-28)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-29)>>> slow_ma = vbt.talib("SMA").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-30)... data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-31)... vbt.Default(20), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-32)... short_name="slow_ma"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-33)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-34)>>> entries = fast_ma.real_crossed_above(slow_ma) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-35)>>> entries.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-36)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-37)BTCUSDT 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-38)ETHUSDT 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-39)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-40)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-41)>>> chain_generator = ChainGenerator.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-42)... entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-43)... data.get("Low"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-44)... data.get("Close") * (1 - 0.1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-45)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-46)>>> request_mask = chain_generator.new_entries 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-47)>>> request_mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-48)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-49)BTCUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-50)ETHUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-51)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-52)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-53)>>> request_price = chain_generator.request_price 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-54)>>> request_price[request_mask.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-55)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-56)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-57)2021-02-04 00:00:00+00:00 33242.994 1436.103
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-58)2021-03-11 00:00:00+00:00 51995.844 1643.202
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-59)2021-04-02 00:00:00+00:00 53055.009 1920.321
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-60)2021-06-07 00:00:00+00:00 30197.511 2332.845
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-61)2021-06-15 00:00:00+00:00 36129.636 2289.186
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-62)2021-07-05 00:00:00+00:00 30321.126 1976.877
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-63)2021-07-06 00:00:00+00:00 30798.009 2090.250
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-64)2021-07-27 00:00:00+00:00 35512.083 2069.541
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-65)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-66)>>> fill_mask = chain_generator.exits 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-67)>>> fill_mask.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-68)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-69)BTCUSDT 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-70)ETHUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-71)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-72)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-73)>>> fill_price = chain_generator.fill_price_out 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-74)>>> fill_price[fill_mask.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-75)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-76)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-77)2021-03-24 00:00:00+00:00 NaN 1643.202
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-78)2021-05-19 00:00:00+00:00 33242.994 1920.321
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-79)2021-06-08 00:00:00+00:00 NaN 2332.845
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-80)2021-06-18 00:00:00+00:00 36129.636 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-81)2021-07-13 00:00:00+00:00 NaN 1976.877
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-64-82)2021-07-19 00:00:00+00:00 30798.009 NaN
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 

For example, the first limit order for `BTCUSDT` was placed on `2021-02-04` and filled on `2021-05-19`. The first limit order for `ETHUSDT` was placed on `2021-03-11` and filled on `2021-03-24`. To simulate this data, we can pass `fill_mask` as entries/order size and `fill_mask` as order price.

Hint

If you want to replace any pending limit order with a new one instead of ignoring it, use `FactoryMode.Exits` and then select the last input signal before each output signal.


# Preset generators[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#preset-generators "Permanent link")

There is an entire range of preset signal generators - [here](https://vectorbt.pro/pvt_7a467f6b/api/signals/generators/) \- that are using the modes we discussed above. Preset indicators were set up for one particular task and are ready to be used without having to provide any custom placement function. The naming of those indicators follows a well-defined schema:

 * Plain generator have no suffix
 * Exit generators have the suffix `X`
 * Both generators have the suffix `NX`
 * Chain exit generators have the suffix `CX`


# Random[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#random "Permanent link")

You hate randomness in trading? Well, there is one particular use case where randomness is heartily welcomed: trading strategy benchmarking. For instance, comparing one configuration of RSI to another one isn't representative at all since both strategy instances may be inherently bad, and deciding for one is like picking a lesser evil. Random signals, on the other hand, give us an entire new universe of strategies yet to be discovered. Generating a sufficient number of such random signal permutations on a market can reveal the underlying structure and behavior of the market and may answer whether our trading strategy is driven by an edge or pure randomness.

There are two types of random signal generation: count-based and probability-based. The former takes a target number of signals `n` to place during a certain period of time, and guarantees to fulfill this number unless the time period is too small. The latter takes a probability `prob` of placing a signal at each timestamp; if the probability is too high, it may place a signal at each single timestamp; if the probability is too low, it may place nothing. Both types can be run using the same accessor method: [SignalsAccessor.generate_random](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random) to spread entry signals across the entire column, [SignalsAccessor.generate_random_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random_exits) to spread exit signals after each entry and before the next entry, and [SignalsAccessor.generate_random_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_random_both) to spread entry and exit signals one after another in a chain.

Warning

Generating a specific number of signals may introduce the look-ahead bias because it incorporates the knowledge about the next opposite signal or the column end. Use it with caution, and only when the position of the last to-be-placed signal is known in advance, such as when trading on the per-month basis.

Let's generate a signal once in 10 timestamps on average:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-1)>>> btcusdt_wrapper = symbol_wrapper["BTCUSDT"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-2)>>> mask = vbt.pd_acc.signals.generate_random(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-3)... btcusdt_wrapper.shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-4)... prob=1 / 10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-5)... wrapper=btcusdt_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-6)... seed=42 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-8)>>> mask_index = mask.index[mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-9)>>> (mask_index[1:] - mask_index[:-1]).mean() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-65-10)Timedelta('8 days 03:20:55.813953488')
 
[/code]

 1. 2. 

Note

The more signals we generate, the closer is the average neighbor distance to the target average.

Now, let's generate exactly one signal each week. To achieve that, we'll generate an "entry" signal on each Monday, and an "exit" signal acting as our target signal. This won't cause the look-ahead bias because we have defined the bounds of the generation space in advance.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-1)>>> monday_mask = btcusdt_wrapper.fill(False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-2)>>> monday_mask.vbt.set(True, every="monday", inplace=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-3)>>> mask = monday_mask.vbt.signals.generate_random_exits(wait=0) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-4)>>> mask_index = mask.index[mask]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-5)>>> mask_index.strftime("%W %A") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-6)Index(['01 Tuesday', '02 Wednesday', '03 Wednesday', '04 Friday', '05 Friday',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-7) '06 Tuesday', '07 Thursday', '08 Tuesday', '09 Friday', '10 Saturday',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-8) '11 Friday', '12 Saturday', '13 Monday', '14 Friday', '15 Monday',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-9) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-10) '41 Wednesday', '42 Friday', '43 Thursday', '44 Sunday', '45 Sunday',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-11) '46 Sunday', '47 Saturday', '48 Saturday', '49 Tuesday', '50 Thursday',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-12) '51 Sunday', '52 Tuesday'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-66-13) dtype='object', name='Open time')
 
[/code]

 1. 2. 3. 

To parametrize the number of signals and the probability, we have at our disposal the indicators starting with the prefix `RAND` and `RPROB` respectively. A powerful feature of those indicators is their ability to take both parameters as array-like objects! In particular, we can provide `n` per column, and `prob` per column, row, or even element in the target shape. 

Let's gradually generate more signals with time using [RPROB](https://vectorbt.pro/pvt_7a467f6b/api/signals/generators/rprob/#vectorbtpro.signals.generators.rprob.RPROB)! We'll start with the probability of 0% and end with the probability of 100% of placing a signal at each timestamp:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-1)>>> prob = np.linspace(0, 1, len(symbol_wrapper.index)) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-2)>>> rprob = vbt.RPROB.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-3)... symbol_wrapper.shape, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-4)... vbt.Default(vbt.to_2d_pr_array(prob)), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-5)... seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-6)... input_index=symbol_wrapper.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-7)... input_columns=symbol_wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-67-9)>>> rprob.entries.astype(int).vbt.ts_heatmap().show() 
 
[/code]

 1. 2. 3. 4. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/rprob.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/rprob.dark.svg#only-dark)

To test multiple values, we can provide them as a list. Let's prove that the fixed probability of 50% yields the same number of signals on average as the one ranging from 0% to 100% (but both are still totally different distributions!):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-1)>>> rprob = vbt.RPROB.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-2)... symbol_wrapper.shape,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-3)... [0.5, vbt.to_2d_pr_array(prob)],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-4)... seed=42,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-5)... input_index=symbol_wrapper.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-6)... input_columns=symbol_wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-8)>>> rprob.entries.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-9)rprob_prob symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-10)0.5 BTCUSDT 176
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-11) ETHUSDT 187
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-12)array_0 BTCUSDT 183
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-13) ETHUSDT 178
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-68-14)dtype: int64
 
[/code]


# Stops[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#stops "Permanent link")

Stop signals are an essential part of signal development because they allow us to propagate a stop condition throughout time. There are two main stop signal generators offered by vectorbt: a basic one that compares a single time series against any stop condition, and a specialized one that compares candlestick data against stop order conditions common in trading.

The first type can be run using the Numba-compiled function [stop_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.stop_place_nb) and its accessor instance method [SignalsAccessor.generate_stop_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_stop_exits). Additionally, there are indicator classes [STX](https://vectorbt.pro/pvt_7a467f6b/api/signals/generators/stx/#vectorbtpro.signals.generators.stx.STX) and [STCX](https://vectorbt.pro/pvt_7a467f6b/api/signals/generators/stcx/#vectorbtpro.signals.generators.stcx.STCX) that make the stop parametrizable. Let's use the accessor method to generate take profit (TP) signals. For this, we need four inputs: entry signals (`entries`), the entry price to apply the stop on (`entry_ts`), the high price (`ts`), and the actual stop(s) in % to compare the high price against (`stop`). We'll use the crossover entries generated previously. We'll also run the method in the chained exits mode to force vectorbt to wait for an exit and remove any entry signals that appear before.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-1)>>> new_entries, exits = entries.vbt.signals.generate_stop_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-2)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-3)... data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-4)... stop=0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-5)... chain=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-7)>>> new_entries[new_entries.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-8)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-9)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-10)2021-02-04 00:00:00+00:00 True False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-11)2021-03-10 00:00:00+00:00 True False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-12)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-13)2021-11-07 00:00:00+00:00 True False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-14)2021-12-02 00:00:00+00:00 False True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-16)>>> exits[exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-17)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-18)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-19)2021-02-06 00:00:00+00:00 True False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-20)2021-03-13 00:00:00+00:00 True False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-21)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-22)2021-10-15 00:00:00+00:00 False True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-69-23)2021-10-19 00:00:00+00:00 True False
 
[/code]

But how do we determine the stop price? Gladly, the Numba-compiled function also accepts a (required) in-output array `stop_ts` that is being written with the stop price of each exit. By default, vectorbt assumes that we're not interested in this array, and to avoid consuming much memory, it creates an empty (uninitialized) array, passes it to Numba, and deletes it afterwards. To make it return the array, we need to pass an empty dictionary `out_dict` where the accessor method can put the array. Whenever the `out_dict` is detected, vectorbt will create a full (initialized) array with `np.nan`, pass it to Numba, and put it back into the dictionary:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-1)>>> out_dict = {}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-2)>>> new_entries, exits = entries.vbt.signals.generate_stop_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-3)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-4)... data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-5)... stop=0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-6)... chain=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-7)... out_dict=out_dict
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-9)>>> out_dict["stop_ts"][exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-10)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-11)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-12)2021-02-06 00:00:00+00:00 40630.326 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-13)2021-03-13 00:00:00+00:00 61436.749 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-14)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-15)2021-10-15 00:00:00+00:00 NaN 3866.797
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-70-16)2021-10-19 00:00:00+00:00 63179.721 NaN
 
[/code]

Hint

We could have also passed our own (already created) `stop_ts` inside `out_dict` and vectorbt would override only those elements that correspond to exits!

The same can be done with the corresponding indicator class. But let's do something completely different: test two trailing stop loss (TSL) parameters instead, where the condition is following the high price upwards and is met once the low price crosses the stop value downwards. The high price can be specified with the argument `follow_ts`. The entry price will be the open price (even though we generated them using the close price, let's assume this scenario for a second), and thus we'll also allow placing the first signal at the entry bar by making `wait` zero:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-1)>>> stcx = vbt.STCX.run( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-2)... entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-3)... data.get("Open"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-4)... ts=data.get("Low"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-5)... follow_ts=data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-6)... stop=-0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-7)... trailing=[False, True], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-8)... wait=0 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-10)>>> fig = data.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-11)... symbol="BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-12)... ohlc_trace_kwargs=dict(opacity=0.5), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-13)... plot_volume=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-15)>>> stcx.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-16)... column=(-0.1, True, "BTCUSDT"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-17)... entry_y="entry_ts", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-18)... exit_y="stop_ts", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-19)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-20)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-71-21)>>> fig.show()
 
[/code]

 1. 2. 3. 4. 5. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/stcx.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/stcx.dark.svg#only-dark)

Note

Waiting time cannot be higher than 1. If waiting time is 0, `entry_ts` should be the first value in the bar. If waiting time is 1, `entry_ts` should be the last value in the bar, otherwise the stop could have also been hit at the first bar.

Also, by making the waiting time zero, you may get an entry and an exit at the same bar. Multiple orders at the same bar can only be implemented using a flexible order function or by converting the signals directly into order records. When passed directly to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals), any conflicting signals will be ignored.

If we're looking into placing solely SL, TSL, TP, and TTP orders, a more complete approach would be using the full OHLC information, which is utilized by the Numba-compiled function [ohlc_stop_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.ohlc_stop_place_nb), the accessor instance method [SignalsAccessor.generate_ohlc_stop_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits), and the corresponding indicator classes [OHLCSTX](https://vectorbt.pro/pvt_7a467f6b/api/signals/generators/ohlcstx/#vectorbtpro.signals.generators.ohlcstx.OHLCSTX) and [OHLCSTCX](https://vectorbt.pro/pvt_7a467f6b/api/signals/generators/ohlcstcx/#vectorbtpro.signals.generators.ohlcstcx.OHLCSTCX). The key advantage of this approach is the ability to check for all stop order conditions simultaneously!

Let's generate signals based on a [stop loss and trailing stop loss combo](https://www.investopedia.com/articles/trading/08/trailing-stop-loss.asp) of 10% and 15% respectively:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-1)>>> ohlcstcx = vbt.OHLCSTCX.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-2)... entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-3)... data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-4)... data.get("Open"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-5)... data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-6)... data.get("Low"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-7)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-8)... sl_stop=vbt.Default(0.1), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-9)... tsl_stop=vbt.Default(0.15),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-10)... is_entry_open=False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-72-12)>>> ohlcstcx.plot(column=("BTCUSDT")).show() 
 
[/code]

 1. 2. 3. 4. 5. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ohlcstcx.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ohlcstcx.dark.svg#only-dark)

Keep in mind that we don't have intra-candle data. If there was a huge price fluctuation in both directions, we wouldn't be able to determine whether SL was triggered before TP and vice versa. So some assumptions need to be made:

 * If a stop has been hit before the open price, the stop price becomes the current open price. This especially holds for `wait=1` and `is_entry_open=True`.
 * Trailing stop can only be based on the previous high/low price, not the current one
 * We pessimistically assume that any SL is triggered before any TP

A common tricky situation is when the entry price is the open price and we're waiting one bar. For instance, what would happen if the condition was met during the waiting time? We cannot place an exit signal at the entry bar. Instead, the function waits until the next bar and checks whether the condition is still valid for the open price. If yes, the signal is placed with the stop price being the open price. If not, the function simply waits until the next opportunity arrives. If the stop is trailing, the target price will update just as usual at the entry timestamp. To avoid any logical bugs, it's advised to use the close price as the entry price when `wait` is one bar (default).

When working with multiple stop types at the same time, we often want to know which exact type was triggered. This information is stored in the array `stop_type` (machine-readable) and `stop_type_readable` (human-readable):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-1)>>> ohlcstcx.stop_type_readable[ohlcstcx.exits.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-2)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-3)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-4)2021-02-22 00:00:00+00:00 TSL None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-5)2021-03-23 00:00:00+00:00 None TSL
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-6)2021-03-24 00:00:00+00:00 TSL None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-7)2021-04-18 00:00:00+00:00 SL TSL
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-8)2021-05-12 00:00:00+00:00 SL None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-9)2021-06-08 00:00:00+00:00 None SL
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-10)2021-06-18 00:00:00+00:00 SL None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-11)2021-07-09 00:00:00+00:00 None TSL
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-12)2021-07-19 00:00:00+00:00 SL None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-13)2021-09-07 00:00:00+00:00 TSL TSL
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-14)2021-11-16 00:00:00+00:00 TSL TSL
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-15)2021-12-03 00:00:00+00:00 None SL
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-16)2021-12-29 00:00:00+00:00 None SL
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-73-17)2021-12-31 00:00:00+00:00 SL None
 
[/code]

All the stop types are listed in the enumerated type [StopType](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.StopType).

Both stop signal generation modes are very flexible towards inputs. For example, if any element in the arrays `ts` and `follow_ts` in the first mode is NaN (default), it will be substituted by the element in `entry_ts`. If only an element in `follow_ts` is NaN, it will be substituted by the minimum or maximum (depending on the sign of the stop value) of the element in both other arrays. Similarly, in the second mode, we can provide only `entry_price` and vectorbt will auto-populate the open price if `is_entry_open` is enabled and the close price otherwise. Without `high`, vectorbt will take the maximum out of `open` and `close`. Generally, we're not forced to provide every bit of information apart from the entry price, but it's in our best interest to provide as much information as we can to make best decisions and to closely mimic the real world.

For example, let's run the same as above but specify the entry price only:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-74-1)>>> ohlcstcx = vbt.OHLCSTCX.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-74-2)... entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-74-3)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-74-4)... sl_stop=vbt.Default(0.1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-74-5)... tsl_stop=vbt.Default(0.15),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-74-6)... is_entry_open=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-74-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-74-8)>>> ohlcstcx.plot(column=("BTCUSDT")).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ohlcstcx2.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ohlcstcx2.dark.svg#only-dark)

The same flexibility goes for parameters: similarly to the behavior of the probability parameter in random signal generators, we can pass each parameter as an array, such as one element per row, column, or even element. Let's treat each second entry as a short entry and thus reverse the [trailing take profit](https://capitalise.ai/trailing-take-profit-manage-your-risk-while-locking-the-profits/) (TTP) logic for it:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-1)>>> entry_pos_rank = entries.vbt.signals.pos_rank(allow_gaps=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-2)>>> short_entries = (entry_pos_rank >= 0) & (entry_pos_rank % 2 == 1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-4)>>> ohlcstcx = vbt.OHLCSTCX.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-5)... entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-6)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-7)... data.get("Open"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-8)... data.get("High"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-9)... data.get("Low"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-10)... data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-11)... tsl_th=vbt.Default(0.2), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-12)... tsl_stop=vbt.Default(0.1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-13)... reverse=vbt.Default(short_entries), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-14)... is_entry_open=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-75-16)>>> ohlcstcx.plot(column=("BTCUSDT")).show()
 
[/code]

 1. 2. 3. 4. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ohlcstcx3.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ohlcstcx3.dark.svg#only-dark)

We can then split both final arrays into four direction-aware arrays for simulation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-1)>>> long_entries = ohlcstcx.new_entries.vbt & (~short_entries) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-2)>>> long_exits = ohlcstcx.exits.vbt.signals.first_after(long_entries) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-3)>>> short_entries = ohlcstcx.new_entries.vbt & short_entries
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-4)>>> short_exits = ohlcstcx.exits.vbt.signals.first_after(short_entries)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-6)>>> fig = data.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-7)... symbol="BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-8)... ohlc_trace_kwargs=dict(opacity=0.5), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-9)... plot_volume=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-11)>>> long_entries["BTCUSDT"].vbt.signals.plot_as_entries(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-12)... ohlcstcx.entry_price["BTCUSDT"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-13)... trace_kwargs=dict(marker=dict(color="limegreen"), name="Long entries"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-14)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-16)>>> long_exits["BTCUSDT"].vbt.signals.plot_as_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-17)... ohlcstcx.stop_price["BTCUSDT"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-18)... trace_kwargs=dict(marker=dict(color="orange"), name="Long exits"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-19)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-20)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-21)>>> short_entries["BTCUSDT"].vbt.signals.plot_as_entries(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-22)... ohlcstcx.entry_price["BTCUSDT"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-23)... trace_kwargs=dict(marker=dict(color="magenta"), name="Short entries"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-24)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-26)>>> short_exits["BTCUSDT"].vbt.signals.plot_as_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-27)... ohlcstcx.stop_price["BTCUSDT"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-28)... trace_kwargs=dict(marker=dict(color="red"), name="Short exits"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-29)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-30)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#__codelineno-76-31)>>> fig.show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ohlcstcx4.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/ohlcstcx4.dark.svg#only-dark)

Seems like all trades are winning, thanks to a range-bound but still volatile market ![🍀](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f340.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/signal-development/generation.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/SignalDevelopment.ipynb)