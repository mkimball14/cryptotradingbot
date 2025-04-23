module_

#  module_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_ "Permanent link")

Utilities for modules.

* * *

## package_shortcut_config HybridConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.package_shortcut_config "Permanent link")

Config for package shortcuts.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-0-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-0-2)    vbt='vectorbtpro',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-0-3)    pd='pandas',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-0-4)    np='numpy',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-0-5)    nb='numba'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-0-6))
    

* * *

## annotate_refname_parts function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L558-L569 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.annotate_refname_parts "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-1-1)annotate_refname_parts(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-1-2)    refname
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-1-3))
    

Return the type of each reference name part.

* * *

## assert_can_import function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L202-L226 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.assert_can_import "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-2-1)assert_can_import(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-2-2)    pkg_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-2-3))
    

Assert that a package can be imported.

Must be listed in `opt_dep_config`.

* * *

## assert_can_import_any function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L229-L247 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.assert_can_import_any "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-3-1)assert_can_import_any(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-3-2)    *pkg_names
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-3-3))
    

Assert that any from packages can be imported.

Must be listed in `opt_dep_config`.

* * *

## check_installed function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L182-L184 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.check_installed "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-4-1)check_installed(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-4-2)    pkg_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-4-3))
    

Check if a package is installed.

* * *

## find_class function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L164-L179 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.find_class "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-5-1)find_class(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-5-2)    path
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-5-3))
    

Find the class by its path.

* * *

## get_api_ref function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L582-L609 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_api_ref "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-6-1)get_api_ref(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-6-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-6-3)    module=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-6-4)    resolve=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-6-5)    vbt_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-6-6))
    

Get the API reference to an object.

* * *

## get_caller_qualname function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L274-L296 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_caller_qualname "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-7-1)get_caller_qualname()
    

Returns the qualified name of the method or function that called this function.

* * *

## get_imlucky_url function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L572-L574 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_imlucky_url "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-8-1)get_imlucky_url(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-8-2)    query
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-8-3))
    

Get the "I'm lucky" URL on DuckDuckGo for a query.

* * *

## get_installed_overview function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L187-L189 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_installed_overview "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-9-1)get_installed_overview()
    

Get an overview of installed packages in `opt_dep_config`.

* * *

## get_method_class function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L299-L314 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_method_class "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-10-1)get_method_class(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-10-2)    meth
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-10-3))
    

Get the class of a method.

* * *

## get_module function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L59-L61 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_module "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-11-1)get_module(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-11-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-11-3))
    

Get module of an object.

* * *

## get_obj function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L499-L517 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-12-1)get_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-12-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-12-3)    allow_multiple=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-12-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-12-5))
    

Get the object by its (resolved) reference name.

* * *

## get_package_meta function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L192-L199 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_package_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-13-1)get_package_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-13-2)    pkg_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-13-3))
    

Get metadata of a package.

* * *

## get_refname function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L466-L484 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_refname "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-14-1)get_refname(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-14-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-14-3)    module=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-14-4)    resolve=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-14-5))
    

Parse and (optionally) resolve the reference name(s) of an object.

* * *

## get_refname_module_and_qualname function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L348-L367 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_refname_module_and_qualname "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-15-1)get_refname_module_and_qualname(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-15-2)    refname,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-15-3)    module=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-15-4))
    

Get the module and the qualified name from a reference name.

* * *

## get_refname_obj function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L487-L496 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.get_refname_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-16-1)get_refname_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-16-2)    refname
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-16-3))
    

Get the object under a reference name.

* * *

## imlucky function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L577-L579 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.imlucky "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-17-1)imlucky(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-17-2)    query,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-17-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-17-4))
    

Open the "I'm lucky" URL on DuckDuckGo for a query.

* * *

## import_module_from_path function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L262-L271 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.import_module_from_path "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-18-1)import_module_from_path(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-18-2)    module_path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-18-3)    reload=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-18-4))
    

Import the module from a path.

* * *

## is_from_module function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L64-L67 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.is_from_module "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-19-1)is_from_module(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-19-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-19-3)    module
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-19-4))
    

Return whether `obj` is from module `module`.

* * *

## list_module_keys function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L70-L96 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.list_module_keys "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-20-1)list_module_keys(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-20-2)    module_or_name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-20-3)    whitelist=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-20-4)    blacklist=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-20-5))
    

List the names of all public functions and classes defined in the module `module_name`.

Includes the names listed in `whitelist` and excludes the names listed in `blacklist`.

* * *

## open_api_ref function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L612-L619 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.open_api_ref "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-21-1)open_api_ref(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-21-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-21-3)    module=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-21-4)    resolve=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-21-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-21-6))
    

Open the API reference to an object.

* * *

## parse_refname function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L317-L345 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.parse_refname "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-22-1)parse_refname(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-22-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-22-3))
    

Get the reference name of an object.

* * *

## prepare_refname function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L520-L555 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.prepare_refname "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-23-1)prepare_refname(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-23-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-23-3)    module=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-23-4)    resolve=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-23-5)    vbt_only=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-23-6)    return_parts=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-23-7)    raise_error=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-23-8))
    

Prepare (optionally) the module and the qualified name.

* * *

## resolve_refname function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L370-L463 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.resolve_refname "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-24-1)resolve_refname(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-24-2)    refname,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-24-3)    module=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-24-4))
    

Resolve a reference name.

* * *

## search_package function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L99-L161 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.search_package "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-25-1)search_package(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-25-2)    package,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-25-3)    match_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-25-4)    blacklist=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-25-5)    path_attrs=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-25-6)    return_first=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-25-7))
    

Search a package.

Match function should accept the name of the object and the object itself, and return a boolean.

* * *

## warn_cannot_import function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/module_.py#L250-L259 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.warn_cannot_import "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-26-1)warn_cannot_import(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-26-2)    pkg_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#__codelineno-26-3))
    

Warn if a package is cannot be imported.

Must be listed in `opt_dep_config`.
