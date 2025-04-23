reshaping

#  reshaping module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping "Permanent link")

Functions for reshaping arrays.

Reshape functions transform a Pandas object/NumPy array in some way.

* * *

## IndexFromLike literal[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.IndexFromLike "Permanent link")

Any object that can be coerced into a `index_from` argument.

* * *

## to_1d_array partial function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_1d_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-0-1)to_1d_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-0-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-0-3)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-0-4)    raw=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-0-5))
    

[to_1d](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_1d "vectorbtpro.base.reshaping.to_1d") with `raw` enabled.

* * *

## to_2d_array partial function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-1-1)to_2d_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-1-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-1-3)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-1-4)    raw=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-1-5)    expand_axis=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-1-6))
    

[to_2d](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d "vectorbtpro.base.reshaping.to_2d") with `raw` enabled.

* * *

## to_2d_pc_array partial function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_pc_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-2-1)to_2d_pc_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-2-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-2-3)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-2-4)    raw=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-2-5)    expand_axis=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-2-6))
    

[to_2d_array](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_array "vectorbtpro.base.reshaping.to_2d_array") with `expand_axis=0`.

* * *

## to_2d_pr_array partial function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_pr_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-3-1)to_2d_pr_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-3-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-3-3)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-3-4)    raw=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-3-5)    expand_axis=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-3-6))
    

[to_2d_array](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_array "vectorbtpro.base.reshaping.to_2d_array") with `expand_axis=1`.

* * *

## align_pd_arrays function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L626-L710 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.align_pd_arrays "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-1)align_pd_arrays(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-3)    align_index=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-4)    align_columns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-5)    to_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-6)    to_columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-7)    axis=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-8)    reindex_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-4-9))
    

Align Pandas arrays against common index and/or column levels using reindexing and [align_indexes](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.align_indexes "vectorbtpro.base.indexes.align_indexes") respectively.

* * *

## broadcast function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L801-L1724 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-1)broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-3)    to_shape=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-4)    align_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-5)    align_columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-6)    index_from=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-7)    columns_from=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-8)    to_frame=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-9)    axis=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-10)    to_pd=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-11)    keep_flex=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-12)    min_ndim=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-13)    expand_axis=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-14)    post_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-15)    require_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-16)    reindex_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-17)    merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-18)    tile=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-19)    random_subset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-20)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-21)    keep_wrap_default=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-22)    return_wrapper=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-23)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-24)    ignore_sr_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-25)    ignore_ranges=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-26)    check_index_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-27)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-28)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-5-29))
    

Bring any array-like object in `objs` to the same shape by using NumPy-like broadcasting.

See [Broadcasting](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html).

Important

The major difference to NumPy is that one-dimensional arrays will always broadcast against the row axis!

Can broadcast Pandas objects by broadcasting their index/columns with [broadcast_index](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_index "vectorbtpro.base.reshaping.broadcast_index").

**Args**

**`*objs`**
    

Objects to broadcast.

If the first and only argument is a mapping, will return a dict.

Allows using [BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO "vectorbtpro.base.reshaping.BCO"), [Ref](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Ref "vectorbtpro.base.reshaping.Ref"), [Default](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Default "vectorbtpro.base.reshaping.Default"), [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param"), [index_dict](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.index_dict "vectorbtpro.base.indexing.index_dict"), [IdxSetter](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter "vectorbtpro.base.indexing.IdxSetter"), [IdxSetterFactory](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory "vectorbtpro.base.indexing.IdxSetterFactory"), and templates. If an index dictionary, fills using [ArrayWrapper.fill_and_set](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.fill_and_set "vectorbtpro.base.wrapping.ArrayWrapper.fill_and_set").

**`to_shape`** : `tuple` of `int`
    Target shape. If set, will broadcast every object in `objs` to `to_shape`.
**`align_index`** : `bool`
    

Whether to align index of Pandas objects using union.

Pass None to use the default.

**`align_columns`** : `bool`
    

Whether to align columns of Pandas objects using multi-index.

Pass None to use the default.

**`index_from`** : `any`
    

Broadcasting rule for index.

Pass None to use the default.

**`columns_from`** : `any`
    

Broadcasting rule for columns.

Pass None to use the default.

**`to_frame`** : `bool`
    Whether to convert all Series to DataFrames.
**`axis`** : `int`, `sequence` or `mapping`
    See [BCO.axis](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.axis "vectorbtpro.base.reshaping.BCO.axis").
**`to_pd`** : `bool`, `sequence` or `mapping`
    

See [BCO.to_pd](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.to_pd "vectorbtpro.base.reshaping.BCO.to_pd").

If None, converts only if there is at least one Pandas object among them.

**`keep_flex`** : `bool`, `sequence` or `mapping`
    See [BCO.keep_flex](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.keep_flex "vectorbtpro.base.reshaping.BCO.keep_flex").
**`min_ndim`** : `int`, `sequence` or `mapping`
    

See [BCO.min_ndim](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.min_ndim "vectorbtpro.base.reshaping.BCO.min_ndim").

If None, becomes 2 if `keep_flex` is True, otherwise 1.

**`expand_axis`** : `int`, `sequence` or `mapping`
    See [BCO.expand_axis](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.expand_axis "vectorbtpro.base.reshaping.BCO.expand_axis").
**`post_func`** : `callable`, `sequence` or `mapping`
    

See [BCO.post_func](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.post_func "vectorbtpro.base.reshaping.BCO.post_func").

Applied only when `keep_flex` is False.

**`require_kwargs`** : `dict`, `sequence` or `mapping`
    

See [BCO.require_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.require_kwargs "vectorbtpro.base.reshaping.BCO.require_kwargs").

This key will be merged with any argument-specific dict. If the mapping contains all keys in `np.require`, it will be applied to all objects.

**`reindex_kwargs`** : `dict`, `sequence` or `mapping`
    

See [BCO.reindex_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.reindex_kwargs "vectorbtpro.base.reshaping.BCO.reindex_kwargs").

This key will be merged with any argument-specific dict. If the mapping contains all keys in `pd.DataFrame.reindex`, it will be applied to all objects.

**`merge_kwargs`** : `dict`, `sequence` or `mapping`
    

See [BCO.merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.merge_kwargs "vectorbtpro.base.reshaping.BCO.merge_kwargs").

This key will be merged with any argument-specific dict. If the mapping contains all keys in `pd.DataFrame.merge`, it will be applied to all objects.

**`tile`** : `int` or `index_like`
    Tile the final object by the number of times or index.
**`random_subset`** : `int`
    

Select a random subset of parameter values.

Seed can be set using NumPy before calling this function.

**`seed`** : `int`
    Seed to make output deterministic.
**`keep_wrap_default`** : `bool`
    Whether to keep wrapping with [Default](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Default "vectorbtpro.base.reshaping.Default").
**`return_wrapper`** : `bool`
    Whether to also return the wrapper associated with the operation.
**`wrapper_kwargs`** : `dict`
    Keyword arguments passed to [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper").
**`ignore_sr_names`** : `bool`
    See [broadcast_index](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_index "vectorbtpro.base.reshaping.broadcast_index").
**`ignore_ranges`** : `bool`
    See [broadcast_index](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_index "vectorbtpro.base.reshaping.broadcast_index").
**`check_index_names`** : `bool`
    See [broadcast_index](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_index "vectorbtpro.base.reshaping.broadcast_index").
**`clean_index_kwargs`** : `dict`
    Keyword arguments passed to [clean_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.clean_index "vectorbtpro.base.indexes.clean_index").
**`template_context`** : `dict`
    Context used to substitute templates.

For defaults, see [broadcasting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.broadcasting "vectorbtpro._settings.broadcasting").

Any keyword argument that can be associated with an object can be passed as

  * a const that is applied to all objects,
  * a sequence with value per object, and
  * a mapping with value per object name and the special key `_def` denoting the default value.



Additionally, any object can be passed wrapped with [BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO "vectorbtpro.base.reshaping.BCO"), which ibutes will override any of the above arguments if not None.

**Usage**

  * Without broadcasting index and columns:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-3)>>> v = 0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-4)>>> a = np.array([1, 2, 3])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-5)>>> sr = pd.Series([1, 2, 3], index=pd.Index(['x', 'y', 'z']), name='a')
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-6)>>> df = pd.DataFrame(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-7)...     [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-8)...     index=pd.Index(['x2', 'y2', 'z2']),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-9)...     columns=pd.Index(['a2', 'b2', 'c2']),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-10)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-12)>>> for i in vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-13)...     v, a, sr, df,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-14)...     index_from='keep',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-15)...     columns_from='keep',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-16)...     align_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-17)... ): print(i)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-18)   0  1  2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-19)0  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-20)1  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-21)2  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-22)   0  1  2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-23)0  1  2  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-24)1  1  2  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-25)2  1  2  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-26)   a  a  a
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-27)x  1  1  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-28)y  2  2  2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-29)z  3  3  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-30)    a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-31)x2   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-32)y2   4   5   6
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-6-33)z2   7   8   9
    

  * Take index and columns from the argument at specific position:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-1)>>> for i in vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-2)...     v, a, sr, df,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-3)...     index_from=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-4)...     columns_from=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-5)...     align_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-6)... ): print(i)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-7)   a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-8)x   0   0   0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-9)y   0   0   0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-10)z   0   0   0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-11)   a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-12)x   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-13)y   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-14)z   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-15)   a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-16)x   1   1   1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-17)y   2   2   2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-18)z   3   3   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-19)   a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-20)x   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-21)y   4   5   6
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-7-22)z   7   8   9
    

  * Broadcast index and columns through stacking:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-1)>>> for i in vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-2)...     v, a, sr, df,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-3)...     index_from='stack',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-4)...     columns_from='stack',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-5)...     align_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-6)... ): print(i)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-7)      a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-8)x x2   0   0   0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-9)y y2   0   0   0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-10)z z2   0   0   0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-11)      a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-12)x x2   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-13)y y2   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-14)z z2   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-15)      a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-16)x x2   1   1   1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-17)y y2   2   2   2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-18)z z2   3   3   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-19)      a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-20)x x2   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-21)y y2   4   5   6
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-8-22)z z2   7   8   9
    

  * Set index and columns manually:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-1)>>> for i in vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-2)...     v, a, sr, df,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-3)...     index_from=['a', 'b', 'c'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-4)...     columns_from=['d', 'e', 'f'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-5)...     align_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-6)... ): print(i)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-7)   d  e  f
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-8)a  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-9)b  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-10)c  0  0  0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-11)   d  e  f
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-12)a  1  2  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-13)b  1  2  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-14)c  1  2  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-15)   d  e  f
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-16)a  1  1  1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-17)b  2  2  2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-18)c  3  3  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-19)   d  e  f
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-20)a  1  2  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-21)b  4  5  6
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-9-22)c  7  8  9
    

  * Pass arguments as a mapping returns a mapping:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-1)>>> vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-2)...     dict(v=v, a=a, sr=sr, df=df),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-3)...     index_from='stack',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-4)...     align_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-5)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-6){'v':       a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-7)      x x2   0   0   0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-8)      y y2   0   0   0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-9)      z z2   0   0   0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-10) 'a':       a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-11)      x x2   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-12)      y y2   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-13)      z z2   1   2   3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-14) 'sr':       a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-15)       x x2   1   1   1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-16)       y y2   2   2   2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-17)       z z2   3   3   3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-18) 'df':       a2  b2  c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-19)       x x2   1   2   3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-20)       y y2   4   5   6
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-10-21)       z z2   7   8   9}
    

  * Keep all results in a format suitable for flexible indexing apart from one:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-1)>>> vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-2)...     dict(v=v, a=a, sr=sr, df=df),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-3)...     index_from='stack',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-4)...     keep_flex=dict(_def=True, df=False),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-5)...     require_kwargs=dict(df=dict(dtype=float)),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-6)...     align_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-8){'v': array([0]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-9) 'a': array([1, 2, 3]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-10) 'sr': array([[1],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-11)              [2],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-12)              [3]]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-13) 'df':        a2   b2   c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-14)       x x2  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-15)       y y2  4.0  5.0  6.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-11-16)       z z2  7.0  8.0  9.0}
    

  * Specify arguments per object using [BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO "vectorbtpro.base.reshaping.BCO"):


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-1)>>> df_bco = vbt.BCO(df, keep_flex=False, require_kwargs=dict(dtype=float))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-2)>>> vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-3)...     dict(v=v, a=a, sr=sr, df=df_bco),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-4)...     index_from='stack',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-5)...     keep_flex=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-6)...     align_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-8){'v': array([0]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-9) 'a': array([1, 2, 3]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-10) 'sr': array([[1],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-11)              [2],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-12)              [3]]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-13) 'df':        a2   b2   c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-14)       x x2  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-15)       y y2  4.0  5.0  6.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-12-16)       z z2  7.0  8.0  9.0}
    

  * Introduce a parameter that should build a Cartesian product of its values and other objects:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-1)>>> df_bco = vbt.BCO(df, keep_flex=False, require_kwargs=dict(dtype=float))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-2)>>> p_bco = vbt.BCO(pd.Param([1, 2, 3], name='my_p'))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-3)>>> vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-4)...     dict(v=v, a=a, sr=sr, df=df_bco, p=p_bco),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-5)...     index_from='stack',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-6)...     keep_flex=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-7)...     align_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-8)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-9){'v': array([0]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-10) 'a': array([1, 2, 3, 1, 2, 3, 1, 2, 3]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-11) 'sr': array([[1],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-12)        [2],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-13)        [3]]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-14) 'df': my_p        1              2              3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-15)        a2   b2   c2   a2   b2   c2   a2   b2   c2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-16) x x2  1.0  2.0  3.0  1.0  2.0  3.0  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-17) y y2  4.0  5.0  6.0  4.0  5.0  6.0  4.0  5.0  6.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-18) z z2  7.0  8.0  9.0  7.0  8.0  9.0  7.0  8.0  9.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-19) 'p': array([[1, 1, 1, 2, 2, 2, 3, 3, 3],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-20)        [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-13-21)        [1, 1, 1, 2, 2, 2, 3, 3, 3]])}
    

  * Build a Cartesian product of all parameters:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-1)>>> vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-2)...     dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-3)...         a=vbt.Param([1, 2, 3]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-4)...         b=vbt.Param(['x', 'y']),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-5)...         c=vbt.Param([False, True])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-6)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-8){'a': array([[1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-9) 'b': array([['x', 'x', 'y', 'y', 'x', 'x', 'y', 'y', 'x', 'x', 'y', 'y']], dtype='<U1'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-14-10) 'c': array([[False, True, False, True, False, True, False, True, False, True, False, True]])}
    

  * Build a Cartesian product of two groups of parameters - (a, d) and (b, c):


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-1)>>> vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-2)...     dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-3)...         a=vbt.Param([1, 2, 3], level=0),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-4)...         b=vbt.Param(['x', 'y'], level=1),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-5)...         d=vbt.Param([100., 200., 300.], level=0),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-6)...         c=vbt.Param([False, True], level=1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-7)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-8)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-9){'a': array([[1, 1, 2, 2, 3, 3]]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-10) 'b': array([['x', 'y', 'x', 'y', 'x', 'y']], dtype='<U1'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-11) 'd': array([[100., 100., 200., 200., 300., 300.]]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-15-12) 'c': array([[False,  True, False,  True, False,  True]])}
    

  * Select a random subset of parameter combinations:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-1)>>> vbt.broadcast(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-2)...     dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-3)...         a=vbt.Param([1, 2, 3]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-4)...         b=vbt.Param(['x', 'y']),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-5)...         c=vbt.Param([False, True])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-6)...     ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-7)...     random_subset=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-8)...     seed=42
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-9)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-10){'a': array([[1, 2, 3, 3, 3]]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-11) 'b': array([['x', 'x', 'x', 'x', 'y']], dtype='<U1'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-16-12) 'c': array([[False,  True, False,  True, False]])}
    

* * *

## broadcast_array_to function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L388-L420 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_array_to "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-17-1)broadcast_array_to(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-17-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-17-3)    target_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-17-4)    axis=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-17-5)    expand_axis=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-17-6))
    

Broadcast an array-like object to a target shape using vectorbt's broadcasting rules.

* * *

## broadcast_arrays function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L423-L455 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_arrays "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-18-1)broadcast_arrays(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-18-2)    *arrs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-18-3)    target_shape=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-18-4)    axis=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-18-5)    expand_axis=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-18-6))
    

Broadcast array-like objects using vectorbt's broadcasting rules.

Optionally to a target shape.

* * *

## broadcast_combs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L1850-L1919 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_combs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-19-1)broadcast_combs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-19-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-19-3)    axis=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-19-4)    comb_func=itertools.product,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-19-5)    **broadcast_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-19-6))
    

Align an axis of each array using a combinatoric function and broadcast their indexes.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-2)>>> from vectorbtpro.base.reshaping import broadcast_combs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-4)>>> df = pd.DataFrame([[1, 2, 3], [3, 4, 5]], columns=pd.Index(['a', 'b', 'c'], name='df_param'))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-5)>>> df2 = pd.DataFrame([[6, 7], [8, 9]], columns=pd.Index(['d', 'e'], name='df2_param'))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-6)>>> sr = pd.Series([10, 11], name='f')
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-8)>>> new_df, new_df2, new_sr = broadcast_combs((df, df2, sr))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-10)>>> new_df
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-11)df_param   a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-12)df2_param  d  e  d  e  d  e
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-13)0          1  1  2  2  3  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-14)1          3  3  4  4  5  5
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-16)>>> new_df2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-17)df_param   a     b     c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-18)df2_param  d  e  d  e  d  e
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-19)0          6  7  6  7  6  7
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-20)1          8  9  8  9  8  9
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-21)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-22)>>> new_sr
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-23)df_param    a       b       c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-24)df2_param   d   e   d   e   d   e
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-25)0          10  10  10  10  10  10
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-20-26)1          11  11  11  11  11  11
    

* * *

## broadcast_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L462-L581 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-1)broadcast_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-2)    objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-3)    to_shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-4)    index_from=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-5)    axis=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-6)    ignore_sr_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-7)    ignore_ranges=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-8)    check_index_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-9)    **clean_index_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-21-10))
    

Produce a broadcast index/columns.

**Args**

**`objs`** : `iterable` of `array_like`
    Array-like objects.
**`to_shape`** : `tuple` of `int`
    Target shape.
**`index_from`** : `any`
    

Broadcasting rule for this index/these columns.

Accepts the following values:

  * 'keep' or None - keep the original index/columns of the objects in `objs`
  * 'stack' - stack different indexes/columns using [stack_indexes](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.stack_indexes "vectorbtpro.base.indexes.stack_indexes")
  * 'strict' - ensure that all Pandas objects have the same index/columns
  * 'reset' - reset any index/columns (they become a simple range)
  * integer - use the index/columns of the i-th object in `objs`
  * everything else will be converted to `pd.Index`


**`axis`** : `int`
    Set to 0 for index and 1 for columns.
**`ignore_sr_names`** : `bool`
    

Whether to ignore Series names if they are in conflict.

Conflicting Series names are those that are different but not None.

**`ignore_ranges`** : `bool`
    Whether to ignore indexes of type `pd.RangeIndex`.
**`check_index_names`** : `bool`
    See [is_index_equal](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_index_equal "vectorbtpro.utils.checks.is_index_equal").
**`**clean_index_kwargs`**
    Keyword arguments passed to [clean_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.clean_index "vectorbtpro.base.indexes.clean_index").

For defaults, see [broadcasting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.broadcasting "vectorbtpro._settings.broadcasting").

Note

Series names are treated as columns with a single element but without a name. If a column level without a name loses its meaning, better to convert Series to DataFrames with one column prior to broadcasting. If the name of a Series is not that important, better to drop it altogether by setting it to None.

* * *

## broadcast_shapes function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L335-L385 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_shapes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-22-1)broadcast_shapes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-22-2)    *shapes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-22-3)    axis=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-22-4)    expand_axis=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-22-5))
    

Broadcast shape-like objects using vectorbt's broadcasting rules.

* * *

## broadcast_to function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L1727-L1791 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_to "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-23-1)broadcast_to(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-23-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-23-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-23-4)    to_pd=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-23-5)    index_from=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-23-6)    columns_from=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-23-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-23-8))
    

Broadcast `arg1` to `arg2`.

Argument `arg2` can be a shape, an instance of [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper"), or any array-like object.

Pass None to `index_from`/`columns_from` to use index/columns of the second argument.

Keyword arguments `**kwargs` are passed to [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "vectorbtpro.base.reshaping.broadcast").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-2)>>> from vectorbtpro.base.reshaping import broadcast_to
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-4)>>> a = np.array([1, 2, 3])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-5)>>> sr = pd.Series([4, 5, 6], index=pd.Index(['x', 'y', 'z']), name='a')
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-7)>>> broadcast_to(a, sr)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-8)x    1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-9)y    2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-10)z    3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-11)Name: a, dtype: int64
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-13)>>> broadcast_to(sr, a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-24-14)array([4, 5, 6])
    

* * *

## broadcast_to_array_of function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L1794-L1826 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_to_array_of "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-25-1)broadcast_to_array_of(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-25-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-25-3)    arg2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-25-4))
    

Broadcast `arg1` to the shape `(1, *arg2.shape)`.

`arg1` must be either a scalar, a 1-dim array, or have 1 dimension more than `arg2`.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-2)>>> from vectorbtpro.base.reshaping import broadcast_to_array_of
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-4)>>> broadcast_to_array_of([0.1, 0.2], np.empty((2, 2)))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-5)[[[0.1 0.1]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-6)  [0.1 0.1]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-8) [[0.2 0.2]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-26-9)  [0.2 0.2]]]
    

* * *

## broadcast_to_axis_of function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L1829-L1847 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast_to_axis_of "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-27-1)broadcast_to_axis_of(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-27-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-27-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-27-4)    axis,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-27-5)    require_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-27-6))
    

Broadcast `arg1` to an axis of `arg2`.

If `arg2` has less dimensions than requested, will broadcast `arg1` to a single number.

For other keyword arguments, see [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "vectorbtpro.base.reshaping.broadcast").

* * *

## get_multiindex_series function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L1922-L1935 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.get_multiindex_series "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-28-1)get_multiindex_series(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-28-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-28-3))
    

Get Series with a multi-index.

If DataFrame has been passed, must at maximum have one row or column.

* * *

## index_to_frame function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L114-L118 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.index_to_frame "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-29-1)index_to_frame(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-29-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-29-3)    reset_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-29-4))
    

Convert Index to DataFrame.

* * *

## index_to_series function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L107-L111 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.index_to_series "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-30-1)index_to_series(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-30-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-30-3)    reset_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-30-4))
    

Convert Index to Series.

* * *

## make_symmetric function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L2001-L2066 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.make_symmetric "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-31-1)make_symmetric(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-31-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-31-3)    sort=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-31-4))
    

Make `obj` symmetric.

The index and columns of the resulting DataFrame will be identical.

Requires the index and columns to have the same number of levels.

Pass `sort=False` if index and columns should not be sorted, but concatenated and get duplicates removed.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-2)>>> from vectorbtpro.base.reshaping import make_symmetric
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-4)>>> df = pd.DataFrame([[1, 2], [3, 4]], index=['a', 'b'], columns=['c', 'd'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-6)>>> make_symmetric(df)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-7)     a    b    c    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-8)a  NaN  NaN  1.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-9)b  NaN  NaN  3.0  4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-10)c  1.0  3.0  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-32-11)d  2.0  4.0  NaN  NaN
    

* * *

## mapping_to_series function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L121-L125 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.mapping_to_series "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-33-1)mapping_to_series(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-33-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-33-3))
    

Convert a mapping-like object to Series.

* * *

## repeat function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L282-L303 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.repeat "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-34-1)repeat(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-34-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-34-3)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-34-4)    axis=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-34-5)    raw=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-34-6)    ignore_ranges=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-34-7))
    

Repeat `obj` `n` times along the specified axis.

* * *

## repeat_shape function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L92-L97 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.repeat_shape "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-35-1)repeat_shape(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-35-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-35-3)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-35-4)    axis=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-35-5))
    

Repeat shape `n` times along the specified axis.

* * *

## resolve_ref function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L775-L798 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.resolve_ref "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-36-1)resolve_ref(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-36-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-36-3)    k,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-36-4)    inside_bco=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-36-5)    keep_wrap_default=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-36-6))
    

Resolve a potential reference.

* * *

## soft_to_ndim function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L169-L183 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.soft_to_ndim "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-37-1)soft_to_ndim(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-37-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-37-3)    ndim,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-37-4)    raw=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-37-5))
    

Try to softly bring `obj` to the specified number of dimensions `ndim` (max 2).

* * *

## tile function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L306-L332 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.tile "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-38-1)tile(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-38-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-38-3)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-38-4)    axis=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-38-5)    raw=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-38-6)    ignore_ranges=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-38-7))
    

Tile `obj` `n` times along the specified axis.

* * *

## tile_shape function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L100-L104 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.tile_shape "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-39-1)tile_shape(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-39-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-39-3)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-39-4)    axis=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-39-5))
    

Tile shape `n` times along the specified axis.

Identical to [repeat_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.repeat_shape "vectorbtpro.base.reshaping.repeat_shape"). Exists purely for naming consistency.

* * *

## to_1d function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L186-L201 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_1d "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-40-1)to_1d(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-40-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-40-3)    raw=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-40-4))
    

Reshape argument to one dimension.

If `raw` is True, returns NumPy array. If 2-dim, will collapse along axis 1 (i.e., DataFrame with one column to Series).

* * *

## to_1d_array_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L238-L247 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_1d_array_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-41-1)to_1d_array_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-41-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-41-3))
    

Resize array to one dimension.

* * *

## to_1d_shape function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L65-L74 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_1d_shape "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-42-1)to_1d_shape(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-42-2)    shape
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-42-3))
    

Convert a shape-like object to a 1-dim shape.

* * *

## to_2d function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L208-L225 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-43-1)to_2d(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-43-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-43-3)    raw=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-43-4)    expand_axis=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-43-5))
    

Reshape argument to two dimensions.

If `raw` is True, returns NumPy array. If 1-dim, will expand along axis 1 (i.e., Series to DataFrame with one column).

* * *

## to_2d_array_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L250-L259 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_array_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-44-1)to_2d_array_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-44-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-44-3)    expand_axis=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-44-4))
    

Resize array to two dimensions.

* * *

## to_2d_pc_array_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L268-L271 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_pc_array_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-45-1)to_2d_pc_array_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-45-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-45-3))
    

[to_2d_array_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_array_nb "vectorbtpro.base.reshaping.to_2d_array_nb") with `expand_axis=0`.

* * *

## to_2d_pr_array_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L262-L265 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_pr_array_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-46-1)to_2d_pr_array_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-46-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-46-3))
    

[to_2d_array_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_array_nb "vectorbtpro.base.reshaping.to_2d_array_nb") with `expand_axis=1`.

* * *

## to_2d_shape function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L77-L89 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_2d_shape "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-47-1)to_2d_shape(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-47-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-47-3)    expand_axis=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-47-4))
    

Convert a shape-like object to a 2-dim shape.

* * *

## to_any_array function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L128-L143 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_any_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-48-1)to_any_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-48-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-48-3)    raw=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-48-4)    convert_index=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-48-5))
    

Convert any array-like object to an array.

Pandas objects are kept as-is unless `raw` is True.

* * *

## to_dict function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L274-L279 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-49-1)to_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-49-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-49-3)    orient='dict'
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-49-4))
    

Convert object to dict.

* * *

## to_pd_array function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L146-L166 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_pd_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-50-1)to_pd_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-50-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-50-3)    convert_index=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-50-4))
    

Convert any array-like object to a Pandas object.

* * *

## to_tuple_shape function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L58-L62 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.to_tuple_shape "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-51-1)to_tuple_shape(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-51-2)    shape
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-51-3))
    

Convert a shape-like object to a tuple.

* * *

## unstack_to_array function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L1938-L1998 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.unstack_to_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-52-1)unstack_to_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-52-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-52-3)    levels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-52-4)    sort=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-52-5)    return_indexes=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-52-6))
    

Reshape `obj` based on its multi-index into a multi-dimensional array.

Use `levels` to specify what index levels to unstack and in which order.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-2)>>> from vectorbtpro.base.reshaping import unstack_to_array
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-4)>>> index = pd.MultiIndex.from_arrays(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-5)...     [[1, 1, 2, 2], [3, 4, 3, 4], ['a', 'b', 'c', 'd']])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-6)>>> sr = pd.Series([1, 2, 3, 4], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-8)>>> unstack_to_array(sr).shape
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-9)(2, 2, 4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-11)>>> unstack_to_array(sr)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-12)[[[ 1. nan nan nan]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-13) [nan  2. nan nan]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-15) [[nan nan  3. nan]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-16)[nan nan nan  4.]]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-17)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-18)>>> unstack_to_array(sr, levels=(2, 0))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-19)[[ 1. nan]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-20) [ 2. nan]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-21) [nan  3.]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-53-22) [nan  4.]]
    

* * *

## unstack_to_df function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L2069-L2121 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.unstack_to_df "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-54-1)unstack_to_df(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-54-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-54-3)    index_levels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-54-4)    column_levels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-54-5)    symmetric=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-54-6)    sort=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-54-7))
    

Reshape `obj` based on its multi-index into a DataFrame.

Use `index_levels` to specify what index levels will form new index, and `column_levels` for new columns. Set `symmetric` to True to make DataFrame symmetric.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-2)>>> from vectorbtpro.base.reshaping import unstack_to_df
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-4)>>> index = pd.MultiIndex.from_arrays(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-5)...     [[1, 1, 2, 2], [3, 4, 3, 4], ['a', 'b', 'c', 'd']],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-6)...     names=['x', 'y', 'z'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-7)>>> sr = pd.Series([1, 2, 3, 4], index=index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-9)>>> unstack_to_df(sr, index_levels=(0, 1), column_levels=2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-10)z      a    b    c    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-11)x y
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-12)1 3  1.0  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-13)1 4  NaN  2.0  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-14)2 3  NaN  NaN  3.0  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-55-15)2 4  NaN  NaN  NaN  4.0
    

* * *

## wrap_broadcasted function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L584-L623 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.wrap_broadcasted "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-1)wrap_broadcasted(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-2)    new_obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-3)    old_obj=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-4)    axis=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-5)    is_pd=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-6)    new_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-7)    new_columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-8)    ignore_ranges=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-56-9))
    

If the newly brodcasted array was originally a Pandas object, make it Pandas object again and assign it the newly broadcast index/columns.

* * *

## BCO class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L713-L756 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-57-1)BCO(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-57-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-57-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-57-4))
    

Class that represents an object passed to [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "vectorbtpro.base.reshaping.broadcast").

If any value is None, mostly defaults to the global value passed to [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast "vectorbtpro.base.reshaping.broadcast").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.attr_.DefineMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.attr_.DefineMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.attr_.DefineMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.attr_.DefineMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.attr_.DefineMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.attr_.DefineMixin.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.attr_.DefineMixin.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing")
  * [DefineMixin.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.attr_.DefineMixin.fields")
  * [DefineMixin.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.attr_.DefineMixin.fields_dict")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.attr_.DefineMixin.get_field")
  * [DefineMixin.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.attr_.DefineMixin.hash")
  * [DefineMixin.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.attr_.DefineMixin.hash_key")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.attr_.DefineMixin.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.attr_.DefineMixin.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.attr_.DefineMixin.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.attr_.DefineMixin.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.attr_.DefineMixin.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.attr_.DefineMixin.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.attr_.DefineMixin.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### axis field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.axis "Permanent link")

Axis to broadcast.

Set to None to broadcast all axes.

* * *

### context field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.context "Permanent link")

Context used in evaluation of templates.

Will be merged over `template_context`.

* * *

### expand_axis field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.expand_axis "Permanent link")

Axis to expand if the array is 1-dim but the target shape is 2-dim.

* * *

### keep_flex field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.keep_flex "Permanent link")

Whether to keep the raw version of the output for flexible indexing.

Only makes sure that the array can broadcast to the target shape.

* * *

### merge_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.merge_kwargs "Permanent link")

Keyword arguments passed to [column_stack_merge](https://vectorbt.pro/pvt_7a467f6b/api/base/merging/#vectorbtpro.base.merging.column_stack_merge "vectorbtpro.base.merging.column_stack_merge").

* * *

### min_ndim field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.min_ndim "Permanent link")

Minimum number of dimensions.

* * *

### post_func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.post_func "Permanent link")

Function to post-process the output array.

* * *

### reindex_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.reindex_kwargs "Permanent link")

Keyword arguments passed to `pd.DataFrame.reindex`.

* * *

### require_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.require_kwargs "Permanent link")

Keyword arguments passed to `np.require`.

* * *

### to_pd field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.to_pd "Permanent link")

Whether to convert the output array to a Pandas object.

* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO.value "Permanent link")

Value of the object.

* * *

## Default class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L759-L764 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Default "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-58-1)Default(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-58-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-58-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-58-4))
    

Class for wrapping default values.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.attr_.DefineMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.attr_.DefineMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.attr_.DefineMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.attr_.DefineMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.attr_.DefineMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.attr_.DefineMixin.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.attr_.DefineMixin.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing")
  * [DefineMixin.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.attr_.DefineMixin.fields")
  * [DefineMixin.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.attr_.DefineMixin.fields_dict")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.attr_.DefineMixin.get_field")
  * [DefineMixin.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.attr_.DefineMixin.hash")
  * [DefineMixin.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.attr_.DefineMixin.hash_key")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.attr_.DefineMixin.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.attr_.DefineMixin.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.attr_.DefineMixin.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.attr_.DefineMixin.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.attr_.DefineMixin.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.attr_.DefineMixin.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.attr_.DefineMixin.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Default.value "Permanent link")

Default value.

* * *

## Ref class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py#L767-L772 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Ref "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-59-1)Ref(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-59-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-59-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#__codelineno-59-4))
    

Class for wrapping references to other values.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.attr_.DefineMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.attr_.DefineMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.attr_.DefineMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.attr_.DefineMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.attr_.DefineMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.attr_.DefineMixin.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.attr_.DefineMixin.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing")
  * [DefineMixin.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.attr_.DefineMixin.fields")
  * [DefineMixin.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.attr_.DefineMixin.fields_dict")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.attr_.DefineMixin.get_field")
  * [DefineMixin.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.attr_.DefineMixin.hash")
  * [DefineMixin.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.attr_.DefineMixin.hash_key")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.attr_.DefineMixin.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.attr_.DefineMixin.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.attr_.DefineMixin.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.attr_.DefineMixin.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.attr_.DefineMixin.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.attr_.DefineMixin.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.attr_.DefineMixin.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### key field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/reshaping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Ref.key "Permanent link")

Reference to another key.
