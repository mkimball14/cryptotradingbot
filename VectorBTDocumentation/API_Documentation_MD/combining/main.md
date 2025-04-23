combining

#  combining module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining "Permanent link")

Functions for combining arrays.

Combine functions combine two or more NumPy arrays using a custom function. The emphasis here is done upon stacking the results into one NumPy array - since vectorbt is all about brute-forcing large spaces of hyper-parameters, concatenating the results of each hyper-parameter combination into a single DataFrame is important. All functions are available in both Python and Numba-compiled form.

* * *

## apply_and_concat function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L166-L223 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.apply_and_concat "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-1)apply_and_concat(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-2)    ntimes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-3)    apply_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-4)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-5)    n_outputs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-6)    jitted_loop=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-7)    jitted_warmup=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-8)    execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-9)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-0-10))
    

Run `apply_func` function a number of times and concatenate the results depending upon how many array-like objects it generates.

`apply_func` must accept arguments `i`, `*args`, and `**kwargs`.

Set `jitted_loop` to True to use the JIT-compiled version.

All jitted iteration functions are resolved using [JITRegistry.resolve](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve "vectorbtpro.registries.jit_registry.JITRegistry.resolve").

Note

`n_outputs` must be set when `jitted_loop` is True.

Numba doesn't support variable keyword arguments.

* * *

## apply_and_concat_each function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L136-L163 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.apply_and_concat_each "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-1-1)apply_and_concat_each(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-1-2)    tasks,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-1-3)    n_outputs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-1-4)    execute_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-1-5))
    

Apply each function on its own set of positional and keyword arguments.

Executes the function using [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute "vectorbtpro.utils.execution.execute").

* * *

## apply_and_concat_multiple_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L124-L133 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.apply_and_concat_multiple_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-2-1)apply_and_concat_multiple_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-2-2)    ntimes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-2-3)    apply_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-2-4)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-2-5))
    

Run `apply_func_nb` that returns multiple arrays number of times.

Uses [custom_apply_and_concat_multiple_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.custom_apply_and_concat_multiple_nb "vectorbtpro.base.combining.custom_apply_and_concat_multiple_nb").

* * *

## apply_and_concat_none_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L42-L51 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.apply_and_concat_none_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-3-1)apply_and_concat_none_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-3-2)    ntimes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-3-3)    apply_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-3-4)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-3-5))
    

Run `apply_func_nb` that returns nothing number of times.

Uses [custom_apply_and_concat_none_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.custom_apply_and_concat_none_nb "vectorbtpro.base.combining.custom_apply_and_concat_none_nb").

* * *

## apply_and_concat_one_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L80-L89 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.apply_and_concat_one_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-4-1)apply_and_concat_one_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-4-2)    ntimes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-4-3)    apply_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-4-4)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-4-5))
    

Run `apply_func_nb` that returns one array number of times.

Uses [custom_apply_and_concat_one_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.custom_apply_and_concat_one_nb "vectorbtpro.base.combining.custom_apply_and_concat_one_nb").

* * *

## combine_and_concat function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L261-L286 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.combine_and_concat "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-5-1)combine_and_concat(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-5-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-5-3)    others,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-5-4)    combine_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-5-5)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-5-6)    jitted_loop=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-5-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-5-8))
    

Combine `obj` with each in `others` using `combine_func` and concatenate.

[select_and_combine_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.select_and_combine_nb "vectorbtpro.base.combining.select_and_combine_nb") is resolved using [JITRegistry.resolve](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve "vectorbtpro.registries.jit_registry.JITRegistry.resolve").

* * *

## combine_and_concat_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L238-L246 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.combine_and_concat_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-6-1)combine_and_concat_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-6-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-6-3)    others,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-6-4)    combine_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-6-5)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-6-6))
    

Numba-compiled version of [combine_and_concat](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.combine_and_concat "vectorbtpro.base.combining.combine_and_concat").

* * *

## combine_multiple function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L302-L323 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.combine_multiple "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-7-1)combine_multiple(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-7-2)    objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-7-3)    combine_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-7-4)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-7-5)    jitted_loop=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-7-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-7-7))
    

Combine `objs` pairwise into a single object.

Set `jitted_loop` to True to use the JIT-compiled version.

[combine_multiple_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.combine_multiple_nb "vectorbtpro.base.combining.combine_multiple_nb") is resolved using [JITRegistry.resolve](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve "vectorbtpro.registries.jit_registry.JITRegistry.resolve").

Note

Numba doesn't support variable keyword arguments.

* * *

## combine_multiple_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L289-L299 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.combine_multiple_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-8-1)combine_multiple_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-8-2)    objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-8-3)    combine_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-8-4)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-8-5))
    

Numba-compiled version of [combine_multiple](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.combine_multiple "vectorbtpro.base.combining.combine_multiple").

* * *

## custom_apply_and_concat_multiple_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L101-L121 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.custom_apply_and_concat_multiple_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-9-1)custom_apply_and_concat_multiple_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-9-2)    indices,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-9-3)    apply_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-9-4)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-9-5))
    

Run `apply_func_nb` that returns multiple arrays for each index.

* * *

## custom_apply_and_concat_none_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L29-L39 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.custom_apply_and_concat_none_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-10-1)custom_apply_and_concat_none_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-10-2)    indices,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-10-3)    apply_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-10-4)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-10-5))
    

Run `apply_func_nb` that returns nothing for each index.

Meant for in-place outputs.

* * *

## custom_apply_and_concat_one_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L62-L77 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.custom_apply_and_concat_one_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-11-1)custom_apply_and_concat_one_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-11-2)    indices,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-11-3)    apply_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-11-4)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-11-5))
    

Run `apply_func_nb` that returns one array for each index.

* * *

## select_and_combine function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L249-L258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.select_and_combine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-12-1)select_and_combine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-12-2)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-12-3)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-12-4)    others,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-12-5)    combine_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-12-6)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-12-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-12-8))
    

Combine `obj` with an array at position `i` in `others` using `combine_func`.

* * *

## select_and_combine_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L226-L235 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.select_and_combine_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-13-1)select_and_combine_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-13-2)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-13-3)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-13-4)    others,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-13-5)    combine_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-13-6)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-13-7))
    

Numba-compiled version of [select_and_combine](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.select_and_combine "vectorbtpro.base.combining.select_and_combine").

* * *

## to_2d_multiple_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L92-L98 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.to_2d_multiple_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-14-1)to_2d_multiple_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-14-2)    a
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-14-3))
    

Expand the dimensions of each array in `a` along axis 1.

* * *

## to_2d_one_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/combining.py#L54-L59 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#vectorbtpro.base.combining.to_2d_one_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-15-1)to_2d_one_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-15-2)    a
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/combining/#__codelineno-15-3))
    

Expand the dimensions of the array along the axis 1.
