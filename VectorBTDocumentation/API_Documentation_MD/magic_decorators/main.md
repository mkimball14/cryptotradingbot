decorators magic_decorators

#  magic_decorators module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/magic_decorators.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#vectorbtpro.utils.magic_decorators "Permanent link")

Class decorators for attaching magic methods.

* * *

## binary_magic_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/magic_decorators.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#vectorbtpro.utils.magic_decorators.binary_magic_config "Permanent link")

Config of binary magic methods to be attached to a class.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-2)    __eq__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-3)        func=<ufunc 'equal'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-4)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-5)    __ne__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-6)        func=<ufunc 'not_equal'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-8)    __lt__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-9)        func=<ufunc 'less'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-10)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-11)    __gt__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-12)        func=<ufunc 'greater'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-14)    __le__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-15)        func=<ufunc 'less_equal'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-16)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-17)    __ge__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-18)        func=<ufunc 'greater_equal'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-19)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-20)    __add__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-21)        func=<ufunc 'add'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-22)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-23)    __sub__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-24)        func=<ufunc 'subtract'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-25)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-26)    __mul__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-27)        func=<ufunc 'multiply'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-28)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-29)    __pow__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-30)        func=<ufunc 'power'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-31)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-32)    __mod__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-33)        func=<ufunc 'remainder'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-35)    __floordiv__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-36)        func=<ufunc 'floor_divide'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-37)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-38)    __truediv__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-39)        func=<ufunc 'divide'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-40)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-41)    __radd__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-42)        func=<function <lambda> at 0x11df83740>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-43)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-44)    __rsub__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-45)        func=<function <lambda> at 0x11dfe9e40>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-46)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-47)    __rmul__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-48)        func=<function <lambda> at 0x11dfe9ee0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-49)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-50)    __rpow__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-51)        func=<function <lambda> at 0x11dfe9f80>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-52)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-53)    __rmod__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-54)        func=<function <lambda> at 0x11dfea020>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-55)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-56)    __rfloordiv__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-57)        func=<function <lambda> at 0x11dfea0c0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-58)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-59)    __rtruediv__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-60)        func=<function <lambda> at 0x11dfea160>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-61)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-62)    __and__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-63)        func=<ufunc 'bitwise_and'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-64)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-65)    __or__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-66)        func=<ufunc 'bitwise_or'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-67)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-68)    __xor__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-69)        func=<ufunc 'bitwise_xor'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-70)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-71)    __rand__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-72)        func=<function <lambda> at 0x11dfea200>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-73)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-74)    __ror__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-75)        func=<function <lambda> at 0x11dfea2a0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-76)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-77)    __rxor__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-78)        func=<function <lambda> at 0x11dfea340>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-79)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-0-80))
    

* * *

## unary_magic_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/magic_decorators.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#vectorbtpro.utils.magic_decorators.unary_magic_config "Permanent link")

Config of unary magic methods to be attached to a class.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-2)    __neg__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-3)        func=<ufunc 'negative'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-4)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-5)    __pos__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-6)        func=<ufunc 'positive'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-8)    __abs__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-9)        func=<ufunc 'absolute'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-10)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-11)    __invert__=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-12)        func=<ufunc 'invert'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-13)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-1-14))
    

* * *

## attach_binary_magic_methods function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/magic_decorators.py#L69-L107 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#vectorbtpro.utils.magic_decorators.attach_binary_magic_methods "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-2-1)attach_binary_magic_methods(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-2-2)    translate_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-2-3)    config=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-2-4))
    

Class decorator to attach binary magic methods to a class.

`translate_func` must

  * take `self`, `other`, and unary function,
  * perform computation, and
  * return the result.



`config` defaults to [binary_magic_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#vectorbtpro.utils.magic_decorators.binary_magic_config "vectorbtpro.utils.magic_decorators.binary_magic_config") and must contain target method names (keys) and dictionaries (values) with the following keys:

  * `func`: Function that combines two array-like objects.



* * *

## attach_unary_magic_methods function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/magic_decorators.py#L132-L169 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#vectorbtpro.utils.magic_decorators.attach_unary_magic_methods "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-3-1)attach_unary_magic_methods(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-3-2)    translate_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-3-3)    config=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#__codelineno-3-4))
    

Class decorator to attach unary magic methods to a class.

`translate_func` must

  * take `self` and unary function,
  * perform computation, and
  * return the result.



`config` defaults to [unary_magic_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/magic_decorators/#vectorbtpro.utils.magic_decorators.unary_magic_config "vectorbtpro.utils.magic_decorators.unary_magic_config") and must contain target method names (keys) and dictionaries (values) with the following keys:

  * `func`: Function that transforms one array-like object.


