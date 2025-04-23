jitting

#  jitting module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting "Permanent link")

Utilities for jitting.

* * *

## get_func_suffix function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L151-L163 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.get_func_suffix "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-0-1)get_func_suffix(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-0-2)    py_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-0-3))
    

Get the suffix of the function.

* * *

## get_id_of_jitter_type function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L213-L229 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.get_id_of_jitter_type "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-1-1)get_id_of_jitter_type(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-1-2)    jitter_type
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-1-3))
    

Get id of a jitter type using `jitters` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting").

* * *

## jitted function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L306-L340 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.jitted "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-2-1)jitted(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-2-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-2-3)    tags=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-2-4)    **jitted_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-2-5))
    

Decorate a jitable function.

Resolves `jitter` using [resolve_jitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitter "vectorbtpro.utils.jitting.resolve_jitter").

The wrapping mechanism can be disabled by using the global setting `disable_wrapping` (=> returns the wrapped function).

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-3)>>> @vbt.jitted
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-4)... def my_func_nb():
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-5)...     total = 0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-6)...     for i in range(1000000):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-7)...         total += 1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-8)...     return total
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-10)>>> %timeit my_func_nb()
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-3-11)68.1 ns ± 0.32 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
    

Jitter is automatically detected using the suffix of the wrapped function.

* * *

## resolve_jitted_kwargs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L270-L288 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitted_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-4-1)resolve_jitted_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-4-2)    option=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-4-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-4-4))
    

Resolve keyword arguments for [jitted](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.jitted "vectorbtpro.utils.jitting.jitted").

Resolves `option` using [resolve_jitted_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitted_option "vectorbtpro.utils.jitting.resolve_jitted_option").

Note

Keys in `option` have more priority than in `kwargs`.

* * *

## resolve_jitted_option function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L232-L258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitted_option "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-5-1)resolve_jitted_option(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-5-2)    option=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-5-3))
    

Return keyword arguments for [jitted](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.jitted "vectorbtpro.utils.jitting.jitted").

`option` can be:

  * True: Decorate using default settings
  * False: Do not decorate (returns None)
  * string: Use `option` as the name of the jitter
  * dict: Use `option` as keyword arguments for jitting



For defaults, see `option` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting").

* * *

## resolve_jitter function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L291-L303 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-6-1)resolve_jitter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-6-2)    jitter=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-6-3)    py_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-6-4)    **jitter_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-6-5))
    

Resolve jitter.

Note

If `jitter` is already an instance of [Jitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter "vectorbtpro.utils.jitting.Jitter") and there are other keyword arguments, discards them.

* * *

## resolve_jitter_type function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L166-L210 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitter_type "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-7-1)resolve_jitter_type(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-7-2)    jitter=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-7-3)    py_func=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-7-4))
    

Resolve `jitter`.

  * If `jitter` is None and `py_func` is not None, uses [get_func_suffix](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.get_func_suffix "vectorbtpro.utils.jitting.get_func_suffix")
  * If `jitter` is a string, looks in `jitters` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting")
  * If `jitter` is a subclass of [Jitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter "vectorbtpro.utils.jitting.Jitter"), returns it
  * If `jitter` is an instance of [Jitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter "vectorbtpro.utils.jitting.Jitter"), returns its class
  * Otherwise, throws an error



* * *

## specialize_jitted_option function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L261-L267 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.specialize_jitted_option "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-8-1)specialize_jitted_option(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-8-2)    option=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-8-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-8-4))
    

Resolve `option` and merge it with `kwargs` if it's not None so the dict can be passed as an option to other functions.

* * *

## Jitter class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L23-L46 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-9-1)Jitter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-9-2)    **config
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-9-3))
    

Abstract class for decorating jitable functions.

Represents a single configuration for jitting.

When overriding [Jitter.decorate](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter.decorate "vectorbtpro.utils.jitting.Jitter.decorate"), make sure to check whether wrapping is disabled globally using [Jitter.wrapping_disabled](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter.wrapping_disabled "vectorbtpro.utils.jitting.Jitter.wrapping_disabled").

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

  * [NumPyJitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumPyJitter "vectorbtpro.utils.jitting.NumPyJitter")
  * [NumbaJitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter "vectorbtpro.utils.jitting.NumbaJitter")



* * *

### decorate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L42-L46 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter.decorate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-10-1)Jitter.decorate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-10-2)    py_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-10-3)    tags=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-10-4))
    

Decorate a jitable function.

* * *

### wrapping_disabled class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L33-L40 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter.wrapping_disabled "Permanent link")

Whether wrapping is disabled globally.

* * *

## NumPyJitter class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L49-L55 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumPyJitter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-11-1)NumPyJitter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-11-2)    **config
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-11-3))
    

Class for decorating functions that use NumPy.

Returns the function without decorating.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Jitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter "vectorbtpro.utils.jitting.Jitter")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.jitting.Jitter.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.jitting.Jitter.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.jitting.Jitter.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.jitting.Jitter.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.jitting.Jitter.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.jitting.Jitter.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.jitting.Jitter.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.jitting.Jitter.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.jitting.Jitter.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.jitting.Jitter.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.jitting.Jitter.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.jitting.Jitter.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.jitting.Jitter.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.jitting.Jitter.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.jitting.Jitter.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.jitting.Jitter.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.jitting.Jitter.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.jitting.Jitter.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.jitting.Jitter.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.jitting.Jitter.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.jitting.Jitter.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.jitting.Jitter.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.jitting.Jitter.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.jitting.Jitter.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.jitting.Jitter.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.jitting.Jitter.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.jitting.Jitter.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.jitting.Jitter.set_settings")
  * [Jitter.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.jitting.Jitter.config")
  * [Jitter.decorate](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter.decorate "vectorbtpro.utils.jitting.Jitter.decorate")
  * [Jitter.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.jitting.Jitter.rec_state")
  * [Jitter.wrapping_disabled](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter.wrapping_disabled "vectorbtpro.utils.jitting.Jitter.wrapping_disabled")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.jitting.Jitter.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.jitting.Jitter.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.jitting.Jitter.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.jitting.Jitter.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.jitting.Jitter.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.jitting.Jitter.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.jitting.Jitter.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.jitting.Jitter.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.jitting.Jitter.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.jitting.Jitter.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.jitting.Jitter.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.jitting.Jitter.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.jitting.Jitter.pprint")



* * *

## NumbaJitter class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L58-L148 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-1)NumbaJitter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-2)    fix_cannot_parallel=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-3)    nopython=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-4)    nogil=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-5)    parallel=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-6)    cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-7)    boundscheck=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-8)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#__codelineno-12-9))
    

Class for decorating functions using Numba.

Note

If `fix_cannot_parallel` is True, `parallel=True` will be ignored if there is no `can_parallel` tag.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Jitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter "vectorbtpro.utils.jitting.Jitter")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.jitting.Jitter.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.jitting.Jitter.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.jitting.Jitter.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.jitting.Jitter.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.jitting.Jitter.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.jitting.Jitter.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.jitting.Jitter.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.jitting.Jitter.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.jitting.Jitter.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.jitting.Jitter.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.jitting.Jitter.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.jitting.Jitter.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.jitting.Jitter.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.jitting.Jitter.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.jitting.Jitter.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.jitting.Jitter.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.jitting.Jitter.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.jitting.Jitter.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.jitting.Jitter.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.jitting.Jitter.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.jitting.Jitter.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.jitting.Jitter.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.jitting.Jitter.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.jitting.Jitter.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.jitting.Jitter.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.jitting.Jitter.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.jitting.Jitter.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.jitting.Jitter.set_settings")
  * [Jitter.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.jitting.Jitter.config")
  * [Jitter.decorate](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter.decorate "vectorbtpro.utils.jitting.Jitter.decorate")
  * [Jitter.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.jitting.Jitter.rec_state")
  * [Jitter.wrapping_disabled](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter.wrapping_disabled "vectorbtpro.utils.jitting.Jitter.wrapping_disabled")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.jitting.Jitter.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.jitting.Jitter.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.jitting.Jitter.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.jitting.Jitter.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.jitting.Jitter.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.jitting.Jitter.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.jitting.Jitter.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.jitting.Jitter.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.jitting.Jitter.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.jitting.Jitter.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.jitting.Jitter.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.jitting.Jitter.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.jitting.Jitter.pprint")



* * *

### boundscheck class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L118-L121 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter.boundscheck "Permanent link")

Whether to enable bounds checking for array indices.

* * *

### cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L123-L126 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter.cache "Permanent link")

Whether to write the result of function compilation into a file-based cache.

* * *

### fix_cannot_parallel class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L93-L96 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter.fix_cannot_parallel "Permanent link")

Whether to set `parallel` to False if there is no 'can_parallel' tag.

* * *

### nogil class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L108-L111 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter.nogil "Permanent link")

Whether to release the GIL.

* * *

### nopython class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L103-L106 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter.nopython "Permanent link")

Whether to run in nopython mode.

* * *

### options class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L98-L101 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter.options "Permanent link")

Options passed to the Numba decorator.

* * *

### parallel class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/jitting.py#L113-L116 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter.parallel "Permanent link")

Whether to enable automatic parallelization.
