formatting

#  formatting module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting "Permanent link")

Utilities for formatting.

* * *

## camel_to_snake_case function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L35-L40 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.camel_to_snake_case "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-0-1)camel_to_snake_case(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-0-2)    camel_str
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-0-3))
    

Convert a camel case string to a snake case string.

* * *

## dump function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L370-L459 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.dump "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-1-1)dump(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-1-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-1-3)    dump_engine='prettify',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-1-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-1-5))
    

Dump an object to a string.

* * *

## format_array function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L218-L246 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.format_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-2-1)format_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-2-2)    array,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-2-3)    tabulate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-2-4)    html=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-2-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-2-6))
    

Format an array.

Arguments are passed to `pd.DataFrame.to_string` or `pd.DataFrame.to_html` if `tabulate` is False, otherwise to `tabulate.tabulate`. If `tabulate` is None, will be set to True if the `tabulate` library is installed and `html` is disabled.

* * *

## format_func function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L334-L355 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.format_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-3-1)format_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-3-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-3-3)    incl_doc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-3-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-3-5))
    

Format a function.

* * *

## format_parameter function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L266-L285 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.format_parameter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-4-1)format_parameter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-4-2)    param,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-4-3)    annotate=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-4-4))
    

Format a parameter of a signature.

* * *

## format_signature function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L288-L331 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.format_signature "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-5-1)format_signature(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-5-2)    signature,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-5-3)    annotate=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-5-4)    start='\n    ',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-5-5)    separator=',\n    ',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-5-6)    end='\n'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-5-7))
    

Format a signature.

* * *

## get_dump_language function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L462-L480 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.get_dump_language "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-6-1)get_dump_language(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-6-2)    dump_engine
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-6-3))
    

Get language corresponding to the dump engine.

* * *

## pdir function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L363-L367 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.pdir "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-7-1)pdir(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-7-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-7-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-7-4))
    

Print the output of [parse_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.parse_attrs "vectorbtpro.utils.attr_.parse_attrs").

* * *

## phelp function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L358-L360 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.phelp "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-8-1)phelp(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-8-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-8-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-8-4))
    

Print the output of [format_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.format_func "vectorbtpro.utils.formatting.format_func").

* * *

## pprint function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L213-L215 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.pprint "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-9-1)pprint(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-9-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-9-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-9-4))
    

Print the output of [prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.prettify "vectorbtpro.utils.formatting.prettify").

* * *

## prettify function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L137-L210 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.prettify "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-10-1)prettify(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-10-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-10-3)    replace=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-10-4)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-10-5)    htchar='    ',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-10-6)    lfchar='\n',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-10-7)    indent=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-10-8))
    

Prettify an object.

Unfolds regular Python data structures such as lists and tuples.

If `obj` is an instance of [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified"), calls [Prettified.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.formatting.Prettified.prettify").

* * *

## prettify_dict function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L96-L134 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.prettify_dict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-11-1)prettify_dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-11-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-11-3)    replace=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-11-4)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-11-5)    htchar='    ',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-11-6)    lfchar='\n',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-11-7)    indent=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-11-8))
    

Prettify a dictionary.

* * *

## prettify_inited function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L65-L93 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.prettify_inited "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-1)prettify_inited(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-2)    cls,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-3)    kwargs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-4)    replace=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-5)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-6)    htchar='    ',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-7)    lfchar='\n',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-8)    indent=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-12-9))
    

Prettify an instance initialized with keyword arguments.

* * *

## ptable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L249-L263 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.ptable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-13-1)ptable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-13-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-13-3)    display_html=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-13-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-13-5))
    

Print the output of [format_array](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.format_array "vectorbtpro.utils.formatting.format_array").

If `display_html` is None, checks whether the code runs in a IPython notebook, and if so, becomes True. If `display_html` is True, displays the table in HTML format.

* * *

## Prettified class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L43-L62 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-14-1)Prettified()
    

Abstract class that can be prettified.

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
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



* * *

### pprint method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L54-L56 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-15-1)Prettified.pprint(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-15-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-15-3))
    

Pretty-print the object.

* * *

### prettify method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/formatting.py#L46-L52 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-16-1)Prettified.prettify(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-16-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#__codelineno-16-3))
    

Prettify the object.

Warning

Calling [prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.prettify "vectorbtpro.utils.formatting.prettify") can lead to an infinite recursion. Make sure to pre-process this object.
