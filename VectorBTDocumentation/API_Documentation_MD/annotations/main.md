annotations

#  annotations module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations "Permanent link")

Utilities for annotations.

* * *

## flatten_annotations function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L120-L151 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.flatten_annotations "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-0-1)flatten_annotations(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-0-2)    annotations,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-0-3)    only_var_args=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-0-4)    return_var_arg_maps=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-0-5))
    

Flatten annotations of variable arguments.

* * *

## get_annotations function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L109-L117 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.get_annotations "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-1-1)get_annotations(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-1-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-1-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-1-4))
    

Get annotations.

* * *

## has_annotatables function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L174-L182 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.has_annotatables "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-2-1)has_annotatables(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-2-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-2-3)    target_cls=vectorbtpro.utils.annotations.Annotatable
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-2-4))
    

Check if a function has subclasses or instances of [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable") in its signature.

* * *

## Annotatable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L164-L171 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-3-1)Annotatable()
    

Class that can be used in annotations.

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

  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [Chunkable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable "vectorbtpro.utils.chunking.Chunkable")
  * [MergeFunc](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc "vectorbtpro.utils.merging.MergeFunc")
  * [NotChunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.NotChunked "vectorbtpro.utils.chunking.NotChunked")
  * [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param")
  * [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer")
  * [Takeable](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Takeable "vectorbtpro.generic.splitting.base.Takeable")
  * [Union](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Union "vectorbtpro.utils.annotations.Union")
  * [VarArgs](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.VarArgs "vectorbtpro.utils.annotations.VarArgs")
  * [VarKwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.VarKwargs "vectorbtpro.utils.annotations.VarKwargs")



* * *

## MetaAnnotatable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L154-L161 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.MetaAnnotatable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-4-1)MetaAnnotatable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-4-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-4-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-4-4))
    

Metaclass for [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable").

**Superclasses**

  * `builtins.type`



* * *

## Union class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L207-L297 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Union "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-5-1)Union(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-5-2)    *annotations,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-5-3)    resolved=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-5-4))
    

Class representing a union of one to multiple annotations.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.annotations.Annotatable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.annotations.Annotatable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.annotations.Annotatable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.annotations.Annotatable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.annotations.Annotatable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.annotations.Annotatable.find_messages")
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
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### annotations field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Union.annotations "Permanent link")

Annotations.

* * *

### resolve method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L220-L297 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Union.resolve "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-6-1)Union.resolve()
    

Resolve the union.

* * *

### resolved field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Union.resolved "Permanent link")

Whether the instance is resolved.

* * *

## VarArgs class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L185-L193 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.VarArgs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-7-1)VarArgs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-7-2)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-7-3))
    

Class representing annotations for variable positional arguments.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.annotations.Annotatable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.annotations.Annotatable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.annotations.Annotatable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.annotations.Annotatable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.annotations.Annotatable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.annotations.Annotatable.find_messages")
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

### args field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.VarArgs.args "Permanent link")

Tuple with annotations.

* * *

## VarKwargs class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py#L196-L204 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.VarKwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-8-1)VarKwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-8-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#__codelineno-8-3))
    

Class representing annotations for variable keyword arguments.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.annotations.Annotatable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.annotations.Annotatable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.annotations.Annotatable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.annotations.Annotatable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.annotations.Annotatable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.annotations.Annotatable.find_messages")
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

### kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/annotations.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.VarKwargs.kwargs "Permanent link")

Dict with annotations.
