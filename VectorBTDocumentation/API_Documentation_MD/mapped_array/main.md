mapped_array

#  mapped_array module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array "Permanent link")

Base class for working with mapped arrays.

This class takes the mapped array and the corresponding column and (optionally) index arrays, and offers features to directly process the mapped array without converting it to pandas; for example, to compute various statistics by column, such as standard deviation.

Consider the following example:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-0-3)>>> a = np.array([10., 11., 12., 13., 14., 15., 16., 17., 18.])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-0-4)>>> col_arr = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-0-5)>>> idx_arr = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-0-6)>>> wrapper = vbt.ArrayWrapper(index=['x', 'y', 'z'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-0-7)...     columns=['a', 'b', 'c'], ndim=2, freq='1 day')
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-0-8)>>> ma = vbt.MappedArray(wrapper, a, col_arr, idx_arr=idx_arr)
    

## Reducing[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#reducing "Permanent link")

Using [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray"), we can then reduce by column as follows:

  * Use already provided reducers such as [MappedArray.mean](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.mean "vectorbtpro.records.mapped_array.MappedArray.mean"):


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-1-1)>>> ma.mean()
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-1-2)a    11.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-1-3)b    14.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-1-4)c    17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-1-5)dtype: float64
    

  * Use [MappedArray.to_pd](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_pd "vectorbtpro.records.mapped_array.MappedArray.to_pd") to map to pandas and then reduce manually (expensive):


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-2-1)>>> ma.to_pd().mean()
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-2-2)a    11.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-2-3)b    14.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-2-4)c    17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-2-5)dtype: float64
    

  * Use [MappedArray.reduce](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.reduce "vectorbtpro.records.mapped_array.MappedArray.reduce") to reduce using a custom function:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-1)>>> # Reduce to a scalar
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-3)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-4)... def pow_mean_reduce_nb(a, pow):
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-5)...     return np.mean(a ** pow)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-7)>>> ma.reduce(pow_mean_reduce_nb, 2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-8)a    121.666667
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-9)b    196.666667
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-10)c    289.666667
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-11)dtype: float64
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-13)>>> # Reduce to an array
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-15)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-16)... def min_max_reduce_nb(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-17)...     return np.array([np.min(a), np.max(a)])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-18)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-19)>>> ma.reduce(min_max_reduce_nb, returns_array=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-20)...     wrap_kwargs=dict(name_or_index=['min', 'max']))
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-21)        a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-22)min  10.0  13.0  16.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-23)max  12.0  15.0  18.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-24)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-25)>>> # Reduce to an array of indices
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-27)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-28)... def idxmin_idxmax_reduce_nb(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-29)...     return np.array([np.argmin(a), np.argmax(a)])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-30)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-31)>>> ma.reduce(idxmin_idxmax_reduce_nb, returns_array=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-32)...     returns_idx=True, wrap_kwargs=dict(name_or_index=['idxmin', 'idxmax']))
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-33)        a  b  c
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-34)idxmin  x  x  x
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-35)idxmax  z  z  z
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-36)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-37)>>> # Reduce using a meta function to combine multiple mapped arrays
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-38)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-39)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-40)... def mean_ratio_reduce_meta_nb(idxs, col, a, b):
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-41)...     return np.mean(a[idxs]) / np.mean(b[idxs])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-42)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-43)>>> vbt.MappedArray.reduce(mean_ratio_reduce_meta_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-44)...     ma.values - 1, ma.values + 1, col_mapper=ma.col_mapper)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-45)a    0.833333
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-46)b    0.866667
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-47)c    0.888889
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-3-48)Name: reduce, dtype: float64
    

## Mapping[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#mapping "Permanent link")

Use [MappedArray.apply](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.apply "vectorbtpro.records.mapped_array.MappedArray.apply") to apply a function on each column/group:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-1)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-2)... def cumsum_apply_nb(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-3)...     return np.cumsum(a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-5)>>> ma.apply(cumsum_apply_nb)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-6)<vectorbtpro.records.mapped_array.MappedArray at 0x7ff061382198>
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-8)>>> ma.apply(cumsum_apply_nb).values
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-9)array([10., 21., 33., 13., 27., 42., 16., 33., 51.])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-11)>>> group_by = np.array(['first', 'first', 'second'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-12)>>> ma.apply(cumsum_apply_nb, group_by=group_by, apply_per_group=True).values
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-13)array([10., 21., 33., 46., 60., 75., 16., 33., 51.])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-15)>>> # Apply using a meta function
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-16)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-17)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-18)... def cumsum_apply_meta_nb(ridxs, col, a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-19)...     return np.cumsum(a[ridxs])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-21)>>> vbt.MappedArray.apply(cumsum_apply_meta_nb, ma.values, col_mapper=ma.col_mapper).values
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-4-22)array([10., 21., 33., 13., 27., 42., 16., 33., 51.])
    

Notice how cumsum resets at each column in the first example and at each group in the second example.

## Conversion[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#conversion "Permanent link")

We can unstack any [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") instance to pandas:

  * Given `idx_arr` was provided:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-5-1)>>> ma.to_pd()
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-5-2)      a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-5-3)x  10.0  13.0  16.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-5-4)y  11.0  14.0  17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-5-5)z  12.0  15.0  18.0
    

Note

Will throw a warning if there are multiple values pointing to the same position.

  * In case `group_by` was provided, index can be ignored, or there are position conflicts:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-6-1)>>> ma.to_pd(group_by=np.array(['first', 'first', 'second']), ignore_index=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-6-2)   first  second
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-6-3)0   10.0    16.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-6-4)1   11.0    17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-6-5)2   12.0    18.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-6-6)3   13.0     NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-6-7)4   14.0     NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-6-8)5   15.0     NaN
    

## Resolving conflicts[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#resolving-conflicts "Permanent link")

Sometimes, we may encounter multiple values for each index and column combination. In such case, we can use [MappedArray.reduce_segments](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.reduce_segments "vectorbtpro.records.mapped_array.MappedArray.reduce_segments") to aggregate "duplicate" elements. For example, let's sum up duplicate values per each index and column combination:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-1)>>> ma_conf = ma.replace(idx_arr=np.array([0, 0, 0, 1, 1, 1, 2, 2, 2]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-2)>>> ma_conf.to_pd()
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-3)UserWarning: Multiple values are pointing to the same position. Only the latest value is used.
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-4)      a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-5)x  12.0   NaN   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-6)y   NaN  15.0   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-7)z   NaN   NaN  18.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-9)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-10)... def sum_reduce_nb(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-11)...     return np.sum(a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-13)>>> ma_no_conf = ma_conf.reduce_segments(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-14)...     (ma_conf.idx_arr, ma_conf.col_arr),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-15)...     sum_reduce_nb
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-16)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-17)>>> ma_no_conf.to_pd()
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-18)      a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-19)x  33.0   NaN   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-20)y   NaN  42.0   NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-7-21)z   NaN   NaN  51.0
    

## Filtering[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#filtering "Permanent link")

Use [MappedArray.apply_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.apply_mask "vectorbtpro.records.mapped_array.MappedArray.apply_mask") to filter elements per column/group:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-1)>>> mask = [True, False, True, False, True, False, True, False, True]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-2)>>> filtered_ma = ma.apply_mask(mask)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-3)>>> filtered_ma.count()
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-4)a    2
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-5)b    1
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-6)c    2
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-7)dtype: int64
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-9)>>> filtered_ma.id_arr
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-8-10)array([0, 2, 4, 6, 8])
    

## Grouping[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#grouping "Permanent link")

One of the key features of [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") is that we can perform reducing operations on a group of columns as if they were a single column. Groups can be specified by `group_by`, which can be anything from positions or names of column levels, to a NumPy array with actual groups.

There are multiple ways of define grouping:

  * When creating [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray"), pass `group_by` to [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper"):


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-9-1)>>> group_by = np.array(['first', 'first', 'second'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-9-2)>>> grouped_wrapper = wrapper.replace(group_by=group_by)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-9-3)>>> grouped_ma = vbt.MappedArray(grouped_wrapper, a, col_arr, idx_arr=idx_arr)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-9-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-9-5)>>> grouped_ma.mean()
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-9-6)first     12.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-9-7)second    17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-9-8)dtype: float64
    

  * Regroup an existing [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray"):


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-10-1)>>> ma.regroup(group_by).mean()
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-10-2)first     12.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-10-3)second    17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-10-4)dtype: float64
    

  * Pass `group_by` directly to the reducing method:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-11-1)>>> ma.mean(group_by=group_by)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-11-2)first     12.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-11-3)second    17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-11-4)dtype: float64
    

By the same way we can disable or modify any existing grouping:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-12-1)>>> grouped_ma.mean(group_by=False)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-12-2)a    11.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-12-3)b    14.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-12-4)c    17.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-12-5)dtype: float64
    

Note

Grouping applies only to reducing operations, there is no change to the arrays.

## Operators[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#operators "Permanent link")

[MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") implements arithmetic, comparison, and logical operators. We can perform basic operations (such as addition) on mapped arrays as if they were NumPy arrays.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-13-1)>>> ma ** 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-13-2)<vectorbtpro.records.mapped_array.MappedArray at 0x7f97bfc49358>
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-13-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-13-4)>>> ma * np.array([1, 2, 3, 4, 5, 6])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-13-5)<vectorbtpro.records.mapped_array.MappedArray at 0x7f97bfc65e80>
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-13-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-13-7)>>> ma + ma
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-13-8)<vectorbtpro.records.mapped_array.MappedArray at 0x7fd638004d30>
    

Note

Ensure that your [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") operand is on the left if the other operand is an array.

If two [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") operands have different metadata, will copy metadata from the first one, but at least their `id_arr` and `col_arr` must match.

## Indexing[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#indexing "Permanent link")

Like any other class subclassing [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping"), we can do pandas indexing on a [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") instance, which forwards indexing operation to each object with columns:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-14-1)>>> ma['a'].values
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-14-2)array([10., 11., 12.])
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-14-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-14-4)>>> grouped_ma['first'].values
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-14-5)array([10., 11., 12., 13., 14., 15.])
    

Note

Changing index (time axis) is not supported. The object should be treated as a Series rather than a DataFrame; for example, use `some_field.iloc[0]` instead of `some_field.iloc[:, 0]` to get the first column.

Indexing behavior depends solely upon [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper"). For example, if `group_select` is enabled indexing will be performed on groups, otherwise on single columns.

## Caching[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#caching "Permanent link")

[MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") supports caching. If a method or a property requires heavy computation, it's wrapped with [cached_method](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cached_method "vectorbtpro.utils.decorators.cached_method") and [cached_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cached_property "vectorbtpro.utils.decorators.cached_property") respectively. Caching can be disabled globally in [caching](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.caching "vectorbtpro._settings.caching").

Note

Because of caching, class is meant to be immutable and all properties are read-only. To change any attribute, use the [MappedArray.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.replace "vectorbtpro.records.mapped_array.MappedArray.replace") method and pass changes as keyword arguments.

## Saving and loading[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#saving-and-loading "Permanent link")

Like any other class subclassing [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable"), we can save a [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") instance to the disk with [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.records.mapped_array.MappedArray.save") and load it with [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.records.mapped_array.MappedArray.load").

## Stats[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#stats "Permanent link")

Hint

See [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats") and [MappedArray.metrics](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.metrics "vectorbtpro.records.mapped_array.MappedArray.metrics").

Metric for mapped arrays are similar to that for [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor "vectorbtpro.generic.accessors.GenericAccessor").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-1)>>> ma.stats(column='a')
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-2)Start                      x
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-3)End                        z
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-4)Period       3 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-5)Count                      3
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-6)Mean                    11.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-7)Std                      1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-8)Min                     10.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-9)Median                  11.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-10)Max                     12.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-11)Min Index                  x
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-12)Max Index                  z
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-15-13)Name: a, dtype: object
    

The main difference unfolds once the mapped array has a mapping: values are then considered as categorical and usual statistics are meaningless to compute. For this case, [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.records.mapped_array.MappedArray.stats") returns the value counts:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-1)>>> mapping = {v: "test_" + str(v) for v in np.unique(ma.values)}
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-2)>>> ma.stats(column='a', settings=dict(mapping=mapping))
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-3)Start                                    x
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-4)End                                      z
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-5)Period                     3 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-6)Count                                    3
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-7)Value Counts: test_10.0                  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-8)Value Counts: test_11.0                  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-9)Value Counts: test_12.0                  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-10)Value Counts: test_13.0                  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-11)Value Counts: test_14.0                  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-12)Value Counts: test_15.0                  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-13)Value Counts: test_16.0                  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-14)Value Counts: test_17.0                  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-15)Value Counts: test_18.0                  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-16-16)Name: a, dtype: object
    

[StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.records.mapped_array.MappedArray.stats") also supports (re-)grouping:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-1)>>> grouped_ma.stats(column='first')
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-2)Start                      x
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-3)End                        z
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-4)Period       3 days 00:00:00
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-5)Count                      6
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-6)Mean                    12.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-7)Std                 1.870829
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-8)Min                     10.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-9)Median                  12.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-10)Max                     15.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-11)Min Index                  x
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-12)Max Index                  z
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-17-13)Name: first, dtype: object
    

## Plots[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#plots "Permanent link")

We can build histograms and boxplots of [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") directly:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-18-1)>>> ma.boxplot().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/mapped_boxplot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/mapped_boxplot.dark.svg#only-dark)

To use scatterplots or any other plots that require index, convert to pandas first:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-19-1)>>> ma.to_pd().vbt.plot().show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/mapped_to_pd_plot.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/mapped_to_pd_plot.dark.svg#only-dark)

Hint

See [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots") and [MappedArray.subplots](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.subplots "vectorbtpro.records.mapped_array.MappedArray.subplots").

[MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") class has a single subplot based on [MappedArray.to_pd](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_pd "vectorbtpro.records.mapped_array.MappedArray.to_pd") and [GenericAccessor.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.plot "vectorbtpro.generic.accessors.GenericAccessor.plot").

* * *

## combine_mapped_with_other function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L448-L460 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.combine_mapped_with_other "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-20-1)combine_mapped_with_other(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-20-2)    other,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-20-3)    np_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-20-4))
    

Combine [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") with other compatible object.

If other object is also [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray"), their `id_arr` and `col_arr` must match.

* * *

## MappedArray class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L463-L1946 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-1)MappedArray(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-3)    mapped_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-4)    col_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-5)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-6)    id_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-7)    mapping=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-8)    col_mapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-9)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-21-10))
    

Exposes methods for reducing, converting, and plotting arrays mapped by [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records") class.

**Args**

**`wrapper`** : `ArrayWrapper`
    

Array wrapper.

See [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper").

**`mapped_arr`** : `array_like`
    A one-dimensional array of mapped record values.
**`col_arr`** : `array_like`
    

A one-dimensional column array.

Must be of the same size as `mapped_arr`.

**`id_arr`** : `array_like`
    

A one-dimensional id array. Defaults to simple range.

Must be of the same size as `mapped_arr`.

**`idx_arr`** : `array_like`
    

A one-dimensional index array. Optional.

Must be of the same size as `mapped_arr`.

**`mapping`** : `namedtuple`, `dict` or `callable`
    Mapping.
**`col_mapper`** : `ColumnMapper`
    

Column mapper if already known.

Note

It depends upon `wrapper` and `col_arr`, so make sure to invalidate `col_mapper` upon creating a [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") instance with a modified `wrapper` or `col_arr.

[MappedArray.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.replace "vectorbtpro.records.mapped_array.MappedArray.replace") does it automatically.

**`**kwargs`**
    

Custom keyword arguments passed to the config.

Useful if any subclass wants to extend the config.

**Superclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")
  * [IndexApplier](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "vectorbtpro.base.indexes.IndexApplier")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [Analyzable.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.generic.analyzable.Analyzable.cls_dir")
  * [Analyzable.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.generic.analyzable.Analyzable.column_only_select")
  * [Analyzable.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.analyzable.Analyzable.config")
  * [Analyzable.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.generic.analyzable.Analyzable.group_select")
  * [Analyzable.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.generic.analyzable.Analyzable.iloc")
  * [Analyzable.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.generic.analyzable.Analyzable.indexing_kwargs")
  * [Analyzable.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.generic.analyzable.Analyzable.loc")
  * [Analyzable.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.generic.analyzable.Analyzable.range_only_select")
  * [Analyzable.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.analyzable.Analyzable.rec_state")
  * [Analyzable.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.generic.analyzable.Analyzable.self_aliases")
  * [Analyzable.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.generic.analyzable.Analyzable.unwrapped")
  * [Analyzable.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.generic.analyzable.Analyzable.wrapper")
  * [Analyzable.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.generic.analyzable.Analyzable.xloc")
  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.generic.analyzable.Analyzable.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.generic.analyzable.Analyzable.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.generic.analyzable.Analyzable.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.generic.analyzable.Analyzable.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.generic.analyzable.Analyzable.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.analyzable.Analyzable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.analyzable.Analyzable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.analyzable.Analyzable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.analyzable.Analyzable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.analyzable.Analyzable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.analyzable.Analyzable.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.analyzable.Analyzable.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.analyzable.Analyzable.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.analyzable.Analyzable.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.analyzable.Analyzable.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.analyzable.Analyzable.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.analyzable.Analyzable.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.analyzable.Analyzable.prettify")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.analyzable.Analyzable.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.analyzable.Analyzable.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.analyzable.Analyzable.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.analyzable.Analyzable.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.analyzable.Analyzable.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.analyzable.Analyzable.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.analyzable.Analyzable.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.analyzable.Analyzable.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.analyzable.Analyzable.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.analyzable.Analyzable.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.analyzable.Analyzable.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.analyzable.Analyzable.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.analyzable.Analyzable.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.analyzable.Analyzable.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.generic.analyzable.Analyzable.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.generic.analyzable.Analyzable.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.generic.analyzable.Analyzable.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.generic.analyzable.Analyzable.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.generic.analyzable.Analyzable.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.generic.analyzable.Analyzable.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.generic.analyzable.Analyzable.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.generic.analyzable.Analyzable.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.generic.analyzable.Analyzable.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.generic.analyzable.Analyzable.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.generic.analyzable.Analyzable.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.generic.analyzable.Analyzable.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.generic.analyzable.Analyzable.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.generic.analyzable.Analyzable.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.generic.analyzable.Analyzable.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.generic.analyzable.Analyzable.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.generic.analyzable.Analyzable.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.generic.analyzable.Analyzable.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.generic.analyzable.Analyzable.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.analyzable.Analyzable.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.analyzable.Analyzable.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.analyzable.Analyzable.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.analyzable.Analyzable.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.analyzable.Analyzable.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.analyzable.Analyzable.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.analyzable.Analyzable.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.analyzable.Analyzable.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.analyzable.Analyzable.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.analyzable.Analyzable.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.analyzable.Analyzable.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.analyzable.Analyzable.save")
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.generic.analyzable.Analyzable.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.generic.analyzable.Analyzable.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.analyzable.Analyzable.plots")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.generic.analyzable.Analyzable.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.analyzable.Analyzable.pprint")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.generic.analyzable.Analyzable.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.generic.analyzable.Analyzable.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.generic.analyzable.Analyzable.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.analyzable.Analyzable.stats")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.generic.analyzable.Analyzable.apply_to_index")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.generic.analyzable.Analyzable.regroup")
  * [Wrapping.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_column_stack_kwargs "vectorbtpro.generic.analyzable.Analyzable.resolve_column_stack_kwargs")
  * [Wrapping.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_row_stack_kwargs "vectorbtpro.generic.analyzable.Analyzable.resolve_row_stack_kwargs")
  * [Wrapping.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "vectorbtpro.generic.analyzable.Analyzable.resolve_self")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.generic.analyzable.Analyzable.resolve_stack_kwargs")



* * *

### apply class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1051-L1087 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.apply "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-1)MappedArray.apply(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-2)    apply_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-4)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-5)    apply_per_group=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-6)    dtype=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-7)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-8)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-9)    col_mapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-10)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-22-11))
    

Apply function on mapped array per column/group. Returns a new mapped array.

Applies per group of columns if `apply_per_group` is True.

See [apply_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.apply_nb "vectorbtpro.records.nb.apply_nb").

For details on the meta version, see [apply_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.apply_meta_nb "vectorbtpro.records.nb.apply_meta_nb").

`**kwargs` are passed to [MappedArray.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.replace "vectorbtpro.records.mapped_array.MappedArray.replace").

* * *

### apply_mapping method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1010-L1019 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.apply_mapping "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-23-1)MappedArray.apply_mapping(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-23-2)    mapping=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-23-3)    mapping_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-23-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-23-5))
    

Apply mapping on each element.

* * *

### apply_mask method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L920-L939 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.apply_mask "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-24-1)MappedArray.apply_mask(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-24-2)    mask,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-24-3)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-24-4)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-24-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-24-6))
    

Return a new class instance, filtered by mask.

`**kwargs` are passed to [MappedArray.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.replace "vectorbtpro.records.mapped_array.MappedArray.replace").

* * *

### bottom_n method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L978-L987 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.bottom_n "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-25-1)MappedArray.bottom_n(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-25-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-25-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-25-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-25-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-25-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-25-7))
    

Filter bottom N elements from each column/group.

* * *

### bottom_n_mask method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L954-L965 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.bottom_n_mask "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-26-1)MappedArray.bottom_n_mask(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-26-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-26-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-26-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-26-5)    chunked=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-26-6))
    

Return mask of bottom N elements in each column/group.

* * *

### boxplot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1917-L1919 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.boxplot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-27-1)MappedArray.boxplot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-27-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-27-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-27-4))
    

Plot box plot by column/group.

* * *

### col_arr class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L854-L857 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.col_arr "Permanent link")

Column array.

* * *

### col_mapper class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L859-L864 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.col_mapper "Permanent link")

Column mapper.

See [ColumnMapper](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper "vectorbtpro.records.col_mapper.ColumnMapper").

* * *

### column_stack class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L588-L672 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.column_stack "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-28-1)MappedArray.column_stack(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-28-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-28-3)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-28-4)    get_indexer_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-28-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-28-6))
    

Stack multiple [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") instances along columns.

Uses [ArrayWrapper.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.column_stack "vectorbtpro.base.wrapping.ArrayWrapper.column_stack") to stack the wrappers.

`get_indexer_kwargs` are passed to [pandas.Index.get_indexer](https://pandas.pydata.org/docs/reference/api/pandas.Index.get_indexer.html) to translate old indices to new ones after the reindexing operation.

Note

Will produce a column-sorted array.

* * *

### count cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1567-L1575 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.count "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-29-1)MappedArray.count(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-29-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-29-3)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-29-4))
    

Return number of values by column/group.

* * *

### coverage_map method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1694-L1710 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.coverage_map "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-30-1)MappedArray.coverage_map(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-30-2)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-30-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-30-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-30-5)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-30-6))
    

See [mapped_coverage_map_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.mapped_coverage_map_nb "vectorbtpro.records.nb.mapped_coverage_map_nb").

* * *

### describe cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1521-L1565 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.describe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-1)MappedArray.describe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-2)    percentiles=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-3)    ddof=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-4)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-5)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-6)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-7)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-31-9))
    

Return statistics by column/group.

* * *

### get_pd_mask method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1815-L1830 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.get_pd_mask "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-32-1)MappedArray.get_pd_mask(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-32-2)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-32-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-32-4)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-32-5))
    

Get mask in form of a Series/DataFrame from row and column indices.

* * *

### has_conflicts cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1677-L1692 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.has_conflicts "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-33-1)MappedArray.has_conflicts(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-33-2)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-33-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-33-4)    jitted=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-33-5))
    

See [mapped_has_conflicts_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.mapped_has_conflicts_nb "vectorbtpro.records.nb.mapped_has_conflicts_nb").

* * *

### histplot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1913-L1915 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.histplot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-34-1)MappedArray.histplot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-34-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-34-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-34-4))
    

Plot histogram by column/group.

* * *

### id_arr class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L871-L874 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.id_arr "Permanent link")

Id array.

* * *

### idx_arr class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L866-L869 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.idx_arr "Permanent link")

Index array.

* * *

### idxmax cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1499-L1519 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.idxmax "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-35-1)MappedArray.idxmax(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-35-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-35-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-35-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-35-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-35-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-35-7))
    

Return index of max by column/group.

* * *

### idxmin cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1477-L1497 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.idxmin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-36-1)MappedArray.idxmin(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-36-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-36-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-36-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-36-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-36-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-36-7))
    

Return index of min by column/group.

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L770-L780 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-37-1)MappedArray.indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-37-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-37-3)    mapped_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-37-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-37-5))
    

Perform indexing on [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray").

* * *

### indexing_func_meta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L735-L768 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.indexing_func_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-38-1)MappedArray.indexing_func_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-38-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-38-3)    wrapper_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-38-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-38-5))
    

Perform indexing on [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") and return metadata.

* * *

### is_sorted cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L883-L890 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.is_sorted "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-39-1)MappedArray.is_sorted(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-39-2)    incl_id=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-39-3)    jitted=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-39-4))
    

Check whether mapped array is sorted.

* * *

### mapped_arr class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L806-L809 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.mapped_arr "Permanent link")

Mapped array.

* * *

### mapped_readable class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L844-L847 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.mapped_readable "Permanent link")

[MappedArray.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_readable "vectorbtpro.records.mapped_array.MappedArray.to_readable") with default arguments.

* * *

### mapping class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L876-L879 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.mapping "Permanent link")

Mapping.

* * *

### max cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1355-L1375 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.max "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-40-1)MappedArray.max(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-40-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-40-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-40-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-40-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-40-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-40-7))
    

Return max by column/group.

* * *

### mean cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1377-L1397 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.mean "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-41-1)MappedArray.mean(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-41-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-41-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-41-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-41-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-41-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-41-7))
    

Return mean by column/group.

* * *

### median cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1399-L1419 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.median "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-42-1)MappedArray.median(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-42-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-42-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-42-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-42-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-42-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-42-7))
    

Return median by column/group.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.metrics "Permanent link")

Metrics supported by [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-4)        calc_func=<function MappedArray.<lambda> at 0x11e2856c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-10)        calc_func=<function MappedArray.<lambda> at 0x11e285760>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-16)        calc_func=<function MappedArray.<lambda> at 0x11e285800>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-21)    count=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-22)        title='Count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-23)        calc_func='count',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-24)        tags='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-26)    mean=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-27)        title='Mean',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-28)        calc_func='mean',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-29)        inv_check_has_mapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-30)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-31)            'mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-32)            'describe'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-33)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-35)    std=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-36)        title='Std',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-37)        calc_func='std',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-38)        inv_check_has_mapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-39)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-40)            'mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-41)            'describe'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-42)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-43)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-44)    min=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-45)        title='Min',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-46)        calc_func='min',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-47)        inv_check_has_mapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-48)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-49)            'mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-50)            'describe'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-51)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-52)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-53)    median=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-54)        title='Median',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-55)        calc_func='median',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-56)        inv_check_has_mapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-57)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-58)            'mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-59)            'describe'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-60)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-61)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-62)    max=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-63)        title='Max',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-64)        calc_func='max',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-65)        inv_check_has_mapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-66)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-67)            'mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-68)            'describe'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-69)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-70)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-71)    idx_min=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-72)        title='Min Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-73)        calc_func='idxmin',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-74)        inv_check_has_mapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-75)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-76)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-77)            'mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-78)            'index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-79)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-80)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-81)    idx_max=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-82)        title='Max Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-83)        calc_func='idxmax',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-84)        inv_check_has_mapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-85)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-86)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-87)            'mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-88)            'index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-89)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-90)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-91)    value_counts=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-92)        title='Value Counts',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-93)        calc_func=<function MappedArray.<lambda> at 0x11e2858a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-94)        resolve_value_counts=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-95)        check_has_mapping=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-96)        tags=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-97)            'mapped_array',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-98)            'value_counts'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-99)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-100)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-43-101))
    

Returns `MappedArray._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `MappedArray._metrics`.

* * *

### min cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1333-L1353 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.min "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-44-1)MappedArray.min(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-44-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-44-3)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-44-4)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-44-5)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-44-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-44-7))
    

Return min by column/group.

* * *

### nth cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1269-L1299 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.nth "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-45-1)MappedArray.nth(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-45-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-45-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-45-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-45-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-45-6)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-45-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-45-8))
    

Return n-th element of each column/group.

* * *

### nth_index cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1301-L1331 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.nth_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-46-1)MappedArray.nth_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-46-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-46-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-46-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-46-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-46-6)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-46-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-46-8))
    

Return index of n-th element of each column/group.

* * *

### pd_mask class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1832-L1835 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.pd_mask "Permanent link")

[MappedArray.get_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.get_pd_mask "vectorbtpro.records.mapped_array.MappedArray.get_pd_mask") with default arguments.

* * *

### plots_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1921-L1931 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.plots_defaults "Permanent link")

Defaults for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.records.mapped_array.MappedArray.plots").

Merges [PlotsBuilderMixin.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots_defaults "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots_defaults") and `plots` from [mapped_array](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.mapped_array "vectorbtpro._settings.mapped_array").

* * *

### readable class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L844-L847 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.readable "Permanent link")

[MappedArray.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_readable "vectorbtpro.records.mapped_array.MappedArray.to_readable") with default arguments.

* * *

### reduce class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1163-L1267 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.reduce "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-1)MappedArray.reduce(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-2)    reduce_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-4)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-5)    returns_array=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-6)    returns_idx=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-7)    to_index=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-8)    fill_value=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-9)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-10)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-11)    col_mapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-12)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-13)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-47-14))
    

Reduce mapped array by column/group.

Set `returns_array` to True if `reduce_func_nb` returns an array.

Set `returns_idx` to True if `reduce_func_nb` returns row index/position. Must pass `idx_arr`.

Set `to_index` to True to return labels instead of positions.

Use `fill_value` to set the default value.

For implementation details, see

  * [reduce_mapped_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_nb "vectorbtpro.records.nb.reduce_mapped_nb") if `returns_array` is False and `returns_idx` is False
  * [reduce_mapped_to_idx_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_to_idx_nb "vectorbtpro.records.nb.reduce_mapped_to_idx_nb") if `returns_array` is False and `returns_idx` is True
  * [reduce_mapped_to_array_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_to_array_nb "vectorbtpro.records.nb.reduce_mapped_to_array_nb") if `returns_array` is True and `returns_idx` is False
  * [reduce_mapped_to_idx_array_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_to_idx_array_nb "vectorbtpro.records.nb.reduce_mapped_to_idx_array_nb") if `returns_array` is True and `returns_idx` is True



For implementation details on the meta versions, see

  * [reduce_mapped_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_meta_nb "vectorbtpro.records.nb.reduce_mapped_meta_nb") if `returns_array` is False and `returns_idx` is False
  * [reduce_mapped_to_idx_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_to_idx_meta_nb "vectorbtpro.records.nb.reduce_mapped_to_idx_meta_nb") if `returns_array` is False and `returns_idx` is True
  * [reduce_mapped_to_array_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_to_array_meta_nb "vectorbtpro.records.nb.reduce_mapped_to_array_meta_nb") if `returns_array` is True and `returns_idx` is False
  * [reduce_mapped_to_idx_array_meta_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_to_idx_array_meta_nb "vectorbtpro.records.nb.reduce_mapped_to_idx_array_meta_nb") if `returns_array` is True and `returns_idx` is True



* * *

### reduce_segments method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1091-L1161 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.reduce_segments "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-1)MappedArray.reduce_segments(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-2)    segment_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-3)    reduce_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-4)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-5)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-6)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-7)    apply_per_group=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-8)    dtype=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-9)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-10)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-11)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-48-12))
    

Reduce each segment of values in mapped array. Returns a new mapped array.

`segment_arr` must be an array of integers increasing per column, each indicating a segment. It must have the same length as the mapped array. You can also pass a list of such arrays. In this case, each unique combination of values will be considered a single segment. Can also pass the string "idx" to use the index array.

`reduce_func_nb` can be a string denoting the suffix of a reducing function from [vectorbtpro.generic.nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/ "vectorbtpro.generic.nb"). For example, "sum" will refer to "sum_reduce_nb".

Warning

Each segment or combination of segments in `segment_arr` is assumed to be coherent and non-repeating. That is, `np.array([0, 1, 0])` for a single column annotates three different segments, not two. See [index_repeating_rows_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.index_repeating_rows_nb "vectorbtpro.utils.array_.index_repeating_rows_nb").

Hint

Use [MappedArray.sort](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.sort "vectorbtpro.records.mapped_array.MappedArray.sort") to bring the mapped array to the desired order, if required.

Applies per group of columns if `apply_per_group` is True.

See [reduce_mapped_segments_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.reduce_mapped_segments_nb "vectorbtpro.records.nb.reduce_mapped_segments_nb").

`**kwargs` are passed to [MappedArray.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.replace "vectorbtpro.records.mapped_array.MappedArray.replace").

* * *

### replace method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L722-L733 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.replace "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-49-1)MappedArray.replace(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-49-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-49-3))
    

See [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.config.Configured.replace").

Also, makes sure that [MappedArray.col_mapper](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.col_mapper "vectorbtpro.records.mapped_array.MappedArray.col_mapper") is not passed to the new instance.

* * *

### resample method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L797-L804 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.resample "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-50-1)MappedArray.resample(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-50-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-50-3)    mapped_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-50-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-50-5))
    

Perform resampling on [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray").

* * *

### resample_meta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L782-L795 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.resample_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-51-1)MappedArray.resample_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-51-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-51-3)    wrapper_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-51-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-51-5))
    

Perform resampling on [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") and return metadata.

* * *

### resolve_mapping method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L991-L1008 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.resolve_mapping "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-52-1)MappedArray.resolve_mapping(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-52-2)    mapping=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-52-3))
    

Resolve mapping.

Set `mapping` to False to disable mapping completely.

* * *

### row_stack class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L496-L586 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.row_stack "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-53-1)MappedArray.row_stack(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-53-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-53-3)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-53-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-53-5))
    

Stack multiple [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") instances along rows.

Uses [ArrayWrapper.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.row_stack "vectorbtpro.base.wrapping.ArrayWrapper.row_stack") to stack the wrappers.

Note

Will produce a column-sorted array.

* * *

### sort method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L892-L916 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.sort "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-54-1)MappedArray.sort(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-54-2)    incl_id=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-54-3)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-54-4)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-54-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-54-6))
    

Sort mapped array by column array (primary) and id array (secondary, optional).

`**kwargs` are passed to [MappedArray.replace](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.replace "vectorbtpro.records.mapped_array.MappedArray.replace").

* * *

### stats_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1839-L1849 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.stats_defaults "Permanent link")

Defaults for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.records.mapped_array.MappedArray.stats").

Merges [StatsBuilderMixin.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults") and `stats` from [mapped_array](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.mapped_array "vectorbtpro._settings.mapped_array").

* * *

### std cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1421-L1451 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.std "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-55-1)MappedArray.std(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-55-2)    ddof=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-55-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-55-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-55-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-55-6)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-55-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-55-8))
    

Return std by column/group.

* * *

### subplots property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.subplots "Permanent link")

Subplots supported by [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-56-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-56-2)    to_pd_plot=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-56-3)        check_is_not_grouped=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-56-4)        plot_func='to_pd.vbt.plot',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-56-5)        pass_trace_names=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-56-6)        tags='mapped_array'
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-56-7)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-56-8))
    

Returns `MappedArray._subplots`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `MappedArray._subplots`.

* * *

### sum cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1453-L1475 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.sum "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-57-1)MappedArray.sum(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-57-2)    fill_value=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-57-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-57-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-57-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-57-6)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-57-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-57-8))
    

Return sum by column/group.

* * *

### to_columns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1045-L1049 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_columns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-58-1)MappedArray.to_columns()
    

Convert to columns.

* * *

### to_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1021-L1043 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-59-1)MappedArray.to_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-59-2)    minus_one_to_zero=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-59-3))
    

Convert to index.

If `minus_one_to_zero` is True, index -1 will automatically become 0. Otherwise, will throw an error.

* * *

### to_pd method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1714-L1811 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_pd "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-1)MappedArray.to_pd(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-2)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-3)    reduce_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-4)    reduce_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-5)    dtype=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-6)    ignore_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-7)    repeat_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-8)    fill_value=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-9)    mapping=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-10)    mapping_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-11)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-12)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-13)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-14)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-15)    silence_warnings=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-60-16))
    

Unstack mapped array to a Series/DataFrame.

If `reduce_func_nb` is not None, will use it to reduce conflicting index segments using [MappedArray.reduce_segments](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.reduce_segments "vectorbtpro.records.mapped_array.MappedArray.reduce_segments").

  * If `ignore_index`, will ignore the index and place values on top of each other in every column/group. See [ignore_unstack_mapped_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.ignore_unstack_mapped_nb "vectorbtpro.records.nb.ignore_unstack_mapped_nb").
  * If `repeat_index`, will repeat any index pointed from multiple values. Otherwise, in case of positional conflicts, will throw a warning and use the latest value. See [repeat_unstack_mapped_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.repeat_unstack_mapped_nb "vectorbtpro.records.nb.repeat_unstack_mapped_nb").
  * Otherwise, see [unstack_mapped_nb](https://vectorbt.pro/pvt_7a467f6b/api/records/nb/#vectorbtpro.records.nb.unstack_mapped_nb "vectorbtpro.records.nb.unstack_mapped_nb").



Note

Will raise an error if there are multiple values pointing to the same position. Set `ignore_index` to True in this case.

Warning

Mapped arrays represent information in the most memory-friendly format. Mapping back to pandas may occupy lots of memory if records are sparse.

* * *

### to_readable method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L816-L842 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_readable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-61-1)MappedArray.to_readable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-61-2)    title='Value',
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-61-3)    only_values=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-61-4)    expand_columns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-61-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-61-6))
    

Get values in a human-readable format.

* * *

### top_n method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L967-L976 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.top_n "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-62-1)MappedArray.top_n(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-62-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-62-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-62-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-62-5)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-62-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-62-7))
    

Filter top N elements from each column/group.

* * *

### top_n_mask method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L941-L952 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.top_n_mask "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-63-1)MappedArray.top_n_mask(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-63-2)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-63-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-63-4)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-63-5)    chunked=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-63-6))
    

Return mask of top N elements in each column/group.

* * *

### value_counts cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L1579-L1673 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.value_counts "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-1)MappedArray.value_counts(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-2)    axis=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-3)    idx_arr=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-4)    normalize=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-5)    sort_uniques=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-6)    sort=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-7)    ascending=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-8)    dropna=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-9)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-10)    mapping=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-11)    incl_all_keys=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-12)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-13)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-14)    wrap_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-15)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#__codelineno-64-16))
    

See [GenericAccessor.value_counts](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.value_counts "vectorbtpro.generic.accessors.GenericAccessor.value_counts").

* * *

### values class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/mapped_array.py#L811-L814 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.values "Permanent link")

Mapped array.
