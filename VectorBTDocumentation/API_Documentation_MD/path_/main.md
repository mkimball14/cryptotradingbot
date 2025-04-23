path_

#  path_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_ "Permanent link")

Utilities for working with paths.

* * *

## check_mkdir function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L104-L132 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.check_mkdir "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-0-1)check_mkdir(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-0-2)    dir_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-0-3)    mkdir=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-0-4)    mode=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-0-5)    parents=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-0-6)    exist_ok=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-0-7))
    

Check whether the path to a directory exists and create if it doesn't.

For defaults, see `mkdir` in [path](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.path "vectorbtpro._settings.path").

* * *

## dir_exists function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L74-L79 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.dir_exists "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-1-1)dir_exists(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-1-2)    dir_path
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-1-3))
    

Check whether a directory exists.

* * *

## dir_size function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L93-L101 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.dir_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-2-1)dir_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-2-2)    dir_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-2-3)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-2-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-2-5))
    

Get size of a directory.

* * *

## dir_tree function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L317-L327 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.dir_tree "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-3-1)dir_tree(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-3-2)    dir_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-3-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-3-4))
    

Generate a visual tree structure.

Uses [dir_tree_from_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.dir_tree_from_paths "vectorbtpro.utils.path_.dir_tree_from_paths").

* * *

## dir_tree_from_paths function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L212-L314 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.dir_tree_from_paths "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-1)dir_tree_from_paths(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-2)    paths,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-3)    root=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-4)    path_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-5)    root_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-6)    level=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-7)    limit_to_dirs=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-8)    length_limit=1000,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-9)    sort=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-10)    space='    ',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-11)    branch='│   ',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-12)    tee='├── ',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-13)    last='└── '
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-4-14))
    

Given paths, generate a visual tree structure.

* * *

## file_exists function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L66-L71 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.file_exists "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-5-1)file_exists(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-5-2)    file_path
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-5-3))
    

Check whether a file exists.

* * *

## file_size function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L82-L90 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.file_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-6-1)file_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-6-2)    file_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-6-3)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-6-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-6-5))
    

Get size of a file.

* * *

## get_common_prefix function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L169-L209 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.get_common_prefix "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-7-1)get_common_prefix(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-7-2)    paths
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-7-3))
    

Returns the common prefix of a list of URLs or file paths.

* * *

## list_any_files function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L40-L53 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.list_any_files "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-8-1)list_any_files(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-8-2)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-8-3)    recursive=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-8-4))
    

List files and dirs matching a path.

If the directory path is not provided, the current working directory is used.

* * *

## list_dirs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L61-L63 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.list_dirs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-9-1)list_dirs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-9-2)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-9-3)    recursive=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-9-4))
    

List dirs matching a path using [list_any_files](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.list_any_files "vectorbtpro.utils.path_.list_any_files").

* * *

## list_files function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L56-L58 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.list_files "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-10-1)list_files(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-10-2)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-10-3)    recursive=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-10-4))
    

List files matching a path using [list_any_files](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.list_any_files "vectorbtpro.utils.path_.list_any_files").

* * *

## make_dir function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L143-L146 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.make_dir "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-11-1)make_dir(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-11-2)    dir_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-11-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-11-4))
    

Make an empty directory.

* * *

## make_file function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L135-L140 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.make_file "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-12-1)make_file(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-12-2)    file_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-12-3)    mode=438,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-12-4)    exist_ok=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-12-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-12-6))
    

Make an empty file.

* * *

## print_dir_tree function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L330-L332 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.print_dir_tree "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-13-1)print_dir_tree(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-13-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-13-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-13-4))
    

Generate a directory tree with `tree` and print it out.

* * *

## remove_dir function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L158-L166 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.remove_dir "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-14-1)remove_dir(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-14-2)    dir_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-14-3)    missing_ok=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-14-4)    with_contents=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-14-5))
    

Remove (delete) a directory.

* * *

## remove_file function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/path_.py#L149-L155 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.remove_file "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-15-1)remove_file(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-15-2)    file_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-15-3)    missing_ok=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#__codelineno-15-4))
    

Remove (delete) a file.
