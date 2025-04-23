# Pre-analysis[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#pre-analysis "Permanent link")

Pre-analysis is an analysis phase that comes before the simulation. It enables us in introspecting the generated signal data, selecting specific signals such as by removing duplicates, but also analyzing the distribution of the signal data to identify potential issues with the selected trading strategy. Since signals are usually conditionally bound to their neighboring signals and introduce other cross-timestamp dependencies, the analysis cannot be (easily) performed in a vectorized manner using Pandas or other data science tools alone. But luckily, vectorbt lifts a lot of weight for us here too ![💪](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4aa.svg)


# Ranking[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#ranking "Permanent link")

Ideally, signals with opposite signs come one after another such that we can easily connect them together. But usually, things get messy very quickly: we might get entire partitions of signals with the same sign (that is, there are multiple `True` values with no `False` value in-between), or there might be signals that don't have an opposite signal at all. When dealing with such cases, we usually try to sort out signals that shouldn't be executed before passing them to the simulator. For example, when comparing one time series to another, we may consider the first signal in each partition to be the most important (= main signal), and other signals to be of much lesser importance because they are arriving too late. This importance imbalance among signals requires us to go through each signal and decide whether it's worth keeping.

Instead of implementing our own loop, we can use ranking - one of the most powerful approaches to quantifying signal locations. Ranking takes each signal and assigns it a number that exists only within a predefined context. For example, we can assign the first signal of each partition to `1` and each other signal to `0`, such that selecting the first signal requires just comparing the entire mask to `1` (it's yet another advantage of working with mask arrays over integer arrays). In vectorbt, ranking is implemented by the Numba-compiled function [rank_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rank_nb) and its accessor method [SignalsAccessor.rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rank), which takes a mask, and calls a UDF `rank_func_nb` at each signal encountered in a mask by passing a context of the type [RankContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext) and optionally arguments provided via `rank_args`.

For example, let's create a ranker that does what we discussed above:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-1)>>> @njit
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-2)>>> def rank_func_nb(c):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-3)... if c.sig_in_part_cnt == 1: 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-4)... return 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-5)... return 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-7)>>> sample_mask = pd.Series([True, True, False, True, True])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-8)>>> ranked = sample_mask.vbt.signals.rank(rank_func_nb)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-9)>>> ranked
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-10)0 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-11)1 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-12)2 -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-13)3 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-14)4 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-0-15)dtype: int64
 
[/code]

 1. 

As we see, it assigned `1` to each primary signal and `0` to each secondary signal. The ranking function also denoted all `False` values with `-1`, which is a kind of reserved number. We can then easily select the first signal of each partition:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-1-1)>>> ranked == 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-1-2)0 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-1-3)1 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-1-4)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-1-5)3 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-1-6)4 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-1-7)dtype: bool
 
[/code]

Hint

This is quite similar to how [SignalsAccessor.first](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first) works.

To call our UDF only on `True` values that come after encountering a `False` value, use `after_false`. This is particularly useful in crossover calculations since we usually want to rule the possibility of assigning a signal during an initial period of time when a time series is already above/below another time series.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-1)>>> ranked = sample_mask.vbt.signals.rank(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-2)... rank_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-3)... after_false=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-5)>>> ranked == 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-6)0 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-7)1 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-8)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-9)3 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-10)4 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-2-11)dtype: bool
 
[/code]

Another advantage of this method is that it allows us to specify another mask - resetter - whose signal can reset partitions in the main mask. Consider a scenario where we have an entries and an exits array. To select the first entry between each pair of exits, we need to specify the entries array as the main mask and the exits array as the resetting mask. Again, this will ignore all signals that come before the first resetting signal and call our UDF only on valid signals.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-1)>>> sample_entries = pd.Series([True, True, True, True, True])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-2)>>> sample_exits = pd.Series([False, False, True, False, False])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-3)>>> ranked = sample_entries.vbt.signals.rank(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-4)... rank_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-5)... reset_by=sample_exits
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-7)>>> ranked == 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-8)0 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-9)1 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-10)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-11)3 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-12)4 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-3-13)dtype: bool
 
[/code]

Info

As you might have noticed, the partition is effectively reset at the next timestamp after the resetting signal. This is because when an entry and an exit are placed at the same timestamp, the entry is assumed to come first, thus it should belong to the previous partition. To make vectorbt assume that the main signal comes after the resetting signal (such as when the main mask are exits and the resetting mask are entries), pass `wait=0`.

To avoid setting any entry signal before the first exit signal, we can use `after_reset`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-1)>>> ranked = sample_entries.vbt.signals.rank(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-2)... rank_func_nb, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-3)... reset_by=sample_exits,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-4)... after_reset=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-6)>>> ranked == 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-7)0 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-8)1 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-9)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-10)3 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-11)4 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-4-12)dtype: bool
 
[/code]


# Preset rankers[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#preset-rankers "Permanent link")

Writing own ranking functions is fun, but there are two preset rankers that suffice for most use cases: [sig_pos_rank_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.sig_pos_rank_nb) for ranking signals, and [part_pos_rank_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.part_pos_rank_nb) for ranking entire partitions. They are used by the accessor methods [SignalsAccessor.pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.pos_rank) and [SignalsAccessor.partition_pos_rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_pos_rank) respectively. Both methods assign ranks starting with a zero.

The first method assigns each signal a rank based on its position either in the current partition (`allow_gaps=False`) or globally (`allow_gaps=True`):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-1)>>> sample_mask = pd.Series([True, True, False, True, True])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-2)>>> ranked = sample_mask.vbt.signals.pos_rank()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-3)>>> ranked
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-4)0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-5)1 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-6)2 -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-7)3 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-8)4 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-9)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-11)>>> ranked == 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-12)0 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-13)1 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-14)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-15)3 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-16)4 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-17)dtype: bool
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-19)>>> ranked = sample_mask.vbt.signals.pos_rank(allow_gaps=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-20)>>> ranked
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-21)0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-22)1 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-23)2 -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-24)3 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-25)4 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-26)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-27)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-28)>>> (ranked > -1) & (ranked % 2 == 1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-29)0 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-30)1 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-31)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-32)3 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-33)4 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-5-34)dtype: bool
 
[/code]

 1. 2. 

The second method assigns each signal a rank based on the position of its partition, such that we can select entire partitions of signals easily:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-1)>>> ranked = sample_mask.vbt.signals.partition_pos_rank(allow_gaps=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-2)>>> ranked
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-3)0 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-4)1 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-5)2 -1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-6)3 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-7)4 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-8)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-10)>>> ranked == 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-11)0 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-12)1 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-13)2 False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-14)3 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-15)4 True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-6-16)dtype: bool
 
[/code]

 1. 

In addition, there are accessor methods that do the comparison operation for us: [SignalsAccessor.first](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first), [SignalsAccessor.nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth), [SignalsAccessor.from_nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.from_nth), and [SignalsAccessor.to_nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth). They are all based on the signal position ranker (first method), and each has its own version with the suffix `after`, such as [SignalsAccessor.to_nth_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth_after), that does the same but conditionally after each resetting signal and with enabled `allow_gaps`.

So, why should we care? Because we can do the following: compare one time series to another, and select the first signal after a number of successful confirmations. Let's get back to our Bollinger Bands example based on two conditions, and check how many signals would be left if we waited for a minimum of zero, one, and two confirmations:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-1)>>> entry_cond1 = data.get("Low") < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-2)>>> entry_cond2 = bandwidth > 0.3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-3)>>> entry_cond3 = data.get("High") > bb.upperband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-4)>>> entry_cond4 = bandwidth < 0.15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-5)>>> entries = (entry_cond1 & entry_cond2) | (entry_cond3 & entry_cond4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-7)>>> entries.vbt.signals.from_nth(0).sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-8)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-9)BTCUSDT 25
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-10)ETHUSDT 13
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-11)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-13)>>> entries.vbt.signals.from_nth(1).sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-14)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-15)BTCUSDT 14
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-16)ETHUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-17)dtype: int64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-19)>>> entries.vbt.signals.from_nth(2).sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-20)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-21)BTCUSDT 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-22)ETHUSDT 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-7-23)dtype: int64
 
[/code]

Let's generate exit signals from the opposite conditions:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-8-1)>>> exit_cond1 = data.get("High") > bb.upperband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-8-2)>>> exit_cond2 = bandwidth > 0.3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-8-3)>>> exit_cond3 = data.get("Low") < bb.lowerband
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-8-4)>>> exit_cond4 = bandwidth < 0.15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-8-5)>>> exits = (exit_cond1 & exit_cond2) | (exit_cond3 & exit_cond4)
 
[/code]

What's the maximum number of exit signals after each entry signal?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-9-1)>>> exits.vbt.signals.pos_rank_after(entries, reset_wait=0).max() + 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-9-2)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-9-3)BTCUSDT 9
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-9-4)ETHUSDT 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-9-5)dtype: int64
 
[/code]

 1. 

Conversely, what's the maximum number of entry signals after each exit signal?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-10-1)>>> entries.vbt.signals.pos_rank_after(exits).max() + 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-10-2)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-10-3)BTCUSDT 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-10-4)ETHUSDT 7
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-10-5)dtype: int64
 
[/code]

Get the timestamps and ranks of exit signals with the highest rank after each entry signal:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-11-1)>>> ranked = exits.vbt.signals.pos_rank_after(entries, reset_wait=0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-11-2)>>> highest_ranked = ranked == ranked.max()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-11-3)>>> ranked[highest_ranked.any(axis=1)]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-11-4)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-11-5)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-11-6)2021-05-12 00:00:00+00:00 -1 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-11-7)2021-07-28 00:00:00+00:00 8 -1
 
[/code]

Are there any exit signals before the first entry signal, and if yes, how many?
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-12-1)>>> exits_after = exits.vbt.signals.from_nth_after(0, entries, reset_wait=0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-12-2)>>> (exits ^ exits_after).sum() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-12-3)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-12-4)BTCUSDT 10
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-12-5)ETHUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-12-6)dtype: int64
 
[/code]

 1. 


# Mapped ranks[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#mapped-ranks "Permanent link")

To enhance any ranking analysis, we can use the flag `as_mapped` in [SignalsAccessor.rank](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rank) to instruct vectorbt to produce a mapped array of ranks instead of an integer Series/DataFrame. Mapped arrays have the advantage of not storing `-1` and working directly on zero and positive ranks, which compresses the data but still allows us to produce various metrics per column or even per group. For example, let's consider that both symbols belong to one portfolio and we want to aggregate their statistics. Let's compare the bandwidth against multiple threshold combinations and return the maximum rank across both symbol columns for each combination:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-1)>>> mask = bandwidth.vbt > vbt.Param(np.arange(1, 10) / 10, name="bw_th")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-2)>>> mapped_ranks = mask.vbt.signals.pos_rank(as_mapped=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-3)>>> mapped_ranks.max(group_by=vbt.ExceptLevel("symbol")) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-4)bw_th
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-5)0.1 237.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-6)0.2 50.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-7)0.3 19.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-8)0.4 12.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-9)0.5 10.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-10)0.6 8.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-11)0.7 5.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-12)0.8 2.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-13)0.9 NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-13-14)Name: max, dtype: float64
 
[/code]

 1. 


# Cleaning[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#cleaning "Permanent link")

Cleaning is all about removing signals that shouldn't be converted into orders. Since we're mostly interested in one signal opening a position and another one closing or reversing it, we need to arrive at a signal schema where signals of opposite signs come one after another forming a [chain](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/generation/#chained-exits). Moreover, unless we want to accumulate orders using the argument `accumulate` in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals), only the first signal will be executed anyway. Removing redundant signals is easily done with [SignalsAccessor.first_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first_after). Below, we're selecting the first exit signal after each entry signal and the first entry signal after each exit signal (in this particular order!):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-14-1)>>> new_exits = exits.vbt.signals.first_after(entries, reset_wait=0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-14-2)>>> new_entries = entries.vbt.signals.first_after(exits)
 
[/code]

Let's visualize the selected signals:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-1)>>> symbol = "ETHUSDT"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-2)>>> fig = data.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-3)... symbol=symbol, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-4)... ohlc_trace_kwargs=dict(opacity=0.5), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-5)... plot_volume=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-7)>>> entries[symbol].vbt.signals.plot_as_entries(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-8)... y=data.get("Close", symbol), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-9)>>> exits[symbol].vbt.signals.plot_as_exits(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-10)... y=data.get("Close", symbol), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-11)>>> new_entries[symbol].vbt.signals.plot_as_entry_marks(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-12)... y=data.get("Close", symbol), fig=fig, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-13)... trace_kwargs=dict(name="New entries"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-14)>>> new_exits[symbol].vbt.signals.plot_as_exit_marks(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-15)... y=data.get("Close", symbol), fig=fig, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-16)... trace_kwargs=dict(name="New exits"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-15-17)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/cleaning.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/signal-dev/cleaning.dark.svg#only-dark)

Hint

To allow having the first exit signal before the first entry signal, pass `after_reset=False`. To **require** the first exit signal to be before the first entry signal, reverse the order of `first_after` calls.

But there is even simpler method - [SignalsAccessor.clean](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.clean), which does the same as above but with a single loop passing over all the signal data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-16-1)>>> new_entries, new_exits = entries.vbt.signals.clean(exits)
 
[/code]

It also offers a couple of convenient arguments for controlling the cleaning process. For example, by default, it assumes that entry signals are executed before exit signals (use `reverse_order` to change). It also removes all entry and exit signals that happen at the same time (use `keep_conflicts` to disable), and guarantees to place an entry first (use `force_first` to disable). For a more complex cleaning process, there is no way around a custom loop. Without the second mask (`exits` in our case), it will simply select the first signal out of each partition.


# Duration[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#duration "Permanent link")

Apart from ranks, we can also analyze duration! For example, we might be interested in knowing what's the average, minimum, and maximum distance between each pair of neighboring signals in a mask. Even though extracting such information is usually not a problem, the real challenge is its representation: we often want to know not only the distance itself but also the index of the first and last signal. Using mapped arrays is not enough since they allow us to represent one feature of data at most. But here's the solution: use the [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges) records, which is the backbone class for analyzing time-bound processes, such as positions and drawdowns! We can then mark one signal as the range's start and another signal as the range's end, and assess various metrics related to the distance between them ![📐](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d0.svg)

To get the range records for a single mask, we can use the Numba-compiled function [between_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_ranges_nb) and its accessor method [SignalsAccessor.between_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_ranges). Let's map each pair of neighboring signals in `entries` into a range:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-1)>>> ranges = entries.vbt.signals.between_ranges()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-2)>>> ranges.records
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-3) id col start_row end_row status
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-4)0 0 0 99 100 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-5)1 1 0 100 101 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-6)2 2 0 101 102 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-7)...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-8)33 9 1 173 242 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-9)34 10 1 242 286 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-17-10)35 11 1 286 313 1
 
[/code]

Hint

To print the records in a human-readable format, use `records_readable`.

Here, `col` is the column index, `start_idx` is the index of the left signal, `end_row` is the index of the right signal, and `status` of type [RangeStatus](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.RangeStatus) is always `RangeStatus.Closed`. We can access each of those fields as regular attributes and get an analyzable mapped array in return. Let's get the index of the first signal in each column:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-18-1)>>> ranges.start_idx.min(wrap_kwargs=dict(to_index=True))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-18-2)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-18-3)BTCUSDT 2021-04-10 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-18-4)ETHUSDT 2021-02-25 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-18-5)Name: min, dtype: datetime64[ns, UTC]
 
[/code]

Similarly, the duration as a mapped array is accessible via the attribute `duration`. Let's describe the duration in each column:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-1)>>> ranges.duration.describe(wrap_kwargs=dict(to_timedelta=True))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-2)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-3)mean 10 days 21:00:00 21 days 12:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-4)std 22 days 18:47:41.748587504 28 days 19:32:48.777556028
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-5)min 1 days 00:00:00 1 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-6)25% 1 days 00:00:00 1 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-7)50% 1 days 00:00:00 2 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-8)75% 2 days 06:00:00 32 days 18:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-19-9)max 89 days 00:00:00 80 days 00:00:00
 
[/code]

We see that at least 50% of the entry signals in the column `BTCUSDT` are laid out next to each other (one bar = one day), while the average duration between two signals is 10 days. We also see that signals in `ETHUSDT` are distributed more sparsely. The longest period of time when our strategy generated no signal is 90 days for `BTCUSDT` and 80 days for `ETHSUDT`.

When dealing with two masks, such as entry and exit signals, we're more likely interested in assessing the space between signals of both masks rather than signals in each mask separately. This can be realized by a mapping procedure that goes one signal at a time in the first mask (a.k.a. "source mask") and looks for one to many succeeding signals in the second mask (a.k.a. "target mask"), up until the next signal in the source mask. Such a procedure is implemented by the Numba-compiled function [between_two_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_two_ranges_nb). The accessor method is the same as above - [SignalsAccessor.between_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_ranges), which switches to the second mode if the argument `target` is specified. For example, let's get the average distance from each entry signal to its succeeding exit signal before and after cleaning:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-1)>>> ranges = entries.vbt.signals.between_ranges(target=exits)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-2)>>> ranges.avg_duration
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-3)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-4)BTCUSDT 46 days 00:51:25.714285714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-5)ETHUSDT 38 days 18:51:25.714285714
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-6)Name: avg_duration, dtype: timedelta64[ns]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-8)>>> new_ranges = new_entries.vbt.signals.between_ranges(target=new_exits)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-9)>>> new_ranges.avg_duration 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-10)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-11)BTCUSDT 43 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-12)ETHUSDT 23 days 12:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-20-13)Name: avg_duration, dtype: timedelta64[ns]
 
[/code]

 1. 

Info

If two signals are happening at the same time, the signal from the source mask is assumed to come first.

Since an exit signal can happen after many entry signals, we can also reverse the mapping order by specifying the many-to-one relationship with `relation="manyone"`, and get the average distance from each exit to any of its preceding entry signals:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-1)>>> ranges = entries.vbt.signals.between_ranges(target=exits, relation="manyone")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-2)>>> ranges.avg_duration
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-3)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-4)BTCUSDT 37 days 14:10:54.545454545
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-5)ETHUSDT 22 days 01:50:46.153846153
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-6)Name: avg_duration, dtype: timedelta64[ns]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-8)>>> new_ranges = new_entries.vbt.signals.between_ranges(target=new_exits, relation="manyone")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-9)>>> new_ranges.avg_duration
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-10)symbol
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-11)BTCUSDT 43 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-12)ETHUSDT 23 days 12:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-21-13)Name: avg_duration, dtype: timedelta64[ns]
 
[/code]

We can see that the cleaning process was successful because the average distance from each entry to its exit signal and vice versa is the same.

Remember how a partition is just a sequence of `True` values with no `False` value in-between? The same mapping approach can be applied to measure the length of entire partitions of signals: take the first and last signal of a partition, and map them to a range record. This is possible thanks to the Numba-compiled function [partition_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.partition_ranges_nb) and its accessor method [SignalsAccessor.partition_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_ranges). Let's extract the number of entry signal partitions and their length distribution before and after cleaning:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-1)>>> ranges = entries.vbt.signals.partition_ranges()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-2)>>> ranges.duration.describe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-3)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-4)count 11.000000 8.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-5)mean 2.272727 1.625000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-6)std 1.190874 0.916125
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-7)min 1.000000 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-8)25% 1.500000 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-9)50% 2.000000 1.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-10)75% 3.000000 2.250000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-11)max 5.000000 3.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-12)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-13)>>> new_ranges = new_entries.vbt.signals.partition_ranges()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-14)>>> new_ranges.duration.describe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-15)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-16)count 4.0 4.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-17)mean 1.0 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-18)std 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-19)min 1.0 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-20)25% 1.0 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-21)50% 1.0 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-22)75% 1.0 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-22-23)max 1.0 1.0
 
[/code]

We see that there are 11 partitions in the column `BTCUSDT`, with at least 50% of them consisting of two or more signals. What does it mean? It means that whenever our strategy indicates an entry, this entry signal stays valid for 2 or more days at least 50% of time. After cleaning, we see that we've removed lots of partitions that were located between two exit signals, and that each partition is now exactly one signal long (= the first signal). We also see that our strategy is more active in the `BTCUSDT` marked compared to the `ETHSUDT` market.

Finally, we can not only quantify partitions themselves, but also the pairwise distance between partitions! Let's derive the distribution of the distance between the last signal of one partition and the first signal of the next partition using the range records generated by the accessor method [SignalsAccessor.between_partition_ranges](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.between_partition_ranges), which is based on the Numba-compiled function [between_partition_ranges_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_partition_ranges_nb):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-1)>>> ranges = entries.vbt.signals.between_partition_ranges()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-2)>>> ranges.duration.describe(wrap_kwargs=dict(to_timedelta=True))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-3)symbol BTCUSDT ETHUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-4)mean 24 days 16:48:00 36 days 03:25:42.857142857
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-5)std 31 days 00:33:47.619615945 30 days 08:40:17.723113570
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-6)min 2 days 00:00:00 2 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-7)25% 2 days 00:00:00 14 days 12:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-8)50% 6 days 12:00:00 29 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-9)75% 40 days 06:00:00 56 days 12:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-23-10)max 89 days 00:00:00 80 days 00:00:00
 
[/code]

We can now better analyze how many periods in a row our strategy marked as "do not order". Here, the average streak without a signal in the `ETHUSDT` column is 36 days.


# Overview[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#overview "Permanent link")

If we want a quick overview of what's happening in our signal arrays, we can compute a variety of metrics and display them together using the base method [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats), which has been overridden by the accessor [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor) and tailored specifically for signal data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-1)>>> entries.vbt.signals.stats(column="BTCUSDT")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-2)Start 2021-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-3)End 2021-12-31 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-4)Period 365 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-5)Total 25
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-6)Rate [%] 6.849315
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-7)First Index 2021-04-10 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-8)Last Index 2021-12-27 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-9)Norm Avg Index [-1, 1] 0.159121
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-10)Distance: Min 1 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-11)Distance: Median 1 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-12)Distance: Max 89 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-13)Total Partitions 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-14)Partition Rate [%] 44.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-15)Partition Length: Min 1 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-16)Partition Length: Median 2 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-17)Partition Length: Max 5 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-18)Partition Distance: Min 2 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-19)Partition Distance: Median 6 days 12:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-20)Partition Distance: Max 89 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-24-21)Name: BTCUSDT, dtype: object
 
[/code]

Note

Without providing a column, the method will take the mean of all columns.

And here's what it means. The signal mask starts on the January 1st, 2021 and ends on the December 31, 2021. The entire period stretches over 365 days. There are 25 signals in our mask, which is 6.85% out of 365 (the total number of entries). The index of the first and last signal (see [SignalsAccessor.nth_index](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.nth_index)) was placed on the April 10th and December 27th respectively. A positive normalized average index, which tracks the skew of signal positions in the mask (see [SignalsAccessor.norm_avg_index](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.norm_avg_index)), hints at the signals being more prevalent in the second half of the backtesting period. Also, at least 50% of signals are located next to each other, while the maximum distance between each pair of signals is 89 days. There are 11 signal partitions present in the mask, which is lower than the total number of signals, thus there exist partitions with two or more signals. The partition rate, which is the number of partitions divided by the number of signals (see [SignalsAccessor.partition_rate](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.partition_rate)), is 44%, which is somewhat in the middle between 1 / 25 = 4% (all signals are contained in one big partition) and 25 / 25 = 100% (all partitions contain only one signal). This is then proved by the median partition length of 2 signals. The biggest streak of `True` values is 5 days. The minimum distance between each pair of partitions is just 1 `False` value (`[True, False, True]` yields a distance of 2). The biggest streak of `False` values is 89 days.

Since our `entries` mask exists relative to our `exits` mask, we can specify the second mask using the setting `other`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-1)>>> entries.vbt.signals.stats(column="BTCUSDT", settings=dict(target=exits))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-2)Start 2021-01-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-3)End 2021-12-31 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-4)Period 365 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-5)Total 25
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-6)Rate [%] 6.849315
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-7)Total Overlapping 1 << new
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-8)Overlapping Rate [%] 1.923077 << new
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-9)First Index 2021-04-10 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-10)Last Index 2021-12-27 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-11)Norm Avg Index [-1, 1] 0.159121
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-12)Distance -> Target: Min 0 days 00:00:00 << new
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-13)Distance -> Target: Median 49 days 00:00:00 << new
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-14)Distance -> Target: Max 66 days 00:00:00 << new
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-15)Total Partitions 11
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-16)Partition Rate [%] 44.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-17)Partition Length: Min 1 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-18)Partition Length: Median 2 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-19)Partition Length: Max 5 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-20)Partition Distance: Min 2 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-21)Partition Distance: Median 6 days 12:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-22)Partition Distance: Max 89 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#__codelineno-25-23)Name: BTCUSDT, dtype: object
 
[/code]

This produced three more metrics: the number of overlapping signals in both masks, the same number but in relation to the total number of signals in both masks (in %), and the distribution of the distance from each entry to the next exit up to the next entry signal. For instance, we see that there is only one signal that exists at the same timestamp in both masks. This is also confirmed by the minimum pairwise distance of 0 days between entries and exits. What's interesting: at least 50% of the time we're more than 49 days in the market.


# Summary[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development/pre-analysis/#summary "Permanent link")

Most trading strategies can be easily decomposed into a set of primitive conditions, most of which can be easily implemented and even vectorized. And since each of those conditions is just a regular question that can be answered with "yes" or "no" (like _"is the bandwidth below 10%?"_), we can translate it into a mask - a boolean array where this question is addressed at each single timestamp. Combining the answers for all the questions means combining the entire masks using logical operations, which is both easy and hell of efficient. But why don't we simply define a trading strategy iteratively, like done by other software? Building each of those masks separately provides us with a unique opportunity to analyze the answers that our strategy produces, but also to assess the effectiveness of the questions themselves. Instead of treating our trading strategy like a black box and relying exclusively on simulation metrics such as Sharpe, we're able to analyze each logical component of our strategy even before passing the entire thing to the backtester - the ultimate portal to the world of data science ![🪞](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1fa9e.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/signal-development/pre-analysis.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/SignalDevelopment.ipynb)