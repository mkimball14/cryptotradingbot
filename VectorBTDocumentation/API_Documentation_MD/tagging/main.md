tagging

#  tagging module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/tagging.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#vectorbtpro.utils.tagging "Permanent link")

Utilities for working with tags.

* * *

## match_tags function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/tagging.py#L20-L65 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#vectorbtpro.utils.tagging.match_tags "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-0-1)match_tags(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-0-2)    tags,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-0-3)    in_tags
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-0-4))
    

Match tags in `tags` to that in `in_tags`.

Multiple tags in `tags` are combined using OR rule, that is, returns True if any of them is found in `in_tags`. If any tag is not an identifier, evaluates it as a boolean expression. All tags in `in_tags` must be identifiers.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-1)>>> from vectorbtpro.utils.tagging import match_tags
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-3)>>> match_tags('hello', 'hello')
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-4)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-5)>>> match_tags('hello', 'world')
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-6)False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-7)>>> match_tags(['hello', 'world'], 'world')
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-8)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-9)>>> match_tags('hello', ['hello', 'world'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-10)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-11)>>> match_tags('hello and world', ['hello', 'world'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-12)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-13)>>> match_tags('hello and not world', ['hello', 'world'])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#__codelineno-1-14)False
    
