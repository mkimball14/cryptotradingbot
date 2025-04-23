eval_

#  eval_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/eval_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_ "Permanent link")

Utilities for evaluation and compilation.

* * *

## evaluate function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/eval_.py#L27-L40 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.evaluate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-0-1)evaluate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-0-2)    expr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-0-3)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-0-4))
    

Evaluate one to multiple lines of expression.

Returns the result of the last line.

* * *

## get_free_vars function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/eval_.py#L55-L73 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.get_free_vars "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-1-1)get_free_vars(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-1-2)    expr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-1-3))
    

Parse the code and retrieve all free variables, excluding built-in names.

* * *

## get_symbols function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/eval_.py#L43-L52 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.get_symbols "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-2-1)get_symbols(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-2-2)    table
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-2-3))
    

Get symbols from a symbol table recursively.

* * *

## Evaluable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/eval_.py#L76-L88 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-3-1)Evaluable()
    

Abstract class for instances that can be evaluated.

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
  * [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * [MergeFunc](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/#vectorbtpro.utils.merging.MergeFunc "vectorbtpro.utils.merging.MergeFunc")
  * [NotChunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.NotChunked "vectorbtpro.utils.chunking.NotChunked")
  * [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param "vectorbtpro.utils.params.Param")
  * [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer")
  * [Takeable](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Takeable "vectorbtpro.generic.splitting.base.Takeable")



* * *

### meets_eval_id method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/eval_.py#L79-L88 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-4-1)Evaluable.meets_eval_id(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-4-2)    eval_id
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#__codelineno-4-3))
    

Return whether the evaluation id of the instance meets the global evaluation id.
