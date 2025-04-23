params

#  params module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params "Permanent link")

Utilities for working with parameters.

* * *

## broadcast_params function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L113-L135 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.broadcast_params "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-0-1)broadcast_params(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-0-2)    params_or_dict,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-0-3)    to_n=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-0-4))
    

Broadcast parameters in `params`.

* * *

## combine_params function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L382-L934 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-1)combine_params(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-2)    param_dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-3)    build_grid=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-4)    grid_indices=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-5)    random_subset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-6)    random_replace=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-7)    random_sort=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-8)    max_guesses=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-9)    max_misses=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-10)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-11)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-12)    name_tuple_to_str=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-13)    build_index=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-14)    raise_empty_error=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-1-15))
    

Combine a dictionary with parameters of the type [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param").

Returns a dictionary with combined parameters and an index if `build_index` is True.

If `build_grid` is True, first builds the entire grid and then filters parameter combinations by conditions and selects random combinations. If `build_grid` is False, doesn't build the entire grid, but selects and combines combinations on the fly. Materializing the grid is recommended only when the number of combinations is relatively low (less than one million) and parameters have conditions.

Argument `grid_indices` can be a slice (for example, `slice(None, None, 2)` for `::2`) or an array with indices that map to the length of the grid. It can be used to skip a some combinations before a random subset is drawn.

Argument `random_subset` can be an integer (number of combinations) or a float relative to the length of the grid. If parameters have conditions, `random_subset` is drawn from the subset of combinations whose conditions have been met, not the other way around. If `random_replace` is True, draws random combinations with replacement (that is, duplicate combinations will likely occur). If `random_replace` is False (default), each drawn combination will be unique. If `random_sort` is True (default), positions of combinations will be sorted. Otherwise, they will remain in their randomly-selected positions.

Arguments `max_guesses` and `max_misses` are effective only when the grid is not buildd and parameters have conditions. They mean the maximum number of guesses and misses respectively when doing the search for a valid combination in a while-loop. Once any of these two numbers is reached, the search will stop. They are useful for limiting the number of guesses; without them, the search may continue forever.

If a name of any parameter is a tuple, can convert this tuple into a string by setting `name_tuple_to_str` either to True or providing a callable that does this.

Keyword arguments `clean_index_kwargs` are passed to [clean_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.clean_index "vectorbtpro.base.indexes.clean_index").

* * *

## create_param_product function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L138-L149 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.create_param_product "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-2-1)create_param_product(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-2-2)    params_or_dict
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-2-3))
    

Make Cartesian product out of all params in `params`.

* * *

## flatten_param_tuples function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L60-L70 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.flatten_param_tuples "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-3-1)flatten_param_tuples(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-3-2)    param_tuples
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-3-3))
    

Flattens a nested list of iterables using unzipping.

* * *

## generate_param_combs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L73-L110 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.generate_param_combs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-4-1)generate_param_combs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-4-2)    op_tree,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-4-3)    depth=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-4-4))
    

Generate arbitrary parameter combinations from the operation tree `op_tree`.

`op_tree` is a tuple with nested instructions to generate parameters. The first element of the tuple must be either the name of a callale from `itertools` or the callable itself that takes remaining elements as arguments. If one of the elements is a tuple itself and its first argument is a callable, it will be unfolded in the same way as above.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-3)>>> vbt.generate_param_combs(("product", ("combinations", [0, 1, 2, 3], 2), [4, 5]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-4)[[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2],
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-5) [1, 1, 2, 2, 3, 3, 2, 2, 3, 3, 3, 3],
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-6) [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-8)>>> vbt.generate_param_combs(("product", (zip, [0, 1, 2, 3], [4, 5, 6, 7]), [8, 9]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-5-9)[[0, 0, 1, 1, 2, 2, 3, 3], [4, 4, 5, 5, 6, 6, 7, 7], [8, 9, 8, 9, 8, 9, 8, 9]]
    

* * *

## get_param_grid_len function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L181-L195 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.get_param_grid_len "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-6-1)get_param_grid_len(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-6-2)    param_grid
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-6-3))
    

Get the number of parameter combinations in a parameter grid.

Parameter values can also be an integer to represent the number of values.

* * *

## is_single_param_value function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L152-L167 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.is_single_param_value "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-7-1)is_single_param_value(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-7-2)    param_values,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-7-3)    is_tuple=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-7-4)    is_array_like=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-7-5))
    

Check whether `param_values` is a single value.

* * *

## parameterized function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1884-L2130 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-8-1)parameterized(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-8-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-8-3)    parameterizer=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-8-4)    replace_parameterizer=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-8-5)    merge_to_execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-8-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-8-7))
    

Decorator that parameterizes inputs of a function using [Parameterizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer "vectorbtpro.utils.params.Parameterizer").

Returns a new function with the same signature as the passed one.

Each option can be modified in the `options` attribute of the wrapper function or directly passed as a keyword argument with a leading underscore.

Keyword arguments not listed in [Parameterizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer "vectorbtpro.utils.params.Parameterizer") and `execute_kwargs` are merged into `execute_kwargs` if `merge_to_execute_kwargs` is True, otherwise, they are passed directly to [Parameterizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer "vectorbtpro.utils.params.Parameterizer").

If a parameterizer instance is provided and `replace_parameterizer` is True, will create a new [Parameterizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer "vectorbtpro.utils.params.Parameterizer") instance by replacing any arguments that are not None.

**Usage**

  * No parameters, no parameter configs:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-3)>>> @vbt.parameterized(merge_func="column_stack")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-4)... def my_ma(sr_or_df, window, wtype="simple", minp=0, adjust=False):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-5)...     return sr_or_df.vbt.ma(window, wtype=wtype, minp=minp, adjust=adjust)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-7)>>> sr = pd.Series([1, 2, 3, 4, 3, 2, 1])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-8)>>> my_ma(sr, 3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-9)0    1.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-10)1    1.500000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-11)2    2.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-12)3    3.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-13)4    3.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-14)5    3.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-15)6    2.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-9-16)dtype: float64
    

  * One parameter, no parameter configs:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-1)>>> my_ma(sr, vbt.Param([3, 4, 5]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-2)window         3    4    5
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-3)0       1.000000  1.0  1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-4)1       1.500000  1.5  1.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-5)2       2.000000  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-6)3       3.000000  2.5  2.5
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-7)4       3.333333  3.0  2.6
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-8)5       3.000000  3.0  2.8
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-10-9)6       2.000000  2.5  2.6
    

  * Product of two parameters, no parameter configs:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-1)>>> my_ma(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-2)...     sr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-3)...     vbt.Param([3, 4, 5]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-4)...     wtype=vbt.Param(["simple", "exp"])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-5)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-6)window         3                4                5
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-7)wtype     simple       exp simple       exp simple       exp
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-8)0       1.000000  1.000000    1.0  1.000000    1.0  1.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-9)1       1.500000  1.500000    1.5  1.400000    1.5  1.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-10)2       2.000000  2.250000    2.0  2.040000    2.0  1.888889
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-11)3       3.000000  3.125000    2.5  2.824000    2.5  2.592593
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-12)4       3.333333  3.062500    3.0  2.894400    2.6  2.728395
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-13)5       3.000000  2.531250    3.0  2.536640    2.8  2.485597
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-11-14)6       2.000000  1.765625    2.5  1.921984    2.6  1.990398
    

  * No parameters, one partial parameter config:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-1)>>> my_ma(sr, param_configs=[dict(window=3)])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-2)param_config         0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-3)0             1.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-4)1             1.500000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-5)2             2.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-6)3             3.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-7)4             3.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-8)5             3.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-12-9)6             2.000000
    

  * No parameters, one full parameter config:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-1)>>> my_ma(param_configs=[dict(sr_or_df=sr, window=3)])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-2)param_config         0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-3)0             1.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-4)1             1.500000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-5)2             2.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-6)3             3.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-7)4             3.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-8)5             3.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-13-9)6             2.000000
    

  * No parameters, multiple parameter configs:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-1)>>> my_ma(param_configs=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-2)...     dict(sr_or_df=sr + 1, window=2),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-3)...     dict(sr_or_df=sr - 1, window=3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-4)... ], minp=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-5)param_config    0         1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-6)0             NaN       NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-7)1             2.5       NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-8)2             3.5  1.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-9)3             4.5  2.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-10)4             4.5  2.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-11)5             3.5  2.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-14-12)6             2.5  1.000000
    

  * Multiple parameters, multiple parameter configs:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-1)>>> my_ma(param_configs=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-2)...     dict(sr_or_df=sr + 1, minp=0),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-3)...     dict(sr_or_df=sr - 1, minp=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-4)... ], window=vbt.Param([2, 3]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-5)window          2              3
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-6)param_config    0    1         0         1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-7)0             2.0  NaN  2.000000       NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-8)1             2.5  0.5  2.500000       NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-9)2             3.5  1.5  3.000000  1.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-10)3             4.5  2.5  4.000000  2.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-11)4             4.5  2.5  4.333333  2.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-12)5             3.5  1.5  4.000000  2.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-15-13)6             2.5  0.5  3.000000  1.000000
    

  * Using annotations:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-1)>>> @vbt.parameterized
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-2)... def my_ma(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-3)...     sr_or_df,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-4)...     window: vbt.Param,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-5)...     wtype: vbt.Param = "simple",
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-6)...     minp=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-7)...     adjust=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-8)... ) -> vbt.MergeFunc("column_stack"):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-9)...     return sr_or_df.vbt.ma(window, wtype=wtype, minp=minp, adjust=adjust)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-11)>>> my_ma(sr, [3, 4, 5], ["simple", "exp"])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-12)window         3                4                5
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-13)wtype     simple       exp simple       exp simple       exp
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-14)0       1.000000  1.000000    1.0  1.000000    1.0  1.000000
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-15)1       1.500000  1.500000    1.5  1.400000    1.5  1.333333
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-16)2       2.000000  2.250000    2.0  2.040000    2.0  1.888889
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-17)3       3.000000  3.125000    2.5  2.824000    2.5  2.592593
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-18)4       3.333333  3.062500    3.0  2.894400    2.6  2.728395
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-19)5       3.000000  2.531250    3.0  2.536640    2.8  2.485597
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-16-20)6       2.000000  1.765625    2.5  1.921984    2.6  1.990398
    

* * *

## params_to_list function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L170-L178 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.params_to_list "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-17-1)params_to_list(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-17-2)    param_values,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-17-3)    is_tuple=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-17-4)    is_array_like=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-17-5))
    

Cast parameters to a list.

* * *

## pick_from_param_grid function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L198-L228 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.pick_from_param_grid "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-18-1)pick_from_param_grid(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-18-2)    param_grid,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-18-3)    i=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-18-4))
    

Pick one or more parameter combinations from a parameter grid.

Parameter values can also be an integer to represent the number of values.

* * *

## to_typed_list function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L49-L57 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.to_typed_list "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-19-1)to_typed_list(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-19-2)    lst
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-19-3))
    

Cast Python list to typed list.

Direct construction is flawed in Numba 0.52.0. See <https://github.com/numba/numba/issues/6651>

* * *

## ItemParamable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L359-L379 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-20-1)ItemParamable()
    

Class representing an object that can be returned as both items and parameters.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.params.Itemable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.params.Itemable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.params.Itemable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.params.Itemable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.params.Itemable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.params.Itemable.find_messages")
  * [Itemable.items](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable.items "vectorbtpro.utils.params.Itemable.items")
  * [Paramable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.utils.params.Paramable.as_param")



**Subclasses**

  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")



* * *

## Itemable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L343-L348 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-21-1)Itemable()
    

Class representing an object that can be returned as items.

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

  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")



* * *

### items method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L346-L348 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable.items "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-22-1)Itemable.items(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-22-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-22-3))
    

Return this instance as items.

* * *

## Param class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L234-L340 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-23-1)Param(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-23-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-23-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-23-4))
    

Class that represents a parameter.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.eval_.Evaluable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.eval_.Evaluable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.eval_.Evaluable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.eval_.Evaluable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.eval_.Evaluable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.eval_.Evaluable.find_messages")
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
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.eval_.Evaluable.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### condition field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.condition "Permanent link")

Keep a parameter combination only if the condition is met.

Condition can be a template or an expression where `x` (or parameter name) denotes this parameter and any other variable denotes the name of other parameter(s). If passed as an expression, it will be pre-compiled so its execution may be faster than if passed as a template.

To access a parameter index value, prepend and append `__` to the level name. For example, use `__fast_sma_timeperiod__` if the parameter index contains a level `fast_sma_timeperiod`.

* * *

### context field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.context "Permanent link")

Context used in evaluation of [Param.condition](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.condition "vectorbtpro.utils.params.Param.condition") and [Param.map_template](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.map_template "vectorbtpro.utils.params.Param.map_template").

* * *

### eval_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.eval_id "Permanent link")

One or more identifiers at which to evaluate this instance.

* * *

### hide field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.hide "Permanent link")

Whether to hide the parameter from the parameter index.

* * *

### is_array_like field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.is_array_like "Permanent link")

Whether [Param.value](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.value "vectorbtpro.utils.params.Param.value") is array-like.

If so, providing a NumPy array will be considered as a single value.

* * *

### is_tuple field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.is_tuple "Permanent link")

Whether [Param.value](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.value "vectorbtpro.utils.params.Param.value") is a tuple.

If so, providing a tuple will be considered as a single value.

* * *

### keys field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.keys "Permanent link")

Keys acting as an index level.

If None, converts [Param.value](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.value "vectorbtpro.utils.params.Param.value") to an index using [index_from_values](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.index_from_values "vectorbtpro.base.indexes.index_from_values").

* * *

### level field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.level "Permanent link")

Level of the product the parameter takes part in.

Parameters with the same level are stacked together, while parameters with different levels are combined as usual.

Parameters are processed based on their level: a lower-level parameter is processed before (and thus displayed above) a higher-level parameter. If two parameters share the same level, they are processed in the order they were passed to the function.

Levels must come in a strict order starting with 0 and without gaps. If any of the parameters have a level specified, all parameters must specify their level.

* * *

### map_template field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.map_template "Permanent link")

Template to map [Param.value](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.value "vectorbtpro.utils.params.Param.value") before building parameter combinations.

* * *

### map_value method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L312-L340 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.map_value "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-24-1)Param.map_value(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-24-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-24-3)    old_as_keys=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-24-4))
    

Execute a function on each value in [Param.value](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.value "vectorbtpro.utils.params.Param.value") and create a new [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param") instance.

If `old_as_keys` is True, will use old values as keys, unless keys are already provided.

* * *

### mono_merge_func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.mono_merge_func "Permanent link")

Merge function to apply when building a mono-chunk.

Resolved using [resolve_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/base/merging/#vectorbtpro.base.merging.resolve_merge_func "vectorbtpro.base.merging.resolve_merge_func").

* * *

### mono_merge_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.mono_merge_kwargs "Permanent link")

Keyword arguments passed to [Param.mono_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.mono_merge_func "vectorbtpro.utils.params.Param.mono_merge_func").

* * *

### mono_reduce field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.mono_reduce "Permanent link")

Whether to reduce a mono-chunk of the same values into one value.

* * *

### name field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.name "Permanent link")

Name of the parameter.

If None, defaults to the name of the index in [Param.keys](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.keys "vectorbtpro.utils.params.Param.keys"), or to the key in `param_dct` passed to [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### random_subset field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.random_subset "Permanent link")

Random subset of values to select.

* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.value "Permanent link")

One or more parameter values.

* * *

## Paramable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L351-L356 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-25-1)Paramable()
    

Class representing an object that can be returned as a parameter.

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

  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")



* * *

### as_param method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L354-L356 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-26-1)Paramable.as_param(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-26-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-26-3))
    

Return this instance as a parameter.

* * *

## Parameterizer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L937-L1881 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-1)Parameterizer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-2)    param_search_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-3)    skip_single_comb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-4)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-5)    build_grid=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-6)    grid_indices=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-7)    random_subset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-8)    random_replace=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-9)    random_sort=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-10)    max_guesses=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-11)    max_misses=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-12)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-13)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-14)    name_tuple_to_str=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-15)    selection=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-16)    forward_kwargs_as=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-17)    mono_min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-18)    mono_n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-19)    mono_chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-20)    mono_chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-21)    mono_reduce=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-22)    mono_merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-23)    mono_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-24)    filter_results=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-25)    raise_no_results=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-26)    merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-27)    merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-28)    return_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-29)    return_param_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-30)    execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-31)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-27-32))
    

Class responsible for parameterizing and running a function.

Does the following:

  1. Searches for values wrapped with the class [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param") in any nested dicts and tuples using [Parameterizer.find_params_in_obj](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.find_params_in_obj "vectorbtpro.utils.params.Parameterizer.find_params_in_obj")
  2. Uses [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params") to build parameter combinations
  3. Maps parameter combinations to configs using [Parameterizer.param_product_to_objs](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.param_product_to_objs "vectorbtpro.utils.params.Parameterizer.param_product_to_objs")
  4. Generates and resolves parameter configs by combining combinations from the step above with `param_configs` that is optionally passed by the user. User-defined `param_configs` have more priority.
  5. If `selection` is not None, substitutes it as a template, translates it into indices that can be mapped to `param_index`, and selects them from all the objects generated above.
  6. Builds mono-chunks if `mono_n_chunks`, `mono_chunk_len`, or `mono_chunk_meta` is not None
  7. Extracts arguments and keyword arguments from each parameter config and substitutes any templates (lazily)
  8. Passes each set of the function and its arguments to [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute "vectorbtpro.utils.execution.execute") for execution
  9. Optionally, post-processes and merges the results by passing them and `**merge_kwargs` to `merge_func`



Argument `param_configs` accepts either a list of dictionaries with arguments named by their names in the signature, or a dictionary of dictionaries, where keys are config names. If a list is passed, each dictionary can also contain the key `_name` to give the config a name. Variable arguments can be passed either in the rolled (`args=(...), kwargs={...}`) or unrolled (`args_0=..., args_1=..., some_kwarg=...`) format.

Important

Defining a parameter and listing the same argument in `param_configs` will prioritize the config over the parameter, even though the parameter will still be visible in the final columns. There are no checks implemented to raise an error when this happens!

If mono-chunking is enabled, parameter configs will be distributed over chunks. Any argument that is wrapped with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param") or appears in `mono_merge_func` will be aggregated into a list. It will be merged using either [Param.mono_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.mono_merge_func "vectorbtpro.utils.params.Param.mono_merge_func") or `mono_merge_func` in the same way as `merge_func`. If an argument satisfies neither of the above requirements and all its values within a chunk are same, this value will be passed as a scalar. Arguments `mono_merge_func` and `mono_merge_kwargs` must be dictionaries where keys are argument names in the flattened signature and values are functions and keyword arguments respectively.

If [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "vectorbtpro.utils.execution.NoResult") is returned, will skip the current iteration and remove it from the final index.

For defaults, see [params](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.params "vectorbtpro._settings.params").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Configured.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Configured.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Configured.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Configured.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Configured.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Configured.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.config.Configured.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.config.Configured.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.config.Configured.pipe")
  * [Configured.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.config.Configured.config")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.config.Configured.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.config.Configured.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.config.Configured.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Configured.prettify")
  * [Configured.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Configured.rec_state")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.config.Configured.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.config.Configured.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.config.Configured.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.config.Configured.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.config.Configured.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.config.Configured.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.config.Configured.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.config.Configured.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.config.Configured.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.config.Configured.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.config.Configured.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.config.Configured.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.config.Configured.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.config.Configured.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.config.Configured.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Configured.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Configured.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Configured.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Configured.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Configured.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Configured.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Configured.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Configured.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Configured.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Configured.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Configured.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Configured.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Configured.pprint")



* * *

### build_grid class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1098-L1101 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.build_grid "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### build_mono_chunk_config method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1480-L1571 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.build_mono_chunk_config "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-1)Parameterizer.build_mono_chunk_config(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-2)    chunk_indices,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-3)    param_configs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-4)    param_config_keys,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-5)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-6)    flat_ann_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-7)    mono_reduce=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-8)    mono_merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-9)    mono_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-10)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-28-11))
    

Build the parameter config for a mono-chunk.

* * *

### clean_index_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1138-L1141 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.clean_index_kwargs "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### execute_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1257-L1260 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.execute_kwargs "Permanent link")

Keyword arguments passed to [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute "vectorbtpro.utils.execution.execute").

* * *

### filter_results class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1217-L1220 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.filter_results "Permanent link")

Whether to filter [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "vectorbtpro.utils.execution.NoResult") results.

* * *

### find_params_in_obj class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1262-L1267 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.find_params_in_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-29-1)Parameterizer.find_params_in_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-29-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-29-3)    eval_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-29-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-29-5))
    

Find values wrapped with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param") in a recursive manner.

Uses [find_in_obj](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_in_obj "vectorbtpro.utils.search_.find_in_obj").

* * *

### forward_kwargs_as class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1160-L1165 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.forward_kwargs_as "Permanent link")

Map to rename keyword arguments.

Can also pass any variable from the scope of `Parameterized.run`.

* * *

### get_mono_chunk_indices class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1441-L1478 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.get_mono_chunk_indices "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-30-1)Parameterizer.get_mono_chunk_indices(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-30-2)    param_configs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-30-3)    mono_min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-30-4)    mono_n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-30-5)    mono_chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-30-6)    mono_chunk_meta=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-30-7))
    

Get the indices of each mono-chunk.

* * *

### get_var_arg_names class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1305-L1315 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.get_var_arg_names "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-31-1)Parameterizer.get_var_arg_names(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-31-2)    ann_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-31-3))
    

Get the name of any packed variable position arguments and keyword arguments.

* * *

### grid_indices class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1103-L1106 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.grid_indices "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### iter_tasks class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1419-L1439 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.iter_tasks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-32-1)Parameterizer.iter_tasks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-32-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-32-3)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-32-4)    param_configs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-32-5)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-32-6))
    

Yield functions and their arguments for execution.

* * *

### max_guesses class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1123-L1126 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.max_guesses "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### max_misses class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1128-L1131 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.max_misses "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### merge_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1232-L1237 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.merge_func "Permanent link")

Merging function.

Resolved using [resolve_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/base/merging/#vectorbtpro.base.merging.resolve_merge_func "vectorbtpro.base.merging.resolve_merge_func").

* * *

### merge_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1239-L1245 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.merge_kwargs "Permanent link")

Keyword arguments passed to the merging function.

When defining a custom merging function, make sure to make use of `param_index` (via templates) to build the final index hierarchy.

* * *

### mono_chunk_len class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1181-L1186 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.mono_chunk_len "Permanent link")

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

Applied to generate chunk meta.

* * *

### mono_chunk_meta class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1188-L1191 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.mono_chunk_meta "Permanent link")

Chunk meta.

* * *

### mono_merge_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1201-L1207 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.mono_merge_func "Permanent link")

See [Param.mono_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.mono_merge_func "vectorbtpro.utils.params.Param.mono_merge_func").

Can be a dictionary with a value per (unpacked) argument name. Otherwise, gets applied to each parameter, unless the parameter overrides it.

* * *

### mono_merge_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1209-L1215 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.mono_merge_kwargs "Permanent link")

See [Param.mono_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.mono_merge_kwargs "vectorbtpro.utils.params.Param.mono_merge_kwargs").

Can be a dictionary with a value per (unpacked) argument name. Otherwise, gets applied to each parameter, unless the parameter overrides it.

* * *

### mono_min_size class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1167-L1172 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.mono_min_size "Permanent link")

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

Applied to generate chunk meta.

* * *

### mono_n_chunks class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1174-L1179 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.mono_n_chunks "Permanent link")

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

Applied to generate chunk meta.

* * *

### mono_reduce class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1193-L1199 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.mono_reduce "Permanent link")

See [Param.mono_reduce](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param.mono_reduce "vectorbtpro.utils.params.Param.mono_reduce").

Can be a dictionary with a value per (unpacked) argument name. Otherwise, gets applied to each parameter, unless the parameter overrides it.

* * *

### name_tuple_to_str class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1143-L1146 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.name_tuple_to_str "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### param_product_to_objs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1269-L1282 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.param_product_to_objs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-33-1)Parameterizer.param_product_to_objs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-33-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-33-3)    param_product
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-33-4))
    

Resolve parameter product into a list of objects based on the original object.

Uses [replace_in_obj](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace_in_obj "vectorbtpro.utils.search_.replace_in_obj").

* * *

### param_search_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1078-L1081 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.param_search_kwargs "Permanent link")

See `Parameterized.find_params_in_obj`.

* * *

### parse_and_inject_params class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1284-L1303 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.parse_and_inject_params "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-34-1)Parameterizer.parse_and_inject_params(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-34-2)    flat_ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-34-3)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-34-4))
    

Parse [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param") instances from function annotations and inject them into flattened annotated arguments.

* * *

### raise_no_results class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1222-L1230 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.raise_no_results "Permanent link")

Whether to raise [NoResultsException](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResultsException "vectorbtpro.utils.execution.NoResultsException") if there are no results.

Otherwise, returns [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "vectorbtpro.utils.execution.NoResult").

Has effect only if [Parameterizer.filter_results](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.filter_results "vectorbtpro.utils.params.Parameterizer.filter_results") is True. But regardless of this setting, gets passed to the merging function if the merging function is pre-configured.

* * *

### random_replace class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1113-L1116 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.random_replace "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### random_sort class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1118-L1121 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.random_sort "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### random_subset class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1108-L1111 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.random_subset "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### return_meta class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1247-L1250 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.return_meta "Permanent link")

Whether to return all the metadata generated before running the function.

* * *

### return_param_index class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1252-L1255 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.return_param_index "Permanent link")

Whether to return the results along with the parameter index (as a tuple).

* * *

### roll_param_config class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1330-L1349 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.roll_param_config "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-35-1)Parameterizer.roll_param_config(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-35-2)    param_config,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-35-3)    ann_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-35-4))
    

Roll a parameter config.

* * *

### run method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1573-L1881 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.run "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-36-1)Parameterizer.run(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-36-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-36-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-36-4)    param_configs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-36-5)    eval_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-36-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-36-7))
    

Parameterize arguments and run the function.

* * *

### seed class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1133-L1136 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.seed "Permanent link")

See [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params "vectorbtpro.utils.params.combine_params").

* * *

### select_comb class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1351-L1417 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.select_comb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-37-1)Parameterizer.select_comb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-37-2)    param_configs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-37-3)    param_index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-37-4)    selection,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-37-5)    single_comb=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-37-6)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-37-7)    raise_no_results=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-37-8))
    

Select a parameter combination from parameter configs and index.

* * *

### selection class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1148-L1158 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.selection "Permanent link")

Parameter combination to select.

The selection can be one or more positions or labels from the parameter index. The selection value(s) can be wrapped with [PosSel](https://vectorbt.pro/pvt_7a467f6b/api/utils/selection/#vectorbtpro.utils.selection.PosSel "vectorbtpro.utils.selection.PosSel") or [LabelSel](https://vectorbt.pro/pvt_7a467f6b/api/utils/selection/#vectorbtpro.utils.selection.LabelSel "vectorbtpro.utils.selection.LabelSel") to instruct vectorbtpro what the value(s) should denote. Make sure that it's a sequence (for example, by wrapping it with a list) to attach the parameter index to the final result. It can be also [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "vectorbtpro.utils.execution.NoResult") to indicate that there's no result, or a template to yield any of the above.

* * *

### skip_single_comb class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1083-L1086 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.skip_single_comb "Permanent link")

Whether to execute the function directly if there's only one parameter combination.

* * *

### template_context class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1088-L1096 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.template_context "Permanent link")

Template context.

Any template in both `execute_kwargs` and `merge_kwargs` will be substituted. You can use the keys `param_configs`, `param_index`, all keys in `template_context`, and all arguments as found in the signature of the function. To substitute templates further down the pipeline, use substitution ids.

* * *

### unroll_param_config class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/params.py#L1317-L1328 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer.unroll_param_config "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-38-1)Parameterizer.unroll_param_config(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-38-2)    param_config,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-38-3)    ann_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#__codelineno-38-4))
    

Unroll a parameter config.
