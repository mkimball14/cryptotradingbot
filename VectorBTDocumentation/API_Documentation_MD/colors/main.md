colors

#  colors module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/colors.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#vectorbtpro.utils.colors "Permanent link")

Utilities for working with colors.

* * *

## adjust_lightness function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/colors.py#L91-L112 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#vectorbtpro.utils.colors.adjust_lightness "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-0-1)adjust_lightness(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-0-2)    color,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-0-3)    amount=0.7
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-0-4))
    

Lightens the given color by multiplying (1-luminosity) by the given amount.

Input can be matplotlib color string, hex string, or RGB tuple. Output will be an RGB string.

* * *

## adjust_opacity function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/colors.py#L76-L88 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#vectorbtpro.utils.colors.adjust_opacity "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-1-1)adjust_opacity(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-1-2)    color,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-1-3)    opacity
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-1-4))
    

Adjust opacity of color.

* * *

## map_value_to_cmap function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/colors.py#L20-L61 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#vectorbtpro.utils.colors.map_value_to_cmap "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-2-1)map_value_to_cmap(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-2-2)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-2-3)    cmap,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-2-4)    vmin=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-2-5)    vcenter=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-2-6)    vmax=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-2-7))
    

Get RGB of `value` from the colormap.

* * *

## parse_rgb_tuple function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/colors.py#L70-L73 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#vectorbtpro.utils.colors.parse_rgb_tuple "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-3-1)parse_rgb_tuple(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-3-2)    color
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-3-3))
    

Parse floating RGB tuple from string.

* * *

## parse_rgba_tuple function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/colors.py#L64-L67 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#vectorbtpro.utils.colors.parse_rgba_tuple "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-4-1)parse_rgba_tuple(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-4-2)    color
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/colors/#__codelineno-4-3))
    

Parse floating RGBA tuple from string.
