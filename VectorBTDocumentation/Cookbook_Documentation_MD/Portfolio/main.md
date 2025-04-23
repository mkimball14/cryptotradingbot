# Portfolio[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#portfolio "Permanent link")

Question

Learn more in [Portfolio documentation](https://vectorbt.pro/pvt_7a467f6b/documentation/portfolio/).


# From data[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#from-data "Permanent link")

To quickly simulate a portfolio from any OHLC data, either use [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run) or pass the data instance (or just a symbol or `class_name:symbol`) to the simulation method.

Various way to quickly simulate a portfolio from a Data instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-0-1)pf = data.run("from_holding") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-0-2)pf = data.run("from_random_signals", n=10) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-0-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-0-4)pf = vbt.PF.from_holding(data) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-0-5)pf = vbt.PF.from_holding("BTC-USD") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-0-6)pf = vbt.PF.from_holding("BinanceData:BTCUSDT") 
 
[/code]

 1. 2. 3. 4. 5. 


# From signals[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#from-signals "Permanent link")

This simulation method is easy to use but still very powerful as long as your strategy can be expressed as signals, such as buy, sell, short sell, and buy to cover.

Various signal configurations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-1)pf = vbt.PF.from_signals(data, ...) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-2)pf = vbt.PF.from_signals(open=open, high=high, low=low, close=close, ...) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-3)pf = vbt.PF.from_signals(close, ...) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-5)pf = vbt.PF.from_signals(data, entries, exits) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-6)pf = vbt.PF.from_signals(data, entries, exits, direction="shortonly") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-7)pf = vbt.PF.from_signals(data, entries, exits, direction="both") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-8)pf = vbt.PF.from_signals( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-9) data, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-10) long_entries=long_entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-11) long_exits=long_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-12) short_entries=short_entries, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-13) short_exits=short_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-1-14))
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 


* * *

+


* * *

To specify a different price or other argument for long and short signals, create an empty array and use each signal type as a mask to set the corresponding value.

Manually apply a 1% slippage to the price
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-2-1)price = data.symbol_wrapper.fill()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-2-2)price[entries] = data.close * (1 + 0.01) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-2-3)price[exits] = data.close * (1 - 0.01)
 
[/code]

 1. 

Use the ask price for buying and the bid price for selling
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-3-1)price = (bid_price + ask_price) / 2
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-3-2)price[entries] = ask_price
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-3-3)price[exits] = bid_price
 
[/code]


* * *

+


* * *

To exit a trade after a specific amount of time or number of rows, use the `td_stop` argument. The measurement is done from the opening time of the entry row.

How to close out a position after some time
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-4-1)pf = vbt.PF.from_signals(..., td_stop="7 days") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-4-2)pf = vbt.PF.from_signals(..., td_stop=pd.Timedelta(days=7))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-4-3)pf = vbt.PF.from_signals(..., td_stop=td_arr) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-4-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-4-5)pf = vbt.PF.from_signals(..., td_stop=7, time_delta_format="rows") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-4-6)pf = vbt.PF.from_signals(..., td_stop=int_arr, time_delta_format="rows") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-4-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-4-8)pf = vbt.PF.from_signals(..., td_stop=vbt.Param(["1 day", "7 days"])) 
 
[/code]

 1. 2. 3. 4. 5. 


* * *

+


* * *

To exit a trade at some specific point of time or number of rows, use the `dt_stop` argument. If you pass a timedelta (like above), the position will be exited at the last bar _before_ the target date. Otherwise, if you pass an exact date or time, the position will be exited _at_ or _after_ it. This behavior can be overridden via the argument config.

How to close out a position at some time
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-1)import datetime
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-3)pf = vbt.PF.from_signals(..., dt_stop="daily") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-4)pf = vbt.PF.from_signals(..., dt_stop=pd.Timedelta(days=1))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-5)pf = vbt.PF.from_signals( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-6) ..., 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-7) dt_stop="daily", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-8) arg_config=dict(dt_stop=dict(last_before=False))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-9))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-11)pf = vbt.PF.from_signals(..., dt_stop="16:00") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-12)pf = vbt.PF.from_signals(..., dt_stop=datetime.time(16, 0))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-13)pf = vbt.PF.from_signals( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-14) ..., 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-15) dt_stop="16:00", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-16) arg_config=dict(dt_stop=dict(last_before=True))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-17))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-18)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-19)pf = vbt.PF.from_signals(..., dt_stop="2024-01-01") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-20)pf = vbt.PF.from_signals(..., dt_stop=pd.Timestamp("2024-01-01"))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-21)pf = vbt.PF.from_signals( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-22) ..., 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-23) dt_stop="2024-01-01", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-24) arg_config=dict(dt_stop=dict(last_before=True))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-25))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-26)pf = vbt.PF.from_signals(..., dt_stop=dt_arr) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-27)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-28)pf = vbt.PF.from_signals(..., dt_stop=int_arr, time_delta_format="rows") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-29)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-5-30)pf = vbt.PF.from_signals(..., dt_stop=vbt.Param(["1 day", "7 days"])) 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 

Note

Don't confuse `td_stop` with `dt_stop` \- "td" is an abbreviation for a timedelta while "dt" is an abbreviation for a datetime.


* * *

+


* * *

To perform multiple actions per bar, the trick is to split each bar into three sub-bars: opening nanosecond, middle, closing nanosecond. For example, you can execute your signals at the end of the bar and your stop orders will guarantee to be executed at the first two sub-bars, so you can close out your position and enter a new one at the same bar.

Execute entries at open, exits at close
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-1)x3_open = open.vbt.repeat(3, axis=0) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-2)x3_high = high.vbt.repeat(3, axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-3)x3_low = low.vbt.repeat(3, axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-4)x3_close = close.vbt.repeat(3, axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-5)x3_entries = entries.vbt.repeat(3, axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-6)x3_exits = exits.vbt.repeat(3, axis=0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-8)bar_open = slice(0, None, 3) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-9)bar_middle = slice(1, None, 3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-10)bar_close = slice(2, None, 3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-12)x3_high.iloc[bar_open] = open.copy() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-13)x3_low.iloc[bar_open] = open.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-14)x3_close.iloc[bar_open] = open.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-15)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-16)x3_open.iloc[bar_close] = close.copy() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-17)x3_high.iloc[bar_close] = close.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-18)x3_low.iloc[bar_close] = close.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-19)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-20)x3_entries.iloc[bar_middle] = False 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-21)x3_entries.iloc[bar_close] = False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-22)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-23)x3_exits.iloc[bar_open] = False 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-24)x3_exits.iloc[bar_middle] = False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-25)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-26)x3_index = pd.Series(x3_close.index) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-27)x3_index.iloc[bar_middle] += pd.Timedelta(nanoseconds=1)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-28)x3_index.iloc[bar_close] += index.freq - pd.Timedelta(nanoseconds=1)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-29)x3_index = pd.Index(x3_index)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-30)x3_open.index = x3_index
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-31)x3_high.index = x3_index
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-32)x3_low.index = x3_index
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-33)x3_close.index = x3_index
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-34)x3_entries.index = x3_index
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-35)x3_exits.index = x3_index
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-36)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-37)x3_pf = vbt.PF.from_signals( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-38) open=x3_open,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-39) high=x3_high,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-40) low=x3_low,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-41) close=x3_close,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-42) entries=x3_entries,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-43) exits=x3_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-44))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-6-45)pf = x3_pf.resample(close.index, freq=False, silence_warnings=True) 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 


# Callbacks[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#callbacks "Permanent link")

To save an information piece at one timestamp and re-use at a later timestamp in a callback, create a NumPy array and pass it to the callback. The array should be one-dimensional and have the same number of elements as there are columns. The element under the current column can then be read and written using the same mechanism as accessing the latest position via `c.last_position[c.col]`. More information pieces would require either more arrays or one structured array. Multiple arrays can be put into a named tuple for convenience.

Execute only the first signal
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-1)from collections import namedtuple
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-3)Memory = namedtuple("Memory", ["signal_executed"])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-5)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-6)def signal_func_nb(c, entries, exits, memory):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-7) is_entry = vbt.pf_nb.select_nb(c, entries)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-8) is_exit = vbt.pf_nb.select_nb(c, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-9) if is_entry and not memory.signal_executed[c.col]: 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-10) memory.signal_executed[c.col] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-11) return True, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-12) if is_exit:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-13) return False, True, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-14) return False, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-15)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-16)def init_memory(target_shape):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-17) return Memory(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-18) signal_executed=np.full(target_shape[1], False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-19) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-20)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-21)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-22) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-23) entries=entries,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-24) exits=exits,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-25) signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-26) signal_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-27) vbt.Rep("entries"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-28) vbt.Rep("exits"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-29) vbt.RepFunc(init_memory)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-30) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-7-31))
 
[/code]

 1. 2. 3. 


* * *

+


* * *

To overcome the restriction of having only one active built-in limit order at a time, you can create custom limit orders, allowing you to have multiple active orders simultaneously. This can be achieved by storing relevant data in memory and manually checking if the limit order price has been reached each bar. When the price is hit, simply generate a signal.

Breakout strategy by straddling current price with opposing limit orders
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-1)Memory = namedtuple("Memory", ["signal_price"]) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-3)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-4)def signal_func_nb(c, signals, memory, limit_delta):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-5) if np.isnan(memory.signal_price[c.col]):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-6) signal = vbt.pf_nb.select_nb(c, signals)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-7) if signal:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-8) memory.signal_price[c.col] = vbt.pf_nb.select_nb(c, c.close) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-9) else:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-10) open = vbt.pf_nb.select_nb(c, c.open)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-11) high = vbt.pf_nb.select_nb(c, c.high)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-12) low = vbt.pf_nb.select_nb(c, c.low)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-13) close = vbt.pf_nb.select_nb(c, c.close)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-14) above_price = vbt.pf_nb.resolve_limit_price_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-15) init_price=memory.signal_price[c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-16) limit_delta=limit_delta,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-17) hit_below=False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-18) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-19) if vbt.pf_nb.check_price_hit_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-20) open=open,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-21) high=high,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-22) low=low,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-23) close=close,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-24) price=above_price,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-25) hit_below=False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-26) )[2]:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-27) memory.signal_price[c.col] = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-28) return True, False, False, False 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-29) below_price = vbt.pf_nb.resolve_limit_price_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-30) init_price=memory.signal_price[c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-31) limit_delta=limit_delta,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-32) hit_below=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-33) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-34) if vbt.pf_nb.check_price_hit_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-35) open=open,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-36) high=high,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-37) low=low,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-38) close=close,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-39) price=below_price,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-40) hit_below=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-41) )[2]:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-42) memory.signal_price[c.col] = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-43) return False, False, True, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-44) return False, False, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-45)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-46)def init_memory(target_shape):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-47) return Memory(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-48) signal_price=np.full(target_shape[1], np.nan)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-49) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-50)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-51)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-52) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-53) signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-54) signal_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-55) vbt.Rep("signals"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-56) vbt.RepFunc(init_memory),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-57) 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-58) ),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-59) broadcast_named_args=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-60) signals=signals
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-61) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-8-62))
 
[/code]

 1. 2. 3. 4. 5. 6. 


* * *

+


* * *

If signals are generated dynamically and only a subset of the signals are actually executed, you may want to keep track of all the generated signals for later analysis. For this, use function templates to create **global** custom arrays and fill those arrays during the simulation.

Place entries and exits randomly and access them outside the simulation
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-1)custom_arrays = dict()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-3)def create_entries_out(wrapper): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-4) entries_out = np.full(wrapper.shape_2d, False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-5) custom_arrays["entries"] = entries_out 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-6) return entries_out
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-8)def create_exits_out(wrapper):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-9) exits_out = np.full(wrapper.shape_2d, False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-10) custom_arrays["exits"] = exits_out
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-11) return exits_out
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-13)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-14)def signal_func_nb(c, entry_prob, exit_prob, entries_out, exits_out):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-15) entry_prob_now = vbt.pf_nb.select_nb(c, entry_prob)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-16) exit_prob_now = vbt.pf_nb.select_nb(c, exit_prob)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-17) if np.random.uniform(0, 1) < entry_prob_now:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-18) is_entry = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-19) entries_out[c.i, c.col] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-20) else:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-21) is_entry = False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-22) if np.random.uniform(0, 1) < exit_prob_now:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-23) is_exit = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-24) exits_out[c.i, c.col] = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-25) else:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-26) is_exit = False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-27) return is_entry, is_exit, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-28)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-29)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-30) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-31) signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-32) signal_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-33) vbt.Rep("entry_prob"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-34) vbt.Rep("exit_prob"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-35) vbt.RepFunc(create_entries_out), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-36) vbt.RepFunc(create_exits_out),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-37) ),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-38) broadcast_named_args=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-39) entry_prob=0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-40) exit_prob=0.1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-41) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-42))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-43)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-9-44)print(custom_arrays)
 
[/code]

 1. 2. 3. 4. 


* * *

+


* * *

To limit the number of active positions within a group, in a custom signal function, disable any entry signal whenever the number has been reached. The exit signal should be allowed to be executed at any time.

Allow at most one active position at a time
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-2)def signal_func_nb(c, entries, exits, max_active_positions):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-3) is_entry = vbt.pf_nb.select_nb(c, entries)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-4) is_exit = vbt.pf_nb.select_nb(c, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-5) n_active_positions = vbt.pf_nb.get_n_active_positions_nb(c)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-6) if n_active_positions >= max_active_positions:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-7) return False, is_exit, False, False 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-8) return is_entry, is_exit, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-10)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-11) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-12) entries=entries,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-13) exits=exits,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-14) signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-15) signal_args=(vbt.Rep("entries"), vbt.Rep("exits"), 1),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-16) group_by=True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-10-17))
 
[/code]

 1. 2. 


* * *

+


* * *

To access information on the current or previous position, query the position information records.

Ignore entries for a number of days after a losing trade
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-2)def signal_func_nb(c, entries, exits, cooldown):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-3) entry = vbt.pf_nb.select_nb(c, entries)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-4) exit = vbt.pf_nb.select_nb(c, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-5) if not vbt.pf_nb.in_position_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-6) if vbt.pf_nb.has_orders_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-7) if c.last_pos_info[c.col]["pnl"] < 0: 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-8) last_exit_idx = c.last_pos_info[c.col]["exit_idx"]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-9) if c.index[c.i] - c.index[last_exit_idx] < cooldown:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-10) return False, exit, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-11) return entry, exit, False, False
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-13)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-14) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-15) signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-16) signal_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-17) vbt.Rep("entries"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-18) vbt.Rep("exits"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-19) vbt.dt.to_ns(vbt.timedelta("7D"))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-20) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-11-21))
 
[/code]

 1. 2. Cooldown should be an integer representing a number of nanoseconds, thus any timedelta should be converted to the number of nanoseconds prior to execution


* * *

+


* * *

To activate SL or other stop order after a certain condition, set it initially to infinity and then change the stop value in a callback once the condition is met.

Set SL to breakeven after price has moved a certain %
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-2)def adjust_func_nb(c, perc):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-4) sl_stop = c.last_sl_info[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-5) if c.i > 0 and np.isinf(sl_stop["stop"]): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-6) prev_close = vbt.pf_nb.select_nb(c, c.close, i=c.i - 1)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-7) price_change = prev_close / sl_stop["init_price"] - 1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-8) if c.last_position[c.col] < 0:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-9) price_change *= -1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-10) if price_change >= perc:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-11) sl_stop["stop"] = 0.0 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-13)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-14) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-15) sl_stop=np.inf,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-16) stop_entry_price="fillprice",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-17) adjust_func_nb=adjust_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-18) adjust_args=(0.1,),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-12-19))
 
[/code]

 1. 2. 


* * *

+


* * *

Stop value can be changed not only once, but at every bar.

ATR-based TSL order
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-2)def adjust_func_nb(c, atr):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-4) if c.i > 0:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-5) tsl_info = c.last_tsl_info[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-6) tsl_info["stop"] = vbt.pf_nb.select_nb(c, atr, i=c.i - 1)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-8)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-9) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-10) tsl_stop=np.inf,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-11) stop_entry_price="fillprice",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-12) delta_format="absolute",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-13) broadcast_named_args=dict(atr=atr),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-14) adjust_func_nb=adjust_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-15) adjust_args=(vbt.Rep("atr"),)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-13-16))
 
[/code]


* * *

+


* * *

To set a ladder dynamically, use `stop_ladder="dynamic"` and then in a callback use the current ladder step to pull information from a custom array and override the stop information with it.

Set a ladder based on ATR multipliers
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-2)def adjust_func_nb(c, atr, multipliers, exit_sizes):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-3) tp_info = c.last_tp_info[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-4) if vbt.pf_nb.is_stop_info_ladder_active_nb(tp_info):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-5) if np.isnan(tp_info["stop"]):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-6) step = tp_info["step"]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-7) init_atr = vbt.pf_nb.select_nb(c, atr, i=tp_info["init_idx"])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-8) tp_info["stop"] = init_atr * multipliers[step]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-9) tp_info["delta_format"] = vbt.pf_enums.DeltaFormat.Absolute
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-10) tp_info["exit_size"] = exit_sizes[step]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-11) tp_info["exit_size_type"] = vbt.pf_enums.SizeType.Percent
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-13)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-14) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-15) adjust_func_nb=adjust_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-16) adjust_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-17) vbt.Rep("atr"),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-18) np.array([1, 2]),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-19) np.array([0.5, 1.0])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-20) ),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-21) stop_ladder="dynamic",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-22) broadcast_named_args=dict(atr=atr)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-14-23))
 
[/code]


* * *

+


* * *

Position metrics such as the current open P&L and return are available via the `last_pos_info` context field, which is an array with one record per column and the data type [trade_dt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.trade_dt).

By hitting an unrealized profit of 100%, lock in 50% of it with SL
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-2)def adjust_func_nb(c, x, y): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-3) pos_info = c.last_pos_info[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-4) if pos_info["status"] == vbt.pf_enums.TradeStatus.Open:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-5) if pos_info["return"] >= x:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-6) sl_info = c.last_sl_info[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-7) if not vbt.pf_nb.is_stop_info_active_nb(sl_info):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-8) entry_price = pos_info["entry_price"]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-9) if vbt.pf_nb.in_long_position_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-10) x_price = entry_price * (1 + x) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-11) y_price = entry_price * (1 + y) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-12) else:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-13) x_price = entry_price * (1 - x)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-14) y_price = entry_price * (1 - y)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-15) vbt.pf_nb.set_sl_info_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-16) sl_info, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-17) init_idx=c.i, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-18) init_price=x_price,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-19) stop=y_price,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-20) delta_format=vbt.pf_enums.DeltaFormat.Target
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-21) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-22)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-23)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-24) ..., 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-25) adjust_func_nb=adjust_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-26) adjust_args=(1.0, 0.5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-15-27))
 
[/code]

 1. 2. 3. 


* * *

+


* * *

To dynamically determine and apply an optimal position size, create an empty size array full of NaN, and in a callback, compute the target size and write it to the size array.

Risk only 1% of the cash balance with each trade
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-2)def adjust_func_nb(c, size, sl_stop, delta_format, risk_amount):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-3) close_now = vbt.pf_nb.select_nb(c, c.close)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-4) sl_stop_now = vbt.pf_nb.select_nb(c, sl_stop)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-5) delta_format_now = vbt.pf_nb.select_nb(c, delta_format)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-6) risk_amount_now = vbt.pf_nb.select_nb(c, risk_amount)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-7) free_cash_now = vbt.pf_nb.get_free_cash_nb(c)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-9) stop_price = vbt.pf_nb.resolve_stop_price_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-10) init_price=close_now,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-11) stop=sl_stop_now,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-12) delta_format=delta_format_now,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-13) hit_below=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-14) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-15) price_diff = abs(close_now - stop_price)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-16) size[c.i, c.col] = risk_amount_now * free_cash_now / price_diff
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-18)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-19) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-20) adjust_func_nb=adjust_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-21) adjust_args=(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-22) vbt.Rep("size"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-23) vbt.Rep("sl_stop"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-24) vbt.Rep("delta_format"), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-25) vbt.Rep("risk_amount")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-26) ),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-27) size=vbt.RepFunc(lambda wrapper: np.full(wrapper.shape_2d, np.nan)),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-28) sl_stop=0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-29) delta_format="percent",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-30) broadcast_named_args=dict(risk_amount=0.01)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-16-31))
 
[/code]


* * *

+


* * *

To make SL/TP consider the average entry price instead of the entry price of the first order only when accumulation is enabled, set the initial price of the stop record to the entry price of the position.

Apply an SL of 10% to the accumulated position
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-2)def post_signal_func_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-3) if vbt.pf_nb.order_increased_position_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-4) c.last_sl_info[c.col]["init_price"] = c.last_pos_info[c.col]["entry_price"]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-6)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-7) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-8) accumulate="addonly",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-9) sl_stop=0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-10) post_signal_func_nb=post_signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-17-11))
 
[/code]


* * *

+


* * *

To check at the end of the bar whether a signal has been executed, use `post_signal_func_nb` or `post_segment_func_nb`. The former is called right after an order was executed and can access information on the result of the executed order (`c.order_result`). The latter is called after all the columns in the current group were processed (just one column if there's no grouping), cash deposits and earnings were applied, and the portfolio value and returns were updated.

Apply a 20% tax on any positive P&L generated from closing out a position
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-2)def post_signal_func_nb(c, cash_earnings, tax):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-3) if vbt.pf_nb.order_closed_position_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-4) pos_info = c.last_pos_info[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-5) pnl = pos_info["pnl"]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-6) if pnl > 0:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-7) cash_earnings[c.i, c.col] = -tax * pnl
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-9)tax = 0.2
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-10)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-11) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-12) post_signal_func_nb=post_signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-13) post_signal_args=(vbt.Rep("cash_earnings"), tax),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-14) cash_earnings=vbt.RepEval("np.full(wrapper.shape_2d, 0.0)")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-18-15))
 
[/code]

Tip

Alternative approach after creating the portfolio:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-1)winning_positions = pf.positions.winning
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-2)winning_idxs = winning_positions.end_idx.values
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-3)winning_pnl = winning_positions.pnl.values
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-4)cash_earnings = pf.get_cash_earnings(group_by=False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-5)if pf.wrapper.ndim == 2:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-6) winning_cols = winning_positions.col_arr
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-7) cash_earnings.values[winning_idxs, winning_cols] += -tax * winning_pnl
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-8)else:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-9) cash_earnings.values[winning_idxs] += -tax * winning_pnl
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-19-10)new_pf = pf.replace(cash_earnings=cash_earnings)
 
[/code]


* * *

+


* * *

To be able to access the running total return of the simulation, create an empty array for cumulative returns and populate it inside the `post_segment_func_nb` callback. The same array accessed by other callbacks can be used to get the total return at any time step.

Access the running total return from within a simulation
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-1)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-2)def adjust_func_nb(c, cum_return):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-3) if c.cash_sharing:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-4) total_return = cum_return[c.group] - 1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-5) else:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-6) total_return = cum_return[c.col] - 1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-7) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-9)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-10)def post_segment_func_nb(c, cum_return):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-11) if c.cash_sharing:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-12) cum_return[c.group] *= 1 + c.last_return[c.group]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-13) else:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-14) for col in range(c.from_col, c.to_col):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-15) cum_return[col] *= 1 + c.last_return[col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-17)cum_return = None
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-18)def init_cum_return(wrapper):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-19) global cum_return
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-20) if cum_return is None:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-21) cum_return = np.full(wrapper.shape_2d[1], 1.0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-22) return cum_return
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-23)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-24)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-25) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-26) adjust_func_nb=adjust_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-27) adjust_args=(vbt.RepFunc(init_cum_return),),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-28) post_segment_func_nb=post_segment_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-29) post_segment_args=(vbt.RepFunc(init_cum_return),),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-20-30))
 
[/code]

 1. 


* * *

+


* * *

The same procedure can be applied to access the running trade records of the simulation.

Access the running trade records from within a simulation
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-1)from collections import namedtuple
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-3)TradeMemory = namedtuple("TradeMemory", ["trade_records", "trade_counts"])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-5)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-6)def adjust_func_nb(c, trade_memory):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-7) trade_count = trade_memory.trade_counts[c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-8) trade_records = trade_memory.trade_records[:trade_count, c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-9) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-10)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-11)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-12)def post_signal_func_nb(c, trade_memory):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-13) if vbt.pf_nb.order_filled_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-14) exit_trade_records = vbt.pf_nb.get_exit_trade_records_nb(c)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-15) trade_memory.trade_records[:len(exit_trade_records), c.col] = exit_trade_records
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-16) trade_memory.trade_counts[c.col] = len(exit_trade_records)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-18)trade_memory = None
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-19)def init_trade_memory(target_shape):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-20) global trade_memory
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-21) if trade_memory is None:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-22) trade_memory = TradeMemory(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-23) trade_records=np.empty(target_shape, dtype=vbt.pf_enums.trade_dt), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-24) trade_counts=np.full(target_shape[1], 0)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-25) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-26) return trade_memory
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-27)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-28)pf = vbt.PF.from_random_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-29) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-30) post_signal_func_nb=post_signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-31) post_signal_args=(vbt.RepFunc(init_trade_memory),),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-21-32))
 
[/code]

 1. 2. 


* * *

+


* * *

To execute SL (or any other order type) at the same bar as entry, we can check whether the stop order can be fulfilled at this bar, and if so, execute it as a regular signal at the next bar.

Execute each entry using open price and potentially SL at the same bar
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-1)Memory = namedtuple("Memory", ["stop_price", "order_type"])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-2)memory = None
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-4)def init_memory(target_shape):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-5) global memory
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-6) if memory is None:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-7) memory = Memory(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-8) stop_price=np.full(target_shape, np.nan),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-9) order_type=np.full(target_shape, -1),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-10) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-11) return memory
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-13)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-14)def signal_func_nb(c, price, memory, ...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-15) if c.i > 0 and not np.isnan(memory.stop_price[c.i - 1, c.col]):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-16) price[c.i, c.col] = memory.stop_price[c.i - 1, c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-17) return False, True, False, True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-18) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-19)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-20)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-21)@njit
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-22)def post_signal_func_nb(c, memory, ...):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-23) if vbt.pf_nb.order_opened_position_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-24) open = vbt.pf_nb.select_nb(c, c.open)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-25) high = vbt.pf_nb.select_nb(c, c.high)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-26) low = vbt.pf_nb.select_nb(c, c.low)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-27) close = vbt.pf_nb.select_nb(c, c.close)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-28) sl_stop_price, _, sl_stop_hit = vbt.pf_nb.check_stop_hit_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-29) open=open,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-30) high=high,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-31) low=low,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-32) close=close,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-33) is_position_long=c.last_position[c.col] > 0,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-34) init_price=c.last_sl_info["init_price"][c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-35) stop=c.last_sl_info["stop"][c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-36) delta_format=c.last_sl_info["delta_format"][c.col],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-37) hit_below=True,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-38) can_use_ohlc=True,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-39) check_open=False,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-40) hard_stop=c.last_sl_info["exit_price"][c.col] == vbt.pf_enums.StopExitPrice.HardStop,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-41) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-42) if sl_stop_hit:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-43) memory.stop_price[c.i, c.col] = sl_stop_price
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-44) memory.order_type[c.i, c.col] = vbt.sig_enums.StopType.SL
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-45) vbt.pf_nb.clear_sl_info_nb(c.last_sl_info[c.col])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-46) vbt.pf_nb.clear_tp_info_nb(c.last_tp_info[c.col])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-47)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-48) elif vbt.pf_nb.order_closed_position_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-49) if memory.order_type[c.i - 1, c.col] != -1:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-50) order = c.order_records[c.order_counts[c.col] - 1, c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-51) order["stop_type"] = memory.order_type[c.i - 1, c.col]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-52) order["signal_idx"] = c.i - 1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-53) order["creation_idx"] = c.i - 1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-54) order["idx"] = c.i - 1
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-55) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-56)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-57)pf = vbt.PF.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-58) ...,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-59) signal_func_nb=signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-60) signal_args=(vbt.Rep("price"), vbt.RepFunc(init_memory), ...),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-61) post_signal_func_nb=post_signal_func_nb,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-62) post_signal_args=(vbt.RepFunc(init_memory), ...),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-63) price=vbt.RepFunc(lambda wrapper: np.full(wrapper.shape_2d, -np.inf)),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-64) sl_stop=0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-65) stop_entry_price="fillprice"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-22-66))
 
[/code]


# Records[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#records "Permanent link")

There are various ways to examine the orders, trades, and positions generated by a simulation. They all represent different concepts in vectorbtpro, make sure to learn their differences by reading the examples listed at the top of the [trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/) module.

Print out information on various records
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-23-1)print(pf.orders.readable) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-23-2)print(pf.entry_trades.readable) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-23-3)print(pf.exit_trades.readable) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-23-4)print(pf.trades.readable) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-23-5)print(pf.positions.readable) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-23-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-23-7)print(pf.trade_history) 
 
[/code]

 1. 2. 3. 4. 5. 6. 


# Metrics[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#metrics "Permanent link")

The default year frequency is 365 days, which also assumes that a trading day spans over 24 hours, but when trading stocks or other securities it must be changed to 252 days or less. Also, you must account for trading hours when dealing with a sub-daily data frequency.

Change the year frequency
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-1)vbt.settings.returns.year_freq = "auto" 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-3)vbt.settings.returns.year_freq = "252 days" 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-4)vbt.settings.returns.year_freq = pd.Timedelta(days=252) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-5)vbt.settings.returns.year_freq = pd.offsets.BDay() * 252 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-6)vbt.settings.returns.year_freq = pd.Timedelta(hours=6.5) * 252 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-8)returns_df.vbt.returns(year_freq="252 days").stats() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-24-9)pf = vbt.PF.from_signals(..., year_freq="252 days") 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

Info

The year frequency will be divided by the frequency of your data to get the annualization factor. For example, `pd.Timedelta(hours=6.5) * 252` divided by `15 minutes` will yield a factor of 6552.


* * *

+


* * *

To instruct VBT to put zero instead of infinity and NaN in any generated returns, create a [configuration](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#settings) file (such as `vbt.config`) with the following content:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-25-1)[returns]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-25-2)inf_to_nan = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-25-3)nan_to_zero = True
 
[/code]

Note

If there is no change, run `vbt.clear_pycache()` and restart the kernel.


* * *

+


* * *

To compute a metric based on the returns or other time series of each trade rather than the entire equity, use projections to extract the time series range that corresponds to the trade.

Calculate the average total log return of winning and losing trades
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-26-1)winning_trade_returns = pf.trades.winning.get_projections(pf.log_returns, rebase=False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-26-2)losing_trade_returns = pf.trades.losing.get_projections(pf.log_returns, rebase=False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-26-3)avg_winning_trade_return = vbt.pd_acc.returns(winning_trade_returns, log_returns=True).total().mean()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-26-4)avg_losing_trade_return = vbt.pd_acc.returns(losing_trade_returns, log_returns=True).total().mean()
 
[/code]


* * *

+


* * *

To compute a trade metric in pure Numba: convert order records into trade records, calculate the column map for the trade records, and then reduce each column into a single number.

Calculate trade win rate in Numba
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-1)order_records = sim_out.order_records 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-3)order_col_map = vbt.rec_nb.col_map_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-4) order_records["col"],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-5) close.shape[1] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-6))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-7)trade_records = vbt.pf_nb.get_exit_trades_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-8) order_records, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-9) close, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-10) order_col_map
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-11))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-12)trade_col_map = vbt.rec_nb.col_map_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-13) trade_records["col"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-14) close.shape[1]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-15))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-16)win_rate = vbt.rec_nb.reduce_mapped_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-17) trade_records["pnl"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-18) trade_col_map, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-19) np.nan, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-20) vbt.pf_nb.win_rate_reduce_nb
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-27-21))
 
[/code]

 1. 2. 


* * *

+


* * *

Same goes for drawdown records, which are based on cumulative returns.

Calculate maximum drawdown duration in Numba
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-1)returns = sim_out.in_outputs.returns
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-3)cumulative_returns = vbt.ret_nb.cumulative_returns_nb(returns) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-4)drawdown_records = vbt.nb.get_drawdowns_nb(None, None, None, cumulative_returns)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-5)dd_duration = vbt.nb.range_duration_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-6) drawdown_records["start_idx"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-7) drawdown_records["end_idx"], 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-8) drawdown_records["status"]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-9))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-10)dd_col_map = vbt.rec_nb.col_map_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-11) drawdown_records["col"],
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-12) returns.shape[1]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-13))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-14)max_dd_duration = vbt.rec_nb.reduce_mapped_nb( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-15) dd_duration,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-16) dd_col_map,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-17) np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-18) vbt.nb.max_reduce_nb
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-28-19))
 
[/code]

 1. 2. 3. 


* * *

+


* * *

Return metrics aren't based on records but can be calculated directly from returns.

Calculate various return metrics in Numba
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-29-1)returns = sim_out.in_outputs.returns
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-29-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-29-3)total_return = vbt.ret_nb.total_return_nb(returns) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-29-4)max_dd = vbt.ret_nb.max_drawdown_nb(returns) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-29-5)sharpe_ratio = vbt.ret_nb.sharpe_ratio_nb(returns, ann_factor=ann_factor) 
 
[/code]

 1. 2. 3. 


# Metadata[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#metadata "Permanent link")

The columns and groups of the portfolio can be accessed via its wrapper and grouper respectively.

How to get the columns and groups of a Portfolio instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-30-1)print(pf.wrapper.columns) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-30-2)print(pf.wrapper.grouper.is_grouped()) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-30-3)print(pf.wrapper.grouper.grouped_index) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-30-4)print(pf.wrapper.get_columns()) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-30-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-30-6)columns_or_groups = pf.wrapper.get_columns()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-30-7)first_pf = pf[columns_or_groups[0]] 
 
[/code]

 1. 2. 3. 4. 5. 


# Stacking[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#stacking "Permanent link")

Multiple compatible array-based strategies can be put into the same portfolio by stacking their respective arrays along columns.

Simulate and analyze multiple strategies jointly
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-31-1)strategy_keys = pd.Index(["strategy1", "strategy2"], name="strategy")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-31-2)entries = pd.concat((entries1, entries2), axis=1, keys=strategy_keys)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-31-3)exits = pd.concat((exits1, exits2), axis=1, keys=strategy_keys)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-31-4)pf = vbt.PF.from_signals(data, entries, exits)
 
[/code]


* * *

+


* * *

Multiple incompatible strategies such as those that require different simulation methods or argument combinations can be simulated independently and then stacked for joint analysis. This will combine their data, order records, initial states, in-output arrays, and more, as if they were stacked prior to the simulation with grouping disabled.

Simulate multiple strategies separately but analyze them jointly
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-1)strategy_keys = pd.Index(["strategy1", "strategy2"], name="strategy")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-2)pf1 = vbt.PF.from_signals(data, entries, exits)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-3)pf2 = vbt.PF.from_orders(data, size, price)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-4)pf = vbt.PF.column_stack((pf1, pf2), wrapper_kwargs=dict(keys=strategy_keys))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-6)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-8)pf = vbt.PF.column_stack(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-9) (pf1, pf2), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-10) wrapper_kwargs=dict(keys=strategy_keys), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-11) group_by=strategy_keys.name 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-32-12))
 
[/code]

 1. 


# Parallelizing[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#parallelizing "Permanent link")

If you want to simulate multiple columns (without cash sharing) or multiple groups (with or without cash sharing), you can easily parallelize execution in multiple ways.

How to parallelize simulation
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-33-1)pf = vbt.PF.from_signals(..., chunked="threadpool") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-33-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-33-3)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-33-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-33-5)pf = vbt.PF.from_signals(..., jitted=dict(parallel=True)) 
 
[/code]

 1. 2. 

You can also parallelize statistics once your portfolio is simulated.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-1)@vbt.chunked(engine="threadpool")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-2)def chunked_stats(pf: vbt.ChunkedArray(axis=1)) -> "row_stack":
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-3) return pf.stats(agg_func=None)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-5)chunked_stats(pf) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-7)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-9)pf.chunk_apply( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-10) "stats", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-11) agg_func=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-12) execute_kwargs=dict(engine="threadpool", merge_func="row_stack")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-13))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-15)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-16)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/portfolio/#__codelineno-34-17)pf.stats(agg_func=None, settings=dict(jitted=dict(parallel=True))) 
 
[/code]

 1. 2. 3.