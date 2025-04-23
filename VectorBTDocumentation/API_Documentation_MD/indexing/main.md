indexing

#  indexing module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing "Permanent link")

Classes and functions for indexing.

* * *

## build_param_indexer function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L413-L504 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.build_param_indexer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-0-1)build_param_indexer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-0-2)    param_names,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-0-3)    class_name='ParamIndexer',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-0-4)    module_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-0-5))
    

A factory to create a class with parameter indexing.

Parameter indexer enables accessing a group of rows and columns by a parameter array (similar to `loc`). This way, one can query index/columns by another Series called a parameter mapper, which is just a `pd.Series` that maps columns (its index) to params (its values).

Parameter indexing is important, since querying by column/index labels alone is not always the best option. For example, `pandas` doesn't let you query by list at a specific index/column level.

**Args**

**`param_names`** : `list` of `str`
    Names of the parameters.
**`class_name`** : `str`
    Name of the generated class.
**`module_name`** : `str`
    Name of the module to which the class should be bound.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-2)>>> from vectorbtpro.base.indexing import build_param_indexer, indexing_on_mapper
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-4)>>> MyParamIndexer = build_param_indexer(['my_param'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-5)>>> class C(MyParamIndexer):
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-6)...     def __init__(self, df, param_mapper):
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-7)...         self.df = df
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-8)...         self._my_param_mapper = param_mapper
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-9)...         super().__init__([param_mapper])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-10)...
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-11)...     def indexing_func(self, pd_indexing_func):
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-12)...         return type(self)(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-13)...             pd_indexing_func(self.df),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-14)...             indexing_on_mapper(self._my_param_mapper, self.df, pd_indexing_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-15)...         )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-16)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-17)>>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-18)>>> param_mapper = pd.Series(['First', 'Second'], index=['a', 'b'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-19)>>> c = C(df, param_mapper)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-21)>>> c.my_param_loc['First'].df
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-22)0    1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-23)1    2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-24)Name: a, dtype: int64
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-25)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-26)>>> c.my_param_loc['Second'].df
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-27)0    3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-28)1    4
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-29)Name: b, dtype: int64
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-30)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-31)>>> c.my_param_loc[['First', 'First', 'Second', 'Second']].df
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-32)      a     b
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-33)0  1  1  3  3
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-1-34)1  2  2  4  4
    

* * *

## get_idxs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2241-L2256 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.get_idxs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-2-1)get_idxs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-2-2)    idxr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-2-3)    index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-2-4)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-2-5)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-2-6)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-2-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-2-8))
    

Translate indexer to row and column indices.

If `idxr` is not an indexer class, wraps it with [Idxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr "vectorbtpro.base.indexing.Idxr").

Keyword arguments are passed when constructing a new [Idxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr "vectorbtpro.base.indexing.Idxr").

* * *

## get_index_points function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L1096-L1301 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.get_index_points "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-1)get_index_points(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-3)    every=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-4)    normalize_every=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-5)    at_time=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-6)    start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-7)    end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-8)    exact_start=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-9)    on=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-10)    add_delta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-11)    kind=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-12)    indexer_method='bfill',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-13)    indexer_tolerance=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-14)    skip_not_found=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-3-15))
    

Translate indices or labels into index points.

See [PointIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr "vectorbtpro.base.indexing.PointIdxr") for arguments.

**Usage**

  * Provide nothing to generate at the beginning:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-4-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-4-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-4-3)>>> index = pd.date_range("2020-01", "2020-02", freq="1d")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-4-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-4-5)>>> vbt.get_index_points(index)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-4-6)array([0])
    

  * Provide `every` as an integer frequency to generate index points using NumPy:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-1)>>> # Generate a point every five rows
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-2)>>> vbt.get_index_points(index, every=5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-3)array([ 0,  5, 10, 15, 20, 25, 30])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-5)>>> # Generate a point every five rows starting at 6th row
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-6)>>> vbt.get_index_points(index, every=5, start=5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-7)array([ 5, 10, 15, 20, 25, 30])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-9)>>> # Generate a point every five rows from 6th to 16th row
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-10)>>> vbt.get_index_points(index, every=5, start=5, end=15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-5-11)array([ 5, 10])
    

  * Provide `every` as a time delta frequency to generate index points using Pandas:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-1)>>> # Generate a point every week
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-2)>>> vbt.get_index_points(index, every="W")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-3)array([ 4, 11, 18, 25])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-5)>>> # Generate a point every second day of the week
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-6)>>> vbt.get_index_points(index, every="W", add_delta="2d")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-7)array([ 6, 13, 20, 27])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-9)>>> # Generate a point every week, starting at 11th row
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-10)>>> vbt.get_index_points(index, every="W", start=10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-11)array([11, 18, 25])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-13)>>> # Generate a point every week, starting exactly at 11th row
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-14)>>> vbt.get_index_points(index, every="W", start=10, exact_start=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-15)array([10, 11, 18, 25])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-16)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-17)>>> # Generate a point every week, starting at 2020-01-10
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-18)>>> vbt.get_index_points(index, every="W", start="2020-01-10")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-6-19)array([11, 18, 25])
    

  * Instead of using `every`, provide indices explicitly:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-7-1)>>> # Generate one point
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-7-2)>>> vbt.get_index_points(index, on="2020-01-07")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-7-3)array([6])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-7-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-7-5)>>> # Generate multiple points
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-7-6)>>> vbt.get_index_points(index, on=["2020-01-07", "2020-01-14"])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-7-7)array([ 6, 13])
    

* * *

## get_index_ranges function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L1434-L1894 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.get_index_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-1)get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-3)    index_freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-4)    every=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-5)    normalize_every=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-6)    split_every=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-7)    start_time=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-8)    end_time=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-9)    lookback_period=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-10)    start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-11)    end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-12)    exact_start=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-13)    fixed_start=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-14)    closed_start=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-15)    closed_end=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-16)    add_start_delta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-17)    add_end_delta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-18)    kind=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-19)    skip_not_found=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-20)    jitted=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-8-21))
    

Translate indices, labels, or bounds into index ranges.

See [RangeIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr "vectorbtpro.base.indexing.RangeIdxr") for arguments.

**Usage**

  * Provide nothing to generate one largest index range:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-9-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-9-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-9-3)>>> index = pd.date_range("2020-01", "2020-02", freq="1d")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-9-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-9-5)>>> np.column_stack(vbt.get_index_ranges(index))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-9-6)array([[ 0, 32]])
    

  * Provide `every` as an integer frequency to generate index ranges using NumPy:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-1)>>> # Generate a range every five rows
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-2)>>> np.column_stack(vbt.get_index_ranges(index, every=5))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-3)array([[ 0,  5],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-4)       [ 5, 10],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-5)       [10, 15],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-6)       [15, 20],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-7)       [20, 25],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-8)       [25, 30]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-10)>>> # Generate a range every five rows, starting at 6th row
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-11)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-12)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-13)...     every=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-14)...     start=5
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-15)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-16)array([[ 5, 10],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-17)       [10, 15],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-18)       [15, 20],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-19)       [20, 25],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-20)       [25, 30]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-21)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-22)>>> # Generate a range every five rows from 6th to 16th row
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-23)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-24)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-25)...     every=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-26)...     start=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-27)...     end=15
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-28)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-29)array([[ 5, 10],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-10-30)       [10, 15]])
    

  * Provide `every` as a time delta frequency to generate index ranges using Pandas:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-1)>>> # Generate a range every week
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-2)>>> np.column_stack(vbt.get_index_ranges(index, every="W"))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-3)array([[ 4, 11],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-4)       [11, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-5)       [18, 25]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-7)>>> # Generate a range every second day of the week
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-8)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-9)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-10)...     every="W",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-11)...     add_start_delta="2d"
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-12)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-13)array([[ 6, 11],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-14)       [13, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-15)       [20, 25]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-16)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-17)>>> # Generate a range every week, starting at 11th row
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-18)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-19)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-20)...     every="W",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-21)...     start=10
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-22)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-23)array([[11, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-24)       [18, 25]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-25)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-26)>>> # Generate a range every week, starting exactly at 11th row
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-27)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-28)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-29)...     every="W",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-30)...     start=10,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-31)...     exact_start=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-32)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-33)array([[10, 11],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-34)       [11, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-35)       [18, 25]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-36)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-37)>>> # Generate a range every week, starting at 2020-01-10
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-38)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-39)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-40)...     every="W",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-41)...     start="2020-01-10"
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-42)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-43)array([[11, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-44)       [18, 25]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-45)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-46)>>> # Generate a range every week, each starting at 2020-01-10
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-47)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-48)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-49)...     every="W",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-50)...     start="2020-01-10",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-51)...     fixed_start=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-52)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-53)array([[11, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-54)       [11, 25]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-55)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-56)>>> # Generate an expanding range that increments by week
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-57)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-58)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-59)...     every="W",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-60)...     start=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-61)...     exact_start=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-62)...     fixed_start=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-63)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-64)array([[ 0,  4],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-65)       [ 0, 11],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-66)       [ 0, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-11-67)       [ 0, 25]])
    

  * Use a look-back period (instead of an end index):


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-1)>>> # Generate a range every week, looking 5 days back
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-2)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-3)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-4)...     every="W",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-5)...     lookback_period=5
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-6)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-7)array([[ 6, 11],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-8)       [13, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-9)       [20, 25]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-11)>>> # Generate a range every week, looking 2 weeks back
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-12)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-13)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-14)...     every="W",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-15)...     lookback_period="2W"
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-16)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-17)array([[ 0, 11],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-18)       [ 4, 18],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-12-19)       [11, 25]])
    

  * Instead of using `every`, provide start and end indices explicitly:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-1)>>> # Generate one range
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-2)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-3)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-4)...     start="2020-01-01",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-5)...     end="2020-01-07"
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-6)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-7)array([[0, 6]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-9)>>> # Generate ranges between multiple dates
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-10)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-11)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-12)...     start=["2020-01-01", "2020-01-07"],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-13)...     end=["2020-01-07", "2020-01-14"]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-14)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-15)array([[ 0,  6],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-16)       [ 6, 13]])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-17)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-18)>>> # Generate ranges with a fixed start
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-19)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-20)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-21)...     start="2020-01-01",
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-22)...     end=["2020-01-07", "2020-01-14"]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-23)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-24)array([[ 0,  6],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-13-25)       [ 0, 13]])
    

  * Use `closed_start` and `closed_end` to exclude any of the bounds:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-1)>>> # Generate ranges between multiple dates
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-2)>>> # by excluding the start date and including the end date
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-3)>>> np.column_stack(vbt.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-4)...     index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-5)...     start=["2020-01-01", "2020-01-07"],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-6)...     end=["2020-01-07", "2020-01-14"],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-7)...     closed_start=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-8)...     closed_end=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-9)... ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-10)array([[ 1,  7],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-14-11)       [ 7, 14]])
    

* * *

## indexing_on_mapper function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L389-L410 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.indexing_on_mapper "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-15-1)indexing_on_mapper(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-15-2)    mapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-15-3)    ref_obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-15-4)    pd_indexing_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-15-5))
    

Broadcast `mapper` Series to `ref_obj` and perform pandas indexing using `pd_indexing_func`.

* * *

## normalize_idxs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L615-L629 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.normalize_idxs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-16-1)normalize_idxs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-16-2)    idxs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-16-3)    target_len
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-16-4))
    

Normalize indexes into a 1-dim integer array.

* * *

## AutoIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L1897-L2105 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-17-1)AutoIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-17-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-17-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-17-4))
    

Class for resolving indices, datetime-like objects, frequency-like objects, and labels for one axis.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### above_to_len field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.above_to_len "Permanent link")

Whether to place `len(index)` instead of -1 if [AutoIdxr.value](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.value "vectorbtpro.base.indexing.AutoIdxr.value") is above the last index.

* * *

### below_to_zero field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.below_to_zero "Permanent link")

Whether to place 0 instead of -1 if [AutoIdxr.value](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.value "vectorbtpro.base.indexing.AutoIdxr.value") is below the first index.

* * *

### closed_end field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.closed_end "Permanent link")

Whether slice end should be inclusive.

* * *

### closed_start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.closed_start "Permanent link")

Whether slice start should be inclusive.

* * *

### idxr_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.idxr_kwargs "Permanent link")

Keyword arguments passed to the selected indexer.

* * *

### indexer_method field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.indexer_method "Permanent link")

Method for `pd.Index.get_indexer`.

* * *

### kind field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.kind "Permanent link")

Kind of value.

Allowed are

  * "position(s)" for [PosIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PosIdxr "vectorbtpro.base.indexing.PosIdxr")
  * "mask" for [MaskIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.MaskIdxr "vectorbtpro.base.indexing.MaskIdxr")
  * "label(s)" for [LabelIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr "vectorbtpro.base.indexing.LabelIdxr")
  * "datetime" for [DatetimeIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr "vectorbtpro.base.indexing.DatetimeIdxr")
  * "dtc": for [DTCIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr "vectorbtpro.base.indexing.DTCIdxr")
  * "frequency" for [PointIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr "vectorbtpro.base.indexing.PointIdxr")



If None, will (try to) determine automatically based on the type of indices.

* * *

### level field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.level "Permanent link")

One or more levels.

If `level` is not None and `kind` is None, `kind` becomes "labels".

* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr.value "Permanent link")

One or more integer indices, datetime-like objects, frequency-like objects, or labels.

Can also be an instance of [PosSel](https://vectorbt.pro/pvt_7a467f6b/api/utils/selection/#vectorbtpro.utils.selection.PosSel "vectorbtpro.utils.selection.PosSel") holding position(s) and [LabelSel](https://vectorbt.pro/pvt_7a467f6b/api/utils/selection/#vectorbtpro.utils.selection.LabelSel "vectorbtpro.utils.selection.LabelSel") holding label(s).

* * *

## ColIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2140-L2168 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-18-1)ColIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-18-2)    idxr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-18-3)    **idxr_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-18-4))
    

Class for resolving column indices.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IdxrBase.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IdxrBase.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IdxrBase.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IdxrBase.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IdxrBase.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IdxrBase.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.IdxrBase.check_idxs")
  * [IdxrBase.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.IdxrBase.get")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.IdxrBase.slice_indexer")



* * *

### idxr field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr.idxr "Permanent link")

Indexer.

Can be an instance of [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr"), a custom template, or a value to be wrapped with [AutoIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr "vectorbtpro.base.indexing.AutoIdxr").

* * *

### idxr_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr.idxr_kwargs "Permanent link")

Keyword arguments passed to [AutoIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr "vectorbtpro.base.indexing.AutoIdxr").

* * *

## DTCIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L933-L1002 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-19-1)DTCIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-19-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-19-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-19-4))
    

Class for resolving indices provided as datetime-like components.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### closed_end field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr.closed_end "Permanent link")

Whether slice end should be inclusive.

* * *

### closed_start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr.closed_start "Permanent link")

Whether slice start should be inclusive.

* * *

### get_dtc_namedtuple static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L953-L962 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr.get_dtc_namedtuple "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-20-1)DTCIdxr.get_dtc_namedtuple(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-20-2)    value=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-20-3)    **parse_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-20-4))
    

Convert a value to a [DTCNT](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT "vectorbtpro.utils.datetime_.DTCNT") instance.

* * *

### jitted field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr.jitted "Permanent link")

Jitting option passed to [index_matches_dtc_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.index_matches_dtc_nb "vectorbtpro.utils.datetime_nb.index_matches_dtc_nb") and [index_within_dtc_range_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.index_within_dtc_range_nb "vectorbtpro.utils.datetime_nb.index_within_dtc_range_nb").

* * *

### parse_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr.parse_kwargs "Permanent link")

Keyword arguments passed to [DTC.parse](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.parse "vectorbtpro.utils.datetime_.DTC.parse").

* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr.value "Permanent link")

One or more datetime-like components.

* * *

## DatetimeIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L855-L930 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-21-1)DatetimeIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-21-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-21-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-21-4))
    

Class for resolving indices provided as datetime-like objects.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### above_to_len field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr.above_to_len "Permanent link")

Whether to place `len(index)` instead of -1 if [DatetimeIdxr.value](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr.value "vectorbtpro.base.indexing.DatetimeIdxr.value") is above the last index.

* * *

### below_to_zero field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr.below_to_zero "Permanent link")

Whether to place 0 instead of -1 if [DatetimeIdxr.value](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr.value "vectorbtpro.base.indexing.DatetimeIdxr.value") is below the first index.

* * *

### closed_end field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr.closed_end "Permanent link")

Whether slice end should be inclusive.

* * *

### closed_start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr.closed_start "Permanent link")

Whether slice start should be inclusive.

* * *

### indexer_method field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr.indexer_method "Permanent link")

Method for `pd.Index.get_indexer`.

Allows two additional values: "before" and "after".

* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr.value "Permanent link")

One or more datetime-like objects.

* * *

## ExtPandasIndexer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L288-L300 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-22-1)ExtPandasIndexer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-22-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-22-3))
    

Extension of [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer") that also implements indexing using [xLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.xLoc "vectorbtpro.base.indexing.xLoc").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.PandasIndexer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.PandasIndexer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.PandasIndexer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.PandasIndexer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.PandasIndexer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.PandasIndexer.find_messages")
  * [IndexingBase.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_func "vectorbtpro.base.indexing.PandasIndexer.indexing_func")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.base.indexing.PandasIndexer.indexing_setter_func")
  * [PandasIndexer.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.base.indexing.PandasIndexer.iloc")
  * [PandasIndexer.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs")
  * [PandasIndexer.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.base.indexing.PandasIndexer.loc")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.base.indexing.PandasIndexer.xs")



**Subclasses**

  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")



* * *

### xloc class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L295-L298 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "Permanent link")

Subclass of [iLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.iLoc "vectorbtpro.base.indexing.iLoc") that transforms an [Idxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr "vectorbtpro.base.indexing.Idxr")-based operation with [get_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.get_idxs "vectorbtpro.base.indexing.get_idxs") to an [iLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.iLoc "vectorbtpro.base.indexing.iLoc") operation.

* * *

## IdxDict class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2543-L2551 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxDict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-23-1)IdxDict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-23-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-23-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-23-4))
    

Class for building an index setter from a dict.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxSetterFactory](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory "vectorbtpro.base.indexing.IdxSetterFactory")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IdxSetterFactory.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IdxSetterFactory.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IdxSetterFactory.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IdxSetterFactory.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IdxSetterFactory.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IdxSetterFactory.find_messages")
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
  * [IdxSetterFactory.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory.get "vectorbtpro.base.indexing.IdxSetterFactory.get")



* * *

### index_dct field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxDict.index_dct "Permanent link")

Dict that contains indexer objects as keys and values to be set as values.

* * *

## IdxFrame class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2593-L2662 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxFrame "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-24-1)IdxFrame(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-24-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-24-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-24-4))
    

Class for building an index setter from a DataFrame.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxSetterFactory](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory "vectorbtpro.base.indexing.IdxSetterFactory")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IdxSetterFactory.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IdxSetterFactory.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IdxSetterFactory.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IdxSetterFactory.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IdxSetterFactory.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IdxSetterFactory.find_messages")
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
  * [IdxSetterFactory.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory.get "vectorbtpro.base.indexing.IdxSetterFactory.get")



* * *

### colidx_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxFrame.colidx_kwargs "Permanent link")

Keyword arguments passed to `colidx` if the indexer isn't an instance of [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "vectorbtpro.base.indexing.ColIdxr").

* * *

### df field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxFrame.df "Permanent link")

DataFrame or any array-like object to create the DataFrame from.

* * *

### rowidx_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxFrame.rowidx_kwargs "Permanent link")

Keyword arguments passed to `rowidx` if the indexer isn't an instance of [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr").

* * *

### split field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxFrame.split "Permanent link")

Whether to split the setting operation.

If False, will set all values using a single operation. Otherwise, the following options are supported:

  * 'columns': one operation per column
  * 'rows': one operation per row
  * True or 'elements': one operation per element



* * *

## IdxRecords class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2665-L2821 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-25-1)IdxRecords(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-25-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-25-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-25-4))
    

Class for building index setters from records - one per field.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxSetterFactory](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory "vectorbtpro.base.indexing.IdxSetterFactory")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IdxSetterFactory.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IdxSetterFactory.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IdxSetterFactory.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IdxSetterFactory.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IdxSetterFactory.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IdxSetterFactory.find_messages")
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
  * [IdxSetterFactory.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory.get "vectorbtpro.base.indexing.IdxSetterFactory.get")



* * *

### col_field field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords.col_field "Permanent link")

Column field.

If None or True, will search for "col", "column", and "symbol" (case-insensitive).

If a record doesn't have a column field, all columns will be set. If there's no row and column field, the field value will become the default of the entire array.

* * *

### colidx_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords.colidx_kwargs "Permanent link")

Keyword arguments passed to `colidx` if the indexer isn't an instance of [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "vectorbtpro.base.indexing.ColIdxr").

* * *

### records field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords.records "Permanent link")

Series, DataFrame, or any sequence of mapping-like objects.

If a Series or DataFrame and the index is not a default range, the index will become a row field. If a custom row field is provided, the index will be ignored.

* * *

### row_field field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords.row_field "Permanent link")

Row field.

If None or True, will search for "row", "index", "open time", and "date" (case-insensitive). If [IdxRecords.records](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords.records "vectorbtpro.base.indexing.IdxRecords.records") is a Series or DataFrame, will also include the index name if the index is not a default range.

If a record doesn't have a row field, all rows will be set. If there's no row and column field, the field value will become the default of the entire array.

* * *

### rowidx_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords.rowidx_kwargs "Permanent link")

Keyword arguments passed to `rowidx` if the indexer isn't an instance of [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr").

* * *

## IdxSeries class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2554-L2590 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSeries "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-26-1)IdxSeries(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-26-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-26-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-26-4))
    

Class for building an index setter from a Series.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxSetterFactory](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory "vectorbtpro.base.indexing.IdxSetterFactory")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IdxSetterFactory.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IdxSetterFactory.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IdxSetterFactory.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IdxSetterFactory.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IdxSetterFactory.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IdxSetterFactory.find_messages")
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
  * [IdxSetterFactory.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory.get "vectorbtpro.base.indexing.IdxSetterFactory.get")



* * *

### idx_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSeries.idx_kwargs "Permanent link")

Keyword arguments passed to `idx` if the indexer isn't an instance of [Idxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr "vectorbtpro.base.indexing.Idxr").

* * *

### split field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSeries.split "Permanent link")

Whether to split the setting operation.

If False, will set all values using a single operation. Otherwise, will do one operation per element.

* * *

### sr field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSeries.sr "Permanent link")

Series or any array-like object to create the Series from.

* * *

## IdxSetter class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2273-L2532 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-27-1)IdxSetter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-27-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-27-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-27-4))
    

Class for setting values based on indexing.

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

### fill_and_set method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2502-L2532 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.fill_and_set "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-28-1)IdxSetter.fill_and_set(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-28-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-28-3)    keep_flex=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-28-4)    fill_value=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-28-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-28-6))
    

Fill a new array and set its values based on [IdxSetter.get_set_meta](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.get_set_meta "vectorbtpro.base.indexing.IdxSetter.get_set_meta").

If `keep_flex` is True, will return the most memory-efficient array representation capable of flexible indexing.

If `fill_value` is None, will search for the `_def` key in [IdxSetter.idx_items](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.idx_items "vectorbtpro.base.indexing.IdxSetter.idx_items"). If there's none, will be set to NaN.

* * *

### get_set_meta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2397-L2483 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.get_set_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-29-1)IdxSetter.get_set_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-29-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-29-3)    index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-29-4)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-29-5)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-29-6)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-29-7))
    

Get meta of setting operations in [IdxSetter.idx_items](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.idx_items "vectorbtpro.base.indexing.IdxSetter.idx_items").

* * *

### idx_items field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.idx_items "Permanent link")

Items where the first element is an indexer and the second element is a value to be set.

* * *

### set method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2485-L2491 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.set "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-30-1)IdxSetter.set(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-30-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-30-3)    set_funcs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-30-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-30-5))
    

Set values of a NumPy array based on [IdxSetter.get_set_meta](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.get_set_meta "vectorbtpro.base.indexing.IdxSetter.get_set_meta").

* * *

### set_col_idxs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2309-L2328 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.set_col_idxs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-31-1)IdxSetter.set_col_idxs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-31-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-31-3)    idxs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-31-4)    v
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-31-5))
    

Set column indices in an array.

* * *

### set_pd method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2493-L2500 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.set_pd "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-32-1)IdxSetter.set_pd(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-32-2)    pd_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-32-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-32-4))
    

Set values of a Pandas array based on [IdxSetter.get_set_meta](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.get_set_meta "vectorbtpro.base.indexing.IdxSetter.get_set_meta").

* * *

### set_row_and_col_idxs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2330-L2395 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.set_row_and_col_idxs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-33-1)IdxSetter.set_row_and_col_idxs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-33-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-33-3)    row_idxs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-33-4)    col_idxs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-33-5)    v
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-33-6))
    

Set row and column indices in an array.

* * *

### set_row_idxs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2280-L2307 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.set_row_idxs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-34-1)IdxSetter.set_row_idxs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-34-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-34-3)    idxs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-34-4)    v
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-34-5))
    

Set row indices in an array.

* * *

## IdxSetterFactory class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2535-L2540 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-35-1)IdxSetterFactory()
    

Class for building index setters.

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

  * [IdxDict](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxDict "vectorbtpro.base.indexing.IdxDict")
  * [IdxFrame](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxFrame "vectorbtpro.base.indexing.IdxFrame")
  * [IdxRecords](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords "vectorbtpro.base.indexing.IdxRecords")
  * [IdxSeries](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSeries "vectorbtpro.base.indexing.IdxSeries")



* * *

### get method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2538-L2540 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory.get "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-36-1)IdxSetterFactory.get()
    

Get an instance of [IdxSetter](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter "vectorbtpro.base.indexing.IdxSetter") or a dict of such instances - one per array name.

* * *

## Idxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2171-L2238 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-37-1)Idxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-37-2)    *idxrs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-37-3)    **idxr_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-37-4))
    

Class for resolving indices.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IdxrBase.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IdxrBase.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IdxrBase.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IdxrBase.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IdxrBase.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IdxrBase.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.IdxrBase.check_idxs")
  * [IdxrBase.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.IdxrBase.get")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.IdxrBase.slice_indexer")



* * *

### idxr_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr.idxr_kwargs "Permanent link")

Keyword arguments passed to [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr") and [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "vectorbtpro.base.indexing.ColIdxr").

* * *

### idxrs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr.idxrs "Permanent link")

A tuple of one or more indexers.

If one indexer is provided, can be an instance of [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr") or [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "vectorbtpro.base.indexing.ColIdxr"), a custom template, or a value to wrapped with [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr").

If two indexers are provided, can be an instance of [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr") and [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "vectorbtpro.base.indexing.ColIdxr") respectively, or a value to wrapped with [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr") and [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "vectorbtpro.base.indexing.ColIdxr") respectively.

* * *

## IdxrBase class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L546-L612 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-38-1)IdxrBase()
    

Abstract class for resolving indices.

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

  * [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "vectorbtpro.base.indexing.ColIdxr")
  * [Idxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr "vectorbtpro.base.indexing.Idxr")
  * [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



* * *

### check_idxs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L580-L612 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-39-1)IdxrBase.check_idxs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-39-2)    idxs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-39-3)    check_minus_one=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-39-4))
    

Check indices after resolving them.

* * *

### get method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L549-L551 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-40-1)IdxrBase.get(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-40-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-40-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-40-4))
    

Get indices.

* * *

### slice_indexer class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L553-L578 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-41-1)IdxrBase.slice_indexer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-41-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-41-3)    slice_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-41-4)    closed_start=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-41-5)    closed_end=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-41-6))
    

Compute the slice indexer for input labels and step.

* * *

## IndexingBase class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L70-L83 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-42-1)IndexingBase()
    

Class that supports indexing through [IndexingBase.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_func "vectorbtpro.base.indexing.IndexingBase.indexing_func").

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

  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * `vectorbtpro.indicators.custom.adx.ParamIndexer`
  * `vectorbtpro.indicators.custom.atr.ParamIndexer`
  * `vectorbtpro.indicators.custom.bbands.ParamIndexer`
  * `vectorbtpro.indicators.custom.hurst.ParamIndexer`
  * `vectorbtpro.indicators.custom.ma.ParamIndexer`
  * `vectorbtpro.indicators.custom.macd.ParamIndexer`
  * `vectorbtpro.indicators.custom.msd.ParamIndexer`
  * `vectorbtpro.indicators.custom.obv.ParamIndexer`
  * `vectorbtpro.indicators.custom.ols.ParamIndexer`
  * `vectorbtpro.indicators.custom.patsim.ParamIndexer`
  * `vectorbtpro.indicators.custom.pivotinfo.ParamIndexer`
  * `vectorbtpro.indicators.custom.rsi.ParamIndexer`
  * `vectorbtpro.indicators.custom.sigdet.ParamIndexer`
  * `vectorbtpro.indicators.custom.stoch.ParamIndexer`
  * `vectorbtpro.indicators.custom.supertrend.ParamIndexer`
  * `vectorbtpro.indicators.custom.vwap.ParamIndexer`
  * `vectorbtpro.labels.generators.bolb.ParamIndexer`
  * `vectorbtpro.labels.generators.fixlb.ParamIndexer`
  * `vectorbtpro.labels.generators.fmax.ParamIndexer`
  * `vectorbtpro.labels.generators.fmean.ParamIndexer`
  * `vectorbtpro.labels.generators.fmin.ParamIndexer`
  * `vectorbtpro.labels.generators.fstd.ParamIndexer`
  * `vectorbtpro.labels.generators.meanlb.ParamIndexer`
  * `vectorbtpro.labels.generators.pivotlb.ParamIndexer`
  * `vectorbtpro.labels.generators.trendlb.ParamIndexer`
  * `vectorbtpro.signals.generators.ohlcstcx.ParamIndexer`
  * `vectorbtpro.signals.generators.ohlcstx.ParamIndexer`
  * `vectorbtpro.signals.generators.rand.ParamIndexer`
  * `vectorbtpro.signals.generators.randnx.ParamIndexer`
  * `vectorbtpro.signals.generators.randx.ParamIndexer`
  * `vectorbtpro.signals.generators.rprob.ParamIndexer`
  * `vectorbtpro.signals.generators.rprobcx.ParamIndexer`
  * `vectorbtpro.signals.generators.rprobnx.ParamIndexer`
  * `vectorbtpro.signals.generators.rprobx.ParamIndexer`
  * `vectorbtpro.signals.generators.stcx.ParamIndexer`
  * `vectorbtpro.signals.generators.stx.ParamIndexer`



* * *

### indexing_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L73-L77 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-43-1)IndexingBase.indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-43-2)    pd_indexing_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-43-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-43-4))
    

Apply `pd_indexing_func` on all pandas objects in question and return a new instance of the class.

Should be overridden.

* * *

### indexing_setter_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L79-L83 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-44-1)IndexingBase.indexing_setter_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-44-2)    pd_indexing_setter_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-44-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-44-4))
    

Apply `pd_indexing_setter_func` on all pandas objects in question.

Should be overridden.

* * *

## IndexingError class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L63-L64 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingError "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-45-1)IndexingError(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-45-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-45-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-45-4))
    

Exception raised when an indexing error has occurred.

**Superclasses**

  * `builtins.BaseException`
  * `builtins.Exception`



* * *

## LabelIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L805-L852 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-46-1)LabelIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-46-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-46-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-46-4))
    

Class for resolving indices provided as labels.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### closed_end field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr.closed_end "Permanent link")

Whether slice end should be inclusive.

* * *

### closed_start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr.closed_start "Permanent link")

Whether slice start should be inclusive.

* * *

### level field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr.level "Permanent link")

One or more levels.

* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr.value "Permanent link")

One or more labels.

* * *

## Loc class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L157-L167 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Loc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-47-1)Loc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-47-2)    indexing_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-47-3)    indexing_setter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-47-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-47-5))
    

Forwards `pd.Series.loc`/`pd.DataFrame.loc` operation to each Series/DataFrame and returns a new class instance.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [LocBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase "vectorbtpro.base.indexing.LocBase")
  * [pdLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc "vectorbtpro.base.indexing.pdLoc")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.pdLoc.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.pdLoc.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.pdLoc.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.pdLoc.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.pdLoc.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.pdLoc.find_messages")
  * [pdLoc.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_func "vectorbtpro.base.indexing.pdLoc.indexing_func")
  * [pdLoc.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_kwargs "vectorbtpro.base.indexing.pdLoc.indexing_kwargs")
  * [pdLoc.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_setter_func "vectorbtpro.base.indexing.pdLoc.indexing_setter_func")
  * [pdLoc.pd_indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc.pd_indexing_func "vectorbtpro.base.indexing.pdLoc.pd_indexing_func")
  * [pdLoc.pd_indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc.pd_indexing_setter_func "vectorbtpro.base.indexing.pdLoc.pd_indexing_setter_func")



* * *

## LocBase class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L86-L121 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-48-1)LocBase(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-48-2)    indexing_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-48-3)    indexing_setter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-48-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-48-5))
    

Class that implements location-based indexing.

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

  * [ParamLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ParamLoc "vectorbtpro.base.indexing.ParamLoc")
  * [pdLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc "vectorbtpro.base.indexing.pdLoc")



* * *

### indexing_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L99-L102 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_func "Permanent link")

Indexing function.

* * *

### indexing_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L109-L112 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_kwargs "Permanent link")

Keyword arguments passed to [LocBase.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_func "vectorbtpro.base.indexing.LocBase.indexing_func").

* * *

### indexing_setter_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L104-L107 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_setter_func "Permanent link")

Indexing setter function.

* * *

## MaskIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L786-L802 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.MaskIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-49-1)MaskIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-49-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-49-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-49-4))
    

Class for resolving indices provided as a mask.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.MaskIdxr.value "Permanent link")

Mask.

* * *

## PandasIndexer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L173-L254 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-50-1)PandasIndexer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-50-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-50-3))
    

Implements indexing using `iloc`, `loc`, `xs` and `__getitem__`.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-2)>>> from vectorbtpro.base.indexing import PandasIndexer
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-4)>>> class C(PandasIndexer):
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-5)...     def __init__(self, df1, df2):
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-6)...         self.df1 = df1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-7)...         self.df2 = df2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-8)...         super().__init__()
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-9)...
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-10)...     def indexing_func(self, pd_indexing_func):
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-11)...         return type(self)(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-12)...             pd_indexing_func(self.df1),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-13)...             pd_indexing_func(self.df2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-14)...         )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-16)>>> df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-17)>>> df2 = pd.DataFrame({'a': [5, 6], 'b': [7, 8]})
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-18)>>> c = C(df1, df2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-19)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-20)>>> c.iloc[:, 0]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-21)<__main__.C object at 0x1a1cacbbe0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-22)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-23)>>> c.iloc[:, 0].df1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-24)0    1
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-25)1    2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-26)Name: a, dtype: int64
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-27)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-28)>>> c.iloc[:, 0].df2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-29)0    5
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-30)1    6
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-51-31)Name: a, dtype: int64
    

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IndexingBase.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IndexingBase.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IndexingBase.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IndexingBase.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IndexingBase.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IndexingBase.find_messages")
  * [IndexingBase.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_func "vectorbtpro.base.indexing.IndexingBase.indexing_func")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.base.indexing.IndexingBase.indexing_setter_func")



**Subclasses**

  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")



* * *

### iloc class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L222-L225 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "Permanent link")

Forwards `pd.Series.iloc`/`pd.DataFrame.iloc` operation to each Series/DataFrame and returns a new class instance.

* * *

### indexing_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L217-L220 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "Permanent link")

Indexing keyword arguments.

* * *

### loc class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L229-L232 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "Permanent link")

Forwards `pd.Series.loc`/`pd.DataFrame.loc` operation to each Series/DataFrame and returns a new class instance.

* * *

### xs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L236-L239 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-52-1)PandasIndexer.xs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-52-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-52-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-52-4))
    

Forwards `pd.Series.xs`/`pd.DataFrame.xs` operation to each Series/DataFrame and returns a new class instance.

* * *

## ParamLoc class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L303-L386 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ParamLoc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-53-1)ParamLoc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-53-2)    mapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-53-3)    indexing_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-53-4)    indexing_setter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-53-5)    level_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-53-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-53-7))
    

Access a group of columns by parameter using `pd.Series.loc`.

Uses `mapper` to establish link between columns and parameter values.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [LocBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase "vectorbtpro.base.indexing.LocBase")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.LocBase.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.LocBase.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.LocBase.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.LocBase.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.LocBase.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.LocBase.find_messages")
  * [LocBase.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_func "vectorbtpro.base.indexing.LocBase.indexing_func")
  * [LocBase.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_kwargs "vectorbtpro.base.indexing.LocBase.indexing_kwargs")
  * [LocBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_setter_func "vectorbtpro.base.indexing.LocBase.indexing_setter_func")



* * *

### encode_key class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L308-L314 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ParamLoc.encode_key "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-54-1)ParamLoc.encode_key(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-54-2)    key
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-54-3))
    

Encode key.

* * *

### get_idxs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L346-L361 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ParamLoc.get_idxs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-55-1)ParamLoc.get_idxs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-55-2)    key
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-55-3))
    

Get array of indices affected by this key.

* * *

### level_name class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L341-L344 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ParamLoc.level_name "Permanent link")

Level name.

* * *

### mapper class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L336-L339 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ParamLoc.mapper "Permanent link")

Mapper.

* * *

## PointIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L1005-L1090 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-56-1)PointIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-56-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-56-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-56-4))
    

Class for resolving index points.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### add_delta field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.add_delta "Permanent link")

Offset to be added to each in `on`.

Gets converted to a proper offset/timedelta using [to_freq](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_freq "vectorbtpro.utils.datetime_.to_freq").

* * *

### at_time field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.at_time "Permanent link")

Time of the day either as a (human-readable) string or `datetime.time`. 

Every datetime in `on` gets floored to the daily frequency, while `at_time` gets converted into a timedelta using [time_to_timedelta](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.time_to_timedelta "vectorbtpro.utils.datetime_.time_to_timedelta") and added to `add_delta`. Index must be datetime-like.

* * *

### end field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.end "Permanent link")

End index/date.

If (human-readable) string, gets converted into a datetime.

If `every` is None, gets used to filter the final index array.

* * *

### every field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.every "Permanent link")

Frequency either as an integer or timedelta.

Gets translated into `on` array by creating a range. If integer, an index sequence from `start` to `end` (exclusive) is created and 'indices' as `kind` is used. If timedelta-like, a date sequence from `start` to `end` (inclusive) is created and 'labels' as `kind` is used.

If `at_time` is not None and `every` and `on` are None, `every` defaults to one day.

* * *

### exact_start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.exact_start "Permanent link")

Whether the first index should be exactly `start`.

Depending on `every`, the first index picked by `pd.date_range` may happen after `start`. In such a case, `start` gets injected before the first index generated by `pd.date_range`.

* * *

### indexer_method field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.indexer_method "Permanent link")

Method for `pd.Index.get_indexer`.

Allows two additional values: "before" and "after".

* * *

### indexer_tolerance field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.indexer_tolerance "Permanent link")

Tolerance for `pd.Index.get_indexer`.

If `at_time` is set and `indexer_method` is neither exact nor nearest, `indexer_tolerance` becomes such that the next element must be within the current day.

* * *

### kind field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.kind "Permanent link")

Kind of data in `on`: indices or labels.

If None, gets assigned to `indices` if `on` contains integer data, otherwise to `labels`.

If `kind` is 'labels', `on` gets converted into indices using `pd.Index.get_indexer`. Prior to this, gets its timezone aligned to the timezone of the index. If `kind` is 'indices', `on` gets wrapped with NumPy.

* * *

### normalize_every field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.normalize_every "Permanent link")

Normalize start/end dates to midnight before generating date range.

* * *

### on field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.on "Permanent link")

Index/label or a sequence of such.

Gets converted into datetime format whenever possible.

* * *

### skip_not_found field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.skip_not_found "Permanent link")

Whether to drop indices that are -1 (not found).

* * *

### start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr.start "Permanent link")

Start index/date.

If (human-readable) string, gets converted into a datetime.

If `every` is None, gets used to filter the final index array.

* * *

## PosIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L763-L783 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PosIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-57-1)PosIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-57-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-57-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-57-4))
    

Class for resolving indices provided as integer positions.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PosIdxr.value "Permanent link")

One or more integer positions.

* * *

## RangeIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L1304-L1428 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-58-1)RangeIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-58-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-58-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-58-4))
    

Class for resolving index ranges.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### add_end_delta field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.add_end_delta "Permanent link")

Offset to be added to each in `end`.

If string, gets converted to a proper offset/timedelta using [to_freq](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_freq "vectorbtpro.utils.datetime_.to_freq").

* * *

### add_start_delta field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.add_start_delta "Permanent link")

Offset to be added to each in `start`.

If string, gets converted to a proper offset/timedelta using [to_freq](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_freq "vectorbtpro.utils.datetime_.to_freq").

* * *

### closed_end field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.closed_end "Permanent link")

Whether `end` should be inclusive.

* * *

### closed_start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.closed_start "Permanent link")

Whether `start` should be inclusive.

* * *

### end field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.end "Permanent link")

End index/label or a sequence of such.

Gets converted into datetime format whenever possible.

Gets broadcasted together with `start`.

* * *

### end_time field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.end_time "Permanent link")

End time of the day either as a (human-readable) string or `datetime.time`. 

Every datetime in `end` gets floored to the daily frequency, while `end_time` gets converted into a timedelta using [time_to_timedelta](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.time_to_timedelta "vectorbtpro.utils.datetime_.time_to_timedelta") and added to `add_end_delta`. Index must be datetime-like.

* * *

### every field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.every "Permanent link")

Frequency either as an integer or timedelta.

Gets translated into `start` and `end` arrays by creating a range. If integer, an index sequence from `start` to `end` (exclusive) is created and 'indices' as `kind` is used. If timedelta-like, a date sequence from `start` to `end` (inclusive) is created and 'bounds' as `kind` is used. 

If `start_time` and `end_time` are not None and `every`, `start`, and `end` are None, `every` defaults to one day.

* * *

### exact_start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.exact_start "Permanent link")

Whether the first index in the `start` array should be exactly `start`.

Depending on `every`, the first index picked by `pd.date_range` may happen after `start`. In such a case, `start` gets injected before the first index generated by `pd.date_range`.

Cannot be used together with `lookback_period`.

* * *

### fixed_start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.fixed_start "Permanent link")

Whether all indices in the `start` array should be exactly `start`.

Works only together with `every`.

Cannot be used together with `lookback_period`.

* * *

### jitted field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.jitted "Permanent link")

Jitting option passed to [Resampler.map_bounds_to_source_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.map_bounds_to_source_ranges "vectorbtpro.base.resampling.base.Resampler.map_bounds_to_source_ranges").

* * *

### kind field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.kind "Permanent link")

Kind of data in `on`: indices, labels or bounds.

If None, gets assigned to `indices` if `start` and `end` contain integer data, to `bounds` if `start`, `end`, and index are datetime-like, otherwise to `labels`.

If `kind` is 'labels', `start` and `end` get converted into indices using `pd.Index.get_indexer`. Prior to this, get their timezone aligned to the timezone of the index. If `kind` is 'indices', `start` and `end` get wrapped with NumPy. If kind` is 'bounds', [Resampler.map_bounds_to_source_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.map_bounds_to_source_ranges "vectorbtpro.base.resampling.base.Resampler.map_bounds_to_source_ranges") is used.

* * *

### lookback_period field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.lookback_period "Permanent link")

Lookback period either as an integer or offset.

If `lookback_period` is set, `start` becomes `end-lookback_period`. If `every` is not None, the sequence is generated from `start+lookback_period` to `end` and then assigned to `end`.

If string, gets converted to a proper offset/timedelta using [to_freq](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_freq "vectorbtpro.utils.datetime_.to_freq"). If integer, gets multiplied by the frequency of the index if the index is not integer.

* * *

### normalize_every field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.normalize_every "Permanent link")

Normalize start/end dates to midnight before generating date range.

* * *

### skip_not_found field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.skip_not_found "Permanent link")

Whether to drop indices that are -1 (not found).

* * *

### split_every field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.split_every "Permanent link")

Whether to split the sequence generated using `every` into `start` and `end` arrays.

After creation, and if `split_every` is True, an index range is created from each pair of elements in the generated sequence. Otherwise, the entire sequence is assigned to `start` and `end`, and only time and delta instructions can be used to further differentiate between them.

Forced to False if `every`, `start_time`, and `end_time` are not None and `fixed_start` is False.

* * *

### start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.start "Permanent link")

Start index/label or a sequence of such.

Gets converted into datetime format whenever possible.

Gets broadcasted together with `end`.

* * *

### start_time field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr.start_time "Permanent link")

Start time of the day either as a (human-readable) string or `datetime.time`. 

Every datetime in `start` gets floored to the daily frequency, while `start_time` gets converted into a timedelta using [time_to_timedelta](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.time_to_timedelta "vectorbtpro.utils.datetime_.time_to_timedelta") and added to `add_start_delta`. Index must be datetime-like.

* * *

## RowIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2108-L2137 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-59-1)RowIdxr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-59-2)    idxr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-59-3)    **idxr_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-59-4))
    

Class for resolving row indices.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IdxrBase.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IdxrBase.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IdxrBase.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IdxrBase.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IdxrBase.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IdxrBase.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.IdxrBase.check_idxs")
  * [IdxrBase.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.IdxrBase.get")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.IdxrBase.slice_indexer")



* * *

### idxr field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr.idxr "Permanent link")

Indexer.

Can be an instance of [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr"), a custom template, or a value to be wrapped with [AutoIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr "vectorbtpro.base.indexing.AutoIdxr").

* * *

### idxr_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr.idxr_kwargs "Permanent link")

Keyword arguments passed to [AutoIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr "vectorbtpro.base.indexing.AutoIdxr").

* * *

## UniIdxr class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L632-L727 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-60-1)UniIdxr()
    

Abstract class for resolving indices based on a single index.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.IdxrBase.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.IdxrBase.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.IdxrBase.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.IdxrBase.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.IdxrBase.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.IdxrBase.find_messages")
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.IdxrBase.check_idxs")
  * [IdxrBase.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.IdxrBase.get")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.IdxrBase.slice_indexer")



**Subclasses**

  * [AutoIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr "vectorbtpro.base.indexing.AutoIdxr")
  * [DTCIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr "vectorbtpro.base.indexing.DTCIdxr")
  * [DatetimeIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr "vectorbtpro.base.indexing.DatetimeIdxr")
  * [LabelIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr "vectorbtpro.base.indexing.LabelIdxr")
  * [MaskIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.MaskIdxr "vectorbtpro.base.indexing.MaskIdxr")
  * [PointIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr "vectorbtpro.base.indexing.PointIdxr")
  * [PosIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PosIdxr "vectorbtpro.base.indexing.PosIdxr")
  * [RangeIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr "vectorbtpro.base.indexing.RangeIdxr")
  * [UniIdxrOp](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxrOp "vectorbtpro.base.indexing.UniIdxrOp")



* * *

## UniIdxrOp class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L730-L760 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxrOp "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-61-1)UniIdxrOp(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-61-2)    op_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-61-3)    *idxrs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-61-4))
    

Class for applying an operation to one or more indexers.

Produces a single set of indices.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [UniIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxr "vectorbtpro.base.indexing.UniIdxr")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.UniIdxr.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.UniIdxr.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.UniIdxr.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.UniIdxr.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.UniIdxr.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.UniIdxr.find_messages")
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
  * [IdxrBase.check_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.check_idxs "vectorbtpro.base.indexing.UniIdxr.check_idxs")
  * [IdxrBase.slice_indexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.slice_indexer "vectorbtpro.base.indexing.UniIdxr.slice_indexer")
  * [UniIdxr.get](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase.get "vectorbtpro.base.indexing.UniIdxr.get")



* * *

### idxrs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxrOp.idxrs "Permanent link")

A tuple of one or more indexers.

* * *

### op_func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxrOp.op_func "Permanent link")

Operation function that takes the indices of each indexer (as `*args`), `index` (keyword argument), and `freq` (keyword argument), and returns new indices.

* * *

## hslice class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L510-L543 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.hslice "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-62-1)hslice(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-62-2)    start=_Missing.MISSING,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-62-3)    stop=_Missing.MISSING,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-62-4)    step=_Missing.MISSING
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-62-5))
    

Hashable slice.

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

### from_slice class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L536-L539 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.hslice.from_slice "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-63-1)hslice.from_slice(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-63-2)    slice_
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-63-3))
    

Construct from a slice.

* * *

### start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.hslice.start "Permanent link")

Start.

* * *

### step field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.hslice.step "Permanent link")

Step.

* * *

### stop field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.hslice.stop "Permanent link")

Stop.

* * *

### to_slice method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L541-L543 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.hslice.to_slice "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-64-1)hslice.to_slice()
    

Convert to a slice.

* * *

## iLoc class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L144-L154 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.iLoc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-65-1)iLoc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-65-2)    indexing_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-65-3)    indexing_setter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-65-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-65-5))
    

Forwards `pd.Series.iloc`/`pd.DataFrame.iloc` operation to each Series/DataFrame and returns a new class instance.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [LocBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase "vectorbtpro.base.indexing.LocBase")
  * [pdLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc "vectorbtpro.base.indexing.pdLoc")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.pdLoc.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.pdLoc.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.pdLoc.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.pdLoc.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.pdLoc.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.pdLoc.find_messages")
  * [pdLoc.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_func "vectorbtpro.base.indexing.pdLoc.indexing_func")
  * [pdLoc.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_kwargs "vectorbtpro.base.indexing.pdLoc.indexing_kwargs")
  * [pdLoc.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_setter_func "vectorbtpro.base.indexing.pdLoc.indexing_setter_func")
  * [pdLoc.pd_indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc.pd_indexing_func "vectorbtpro.base.indexing.pdLoc.pd_indexing_func")
  * [pdLoc.pd_indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc.pd_indexing_setter_func "vectorbtpro.base.indexing.pdLoc.pd_indexing_setter_func")



**Subclasses**

  * [xLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.xLoc "vectorbtpro.base.indexing.xLoc")



* * *

## index_dict class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L2259-L2267 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.index_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-66-1)index_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-66-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-66-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-66-4))
    

Dict that contains indexer objects as keys and values to be set as values.

Each indexer object must be hashable. To make a slice hashable, use [hslice](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.hslice "vectorbtpro.base.indexing.hslice"). To make an array hashable, convert it into a tuple.

To set a default value, use the `_def` key (case-sensitive!).

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * `builtins.dict`
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.pickling.pdict.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.pickling.pdict.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.pickling.pdict.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.pickling.pdict.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.pickling.pdict.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.pickling.pdict.find_messages")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.pickling.pdict.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.pickling.pdict.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.pickling.pdict.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.pickling.pdict.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.pickling.pdict.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.pickling.pdict.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.pickling.pdict.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.pickling.pdict.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.pickling.pdict.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.pickling.pdict.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.pickling.pdict.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.pickling.pdict.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.pickling.pdict.pprint")
  * [pdict.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "vectorbtpro.utils.pickling.pdict.equals")
  * [pdict.load_update](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "vectorbtpro.utils.pickling.pdict.load_update")
  * [pdict.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.pickling.pdict.prettify")
  * [pdict.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.pickling.pdict.rec_state")



* * *

## pdLoc class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L124-L141 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-67-1)pdLoc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-67-2)    indexing_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-67-3)    indexing_setter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-67-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-67-5))
    

Forwards a Pandas-like indexing operation to each Series/DataFrame and returns a new class instance.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [LocBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase "vectorbtpro.base.indexing.LocBase")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.LocBase.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.LocBase.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.LocBase.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.LocBase.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.LocBase.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.LocBase.find_messages")
  * [LocBase.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_func "vectorbtpro.base.indexing.LocBase.indexing_func")
  * [LocBase.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_kwargs "vectorbtpro.base.indexing.LocBase.indexing_kwargs")
  * [LocBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_setter_func "vectorbtpro.base.indexing.LocBase.indexing_setter_func")



**Subclasses**

  * [Loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Loc "vectorbtpro.base.indexing.Loc")
  * [iLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.iLoc "vectorbtpro.base.indexing.iLoc")



* * *

### pd_indexing_func class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L127-L130 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc.pd_indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-68-1)pdLoc.pd_indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-68-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-68-3)    key
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-68-4))
    

Pandas-like indexing operation.

* * *

### pd_indexing_setter_func class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L132-L135 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc.pd_indexing_setter_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-69-1)pdLoc.pd_indexing_setter_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-69-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-69-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-69-4)    value
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-69-5))
    

Pandas-like indexing setter operation.

* * *

## xLoc class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/indexing.py#L257-L285 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.xLoc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-70-1)xLoc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-70-2)    indexing_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-70-3)    indexing_setter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-70-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#__codelineno-70-5))
    

Subclass of [iLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.iLoc "vectorbtpro.base.indexing.iLoc") that transforms an [Idxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr "vectorbtpro.base.indexing.Idxr")-based operation with [get_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.get_idxs "vectorbtpro.base.indexing.get_idxs") to an [iLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.iLoc "vectorbtpro.base.indexing.iLoc") operation.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [LocBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase "vectorbtpro.base.indexing.LocBase")
  * [iLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.iLoc "vectorbtpro.base.indexing.iLoc")
  * [pdLoc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc "vectorbtpro.base.indexing.pdLoc")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.iLoc.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.iLoc.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.iLoc.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.iLoc.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.iLoc.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.iLoc.find_messages")
  * [iLoc.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_func "vectorbtpro.base.indexing.iLoc.indexing_func")
  * [iLoc.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_kwargs "vectorbtpro.base.indexing.iLoc.indexing_kwargs")
  * [iLoc.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase.indexing_setter_func "vectorbtpro.base.indexing.iLoc.indexing_setter_func")
  * [iLoc.pd_indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc.pd_indexing_func "vectorbtpro.base.indexing.iLoc.pd_indexing_func")
  * [iLoc.pd_indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.pdLoc.pd_indexing_setter_func "vectorbtpro.base.indexing.iLoc.pd_indexing_setter_func")


