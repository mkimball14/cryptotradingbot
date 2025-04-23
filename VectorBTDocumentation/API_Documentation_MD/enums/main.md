enums

#  enums module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums "Permanent link")

Named tuples and enumerated types for signals.

Defines enums and other schemas for [vectorbtpro.signals](https://vectorbt.pro/pvt_7a467f6b/api/signals/ "vectorbtpro.signals").

* * *

## FactoryMode namedtuple[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.FactoryMode "Permanent link")

Factory mode.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-0-1)FactoryModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-0-2)    Entries=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-0-3)    Exits=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-0-4)    Both=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-0-5)    Chain=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-0-6))
    

**Attributes**

**`Entries`**
    

Generate entries only using `generate_func_nb`.

Takes no input signal arrays. Produces one output signal array - `entries`.

Such generators often have no suffix.

**`Exits`**
    

Generate exits only using `generate_ex_func_nb`.

Takes one input signal array - `entries`. Produces one output signal array - `exits`.

Such generators often have suffix 'X'.

**`Both`**
    

Generate both entries and exits using `generate_enex_func_nb`.

Takes no input signal arrays. Produces two output signal arrays - `entries` and `exits`.

Such generators often have suffix 'NX'.

**`Chain`**
    

Generate chain of entries and exits using `generate_enex_func_nb`.

Takes one input signal array - `entries`. Produces two output signal arrays - `new_entries` and `exits`.

Such generators often have suffix 'CX'.

* * *

## SignalRelation namedtuple[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.SignalRelation "Permanent link")

SignalRelation between two masks.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-1-1)SignalRelationT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-1-2)    OneOne=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-1-3)    OneMany=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-1-4)    ManyOne=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-1-5)    ManyMany=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-1-6)    Chain=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-1-7)    AnyChain=5
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-1-8))
    

**Attributes**

**`OneOne`**
    One source signal maps to exactly one succeeding target signal.
**`OneMany`**
    One source signal can map to one or more succeeding target signals.
**`ManyOne`**
    One or more source signals can map to exactly one succeeding target signal.
**`ManyMany`**
    One or more source signals can map to one or more succeeding target signals.
**`Chain`**
    First source signal maps to the first target signal after it and vice versa.
**`AnyChain`**
    First signal maps to the first opposite signal after it and vice versa.

* * *

## StopType namedtuple[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.StopType "Permanent link")

Stop type.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-2-1)StopTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-2-2)    SL=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-2-3)    TSL=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-2-4)    TTP=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-2-5)    TP=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-2-6)    TD=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-2-7)    DT=5
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-2-8))
    

* * *

## GenEnContext class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py#L135-L143 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-1)GenEnContext(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-2)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-3)    only_once,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-4)    wait,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-5)    entries_out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-6)    out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-7)    from_i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-8)    to_i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-9)    col
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-3-10))
    

Context of an entry signal generator.

**Superclasses**

  * `builtins.tuple`



* * *

### col field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext.col "Permanent link")

Column of the segment.

* * *

### entries_out field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext.entries_out "Permanent link")

Output array with entries.

* * *

### from_i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext.from_i "Permanent link")

Start index of the segment (inclusive).

* * *

### only_once field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext.only_once "Permanent link")

Whether to run the placement function only once.

* * *

### out field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext.out "Permanent link")

Current segment of the output array with entries.

* * *

### target_shape field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext.target_shape "Permanent link")

Target shape.

* * *

### to_i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext.to_i "Permanent link")

End index of the segment (exclusive).

* * *

### wait field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext.wait "Permanent link")

Number of ticks to wait before placing the next entry.

* * *

## GenEnExContext class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py#L181-L192 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-1)GenEnExContext(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-2)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-3)    entry_wait,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-4)    exit_wait,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-5)    entries_out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-6)    exits_out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-7)    entries_turn,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-8)    wait,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-9)    out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-10)    from_i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-11)    to_i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-12)    col
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-4-13))
    

GenEnExContext(target_shape, entry_wait, exit_wait, entries_out, exits_out, entries_turn, wait, out, from_i, to_i, col)

**Superclasses**

  * `builtins.tuple`



* * *

### col field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.col "Permanent link")

Alias for field number 10

* * *

### entries_out field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.entries_out "Permanent link")

Alias for field number 3

* * *

### entries_turn field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.entries_turn "Permanent link")

Alias for field number 5

* * *

### entry_wait field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.entry_wait "Permanent link")

Alias for field number 1

* * *

### exit_wait field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.exit_wait "Permanent link")

Alias for field number 2

* * *

### exits_out field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.exits_out "Permanent link")

Alias for field number 4

* * *

### from_i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.from_i "Permanent link")

Alias for field number 8

* * *

### out field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.out "Permanent link")

Alias for field number 7

* * *

### target_shape field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.target_shape "Permanent link")

Alias for field number 0

* * *

### to_i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.to_i "Permanent link")

Alias for field number 9

* * *

### wait field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnExContext.wait "Permanent link")

Alias for field number 6

* * *

## GenExContext class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py#L157-L166 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-1)GenExContext(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-2)    entries,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-3)    until_next,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-4)    skip_until_exit,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-5)    exits_out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-6)    out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-7)    wait,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-8)    from_i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-9)    to_i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-10)    col
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-5-11))
    

Context of an entry/exit signal generator.

**Superclasses**

  * `builtins.tuple`



* * *

### col field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.col "Permanent link")

Column of the segment.

* * *

### entries field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.entries "Permanent link")

Input array with entries.

* * *

### exits_out field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.exits_out "Permanent link")

Output array with exits.

* * *

### from_i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.from_i "Permanent link")

Start index of the segment (inclusive).

* * *

### out field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.out "Permanent link")

Current segment of the output array with entries/exits.

* * *

### skip_until_exit field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.skip_until_exit "Permanent link")

Whether to skip processing entry signals until the next exit.

* * *

### to_i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.to_i "Permanent link")

End index of the segment (exclusive).

* * *

### until_next field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.until_next "Permanent link")

Whether to place signals up to the next entry signal.

* * *

### wait field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenExContext.wait "Permanent link")

Number of ticks to wait before placing entries/exits.

* * *

## RankContext class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py#L209-L227 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-1)RankContext(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-3)    reset_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-4)    after_false,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-5)    after_reset,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-6)    reset_wait,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-7)    col,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-8)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-9)    last_false_i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-10)    last_reset_i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-11)    all_sig_cnt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-12)    all_part_cnt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-13)    all_sig_in_part_cnt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-14)    nonres_sig_cnt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-15)    nonres_part_cnt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-16)    nonres_sig_in_part_cnt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-17)    sig_cnt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-18)    part_cnt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-19)    sig_in_part_cnt
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#__codelineno-6-20))
    

Context of a ranker.

**Superclasses**

  * `builtins.tuple`



* * *

### after_false field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.after_false "Permanent link")

Whether to disregard the first partition of True values if there is no False value before them.

* * *

### after_reset field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.after_reset "Permanent link")

Whether to disregard the first partition of True values coming before the first reset signal.

* * *

### all_part_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.all_part_cnt "Permanent link")

Number of all partitions encountered including this.

* * *

### all_sig_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.all_sig_cnt "Permanent link")

Number of all signals encountered including this.

* * *

### all_sig_in_part_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.all_sig_in_part_cnt "Permanent link")

Number of signals encountered in the current partition including this.

* * *

### col field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.col "Permanent link")

Current column.

* * *

### i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.i "Permanent link")

Current row.

* * *

### last_false_i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.last_false_i "Permanent link")

Row of the last False value in the main mask.

* * *

### last_reset_i field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.last_reset_i "Permanent link")

Row of the last True value in the resetting mask. 

Doesn't take into account `reset_wait`.

* * *

### mask field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.mask "Permanent link")

Source mask.

* * *

### nonres_part_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.nonres_part_cnt "Permanent link")

Number of non-resetting partitions encountered including this.

* * *

### nonres_sig_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.nonres_sig_cnt "Permanent link")

Number of non-resetting signals encountered including this.

* * *

### nonres_sig_in_part_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.nonres_sig_in_part_cnt "Permanent link")

Number of signals encountered in the current non-resetting partition including this.

* * *

### part_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.part_cnt "Permanent link")

Number of valid and resetting partitions encountered including this.

* * *

### reset_by field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.reset_by "Permanent link")

Resetting mask.

* * *

### reset_wait field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.reset_wait "Permanent link")

Number of ticks to wait before resetting the current partition.

* * *

### sig_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.sig_cnt "Permanent link")

Number of valid and resetting signals encountered including this.

* * *

### sig_in_part_cnt field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/enums.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext.sig_in_part_cnt "Permanent link")

Number of signals encountered in the current valid and resetting partition including this.
