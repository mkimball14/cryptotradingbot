parsing

#  parsing module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing "Permanent link")

Utilities for parsing.

* * *

## ann_args_to_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L253-L268 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.ann_args_to_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-0-1)ann_args_to_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-0-2)    ann_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-0-3))
    

Convert annotated arguments back to positional and keyword arguments.

* * *

## annotate_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L168-L250 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.annotate_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-1)annotate_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-3)    args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-4)    kwargs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-5)    only_passed=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-6)    allow_partial=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-7)    attach_annotations=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-8)    flatten=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-1-9))
    

Annotate arguments and keyword arguments using the function's signature.

If `allow_partial` is True, required arguments that weren't provided won't raise an error. But regardless of `allow_partial`, arguments that aren't in the signature will still raise an error.

* * *

## extend_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L132-L165 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.extend_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-2-1)extend_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-2-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-2-3)    args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-2-4)    kwargs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-2-5)    **with_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-2-6))
    

Extend arguments and keyword arguments with other arguments.

* * *

## flat_ann_args_to_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L271-L273 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.flat_ann_args_to_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-3-1)flat_ann_args_to_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-3-2)    ann_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-3-3))
    

Convert flattened annotated arguments back to positional and keyword arguments.

* * *

## flatten_ann_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L276-L316 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.flatten_ann_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-4-1)flatten_ann_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-4-2)    ann_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-4-3))
    

Flatten annotated arguments.

* * *

## get_context_vars function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L477-L505 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.get_context_vars "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-5-1)get_context_vars(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-5-2)    var_names,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-5-3)    frames_back=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-5-4)    local_dict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-5-5)    global_dict=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-5-6))
    

Get variables from the local/global context.

* * *

## get_expr_var_names function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L472-L474 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.get_expr_var_names "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-6-1)get_expr_var_names(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-6-2)    expression
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-6-3))
    

Get variable names listed in the expression.

* * *

## get_forward_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L107-L129 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.get_forward_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-7-1)get_forward_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-7-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-7-3)    local_dict,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-7-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-7-5))
    

Get positional and keyword arguments to forward.

* * *

## get_func_arg_names function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L53-L76 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.get_func_arg_names "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-8-1)get_func_arg_names(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-8-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-8-3)    arg_kind=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-8-4)    req_only=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-8-5)    opt_only=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-8-6))
    

Get argument names of a function.

* * *

## get_func_kwargs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L47-L50 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.get_func_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-9-1)get_func_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-9-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-9-3))
    

Get keyword arguments with defaults of a function.

* * *

## get_variable_args_name function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L79-L85 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.get_variable_args_name "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-10-1)get_variable_args_name(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-10-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-10-3))
    

Get the name of variable positional arguments.

* * *

## get_variable_kwargs_name function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L93-L99 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.get_variable_kwargs_name "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-11-1)get_variable_kwargs_name(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-11-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-11-3))
    

Get the name of variable keyword arguments.

* * *

## has_variable_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L88-L90 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.has_variable_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-12-1)has_variable_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-12-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-12-3))
    

Return whether function accepts variable positions arguments.

* * *

## has_variable_kwargs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L102-L104 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.has_variable_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-13-1)has_variable_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-13-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-13-3))
    

Return whether function accepts variable keyword arguments.

* * *

## hash_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L451-L469 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.hash_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-14-1)hash_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-14-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-14-3)    args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-14-4)    kwargs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-14-5)    ignore_args=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-14-6))
    

Get hash of arguments.

Use `ignore_args` to provide a sequence of queries for arguments that should be ignored.

* * *

## ignore_flat_ann_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L427-L442 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.ignore_flat_ann_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-15-1)ignore_flat_ann_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-15-2)    flat_ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-15-3)    ignore_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-15-4))
    

Ignore flattened annotated arguments.

* * *

## match_and_set_flat_ann_arg function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L406-L424 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.match_and_set_flat_ann_arg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-16-1)match_and_set_flat_ann_arg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-16-2)    flat_ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-16-3)    query,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-16-4)    new_value
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-16-5))
    

Match an argument from flattened annotated arguments and set it to a new value.

See [match_flat_ann_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.match_flat_ann_arg "vectorbtpro.utils.parsing.match_flat_ann_arg") for matching logic.

* * *

## match_ann_arg function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L389-L403 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.match_ann_arg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-17-1)match_ann_arg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-17-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-17-3)    query,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-17-4)    return_name=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-17-5)    return_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-17-6))
    

Match an argument from annotated arguments.

See [match_flat_ann_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.match_flat_ann_arg "vectorbtpro.utils.parsing.match_flat_ann_arg") for matching logic.

* * *

## match_flat_ann_arg function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L359-L386 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.match_flat_ann_arg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-18-1)match_flat_ann_arg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-18-2)    flat_ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-18-3)    query,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-18-4)    return_name=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-18-5)    return_index=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-18-6))
    

Match an argument from flattened annotated arguments.

A query can be an integer indicating the position of the argument, or a string containing the name of the argument, or a regular expression for matching the name of the argument.

If multiple arguments were matched, returns the first one.

The position can stretch over any variable argument.

* * *

## suppress_stdout function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L508-L516 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.suppress_stdout "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-19-1)suppress_stdout(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-19-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-19-3))
    

Suppress output from a function.

* * *

## unflatten_ann_args function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L319-L356 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.unflatten_ann_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-20-1)unflatten_ann_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-20-2)    flat_ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-20-3)    partial_ann_args=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-20-4))
    

Unflatten annotated arguments.

* * *

## PrintsSuppressed class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L522-L526 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.PrintsSuppressed "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-21-1)PrintsSuppressed(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-21-2)    new_target
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-21-3))
    

Context manager to ignore print statements.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `abc.ABC`
  * `contextlib.AbstractContextManager`
  * `contextlib._RedirectStream`
  * `contextlib.redirect_stdout`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

## Regex class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L32-L44 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.Regex "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-22-1)Regex(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-22-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-22-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-22-4))
    

Class for matching a regular expression.

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

### flags field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.Regex.flags "Permanent link")

Flags.

* * *

### matches method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L42-L44 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.Regex.matches "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-23-1)Regex.matches(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-23-2)    string
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-23-3))
    

Return whether the string matches the regular expression pattern.

* * *

### pattern field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.Regex.pattern "Permanent link")

Pattern.

* * *

## UnhashableArgsError class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/parsing.py#L445-L448 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.UnhashableArgsError "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-24-1)UnhashableArgsError(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-24-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-24-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#__codelineno-24-4))
    

Unhashable arguments error.

**Superclasses**

  * `builtins.BaseException`
  * `builtins.Exception`


