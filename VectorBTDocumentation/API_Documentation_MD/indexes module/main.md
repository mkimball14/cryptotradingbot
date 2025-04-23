#  indexes module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes "Permanent link")

Functions for working with indexes: index and columns.

They perform operations on index objects, such as stacking, combining, and cleansing MultiIndex levels.

Note

"Index" in pandas context is referred to both index and columns.

* * *

## align_arr_indices_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L650-L661 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.align_arr_indices_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-0-1)align_arr_indices_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-0-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-0-3)    b
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-0-4))
    

Return indices required to align `a` to `b`.

* * *

## align_index_to function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L664-L727 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.align_index_to "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-1-1)align_index_to(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-1-2)    index1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-1-3)    index2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-1-4)    jitted=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-1-5))
    

Align `index1` to have the same shape as `index2` if they have any levels in common.

Returns index slice for the aligning.

* * *

## align_indexes function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L730-L752 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.align_indexes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-2-1)align_indexes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-2-2)    *indexes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-2-3)    return_new_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-2-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-2-5))
    

Align multiple indexes to each other with [align_index_to](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.align_index_to "vectorbtpro.base.indexes.align_index_to").

* * *

## block_index_product_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L755-L799 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.block_index_product_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-3-1)block_index_product_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-3-2)    block_group_map1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-3-3)    block_group_map2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-3-4)    factorized1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-3-5)    factorized2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-3-6))
    

Return indices required for building a block-wise Cartesian product of two factorized indexes.

* * *

## clean_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L169-L198 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.clean_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-4-1)clean_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-4-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-4-3)    drop_duplicates=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-4-4)    keep=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-4-5)    drop_redundant=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-4-6))
    

Clean index.

Set `drop_duplicates` to True to remove duplicate levels.

For details on `keep`, see [drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.drop_duplicate_levels "vectorbtpro.base.indexes.drop_duplicate_levels").

Set `drop_redundant` to True to use [drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.drop_redundant_levels "vectorbtpro.base.indexes.drop_redundant_levels").

* * *

## combine_index_with_keys function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L243-L264 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.combine_index_with_keys "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-5-1)combine_index_with_keys(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-5-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-5-3)    keys,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-5-4)    lens,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-5-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-5-6))
    

Build keys based on index lengths.

* * *

## combine_indexes function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L226-L240 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.combine_indexes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-6-1)combine_indexes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-6-2)    *indexes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-6-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-6-4))
    

Combine each index in `indexes` using Cartesian product.

Keyword arguments will be passed to [stack_indexes](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.stack_indexes "vectorbtpro.base.indexes.stack_indexes").

* * *

## concat_indexes function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L267-L444 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.concat_indexes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-7-1)concat_indexes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-7-2)    *indexes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-7-3)    index_concat_method='append',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-7-4)    keys=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-7-5)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-7-6)    verify_integrity=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-7-7)    axis=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-7-8))
    

Concatenate indexes.

The following index concatenation methods are supported:

  * 'append': append one index to another
  * 'union': build a union of indexes
  * 'pd_concat': convert indexes to Pandas Series or DataFrames and use `pd.concat`
  * 'factorize': factorize the concatenated index
  * 'factorize_each': factorize each index and concatenate while keeping numbers unique
  * 'reset': reset the concatenated index without applying `keys`
  * Callable: a custom callable that takes the indexes and returns the concatenated index



Argument `index_concat_method` also accepts a tuple of two options: the second option gets applied if the first one fails.

Use `keys` as an index with the same number of elements as there are indexes to add another index level on top of the concatenated indexes.

If `verify_integrity` is True and `keys` is None, performs various checks depending on the axis.

* * *

## cross_index_with function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L802-L882 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.cross_index_with "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-8-1)cross_index_with(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-8-2)    index1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-8-3)    index2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-8-4)    return_new_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-8-5))
    

Build a Cartesian product of one index with another while taking into account levels they have in common.

Returns index slices for the aligning.

* * *

## cross_indexes function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L885-L916 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.cross_indexes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-9-1)cross_indexes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-9-2)    *indexes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-9-3)    return_new_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-9-4))
    

Cross multiple indexes with [cross_index_with](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.cross_index_with "vectorbtpro.base.indexes.cross_index_with").

* * *

## drop_duplicate_levels function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L614-L647 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.drop_duplicate_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-10-1)drop_duplicate_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-10-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-10-3)    keep=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-10-4))
    

Drop levels in `index` with the same name and values.

Set `keep` to 'last' to keep last levels, otherwise 'first'.

Set `keep` to None to use the default.

* * *

## drop_levels function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L447-L497 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.drop_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-11-1)drop_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-11-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-11-3)    levels,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-11-4)    strict=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-11-5))
    

Drop `levels` in `index` by their name(s)/position(s).

Provide `levels` as an instance of [ExceptLevel](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.ExceptLevel "vectorbtpro.base.indexes.ExceptLevel") to drop everything apart from the specified levels.

* * *

## drop_redundant_levels function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L598-L611 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.drop_redundant_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-12-1)drop_redundant_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-12-2)    index
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-12-3))
    

Drop levels in `index` that either have a single unnamed value or a range from 0 to n.

* * *

## find_first_occurrence function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L980-L989 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.find_first_occurrence "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-13-1)find_first_occurrence(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-13-2)    index_value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-13-3)    index
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-13-4))
    

Return index of the first occurrence in `index`.

* * *

## get_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L58-L71 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.get_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-14-1)get_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-14-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-14-3)    axis
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-14-4))
    

Get index of `obj` by `axis`.

* * *

## index_from_values function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L74-L126 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.index_from_values "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-15-1)index_from_values(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-15-2)    values,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-15-3)    single_value=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-15-4)    name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-15-5))
    

Create a new `pd.Index` with `name` by parsing an iterable `values`.

Each in `values` will correspond to an element in the new index.

* * *

## pick_levels function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L922-L977 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.pick_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-16-1)pick_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-16-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-16-3)    required_levels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-16-4)    optional_levels=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-16-5))
    

Pick optional and required levels and return their indices.

Raises an exception if index has less or more levels than expected.

* * *

## rename_levels function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L500-L539 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.rename_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-17-1)rename_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-17-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-17-3)    mapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-17-4)    strict=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-17-5))
    

Rename levels in `index` by `mapper`.

Mapper can be a single or multiple levels to rename to, or a dictionary that maps old level names to new level names.

* * *

## repeat_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L129-L145 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.repeat_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-18-1)repeat_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-18-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-18-3)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-18-4)    ignore_ranges=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-18-5))
    

Repeat each element in `index` `n` times.

Set `ignore_ranges` to True to ignore indexes of type `pd.RangeIndex`.

* * *

## select_levels function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L542-L595 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.select_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-19-1)select_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-19-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-19-3)    levels,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-19-4)    strict=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-19-5))
    

Build a new index by selecting one or multiple `levels` from `index`.

Provide `levels` as an instance of [ExceptLevel](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.ExceptLevel "vectorbtpro.base.indexes.ExceptLevel") to select everything apart from the specified levels.

* * *

## stack_indexes function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L201-L223 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.stack_indexes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-20-1)stack_indexes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-20-2)    *indexes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-20-3)    **clean_index_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-20-4))
    

Stack each index in `indexes` on top of each other, from top to bottom.

* * *

## tile_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L148-L166 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.tile_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-21-1)tile_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-21-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-21-3)    n,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-21-4)    ignore_ranges=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-21-5))
    

Tile the whole `index` `n` times.

Set `ignore_ranges` to True to ignore indexes of type `pd.RangeIndex`.

* * *

## to_any_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L47-L55 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.to_any_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-22-1)to_any_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-22-2)    index_like
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-22-3))
    

Convert any index-like object to an index.

Index objects are kept as-is.

* * *

## ExceptLevel class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L39-L44 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.ExceptLevel "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-23-1)ExceptLevel(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-23-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-23-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-23-4))
    

Class for grouping except one or more levels.

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

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.ExceptLevel.value "Permanent link")

One or more level positions or names.

* * *

## IndexApplier class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L995-L1097 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-24-1)IndexApplier()
    

Abstract class that can apply a function on an index.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



**Subclasses**

  * [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper")
  * [BaseIDXAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor "vectorbtpro.base.accessors.BaseIDXAccessor")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



* * *

### add_levels method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L1002-L1032 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-25-1)IndexApplier.add_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-25-2)    *indexes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-25-3)    on_top=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-25-4)    drop_duplicates=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-25-5)    keep=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-25-6)    drop_redundant=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-25-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-25-8))
    

Append or prepend levels using [stack_indexes](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.stack_indexes "vectorbtpro.base.indexes.stack_indexes").

Set `on_top` to False to stack at bottom.

See [IndexApplier.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.indexes.IndexApplier.apply_to_index") for other keyword arguments.

* * *

### apply_to_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L998-L1000 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-26-1)IndexApplier.apply_to_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-26-2)    apply_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-26-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-26-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-26-5))
    

Apply function `apply_func` on the index of the instance and return a new instance.

* * *

### drop_duplicate_levels method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L1089-L1097 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-27-1)IndexApplier.drop_duplicate_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-27-2)    keep=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-27-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-27-4))
    

Drop any duplicate levels using [drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.drop_duplicate_levels "vectorbtpro.base.indexes.drop_duplicate_levels").

See [IndexApplier.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.indexes.IndexApplier.apply_to_index") for other keyword arguments.

* * *

### drop_levels method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L1034-L1047 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-28-1)IndexApplier.drop_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-28-2)    levels,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-28-3)    strict=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-28-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-28-5))
    

Drop levels using [drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.drop_levels "vectorbtpro.base.indexes.drop_levels").

See [IndexApplier.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.indexes.IndexApplier.apply_to_index") for other keyword arguments.

* * *

### drop_redundant_levels method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L1079-L1087 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-29-1)IndexApplier.drop_redundant_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-29-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-29-3))
    

Drop any redundant levels using [drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.drop_redundant_levels "vectorbtpro.base.indexes.drop_redundant_levels").

See [IndexApplier.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.indexes.IndexApplier.apply_to_index") for other keyword arguments.

* * *

### rename_levels method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L1049-L1062 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-30-1)IndexApplier.rename_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-30-2)    mapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-30-3)    strict=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-30-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-30-5))
    

Rename levels using [rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.rename_levels "vectorbtpro.base.indexes.rename_levels").

See [IndexApplier.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.indexes.IndexApplier.apply_to_index") for other keyword arguments.

* * *

### select_levels method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexes.py#L1064-L1077 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-31-1)IndexApplier.select_levels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-31-2)    level_names,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-31-3)    strict=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-31-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#__codelineno-31-5))
    

Select levels using [select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.select_levels "vectorbtpro.base.indexes.select_levels").

See [IndexApplier.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.indexes.IndexApplier.apply_to_index") for other keyword arguments.
