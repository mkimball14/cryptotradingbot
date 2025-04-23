merging

#  merging module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging "Permanent link")

Utilities for merging.

* * *

## parse_merge_func function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py#L100-L126 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.parse_merge_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-0-1)parse_merge_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-0-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-0-3)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-0-4))
    

Parser the merging function from the function's annotations.

* * *

## MergeFunc class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py#L31-L97 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-1-1)MergeFunc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-1-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-1-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-1-4))
    

Class representing a merging function and its keyword arguments.

Can be directly called to call the underlying (already resolved and with keyword arguments attached) merging function.

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

### context field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc.context "Permanent link")

Context for substituting templates in [MergeFunc.merge_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc.merge_func "vectorbtpro.utils.merging.MergeFunc.merge_func") and [MergeFunc.merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc.merge_kwargs "vectorbtpro.utils.merging.MergeFunc.merge_kwargs").

* * *

### eval_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc.eval_id "Permanent link")

One or more identifiers at which to evaluate this instance.

* * *

### eval_id_prefix field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc.eval_id_prefix "Permanent link")

Prefix for the substitution id.

* * *

### merge_func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc.merge_func "Permanent link")

Merging function.

* * *

### merge_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc.merge_kwargs "Permanent link")

Keyword arguments passed to the merging function.

* * *

### resolve_merge_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/merging.py#L76-L88 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc.resolve_merge_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#__codelineno-2-1)MergeFunc.resolve_merge_func()
    

Get the merging function where keyword arguments are hard-coded.
