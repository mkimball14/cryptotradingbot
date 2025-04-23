config

#  config module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config "Permanent link")

Utilities for configuration.

* * *

## ext_settings_paths_config HybridConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.ext_settings_paths_config "Permanent link")

Config for (currently active) extensional settings paths.

Stores tuples of class names and their settings paths by unique ids.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-0-1)HybridConfig()
    

* * *

## spec_settings_paths_config HybridConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.spec_settings_paths_config "Permanent link")

Config for (currently active) specialized settings paths.

Stores settings path dictionaries by unique ids. In a path dictionary, each key is a path that points to one or more other paths. For instance, a relationship "knowledge" -> "pages" will also consider "pages" settings whenever "knowledge" settings are requested.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-1-1)HybridConfig()
    

* * *

## unsetkey literal[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.unsetkey "Permanent link")

When passed as a value, the corresponding key will be unset.

It can still be overridden by another dict.

* * *

## convert_to_dict function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L78-L100 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.convert_to_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-2-1)convert_to_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-2-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-2-3)    nested=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-2-4))
    

Convert any config to `dict`.

Set `nested` to True to convert all child dicts in recursive manner.

If a config is an instance of [AtomicConfig](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.AtomicConfig "vectorbtpro.utils.config.AtomicConfig"), will convert it to [atomic_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.atomic_dict "vectorbtpro.utils.config.atomic_dict").

* * *

## copy_dict function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L141-L174 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.copy_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-3-1)copy_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-3-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-3-3)    copy_mode='shallow',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-3-4)    nested=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-3-5))
    

Copy dict based on a copy mode.

The following modes are supported:

  * 'none': Does not copy
  * 'shallow': Copies keys only
  * 'hybrid': Copies keys and values using `copy.copy`
  * 'deep': Copies the whole thing using `copy.deepcopy`



Set `nested` to True to copy all child dicts in recursive manner.

* * *

## del_dict_item function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L131-L138 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.del_dict_item "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-4-1)del_dict_item(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-4-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-4-3)    k,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-4-4)    force=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-4-5))
    

Delete dict item.

If the dict is of the type [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config"), also passes `force` keyword to override blocking flags.

* * *

## flat_merge_dicts function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L428-L430 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.flat_merge_dicts "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-5-1)flat_merge_dicts(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-5-2)    *dicts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-5-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-5-4))
    

Merge dicts with default arguments and `nested=False`.

* * *

## get_dict_item function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L103-L118 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.get_dict_item "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-6-1)get_dict_item(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-6-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-6-3)    k,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-6-4)    populate=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-6-5))
    

Get dict item under the key `k`.

The key can be nested using the dot notation, `pathlib.Path`, or a tuple, and must be hashable.

* * *

## merge_dicts function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L337-L425 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.merge_dicts "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-7-1)merge_dicts(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-7-2)    *dicts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-7-3)    to_dict=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-7-4)    copy_mode='shallow',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-7-5)    nested=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-7-6)    same_keys=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-7-7))
    

Merge dicts.

**Args**

**`*dicts`** : `dict`
    Dicts.
**`to_dict`** : `bool`
    Whether to call [convert_to_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.convert_to_dict "vectorbtpro.utils.config.convert_to_dict") on each dict prior to copying.
**`copy_mode`** : `str`
    Mode for [copy_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.copy_dict "vectorbtpro.utils.config.copy_dict") to copy each dict prior to merging.
**`nested`** : `bool`
    

Whether to merge all child dicts in recursive manner.

If None, checks whether any dict is nested.

**`same_keys`** : `bool`
    Whether to merge on the overlapping keys only.

* * *

## reorder_dict function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L222-L252 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.reorder_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-8-1)reorder_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-8-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-8-3)    keys,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-8-4)    skip_missing=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-8-5))
    

Reorder a dict based on a list of keys.

The keys list can include all keys, or a subset of keys with a single Ellipsis (...) representing all other keys.

* * *

## reorder_list function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L255-L307 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.reorder_list "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-9-1)reorder_list(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-9-2)    lst,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-9-3)    keys,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-9-4)    skip_missing=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-9-5))
    

Reorder a list based on a list of integer indices.

The keys list can include all indices, or a subset of indices with a single Ellipsis (...) representing all other indices. When skip_missing is True, missing indices are ignored.

* * *

## resolve_dict function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L54-L65 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.resolve_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-10-1)resolve_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-10-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-10-3)    i=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-10-4))
    

Select keyword arguments.

* * *

## set_dict_item function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L121-L128 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.set_dict_item "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-11-1)set_dict_item(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-11-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-11-3)    k,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-11-4)    v,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-11-5)    force=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-11-6))
    

Set dict item.

If the dict is of the type [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config"), also passes `force` keyword to override blocking flags.

* * *

## unset_keys function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L320-L334 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.unset_keys "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-12-1)unset_keys(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-12-2)    dct,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-12-3)    nested=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-12-4)    force=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-12-5))
    

Unset the keys that have the value [unsetkey](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.unsetkey "vectorbtpro.utils.config.unsetkey").

* * *

## update_dict function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L177-L219 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.update_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-13-1)update_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-13-2)    x,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-13-3)    y,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-13-4)    nested=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-13-5)    force=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-13-6)    same_keys=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-13-7))
    

Update dict with keys and values from other dict.

Set `nested` to True to update all child dicts in recursive manner.

For `force`, see [set_dict_item](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.set_dict_item "vectorbtpro.utils.config.set_dict_item").

If you want to treat any dict as a single value, wrap it with [atomic_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.atomic_dict "vectorbtpro.utils.config.atomic_dict").

If `nested` is True, a value in `x` is an instance of [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured"), and the corresponding value in `y` is a dictionary, calls [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.config.Configured.replace").

Note

If the child dict is not atomic, it will copy only its values, not its meta.

* * *

## AtomicConfig class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L916-L919 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.AtomicConfig "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-14-1)AtomicConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-14-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-14-3)    options_=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-14-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-14-5))
    

Config that behaves like a single value when merging.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [atomic_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.atomic_dict "vectorbtpro.utils.config.atomic_dict")
  * `builtins.dict`
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Config.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Config.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Config.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Config.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Config.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Config.find_messages")
  * [Config.clear](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.clear "vectorbtpro.utils.config.Config.clear")
  * [Config.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.copy "vectorbtpro.utils.config.Config.copy")
  * [Config.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "vectorbtpro.utils.config.Config.equals")
  * [Config.get_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.get_option "vectorbtpro.utils.config.Config.get_option")
  * [Config.load_update](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "vectorbtpro.utils.config.Config.load_update")
  * [Config.make_checkpoint](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.make_checkpoint "vectorbtpro.utils.config.Config.make_checkpoint")
  * [Config.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.merge_with "vectorbtpro.utils.config.Config.merge_with")
  * [Config.options_](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.options_ "vectorbtpro.utils.config.Config.options_")
  * [Config.pop](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.pop "vectorbtpro.utils.config.Config.pop")
  * [Config.popitem](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.popitem "vectorbtpro.utils.config.Config.popitem")
  * [Config.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Config.prettify")
  * [Config.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Config.rec_state")
  * [Config.reset](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.reset "vectorbtpro.utils.config.Config.reset")
  * [Config.set_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.set_option "vectorbtpro.utils.config.Config.set_option")
  * [Config.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.to_dict "vectorbtpro.utils.config.Config.to_dict")
  * [Config.update](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.update "vectorbtpro.utils.config.Config.update")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Config.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Config.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Config.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Config.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Config.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Config.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Config.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Config.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Config.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Config.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Config.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Config.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Config.pprint")



* * *

## Config class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L442-L913 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-15-1)Config(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-15-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-15-3)    options_=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-15-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-15-5))
    

Extends pickleable dict with config features such as nested updates, freezing, and resetting.

**Args**

**`*args`**
    Arguments to construct the dict from.
**`options_`** : `dict`
    Config options (see below).
**`**kwargs`**
    Keyword arguments to construct the dict from.

Options can have the following keys:

**Attributes**

**`copy_kwargs`** : `dict`
    

Keyword arguments passed to [copy_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.copy_dict "vectorbtpro.utils.config.copy_dict") for copying main dict and `reset_dct`.

Copy mode defaults to 'none'.

**`reset_dct`** : `dict`
    

Dict to fall back to in case of resetting.

Defaults to None. If None, copies main dict using `reset_dct_copy_kwargs`.

Note

Defaults to main dict in case it's None and `readonly` is True.

**`reset_dct_copy_kwargs`** : `dict`
    

Keyword arguments that override `copy_kwargs` for `reset_dct`.

Copy mode defaults to 'none' if `readonly` is True, else to 'hybrid'.

**`pickle_reset_dct`** : `bool`
    Whether to pickle `reset_dct`.
**`frozen_keys`** : `bool`
    

Whether to deny updates to the keys of the config.

Defaults to False.

**`readonly`** : `bool`
    

Whether to deny updates to the keys and values of the config.

Defaults to False.

**`nested`** : `bool`
    

Whether to do operations recursively on each child dict.

Such operations include copy, update, and merge. Disable to treat each child dict as a single value. Defaults to True.

**`convert_children`** : `bool` or `type`
    

Whether to convert child dicts of type [child_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.child_dict "vectorbtpro.utils.config.child_dict") to configs with the same configuration.

This will trigger a waterfall reaction across all child dicts. Won't convert dicts that are already configs. Apart from boolean, you can set it to any subclass of [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config") to use it for construction. Requires `nested` to be True. Defaults to False.

**`as_attrs`** : `bool`
    

Whether to enable accessing dict keys via the dot notation.

Enables autocompletion (but only during runtime!). Raises error in case of naming conflicts. Defaults to True if `frozen_keys` or `readonly`, otherwise False.

To make nested dictionaries also accessible via the dot notation, wrap them with [child_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.child_dict "vectorbtpro.utils.config.child_dict") and set `convert_children` and `nested` to True.

**`override_keys`** : `set` of `str`
    Keys to override if `as_attrs` is True.

Defaults can be overridden with settings under [config](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.config "vectorbtpro._settings.config").

If another config is passed, its properties are copied over, but they can still be overridden with the arguments passed to the initializer.

Note

All arguments are applied only once during initialization.

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



**Subclasses**

  * [AtomicConfig](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.AtomicConfig "vectorbtpro.utils.config.AtomicConfig")
  * [FrozenConfig](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.FrozenConfig "vectorbtpro.utils.config.FrozenConfig")
  * [HybridConfig](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HybridConfig "vectorbtpro.utils.config.HybridConfig")
  * [ReadonlyConfig](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.ReadonlyConfig "vectorbtpro.utils.config.ReadonlyConfig")
  * [SettingsConfig](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig "vectorbtpro._settings.SettingsConfig")
  * [flex_cfg](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.flex_cfg "vectorbtpro._settings.flex_cfg")
  * [frozen_cfg](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.frozen_cfg "vectorbtpro._settings.frozen_cfg")



* * *

### clear method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L705-L711 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.clear "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-16-1)Config.clear(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-16-2)    force=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-16-3))
    

Remove all items.

* * *

### copy method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L751-L787 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.copy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-17-1)Config.copy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-17-2)    reset_dct_copy_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-17-3)    copy_mode=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-17-4)    nested=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-17-5))
    

Copy the instance.

By default, copies in the same way as during the initialization.

* * *

### get_option method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L629-L631 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.get_option "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-18-1)Config.get_option(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-18-2)    k
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-18-3))
    

Get an option.

* * *

### make_checkpoint method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L821-L829 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.make_checkpoint "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-19-1)Config.make_checkpoint(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-19-2)    force=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-19-3)    **reset_dct_copy_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-19-4))
    

Replace `reset_dct` by the current state.

`reset_dct_copy_kwargs` override `reset_dct_copy_kwargs`.

* * *

### merge_with method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L789-L803 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.merge_with "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-20-1)Config.merge_with(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-20-2)    other,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-20-3)    copy_mode=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-20-4)    nested=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-20-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-20-6))
    

Merge with another dict into one single dict.

See [merge_dicts](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.merge_dicts "vectorbtpro.utils.config.merge_dicts").

* * *

### options_ class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L624-L627 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.options_ "Permanent link")

Config options.

* * *

### pop method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L684-L694 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.pop "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-21-1)Config.pop(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-21-2)    k,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-21-3)    v=_Missing.MISSING,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-21-4)    force=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-21-5))
    

Remove and return the pair by the key.

* * *

### popitem method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L696-L703 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.popitem "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-22-1)Config.popitem(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-22-2)    force=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-22-3))
    

Remove and return some pair.

* * *

### reset method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L809-L819 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.reset "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-23-1)Config.reset(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-23-2)    force=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-23-3)    **reset_dct_copy_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-23-4))
    

Clears the config and updates it with the initial config.

`reset_dct_copy_kwargs` override `reset_dct_copy_kwargs`.

* * *

### set_option method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L633-L635 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.set_option "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-24-1)Config.set_option(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-24-2)    k,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-24-3)    v
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-24-4))
    

Set an option.

* * *

### to_dict method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L805-L807 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.to_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-25-1)Config.to_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-25-2)    nested=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-25-3))
    

Convert to dict.

* * *

### update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L713-L720 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-26-1)Config.update(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-26-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-26-3)    nested=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-26-4)    force=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-26-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-26-6))
    

Update the config.

See [update_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.update_dict "vectorbtpro.utils.config.update_dict").

* * *

## Configured class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1566-L1801 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-27-1)Configured(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-27-2)    **config
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-27-3))
    

Class with an initialization config.

All subclasses of [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured") are initialized using [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config"), which makes it easier to pickle.

Settings are defined under [configured](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.configured "vectorbtpro._settings.configured").

Warning

If any attribute has been overwritten that isn't listed in `Configured._writeable_attrs`, or if any [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured") argument depends upon global defaults, their values won't be copied over. Make sure to pass them explicitly to make that the saved & loaded / copied instance is resilient to any changes in globals.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.HasSettings.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.HasSettings.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.HasSettings.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.HasSettings.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.HasSettings.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.HasSettings.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.caching.Cacheable.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.chaining.Chainable.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.chaining.Chainable.pipe")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.config.HasSettings.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.config.HasSettings.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.config.HasSettings.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.config.HasSettings.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.config.HasSettings.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.config.HasSettings.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.config.HasSettings.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.config.HasSettings.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.config.HasSettings.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.config.HasSettings.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.config.HasSettings.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.config.HasSettings.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.pickling.Pickleable.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.pickling.Pickleable.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.pickling.Pickleable.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.pickling.Pickleable.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.pickling.Pickleable.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.pickling.Pickleable.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.pickling.Pickleable.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.pickling.Pickleable.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.pickling.Pickleable.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.pickling.Pickleable.modify_state")
  * [Pickleable.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.pickling.Pickleable.rec_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.pickling.Pickleable.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.pickling.Pickleable.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.formatting.Prettified.pprint")
  * [Prettified.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.formatting.Prettified.prettify")



**Subclasses**

  * [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper")
  * [AssetCacheManager](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.AssetCacheManager "vectorbtpro.utils.knowledge.base_assets.AssetCacheManager")
  * [BaseIDXAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor "vectorbtpro.base.accessors.BaseIDXAccessor")
  * [BasePreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer "vectorbtpro.base.preparing.BasePreparer")
  * [Chunker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker "vectorbtpro.utils.chunking.Chunker")
  * [Completions](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Completions "vectorbtpro.utils.knowledge.chatting.Completions")
  * [ContentFormatter](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/formatting/#vectorbtpro.utils.knowledge.formatting.ContentFormatter "vectorbtpro.utils.knowledge.formatting.ContentFormatter")
  * [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "vectorbtpro.data.updater.DataUpdater")
  * [DocumentRanker](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.DocumentRanker "vectorbtpro.utils.knowledge.chatting.DocumentRanker")
  * [Embeddings](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Embeddings "vectorbtpro.utils.knowledge.chatting.Embeddings")
  * [ExecutionEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ExecutionEngine "vectorbtpro.utils.execution.ExecutionEngine")
  * [Executor](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Executor "vectorbtpro.utils.execution.Executor")
  * [FormatHTML](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/formatting/#vectorbtpro.utils.knowledge.formatting.FormatHTML "vectorbtpro.utils.knowledge.formatting.FormatHTML")
  * [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/base/#vectorbtpro.base.grouping.base.Grouper "vectorbtpro.base.grouping.base.Grouper")
  * [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory "vectorbtpro.indicators.factory.IndicatorFactory")
  * [Jitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.Jitter "vectorbtpro.utils.jitting.Jitter")
  * [KnowledgeAsset](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset "vectorbtpro.utils.knowledge.base_assets.KnowledgeAsset")
  * [ObjectStore](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.ObjectStore "vectorbtpro.utils.knowledge.chatting.ObjectStore")
  * [PFPrepResult](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.PFPrepResult "vectorbtpro.portfolio.preparing.PFPrepResult")
  * [Parameterizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer "vectorbtpro.utils.params.Parameterizer")
  * [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter "vectorbtpro.returns.qs_adapter.QSAdapter")
  * [Resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler "vectorbtpro.base.resampling.base.Resampler")
  * [TVClient](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVClient "vectorbtpro.data.custom.tv.TVClient")
  * [TelegramBot](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.TelegramBot "vectorbtpro.utils.telegram.TelegramBot")
  * [TextSplitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.TextSplitter "vectorbtpro.utils.knowledge.chatting.TextSplitter")
  * [ToHTML](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/formatting/#vectorbtpro.utils.knowledge.formatting.ToHTML "vectorbtpro.utils.knowledge.formatting.ToHTML")
  * [ToMarkdown](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/formatting/#vectorbtpro.utils.knowledge.formatting.ToMarkdown "vectorbtpro.utils.knowledge.formatting.ToMarkdown")
  * [Tokenizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Tokenizer "vectorbtpro.utils.knowledge.chatting.Tokenizer")
  * [TraceType](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "vectorbtpro.generic.plotting.TraceType")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



* * *

### config class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1621-L1624 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "Permanent link")

Initialization config.

* * *

### copy method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1730-L1739 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-28-1)Configured.copy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-28-2)    copy_mode=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-28-3)    nested=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-28-4)    cls=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-28-5))
    

Create a new instance by copying the config.

See [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.config.Configured.replace").

* * *

### equals method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1741-L1783 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-29-1)Configured.equals(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-29-2)    other,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-29-3)    check_types=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-29-4)    check_attrs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-29-5)    check_options=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-29-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-29-7))
    

Check two objects for equality.

* * *

### get_writeable_attrs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1626-L1637 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-30-1)Configured.get_writeable_attrs()
    

Get set of attributes that are writeable by this class or by any of its base classes.

* * *

### replace method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1697-L1728 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-31-1)Configured.replace(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-31-2)    copy_mode_=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-31-3)    nested_=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-31-4)    cls_=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-31-5)    copy_writeable_attrs_=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-31-6)    **new_config
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-31-7))
    

Create a new instance by copying and (optionally) changing the config.

Warning

This operation won't return a copy of the instance but a new instance initialized with the same config and writeable attributes (or their copy, depending on `copy_mode`).

* * *

### resolve_merge_kwargs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1639-L1695 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-32-1)Configured.resolve_merge_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-32-2)    *configs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-32-3)    on_merge_conflict='error',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-32-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-32-5))
    

Resolve keyword arguments for initializing [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured") after merging.

* * *

### update_config method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1785-L1787 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-33-1)Configured.update_config(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-33-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-33-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-33-4))
    

Force-update the config.

* * *

## ExtSettingsPath class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1004-L1026 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.ExtSettingsPath "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-34-1)ExtSettingsPath(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-34-2)    ext_settings_paths
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-34-3))
    

Context manager to add extensional settings paths.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### ext_settings_paths class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1016-L1019 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.ExtSettingsPath.ext_settings_paths "Permanent link")

Dictionary with extensional settings paths.

* * *

### unique_id class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1011-L1014 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.ExtSettingsPath.unique_id "Permanent link")

Unique id.

* * *

## FrozenConfig class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L922-L934 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.FrozenConfig "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-35-1)FrozenConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-35-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-35-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-35-4))
    

[Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config") with `frozen_keys` flag set to True.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * `builtins.dict`
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Config.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Config.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Config.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Config.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Config.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Config.find_messages")
  * [Config.clear](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.clear "vectorbtpro.utils.config.Config.clear")
  * [Config.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.copy "vectorbtpro.utils.config.Config.copy")
  * [Config.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "vectorbtpro.utils.config.Config.equals")
  * [Config.get_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.get_option "vectorbtpro.utils.config.Config.get_option")
  * [Config.load_update](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "vectorbtpro.utils.config.Config.load_update")
  * [Config.make_checkpoint](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.make_checkpoint "vectorbtpro.utils.config.Config.make_checkpoint")
  * [Config.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.merge_with "vectorbtpro.utils.config.Config.merge_with")
  * [Config.options_](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.options_ "vectorbtpro.utils.config.Config.options_")
  * [Config.pop](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.pop "vectorbtpro.utils.config.Config.pop")
  * [Config.popitem](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.popitem "vectorbtpro.utils.config.Config.popitem")
  * [Config.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Config.prettify")
  * [Config.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Config.rec_state")
  * [Config.reset](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.reset "vectorbtpro.utils.config.Config.reset")
  * [Config.set_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.set_option "vectorbtpro.utils.config.Config.set_option")
  * [Config.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.to_dict "vectorbtpro.utils.config.Config.to_dict")
  * [Config.update](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.update "vectorbtpro.utils.config.Config.update")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Config.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Config.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Config.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Config.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Config.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Config.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Config.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Config.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Config.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Config.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Config.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Config.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Config.pprint")



* * *

## HasSettings class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1071-L1516 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-36-1)HasSettings()
    

Class that has settings in [vectorbtpro._settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/ "vectorbtpro._settings").

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

  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [Contextable](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Contextable "vectorbtpro.utils.knowledge.chatting.Contextable")
  * [Rankable](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.Rankable "vectorbtpro.utils.knowledge.chatting.Rankable")



* * *

### get_path_setting class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1260-L1300 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-37-1)HasSettings.get_path_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-37-2)    path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-37-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-37-4)    default=_Missing.MISSING,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-37-5)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-37-6)    sub_path_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-37-7))
    

Get a value from the settings under a path.

* * *

### get_path_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1087-L1113 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-38-1)HasSettings.get_path_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-38-2)    path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-38-3)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-38-4)    sub_path_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-38-5))
    

Get the settings under a path.

* * *

### get_setting class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1302-L1362 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-1)HasSettings.get_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-2)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-3)    default=_Missing.MISSING,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-4)    path_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-5)    inherit=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-6)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-7)    sub_path_only=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-8)    merge=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-39-9))
    

Get a value under the settings associated with this class and its superclasses (if `inherit` is True).

* * *

### get_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1190-L1223 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-40-1)HasSettings.get_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-40-2)    path_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-40-3)    inherit=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-40-4)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-40-5)    sub_path_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-40-6))
    

Get the settings associated with this class and its superclasses (if `inherit` is True).

* * *

### has_path_setting class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1364-L1377 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-41-1)HasSettings.has_path_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-41-2)    path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-41-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-41-4)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-41-5)    sub_path_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-41-6))
    

Return whether the setting under a path exists.

* * *

### has_path_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1225-L1237 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-42-1)HasSettings.has_path_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-42-2)    path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-42-3)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-42-4)    sub_path_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-42-5))
    

Return whether the settings under a path exist.

* * *

### has_setting class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1379-L1400 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-43-1)HasSettings.has_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-43-2)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-43-3)    path_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-43-4)    inherit=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-43-5)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-43-6)    sub_path_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-43-7))
    

Return whether the settings associated with this class and its superclasses (if `inherit` is True) exists.

* * *

### has_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1239-L1258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-44-1)HasSettings.has_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-44-2)    path_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-44-3)    inherit=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-44-4)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-44-5)    sub_path_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-44-6))
    

Return whether there the settings associated with this class and its superclasses (if `inherit` is True) exist.

* * *

### reset_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1488-L1516 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-45-1)HasSettings.reset_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-45-2)    path_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-45-3)    sub_path=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-45-4))
    

Reset the settings in [vectorbtpro._settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/ "vectorbtpro._settings") associated with this class.

* * *

### resolve_setting class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1402-L1445 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-1)HasSettings.resolve_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-2)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-4)    default=_Missing.MISSING,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-5)    path_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-6)    inherit=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-7)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-8)    sub_path_only=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-9)    merge=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-46-10))
    

Resolve a value that has a key under the settings in [vectorbtpro._settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/ "vectorbtpro._settings") associated with this class.

If the provided value is None, returns the setting, otherwise the value. If the value is a dict and `merge` is True, merges it over the corresponding dict in the settings.

If `sub_path` is provided, appends it to the resolved path and gives it more priority. If only the `sub_path` should be considered, set `sub_path_only` to True.

* * *

### resolve_settings_paths class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1115-L1188 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-47-1)HasSettings.resolve_settings_paths(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-47-2)    path_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-47-3)    inherit=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-47-4)    super_first=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-47-5)    unique_only=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-47-6))
    

Resolve the settings paths associated with this class and its superclasses (if `inherit` is True).

* * *

### set_settings class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1447-L1486 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-48-1)HasSettings.set_settings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-48-2)    path_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-48-3)    sub_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-48-4)    populate_=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-48-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-48-6))
    

Set the settings in [vectorbtpro._settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/ "vectorbtpro._settings") associated with this class.

If the settings do not exist yet, pass `populate_=True`.

* * *

## HybridConfig class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L952-L968 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HybridConfig "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-49-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-49-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-49-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-49-4))
    

[Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config") with `copy_kwargs` set to `copy_mode='hybrid'`.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * `builtins.dict`
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Config.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Config.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Config.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Config.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Config.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Config.find_messages")
  * [Config.clear](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.clear "vectorbtpro.utils.config.Config.clear")
  * [Config.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.copy "vectorbtpro.utils.config.Config.copy")
  * [Config.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "vectorbtpro.utils.config.Config.equals")
  * [Config.get_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.get_option "vectorbtpro.utils.config.Config.get_option")
  * [Config.load_update](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "vectorbtpro.utils.config.Config.load_update")
  * [Config.make_checkpoint](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.make_checkpoint "vectorbtpro.utils.config.Config.make_checkpoint")
  * [Config.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.merge_with "vectorbtpro.utils.config.Config.merge_with")
  * [Config.options_](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.options_ "vectorbtpro.utils.config.Config.options_")
  * [Config.pop](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.pop "vectorbtpro.utils.config.Config.pop")
  * [Config.popitem](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.popitem "vectorbtpro.utils.config.Config.popitem")
  * [Config.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Config.prettify")
  * [Config.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Config.rec_state")
  * [Config.reset](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.reset "vectorbtpro.utils.config.Config.reset")
  * [Config.set_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.set_option "vectorbtpro.utils.config.Config.set_option")
  * [Config.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.to_dict "vectorbtpro.utils.config.Config.to_dict")
  * [Config.update](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.update "vectorbtpro.utils.config.Config.update")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Config.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Config.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Config.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Config.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Config.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Config.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Config.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Config.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Config.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Config.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Config.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Config.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Config.pprint")



* * *

## MetaConfigured class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1519-L1563 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.MetaConfigured "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-50-1)MetaConfigured(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-50-2)    name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-50-3)    bases,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-50-4)    attrs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-50-5))
    

Metaclass for [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured").

**Superclasses**

  * `builtins.type`



**Subclasses**

  * [MetaAnalyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.MetaAnalyzable "vectorbtpro.generic.analyzable.MetaAnalyzable")
  * [MetaBasePreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.MetaBasePreparer "vectorbtpro.base.preparing.MetaBasePreparer")
  * [MetaKnowledgeAsset](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_assets/#vectorbtpro.utils.knowledge.base_assets.MetaKnowledgeAsset "vectorbtpro.utils.knowledge.base_assets.MetaKnowledgeAsset")
  * [MetaObjectStore](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.MetaObjectStore "vectorbtpro.utils.knowledge.chatting.MetaObjectStore")



* * *

## ReadonlyConfig class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L937-L949 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.ReadonlyConfig "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-51-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-51-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-51-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-51-4))
    

[Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config") with `readonly` flag set to True.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * `builtins.dict`
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Config.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Config.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Config.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Config.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Config.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Config.find_messages")
  * [Config.clear](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.clear "vectorbtpro.utils.config.Config.clear")
  * [Config.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.copy "vectorbtpro.utils.config.Config.copy")
  * [Config.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "vectorbtpro.utils.config.Config.equals")
  * [Config.get_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.get_option "vectorbtpro.utils.config.Config.get_option")
  * [Config.load_update](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "vectorbtpro.utils.config.Config.load_update")
  * [Config.make_checkpoint](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.make_checkpoint "vectorbtpro.utils.config.Config.make_checkpoint")
  * [Config.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.merge_with "vectorbtpro.utils.config.Config.merge_with")
  * [Config.options_](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.options_ "vectorbtpro.utils.config.Config.options_")
  * [Config.pop](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.pop "vectorbtpro.utils.config.Config.pop")
  * [Config.popitem](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.popitem "vectorbtpro.utils.config.Config.popitem")
  * [Config.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Config.prettify")
  * [Config.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Config.rec_state")
  * [Config.reset](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.reset "vectorbtpro.utils.config.Config.reset")
  * [Config.set_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.set_option "vectorbtpro.utils.config.Config.set_option")
  * [Config.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.to_dict "vectorbtpro.utils.config.Config.to_dict")
  * [Config.update](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.update "vectorbtpro.utils.config.Config.update")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Config.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Config.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Config.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Config.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Config.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Config.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Config.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Config.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Config.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Config.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Config.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Config.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Config.pprint")



* * *

## SettingNotFoundError class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L980-L983 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.SettingNotFoundError "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-52-1)SettingNotFoundError(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-52-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-52-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-52-4))
    

Gets raised if a setting could not be found.

**Superclasses**

  * `builtins.BaseException`
  * `builtins.Exception`
  * `builtins.KeyError`
  * `builtins.LookupError`



* * *

## SettingsNotFoundError class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L974-L977 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.SettingsNotFoundError "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-53-1)SettingsNotFoundError(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-53-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-53-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-53-4))
    

Gets raised if settings could not be found.

**Superclasses**

  * `builtins.BaseException`
  * `builtins.Exception`
  * `builtins.KeyError`
  * `builtins.LookupError`



* * *

## SpecSettingsPath class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1046-L1068 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.SpecSettingsPath "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-54-1)SpecSettingsPath(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-54-2)    spec_settings_paths
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-54-3))
    

Context manager to add specialized settings paths.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### spec_settings_paths class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1058-L1061 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.SpecSettingsPath.spec_settings_paths "Permanent link")

Dictionary with specialized settings paths.

* * *

### unique_id class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L1053-L1056 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.SpecSettingsPath.unique_id "Permanent link")

Unique id.

* * *

## atomic_dict class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L68-L71 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.atomic_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-55-1)atomic_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-55-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-55-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-55-4))
    

Dict that behaves like a single value when merging.

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



**Subclasses**

  * [AtomicConfig](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.AtomicConfig "vectorbtpro.utils.config.AtomicConfig")



* * *

## child_dict class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L433-L436 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.child_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-56-1)child_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-56-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-56-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-56-4))
    

Subclass of `dict` acting as a child dict.

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

## hdict class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/config.py#L47-L51 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.hdict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-57-1)hdict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-57-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-57-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#__codelineno-57-4))
    

Hashable dict.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `builtins.dict`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")


