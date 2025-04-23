attr_

#  attr_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_ "Permanent link")

Utilities for working with class/instance attributes.

* * *

## MISSING literal[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.MISSING "Permanent link")

Sentinel that represents a missing value.

* * *

## deep_getattr function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L274-L339 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.deep_getattr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-0-1)deep_getattr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-0-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-0-3)    attr_chain,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-0-4)    getattr_func=<function default_getattr_func>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-0-5)    call_last_attr=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-0-6))
    

Retrieve attribute consecutively.

The attribute chain `attr_chain` can be:

  * string -> get variable/property or method without arguments
  * tuple of string -> call method without arguments
  * tuple of string and tuple -> call method and pass positional arguments (unpacked)
  * tuple of string, tuple, and dict -> call method and pass positional and keyword arguments (unpacked)
  * iterable of any of the above



Use `getattr_func` to overwrite the default behavior of accessing an attribute (see [default_getattr_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.default_getattr_func "vectorbtpro.utils.attr_.default_getattr_func")).

Hint

If your chain includes only attributes and functions without arguments, you can represent this chain as a single (but probably long) string.

* * *

## default_getattr_func function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L256-L271 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.default_getattr_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-1-1)default_getattr_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-1-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-1-3)    attr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-1-4)    args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-1-5)    kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-1-6)    call_attr=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-1-7))
    

Default `getattr_func`.

* * *

## get_dict_attr function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L244-L253 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.get_dict_attr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-2-1)get_dict_attr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-2-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-2-3)    attr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-2-4))
    

Get attribute without invoking the attribute lookup machinery.

* * *

## parse_attrs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L477-L544 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.parse_attrs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-3-1)parse_attrs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-3-2)    obj=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-3-3)    own_only=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-3-4)    sort_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-3-5))
    

Parse attributes of a class, object, or a module, and return a DataFrame with types and paths.

* * *

## AttrResolverMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L345-L474 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-4-1)AttrResolverMixin()
    

Class that implements resolution of self and its attributes.

Resolution is `getattr` that works for self, properties, and methods. It also utilizes built-in caching.

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

  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



* * *

### cls_dir cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "Permanent link")

Get set of attribute names.

* * *

### deep_getattr method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L472-L474 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-5-1)AttrResolverMixin.deep_getattr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-5-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-5-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-5-4))
    

See [deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.deep_getattr "vectorbtpro.utils.attr_.deep_getattr").

* * *

### post_resolve_attr method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L374-L378 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-6-1)AttrResolverMixin.post_resolve_attr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-6-2)    attr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-6-3)    out,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-6-4)    final_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-6-5))
    

Post-process an object after resolution.

Must return an object.

* * *

### pre_resolve_attr method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L368-L372 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-7-1)AttrResolverMixin.pre_resolve_attr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-7-2)    attr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-7-3)    final_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-7-4))
    

Pre-process an attribute before resolution.

Must return an attribute.

* * *

### resolve_attr method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L396-L470 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-1)AttrResolverMixin.resolve_attr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-2)    attr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-3)    args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-4)    cond_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-5)    kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-6)    custom_arg_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-7)    cache_dct=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-8)    use_caching=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-9)    passed_kwargs_out=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-10)    use_shortcuts=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-8-11))
    

Resolve an attribute using keyword arguments and built-in caching.

  * If there is a `get_{arg}` method, uses `get_{arg}` as `attr`.
  * If `attr` is a property, returns its value.
  * If `attr` is a method, passes `*args`, `**kwargs`, and `**cond_kwargs` with keys found in the signature.
  * If `use_shortcuts` is True, resolves the potential shortcuts using [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr").



Won't cache if `use_caching` is False or any passed argument is in `custom_arg_names`.

Use `passed_kwargs_out` to get keyword arguments that were passed.

* * *

### resolve_self method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L355-L366 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_self "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-9-1)AttrResolverMixin.resolve_self(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-9-2)    cond_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-9-3)    custom_arg_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-9-4)    impacts_caching=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-9-5)    silence_warnings=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-9-6))
    

Resolve self.

Note

`cond_kwargs` can be modified in-place.

* * *

### resolve_shortcut_attr method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L385-L394 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-10-1)AttrResolverMixin.resolve_shortcut_attr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-10-2)    attr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-10-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-10-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-10-5))
    

Resolve an attribute that may have shortcut properties.

* * *

### self_aliases class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L350-L353 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "Permanent link")

Names to associate with this object.

* * *

## DefineMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L56-L193 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-11-1)DefineMixin(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-11-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-11-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-11-4))
    

Mixin class for [define](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.define "vectorbtpro.utils.attr_.define").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.hashing.Hashable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.hashing.Hashable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.hashing.Hashable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.hashing.Hashable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.hashing.Hashable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.hashing.Hashable.find_messages")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.hashing.Hashable.get_hash")
  * [Hashable.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.hashing.Hashable.hash")
  * [Hashable.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.hashing.Hashable.hash_key")



**Subclasses**

  * [ArgGetter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "vectorbtpro.utils.chunking.ArgGetter")
  * [ArgSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer "vectorbtpro.utils.chunking.ArgSizer")
  * [AutoIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr "vectorbtpro.base.indexing.AutoIdxr")
  * [AxisSpecifier](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier "vectorbtpro.utils.chunking.AxisSpecifier")
  * [BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO "vectorbtpro.base.reshaping.BCO")
  * [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup")
  * [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup")
  * [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup")
  * [CAQuery](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery "vectorbtpro.registries.ca_registry.CAQuery")
  * [CARule](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule "vectorbtpro.registries.ca_registry.CARule")
  * [CARunResult](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult "vectorbtpro.registries.ca_registry.CARunResult")
  * [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup")
  * [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup")
  * [ChunkMapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper "vectorbtpro.utils.chunking.ChunkMapper")
  * [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta")
  * [ChunkSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSelector "vectorbtpro.utils.chunking.ChunkSelector")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [Chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked "vectorbtpro.utils.chunking.Chunked")
  * [ChunkedArray](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedArray "vectorbtpro.utils.chunking.ChunkedArray")
  * [ChunkedSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkedSetup "vectorbtpro.registries.ch_registry.ChunkedSetup")
  * [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr "vectorbtpro.base.indexing.ColIdxr")
  * [ContainerTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker "vectorbtpro.utils.chunking.ContainerTaker")
  * [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * [DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "vectorbtpro.utils.datetime_.DTC")
  * [DTCIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr "vectorbtpro.base.indexing.DTCIdxr")
  * [DatetimeIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr "vectorbtpro.base.indexing.DatetimeIdxr")
  * [Default](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Default "vectorbtpro.base.reshaping.Default")
  * [DimRetainer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer "vectorbtpro.utils.chunking.DimRetainer")
  * [EmbeddedDocument](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.EmbeddedDocument "vectorbtpro.utils.knowledge.chatting.EmbeddedDocument")
  * [ExceptLevel](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.ExceptLevel "vectorbtpro.base.indexes.ExceptLevel")
  * [FixRange](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.FixRange "vectorbtpro.generic.splitting.base.FixRange")
  * [FlexArraySelector](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.FlexArraySelector "vectorbtpro.base.chunking.FlexArraySelector")
  * [FlexArraySlicer](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.FlexArraySlicer "vectorbtpro.base.chunking.FlexArraySlicer")
  * [GroupIdxsMapper](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupIdxsMapper "vectorbtpro.base.chunking.GroupIdxsMapper")
  * [GroupLensMapper](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupLensMapper "vectorbtpro.base.chunking.GroupLensMapper")
  * [IdxDict](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxDict "vectorbtpro.base.indexing.IdxDict")
  * [IdxFrame](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxFrame "vectorbtpro.base.indexing.IdxFrame")
  * [IdxRecords](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxRecords "vectorbtpro.base.indexing.IdxRecords")
  * [IdxSeries](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSeries "vectorbtpro.base.indexing.IdxSeries")
  * [IdxSetter](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter "vectorbtpro.base.indexing.IdxSetter")
  * [Idxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr "vectorbtpro.base.indexing.Idxr")
  * [JitableSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup "vectorbtpro.registries.jit_registry.JitableSetup")
  * [JittedSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JittedSetup "vectorbtpro.registries.jit_registry.JittedSetup")
  * [LabelIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr "vectorbtpro.base.indexing.LabelIdxr")
  * [LabelSel](https://vectorbt.pro/pvt_7a467f6b/api/utils/selection/#vectorbtpro.utils.selection.LabelSel "vectorbtpro.utils.selection.LabelSel")
  * [MaskIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.MaskIdxr "vectorbtpro.base.indexing.MaskIdxr")
  * [MergeFunc](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc "vectorbtpro.utils.merging.MergeFunc")
  * [Not](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.Not "vectorbtpro.utils.search_.Not")
  * [NotChunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.NotChunked "vectorbtpro.utils.chunking.NotChunked")
  * [PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC "vectorbtpro.generic.ranges.PSC")
  * [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param")
  * [PointIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PointIdxr "vectorbtpro.base.indexing.PointIdxr")
  * [PosIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PosIdxr "vectorbtpro.base.indexing.PosIdxr")
  * [PosSel](https://vectorbt.pro/pvt_7a467f6b/api/utils/selection/#vectorbtpro.utils.selection.PosSel "vectorbtpro.utils.selection.PosSel")
  * [RangeIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RangeIdxr "vectorbtpro.base.indexing.RangeIdxr")
  * [RecInfo](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo "vectorbtpro.utils.pickling.RecInfo")
  * [RecState](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState "vectorbtpro.utils.pickling.RecState")
  * [Ref](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Ref "vectorbtpro.base.reshaping.Ref")
  * [Regex](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.Regex "vectorbtpro.utils.parsing.Regex")
  * [RelRange](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.RelRange "vectorbtpro.generic.splitting.base.RelRange")
  * [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr "vectorbtpro.base.indexing.RowIdxr")
  * [ScoredDocument](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.ScoredDocument "vectorbtpro.utils.knowledge.chatting.ScoredDocument")
  * [ShapeSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSelector "vectorbtpro.utils.chunking.ShapeSelector")
  * [ShapeSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSizer "vectorbtpro.utils.chunking.ShapeSizer")
  * [ShapeSlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSlicer "vectorbtpro.utils.chunking.ShapeSlicer")
  * [StoreDocument](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.StoreDocument "vectorbtpro.utils.knowledge.chatting.StoreDocument")
  * [StoreEmbedding](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.StoreEmbedding "vectorbtpro.utils.knowledge.chatting.StoreEmbedding")
  * [StoreObject](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.StoreObject "vectorbtpro.utils.knowledge.chatting.StoreObject")
  * [Takeable](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Takeable "vectorbtpro.generic.splitting.base.Takeable")
  * [Task](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.Task "vectorbtpro.utils.execution.Task")
  * [TextDocument](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/chatting/#vectorbtpro.utils.knowledge.chatting.TextDocument "vectorbtpro.utils.knowledge.chatting.TextDocument")
  * [UniIdxrOp](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.UniIdxrOp "vectorbtpro.base.indexing.UniIdxrOp")
  * [Union](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Union "vectorbtpro.utils.annotations.Union")
  * [VarArgs](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.VarArgs "vectorbtpro.utils.annotations.VarArgs")
  * [VarKwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.VarKwargs "vectorbtpro.utils.annotations.VarKwargs")
  * [hslice](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.hslice "vectorbtpro.base.indexing.hslice")



* * *

### asdict method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L155-L165 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-12-1)DefineMixin.asdict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-12-2)    full=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-12-3))
    

Convert this instance to a dictionary.

If `full` is False, won't include fields with [MISSING](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.MISSING "vectorbtpro.utils.attr_.MISSING") as value.

* * *

### assert_field_not_missing method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L129-L141 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-13-1)DefineMixin.assert_field_not_missing(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-13-2)    field_or_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-13-3))
    

Raise an error if a field is missing.

* * *

### fields hybrid_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L88-L91 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "Permanent link")

Get a tuple of fields.

* * *

### fields_dict hybrid_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L88-L91 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "Permanent link")

Get a dict of fields.

* * *

### get_field class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L88-L91 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-14-1)DefineMixin.get_field(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-14-2)    field_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-14-3))
    

Get field.

* * *

### is_field_missing method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L125-L127 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-15-1)DefineMixin.is_field_missing(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-15-2)    field_or_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-15-3))
    

Raise an error if a field is missing.

* * *

### is_field_optional class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L102-L109 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-16-1)DefineMixin.is_field_optional(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-16-2)    field_or_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-16-3))
    

Return whether a field is optional.

* * *

### is_field_required class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L93-L100 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-17-1)DefineMixin.is_field_required(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-17-2)    field_or_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-17-3))
    

Return whether a field is required.

* * *

### merge_over method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L177-L181 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-18-1)DefineMixin.merge_over(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-18-2)    other,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-18-3)    **changes
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-18-4))
    

Merge this instance over another instance.

* * *

### merge_with method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L171-L175 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-19-1)DefineMixin.merge_with(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-19-2)    other,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-19-3)    **changes
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-19-4))
    

Merge this instance with another instance.

* * *

### replace method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L167-L169 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-20-1)DefineMixin.replace(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-20-2)    **changes
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-20-3))
    

Create a new instance by making changes to the attribute values.

* * *

### resolve method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L143-L153 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-21-1)DefineMixin.resolve(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-21-2)    assert_not_missing=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-21-3))
    

Resolve a field or all fields.

* * *

### resolve_field method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L111-L123 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-22-1)DefineMixin.resolve_field(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-22-2)    field_or_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-22-3))
    

Resolve a field.

* * *

## define class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L196-L241 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.define "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-23-1)define(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-23-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-23-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-23-4))
    

Prepare a class decorated with [define](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.define "vectorbtpro.utils.attr_.define").

Attaches [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin") as a base class (if not present) and applies `attr.define`.

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

### field class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L201-L204 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.define.field "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-24-1)define.field(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-24-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-24-3))
    

Alias for `attr.field`.

* * *

### optional_field class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L213-L229 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.define.optional_field "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-25-1)define.optional_field(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-25-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-25-3)    default=_Missing.MISSING,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-25-4)    metadata=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-25-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-25-6))
    

Alias for `attr.field` with [MISSING](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.MISSING "vectorbtpro.utils.attr_.MISSING") as default.

Has `default` in metadata.

* * *

### required_field class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/attr_.py#L206-L211 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.define.required_field "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-26-1)define.required_field(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-26-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#__codelineno-26-3))
    

Alias for `attr.field` with [MISSING](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.MISSING "vectorbtpro.utils.attr_.MISSING") as default.

Doesn't have `default` in metadata.
