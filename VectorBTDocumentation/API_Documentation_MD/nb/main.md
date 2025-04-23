nb numba

#  nb module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb "Permanent link")

Numba-compiled functions for signals.

Provides an arsenal of Numba-compiled functions that are used by accessors and in many other parts of the backtesting pipeline, such as technical indicators. These only accept NumPy arrays and other Numba-compatible types.

Note

vectorbt treats matrices as first-class citizens and expects input arrays to be 2-dim, unless function has suffix `_1d` or is meant to be input to another function. Data is processed along index (axis 0).

All functions passed as argument must be Numba-compiled.

* * *

## between_partition_ranges_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1434-L1465 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_partition_ranges_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-0-1)between_partition_ranges_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-0-2)    mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-0-3))
    

Create a record of type [range_dt](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.range_dt "vectorbtpro.generic.enums.range_dt") for each range between two partitions in `mask`.

* * *

## between_ranges_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1302-L1336 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_ranges_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-1-1)between_ranges_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-1-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-1-3)    incl_open=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-1-4))
    

Create a record of type [range_dt](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.range_dt "vectorbtpro.generic.enums.range_dt") for each range between two signals in `mask`.

* * *

## between_two_ranges_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1339-L1387 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.between_two_ranges_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-2-1)between_two_ranges_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-2-2)    source_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-2-3)    target_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-2-4)    relation=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-2-5)    incl_open=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-2-6))
    

Create a record of type [range_dt](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.range_dt "vectorbtpro.generic.enums.range_dt") for each range between a source and target mask.

Index pairs are resolved with [relation_idxs_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.relation_idxs_1d_nb "vectorbtpro.signals.nb.relation_idxs_1d_nb").

* * *

## clean_enex_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1001-L1044 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.clean_enex_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-3-1)clean_enex_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-3-2)    entries,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-3-3)    exits,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-3-4)    force_first=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-3-5)    keep_conflicts=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-3-6)    reverse_order=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-3-7))
    

Clean entry and exit arrays by picking the first signal out of each.

Set `force_first` to True to force placing the first entry/exit before the first exit/entry. Set `keep_conflicts` to True to process signals at the same timestamp sequentially instead of removing them. Set `reverse_order` to True to reverse the order of signals.

* * *

## clean_enex_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1047-L1078 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.clean_enex_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-4-1)clean_enex_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-4-2)    entries,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-4-3)    exits,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-4-4)    force_first=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-4-5)    keep_conflicts=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-4-6)    reverse_order=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-4-7))
    

2-dim version of [clean_enex_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.clean_enex_1d_nb "vectorbtpro.signals.nb.clean_enex_1d_nb").

* * *

## distance_from_last_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L946-L981 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.distance_from_last_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-5-1)distance_from_last_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-5-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-5-3)    nth=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-5-4))
    

Distance from the last n-th True value to the current value.

Unless `nth` is zero, the current True value isn't counted as one of the last True values.

* * *

## distance_from_last_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L984-L995 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.distance_from_last_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-6-1)distance_from_last_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-6-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-6-3)    nth=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-6-4))
    

2-dim version of [distance_from_last_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.distance_from_last_1d_nb "vectorbtpro.signals.nb.distance_from_last_1d_nb").

* * *

## first_place_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L490-L499 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.first_place_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-7-1)first_place_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-7-2)    c,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-7-3)    mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-7-4))
    

`place_func_nb` that keeps only the first signal in `mask`.

* * *

## generate_enex_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L210-L327 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_enex_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-1)generate_enex_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-2)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-3)    entry_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-4)    entry_place_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-5)    exit_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-6)    exit_place_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-7)    entry_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-8)    exit_wait=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-8-9))
    

Place entry signals using `entry_place_func_nb` and exit signals using `exit_place_func_nb` one after another.

**Args**

**`target_shape`** : `array`
    Target shape.
**`entry_place_func_nb`** : `callable`
    

Entry place function.

`entry_place_func_nb` must accept a context of type [GenEnExContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext "vectorbtpro.signals.enums.GenEnExContext"), and return the index of the last signal (-1 to break the loop).

**`entry_place_args`** : `tuple`
    Arguments unpacked and passed to `entry_place_func_nb`.
**`exit_place_func_nb`** : `callable`
    

Exit place function.

`exit_place_func_nb` must accept a context of type [GenEnExContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext "vectorbtpro.signals.enums.GenEnExContext"), and return the index of the last signal (-1 to break the loop).

**`exit_place_args`** : `tuple`
    Arguments unpacked and passed to `exit_place_func_nb`.
**`entry_wait`** : `int`
    

Number of ticks to wait before placing entries.

Note

Setting `entry_wait` to 0 or False assumes that both entry and exit can be processed within the same bar, and exit can be processed before entry.

**`exit_wait`** : `int`
    

Number of ticks to wait before placing exits.

Note

Setting `exit_wait` to 0 or False assumes that both entry and exit can be processed within the same bar, and entry can be processed before exit.

* * *

## generate_ex_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L114-L207 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_ex_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-9-1)generate_ex_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-9-2)    entries,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-9-3)    exit_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-9-4)    exit_place_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-9-5)    wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-9-6)    until_next=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-9-7)    skip_until_exit=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-9-8))
    

Place exit signals using `exit_place_func_nb` after each signal in `entries`.

**Args**

**`entries`** : `array`
    Boolean array with entry signals.
**`exit_place_func_nb`** : `callable`
    

Exit place function.

`exit_place_func_nb` must accept a context of type [GenExContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext "vectorbtpro.signals.enums.GenExContext"), and return the index of the last signal (-1 to break the loop).

**`exit_place_args`** : `callable`
    Arguments passed to `exit_place_func_nb`.
**`wait`** : `int`
    

Number of ticks to wait before placing exits.

Note

Setting `wait` to 0 or False may result in two signals at one bar.

**`until_next`** : `int`
    

Whether to place signals up to the next entry signal.

Note

Setting it to False makes it difficult to tell which exit belongs to which entry.

**`skip_until_exit`** : `bool`
    

Whether to skip processing entry signals until the next exit.

Has only effect when `until_next` is disabled.

Note

Setting it to True makes it impossible to tell which exit belongs to which entry.

* * *

## generate_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L47-L111 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-10-1)generate_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-10-2)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-10-3)    place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-10-4)    place_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-10-5)    only_once=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-10-6)    wait=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-10-7))
    

Create a boolean matrix of `target_shape` and place signals using `place_func_nb`.

**Args**

**`target_shape`** : `array`
    Target shape.
**`place_func_nb`** : `callable`
    

Signal placement function.

`place_func_nb` must accept a context of type [GenEnContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext "vectorbtpro.signals.enums.GenEnContext"), and return the index of the last signal (-1 to break the loop).

**`place_args`**
    Arguments passed to `place_func_nb`.
**`only_once`** : `bool`
    Whether to run the placement function only once.
**`wait`** : `int`
    Number of ticks to wait before placing the next entry.

Note

The first argument is always a 1-dimensional boolean array that contains only those elements where signals can be placed. The range and column indices only describe which range this array maps to.

* * *

## generate_rand_enex_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L370-L474 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_rand_enex_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-11-1)generate_rand_enex_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-11-2)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-11-3)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-11-4)    entry_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-11-5)    exit_wait=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-11-6))
    

Pick a number of entries and the same number of exits one after another.

Respects `entry_wait` and `exit_wait` constraints through a number of tricks. Tries to mimic a uniform distribution as much as possible.

The idea is the following: with constraints, there is some fixed amount of total space required between first entry and last exit. Upscale this space in a way that distribution of entries and exit is similar to a uniform distribution. This means randomizing the position of first entry, last exit, and all signals between them.

`n` uses flexible indexing and thus must be at least a 0-dim array.

* * *

## norm_avg_index_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1763-L1767 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.norm_avg_index_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-12-1)norm_avg_index_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-12-2)    mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-12-3))
    

Get mean index normalized to (-1, 1).

* * *

## norm_avg_index_grouped_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1784-L1810 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.norm_avg_index_grouped_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-13-1)norm_avg_index_grouped_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-13-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-13-3)    group_lens
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-13-4))
    

Grouped version of [norm_avg_index_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.norm_avg_index_nb "vectorbtpro.signals.nb.norm_avg_index_nb").

* * *

## norm_avg_index_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1770-L1781 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.norm_avg_index_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-14-1)norm_avg_index_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-14-2)    mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-14-3))
    

2-dim version of [norm_avg_index_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.norm_avg_index_1d_nb "vectorbtpro.signals.nb.norm_avg_index_1d_nb").

* * *

## nth_index_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1726-L1746 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.nth_index_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-15-1)nth_index_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-15-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-15-3)    n
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-15-4))
    

Get the index of the n-th True value.

Note

`n` starts with 0 and can be negative.

* * *

## nth_index_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1749-L1760 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.nth_index_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-16-1)nth_index_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-16-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-16-3)    n
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-16-4))
    

2-dim version of [nth_index_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.nth_index_1d_nb "vectorbtpro.signals.nb.nth_index_1d_nb").

* * *

## ohlc_stop_place_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L600-L811 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.ohlc_stop_place_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-1)ohlc_stop_place_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-2)    c,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-3)    entry_price,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-4)    open,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-5)    high,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-6)    low,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-7)    close,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-8)    stop_price_out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-9)    stop_type_out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-10)    sl_stop,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-11)    tsl_th,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-12)    tsl_stop,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-13)    tp_stop,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-14)    reverse,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-15)    is_entry_open=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-17-16))
    

`place_func_nb` that places an exit signal whenever a threshold is being hit using OHLC.

Compared to [stop_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.stop_place_nb "vectorbtpro.signals.nb.stop_place_nb"), takes into account the whole bar, can check for both (trailing) stop loss and take profit simultaneously, and tracks hit price and stop type.

Note

Waiting time cannot be higher than 1.

**Args**

**`c`** : `GenExContext` or `GenEnExContext`
    Signal context.
**`entry_price`** : `array` of `float`
    

Entry price.

Utilizes flexible indexing.

**`open`** : `array` of `float`
    

Open price.

Utilizes flexible indexing. If Nan and `is_entry_open` is True, defaults to entry price.

**`high`** : `array` of `float`
    

High price.

Utilizes flexible indexing. If NaN, gets calculated from open and close.

**`low`** : `array` of `float`
    

Low price.

Utilizes flexible indexing. If NaN, gets calculated from open and close.

**`close`** : `array` of `float`
    

Close price.

Utilizes flexible indexing. If Nan and `is_entry_open` is False, defaults to entry price.

**`stop_price_out`** : `array` of `float`
    

Array where hit price of each exit will be stored.

Must be of the full shape.

**`stop_type_out`** : `array` of `int`
    

Array where stop type of each exit will be stored.

Must be of the full shape. 0 for stop loss, 1 for take profit.

**`sl_stop`** : `array` of `float`
    

Stop loss as a percentage.

Utilizes flexible indexing. Set an element to `np.nan` to disable.

**`tsl_th`** : `array` of `float`
    

Take profit threshold as a percentage for the trailing stop loss.

Utilizes flexible indexing. Set an element to `np.nan` to disable.

**`tsl_stop`** : `array` of `float`
    

Trailing stop loss as a percentage for the trailing stop loss.

Utilizes flexible indexing. Set an element to `np.nan` to disable.

**`tp_stop`** : `array` of `float`
    

Take profit as a percentage.

Utilizes flexible indexing. Set an element to `np.nan` to disable.

**`reverse`** : `array` of `float`
    

Whether to do the opposite, i.e.: prices are followed downwards.

Utilizes flexible indexing.

**`is_entry_open`** : `bool`
    

Whether entry price comes right at or before open.

If True, uses high and low of the entry bar. Otherwise, uses only close.

* * *

## part_pos_rank_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L935-L940 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.part_pos_rank_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-18-1)part_pos_rank_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-18-2)    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-18-3))
    

`rank_func_nb` that returns the rank of each partition by its position in the series.

Resets at each reset signal.

* * *

## partition_ranges_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1390-L1431 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.partition_ranges_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-19-1)partition_ranges_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-19-2)    mask
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-19-3))
    

Create a record of type [range_dt](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.range_dt "vectorbtpro.generic.enums.range_dt") for each partition of signals in `mask`.

* * *

## rand_by_prob_place_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L351-L367 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rand_by_prob_place_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-20-1)rand_by_prob_place_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-20-2)    c,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-20-3)    prob,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-20-4)    pick_first=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-20-5))
    

`place_func_nb` to randomly place signals with probability `prob`.

`prob` uses flexible indexing.

* * *

## rand_enex_apply_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L477-L484 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rand_enex_apply_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-21-1)rand_enex_apply_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-21-2)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-21-3)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-21-4)    entry_wait=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-21-5)    exit_wait=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-21-6))
    

`apply_func_nb` that calls [generate_rand_enex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_rand_enex_nb "vectorbtpro.signals.nb.generate_rand_enex_nb").

* * *

## rand_place_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L333-L348 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rand_place_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-22-1)rand_place_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-22-2)    c,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-22-3)    n
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-22-4))
    

`place_func_nb` to randomly pick `n` values.

`n` uses flexible indexing.

* * *

## rank_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L817-L921 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.rank_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-1)rank_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-3)    rank_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-4)    rank_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-5)    reset_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-6)    after_false=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-7)    after_reset=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-8)    reset_wait=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-23-9))
    

Rank each signal using `rank_func_nb`.

Applies `rank_func_nb` on each True value. Must accept a context of type [RankContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext "vectorbtpro.signals.enums.RankContext"). Must return -1 for no rank, otherwise 0 or greater.

Setting `after_false` to True will disregard the first partition of True values if there is no False value before them. Setting `after_reset` to True will disregard the first partition of True values coming before the first reset signal. Setting `reset_wait` to 0 will treat the signal at the same position as the reset signal as the first signal in the next partition. Setting it to 1 will treat it as the last signal in the previous partition.

* * *

## ravel_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1705-L1720 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.ravel_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-24-1)ravel_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-24-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-24-3)    group_map
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-24-4))
    

Ravel True values of each group into a separate column.

* * *

## relation_idxs_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1084-L1296 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.relation_idxs_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-25-1)relation_idxs_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-25-2)    source_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-25-3)    target_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-25-4)    relation=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-25-5))
    

Get index pairs of True values between a source and target mask.

For `relation`, see [SignalRelation](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.SignalRelation "vectorbtpro.signals.enums.SignalRelation").

Note

If both True values happen at the same time, source signal is assumed to come first.

* * *

## sig_pos_rank_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L924-L932 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.sig_pos_rank_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-26-1)sig_pos_rank_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-26-2)    c,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-26-3)    allow_gaps
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-26-4))
    

`rank_func_nb` that returns the rank of each signal by its position in the partition if `allow_gaps` is False, otherwise globally.

Resets at each reset signal.

* * *

## stop_place_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L502-L597 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.stop_place_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-1)stop_place_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-2)    c,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-3)    entry_ts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-4)    ts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-5)    follow_ts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-6)    stop_ts_out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-7)    stop,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-8)    trailing
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-27-9))
    

`place_func_nb` that places an exit signal whenever a threshold is being hit.

Note

Waiting time cannot be higher than 1.

If waiting time is 0, `entry_ts` should be the first value in the bar. If waiting time is 1, `entry_ts` should be the last value in the bar.

**Args**

**`c`** : `GenExContext` or `GenEnExContext`
    Signal context.
**`entry_ts`** : `array` of `float`
    

Entry price.

Utilizes flexible indexing.

**`ts`** : `array` of `float`
    

Price to compare the stop value against.

Utilizes flexible indexing. If NaN, defaults to `entry_ts`.

**`follow_ts`** : `array` of `float`
    

Following price.

Utilizes flexible indexing. If NaN, defaults to `ts`. Applied only if the stop is trailing.

**`stop_ts_out`** : `array` of `float`
    

Array where hit price of each exit will be stored.

Must be of the full shape.

**`stop`** : `array` of `float`
    

Stop value.

Utilizes flexible indexing. Set an element to `np.nan` to disable it.

**`trailing`** : `array` of `bool`
    

Whether the stop is trailing.

Utilizes flexible indexing. Set an element to False to disable it.

* * *

## unravel_between_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1526-L1598 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.unravel_between_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-28-1)unravel_between_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-28-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-28-3)    incl_open_source=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-28-4)    incl_empty_cols=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-28-5))
    

Unravel each pair of successive True values in a mask to a separate column.

Returns the new mask, the index of each source True value in its column, the index of each target True value in its column, the row index of each source True value in the original mask, the row index of each target True value in the original mask, and the column index of each True value in the original mask.

* * *

## unravel_between_two_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1601-L1702 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.unravel_between_two_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-29-1)unravel_between_two_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-29-2)    source_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-29-3)    target_mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-29-4)    relation=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-29-5)    incl_open_source=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-29-6)    incl_open_target=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-29-7)    incl_empty_cols=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-29-8))
    

Unravel each pair of successive True values between a source and target mask to a separate column.

Index pairs are resolved with [relation_idxs_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.relation_idxs_1d_nb "vectorbtpro.signals.nb.relation_idxs_1d_nb").

Returns the new source mask, the new target mask, the index of each source True value in its column, the index of each target True value in its column, the row index of each True value in each original mask, and the column index of each True value in both original masks.

* * *

## unravel_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/nb.py#L1471-L1523 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.unravel_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-30-1)unravel_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-30-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-30-3)    incl_empty_cols=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#__codelineno-30-4))
    

Unravel each True value in a mask to a separate column.

Returns the new mask, the index of each True value in its column, the row index of each True value in its column, and the column index of each True value in the original mask.
