enum_

#  enum_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/enum_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#vectorbtpro.utils.enum_ "Permanent link")

Enum utilities.

In vectorbt, enums are represented by instances of named tuples to be easily used in Numba. Their values start with 0, while -1 means there is no value.

* * *

## map_enum_fields function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/enum_.py#L24-L32 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#vectorbtpro.utils.enum_.map_enum_fields "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-0-1)map_enum_fields(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-0-2)    field,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-0-3)    enum,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-0-4)    enum_unkval=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-0-5)    ignore_type=builtins.int,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-0-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-0-7))
    

Map fields to values.

See [apply_mapping](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.apply_mapping "vectorbtpro.utils.mapping.apply_mapping").

* * *

## map_enum_values function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/enum_.py#L35-L43 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#vectorbtpro.utils.enum_.map_enum_values "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-1-1)map_enum_values(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-1-2)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-1-3)    enum,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-1-4)    enum_unkval=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-1-5)    ignore_type=builtins.str,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-1-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/enum_/#__codelineno-1-7))
    

Map values to fields.

See [apply_mapping](https://vectorbt.pro/pvt_7a467f6b/api/utils/mapping/#vectorbtpro.utils.mapping.apply_mapping "vectorbtpro.utils.mapping.apply_mapping").
