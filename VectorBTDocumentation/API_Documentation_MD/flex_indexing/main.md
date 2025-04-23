flex_indexing

#  flex_indexing module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing "Permanent link")

Classes and functions for flexible indexing.

* * *

## flex_choose_i_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L32-L42 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_choose_i_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-0-1)flex_choose_i_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-0-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-0-3)    i
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-0-4))
    

Choose a position in an array as if it has been broadcast against rows or columns.

Note

Array must be one-dimensional.

* * *

## flex_choose_i_and_col_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L147-L175 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_choose_i_and_col_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-1-1)flex_choose_i_and_col_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-1-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-1-3)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-1-4)    col,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-1-5)    rotate_rows=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-1-6)    rotate_cols=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-1-7))
    

Choose a position in an array as if it has been broadcast rows and columns.

Can use rotational indexing along rows and columns.

Note

Array must be two-dimensional.

* * *

## flex_choose_i_pc_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L101-L115 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_choose_i_pc_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-2-1)flex_choose_i_pc_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-2-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-2-3)    col,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-2-4)    rotate_cols=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-2-5))
    

Choose a position in an array as if it has been broadcast against columns.

Can use rotational indexing along columns.

Note

Array must be one-dimensional.

* * *

## flex_choose_i_pc_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L118-L132 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_choose_i_pc_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-3-1)flex_choose_i_pc_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-3-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-3-3)    col,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-3-4)    rotate_cols=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-3-5))
    

Choose a position in an array as if it has been broadcast against columns.

Can use rotational indexing along columns.

Note

Array must be two-dimensional.

* * *

## flex_choose_i_pr_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L55-L69 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_choose_i_pr_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-4-1)flex_choose_i_pr_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-4-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-4-3)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-4-4)    rotate_rows=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-4-5))
    

Choose a position in an array as if it has been broadcast against rows.

Can use rotational indexing along rows.

Note

Array must be one-dimensional.

* * *

## flex_choose_i_pr_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L72-L86 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_choose_i_pr_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-5-1)flex_choose_i_pr_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-5-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-5-3)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-5-4)    rotate_rows=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-5-5))
    

Choose a position in an array as if it has been broadcast against rows.

Can use rotational indexing along rows.

Note

Array must be two-dimensional.

* * *

## flex_select_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L45-L52 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_select_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-6-1)flex_select_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-6-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-6-3)    i
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-6-4))
    

Select an element of an array as if it has been broadcast against rows or columns.

Note

Array must be one-dimensional.

* * *

## flex_select_1d_pc_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L135-L144 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_select_1d_pc_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-7-1)flex_select_1d_pc_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-7-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-7-3)    col,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-7-4)    rotate_cols=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-7-5))
    

Select an element of an array as if it has been broadcast against columns.

Can use rotational indexing along columns.

Note

Array must be one-dimensional.

* * *

## flex_select_1d_pr_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L89-L98 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_select_1d_pr_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-8-1)flex_select_1d_pr_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-8-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-8-3)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-8-4)    rotate_rows=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-8-5))
    

Select an element of an array as if it has been broadcast against rows.

Can use rotational indexing along rows.

Note

Array must be one-dimensional.

* * *

## flex_select_2d_col_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L232-L239 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_select_2d_col_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-9-1)flex_select_2d_col_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-9-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-9-3)    col,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-9-4)    rotate_cols=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-9-5))
    

Select a column from a flexible 2-dim array. Returns a 2-dim array.

Note

Array must be two-dimensional.

* * *

## flex_select_2d_row_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L222-L229 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_select_2d_row_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-10-1)flex_select_2d_row_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-10-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-10-3)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-10-4)    rotate_rows=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-10-5))
    

Select a row from a flexible 2-dim array. Returns a 2-dim array.

Note

Array must be two-dimensional.

* * *

## flex_select_col_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L212-L219 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_select_col_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-11-1)flex_select_col_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-11-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-11-3)    col,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-11-4)    rotate_cols=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-11-5))
    

Select a column from a flexible 2-dim array. Returns a 1-dim array.

Note

Array must be two-dimensional.

* * *

## flex_select_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L178-L199 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_select_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-12-1)flex_select_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-12-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-12-3)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-12-4)    col,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-12-5)    rotate_rows=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-12-6)    rotate_cols=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-12-7))
    

Select element of an array as if it has been broadcast rows and columns.

Can use rotational indexing along rows and columns.

Note

Array must be two-dimensional.

* * *

## flex_select_row_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/flex_indexing.py#L202-L209 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#vectorbtpro.base.flex_indexing.flex_select_row_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-13-1)flex_select_row_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-13-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-13-3)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-13-4)    rotate_rows=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/#__codelineno-13-5))
    

Select a row from a flexible 2-dim array. Returns a 1-dim array.

Note

Array must be two-dimensional.
