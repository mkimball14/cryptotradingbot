array_

#  array_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_ "Permanent link")

Utilities for working with arrays.

* * *

## build_nan_mask function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L220-L230 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.build_nan_mask "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-0-1)build_nan_mask(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-0-2)    *arrs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-0-3))
    

Build a NaN mask out of one to multiple arrays via the OR rule.

* * *

## cast_to_max_precision function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L298-L344 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.cast_to_max_precision "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-1-1)cast_to_max_precision(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-1-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-1-3)    max_precision,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-1-4)    float_only=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-1-5)    check_bounds=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-1-6)    strict=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-1-7))
    

Cast an array to a maximum integer/floating precision.

Argument must be either an integer denoting the number of bits, or one of 'half', 'single', and 'double'.

* * *

## cast_to_min_precision function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L260-L295 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.cast_to_min_precision "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-2-1)cast_to_min_precision(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-2-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-2-3)    min_precision,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-2-4)    float_only=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-2-5))
    

Cast an array to a minimum integer/floating precision.

Argument must be either an integer denoting the number of bits, or one of 'half', 'single', and 'double'.

* * *

## get_ranges_arr function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L67-L83 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.get_ranges_arr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-3-1)get_ranges_arr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-3-2)    starts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-3-3)    ends
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-3-4))
    

Build array from start and end indices.

Based on <https://stackoverflow.com/a/37626057>

* * *

## hash_int_rows_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L183-L198 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.hash_int_rows_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-4-1)hash_int_rows_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-4-2)    arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-4-3))
    

Hash rows in a 2-dim array.

First digits of each hash correspond to the left-most column, the last digits to the right-most column. Thus, the resulting hashes are not suitable for sorting by value.

* * *

## index_repeating_rows_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L201-L217 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.index_repeating_rows_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-5-1)index_repeating_rows_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-5-2)    arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-5-3))
    

Index repeating rows using monotonically increasing numbers.

* * *

## insert_argsort_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L50-L64 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.insert_argsort_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-6-1)insert_argsort_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-6-2)    A,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-6-3)    I
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-6-4))
    

Perform argsort using insertion sort.

In-memory and without recursion -> very fast for smaller arrays.

* * *

## int_digit_count_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L173-L180 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.int_digit_count_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-7-1)int_digit_count_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-7-2)    number
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-7-3))
    

Get the digit count in a number.

* * *

## is_range function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L36-L38 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.is_range "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-8-1)is_range(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-8-2)    arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-8-3))
    

Checks if array is arr range.

* * *

## is_range_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L41-L47 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.is_range_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-9-1)is_range_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-9-2)    arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-9-3))
    

Numba-compiled version of [is_range](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.is_range "vectorbtpro.utils.array_.is_range").

* * *

## is_sorted function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L22-L24 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.is_sorted "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-10-1)is_sorted(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-10-2)    arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-10-3))
    

Checks if array is sorted.

* * *

## is_sorted_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L27-L33 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.is_sorted_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-11-1)is_sorted_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-11-2)    arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-11-3))
    

Numba-compiled version of [is_sorted](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.is_sorted "vectorbtpro.utils.array_.is_sorted").

* * *

## max_count_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L363-L376 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.max_count_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-12-1)max_count_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-12-2)    arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-12-3))
    

Get the first position, the value, and the count of the array's maximum.

* * *

## max_rel_rescale function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L145-L160 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.max_rel_rescale "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-13-1)max_rel_rescale(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-13-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-13-3)    to_range
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-13-4))
    

Rescale elements in `arr` relatively to maximum.

* * *

## min_count_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L347-L360 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.min_count_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-14-1)min_count_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-14-2)    arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-14-3))
    

Get the first position, the value, and the count of the array's minimum.

* * *

## min_rel_rescale function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L127-L142 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.min_rel_rescale "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-15-1)min_rel_rescale(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-15-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-15-3)    to_range
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-15-4))
    

Rescale elements in `arr` relatively to minimum.

* * *

## rescale function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L100-L110 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.rescale "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-16-1)rescale(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-16-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-16-3)    from_range,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-16-4)    to_range
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-16-5))
    

Renormalize `arr` from one range to another.

* * *

## rescale_float_to_int_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L163-L170 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.rescale_float_to_int_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-17-1)rescale_float_to_int_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-17-2)    floats,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-17-3)    int_range,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-17-4)    total
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-17-5))
    

Rescale a float array into an int array.

* * *

## rescale_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L113-L124 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.rescale_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-18-1)rescale_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-18-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-18-3)    from_range,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-18-4)    to_range
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-18-5))
    

Numba-compiled version of [rescale](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.rescale "vectorbtpro.utils.array_.rescale").

* * *

## squeeze_nan function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L233-L241 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.squeeze_nan "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-19-1)squeeze_nan(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-19-2)    *arrs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-19-3)    nan_mask=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-19-4))
    

Squeeze NaN values using a mask.

* * *

## uniform_summing_to_one_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L86-L97 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.uniform_summing_to_one_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-20-1)uniform_summing_to_one_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-20-2)    n
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-20-3))
    

Generate random floats summing to one.

See # <https://stackoverflow.com/a/2640067/8141780>

* * *

## unsqueeze_nan function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/array_.py#L244-L257 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.unsqueeze_nan "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-21-1)unsqueeze_nan(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-21-2)    *arrs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-21-3)    nan_mask=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#__codelineno-21-4))
    

Un-squeeze NaN values using a mask.
