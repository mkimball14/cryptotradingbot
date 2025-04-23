# Streaming[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#streaming "Permanent link")

If you look closely at the implementation of `faster_supertrend`, you will notice that it repeatedly iterates over the full length of the input data: multiple times in `get_med_price`, multiple times in `get_atr`, multiple times in `get_basic_bands`, and once in `get_final_bands_nb`. This modular computational approach can be tolerated if we have the complete data and all we care about is the final result. But what if we had to process a data stream where arrival of each new element would have to trigger the entire indicator pipeline just to append one SuperTrend value? Suddenly, our performance would suffer dramatically.

VectorBT® PRO tackles this problem by deploying a range of so-called accumulators - Numba-compiled functions that can run per time step and produce a single indicator value. An accumulator takes an input state that contains all the required information collected up to this point in time, and returns an output state that contains the current indicator value and all the variables required by the next time step. To lower memory consumption to the minimum, an input state usually contains no arrays - only constants. Since both input and output states are regular [named tuples](https://realpython.com/python-namedtuple/), we can save them at any time and continue from where we left off.

Let's take a look at the accumulator for the rolling mean: [rolling_mean_acc_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.rolling_mean_acc_nb). It takes an input state of type [RollMeanAIS](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.RollMeanAIS) and returns an output state of type [RollMeanAOS](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.RollMeanAOS). The main pieces of information required by this accumulator are the length of the window and the sum of the elements contained in it (recall how the sum of the values divided by the number of values is the definition of the arithmetic mean).

The function [rolling_mean_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.rolling_mean_1d_nb) then implements a simple for-loop that goes through all elements, and for each one:

 1. Creates the input state and passes it to the accumulator
 2. Receives the output state and updates local variables and the output array

(Reload the page if the diagram doesn't show up)

So, how about our SuperTrend function, can we make it also a [one-pass function](https://en.wikipedia.org/wiki/One-pass_algorithm)? Yes! Most operations including the calculation of the median price, the TR, the basic bands, and the final bands are fairly easy to replicate on the per-element basis:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-1)>>> @njit(nogil=True) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-2)... def get_tr_one_nb(high, low, prev_close):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-3)... tr0 = abs(high - low)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-4)... tr1 = abs(high - prev_close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-5)... tr2 = abs(low - prev_close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-6)... if np.isnan(tr0) or np.isnan(tr1) or np.isnan(tr2):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-7)... tr = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-8)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-9)... tr = max(tr0, tr1, tr2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-10)... return tr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-12)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-13)... def get_med_price_one_nb(high, low):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-14)... return (high + low) / 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-16)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-17)... def get_basic_bands_one_nb(high, low, atr, multiplier):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-18)... med_price = get_med_price_one_nb(high, low)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-19)... matr = multiplier * atr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-20)... upper = med_price + matr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-21)... lower = med_price - matr
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-22)... return upper, lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-23)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-24)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-25)... def get_final_bands_one_nb(close, upper, lower, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-26)... prev_upper, prev_lower, prev_dir_):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-27)... if close > prev_upper:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-28)... dir_ = 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-29)... elif close < prev_lower:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-30)... dir_ = -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-31)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-32)... dir_ = prev_dir_
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-33)... if dir_ > 0 and lower < prev_lower:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-34)... lower = prev_lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-35)... if dir_ < 0 and upper > prev_upper:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-36)... upper = prev_upper
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-37)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-38)... if dir_ > 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-39)... trend = long = lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-40)... short = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-41)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-42)... trend = short = upper
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-43)... long = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-0-44)... return upper, lower, trend, dir_, long, short
 
[/code]

 1. 

But the calculation of the ATR is a bit more tricky since it depends on the Wilder's EMA applied to the TR. Gladly, vectorbt implements an accumulator for it! ![🤩](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f929.svg)

But let's define the input and output state for our future accumulator first:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-1)>>> class SuperTrendAIS(tp.NamedTuple):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-2)... i: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-3)... high: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-4)... low: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-5)... close: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-6)... prev_close: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-7)... prev_upper: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-8)... prev_lower: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-9)... prev_dir_: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-10)... nobs: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-11)... weighted_avg: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-12)... old_wt: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-13)... period: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-14)... multiplier: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-16)>>> class SuperTrendAOS(tp.NamedTuple):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-17)... nobs: int
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-18)... weighted_avg: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-19)... old_wt: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-20)... upper: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-21)... lower: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-22)... trend: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-23)... dir_: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-24)... long: float
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-1-25)... short: float
 
[/code]

As you can see, the fields in both states are all constants. The fields from `i` to `prev_dir_` and `multiplier` in the input state will be used by our own accumulator, while the fields `nobs`, `weighted_avg`, `old_wt`, and `period` are required by the accumulator for EMA - [ewm_mean_acc_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.ewm_mean_acc_nb). The output state contains input fields that are updated by the accumulator, but also fields that might be interesting to the user.

We can now put all puzzles together by implementing a SuperTrend accumulator:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-2)... def superfast_supertrend_acc_nb(in_state):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-3)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-4)... i = in_state.i
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-5)... high = in_state.high
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-6)... low = in_state.low
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-7)... close = in_state.close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-8)... prev_close = in_state.prev_close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-9)... prev_upper = in_state.prev_upper
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-10)... prev_lower = in_state.prev_lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-11)... prev_dir_ = in_state.prev_dir_
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-12)... nobs = in_state.nobs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-13)... weighted_avg = in_state.weighted_avg
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-14)... old_wt = in_state.old_wt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-15)... period = in_state.period
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-16)... multiplier = in_state.multiplier
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-17)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-18)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-19)... tr = get_tr_one_nb(high, low, prev_close)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-20)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-21)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-22)... alpha = vbt.nb.alpha_from_wilder_nb(period) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-23)... ewm_mean_in_state = vbt.nb.EWMMeanAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-24)... i=i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-25)... value=tr,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-26)... old_wt=old_wt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-27)... weighted_avg=weighted_avg,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-28)... nobs=nobs,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-29)... alpha=alpha,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-30)... minp=period,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-31)... adjust=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-32)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-33)... ewm_mean_out_state = vbt.nb.ewm_mean_acc_nb(ewm_mean_in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-34)... atr = ewm_mean_out_state.value
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-35)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-36)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-37)... upper, lower = get_basic_bands_one_nb(high, low, atr, multiplier)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-38)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-39)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-40)... if i == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-41)... trend, dir_, long, short = np.nan, 1, np.nan, np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-42)... else:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-43)... upper, lower, trend, dir_, long, short = get_final_bands_one_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-44)... close, upper, lower, prev_upper, prev_lower, prev_dir_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-45)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-46)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-47)... return SuperTrendAOS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-48)... nobs=ewm_mean_out_state.nobs,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-49)... weighted_avg=ewm_mean_out_state.weighted_avg,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-50)... old_wt=ewm_mean_out_state.old_wt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-51)... upper=upper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-52)... lower=lower,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-53)... trend=trend,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-54)... dir_=dir_,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-55)... long=long,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-56)... short=short
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-2-57)... )
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

That's it, we can now use this accumulator in any streaming function!

Let's write a function similar to `faster_supertrend` but that computes the SuperTrend values by passing across the whole data **only once** :
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-1)>>> @njit(nogil=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-2)... def superfast_supertrend_nb(high, low, close, period=7, multiplier=3):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-3)... trend = np.empty(close.shape, dtype=float_) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-4)... dir_ = np.empty(close.shape, dtype=int_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-5)... long = np.empty(close.shape, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-6)... short = np.empty(close.shape, dtype=float_)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-7)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-8)... if close.shape[0] == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-9)... return trend, dir_, long, short
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-10)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-11)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-12)... nobs = 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-13)... old_wt = 1.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-14)... weighted_avg = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-15)... prev_upper = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-16)... prev_lower = np.nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-17)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-18)... for i in range(close.shape[0]): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-19)... in_state = SuperTrendAIS(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-20)... i=i,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-21)... high=high[i],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-22)... low=low[i],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-23)... close=close[i],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-24)... prev_close=close[i - 1] if i > 0 else np.nan,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-25)... prev_upper=prev_upper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-26)... prev_lower=prev_lower,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-27)... prev_dir_=dir_[i - 1] if i > 0 else 1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-28)... nobs=nobs,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-29)... weighted_avg=weighted_avg,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-30)... old_wt=old_wt,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-31)... period=period,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-32)... multiplier=multiplier
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-33)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-34)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-35)... out_state = superfast_supertrend_acc_nb(in_state)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-36)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-37)... nobs = out_state.nobs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-38)... weighted_avg = out_state.weighted_avg
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-39)... old_wt = out_state.old_wt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-40)... prev_upper = out_state.upper
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-41)... prev_lower = out_state.lower
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-42)... trend[i] = out_state.trend
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-43)... dir_[i] = out_state.dir_
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-44)... long[i] = out_state.long
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-45)... short[i] = out_state.short
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-46)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-3-47)... return trend, dir_, long, short
 
[/code]

 1. 2. 3. 

After writing a streaming algorithm, you should always compare its results to a (semi-)vectorized solution that you trust:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-1)>>> superfast_out = superfast_supertrend_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-2)... high['BTCUSDT'].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-3)... low['BTCUSDT'].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-4)... close['BTCUSDT'].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-7)>>> faster_out = faster_supertrend(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-8)... high['BTCUSDT'].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-9)... low['BTCUSDT'].values,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-10)... close['BTCUSDT'].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-13)>>> np.testing.assert_allclose(superfast_out[0], faster_out[0])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-14)>>> np.testing.assert_allclose(superfast_out[1], faster_out[1])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-15)>>> np.testing.assert_allclose(superfast_out[2], faster_out[2])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-4-16)>>> np.testing.assert_allclose(superfast_out[3], faster_out[3])
 
[/code]

There is nothing more satisfying than having no errors ![😉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f609.svg)

Note

If you compare the results to `faster_supertrend_talib`, they would differ because TA-Lib uses a slightly different EMA in its ATR implementation.

What about speed? Well, you can see it for yourself:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-5-1)>>> %%timeit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-5-2)>>> superfast_supertrend_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-5-3)... high['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-5-4)... low['BTCUSDT'].values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-5-5)... close['BTCUSDT'].values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-5-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend/streaming/#__codelineno-5-7)183 µs ± 1.22 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
 
[/code]

Our algorithm is 40% faster than `faster_supertrend_talib` and can effortlessly compete with similar implementations in C or any other compiled language. Neat! 

Hint

To avoid re-compilation each time you start a new Python session, add the `cache=True` flag to the `@njit` decorator. But make sure that you define the cachable function in a Python file rather than in a cell of Jupyter Notebook.

We just hit the performance ceiling - let's move on with parameter optimization.

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/superfast-supertrend/streaming.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/SuperTrend.ipynb)