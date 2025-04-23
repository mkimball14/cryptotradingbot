# Alignment[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#alignment "Permanent link")

Comparing time series with different time frames is tricky to say the least. Consider an example where we want to calculate the ratio between the close price in `H1` and `H4`.


# Pandas[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#pandas "Permanent link")

Comparing both time series using Pandas yields the following results:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-1)>>> h1_close = h1_data.get("Close")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-2)>>> h4_close = h4_data.get("Close")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-4)>>> h1_close.iloc[:4]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-5)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-6)2020-01-01 00:00:00+00:00 7177.02
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-7)2020-01-01 01:00:00+00:00 7216.27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-8)2020-01-01 02:00:00+00:00 7242.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-9)2020-01-01 03:00:00+00:00 7225.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-10)Name: Close, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-12)>>> h4_close.iloc[:1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-13)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-14)2020-01-01 00:00:00+00:00 7225.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-15)Freq: 4H, Name: Close, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-17)>>> h1_h4_ratio = h1_close / h4_close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-18)>>> h1_h4_ratio.iloc[:4]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-19)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-20)2020-01-01 00:00:00+00:00 0.993358
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-21)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-22)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-23)2020-01-01 03:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-0-24)Name: Close, dtype: float64
 
[/code]

If you think the result is right, you're wrong ![🙃](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f643.svg)

Here, only the timestamp `2020-01-01 00:00:00` in both time series is getting compared, while other timestamps become NaN. This is understandable since Pandas compares values by their index labels. So far so good. The actual problem lies in the fact that each timestamp is the **open time** and holds information all the way up to the next timestamp. In reality, the close price stored at `2020-01-01 00:00:00` happens right before `2020-01-01 01:00:00` in `h1_close` and right before `2020-01-01 04:00:00` in `h4_close`. This means that we are comparing information from the past with information from the future, effectively exposing ourselves to the look-ahead bias!

As we can take from the diagram above, we are only allowed to compare `close_3` between both time frames. Comparing `close_0` and `close_3` won't cause any errors (!), but you will get burned hard in production without having any idea why the backtesting results are so much off.

If we want a more fair comparison of the close price, we should compare each timestamp in `h1_close` with the **previous** timestamp in `h4_close`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-1)>>> h4_close_shifted = h4_close.shift()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-2)>>> h1_h4_ratio = h1_close / h4_close_shifted
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-3)>>> h1_h4_ratio.iloc[:8]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-4)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-5)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-6)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-7)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-8)2020-01-01 03:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-9)2020-01-01 04:00:00+00:00 0.998929
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-10)2020-01-01 05:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-11)2020-01-01 06:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-12)2020-01-01 07:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-1-13)Name: Close, dtype: float64
 
[/code]

This comparison makes more sense, since any timestamp before `2020-01-01 04:00:00` doesn't know about the close price at the end of `2020-01-01 03:00:00` yet. But even this comparison can be further improved because the close price at `2020-01-01 03:00:00` in `h1_close` is the same close price as at `2020-01-01 00:00:00` in `h4_close`. Thus, we can safely shift the resulting series backward:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-1)>>> h1_h4_ratio.shift(-1).iloc[:8]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-3)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-4)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-5)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-6)2020-01-01 03:00:00+00:00 0.998929
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-7)2020-01-01 04:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-8)2020-01-01 05:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-9)2020-01-01 06:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-10)2020-01-01 07:00:00+00:00 0.998725
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-2-11)Name: Close, dtype: float64
 
[/code]

What about all those NaNs, why aren't they compared as well? For this, we need to upsample the `h4_close` to `H1` and forward-fill NaN values:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-1)>>> h4_h1_close = h4_close.shift(1).resample("1h").last().shift(-1).ffill()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-2)>>> h4_h1_close.iloc[:8]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-3)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-4)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-5)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-6)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-7)2020-01-01 03:00:00+00:00 7225.01 << first close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-8)2020-01-01 04:00:00+00:00 7225.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-9)2020-01-01 05:00:00+00:00 7225.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-10)2020-01-01 06:00:00+00:00 7225.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-11)2020-01-01 07:00:00+00:00 7209.83 << second close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-3-12)Freq: H, Name: Close, dtype: float64
 
[/code]

Note

Don't forward and backward shift when downsampling, only when upsampling.

Let's plot the first 16 points of both time series for validation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-4-1)>>> fig = h1_close.rename("H1").iloc[:16].vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-4-2)>>> h4_h1_close.rename("H4_H1").iloc[:16].vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-4-3)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/h4_h1.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/h4_h1.dark.svg#only-dark)

As we see, at each hour, `H4_H1` contains the latest available information from the previous 4 hours. We can now compare both time frames safely:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-1)>>> h1_h4_ratio = h1_close / h4_h1_close
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-2)>>> h1_h4_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-3)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-4)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-5)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-6)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-7)2020-01-01 03:00:00+00:00 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-8)2020-01-01 04:00:00+00:00 0.998929
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-9)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-10)2020-12-31 19:00:00+00:00 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-11)2020-12-31 20:00:00+00:00 1.007920
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-12)2020-12-31 21:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-13)2020-12-31 22:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-14)2020-12-31 23:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-5-15)Name: Close, Length: 8784, dtype: float64
 
[/code]

The same goes for high and low price since their information is also available only at the end of each bar. Open price, on the other hand, is already available at the beginning of each bar, so we don't need to shift `H4` forward and backward:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-1)>>> h1_open = h1_data.get("Open")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-2)>>> h4_open = h4_data.get("Open")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-4)>>> h1_open.iloc[:8]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-5)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-6)2020-01-01 00:00:00+00:00 7195.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-7)2020-01-01 01:00:00+00:00 7176.47
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-8)2020-01-01 02:00:00+00:00 7215.52
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-9)2020-01-01 03:00:00+00:00 7242.66
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-10)2020-01-01 04:00:00+00:00 7225.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-11)2020-01-01 05:00:00+00:00 7217.26
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-12)2020-01-01 06:00:00+00:00 7224.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-13)2020-01-01 07:00:00+00:00 7225.88
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-14)Name: Open, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-16)>>> h4_h1_open = h4_open.resample("1h").first().ffill()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-17)>>> h4_h1_open.iloc[:8]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-18)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-19)2020-01-01 00:00:00+00:00 7195.24 << first open
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-20)2020-01-01 01:00:00+00:00 7195.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-21)2020-01-01 02:00:00+00:00 7195.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-22)2020-01-01 03:00:00+00:00 7195.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-23)2020-01-01 04:00:00+00:00 7225.00 << second open
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-24)2020-01-01 05:00:00+00:00 7225.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-25)2020-01-01 06:00:00+00:00 7225.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-26)2020-01-01 07:00:00+00:00 7225.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-6-27)Freq: H, Name: Open, dtype: float64
 
[/code]


# VBT[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#vbt "Permanent link")

Seems like a lot of work is required to do everything right? But don't worry, vectorbt has got your back! To realign an array safely, we can use [GenericAccessor.realign_opening](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_opening) for information available already at the beginning of each bar, and [GenericAccessor.realign_closing](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_closing) for information available only at the end of each bar:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-1)>>> h4_close.vbt.realign_closing("1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-3)2020-01-01 00:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-4)2020-01-01 01:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-5)2020-01-01 02:00:00+00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-6)2020-01-01 03:00:00+00:00 7225.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-7)2020-01-01 04:00:00+00:00 7225.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-8)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-9)2020-12-31 16:00:00+00:00 28770.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-10)2020-12-31 17:00:00+00:00 28770.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-11)2020-12-31 18:00:00+00:00 28770.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-12)2020-12-31 19:00:00+00:00 28897.83
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-13)2020-12-31 20:00:00+00:00 28897.83
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-14)Freq: H, Name: Close, Length: 8781, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-16)>>> h4_open.vbt.realign_opening("1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-17)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-18)2020-01-01 00:00:00+00:00 7195.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-19)2020-01-01 01:00:00+00:00 7195.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-20)2020-01-01 02:00:00+00:00 7195.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-21)2020-01-01 03:00:00+00:00 7195.24
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-22)2020-01-01 04:00:00+00:00 7225.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-23)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-24)2020-12-31 16:00:00+00:00 28782.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-25)2020-12-31 17:00:00+00:00 28782.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-26)2020-12-31 18:00:00+00:00 28782.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-27)2020-12-31 19:00:00+00:00 28782.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-28)2020-12-31 20:00:00+00:00 28897.84
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-7-29)Freq: H, Name: Open, Length: 8781, dtype: float64
 
[/code]

Important

Use `realign_opening` only if information in the array happens exactly at the beginning of the bar (such as open price), and `realign_closing` if information happens after that (such as high, low, and close price).

That's it - the results above can now be safely combined with any `H1` data ![🥳](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f973.svg)


# Resampler[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#resampler "Permanent link")

If you want to gain a deeper understanding of the inner workings of those two functions, let's first discuss what does "resampler" mean in vectorbt. Resampler is an instance of the [Resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler) class, which simply stores a source index and frequency, and a target index and frequency:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-1)>>> h4_h1_resampler = h4_close.vbt.wrapper.get_resampler("1h") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-2)>>> h4_h1_resampler.source_index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-3)DatetimeIndex(['2020-01-01 00:00:00+00:00', '2020-01-01 04:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-4) '2020-01-01 08:00:00+00:00', '2020-01-01 12:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-5) '2020-01-01 16:00:00+00:00', '2020-01-01 20:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-6) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-7) '2020-12-31 00:00:00+00:00', '2020-12-31 04:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-8) '2020-12-31 08:00:00+00:00', '2020-12-31 12:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-9) '2020-12-31 16:00:00+00:00', '2020-12-31 20:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-10) dtype='datetime64[ns, UTC]', name='Open time', length=2196, freq='4H')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-12)>>> h4_h1_resampler.target_index
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-13)DatetimeIndex(['2020-01-01 00:00:00+00:00', '2020-01-01 01:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-14) '2020-01-01 02:00:00+00:00', '2020-01-01 03:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-15) '2020-01-01 04:00:00+00:00', '2020-01-01 05:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-16) ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-17) '2020-12-31 15:00:00+00:00', '2020-12-31 16:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-18) '2020-12-31 17:00:00+00:00', '2020-12-31 18:00:00+00:00',
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-19) '2020-12-31 19:00:00+00:00', '2020-12-31 20:00:00+00:00'],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-20) dtype='datetime64[ns, UTC]', name='Open time', length=8781, freq='H')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-21)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-22)>>> h4_h1_resampler.source_freq
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-23)Timedelta('0 days 04:00:00')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-24)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-25)>>> h4_h1_resampler.target_freq
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-8-26)Timedelta('0 days 01:00:00')
 
[/code]

 1. 

Having just those two pieces of information is enough to perform most resampling tasks, all we have to do is to iterate over both indexes and track which element in one index belongs to which element in the other one, which is done efficiently using Numba. This also means that, in contrast to Pandas, vectorbt accepts an arbitrary target index for resampling. In fact, [Resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler) has a bunch of convenient class methods to construct an instance out of various Pandas objects and functions. For example, to create a resampler out of a [Pandas Resampler](https://pandas.pydata.org/docs/reference/resampling.html):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-9-1)>>> pd_resampler = h4_close.resample("1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-9-2)>>> vbt.Resampler.from_pd_resampler(pd_resampler, source_freq="4h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-9-3)<vectorbtpro.base.resampling.base.Resampler at 0x7ff518c3f358>
 
[/code]

Or, we can use [Resampler.from_date_range](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.from_date_range) to build our custom hourly index starting from 10 AM and ending at 10 PM:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-10-1)>>> resampler = vbt.Resampler.from_date_range(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-10-2)... source_index=h4_close.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-10-3)... source_freq="4h",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-10-4)... start="2020-01-01 10:00:00",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-10-5)... end="2020-01-01 22:00:00",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-10-6)... freq="1h",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-10-7)... )
 
[/code]

We can then pass the resampler directly to [GenericAccessor.realign_closing](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_closing) to fill the latest information from the `H4` time frame:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-1)>>> h4_close.vbt.realign_closing(resampler)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-2)2020-01-01 10:00:00 7209.83
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-3)2020-01-01 11:00:00 7197.20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-4)2020-01-01 12:00:00 7197.20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-5)2020-01-01 13:00:00 7197.20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-6)2020-01-01 14:00:00 7197.20
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-7)2020-01-01 15:00:00 7234.19
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-8)2020-01-01 16:00:00 7234.19
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-9)2020-01-01 17:00:00 7234.19
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-10)2020-01-01 18:00:00 7234.19
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-11)2020-01-01 19:00:00 7229.48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-12)2020-01-01 20:00:00 7229.48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-13)2020-01-01 21:00:00 7229.48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-14)2020-01-01 22:00:00 7229.48
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-11-15)Freq: H, Name: Close, dtype: float64
 
[/code]


# Custom index[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#custom-index "Permanent link")

We can also specify our target index directly. For instance, let's get the latest information on `H4` at the beginning of each month (= downsampling). Note that without providing the target frequency explicitly, vectorbt will infer it from the target index, which is `MonthBegin` of type [DateOffset](https://pandas.pydata.org/docs/reference/api/pandas.tseries.offsets.DateOffset.html) in our case. Date offsets like this cannot be converted into a timedelta required by the underlying Numba function - Numba accepts only numeric and `np.timedelta64` for frequency (see [this](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#overview) overview). To prevent inferring the frequency, we can set it to False. In this case, vectorbt will calculate the right bound for each index value using the next index value, as opposed to a fixed frequency.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-1)>>> target_index = pd.Index([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-2)... "2020-01-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-3)... "2020-02-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-4)... "2020-03-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-5)... "2020-04-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-6)... "2020-05-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-7)... "2020-06-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-8)... "2020-07-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-9)... "2020-08-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-10)... "2020-09-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-11)... "2020-10-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-12)... "2020-11-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-13)... "2020-12-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-14)... "2021-01-01"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-15)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-16)>>> resampler = vbt.Resampler(h4_close.index, target_index, target_freq=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-17)>>> h4_close.vbt.realign_closing(resampler)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-18)2020-01-01 9352.89
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-19)2020-02-01 8523.61
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-20)2020-03-01 6410.44
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-21)2020-04-01 8620.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-22)2020-05-01 9448.27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-23)2020-06-01 9138.55
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-24)2020-07-01 11335.46
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-25)2020-08-01 11649.51
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-26)2020-09-01 10776.59
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-27)2020-10-01 13791.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-28)2020-11-01 19695.87
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-29)2020-12-01 28923.63
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-30)2021-01-01 28923.63
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-12-31)Name: Close, dtype: float64
 
[/code]

To make sure that the output is correct, let's validate the close value for `2020-08-01`, which must be the latest value for that month:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-13-1)>>> h4_close[h4_close.index < "2020-09-01"].iloc[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-13-2)11649.51
 
[/code]

Hint

Disabling the frequency is only required for offsets that cannot be translated to timedelta. Other offsets, such as for daily data, are converted automatically and without issues.

One major drawback of disabling or not being able to infer the frequency of a target index is that the bounds of each index value are not fixed anymore, but variable. Consider the following scenario where we want to downsample `H4` to two dates, `2020-01-01` and `2020-02-01`, knowing that they are months. If we do not specify the target frequency, vectorbt uses the latest close price after each of those dates:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-1)>>> target_index = pd.Index([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-2)... "2020-01-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-3)... "2020-02-01",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-4)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-5)>>> resampler = vbt.Resampler(h4_close.index, target_index, target_freq=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-6)>>> h4_close.vbt.realign_closing(resampler)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-7)2020-01-01 9352.89
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-8)2020-02-01 28923.63
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-14-9)Name: Close, dtype: float64
 
[/code]

The value for `2020-02-01` is the latest value in `H4`, which is clearly not intended. To limit the bounds of all index values, set the target frequency:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-15-1)>>> resampler = vbt.Resampler(h4_close.index, target_index, target_freq="30d")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-15-2)>>> h4_close.vbt.realign_closing(resampler)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-15-3)2020-01-01 9513.21
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-15-4)2020-02-01 8531.88
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-15-5)Name: Close, dtype: float64
 
[/code]

Much better, but even this is wrong because a month may also be more or less than 30 days long. Since we cannot use date offsets, we need to specify the bounds for each index value. This is possible by using [GenericAccessor.realign](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign), which is the base method for both `realign_closing` and `realign_opening` we used above. This method is a true powerhouse that allows specifying every bit of information manually. The main idea is simple: return the latest available information from an array at each position in a target index.

For example, let's get the latest information on `H4` on some specific time:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-16-1)>>> h4_open.vbt.realign("2020-06-07 12:15:00") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-16-2)9576.57
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-16-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-16-4)>>> h4_close.vbt.realign(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-16-5)... "2020-06-07 12:15:00", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-16-6)... source_rbound=True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-16-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-16-8)9575.59
 
[/code]

 1. 2. 

Note that the target datetime we provided is an exact point in time when information should become available. Let's get the latest highest value at the beginning of two months in `target_index`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-17-1)>>> h4_high = h4_data.get("High")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-17-2)>>> h4_high.vbt.realign(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-17-3)... target_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-17-4)... source_rbound=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-17-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-17-6)2020-01-01 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-17-7)2020-02-01 9430.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-17-8)Name: High, dtype: float64
 
[/code]

Here, `2020-01-01` means exactly `2020-01-01 00:00:00` when there is no information yet, hence NaN. On `2020-02-01` though, we can use the information from `2020-01-31 20:00:00`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-18-1)>>> h4_high.index[h4_high.index < "2020-02-01"][-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-18-2)Timestamp('2020-01-31 20:00:00+0000', tz='UTC', freq='4H')
 
[/code]

To make the target index behave like bars instead of exact points in time, we can turn on the right bound for it too:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-1)>>> h4_high.vbt.realign(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-2)... target_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-3)... source_rbound=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-4)... target_rbound=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-6)UserWarning: Using right bound of target index without frequency. Set target_freq.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-7)2020-01-01 9430.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-8)2020-02-01 29169.55
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-19-9)Name: High, dtype: float64
 
[/code]

We received a warning stating that vectorbt couldn't infer the frequency of `target_index`. But to not make the same mistake we did with a frequency of `30d` (a month has a variable length after all), let's specify the right bound manually instead of enabling `target_rbound`. Thankfully, vectorbt has a nice method for doing that:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-1)>>> resampler = vbt.Resampler(h4_high.index, target_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-2)>>> resampler.target_rbound_index 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-3)DatetimeIndex([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-4) '2020-01-31 23:59:59.999999999', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-5) '2262-04-11 23:47:16.854775807'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-6)], dtype='datetime64[ns]', freq=None)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-8)>>> resampler = vbt.Resampler(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-9)... h4_high.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-10)... target_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-11)... target_freq=pd.offsets.MonthBegin(1))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-12)>>> resampler.target_rbound_index 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-13)DatetimeIndex([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-14) '2020-01-31 23:59:59.999999999', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-15) '2020-02-29 23:59:59.999999999'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-20-16)], dtype='datetime64[ns]', freq=None)
 
[/code]

 1. 2. 

We can now use this right bound as the target index:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-1)>>> h4_high.vbt.realign(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-2)... resampler.replace(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-3)... target_index=resampler.target_rbound_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-4)... target_freq=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-5)... ), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-6)... wrap_kwargs=dict(index=target_index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-8)2020-01-01 9430.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-9)2020-02-01 8671.61
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-21-10)Name: High, dtype: float64
 
[/code]

 1. 2. 

Or conveniently using `target_rbound="pandas"` in [GenericAccessor.realign](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-22-1)>>> h4_high.vbt.realign(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-22-2)... target_index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-22-3)... freq=pd.offsets.MonthBegin(1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-22-4)... target_rbound="pandas"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-22-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-22-6)2020-01-01 9430.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-22-7)2020-02-01 8671.61
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-22-8)Name: High, dtype: float64
 
[/code]

Let's validate the output using Pandas:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-23-1)>>> h4_high[h4_high.index < "2020-03-01"].resample(vbt.offset("M")).last() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-23-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-23-3)2020-01-01 00:00:00+00:00 9430.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-23-4)2020-02-01 00:00:00+00:00 8671.61
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-23-5)Freq: MS, Name: High, dtype: float64
 
[/code]

A clear advantage of vectorbt over Pandas in this regard is:

 1. 2. High efficiency, since vectorbt iterates over data only once, at the speed of C

Info

Why did we use `vbt.offset("M")` instead of just `"M"`? Pandas methods may have a different interpretation of offsets than VBT methods. For instance, Pandas interprets "M" as the month end while VBT interprets it as the month start (since we're working with bars most of the time). As a rule of thumb: explicitly translate any string offset if it must be passed to a Pandas method. If the method belongs to VBT, there's usually no need to perform this step.


# Numeric index[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#numeric-index "Permanent link")

And we haven't even mentioned the ability to do resampling on numeric indexes. Below, we are getting the latest information at each 6th element from the `H4` time frame, which is just another way of downsampling to the daily frequency (as long as there are no gaps):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-1)>>> resampler = vbt.Resampler(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-2)... source_index=np.arange(len(h4_high)),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-3)... target_index=np.arange(len(h4_high))[::6],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-4)... source_freq=1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-5)... target_freq=6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-7)>>> h4_high.vbt.realign(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-8)... resampler, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-9)... source_rbound=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-10)... target_rbound=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-12)0 7242.98
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-13)6 6985.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-14)12 7361.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-15)... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-16)2178 27410.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-17)2184 28996.00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-18)2190 29169.55
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-24-19)Name: High, Length: 366, dtype: float64
 
[/code]

Good luck doing the same with Pandas.


# Forward filling[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#forward-filling "Permanent link")

By default, when upsampling or downsampling, vectorbt will forward fill missing values by propagating the latest known value. This is usually desired when the final task is to compare the resampled time series to another time series of the same timeframe. But this may not hold well for some more sensitive time series types, such as signals: repeating the same signal over and over again may give a distorted view of the original timeframe, especially when upsampling. To place each value only once, we can use the argument `ffill`. For example, let's upsample a 5min mask with 3 entries to a 1min mask with 15 entries, without and with forward filling. We'll assume that the 5min mask itself was generated using the close price:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-1)>>> min5_index = vbt.date_range(start="2020", freq="5min", periods=3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-2)>>> min1_index = vbt.date_range(start="2020", freq="1min", periods=15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-3)>>> min5_mask = pd.Series(False, index=min5_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-4)>>> min5_mask.iloc[0] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-5)>>> min5_mask.iloc[2] = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-7)>>> resampler = vbt.Resampler(min5_index, min1_index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-8)>>> min1_mask = min5_mask.vbt.realign_closing(resampler) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-9)>>> min1_mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-10)2020-01-01 00:00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-11)2020-01-01 00:01:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-12)2020-01-01 00:02:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-13)2020-01-01 00:03:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-14)2020-01-01 00:04:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-15)2020-01-01 00:05:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-16)2020-01-01 00:06:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-17)2020-01-01 00:07:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-18)2020-01-01 00:08:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-19)2020-01-01 00:09:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-20)2020-01-01 00:10:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-21)2020-01-01 00:11:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-22)2020-01-01 00:12:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-23)2020-01-01 00:13:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-24)2020-01-01 00:14:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-25)Freq: T, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-26)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-27)>>> min1_mask = min5_mask.vbt.realign_closing(resampler, ffill=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-28)>>> min1_mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-29)2020-01-01 00:00:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-30)2020-01-01 00:01:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-31)2020-01-01 00:02:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-32)2020-01-01 00:03:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-33)2020-01-01 00:04:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-34)2020-01-01 00:05:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-35)2020-01-01 00:06:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-36)2020-01-01 00:07:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-37)2020-01-01 00:08:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-38)2020-01-01 00:09:00 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-39)2020-01-01 00:10:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-40)2020-01-01 00:11:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-41)2020-01-01 00:12:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-42)2020-01-01 00:13:00 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-43)2020-01-01 00:14:00 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-44)Freq: T, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-45)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-46)>>> min1_mask = min1_mask.fillna(False).astype(bool) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-47)>>> min1_mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-48)2020-01-01 00:00:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-49)2020-01-01 00:01:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-50)2020-01-01 00:02:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-51)2020-01-01 00:03:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-52)2020-01-01 00:04:00 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-53)2020-01-01 00:05:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-54)2020-01-01 00:06:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-55)2020-01-01 00:07:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-56)2020-01-01 00:08:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-57)2020-01-01 00:09:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-58)2020-01-01 00:10:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-59)2020-01-01 00:11:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-60)2020-01-01 00:12:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-61)2020-01-01 00:13:00 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-62)2020-01-01 00:14:00 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-25-63)Freq: T, dtype: bool
 
[/code]

 1. 2. 3. 4. 


# Indicators[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#indicators "Permanent link")

So, how do we use the resampling logic from above in constructing indicators that combine multiple time frames? Quite easily:

 1. Run each indicator on its particular time frame
 2. Resample the arrays to a single index (usually to the highest frequency)
 3. Combine the resampled arrays

Let's demonstrate this by calculating the crossover of two moving averages on the time frames `H4` and `D1`. First, we will run the TA-Lib's SMA indicator on the close price of both time frames:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-1)>>> h4_sma = vbt.talib("SMA").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-2)... h4_data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-3)... skipna=True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-4)... ).real
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-5)>>> d1_sma = vbt.talib("SMA").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-6)... d1_data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-7)... skipna=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-8)... ).real
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-10)>>> h4_sma = h4_sma.ffill() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-26-11)>>> d1_sma = d1_sma.ffill()
 
[/code]

 1. 2. 

Then, upsample `D1` to `H4` such that both indicators have the same index:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-27-1)>>> resampler = vbt.Resampler(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-27-2)... d1_sma.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-27-3)... h4_sma.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-27-4)... source_freq="1d",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-27-5)... target_freq="4h"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-27-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-27-7)>>> d1_h4_sma = d1_sma.vbt.realign_closing(resampler) 
 
[/code]

 1. 2. 3. 

Let's validate the result of resampling:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-1)>>> d1_sma["2020-12-30":]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-3)2020-12-30 00:00:00+00:00 21746.412000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-4)2020-12-31 00:00:00+00:00 22085.034333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-5)Freq: D, Name: Close, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-7)>>> d1_h4_sma["2020-12-30":]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-8)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-9)2020-12-30 00:00:00+00:00 21440.423000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-10)2020-12-30 04:00:00+00:00 21440.423000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-11)2020-12-30 08:00:00+00:00 21440.423000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-12)2020-12-30 12:00:00+00:00 21440.423000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-13)2020-12-30 16:00:00+00:00 21440.423000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-14)2020-12-30 20:00:00+00:00 21746.412000 << first value available
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-15)2020-12-31 00:00:00+00:00 21746.412000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-16)2020-12-31 04:00:00+00:00 21746.412000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-17)2020-12-31 08:00:00+00:00 21746.412000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-18)2020-12-31 12:00:00+00:00 21746.412000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-19)2020-12-31 16:00:00+00:00 21746.412000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-20)2020-12-31 20:00:00+00:00 22085.034333 << second value available
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-28-21)Freq: 4H, Name: Close, dtype: float64
 
[/code]

Finally, as usually, compare the new time series to produce entries and exits:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-1)>>> entries = h4_sma.vbt.crossed_above(d1_h4_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-2)>>> exits = h4_sma.vbt.crossed_below(d1_h4_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-4)>>> def plot_date_range(date_range):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-5)... fig = h4_sma[date_range].rename("H4").vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-6)... d1_h4_sma[date_range].rename("D1_H4").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-7)... entries[date_range].rename("Entry").vbt.signals.plot_as_entries(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-8)... y=h4_sma[date_range], fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-9)... exits[date_range].rename("Exit").vbt.signals.plot_as_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-10)... y=h4_sma[date_range], fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-11)... return fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-29-13)>>> plot_date_range(slice("2020-02-01", "2020-03-01")).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/d1_h4.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/d1_h4.dark.svg#only-dark)

In case any calculation was performed on the open price, we can account for that by directly using [GenericAccessor.realign](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign) and disabling the right bound of the affected index:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-1)>>> d1_open_sma = vbt.talib("SMA").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-2)... d1_data.get("Open"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-3)... skipna=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-4)... ).real
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-5)>>> d1_open_sma = d1_open_sma.ffill()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-7)>>> d1_h4_open_sma = d1_open_sma.vbt.realign(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-8)... resampler, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-9)... source_rbound=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-10)... target_rbound=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-30-11)... )
 
[/code]

 1. 2. 3. 

Let's validate the result of resampling:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-1)>>> d1_open_sma["2020-12-30":]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-2)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-3)2020-12-30 00:00:00+00:00 21440.420333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-4)2020-12-31 00:00:00+00:00 21746.409667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-5)Freq: D, Name: Open, dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-7)>>> d1_h4_open_sma["2020-12-30":]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-8)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-9)2020-12-30 00:00:00+00:00 21440.420333 << first value available
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-10)2020-12-30 04:00:00+00:00 21440.420333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-11)2020-12-30 08:00:00+00:00 21440.420333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-12)2020-12-30 12:00:00+00:00 21440.420333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-13)2020-12-30 16:00:00+00:00 21440.420333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-14)2020-12-30 20:00:00+00:00 21440.420333
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-15)2020-12-31 00:00:00+00:00 21746.409667 << second value available
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-16)2020-12-31 04:00:00+00:00 21746.409667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-17)2020-12-31 08:00:00+00:00 21746.409667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-18)2020-12-31 12:00:00+00:00 21746.409667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-19)2020-12-31 16:00:00+00:00 21746.409667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-20)2020-12-31 20:00:00+00:00 21746.409667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-31-21)Freq: 4H, Name: Open, dtype: float64
 
[/code]

Let's do something more fun: calculate the bandwidth of the Bollinger Bands indicator on a set of arbitrary frequencies and pack everything into a single DataFrame:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-1)>>> def generate_bandwidths(freqs):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-2)... bandwidths = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-3)... for freq in freqs:
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-4)... close = h1_data.resample(freq).get("Close") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-5)... bbands = vbt.talib("BBANDS").run(close, skipna=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-6)... upperband = bbands.upperband.ffill()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-7)... middleband = bbands.middleband.ffill()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-8)... lowerband = bbands.lowerband.ffill()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-9)... bandwidth = (upperband - lowerband) / middleband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-10)... bandwidths.append(bandwidth.vbt.realign_closing("1h")) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-11)... df = pd.concat(bandwidths, axis=1, keys=pd.Index(freqs, name="timeframe")) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-12)... return df.ffill() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-14)>>> bandwidths = generate_bandwidths(["1h", "4h", "1d", "7d"])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-15)>>> bandwidths
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-16)timeframe 1h 4h 1d 7d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-17)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-18)2020-01-01 00:00:00+00:00 NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-19)2020-01-01 01:00:00+00:00 NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-20)2020-01-01 02:00:00+00:00 NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-21)2020-01-01 03:00:00+00:00 NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-22)2020-01-01 04:00:00+00:00 0.011948 NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-23)... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-24)2020-12-31 19:00:00+00:00 0.027320 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-25)2020-12-31 20:00:00+00:00 0.036515 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-26)2020-12-31 21:00:00+00:00 0.025027 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-27)2020-12-31 22:00:00+00:00 0.014318 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-28)2020-12-31 23:00:00+00:00 0.012875 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-29)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-32-30)[8784 rows x 4 columns]
 
[/code]

 1. 2. 3. 4. 

We can then plot the entire thing as a heatmap:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-33-1)>>> bandwidths.loc[:, ::-1].vbt.ts_heatmap().show() 
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/heatmap.dark.svg#only-dark)

We just created such a badass visualization in 10 lines of code! ![🎸](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f3b8.svg)

But we can make the code even shorter: each TA-Lib indicator has a `timeframe` parameter ![😛](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f61b.svg)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-1)>>> bbands = vbt.talib("BBANDS").run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-2)... h1_data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-3)... skipna=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-4)... timeframe=["1h", "4h", "1d", "7d"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-5)... broadcast_kwargs=dict(wrapper_kwargs=dict(freq="1h")) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-7)>>> bandwidth = (bbands.upperband - bbands.lowerband) / bbands.middleband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-8)>>> bandwidths
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-9)timeframe 1h 4h 1d 7d
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-10)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-11)2020-01-01 00:00:00+00:00 NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-12)2020-01-01 01:00:00+00:00 NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-13)2020-01-01 02:00:00+00:00 NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-14)2020-01-01 03:00:00+00:00 NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-15)2020-01-01 04:00:00+00:00 0.011948 NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-16)... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-17)2020-12-31 19:00:00+00:00 0.027320 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-18)2020-12-31 20:00:00+00:00 0.036515 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-19)2020-12-31 21:00:00+00:00 0.025027 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-20)2020-12-31 22:00:00+00:00 0.014318 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-21)2020-12-31 23:00:00+00:00 0.012875 0.017939 0.134607 0.652958
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-22)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-34-23)[8784 rows x 4 columns]
 
[/code]

 1. 


# Testing[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#testing "Permanent link")

As with everything in vectorbt, time frames are just another dimension that can be tested by iteration (loop over frequencies and simulate each one independently) or by stacking columns. If you don't want to inflate the data by storing multiple time frames in a single array, use the first approach. If you want to make decisions based on multiple time frames, or you want to test them from the same angle and using the same conditions (which is a prerequisite for a fair experiment), and you don't have much data to actually hit memory hard, use the second approach.

Let's demonstrate the second approach. Below, for each frequency, we are computing the SMA crossover on the open price of `H1`. We then align and concatenate all time frames, and simulate them as a single entity using the close price of `H1`and some stop loss. This way, we can test multiple time frames by keeping order execution as granular as possible.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-1)>>> def generate_signals(data, freq, fast_window, slow_window):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-2)... open_price = data.resample(freq).get("Open") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-3)... fast_sma = vbt.talib("SMA")\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-4)... .run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-5)... open_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-6)... fast_window, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-7)... skipna=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-8)... short_name="fast_sma"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-9)... )\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-10)... .real.ffill()\ 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-11)... .vbt.realign(data.wrapper.index) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-12)... slow_sma = vbt.talib("SMA")\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-13)... .run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-14)... open_price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-15)... slow_window, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-16)... skipna=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-17)... short_name="slow_sma"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-18)... )\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-19)... .real.ffill()\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-20)... .vbt.realign(data.wrapper.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-21)... entries = fast_sma.vbt.crossed_above(slow_sma) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-22)... exits = fast_sma.vbt.crossed_below(slow_sma)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-23)... return entries, exits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-24)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-25)>>> fast_window = [10, 20] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-26)>>> slow_window = [20, 30]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-27)>>> h1_entries, h1_exits = generate_signals(h1_data, "1h", fast_window, slow_window)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-28)>>> h4_entries, h4_exits = generate_signals(h1_data, "4h", fast_window, slow_window)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-29)>>> d1_entries, d1_exits = generate_signals(h1_data, "1d", fast_window, slow_window)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-30)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-31)>>> entries = pd.concat( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-32)... (h1_entries, h4_entries, d1_entries), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-33)... axis=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-34)... keys=pd.Index(["1h", "4h", "1d"], name="timeframe")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-35)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-36)>>> exits = pd.concat(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-37)... (h1_exits, h4_exits, d1_exits), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-38)... axis=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-39)... keys=pd.Index(["1h", "4h", "1d"], name="timeframe")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-40)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-41)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-42)>>> (entries.astype(int) - exits.astype(int))\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-43)... .resample("1d").sum()\
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-44)... .vbt.ts_heatmap(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-45)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-46)... colorscale=["#ef553b", "rgba(0, 0, 0, 0)", "#17becf"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-47)... colorbar=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-48)... tickvals=[-1, 0, 1], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-49)... ticktext=["Exit", "", "Entry"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-50)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-51)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-35-52)... ).show() 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/bi_signals.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/mtf-analysis/bi_signals.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-1)>>> pf = vbt.Portfolio.from_signals(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-2)... h1_data,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-3)... entries,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-4)... exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-5)... sl_stop=0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-6)... freq="1h"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-9)>>> pf.orders.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-10)timeframe fast_sma_timeperiod slow_sma_timeperiod
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-11)1h 10 20 504
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-12) 20 30 379
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-13)4h 10 20 111
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-14) 20 30 85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-15)1d 10 20 13
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-16) 20 30 7
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-17)Name: count, dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-19)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-20)timeframe fast_sma_timeperiod slow_sma_timeperiod
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-21)1h 10 20 3.400095
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-22) 20 30 2.051091
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-23)4h 10 20 2.751626
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-24) 20 30 1.559501
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-25)1d 10 20 3.239846
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-26) 20 30 2.755367
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis/alignment/#__codelineno-36-27)Name: sharpe_ratio, dtype: float64
 
[/code]

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/mtf-analysis/alignment.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/MTFAnalysis.ipynb)