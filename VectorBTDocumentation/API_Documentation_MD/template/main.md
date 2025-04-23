template

#  template module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template "Permanent link")

Utilities for working with templates.

* * *

## has_templates function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L281-L296 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.has_templates "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-0-1)has_templates(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-0-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-0-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-0-4))
    

Check if the object has any templates.

Uses [contains_in_obj](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.contains_in_obj "vectorbtpro.utils.search_.contains_in_obj").

Default can be overridden with `search_kwargs` under [template](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.template "vectorbtpro._settings.template").

* * *

## substitute_templates function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L299-L353 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.substitute_templates "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-1-1)substitute_templates(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-1-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-1-3)    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-1-4)    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-1-5)    eval_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-1-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-1-7))
    

Traverses the object recursively and, if any template found, substitutes it using a context.

Uses [find_and_replace_in_obj](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_and_replace_in_obj "vectorbtpro.utils.search_.find_and_replace_in_obj").

If `strict` is True, raises an error if processing template fails. Otherwise, returns the original template.

Default can be overridden with `search_kwargs` under [template](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.template "vectorbtpro._settings.template").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-3)>>> vbt.substitute_templates(vbt.Sub('$key', {'key': 100}))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-4)100
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-5)>>> vbt.substitute_templates(vbt.Sub('$key', {'key': 100}), {'key': 200})
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-6)200
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-7)>>> vbt.substitute_templates(vbt.Sub('$key$key'), {'key': 100})
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-8)100100
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-9)>>> vbt.substitute_templates(vbt.Rep('key'), {'key': 100})
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-10)100
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-11)>>> vbt.substitute_templates([vbt.Rep('key'), vbt.Sub('$key$key')], {'key': 100}, incl_types=list)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-12)[100, '100100']
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-13)>>> vbt.substitute_templates(vbt.RepFunc(lambda key: key == 100), {'key': 100})
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-14)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-15)>>> vbt.substitute_templates(vbt.RepEval('key == 100'), {'key': 100})
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-16)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-17)>>> vbt.substitute_templates(vbt.RepEval('key == 100', strict=True))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-18)NameError: name 'key' is not defined
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-19)>>> vbt.substitute_templates(vbt.RepEval('key == 100', strict=False))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-2-20)<vectorbtpro.utils.template.RepEval at 0x7fe3ad2ab668>
    

* * *

## CustomTemplate class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L34-L115 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-3-1)CustomTemplate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-3-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-3-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-3-4))
    

Class for substituting templates.

**Superclasses**

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



**Subclasses**

  * [Rep](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.Rep "vectorbtpro.utils.template.Rep")
  * [RepEval](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.RepEval "vectorbtpro.utils.template.RepEval")
  * [RepFunc](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.RepFunc "vectorbtpro.utils.template.RepFunc")
  * [SafeSub](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.SafeSub "vectorbtpro.utils.template.SafeSub")
  * [Sub](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.Sub "vectorbtpro.utils.template.Sub")



* * *

### context field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "Permanent link")

Context mapping.

* * *

### context_merge_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs "Permanent link")

Keyword arguments passed to [merge_dicts](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.merge_dicts "vectorbtpro.utils.config.merge_dicts").

* * *

### eval_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.eval_id "Permanent link")

One or more identifiers at which to evaluate this instance.

* * *

### get_context_vars method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L103-L105 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.get_context_vars "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-4-1)CustomTemplate.get_context_vars()
    

Get context variables.

* * *

### resolve_context method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L55-L87 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_context "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-5-1)CustomTemplate.resolve_context(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-5-2)    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-5-3)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-5-4))
    

Resolve [CustomTemplate.context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "vectorbtpro.utils.template.CustomTemplate.context").

Merges `context` in [template](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.template "vectorbtpro._settings.template"), [CustomTemplate.context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "vectorbtpro.utils.template.CustomTemplate.context"), and `context`. Automatically appends `eval_id` and `from vectorbtpro import *`.

* * *

### resolve_strict method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L89-L101 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_strict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-6-1)CustomTemplate.resolve_strict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-6-2)    strict=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-6-3))
    

Resolve [CustomTemplate.strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.strict "vectorbtpro.utils.template.CustomTemplate.strict").

If `strict` is None, uses `strict` in [template](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.template "vectorbtpro._settings.template").

* * *

### strict field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.strict "Permanent link")

Whether to raise an error if processing template fails.

If not None, overrides `strict` passed by [substitute_templates](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.substitute_templates "vectorbtpro.utils.template.substitute_templates").

* * *

### substitute method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L107-L115 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.substitute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-7-1)CustomTemplate.substitute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-7-2)    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-7-3)    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-7-4)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-7-5))
    

Abstract method to substitute the template [CustomTemplate.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.CustomTemplate.template") using the context from merging [CustomTemplate.context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "vectorbtpro.utils.template.CustomTemplate.context") and `context`.

* * *

### template field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "Permanent link")

Template to be processed.

* * *

## Rep class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L196-L219 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.Rep "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-8-1)Rep(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-8-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-8-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-8-4))
    

Class for replacing a template with the respective value from `context`.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.template.CustomTemplate.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.template.CustomTemplate.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.template.CustomTemplate.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.template.CustomTemplate.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.template.CustomTemplate.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.template.CustomTemplate.find_messages")
  * [CustomTemplate.context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "vectorbtpro.utils.template.CustomTemplate.context")
  * [CustomTemplate.context_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs "vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs")
  * [CustomTemplate.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.eval_id "vectorbtpro.utils.template.CustomTemplate.eval_id")
  * [CustomTemplate.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.template.CustomTemplate.fields")
  * [CustomTemplate.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.template.CustomTemplate.fields_dict")
  * [CustomTemplate.get_context_vars](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.get_context_vars "vectorbtpro.utils.template.CustomTemplate.get_context_vars")
  * [CustomTemplate.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.template.CustomTemplate.hash")
  * [CustomTemplate.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.template.CustomTemplate.hash_key")
  * [CustomTemplate.resolve_context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_context "vectorbtpro.utils.template.CustomTemplate.resolve_context")
  * [CustomTemplate.resolve_strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_strict "vectorbtpro.utils.template.CustomTemplate.resolve_strict")
  * [CustomTemplate.strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.strict "vectorbtpro.utils.template.CustomTemplate.strict")
  * [CustomTemplate.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.CustomTemplate.template")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.template.CustomTemplate.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.template.CustomTemplate.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.template.CustomTemplate.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.template.CustomTemplate.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.template.CustomTemplate.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.template.CustomTemplate.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.template.CustomTemplate.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.template.CustomTemplate.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.template.CustomTemplate.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.template.CustomTemplate.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.template.CustomTemplate.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.template.CustomTemplate.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.template.CustomTemplate.get_hash")



* * *

### substitute method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L202-L219 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.Rep.substitute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-9-1)Rep.substitute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-9-2)    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-9-3)    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-9-4)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-9-5))
    

Replace [Rep.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.Rep.template") as a key.

* * *

## RepEval class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L222-L246 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.RepEval "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-10-1)RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-10-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-10-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-10-4))
    

Class for evaluating a template expression using [evaluate](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.evaluate "vectorbtpro.utils.eval_.evaluate") with `context` used as locals.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.template.CustomTemplate.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.template.CustomTemplate.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.template.CustomTemplate.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.template.CustomTemplate.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.template.CustomTemplate.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.template.CustomTemplate.find_messages")
  * [CustomTemplate.context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "vectorbtpro.utils.template.CustomTemplate.context")
  * [CustomTemplate.context_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs "vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs")
  * [CustomTemplate.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.eval_id "vectorbtpro.utils.template.CustomTemplate.eval_id")
  * [CustomTemplate.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.template.CustomTemplate.fields")
  * [CustomTemplate.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.template.CustomTemplate.fields_dict")
  * [CustomTemplate.get_context_vars](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.get_context_vars "vectorbtpro.utils.template.CustomTemplate.get_context_vars")
  * [CustomTemplate.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.template.CustomTemplate.hash")
  * [CustomTemplate.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.template.CustomTemplate.hash_key")
  * [CustomTemplate.resolve_context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_context "vectorbtpro.utils.template.CustomTemplate.resolve_context")
  * [CustomTemplate.resolve_strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_strict "vectorbtpro.utils.template.CustomTemplate.resolve_strict")
  * [CustomTemplate.strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.strict "vectorbtpro.utils.template.CustomTemplate.strict")
  * [CustomTemplate.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.CustomTemplate.template")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.template.CustomTemplate.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.template.CustomTemplate.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.template.CustomTemplate.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.template.CustomTemplate.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.template.CustomTemplate.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.template.CustomTemplate.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.template.CustomTemplate.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.template.CustomTemplate.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.template.CustomTemplate.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.template.CustomTemplate.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.template.CustomTemplate.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.template.CustomTemplate.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.template.CustomTemplate.get_hash")



* * *

### substitute method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L229-L246 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.RepEval.substitute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-11-1)RepEval.substitute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-11-2)    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-11-3)    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-11-4)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-11-5))
    

Evaluate [RepEval.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.RepEval.template") as an expression.

* * *

## RepFunc class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L249-L278 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.RepFunc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-12-1)RepFunc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-12-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-12-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-12-4))
    

Class for calling a template function with argument names from `context`.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.template.CustomTemplate.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.template.CustomTemplate.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.template.CustomTemplate.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.template.CustomTemplate.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.template.CustomTemplate.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.template.CustomTemplate.find_messages")
  * [CustomTemplate.context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "vectorbtpro.utils.template.CustomTemplate.context")
  * [CustomTemplate.context_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs "vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs")
  * [CustomTemplate.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.eval_id "vectorbtpro.utils.template.CustomTemplate.eval_id")
  * [CustomTemplate.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.template.CustomTemplate.fields")
  * [CustomTemplate.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.template.CustomTemplate.fields_dict")
  * [CustomTemplate.get_context_vars](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.get_context_vars "vectorbtpro.utils.template.CustomTemplate.get_context_vars")
  * [CustomTemplate.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.template.CustomTemplate.hash")
  * [CustomTemplate.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.template.CustomTemplate.hash_key")
  * [CustomTemplate.resolve_context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_context "vectorbtpro.utils.template.CustomTemplate.resolve_context")
  * [CustomTemplate.resolve_strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_strict "vectorbtpro.utils.template.CustomTemplate.resolve_strict")
  * [CustomTemplate.strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.strict "vectorbtpro.utils.template.CustomTemplate.strict")
  * [CustomTemplate.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.CustomTemplate.template")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.template.CustomTemplate.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.template.CustomTemplate.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.template.CustomTemplate.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.template.CustomTemplate.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.template.CustomTemplate.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.template.CustomTemplate.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.template.CustomTemplate.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.template.CustomTemplate.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.template.CustomTemplate.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.template.CustomTemplate.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.template.CustomTemplate.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.template.CustomTemplate.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.template.CustomTemplate.get_hash")



* * *

### substitute method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L255-L278 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.RepFunc.substitute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-13-1)RepFunc.substitute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-13-2)    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-13-3)    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-13-4)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-13-5))
    

Call [RepFunc.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.RepFunc.template") as a function.

* * *

## SafeSub class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L157-L193 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.SafeSub "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-14-1)SafeSub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-14-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-14-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-14-4))
    

Class for substituting parts of a template string with the respective values from `context`.

Uses `string.Template.safe_substitute`.

Always returns a string.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.template.CustomTemplate.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.template.CustomTemplate.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.template.CustomTemplate.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.template.CustomTemplate.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.template.CustomTemplate.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.template.CustomTemplate.find_messages")
  * [CustomTemplate.context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "vectorbtpro.utils.template.CustomTemplate.context")
  * [CustomTemplate.context_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs "vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs")
  * [CustomTemplate.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.eval_id "vectorbtpro.utils.template.CustomTemplate.eval_id")
  * [CustomTemplate.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.template.CustomTemplate.fields")
  * [CustomTemplate.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.template.CustomTemplate.fields_dict")
  * [CustomTemplate.get_context_vars](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.get_context_vars "vectorbtpro.utils.template.CustomTemplate.get_context_vars")
  * [CustomTemplate.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.template.CustomTemplate.hash")
  * [CustomTemplate.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.template.CustomTemplate.hash_key")
  * [CustomTemplate.resolve_context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_context "vectorbtpro.utils.template.CustomTemplate.resolve_context")
  * [CustomTemplate.resolve_strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_strict "vectorbtpro.utils.template.CustomTemplate.resolve_strict")
  * [CustomTemplate.strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.strict "vectorbtpro.utils.template.CustomTemplate.strict")
  * [CustomTemplate.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.CustomTemplate.template")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.template.CustomTemplate.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.template.CustomTemplate.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.template.CustomTemplate.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.template.CustomTemplate.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.template.CustomTemplate.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.template.CustomTemplate.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.template.CustomTemplate.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.template.CustomTemplate.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.template.CustomTemplate.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.template.CustomTemplate.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.template.CustomTemplate.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.template.CustomTemplate.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.template.CustomTemplate.get_hash")



* * *

### substitute method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L176-L193 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.SafeSub.substitute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-15-1)SafeSub.substitute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-15-2)    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-15-3)    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-15-4)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-15-5))
    

Substitute parts of [Sub.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.Sub.template") as a regular template.

* * *

## Sub class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L118-L154 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.Sub "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-16-1)Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-16-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-16-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-16-4))
    

Class for substituting parts of a template string with the respective values from `context`.

Uses `string.Template.substitute`.

Always returns a string.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.template.CustomTemplate.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.template.CustomTemplate.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.template.CustomTemplate.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.template.CustomTemplate.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.template.CustomTemplate.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.template.CustomTemplate.find_messages")
  * [CustomTemplate.context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context "vectorbtpro.utils.template.CustomTemplate.context")
  * [CustomTemplate.context_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs "vectorbtpro.utils.template.CustomTemplate.context_merge_kwargs")
  * [CustomTemplate.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.eval_id "vectorbtpro.utils.template.CustomTemplate.eval_id")
  * [CustomTemplate.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.template.CustomTemplate.fields")
  * [CustomTemplate.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.template.CustomTemplate.fields_dict")
  * [CustomTemplate.get_context_vars](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.get_context_vars "vectorbtpro.utils.template.CustomTemplate.get_context_vars")
  * [CustomTemplate.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.template.CustomTemplate.hash")
  * [CustomTemplate.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.template.CustomTemplate.hash_key")
  * [CustomTemplate.resolve_context](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_context "vectorbtpro.utils.template.CustomTemplate.resolve_context")
  * [CustomTemplate.resolve_strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.resolve_strict "vectorbtpro.utils.template.CustomTemplate.resolve_strict")
  * [CustomTemplate.strict](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.strict "vectorbtpro.utils.template.CustomTemplate.strict")
  * [CustomTemplate.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.CustomTemplate.template")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.template.CustomTemplate.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.template.CustomTemplate.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.template.CustomTemplate.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.template.CustomTemplate.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.template.CustomTemplate.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.template.CustomTemplate.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.template.CustomTemplate.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.template.CustomTemplate.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.template.CustomTemplate.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.template.CustomTemplate.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.template.CustomTemplate.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.template.CustomTemplate.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.template.CustomTemplate.get_hash")



* * *

### substitute method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/template.py#L137-L154 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.Sub.substitute "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-17-1)Sub.substitute(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-17-2)    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-17-3)    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-17-4)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#__codelineno-17-5))
    

Substitute parts of [Sub.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate.template "vectorbtpro.utils.template.Sub.template") as a regular template.
