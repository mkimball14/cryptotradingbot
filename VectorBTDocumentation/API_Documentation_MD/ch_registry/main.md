ch_registry chunking

#  ch_registry module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry "Permanent link")

Global registry for chunkables.

* * *

## ch_reg ChunkableRegistry[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ch_reg "Permanent link")

Default registry of type [ChunkableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry "vectorbtpro.registries.ch_registry.ChunkableRegistry").

* * *

## register_chunkable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L167-L218 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.register_chunkable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-0-1)register_chunkable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-0-2)    func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-0-3)    setup_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-0-4)    registry=<vectorbtpro.registries.ch_registry.ChunkableRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-0-5)    tags=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-0-6)    return_wrapped=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-0-7)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-0-8))
    

Register a new chunkable function.

If `return_wrapped` is True, wraps with the [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked") decorator. Otherwise, leaves the function as-is (preferred).

Options are merged in the following order:

  * `options` in [chunking](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.chunking "vectorbtpro._settings.chunking")
  * `setup_options.{setup_id}` in [chunking](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.chunking "vectorbtpro._settings.chunking")
  * `options`
  * `override_options` in [chunking](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.chunking "vectorbtpro._settings.chunking")
  * `override_setup_options.{setup_id}` in [chunking](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.chunking "vectorbtpro._settings.chunking")



Note

Calling the [register_chunkable](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.register_chunkable "vectorbtpro.registries.ch_registry.register_chunkable") decorator before (or below) the [register_jitted](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.register_jitted "vectorbtpro.registries.jit_registry.register_jitted") decorator with `return_wrapped` set to True won't work. Doing the same after (or above) [register_jitted](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.register_jitted "vectorbtpro.registries.jit_registry.register_jitted") will work for calling the function from Python but not from Numba. Generally, avoid wrapping right away and use [ChunkableRegistry.decorate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.decorate "vectorbtpro.registries.ch_registry.ChunkableRegistry.decorate") to perform decoration.

* * *

## ChunkableRegistry class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L56-L160 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-1-1)ChunkableRegistry()
    

Class for registering chunkable functions.

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

### decorate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L113-L136 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.decorate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-2-1)ChunkableRegistry.decorate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-2-2)    setup_id_or_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-2-3)    target_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-2-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-2-5))
    

Decorate the setup's function using the [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked") decorator.

Finds setup using [ChunkableRegistry.get_setup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.get_setup "vectorbtpro.registries.ch_registry.ChunkableRegistry.get_setup").

Merges setup's options with `options`.

Specify `target_func` to apply the found setup on another function.

* * *

### get_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L94-L111 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.get_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-3-1)ChunkableRegistry.get_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-3-2)    setup_id_or_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-3-3))
    

Get setup by its id or function.

`setup_id_or_func` can be an identifier or a function. If it's a function, will build the identifier using its module and name.

* * *

### match_setups method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L80-L92 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.match_setups "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-4-1)ChunkableRegistry.match_setups(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-4-2)    expression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-4-3)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-4-4))
    

Match setups against an expression with each setup being a context.

* * *

### register method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L67-L78 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.register "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-5-1)ChunkableRegistry.register(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-5-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-5-3)    setup_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-5-4)    options=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-5-5)    tags=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-5-6))
    

Register a new setup.

* * *

### resolve_option method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L138-L160 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.resolve_option "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-6-1)ChunkableRegistry.resolve_option(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-6-2)    setup_id_or_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-6-3)    option,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-6-4)    target_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-6-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-6-6))
    

Same as [ChunkableRegistry.decorate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.decorate "vectorbtpro.registries.ch_registry.ChunkableRegistry.decorate") but using [resolve_chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.resolve_chunked "vectorbtpro.utils.chunking.resolve_chunked").

* * *

### setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L62-L65 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry.setups "Permanent link")

Dict of registered [ChunkedSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkedSetup "vectorbtpro.registries.ch_registry.ChunkedSetup") instances by [ChunkedSetup.setup_id](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkedSetup.setup_id "vectorbtpro.registries.ch_registry.ChunkedSetup.setup_id").

* * *

## ChunkedSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py#L28-L53 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkedSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-7-1)ChunkedSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-7-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-7-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#__codelineno-7-4))
    

Class that represents a chunkable setup.

Note

Hashed solely by `setup_id`.

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

### func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkedSetup.func "Permanent link")

Chunkable function.

* * *

### options field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkedSetup.options "Permanent link")

Options dictionary.

* * *

### setup_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkedSetup.setup_id "Permanent link")

Setup id.

* * *

### tags field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ch_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkedSetup.tags "Permanent link")

Set of tags.
