mapping

#  mapping module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/mapping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping "Permanent link")

Mapping utilities.

* * *

## apply_mapping function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/mapping.py#L72-L210 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.apply_mapping "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-1)apply_mapping(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-3)    mapping_like=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-4)    enum_unkval=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-5)    reverse=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-6)    ignore_case=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-7)    ignore_underscores=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-8)    ignore_invalid=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-9)    ignore_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-10)    ignore_missing=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-11)    na_sentinel=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-0-12))
    

Apply mapping on object using a mapping-like object.

**Args**

**`obj`** : `any`
    

Any object.

Can take a scalar, tuple, list, set, frozenset, NumPy array, Index, Series, and DataFrame.

**`mapping_like`** : `mapping_like`
    

Any mapping-like object.

See [to_value_mapping](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.to_value_mapping "vectorbtpro.utils.mapping.to_value_mapping").

**`enum_unkval`** : `any`
    Missing value for enumerated types.
**`reverse`** : `bool`
    See `reverse` in [to_value_mapping](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.to_value_mapping "vectorbtpro.utils.mapping.to_value_mapping").
**`ignore_case`** : `bool`
    Whether to ignore the case if the key is a string.
**`ignore_underscores`** : `bool`
    Whether to ignore underscores if the key is a string.
**`ignore_invalid`** : `bool`
    Whether to remove any character that is not allowed in a Python variable.
**`ignore_type`** : `dtype_like` or `tuple`
    One or multiple types or data types to ignore.
**`ignore_missing`** : `bool`
    Whether to ignore missing values.
**`na_sentinel`** : `any`
    Value to mark “not found”.

* * *

## reverse_mapping function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/mapping.py#L24-L28 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.reverse_mapping "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-1-1)reverse_mapping(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-1-2)    mapping
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-1-3))
    

Reverse a mapping.

Returns a dict.

* * *

## to_field_mapping function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/mapping.py#L31-L43 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.to_field_mapping "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-2-1)to_field_mapping(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-2-2)    mapping_like
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-2-3))
    

Convert mapping-like object to a field mapping.

* * *

## to_value_mapping function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/mapping.py#L46-L69 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.to_value_mapping "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-3-1)to_value_mapping(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-3-2)    mapping_like,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-3-3)    reverse=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-3-4)    enum_unkval=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#__codelineno-3-5))
    

Convert mapping-like object to a value mapping.

Enable `reverse` to apply [reverse_mapping](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.reverse_mapping "vectorbtpro.utils.mapping.reverse_mapping") on the result dict.
