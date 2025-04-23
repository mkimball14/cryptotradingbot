warnings_

#  warnings_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/warnings_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_ "Permanent link")

Utilities for warnings.

* * *

## custom_formatwarning function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/warnings_.py#L37-L45 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_.custom_formatwarning "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-0-1)custom_formatwarning(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-0-2)    message,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-0-3)    category,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-0-4)    filename,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-0-5)    lineno,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-0-6)    line=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-0-7))
    

Custom warning formatter.

* * *

## use_formatwarning function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/warnings_.py#L26-L34 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_.use_formatwarning "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-1-1)use_formatwarning(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-1-2)    formatwarning
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-1-3))
    

Context manager to temporarily set a custom warning formatter.

* * *

## warn function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/warnings_.py#L52-L55 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_.warn "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-2-1)warn(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-2-2)    message,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-2-3)    category=vectorbtpro.utils.warnings_.VBTWarning,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-2-4)    stacklevel=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-2-5))
    

Emit a warning with a custom formatter.

* * *

## warn_stdout function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/warnings_.py#L58-L70 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_.warn_stdout "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-3-1)warn_stdout(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-3-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-3-3))
    

Supress and convert to a warning output from a function.

* * *

## VBTWarning class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/warnings_.py#L48-L49 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_.VBTWarning "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-4-1)VBTWarning(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-4-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-4-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-4-4))
    

Base class for warnings raised by VBT.

**Superclasses**

  * `builtins.BaseException`
  * `builtins.Exception`
  * `builtins.Warning`



* * *

## WarningsFiltered class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/warnings_.py#L73-L98 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_.WarningsFiltered "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-5-1)WarningsFiltered(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-5-2)    entries='ignore',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-5-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#__codelineno-5-4))
    

Context manager to ignore warnings.

Specify whether to record warnings and if an alternative module should be used other than sys.modules['warnings'].

For compatibility with Python 3.0, please consider all arguments to be keyword-only.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `warnings.catch_warnings`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### entries class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/warnings_.py#L80-L83 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_.WarningsFiltered.entries "Permanent link")

One or more simple entries to add into the list of warnings filters.
