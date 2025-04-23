search_

#  search_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_ "Permanent link")

Utilities for searching.

* * *

## FIRST_TOKEN_REGEX Pattern[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.FIRST_TOKEN_REGEX "Permanent link")

First token regex for [parse_path_str](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.parse_path_str "vectorbtpro.utils.search_.parse_path_str").

Matches the same as [PATH_TOKEN_REGEX](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.PATH_TOKEN_REGEX "vectorbtpro.utils.search_.PATH_TOKEN_REGEX") but at the start.

* * *

## PATH_TOKEN_REGEX Pattern[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.PATH_TOKEN_REGEX "Permanent link")

Path token regex for [parse_path_str](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.parse_path_str "vectorbtpro.utils.search_.parse_path_str").

Matches `.key`, `['key']`, `["key"]`, `[0]`, `.0`, etc.

* * *

## search_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.search_config "Permanent link")

Config of functions that can be used in searching and replacement.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-2)    find_exact=<function find_exact at 0x11c292020>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-3)    find_start=<function find_start at 0x11c2920c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-4)    find_end=<function find_end at 0x11c292160>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-5)    find_substring=<function find_substring at 0x11c292200>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-6)    find_regex=<function find_regex at 0x11c2922a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-7)    find_fuzzy=<function find_fuzzy at 0x11c292340>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-8)    find_rapidfuzz=<function find_rapidfuzz at 0x11c292480>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-9)    find=<function find at 0x11c292520>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-10)    replace_exact=<function replace_exact at 0x11c2925c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-11)    replace_start=<function replace_start at 0x11c292660>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-12)    replace_end=<function replace_end at 0x11c292700>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-13)    replace_substring=<function replace_substring at 0x11c2927a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-14)    replace_regex=<function replace_regex at 0x11c292840>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-15)    replace_fuzzy=<function replace_fuzzy at 0x11c2928e0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-16)    replace=<function replace at 0x11c292980>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-0-17))
    

* * *

## combine_path_str function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L100-L122 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.combine_path_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-1-1)combine_path_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-1-2)    path_str1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-1-3)    path_str2
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-1-4))
    

Combine two path strings into one.

* * *

## combine_pathlike_keys function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L165-L188 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.combine_pathlike_keys "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-2-1)combine_pathlike_keys(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-2-2)    key1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-2-3)    key2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-2-4)    resolve=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-2-5)    minimize=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-2-6))
    

Combine two path-like keys.

* * *

## contains_in_obj function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L385-L459 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.contains_in_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-1)contains_in_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-3)    match_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-4)    traversal=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-5)    excl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-6)    incl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-7)    max_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-8)    max_depth=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-9)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-3-10))
    

Return whether there is any match in an object in an iterative manner.

Argument `traversal` can be "DFS" for depth-first search or "BFS" for breadth-first search.

See [find_in_obj](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_in_obj "vectorbtpro.utils.search_.find_in_obj") for arguments.

* * *

## find function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1140-L1171 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-4-1)find(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-4-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-4-3)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-4-4)    mode='substring',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-4-5)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-4-6)    return_type='bool',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-4-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-4-8))
    

Find a target within a string using the specified mode and return type.

The following return types are supported:

  * "bool": True for match, False for no match
  * "start": List of start indices of matches
  * "range": List of (start, end) tuples of matches
  * "match": List of matched strings



* * *

## find_and_replace_in_obj function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L614-L750 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_and_replace_in_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-1)find_and_replace_in_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-3)    match_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-4)    replace_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-5)    excl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-6)    incl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-7)    max_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-8)    max_depth=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-9)    make_copy=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-10)    check_any_first=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-11)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-5-12))
    

Find and replace matches in an object in a recursive manner.

See [find_in_obj](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_in_obj "vectorbtpro.utils.search_.find_in_obj") for arguments.

Note

If the object is deep (such as a dict or a list), creates a copy of it if any match found inside, thus losing the reference to the original. Make sure to do a deep or hybrid copy of the object before proceeding for consistent behavior, or disable `make_copy` to override the original in place.

* * *

## find_end function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L970-L993 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_end "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-6-1)find_end(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-6-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-6-3)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-6-4)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-6-5)    return_type='bool'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-6-6))
    

Find at the end of a string.

* * *

## find_exact function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L918-L941 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_exact "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-7-1)find_exact(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-7-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-7-3)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-7-4)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-7-5)    return_type='bool'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-7-6))
    

Find a string.

* * *

## find_fuzzy function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1070-L1111 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_fuzzy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-1)find_fuzzy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-3)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-4)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-5)    threshold=70,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-6)    max_insertions=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-7)    max_substitutions=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-8)    max_deletions=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-9)    max_l_dist=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-10)    return_type='bool'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-8-11))
    

Find a substring in a string using fuzzysearch.

* * *

## find_in_obj function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L462-L558 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_in_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-1)find_in_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-3)    match_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-4)    traversal=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-5)    excl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-6)    incl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-7)    stringify_keys=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-8)    max_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-9)    max_depth=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-10)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-9-11))
    

Find matches in an object in an iterative manner.

Traverses dicts, tuples, lists and (frozen-)sets. Does not look for matches in keys.

Argument `traversal` can be "DFS" for depth-first search or "BFS" for breadth-first search.

If `excl_types` is not None, uses [is_instance_of](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_instance_of "vectorbtpro.utils.checks.is_instance_of") to check whether the object is one of the types that are blacklisted. If so, the object is simply returned. Same for `incl_types` for whitelisting, but it has a priority over `excl_types`.

If `max_len` is not None, processes any object only if it's shorter than the specified length.

If `max_depth` is not None, processes any object only up to a certain recursion level. Level of 0 means dicts and other iterables are not processed, only matches are expected.

Returns a map of keys (multiple levels get represented by a tuple) to their respective values.

For defaults, see [search](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.search "vectorbtpro._settings.search").

* * *

## find_rapidfuzz function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1114-L1137 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_rapidfuzz "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-10-1)find_rapidfuzz(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-10-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-10-3)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-10-4)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-10-5)    processor=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-10-6)    threshold=70,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-10-7)    return_type='bool'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-10-8))
    

Find a substring in a string using RapidFuzz.

* * *

## find_regex function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1030-L1067 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_regex "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-11-1)find_regex(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-11-2)    pattern,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-11-3)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-11-4)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-11-5)    flags=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-11-6)    group=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-11-7)    return_type='bool'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-11-8))
    

Find a RegEx pattern in a string.

* * *

## find_start function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L944-L967 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-12-1)find_start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-12-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-12-3)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-12-4)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-12-5)    return_type='bool'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-12-6))
    

Find at the start of a string.

* * *

## find_substring function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L996-L1027 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_substring "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-13-1)find_substring(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-13-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-13-3)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-13-4)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-13-5)    return_type='bool'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-13-6))
    

Find a substring in a string.

* * *

## flatten_obj function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L753-L842 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.flatten_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-1)flatten_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-3)    traversal=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-4)    annotate_all=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-5)    excl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-6)    incl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-7)    stringify_keys=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-8)    max_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-9)    max_depth=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-14-10))
    

Flatten object.

Argument `traversal` can be "DFS" for depth-first search or "BFS" for breadth-first search.

See [find_in_obj](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.find_in_obj "vectorbtpro.utils.search_.find_in_obj") for arguments.

* * *

## get_pathlike_key function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L191-L233 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.get_pathlike_key "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-15-1)get_pathlike_key(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-15-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-15-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-15-4)    keep_path=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-15-5))
    

Get the value under a path-like key in an object.

Paths can be tuples out of individual tokens, or a string with tokens. Each token can be either a key in a mapping, a position in a sequence, or an attribute.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-1)>>> obj = dict(a=[dict(b="cde")])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-2)>>> vbt.utils.search_.get_pathlike_key(obj, "a")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-3)[{'b': 'cde'}]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-5)>>> vbt.utils.search_.get_pathlike_key(obj, ("a", 0))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-6)>>> vbt.utils.search_.get_pathlike_key(obj, "a.0")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-7)>>> vbt.utils.search_.get_pathlike_key(obj, "a[0]")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-8){'b': 'cde'}
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-10)>>> vbt.utils.search_.get_pathlike_key(obj, ("a", 0, "b"))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-11)>>> vbt.utils.search_.get_pathlike_key(obj, "a[0].b")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-12)>>> vbt.utils.search_.get_pathlike_key(obj, "a[0]['b']")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-13)'cde'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-15)>>> vbt.utils.search_.get_pathlike_key(obj, ("a", 0, "b", 1))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-16)>>> vbt.utils.search_.get_pathlike_key(obj, "a[0].b[1]")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-16-17)'d'
    

* * *

## minimize_pathlike_key function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L125-L132 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.minimize_pathlike_key "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-17-1)minimize_pathlike_key(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-17-2)    key
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-17-3))
    

Minimize a path-like key.

* * *

## parse_path_str function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L65-L97 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.parse_path_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-18-1)parse_path_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-18-2)    path_str
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-18-3))
    

Parse the path string into a list of tokens.

* * *

## remove_pathlike_key function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L306-L382 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.remove_pathlike_key "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-19-1)remove_pathlike_key(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-19-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-19-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-19-4)    make_copy=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-19-5)    prev_keys=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-19-6))
    

Remove the value under a path-like key in an object.

* * *

## replace function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1300-L1323 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-20-1)replace(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-20-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-20-3)    replacement,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-20-4)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-20-5)    mode='substring',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-20-6)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-20-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-20-8))
    

Replace a target string within a source string using the specified mode.

* * *

## replace_end function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1207-L1222 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace_end "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-21-1)replace_end(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-21-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-21-3)    replacement,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-21-4)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-21-5)    ignore_case=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-21-6))
    

Replace at the end of a string.

* * *

## replace_exact function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1174-L1186 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace_exact "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-22-1)replace_exact(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-22-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-22-3)    replacement,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-22-4)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-22-5)    ignore_case=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-22-6))
    

Replace a string.

* * *

## replace_fuzzy function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1253-L1297 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace_fuzzy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-1)replace_fuzzy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-3)    replacement,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-4)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-5)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-6)    threshold=70,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-7)    max_insertions=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-8)    max_substitutions=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-9)    max_deletions=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-10)    max_l_dist=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-23-11))
    

Replace a substring in a string using fuzzysearch.

* * *

## replace_in_obj function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L561-L611 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace_in_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-24-1)replace_in_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-24-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-24-3)    path_dct
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-24-4))
    

Replace matches in an object in a recursive manner using a path dictionary.

Keys in the path dictionary can be path-like keys.

* * *

## replace_regex function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1239-L1250 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace_regex "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-25-1)replace_regex(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-25-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-25-3)    replacement,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-25-4)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-25-5)    ignore_case=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-25-6)    flags=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-25-7))
    

Replace a target in a string using RegEx.

* * *

## replace_start function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1189-L1204 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace_start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-26-1)replace_start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-26-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-26-3)    replacement,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-26-4)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-26-5)    ignore_case=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-26-6))
    

Replace at the start of a string.

* * *

## replace_substring function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L1225-L1236 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.replace_substring "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-27-1)replace_substring(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-27-2)    target,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-27-3)    replacement,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-27-4)    string,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-27-5)    ignore_case=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-27-6))
    

Replace a substring in a string.

* * *

## resolve_pathlike_key function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L135-L147 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.resolve_pathlike_key "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-28-1)resolve_pathlike_key(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-28-2)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-28-3)    minimize=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-28-4))
    

Convert a path-like key into a path key.

* * *

## set_pathlike_key function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L236-L303 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.set_pathlike_key "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-29-1)set_pathlike_key(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-29-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-29-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-29-4)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-29-5)    make_copy=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-29-6)    prev_keys=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-29-7))
    

Set the value under a path-like key in an object.

* * *

## stringify_pathlike_key function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L150-L162 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.stringify_pathlike_key "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-30-1)stringify_pathlike_key(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-30-2)    key
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-30-3))
    

Convert a path-like key into a string.

* * *

## unflatten_obj function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L845-L915 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.unflatten_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-31-1)unflatten_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-31-2)    path_dct
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-31-3))
    

Unflatten object in a recursive manner using a path dictionary.

Keys in the path dictionary can be path-like keys.

* * *

## Not class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py#L30-L35 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.Not "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-32-1)Not(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-32-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-32-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#__codelineno-32-4))
    

Class representing a negation when searching.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.attr_.DefineMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.attr_.DefineMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.attr_.DefineMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.attr_.DefineMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.attr_.DefineMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.attr_.DefineMixin.find_messages")
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

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/search_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.Not.value "Permanent link")

Value.
