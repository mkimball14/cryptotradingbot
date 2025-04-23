execution

#  execution module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution "Permanent link")

Engines for executing functions.

* * *

## DUMMY literal[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.DUMMY "Permanent link")

Sentinel that represents a missing value.

* * *

## NoResult literal[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "Permanent link")

Sentinel that represents no result.

* * *

## execute function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L2431-L2483 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-1)execute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-2)    tasks,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-3)    size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-4)    keys=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-5)    executor=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-6)    replace_executor=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-7)    merge_to_engine_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-0-9))
    

Execute functions and their arguments using [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor").

Keyword arguments not listed in [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor") and `engine_config` are merged into `engine_config` if `merge_to_engine_config` is True, otherwise, they are passed directly to [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor").

If an executor instance is provided and `replace_executor` is True, will create a new [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor") instance by replacing any arguments that are not None.

* * *

## filter_out_no_results function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L135-L162 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.filter_out_no_results "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-1-1)filter_out_no_results(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-1-2)    objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-1-3)    keys=_Missing.MISSING,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-1-4)    raise_error=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-1-5))
    

Filter objects and keys by removing [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "vectorbtpro.utils.execution.NoResult") objects.

* * *

## iterated function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L2528-L2673 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.iterated "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-2-1)iterated(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-2-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-2-3)    over_arg=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-2-4)    executor=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-2-5)    replace_executor=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-2-6)    merge_to_engine_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-2-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-2-8))
    

Decorator that executes a function in iteration using [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor").

Returns a new function with the same signature as the passed one.

Use `over_arg` to specify which argument (position or name) should be iterated over. If it's None (default), uses the first argument.

Each option can be modified in the `options` attribute of the wrapper function or directly passed as a keyword argument with a leading underscore. You can also explicitly specify keys and size by passing them as `_keys` and `_size` respectively if the range-like object is an iterator.

Keyword arguments not listed in [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor") and `engine_config` are merged into `engine_config` if `merge_to_engine_config` is True, otherwise, they are passed directly to [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor").

If an executor instance is provided and `replace_executor` is True, will create a new [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor") instance by replacing any arguments that are not None.

If [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "vectorbtpro.utils.execution.NoResult") is returned, will skip the current iteration and remove it from the final index.

* * *

## parse_iterable_and_keys function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L2486-L2525 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.parse_iterable_and_keys "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-3-1)parse_iterable_and_keys(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-3-2)    iterable_like,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-3-3)    keys=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-3-4))
    

Parse the iterable and the keys from an iterable-like and a keys-like object respectively.

Object can be an integer that will be interpreted as a total or any iterable.

If object is a dictionary, a Pandas Index, or a Pandas Series, keys will be set to the index. Otherwise, keys will be extracted using [index_from_values](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.index_from_values "vectorbtpro.base.indexes.index_from_values"). Keys won't be extracted if the object is not a sequence to avoid materializing it.

* * *

## pass_kwargs_as_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L424-L426 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.pass_kwargs_as_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-4-1)pass_kwargs_as_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-4-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-4-3)    args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-4-4)    kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-4-5))
    

Helper function for `pathos.pools.ParallelPool`.

* * *

## DaskEngine class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L642-L698 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.DaskEngine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-5-1)DaskEngine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-5-2)    compute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-5-3)    hide_inner_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-5-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-5-5))
    

Class for executing functions in parallel using Dask.

For defaults, see `engines.dask` in [execution](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "vectorbtpro._settings.execution").

Note

Use multi-threading mainly on numeric code that releases the GIL (like NumPy, Pandas, Scikit-Learn, Numba).

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.execution.ExecutionEngine.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.execution.ExecutionEngine.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.execution.ExecutionEngine.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.execution.ExecutionEngine.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.execution.ExecutionEngine.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.execution.ExecutionEngine.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.execution.ExecutionEngine.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.execution.ExecutionEngine.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.execution.ExecutionEngine.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.execution.ExecutionEngine.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.execution.ExecutionEngine.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.execution.ExecutionEngine.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.execution.ExecutionEngine.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.execution.ExecutionEngine.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.execution.ExecutionEngine.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.execution.ExecutionEngine.update_config")
  * [ExecutionEngine.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.execution.ExecutionEngine.config")
  * [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute")
  * [ExecutionEngine.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.execution.ExecutionEngine.rec_state")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.execution.ExecutionEngine.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.execution.ExecutionEngine.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.execution.ExecutionEngine.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.execution.ExecutionEngine.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.execution.ExecutionEngine.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.execution.ExecutionEngine.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.execution.ExecutionEngine.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.execution.ExecutionEngine.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.execution.ExecutionEngine.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.execution.ExecutionEngine.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.execution.ExecutionEngine.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.execution.ExecutionEngine.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.execution.ExecutionEngine.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.execution.ExecutionEngine.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.execution.ExecutionEngine.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.execution.ExecutionEngine.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.execution.ExecutionEngine.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.execution.ExecutionEngine.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.execution.ExecutionEngine.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.execution.ExecutionEngine.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.execution.ExecutionEngine.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.execution.ExecutionEngine.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.execution.ExecutionEngine.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.execution.ExecutionEngine.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.execution.ExecutionEngine.pprint")



* * *

### compute_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L669-L672 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.DaskEngine.compute_kwargs "Permanent link")

Keyword arguments passed to `dask.compute`.

* * *

### hide_inner_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L674-L677 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.DaskEngine.hide_inner_progress "Permanent link")

Whether to hide progress bars within each thread.

* * *

## ExecutionEngine class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L165-L177 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-6-1)ExecutionEngine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-6-2)    **config
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-6-3))
    

Abstract class for executing functions.

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



**Subclasses**

  * [DaskEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.DaskEngine "vectorbtpro.utils.execution.DaskEngine")
  * [MpireEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.MpireEngine "vectorbtpro.utils.execution.MpireEngine")
  * [PathosEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine "vectorbtpro.utils.execution.PathosEngine")
  * [ProcessPoolEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ProcessPoolEngine "vectorbtpro.utils.execution.ProcessPoolEngine")
  * [RayEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine "vectorbtpro.utils.execution.RayEngine")
  * [SerialEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine "vectorbtpro.utils.execution.SerialEngine")
  * [ThreadPoolEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ThreadPoolEngine "vectorbtpro.utils.execution.ThreadPoolEngine")



* * *

### execute method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L168-L177 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-7-1)ExecutionEngine.execute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-7-2)    tasks,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-7-3)    size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-7-4)    keys=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-7-5))
    

Run an iterable of tuples out of a function, arguments, and keyword arguments.

Provide `size` in case `tasks` is a generator and the underlying engine needs it.

* * *

## Executor class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L906-L2428 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-1)Executor(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-2)    engine=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-3)    engine_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-4)    min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-5)    n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-6)    chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-7)    chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-8)    distribute=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-9)    warmup=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-10)    in_chunk_order=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-11)    cache_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-12)    chunk_cache_dir=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-13)    chunk_cache_save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-14)    chunk_cache_load_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-15)    pre_clear_chunk_cache=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-16)    post_clear_chunk_cache=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-17)    release_chunk_cache=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-18)    chunk_clear_cache=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-19)    chunk_collect_garbage=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-20)    chunk_delay=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-21)    pre_execute_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-22)    pre_execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-23)    pre_chunk_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-24)    pre_chunk_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-25)    post_chunk_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-26)    post_chunk_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-27)    post_execute_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-28)    post_execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-29)    post_execute_on_sorted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-30)    filter_results=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-31)    raise_no_results=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-32)    merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-33)    merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-34)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-35)    show_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-36)    pbar_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-37)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-8-38))
    

Class responsible executing functions.

Supported values for `engine`:

  * Name of the engine (see supported engines)
  * Subclass of [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine") \- initializes with `engine_config`
  * Instance of [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine") \- calls [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute") with `size`
  * Callable - passes `tasks`, `size` (if not None), and `engine_config`



Can execute per chunk if `chunk_meta` is provided. Otherwise, if any of `n_chunks` and `chunk_len` are set, passes them to [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta") to generate `chunk_meta`. Arguments `n_chunks` and `chunk_len` can be set globally in the engine-specific settings. Set `n_chunks` and `chunk_len` to 'auto' to set them to the number of cores.

If `distribute` is "tasks", distributes tasks within each chunk. If indices in `chunk_meta` are perfectly sorted and `tasks` is an iterable, iterates over `tasks` to avoid converting it into a list. Otherwise, iterates over `chunk_meta`. If `in_chunk_order` is True, returns the results in the order they appear in `chunk_meta`. Otherwise, always returns them in the same order as in `tasks`.

If `distribute` is "chunks", distributes chunks. For this, executes tasks within each chunk serially using [Executor.execute_serially](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.execute_serially "vectorbtpro.utils.execution.Executor.execute_serially"). Also, compresses each chunk such that each unique function, positional argument, and keyword argument is serialized only once.

If `tasks` is a custom template, substitutes it once `chunk_meta` is established. Use `template_context` as an additional context. All the resolved functions and arguments will be immediately passed to the executor.

If `pre_chunk_func` is not None, calls the function before processing a chunk. If it returns anything other than None, the returned object will be appended to the results and the chunk won't be executed. This enables use cases such as caching. If `post_chunk_func` is not None, calls the function after processing the chunk. It should return either None to keep the old call results, or return new ones. Will also substitute any templates in `pre_chunk_kwargs` and `post_chunk_kwargs` and pass them as keyword arguments. The following additional arguments are available in the contexts: the index of the current chunk `chunk_idx`, the list of call indices `call_indices` in the chunk, the list of call results `chunk_cache` returned from caching (only for `pre_chunk_func`), the list of call results `call_results` returned by executing the chunk (only for `post_chunk_func`), and whether the chunk was executed `chunk_executed` or otherwise returned by `pre_chunk_func` (only for `post_chunk_func`).

Note

The both callbacks above are effective only when `distribute` is "tasks" and chunking is enabled.

If `pre_execute_func` is not None, calls the function before processing all tasks. Should return nothing (None). Will also substitute any templates in `post_execute_kwargs` and pass them as keyword arguments. The following additional arguments are available in the context: the number of chunks `n_chunks`.

If `post_execute_func` is not None, calls the function after processing all tasks. Will also substitute any templates in `post_execute_kwargs` and pass them as keyword arguments. Should return either None to keep the default results or return the new ones. The following additional arguments are available in the context: the number of chunks `n_chunks` and the generated flattened list of results `results`. If `post_execute_on_sorted` is True, will run the callback after sorting the call indices.

Info

Chunks are processed sequentially, while functions within each chunk can be processed distributively.

For defaults, see [execution](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "vectorbtpro._settings.execution").

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

### build_serial_chunk class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1576-L1596 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.build_serial_chunk "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-9-1)Executor.build_serial_chunk(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-9-2)    tasks
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-9-3))
    

Build a serial chunk.

* * *

### cache_chunks class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1419-L1422 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.cache_chunks "Permanent link")

Whether to cache chunks.

* * *

### call_execute class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1682-L1699 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.call_execute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-10-1)Executor.call_execute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-10-2)    engine,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-10-3)    tasks,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-10-4)    size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-10-5)    keys=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-10-6))
    

Call [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute").

* * *

### call_post_chunk_func class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1701-L1772 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.call_post_chunk_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-1)Executor.call_post_chunk_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-2)    chunk_idx,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-3)    call_indices,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-4)    call_results,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-5)    cache_chunks=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-6)    chunk_cache_dir=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-7)    chunk_cache_save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-8)    release_chunk_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-9)    chunk_clear_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-10)    chunk_collect_garbage=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-11)    chunk_delay=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-12)    post_chunk_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-13)    post_chunk_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-14)    chunk_executed=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-15)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-11-16))
    

Call [Executor.post_chunk_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_chunk_func "vectorbtpro.utils.execution.Executor.post_chunk_func").

* * *

### call_post_execute_func class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1774-L1825 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.call_post_execute_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-1)Executor.call_post_execute_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-2)    results,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-3)    cache_chunks=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-4)    chunk_cache_dir=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-5)    chunk_cache_load_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-6)    post_clear_chunk_cache=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-7)    release_chunk_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-8)    post_execute_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-9)    post_execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-10)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-12-11))
    

Call [Executor.post_execute_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_execute_func "vectorbtpro.utils.execution.Executor.post_execute_func").

* * *

### call_pre_chunk_func class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1629-L1680 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.call_pre_chunk_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-1)Executor.call_pre_chunk_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-2)    chunk_idx,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-3)    call_indices,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-4)    cache_chunks=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-5)    chunk_cache_dir=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-6)    chunk_cache_load_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-7)    release_chunk_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-8)    pre_chunk_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-9)    pre_chunk_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-10)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-13-11))
    

Call [Executor.pre_chunk_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_chunk_func "vectorbtpro.utils.execution.Executor.pre_chunk_func").

* * *

### call_pre_execute_func class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1598-L1627 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.call_pre_execute_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-14-1)Executor.call_pre_execute_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-14-2)    cache_chunks=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-14-3)    chunk_cache_dir=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-14-4)    pre_clear_chunk_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-14-5)    pre_execute_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-14-6)    pre_execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-14-7)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-14-8))
    

Call [Executor.pre_execute_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_execute_func "vectorbtpro.utils.execution.Executor.pre_execute_func").

* * *

### chunk_cache_dir class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1424-L1427 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.chunk_cache_dir "Permanent link")

Directory where to put chunk cache files.

* * *

### chunk_cache_load_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1434-L1437 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.chunk_cache_load_kwargs "Permanent link")

Keyword arguments passed to [load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.load "vectorbtpro.utils.pickling.load") for chunk caching.

* * *

### chunk_cache_save_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1429-L1432 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.chunk_cache_save_kwargs "Permanent link")

Keyword arguments passed to [save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.save "vectorbtpro.utils.pickling.save") for chunk caching.

* * *

### chunk_clear_cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1455-L1458 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.chunk_clear_cache "Permanent link")

Whether to clear global cache after each chunk or every n chunks.

* * *

### chunk_collect_garbage class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1460-L1463 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.chunk_collect_garbage "Permanent link")

Whether to collect garbage after each chunk or every n chunks.

* * *

### chunk_delay class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1465-L1468 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.chunk_delay "Permanent link")

Number of seconds to sleep after each chunk.

* * *

### chunk_len class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1392-L1395 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.chunk_len "Permanent link")

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

* * *

### chunk_meta class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1397-L1400 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.chunk_meta "Permanent link")

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

* * *

### distribute class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1402-L1405 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.distribute "Permanent link")

Distribution mode.

* * *

### engine class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1377-L1380 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.engine "Permanent link")

Engine resolved with [Executor.resolve_engine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.resolve_engine "vectorbtpro.utils.execution.Executor.resolve_engine").

* * *

### execute_serially static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1565-L1574 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.execute_serially "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-15-1)Executor.execute_serially(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-15-2)    tasks,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-15-3)    id_objs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-15-4))
    

Execute serially.

* * *

### filter_results class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1522-L1525 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.filter_results "Permanent link")

Whether to filter [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "vectorbtpro.utils.execution.NoResult") results.

* * *

### get_engine_setting class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L984-L991 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.get_engine_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-16-1)Executor.get_engine_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-16-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-16-3)    engine_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-16-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-16-5))
    

[HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.execution.Executor.get_setting") with `sub_path=engine_name`.

* * *

### get_engine_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L966-L973 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.get_engine_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-17-1)Executor.get_engine_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-17-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-17-3)    engine_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-17-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-17-5))
    

[HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.execution.Executor.get_settings") with `sub_path=engine_name`.

* * *

### has_engine_setting class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L993-L1000 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.has_engine_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-18-1)Executor.has_engine_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-18-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-18-3)    engine_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-18-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-18-5))
    

[HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.execution.Executor.has_setting") with `sub_path=engine_name`.

* * *

### has_engine_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L975-L982 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.has_engine_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-19-1)Executor.has_engine_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-19-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-19-3)    engine_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-19-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-19-5))
    

[HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.execution.Executor.has_settings") with `sub_path=engine_name`.

* * *

### in_chunk_order class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1412-L1417 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.in_chunk_order "Permanent link")

Whether to return the results in the order they appear in `chunk_meta`.

Otherwise, always returns them in the same order as in `tasks`.

* * *

### merge_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1535-L1540 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.merge_func "Permanent link")

Merging function.

Resolved using [resolve_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/base/merging/#vectorbtpro.base.merging.resolve_merge_func "vectorbtpro.base.merging.resolve_merge_func").

* * *

### merge_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1542-L1545 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.merge_kwargs "Permanent link")

Keyword arguments passed to the merging function.

* * *

### merge_results class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1827-L1870 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.merge_results "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-1)Executor.merge_results(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-2)    results,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-3)    keys=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-4)    filter_results=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-5)    raise_no_results=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-6)    merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-7)    merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-8)    template_context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-20-9))
    

Merge results using [Executor.merge_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.merge_func "vectorbtpro.utils.execution.Executor.merge_func") and [Executor.merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.merge_kwargs "vectorbtpro.utils.execution.Executor.merge_kwargs").

* * *

### min_size class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1382-L1385 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.min_size "Permanent link")

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

* * *

### n_chunks class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1387-L1390 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.n_chunks "Permanent link")

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

* * *

### pbar_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1560-L1563 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pbar_kwargs "Permanent link")

Keyword arguments passed to [ProgressBar](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar "vectorbtpro.utils.pbar.ProgressBar").

* * *

### post_chunk_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1493-L1498 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_chunk_func "Permanent link")

Function to call after processing the chunk.

It should return either None to keep the old call results, or return new ones.

* * *

### post_chunk_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1500-L1503 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_chunk_kwargs "Permanent link")

Keyword arguments passed to [Executor.post_chunk_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_chunk_func "vectorbtpro.utils.execution.Executor.post_chunk_func").

* * *

### post_clear_chunk_cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1444-L1447 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_clear_chunk_cache "Permanent link")

Whether to remove the chunk cache directory after execution.

* * *

### post_execute_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1505-L1510 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_execute_func "Permanent link")

Function to call after processing all tasks.

Should return either None to keep the default results, or return the new ones.

* * *

### post_execute_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1512-L1515 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_execute_kwargs "Permanent link")

Keyword arguments passed to [Executor.post_execute_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_execute_func "vectorbtpro.utils.execution.Executor.post_execute_func").

* * *

### post_execute_on_sorted class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1517-L1520 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_execute_on_sorted "Permanent link")

Whether to run [Executor.post_execute_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.post_execute_func "vectorbtpro.utils.execution.Executor.post_execute_func") after sorting the call indices.

* * *

### pre_chunk_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1480-L1486 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_chunk_func "Permanent link")

Function to call before processing a chunk.

If it returns anything other than None, the returned object will be appended to the results and the chunk won't be executed. This enables use cases such as caching.

* * *

### pre_chunk_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1488-L1491 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_chunk_kwargs "Permanent link")

Keyword arguments passed to [Executor.pre_chunk_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_chunk_func "vectorbtpro.utils.execution.Executor.pre_chunk_func").

* * *

### pre_clear_chunk_cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1439-L1442 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_clear_chunk_cache "Permanent link")

Whether to remove the chunk cache directory before execution.

* * *

### pre_execute_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1470-L1473 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_execute_func "Permanent link")

Function to call before processing all tasks.

* * *

### pre_execute_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1475-L1478 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_execute_kwargs "Permanent link")

Keyword arguments passed to [Executor.pre_execute_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.pre_execute_func "vectorbtpro.utils.execution.Executor.pre_execute_func").

* * *

### raise_no_results class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1527-L1533 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.raise_no_results "Permanent link")

Whether to raise [NoResultsException](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResultsException "vectorbtpro.utils.execution.NoResultsException") if there are no results. Otherwise, returns [NoResult](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResult "vectorbtpro.utils.execution.NoResult").

Has effect only if [Executor.filter_results](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.filter_results "vectorbtpro.utils.execution.Executor.filter_results") is True. But regardless of this setting, gets passed to the merging function if the merging function is pre-configured.

* * *

### release_chunk_cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1449-L1453 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.release_chunk_cache "Permanent link")

Whether to replace chunk cache with dummy objects once the chunk has been executed and then load all cache at once after all chunks have been executed.

* * *

### resolve_engine class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1020-L1102 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.resolve_engine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-21-1)Executor.resolve_engine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-21-2)    engine,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-21-3)    show_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-21-4)    pbar_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-21-5)    **engine_config
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-21-6))
    

Resolve engine and its name in settings.

* * *

### resolve_engine_setting class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1002-L1009 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.resolve_engine_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-22-1)Executor.resolve_engine_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-22-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-22-3)    engine_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-22-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-22-5))
    

[HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.execution.Executor.resolve_setting") with `sub_path=engine_name`.

* * *

### run method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1872-L2428 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.run "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-23-1)Executor.run(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-23-2)    tasks,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-23-3)    size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-23-4)    keys=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-23-5))
    

Execute functions and their arguments.

* * *

### set_engine_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1011-L1018 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.set_engine_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-24-1)Executor.set_engine_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-24-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-24-3)    engine_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-24-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-24-5))
    

[HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.execution.Executor.set_settings") with `sub_path=engine_name`.

* * *

### show_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1552-L1558 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.show_progress "Permanent link")

Whether to show progress bar when iterating over chunks.

If [Executor.engine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.engine "vectorbtpro.utils.execution.Executor.engine") accepts `show_progress` and there's no key `show_progress` in `engine_config`, then passes it to the engine as well.

* * *

### template_context class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1547-L1550 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.template_context "Permanent link")

Context used to substitute templates.

* * *

### warmup class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L1407-L1410 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor.warmup "Permanent link")

Whether to call the first item of `tasks` once before distribution.

* * *

## MpireEngine class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L576-L639 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.MpireEngine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-25-1)MpireEngine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-25-2)    init_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-25-3)    apply_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-25-4)    hide_inner_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-25-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-25-6))
    

Class for executing functions using `WorkerPool` from `mpire`.

For defaults, see `engines.mpire` in [execution](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "vectorbtpro._settings.execution").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.execution.ExecutionEngine.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.execution.ExecutionEngine.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.execution.ExecutionEngine.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.execution.ExecutionEngine.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.execution.ExecutionEngine.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.execution.ExecutionEngine.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.execution.ExecutionEngine.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.execution.ExecutionEngine.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.execution.ExecutionEngine.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.execution.ExecutionEngine.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.execution.ExecutionEngine.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.execution.ExecutionEngine.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.execution.ExecutionEngine.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.execution.ExecutionEngine.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.execution.ExecutionEngine.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.execution.ExecutionEngine.update_config")
  * [ExecutionEngine.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.execution.ExecutionEngine.config")
  * [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute")
  * [ExecutionEngine.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.execution.ExecutionEngine.rec_state")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.execution.ExecutionEngine.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.execution.ExecutionEngine.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.execution.ExecutionEngine.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.execution.ExecutionEngine.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.execution.ExecutionEngine.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.execution.ExecutionEngine.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.execution.ExecutionEngine.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.execution.ExecutionEngine.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.execution.ExecutionEngine.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.execution.ExecutionEngine.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.execution.ExecutionEngine.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.execution.ExecutionEngine.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.execution.ExecutionEngine.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.execution.ExecutionEngine.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.execution.ExecutionEngine.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.execution.ExecutionEngine.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.execution.ExecutionEngine.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.execution.ExecutionEngine.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.execution.ExecutionEngine.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.execution.ExecutionEngine.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.execution.ExecutionEngine.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.execution.ExecutionEngine.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.execution.ExecutionEngine.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.execution.ExecutionEngine.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.execution.ExecutionEngine.pprint")



* * *

### apply_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L607-L610 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.MpireEngine.apply_kwargs "Permanent link")

Keyword arguments passed to `WorkerPool.async_apply`.

* * *

### hide_inner_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L612-L615 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.MpireEngine.hide_inner_progress "Permanent link")

Whether to hide progress bars within each thread.

* * *

### init_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L602-L605 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.MpireEngine.init_kwargs "Permanent link")

Keyword arguments used to initialize `WorkerPool`.

* * *

## NoResultsException class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L129-L132 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.NoResultsException "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-26-1)NoResultsException(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-26-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-26-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-26-4))
    

Gets raised when there are no results.

**Superclasses**

  * `builtins.BaseException`
  * `builtins.Exception`



* * *

## PathosEngine class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L429-L573 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-1)PathosEngine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-2)    pool_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-3)    init_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-4)    timeout=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-5)    check_delay=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-6)    show_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-7)    pbar_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-8)    hide_inner_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-9)    join_pool=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-10)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-27-11))
    

Class for executing functions using `pathos`.

For defaults, see `engines.pathos` in [execution](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "vectorbtpro._settings.execution").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.execution.ExecutionEngine.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.execution.ExecutionEngine.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.execution.ExecutionEngine.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.execution.ExecutionEngine.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.execution.ExecutionEngine.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.execution.ExecutionEngine.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.execution.ExecutionEngine.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.execution.ExecutionEngine.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.execution.ExecutionEngine.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.execution.ExecutionEngine.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.execution.ExecutionEngine.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.execution.ExecutionEngine.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.execution.ExecutionEngine.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.execution.ExecutionEngine.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.execution.ExecutionEngine.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.execution.ExecutionEngine.update_config")
  * [ExecutionEngine.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.execution.ExecutionEngine.config")
  * [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute")
  * [ExecutionEngine.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.execution.ExecutionEngine.rec_state")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.execution.ExecutionEngine.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.execution.ExecutionEngine.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.execution.ExecutionEngine.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.execution.ExecutionEngine.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.execution.ExecutionEngine.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.execution.ExecutionEngine.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.execution.ExecutionEngine.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.execution.ExecutionEngine.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.execution.ExecutionEngine.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.execution.ExecutionEngine.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.execution.ExecutionEngine.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.execution.ExecutionEngine.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.execution.ExecutionEngine.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.execution.ExecutionEngine.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.execution.ExecutionEngine.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.execution.ExecutionEngine.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.execution.ExecutionEngine.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.execution.ExecutionEngine.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.execution.ExecutionEngine.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.execution.ExecutionEngine.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.execution.ExecutionEngine.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.execution.ExecutionEngine.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.execution.ExecutionEngine.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.execution.ExecutionEngine.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.execution.ExecutionEngine.pprint")



* * *

### check_delay class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L485-L488 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine.check_delay "Permanent link")

Number of seconds to sleep between checks.

* * *

### hide_inner_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L500-L503 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine.hide_inner_progress "Permanent link")

Whether to hide progress bars within each thread.

* * *

### init_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L475-L478 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine.init_kwargs "Permanent link")

Keyword arguments used to initialize the pool.

* * *

### join_pool class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L505-L508 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine.join_pool "Permanent link")

Whether to join the pool.

* * *

### pbar_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L495-L498 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine.pbar_kwargs "Permanent link")

Keyword arguments passed to [ProgressBar](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar "vectorbtpro.utils.pbar.ProgressBar").

* * *

### pool_type class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L470-L473 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine.pool_type "Permanent link")

Pool type.

* * *

### show_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L490-L493 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine.show_progress "Permanent link")

Whether to show the progress bar.

* * *

### timeout class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L480-L483 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine.timeout "Permanent link")

Timeout.

* * *

## ProcessPoolEngine class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L361-L421 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ProcessPoolEngine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-28-1)ProcessPoolEngine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-28-2)    init_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-28-3)    timeout=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-28-4)    hide_inner_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-28-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-28-6))
    

Class for executing functions using `ProcessPoolExecutor` from `concurrent.futures`.

For defaults, see `engines.processpool` in [execution](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "vectorbtpro._settings.execution").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.execution.ExecutionEngine.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.execution.ExecutionEngine.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.execution.ExecutionEngine.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.execution.ExecutionEngine.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.execution.ExecutionEngine.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.execution.ExecutionEngine.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.execution.ExecutionEngine.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.execution.ExecutionEngine.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.execution.ExecutionEngine.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.execution.ExecutionEngine.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.execution.ExecutionEngine.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.execution.ExecutionEngine.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.execution.ExecutionEngine.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.execution.ExecutionEngine.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.execution.ExecutionEngine.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.execution.ExecutionEngine.update_config")
  * [ExecutionEngine.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.execution.ExecutionEngine.config")
  * [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute")
  * [ExecutionEngine.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.execution.ExecutionEngine.rec_state")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.execution.ExecutionEngine.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.execution.ExecutionEngine.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.execution.ExecutionEngine.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.execution.ExecutionEngine.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.execution.ExecutionEngine.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.execution.ExecutionEngine.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.execution.ExecutionEngine.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.execution.ExecutionEngine.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.execution.ExecutionEngine.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.execution.ExecutionEngine.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.execution.ExecutionEngine.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.execution.ExecutionEngine.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.execution.ExecutionEngine.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.execution.ExecutionEngine.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.execution.ExecutionEngine.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.execution.ExecutionEngine.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.execution.ExecutionEngine.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.execution.ExecutionEngine.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.execution.ExecutionEngine.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.execution.ExecutionEngine.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.execution.ExecutionEngine.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.execution.ExecutionEngine.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.execution.ExecutionEngine.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.execution.ExecutionEngine.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.execution.ExecutionEngine.pprint")



* * *

### hide_inner_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L397-L400 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ProcessPoolEngine.hide_inner_progress "Permanent link")

Whether to hide progress bars within each thread.

* * *

### init_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L387-L390 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ProcessPoolEngine.init_kwargs "Permanent link")

Keyword arguments used to initialize `ProcessPoolExecutor`.

* * *

### timeout class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L392-L395 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ProcessPoolEngine.timeout "Permanent link")

Timeout.

* * *

## RayEngine class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L701-L887 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-1)RayEngine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-2)    restart=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-3)    reuse_refs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-4)    del_refs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-5)    shutdown=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-6)    init_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-7)    remote_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-8)    hide_inner_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-9)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-29-10))
    

Class for executing functions in parallel using Ray.

For defaults, see `engines.ray` in [execution](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "vectorbtpro._settings.execution").

Note

Ray spawns multiple processes as opposed to threads, so any argument and keyword argument must first be put into an object store to be shared. Make sure that the computation with `func` takes a considerable amount of time compared to this copying operation, otherwise there will be a little to no speedup.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.execution.ExecutionEngine.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.execution.ExecutionEngine.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.execution.ExecutionEngine.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.execution.ExecutionEngine.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.execution.ExecutionEngine.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.execution.ExecutionEngine.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.execution.ExecutionEngine.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.execution.ExecutionEngine.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.execution.ExecutionEngine.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.execution.ExecutionEngine.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.execution.ExecutionEngine.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.execution.ExecutionEngine.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.execution.ExecutionEngine.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.execution.ExecutionEngine.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.execution.ExecutionEngine.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.execution.ExecutionEngine.update_config")
  * [ExecutionEngine.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.execution.ExecutionEngine.config")
  * [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute")
  * [ExecutionEngine.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.execution.ExecutionEngine.rec_state")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.execution.ExecutionEngine.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.execution.ExecutionEngine.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.execution.ExecutionEngine.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.execution.ExecutionEngine.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.execution.ExecutionEngine.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.execution.ExecutionEngine.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.execution.ExecutionEngine.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.execution.ExecutionEngine.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.execution.ExecutionEngine.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.execution.ExecutionEngine.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.execution.ExecutionEngine.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.execution.ExecutionEngine.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.execution.ExecutionEngine.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.execution.ExecutionEngine.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.execution.ExecutionEngine.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.execution.ExecutionEngine.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.execution.ExecutionEngine.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.execution.ExecutionEngine.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.execution.ExecutionEngine.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.execution.ExecutionEngine.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.execution.ExecutionEngine.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.execution.ExecutionEngine.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.execution.ExecutionEngine.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.execution.ExecutionEngine.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.execution.ExecutionEngine.pprint")



* * *

### del_refs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L756-L759 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine.del_refs "Permanent link")

Whether to explicitly delete the result object references.

* * *

### get_ray_refs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L781-L852 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine.get_ray_refs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-30-1)RayEngine.get_ray_refs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-30-2)    tasks,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-30-3)    reuse_refs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-30-4)    remote_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-30-5))
    

Get result references by putting each argument and keyword argument into the object store and invoking the remote decorator on each function using Ray.

If `reuse_refs` is True, will generate one reference per unique object id.

* * *

### hide_inner_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L776-L779 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine.hide_inner_progress "Permanent link")

Whether to hide progress bars within each thread.

* * *

### init_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L766-L769 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine.init_kwargs "Permanent link")

Keyword arguments passed to `ray.init`.

* * *

### remote_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L771-L774 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine.remote_kwargs "Permanent link")

Keyword arguments passed to `ray.remote`.

* * *

### restart class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L745-L748 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine.restart "Permanent link")

Whether to terminate the Ray runtime and initialize a new one.

* * *

### reuse_refs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L750-L754 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine.reuse_refs "Permanent link")

Whether to re-use function and object references, such that each unique object will be copied only once.

* * *

### shutdown class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L761-L764 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine.shutdown "Permanent link")

Whether to True to terminate the Ray runtime upon the job end.

* * *

## SerialEngine class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L180-L295 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-31-1)SerialEngine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-31-2)    show_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-31-3)    pbar_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-31-4)    clear_cache=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-31-5)    collect_garbage=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-31-6)    delay=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-31-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-31-8))
    

Class for executing functions sequentially.

For defaults, see `engines.serial` in [execution](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "vectorbtpro._settings.execution").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.execution.ExecutionEngine.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.execution.ExecutionEngine.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.execution.ExecutionEngine.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.execution.ExecutionEngine.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.execution.ExecutionEngine.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.execution.ExecutionEngine.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.execution.ExecutionEngine.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.execution.ExecutionEngine.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.execution.ExecutionEngine.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.execution.ExecutionEngine.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.execution.ExecutionEngine.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.execution.ExecutionEngine.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.execution.ExecutionEngine.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.execution.ExecutionEngine.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.execution.ExecutionEngine.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.execution.ExecutionEngine.update_config")
  * [ExecutionEngine.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.execution.ExecutionEngine.config")
  * [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute")
  * [ExecutionEngine.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.execution.ExecutionEngine.rec_state")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.execution.ExecutionEngine.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.execution.ExecutionEngine.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.execution.ExecutionEngine.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.execution.ExecutionEngine.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.execution.ExecutionEngine.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.execution.ExecutionEngine.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.execution.ExecutionEngine.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.execution.ExecutionEngine.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.execution.ExecutionEngine.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.execution.ExecutionEngine.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.execution.ExecutionEngine.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.execution.ExecutionEngine.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.execution.ExecutionEngine.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.execution.ExecutionEngine.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.execution.ExecutionEngine.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.execution.ExecutionEngine.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.execution.ExecutionEngine.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.execution.ExecutionEngine.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.execution.ExecutionEngine.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.execution.ExecutionEngine.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.execution.ExecutionEngine.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.execution.ExecutionEngine.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.execution.ExecutionEngine.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.execution.ExecutionEngine.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.execution.ExecutionEngine.pprint")



* * *

### clear_cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L222-L227 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine.clear_cache "Permanent link")

Whether to clear vectorbt's cache after each iteration.

If integer, do it once a number of tasks.

* * *

### collect_garbage class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L229-L234 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine.collect_garbage "Permanent link")

Whether to clear garbage after each iteration.

If integer, do it once a number of tasks.

* * *

### delay class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L236-L239 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine.delay "Permanent link")

Number of seconds to sleep after each call.

* * *

### pbar_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L217-L220 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine.pbar_kwargs "Permanent link")

Keyword arguments passed to [ProgressBar](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar "vectorbtpro.utils.pbar.ProgressBar").

* * *

### show_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L212-L215 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine.show_progress "Permanent link")

Whether to show the progress bar.

* * *

## Task class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L70-L110 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Task "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-32-1)Task(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-32-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-32-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-32-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-32-5))
    

Class that represents an executable task.

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

### args field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Task.args "Permanent link")

Positional arguments.

* * *

### execute method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L105-L107 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Task.execute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-33-1)Task.execute()
    

Execute the task.

* * *

### from_tuple class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L83-L94 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Task.from_tuple "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-34-1)Task.from_tuple(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-34-2)    tuple_
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-34-3))
    

Build [Task](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Task "vectorbtpro.utils.execution.Task") instance from a tuple.

* * *

### func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Task.func "Permanent link")

Function.

* * *

### kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Task.kwargs "Permanent link")

Keyword arguments.

* * *

## ThreadPoolEngine class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L298-L358 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ThreadPoolEngine "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-35-1)ThreadPoolEngine(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-35-2)    init_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-35-3)    timeout=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-35-4)    hide_inner_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-35-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#__codelineno-35-6))
    

Class for executing functions using `ThreadPoolExecutor` from `concurrent.futures`.

For defaults, see `engines.threadpool` in [execution](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "vectorbtpro._settings.execution").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.execution.ExecutionEngine.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.execution.ExecutionEngine.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.execution.ExecutionEngine.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.execution.ExecutionEngine.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.execution.ExecutionEngine.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.execution.ExecutionEngine.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.execution.ExecutionEngine.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.execution.ExecutionEngine.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.execution.ExecutionEngine.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.execution.ExecutionEngine.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.execution.ExecutionEngine.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.execution.ExecutionEngine.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.execution.ExecutionEngine.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.execution.ExecutionEngine.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.execution.ExecutionEngine.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.execution.ExecutionEngine.update_config")
  * [ExecutionEngine.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.execution.ExecutionEngine.config")
  * [ExecutionEngine.execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine.execute "vectorbtpro.utils.execution.ExecutionEngine.execute")
  * [ExecutionEngine.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.execution.ExecutionEngine.rec_state")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.execution.ExecutionEngine.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.execution.ExecutionEngine.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.execution.ExecutionEngine.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.execution.ExecutionEngine.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.execution.ExecutionEngine.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.execution.ExecutionEngine.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.execution.ExecutionEngine.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.execution.ExecutionEngine.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.execution.ExecutionEngine.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.execution.ExecutionEngine.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.execution.ExecutionEngine.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.execution.ExecutionEngine.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.execution.ExecutionEngine.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.execution.ExecutionEngine.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.execution.ExecutionEngine.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.execution.ExecutionEngine.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.execution.ExecutionEngine.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.execution.ExecutionEngine.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.execution.ExecutionEngine.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.execution.ExecutionEngine.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.execution.ExecutionEngine.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.execution.ExecutionEngine.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.execution.ExecutionEngine.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.execution.ExecutionEngine.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.execution.ExecutionEngine.pprint")



* * *

### hide_inner_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L334-L337 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ThreadPoolEngine.hide_inner_progress "Permanent link")

Whether to hide progress bars within each thread.

* * *

### init_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L324-L327 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ThreadPoolEngine.init_kwargs "Permanent link")

Keyword arguments used to initialize `ThreadPoolExecutor`.

* * *

### timeout class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/execution.py#L329-L332 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ThreadPoolEngine.timeout "Permanent link")

Timeout.
