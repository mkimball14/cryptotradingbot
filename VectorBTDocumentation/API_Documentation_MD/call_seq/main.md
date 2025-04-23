call_seq

#  call_seq module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/call_seq.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#vectorbtpro.portfolio.call_seq "Permanent link")

Functions for working with call sequence arrays.

* * *

## build_call_seq function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/call_seq.py#L61-L78 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#vectorbtpro.portfolio.call_seq.build_call_seq "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-0-1)build_call_seq(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-0-2)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-0-3)    group_lens,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-0-4)    call_seq_type=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-0-5))
    

Not compiled but faster version of [build_call_seq_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#vectorbtpro.portfolio.call_seq.build_call_seq_nb "vectorbtpro.portfolio.call_seq.build_call_seq_nb").

* * *

## build_call_seq_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/call_seq.py#L34-L53 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#vectorbtpro.portfolio.call_seq.build_call_seq_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-1-1)build_call_seq_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-1-2)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-1-3)    group_lens,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-1-4)    call_seq_type=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-1-5))
    

Build a new call sequence array.

* * *

## require_call_seq function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/call_seq.py#L56-L58 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#vectorbtpro.portfolio.call_seq.require_call_seq "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-2-1)require_call_seq(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-2-2)    call_seq
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-2-3))
    

Force the call sequence array to pass our requirements.

* * *

## shuffle_call_seq_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/call_seq.py#L23-L31 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#vectorbtpro.portfolio.call_seq.shuffle_call_seq_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-3-1)shuffle_call_seq_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-3-2)    call_seq,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-3-3)    group_lens
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/call_seq/#__codelineno-3-4))
    

Shuffle the call sequence array.
