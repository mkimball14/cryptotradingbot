expr

#  expr module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr "Permanent link")

Functions and config for evaluating indicator expressions.

* * *

## expr_func_config HybridConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.expr_func_config "Permanent link")

Config for functions used in indicator expressions.

Can be modified.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-2)    delay=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-3)        func=<function delay at 0x17466c540>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-4)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-5)    delta=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-6)        func=<function delta at 0x17466c5e0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-8)    cs_rescale=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-9)        func=<function cs_rescale at 0x17466c680>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-10)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-11)    cs_rank=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-12)        func=<function cs_rank at 0x17466c720>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-14)    cs_demean=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-15)        func=<function cs_demean at 0x17466c7c0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-16)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-17)    ts_min=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-18)        func=<function ts_min at 0x17466c860>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-19)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-20)    ts_max=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-21)        func=<function ts_max at 0x17466c900>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-22)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-23)    ts_argmin=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-24)        func=<function ts_argmin at 0x17466c9a0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-26)    ts_argmax=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-27)        func=<function ts_argmax at 0x17466ca40>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-28)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-29)    ts_rank=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-30)        func=<function ts_rank at 0x17466cae0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-31)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-32)    ts_sum=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-33)        func=<function ts_sum at 0x17466cb80>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-35)    ts_product=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-36)        func=<function ts_product at 0x17466cc20>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-37)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-38)    ts_mean=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-39)        func=<function ts_mean at 0x17466ccc0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-40)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-41)    ts_wmean=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-42)        func=<function ts_wmean at 0x17466cd60>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-43)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-44)    ts_std=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-45)        func=<function ts_std at 0x17466ce00>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-46)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-47)    ts_corr=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-48)        func=<function ts_corr at 0x17466cea0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-49)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-50)    ts_cov=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-51)        func=<function ts_cov at 0x17466cf40>
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-52)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-53)    adv=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-54)        func=<function adv at 0x17466cfe0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-55)        magnet_inputs=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-56)            'volume'
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-57)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-58)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-0-59))
    

* * *

## expr_res_func_config HybridConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.expr_res_func_config "Permanent link")

Config for resolvable functions used in indicator expressions.

Can be modified.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-2)    returns=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-3)        func=<function returns at 0x17466d080>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-4)        magnet_inputs=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-5)            'close'
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-6)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-8)    vwap=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-9)        func=<function vwap at 0x17466d120>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-10)        magnet_inputs=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-11)            'high',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-12)            'low',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-13)            'close',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-14)            'volume'
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-15)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-16)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-17)    cap=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-18)        func=<function cap at 0x17466d1c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-19)        magnet_inputs=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-20)            'close',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-21)            'volume'
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-22)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-23)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-1-24))
    

* * *

## wqa101_expr_config HybridConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.wqa101_expr_config "Permanent link")

Config with WorldQuant's 101 alpha expressions.

See [101 Formulaic Alphas](https://arxiv.org/abs/1601.00991).

Can be modified.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-1)HybridConfig({
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-2)    1: 'cs_rank(ts_argmax(power(where(returns < 0, ts_std(returns, 20), close), 2.), 5)) - 0.5',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-3)    2: '-ts_corr(cs_rank(delta(log(volume), 2)), cs_rank((close - open) / open), 6)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-4)    3: '-ts_corr(cs_rank(open), cs_rank(volume), 10)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-5)    4: '-ts_rank(cs_rank(low), 9)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-6)    5: 'cs_rank(open - (ts_sum(vwap, 10) / 10)) * (-abs(cs_rank(close - vwap)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-7)    6: '-ts_corr(open, volume, 10)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-8)    7: 'where(adv(20) < volume, (-ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7)), -1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-9)    8: '-cs_rank((ts_sum(open, 5) * ts_sum(returns, 5)) - delay(ts_sum(open, 5) * ts_sum(returns, 5), 10))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-10)    9: 'where(0 < ts_min(delta(close, 1), 5), delta(close, 1), where(ts_max(delta(close, 1), 5) < 0, delta(close, 1), -delta(close, 1)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-11)    10: 'cs_rank(where(0 < ts_min(delta(close, 1), 4), delta(close, 1), where(ts_max(delta(close, 1), 4) < 0, delta(close, 1), -delta(close, 1))))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-12)    11: '(cs_rank(ts_max(vwap - close, 3)) + cs_rank(ts_min(vwap - close, 3))) * cs_rank(delta(volume, 3))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-13)    12: 'sign(delta(volume, 1)) * (-delta(close, 1))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-14)    13: '-cs_rank(ts_cov(cs_rank(close), cs_rank(volume), 5))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-15)    14: '(-cs_rank(delta(returns, 3))) * ts_corr(open, volume, 10)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-16)    15: '-ts_sum(cs_rank(ts_corr(cs_rank(high), cs_rank(volume), 3)), 3)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-17)    16: '-cs_rank(ts_cov(cs_rank(high), cs_rank(volume), 5))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-18)    17: '((-cs_rank(ts_rank(close, 10))) * cs_rank(delta(delta(close, 1), 1))) * cs_rank(ts_rank(volume / adv(20), 5))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-19)    18: '-cs_rank((ts_std(abs(close - open), 5) + (close - open)) + ts_corr(close, open, 10))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-20)    19: '(-sign((close - delay(close, 7)) + delta(close, 7))) * (1 + cs_rank(1 + ts_sum(returns, 250)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-21)    20: '((-cs_rank(open - delay(high, 1))) * cs_rank(open - delay(close, 1))) * cs_rank(open - delay(low, 1))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-22)    21: 'where(((ts_sum(close, 8) / 8) + ts_std(close, 8)) < (ts_sum(close, 2) / 2), -1, where((ts_sum(close, 2) / 2) < ((ts_sum(close, 8) / 8) - ts_std(close, 8)), 1, where(volume / adv(20) >= 1, 1, -1)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-23)    22: '-(delta(ts_corr(high, volume, 5), 5) * cs_rank(ts_std(close, 20)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-24)    23: 'where((ts_sum(high, 20) / 20) < high, -delta(high, 2), 0)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-25)    24: 'where((delta(ts_sum(close, 100) / 100, 100) / delay(close, 100)) <= 0.05, (-(close - ts_min(close, 100))), -delta(close, 3))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-26)    25: 'cs_rank((((-returns) * adv(20)) * vwap) * (high - close))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-27)    26: '-ts_max(ts_corr(ts_rank(volume, 5), ts_rank(high, 5), 5), 3)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-28)    27: 'where(0.5 < cs_rank(ts_sum(ts_corr(cs_rank(volume), cs_rank(vwap), 6), 2) / 2.0), -1, 1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-29)    28: 'cs_rescale((ts_corr(adv(20), low, 5) + ((high + low) / 2)) - close)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-30)    29: 'ts_min(ts_product(cs_rank(cs_rank(cs_rescale(log(ts_sum(ts_min(cs_rank(cs_rank(-cs_rank(delta(close - 1, 5)))), 2), 1))))), 1), 5) + ts_rank(delay(-returns, 6), 5)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-31)    30: '((1.0 - cs_rank((sign(close - delay(close, 1)) + sign(delay(close, 1) - delay(close, 2))) + sign(delay(close, 2) - delay(close, 3)))) * ts_sum(volume, 5)) / ts_sum(volume, 20)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-32)    31: '(cs_rank(cs_rank(cs_rank(ts_wmean(-cs_rank(cs_rank(delta(close, 10))), 10)))) + cs_rank(-delta(close, 3))) + sign(cs_rescale(ts_corr(adv(20), low, 12)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-33)    32: 'cs_rescale((ts_sum(close, 7) / 7) - close) + (20 * cs_rescale(ts_corr(vwap, delay(close, 5), 230)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-34)    33: 'cs_rank(-(1 - (open / close)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-35)    34: 'cs_rank((1 - cs_rank(ts_std(returns, 2) / ts_std(returns, 5))) + (1 - cs_rank(delta(close, 1))))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-36)    35: '(ts_rank(volume, 32) * (1 - ts_rank((close + high) - low, 16))) * (1 - ts_rank(returns, 32))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-37)    36: '((((2.21 * cs_rank(ts_corr(close - open, delay(volume, 1), 15))) + (0.7 * cs_rank(open - close))) + (0.73 * cs_rank(ts_rank(delay(-returns, 6), 5)))) + cs_rank(abs(ts_corr(vwap, adv(20), 6)))) + (0.6 * cs_rank(((ts_sum(close, 200) / 200) - open) * (close - open)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-38)    37: 'cs_rank(ts_corr(delay(open - close, 1), close, 200)) + cs_rank(open - close)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-39)    38: '(-cs_rank(ts_rank(close, 10))) * cs_rank(close / open)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-40)    39: '(-cs_rank(delta(close, 7) * (1 - cs_rank(ts_wmean(volume / adv(20), 9))))) * (1 + cs_rank(ts_sum(returns, 250)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-41)    40: '(-cs_rank(ts_std(high, 10))) * ts_corr(high, volume, 10)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-42)    41: '((high * low) ** 0.5) - vwap',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-43)    42: 'cs_rank(vwap - close) / cs_rank(vwap + close)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-44)    43: 'ts_rank(volume / adv(20), 20) * ts_rank(-delta(close, 7), 8)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-45)    44: '-ts_corr(high, cs_rank(volume), 5)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-46)    45: '-((cs_rank(ts_sum(delay(close, 5), 20) / 20) * ts_corr(close, volume, 2)) * cs_rank(ts_corr(ts_sum(close, 5), ts_sum(close, 20), 2)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-47)    46: 'where(0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)), -1, where((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0, 1, -(close - delay(close, 1))))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-48)    47: '(((cs_rank(1 / close) * volume) / adv(20)) * ((high * cs_rank(high - close)) / (ts_sum(high, 5) / 5))) - cs_rank(vwap - delay(vwap, 5))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-49)    48: "cs_demean((ts_corr(delta(close, 1), delta(delay(close, 1), 1), 250) * delta(close, 1)) / close, 'subindustry') / ts_sum((delta(close, 1) / delay(close, 1)) ** 2, 250)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-50)    49: 'where((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-0.1), 1, -(close - delay(close, 1)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-51)    50: '-ts_max(cs_rank(ts_corr(cs_rank(volume), cs_rank(vwap), 5)), 5)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-52)    51: 'where((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-0.05), 1, -(close - delay(close, 1)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-53)    52: '(((-ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * cs_rank((ts_sum(returns, 240) - ts_sum(returns, 20)) / 220)) * ts_rank(volume, 5)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-54)    53: '-delta(((close - low) - (high - close)) / (close - low), 9)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-55)    54: '(-((low - close) * (open ** 5))) / ((low - high) * (close ** 5))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-56)    55: '-ts_corr(cs_rank((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12))), cs_rank(volume), 6)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-57)    56: '0 - (1 * (cs_rank(ts_sum(returns, 10) / ts_sum(ts_sum(returns, 2), 3)) * cs_rank(returns * cap)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-58)    57: '0 - (1 * ((close - vwap) / ts_wmean(cs_rank(ts_argmax(close, 30)), 2)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-59)    58: "-ts_rank(ts_wmean(ts_corr(cs_demean(vwap, 'sector'), volume, 3.92795), 7.89291), 5.50322)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-60)    59: "-ts_rank(ts_wmean(ts_corr(cs_demean((vwap * 0.728317) + (vwap * (1 - 0.728317)), 'industry'), volume, 4.25197), 16.2289), 8.19648)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-61)    60: '0 - (1 * ((2 * cs_rescale(cs_rank((((close - low) - (high - close)) / (high - low)) * volume))) - cs_rescale(cs_rank(ts_argmax(close, 10)))))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-62)    61: 'cs_rank(vwap - ts_min(vwap, 16.1219)) < cs_rank(ts_corr(vwap, adv(180), 17.9282))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-63)    62: '(cs_rank(ts_corr(vwap, ts_sum(adv(20), 22.4101), 9.91009)) < cs_rank((cs_rank(open) + cs_rank(open)) < (cs_rank((high + low) / 2) + cs_rank(high)))) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-64)    63: "(cs_rank(ts_wmean(delta(cs_demean(close, 'industry'), 2.25164), 8.22237)) - cs_rank(ts_wmean(ts_corr((vwap * 0.318108) + (open * (1 - 0.318108)), ts_sum(adv(180), 37.2467), 13.557), 12.2883))) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-65)    64: '(cs_rank(ts_corr(ts_sum((open * 0.178404) + (low * (1 - 0.178404)), 12.7054), ts_sum(adv(120), 12.7054), 16.6208)) < cs_rank(delta((((high + low) / 2) * 0.178404) + (vwap * (1 - 0.178404)), 3.69741))) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-66)    65: '(cs_rank(ts_corr((open * 0.00817205) + (vwap * (1 - 0.00817205)), ts_sum(adv(60), 8.6911), 6.40374)) < cs_rank(open - ts_min(open, 13.635))) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-67)    66: '(cs_rank(ts_wmean(delta(vwap, 3.51013), 7.23052)) + ts_rank(ts_wmean((((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2)), 11.4157), 6.72611)) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-68)    67: "(cs_rank(high - ts_min(high, 2.14593)) ** cs_rank(ts_corr(cs_demean(vwap, 'sector'), cs_demean(adv(20), 'subindustry'), 6.02936))) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-69)    68: '(ts_rank(ts_corr(cs_rank(high), cs_rank(adv(15)), 8.91644), 13.9333) < cs_rank(delta((close * 0.518371) + (low * (1 - 0.518371)), 1.06157))) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-70)    69: "(cs_rank(ts_max(delta(cs_demean(vwap, 'industry'), 2.72412), 4.79344)) ** ts_rank(ts_corr((close * 0.490655) + (vwap * (1 - 0.490655)), adv(20), 4.92416), 9.0615)) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-71)    70: "(cs_rank(delta(vwap, 1.29456)) ** ts_rank(ts_corr(cs_demean(close, 'industry'), adv(50), 17.8256), 17.9171)) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-72)    71: 'maximum(ts_rank(ts_wmean(ts_corr(ts_rank(close, 3.43976), ts_rank(adv(180), 12.0647), 18.0175), 4.20501), 15.6948), ts_rank(ts_wmean(cs_rank((low + open) - (vwap + vwap)) ** 2, 16.4662), 4.4388))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-73)    72: 'cs_rank(ts_wmean(ts_corr((high + low) / 2, adv(40), 8.93345), 10.1519)) / cs_rank(ts_wmean(ts_corr(ts_rank(vwap, 3.72469), ts_rank(volume, 18.5188), 6.86671), 2.95011))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-74)    73: 'maximum(cs_rank(ts_wmean(delta(vwap, 4.72775), 2.91864)), ts_rank(ts_wmean((delta((open * 0.147155) + (low * (1 - 0.147155)), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))) * (-1), 3.33829), 16.7411)) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-75)    74: '(cs_rank(ts_corr(close, ts_sum(adv(30), 37.4843), 15.1365)) < cs_rank(ts_corr(cs_rank((high * 0.0261661) + (vwap * (1 - 0.0261661))), cs_rank(volume), 11.4791))) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-76)    75: 'cs_rank(ts_corr(vwap, volume, 4.24304)) < cs_rank(ts_corr(cs_rank(low), cs_rank(adv(50)), 12.4413))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-77)    76: "maximum(cs_rank(ts_wmean(delta(vwap, 1.24383), 11.8259)), ts_rank(ts_wmean(ts_rank(ts_corr(cs_demean(low, 'sector'), adv(81), 8.14941), 19.569), 17.1543), 19.383)) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-78)    77: 'minimum(cs_rank(ts_wmean((((high + low) / 2) + high) - (vwap + high), 20.0451)), cs_rank(ts_wmean(ts_corr((high + low) / 2, adv(40), 3.1614), 5.64125)))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-79)    78: 'cs_rank(ts_corr(ts_sum((low * 0.352233) + (vwap * (1 - 0.352233)), 19.7428), ts_sum(adv(40), 19.7428), 6.83313)) ** cs_rank(ts_corr(cs_rank(vwap), cs_rank(volume), 5.77492))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-80)    79: "cs_rank(delta(cs_demean((close * 0.60733) + (open * (1 - 0.60733)), 'sector'), 1.23438)) < cs_rank(ts_corr(ts_rank(vwap, 3.60973), ts_rank(adv(150), 9.18637), 14.6644))",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-81)    80: "(cs_rank(sign(delta(cs_demean((open * 0.868128) + (high * (1 - 0.868128)), 'industry'), 4.04545))) ** ts_rank(ts_corr(high, adv(10), 5.11456), 5.53756)) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-82)    81: '(cs_rank(log(ts_product(cs_rank(cs_rank(ts_corr(vwap, ts_sum(adv(10), 49.6054), 8.47743)) ** 4), 14.9655))) < cs_rank(ts_corr(cs_rank(vwap), cs_rank(volume), 5.07914))) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-83)    82: "minimum(cs_rank(ts_wmean(delta(open, 1.46063), 14.8717)), ts_rank(ts_wmean(ts_corr(cs_demean(volume, 'sector'), ((open * 0.634196) + (open * (1 - 0.634196))), 17.4842), 6.92131), 13.4283)) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-84)    83: '(cs_rank(delay((high - low) / (ts_sum(close, 5) / 5), 2)) * cs_rank(cs_rank(volume))) / (((high - low) / (ts_sum(close, 5) / 5)) / (vwap - close))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-85)    84: 'power(ts_rank(vwap - ts_max(vwap, 15.3217), 20.7127), delta(close, 4.96796))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-86)    85: 'cs_rank(ts_corr((high * 0.876703) + (close * (1 - 0.876703)), adv(30), 9.61331)) ** cs_rank(ts_corr(ts_rank((high + low) / 2, 3.70596), ts_rank(volume, 10.1595), 7.11408))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-87)    86: '(ts_rank(ts_corr(close, ts_sum(adv(20), 14.7444), 6.00049), 20.4195) < cs_rank((open + close) - (vwap + open))) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-88)    87: "maximum(cs_rank(ts_wmean(delta((close * 0.369701) + (vwap * (1 - 0.369701)), 1.91233), 2.65461)), ts_rank(ts_wmean(abs(ts_corr(cs_demean(adv(81), 'industry'), close, 13.4132)), 4.89768), 14.4535)) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-89)    88: 'minimum(cs_rank(ts_wmean((cs_rank(open) + cs_rank(low)) - (cs_rank(high) + cs_rank(close)), 8.06882)), ts_rank(ts_wmean(ts_corr(ts_rank(close, 8.44728), ts_rank(adv(60), 20.6966), 8.01266), 6.65053), 2.61957))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-90)    89: "ts_rank(ts_wmean(ts_corr((low * 0.967285) + (low * (1 - 0.967285)), adv(10), 6.94279), 5.51607), 3.79744) - ts_rank(ts_wmean(delta(cs_demean(vwap, 'industry'), 3.48158), 10.1466), 15.3012)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-91)    90: "(cs_rank(close - ts_max(close, 4.66719)) ** ts_rank(ts_corr(cs_demean(adv(40), 'subindustry'), low, 5.38375), 3.21856)) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-92)    91: "(ts_rank(ts_wmean(ts_wmean(ts_corr(cs_demean(close, 'industry'), volume, 9.74928), 16.398), 3.83219), 4.8667) - cs_rank(ts_wmean(ts_corr(vwap, adv(30), 4.01303), 2.6809))) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-93)    92: 'minimum(ts_rank(ts_wmean((((high + low) / 2) + close) < (low + open), 14.7221), 18.8683), ts_rank(ts_wmean(ts_corr(cs_rank(low), cs_rank(adv(30)), 7.58555), 6.94024), 6.80584))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-94)    93: "ts_rank(ts_wmean(ts_corr(cs_demean(vwap, 'industry'), adv(81), 17.4193), 19.848), 7.54455) / cs_rank(ts_wmean(delta((close * 0.524434) + (vwap * (1 - 0.524434)), 2.77377), 16.2664))",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-95)    94: '(cs_rank(vwap - ts_min(vwap, 11.5783)) ** ts_rank(ts_corr(ts_rank(vwap, 19.6462), ts_rank(adv(60), 4.02992), 18.0926), 2.70756)) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-96)    95: 'cs_rank(open - ts_min(open, 12.4105)) < ts_rank(cs_rank(ts_corr(ts_sum((high + low) / 2, 19.1351), ts_sum(adv(40), 19.1351), 12.8742)) ** 5, 11.7584)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-97)    96: 'maximum(ts_rank(ts_wmean(ts_corr(cs_rank(vwap), cs_rank(volume), 3.83878), 4.16783), 8.38151), ts_rank(ts_wmean(ts_argmax(ts_corr(ts_rank(close, 7.45404), ts_rank(adv(60), 4.13242), 3.65459), 12.6556), 14.0365), 13.4143)) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-98)    97: "(cs_rank(ts_wmean(delta(cs_demean((low * 0.721001) + (vwap * (1 - 0.721001)), 'industry'), 3.3705), 20.4523)) - ts_rank(ts_wmean(ts_rank(ts_corr(ts_rank(low, 7.87871), ts_rank(adv(60), 17.255), 4.97547), 18.5925), 15.7152), 6.71659)) * (-1)",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-99)    98: 'cs_rank(ts_wmean(ts_corr(vwap, ts_sum(adv(5), 26.4719), 4.58418), 7.18088)) - cs_rank(ts_wmean(ts_rank(ts_argmin(ts_corr(cs_rank(open), cs_rank(adv(15)), 20.8187), 8.62571), 6.95668), 8.07206))',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-100)    99: '(cs_rank(ts_corr(ts_sum((high + low) / 2, 19.8975), ts_sum(adv(60), 19.8975), 8.8136)) < cs_rank(ts_corr(low, volume, 6.28259))) * (-1)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-101)    100: "0 - (1 * (((1.5 * cs_rescale(cs_demean(cs_demean(cs_rank((((close - low) - (high - close)) / (high - low)) * volume), 'subindustry'), 'subindustry'))) - cs_rescale(cs_demean(ts_corr(close, cs_rank(adv(20)), 5) - cs_rank(ts_argmin(close, 30)), 'subindustry'))) * (volume / adv(20))))",
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-102)    101: '(close - open) / ((high - low) + .001)'
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-2-103)})
    

* * *

## adv function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L146-L148 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.adv "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-3-1)adv(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-3-2)    d,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-3-3)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-3-4))
    

Average daily dollar volume for the past `d` days.

* * *

## cap function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L168-L170 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.cap "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-4-1)cap(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-4-2)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-4-3))
    

Market capitalization.

* * *

## cs_demean function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L71-L74 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.cs_demean "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-5-1)cs_demean(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-5-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-5-3)    g,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-5-4)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-5-5))
    

Demean `x` against groups `g` cross-sectionally.

* * *

## cs_rank function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L66-L68 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.cs_rank "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-6-1)cs_rank(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-6-2)    x
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-6-3))
    

Rank cross-sectionally.

* * *

## cs_rescale function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L61-L63 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.cs_rescale "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-7-1)cs_rescale(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-7-2)    x
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-7-3))
    

Rescale `x` such that `sum(abs(x)) = 1`.

* * *

## delay function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L48-L50 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.delay "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-8-1)delay(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-8-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-8-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-8-4))
    

Value of `x` `d` days ago.

* * *

## delta function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L53-L55 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.delta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-9-1)delta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-9-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-9-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-9-4))
    

Today’s value of `x` minus the value of `x` `d` days ago.

* * *

## returns function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L154-L156 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-10-1)returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-10-2)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-10-3))
    

Daily close-to-close returns.

* * *

## ts_argmax function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L98-L103 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_argmax "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-11-1)ts_argmax(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-11-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-11-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-11-4))
    

Return the rolling argmax.

* * *

## ts_argmin function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L90-L95 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_argmin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-12-1)ts_argmin(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-12-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-12-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-12-4))
    

Return the rolling argmin.

* * *

## ts_corr function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L136-L138 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_corr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-13-1)ts_corr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-13-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-13-3)    y,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-13-4)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-13-5))
    

Time-serial correlation of `x` and `y` for the past `d` days.

* * *

## ts_cov function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L141-L143 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_cov "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-14-1)ts_cov(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-14-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-14-3)    y,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-14-4)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-14-5))
    

Time-serial covariance of `x` and `y` for the past `d` days.

* * *

## ts_max function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L85-L87 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_max "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-15-1)ts_max(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-15-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-15-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-15-4))
    

Return the rolling max.

* * *

## ts_mean function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L121-L123 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_mean "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-16-1)ts_mean(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-16-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-16-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-16-4))
    

Return the rolling mean.

* * *

## ts_min function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L80-L82 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_min "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-17-1)ts_min(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-17-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-17-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-17-4))
    

Return the rolling min.

* * *

## ts_product function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L116-L118 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_product "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-18-1)ts_product(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-18-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-18-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-18-4))
    

Return the rolling product.

* * *

## ts_rank function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L106-L108 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_rank "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-19-1)ts_rank(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-19-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-19-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-19-4))
    

Return the rolling rank.

* * *

## ts_std function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L131-L133 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_std "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-20-1)ts_std(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-20-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-20-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-20-4))
    

Return the rolling standard deviation.

* * *

## ts_sum function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L111-L113 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_sum "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-21-1)ts_sum(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-21-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-21-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-21-4))
    

Return the rolling sum.

* * *

## ts_wmean function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L126-L128 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.ts_wmean "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-22-1)ts_wmean(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-22-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-22-3)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-22-4))
    

Weighted moving average over the past `d` days with linearly decaying weight.

* * *

## vwap function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/indicators/expr.py#L159-L165 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#vectorbtpro.indicators.expr.vwap "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-23-1)vwap(
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-23-2)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/indicators/expr/#__codelineno-23-3))
    

VWAP.
