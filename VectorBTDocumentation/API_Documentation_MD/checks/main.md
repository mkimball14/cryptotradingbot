checks

#  checks module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks "Permanent link")

Utilities for validation during runtime.

* * *

## assert_array_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L784-L795 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_array_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-0-1)assert_array_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-0-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-0-3)    arg2
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-0-4))
    

Raise exception if the first argument and the second argument have different metadata or values.

* * *

## assert_columns_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L759-L762 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_columns_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-1-1)assert_columns_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-1-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-1-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-1-4)    check_names=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-1-5))
    

Raise exception if the first argument and the second argument have different columns.

* * *

## assert_dict_sequence_valid function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L837-L845 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_dict_sequence_valid "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-2-1)assert_dict_sequence_valid(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-2-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-2-3)    lvl_keys
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-2-4))
    

Raise exception if a dict or any dict in a sequence of dicts has keys that are not in `lvl_keys`.

* * *

## assert_dict_valid function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L818-L834 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_dict_valid "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-3-1)assert_dict_valid(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-3-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-3-3)    lvl_keys
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-3-4))
    

Raise exception if dict the argument has keys that are not in `lvl_keys`.

`lvl_keys` must be a list of lists, each corresponding to a level in the dict.

* * *

## assert_dtype function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L639-L661 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_dtype "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-4-1)assert_dtype(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-4-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-4-3)    dtype,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-4-4)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-4-5))
    

Raise exception if the argument is not of data type `dtype`.

* * *

## assert_dtype_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L689-L707 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_dtype_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-5-1)assert_dtype_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-5-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-5-3)    arg2
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-5-4))
    

Raise exception if the first argument and the second argument have different data types.

* * *

## assert_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L808-L815 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-6-1)assert_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-6-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-6-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-6-4)    deep=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-6-5))
    

Raise exception if the first argument and the second argument are different.

* * *

## assert_in function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L555-L562 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_in "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-7-1)assert_in(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-7-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-7-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-7-4)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-7-5))
    

Raise exception if the first argument is not in the second argument.

* * *

## assert_index_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L753-L756 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_index_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-8-1)assert_index_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-8-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-8-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-8-4)    check_names=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-8-5))
    

Raise exception if the first argument and the second argument have different index.

* * *

## assert_instance_of function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L581-L591 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_instance_of "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-9-1)assert_instance_of(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-9-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-9-3)    types,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-9-4)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-9-5))
    

Raise exception if the argument is none of types `types`.

* * *

## assert_iterable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L854-L857 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_iterable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-10-1)assert_iterable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-10-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-10-3))
    

Raise exception if the argument is not an iterable.

* * *

## assert_len_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L721-L726 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_len_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-11-1)assert_len_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-11-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-11-3)    arg2
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-11-4))
    

Raise exception if the first argument and the second argument have different length.

Does not transform arguments to NumPy arrays.

* * *

## assert_level_not_exists function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L798-L805 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_level_not_exists "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-12-1)assert_level_not_exists(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-12-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-12-3)    level_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-12-4))
    

Raise exception if index the argument has level `level_name`.

* * *

## assert_meta_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L765-L781 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_meta_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-13-1)assert_meta_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-13-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-13-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-13-4)    axis=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-13-5))
    

Raise exception if the first argument and the second argument have different metadata.

* * *

## assert_ndim function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L710-L718 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_ndim "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-14-1)assert_ndim(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-14-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-14-3)    ndims
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-14-4))
    

Raise exception if the argument has a different number of dimensions than `ndims`.

* * *

## assert_not_instance_of function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L594-L604 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_not_instance_of "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-15-1)assert_not_instance_of(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-15-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-15-3)    types,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-15-4)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-15-5))
    

Raise exception if the argument is one of types `types`.

* * *

## assert_not_none function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L571-L578 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_not_none "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-16-1)assert_not_none(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-16-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-16-3)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-16-4))
    

Raise exception if the argument is None.

* * *

## assert_not_subclass_of function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L620-L630 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_not_subclass_of "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-17-1)assert_not_subclass_of(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-17-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-17-3)    classes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-17-4)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-17-5))
    

Raise exception if the argument is a subclass of classes `classes`.

* * *

## assert_numba_func function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L565-L568 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_numba_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-18-1)assert_numba_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-18-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-18-3))
    

Raise exception if `func` is not Numba-compiled.

* * *

## assert_sequence function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L848-L851 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_sequence "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-19-1)assert_sequence(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-19-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-19-3))
    

Raise exception if the argument is not a sequence.

* * *

## assert_shape_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L729-L750 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_shape_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-20-1)assert_shape_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-20-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-20-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-20-4)    axis=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-20-5))
    

Raise exception if the first argument and the second argument have different shapes along `axis`.

* * *

## assert_subclass_of function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L607-L617 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_subclass_of "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-21-1)assert_subclass_of(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-21-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-21-3)    classes,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-21-4)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-21-5))
    

Raise exception if the argument is not a subclass of classes `classes`.

* * *

## assert_subdtype function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L664-L686 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_subdtype "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-22-1)assert_subdtype(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-22-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-22-3)    dtype,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-22-4)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-22-5))
    

Raise exception if the argument is not a sub data type of `dtype`.

* * *

## assert_type_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L633-L636 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.assert_type_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-23-1)assert_type_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-23-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-23-3)    arg2
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-23-4))
    

Raise exception if the first argument and the second argument have different types.

* * *

## iskeyword function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.iskeyword "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-24-1)frozenset.__contains__(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-24-2)    ...
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-24-3))
    

x.**contains**(y) <==> y in x.

* * *

## func_accepts_arg function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L315-L328 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.func_accepts_arg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-25-1)func_accepts_arg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-25-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-25-3)    arg_name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-25-4)    arg_kind=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-25-5))
    

Check whether `func` accepts a positional or keyword argument with name `arg_name`.

* * *

## in_notebook function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L530-L543 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.in_notebook "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-26-1)in_notebook()
    

Check whether the code runs in a notebook.

* * *

## is_any_array function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L194-L196 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_any_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-27-1)is_any_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-27-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-27-3))
    

Check whether the argument is a NumPy array or a Pandas object.

* * *

## is_bool function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L94-L96 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_bool "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-28-1)is_bool(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-28-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-28-3))
    

Check whether the argument is a bool.

* * *

## is_builtin_func function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L57-L59 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_builtin_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-29-1)is_builtin_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-29-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-29-3))
    

Check whether the argument is a built-in function.

* * *

## is_class function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L461-L476 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_class "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-30-1)is_class(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-30-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-30-3)    types
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-30-4))
    

Check whether the argument is `types`.

`types` can be one or multiple types, strings, or patterns of type [Regex](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.Regex "vectorbtpro.utils.parsing.Regex").

* * *

## is_classic_func function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L52-L54 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_classic_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-31-1)is_classic_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-31-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-31-3))
    

Check whether the argument is a classic function.

* * *

## is_collection function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L208-L216 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_collection "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-32-1)is_collection(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-32-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-32-3))
    

Check whether the argument is a collection.

* * *

## is_complex_collection function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L219-L223 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_complex_collection "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-33-1)is_complex_collection(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-33-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-33-3))
    

Check whether the argument is a collection but not a string or bytes object.

* * *

## is_complex_iterable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L237-L241 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_complex_iterable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-34-1)is_complex_iterable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-34-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-34-3))
    

Check whether the argument is iterable but not a string or bytes object.

* * *

## is_complex_sequence function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L256-L260 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_complex_sequence "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-35-1)is_complex_sequence(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-35-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-35-3))
    

Check whether the argument is a sequence but not a string or bytes object.

* * *

## is_deep_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L344-L458 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_deep_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-36-1)is_deep_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-36-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-36-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-36-4)    check_exact=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-36-5)    debug=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-36-6)    only_types=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-36-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-36-8))
    

Check whether two objects are equal (deep check).

* * *

## is_default_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L292-L294 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_default_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-37-1)is_default_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-37-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-37-3)    check_names=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-37-4))
    

Check whether index is a basic range.

* * *

## is_dt function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L139-L141 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_dt "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-38-1)is_dt(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-38-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-38-3))
    

Check whether the argument is a datetime object.

* * *

## is_dt_like function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L144-L146 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_dt_like "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-39-1)is_dt_like(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-39-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-39-3))
    

Check whether the argument is a datetime-like object.

* * *

## is_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L331-L341 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-40-1)is_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-40-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-40-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-40-4)    equality_func=<function <lambda>>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-40-5))
    

Check whether two objects are equal.

* * *

## is_float function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L104-L106 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_float "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-41-1)is_float(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-41-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-41-3))
    

Check whether the argument is a float.

* * *

## is_frame function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L184-L186 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_frame "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-42-1)is_frame(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-42-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-42-3))
    

Check whether the argument is `pd.DataFrame`.

* * *

## is_frequency function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L129-L131 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_frequency "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-43-1)is_frequency(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-43-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-43-3))
    

Check whether the argument is a frequency object.

* * *

## is_frequency_like function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L134-L136 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_frequency_like "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-44-1)is_frequency_like(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-44-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-44-3))
    

Check whether the argument is a frequency-like object.

* * *

## is_function function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L89-L91 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_function "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-45-1)is_function(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-45-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-45-3))
    

Check whether the argument is a lamdba, (built-in or Numba) function, or method.

* * *

## is_hashable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L263-L272 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_hashable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-46-1)is_hashable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-46-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-46-3))
    

Check whether the argument can be hashed.

* * *

## is_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L174-L176 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-47-1)is_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-47-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-47-3))
    

Check whether the argument is `pd.Index`.

* * *

## is_index_equal function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L275-L289 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_index_equal "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-48-1)is_index_equal(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-48-2)    arg1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-48-3)    arg2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-48-4)    check_names=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-48-5))
    

Check whether indexes are equal.

If `check_names` is True, checks whether names are equal on top of `pd.Index.equals`.

* * *

## is_instance_of function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L508-L512 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_instance_of "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-49-1)is_instance_of(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-49-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-49-3)    types
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-49-4))
    

Check whether the argument is an instance of `types`.

`types` can be one or multiple types or strings.

* * *

## is_int function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L99-L101 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_int "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-50-1)is_int(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-50-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-50-3))
    

Check whether the argument is an integer (and not a timedelta, for example).

* * *

## is_iterable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L226-L234 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_iterable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-51-1)is_iterable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-51-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-51-3))
    

Check whether the argument is iterable.

* * *

## is_mapping function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L515-L517 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_mapping "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-52-1)is_mapping(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-52-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-52-3))
    

Check whether the arguments is a mapping.

* * *

## is_mapping_like function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L520-L522 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_mapping_like "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-53-1)is_mapping_like(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-53-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-53-3))
    

Check whether the arguments is a mapping-like object.

* * *

## is_method function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L62-L64 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_method "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-54-1)is_method(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-54-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-54-3))
    

Check whether the argument is a method.

* * *

## is_multi_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L179-L181 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_multi_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-55-1)is_multi_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-55-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-55-3))
    

Check whether the argument is `pd.MultiIndex`.

* * *

## is_namedtuple function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L297-L307 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_namedtuple "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-56-1)is_namedtuple(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-56-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-56-3))
    

Check whether object is an instance of namedtuple.

* * *

## is_np_array function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L159-L161 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_np_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-57-1)is_np_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-57-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-57-3))
    

Check whether the argument is a NumPy array.

* * *

## is_np_scalar function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L114-L116 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_np_scalar "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-58-1)is_np_scalar(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-58-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-58-3))
    

Check whether the argument is a NumPy scalar.

* * *

## is_numba_enabled function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L67-L69 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_numba_enabled "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-59-1)is_numba_enabled()
    

Check whether Numba is enabled globally.

* * *

## is_numba_func function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L72-L86 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_numba_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-60-1)is_numba_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-60-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-60-3))
    

Check whether the argument is a Numba-compiled function.

* * *

## is_number function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L109-L111 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_number "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-61-1)is_number(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-61-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-61-3))
    

Check whether the argument is a number.

* * *

## is_pandas function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L189-L191 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_pandas "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-62-1)is_pandas(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-62-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-62-3))
    

Check whether the argument is `pd.Series`, `pd.Index`, or `pd.DataFrame`.

* * *

## is_record function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L310-L312 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_record "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-63-1)is_record(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-63-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-63-3))
    

Check whether object is a NumPy record.

* * *

## is_record_array function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L164-L166 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_record_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-64-1)is_record_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-64-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-64-3))
    

Check whether the argument is a structured NumPy array.

* * *

## is_sequence function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L244-L253 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_sequence "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-65-1)is_sequence(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-65-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-65-3))
    

Check whether the argument is a sequence.

* * *

## is_series function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L169-L171 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_series "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-66-1)is_series(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-66-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-66-3))
    

Check whether the argument is `pd.Series`.

* * *

## is_subclass_of function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L479-L505 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_subclass_of "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-67-1)is_subclass_of(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-67-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-67-3)    types
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-67-4))
    

Check whether the argument is a subclass of `types`.

`types` can be one or multiple types, strings, or patterns of type [Regex](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.Regex "vectorbtpro.utils.parsing.Regex").

* * *

## is_td function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L119-L121 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_td "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-68-1)is_td(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-68-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-68-3))
    

Check whether the argument is a timedelta object.

* * *

## is_td_like function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L124-L126 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_td_like "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-69-1)is_td_like(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-69-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-69-3))
    

Check whether the argument is a timedelta-like object.

* * *

## is_time function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L149-L151 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-70-1)is_time(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-70-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-70-3))
    

Check whether the argument is a time object.

* * *

## is_time_like function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L154-L156 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_time_like "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-71-1)is_time_like(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-71-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-71-3))
    

Check whether the argument is a time-like object.

* * *

## is_valid_variable_name function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L525-L527 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_valid_variable_name "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-72-1)is_valid_variable_name(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-72-2)    arg
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-72-3))
    

Check whether the argument is a valid variable name.

* * *

## safe_assert function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L549-L552 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.safe_assert "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-73-1)safe_assert(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-73-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-73-3)    msg=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-73-4))
    

Assert a condition in a safe way.

* * *

## Comparable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L36-L46 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-74-1)Comparable()
    

Class representing an object that can be compared to another object.

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

### equals method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/checks.py#L39-L43 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable.equals "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-75-1)Comparable.equals(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-75-2)    other,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-75-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-75-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#__codelineno-75-5))
    

Check two objects for (deep) equality.

Should accept the keyword arguments accepted by [is_deep_equal](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_deep_equal "vectorbtpro.utils.checks.is_deep_equal").
