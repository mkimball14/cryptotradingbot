_dtypes

#  _dtypes module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_dtypes.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#vectorbtpro._dtypes "Permanent link")

Default data types for internal use.

* * *

## float_ class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_dtypes.py "Jump to source") { #vectorbtpro._dtypes.float64 data-toc-label="float_ " }[¶](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#float_-class-vectorbtprodtypesfloat64-data-toc-labelfloat "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-0-1)float64(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-0-2)    x=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-0-3)    /
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-0-4))
    

Double-precision floating-point number type, compatible with Python `float` and C `double`.

:Character code: `'d'` :Canonical name: `numpy.double` :Alias: `numpy.float_` :Alias on this platform (Darwin arm64): `numpy.float64`: 64-bit precision floating-point number type: sign bit, 11 bits exponent, 52 bits mantissa.

**Superclasses**

  * `builtins.float`
  * `numpy.floating`
  * `numpy.generic`
  * `numpy.inexact`
  * `numpy.number`



* * *

### as_integer_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_dtypes.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#vectorbtpro._dtypes.float64.as_integer_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-1-1)float64.as_integer_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-1-2)    ...
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-1-3))
    

double.as_integer_ratio() -> (int, int)

Return a pair of integers, whose ratio is exactly equal to the original floating point number, and with a positive denominator. Raise `OverflowError` on infinities and a `ValueError` on NaNs.

> > > np.double(10.0).as_integer_ratio() (10, 1) np.double(0.0).as_integer_ratio() (0, 1) np.double(-.25).as_integer_ratio() (-1, 4)

* * *

### is_integer method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_dtypes.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#vectorbtpro._dtypes.float64.is_integer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-2-1)float64.is_integer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-2-2)    ...
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-2-3))
    

double.is_integer() -> bool

Return `True` if the floating point number is finite with integral value, and `False` otherwise.

.. versionadded:: 1.22

## Examples[¶](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#examples "Permanent link")

> > > np.double(-2.0).is_integer() True np.double(3.2).is_integer() False

* * *

## int_ class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_dtypes.py "Jump to source") { #vectorbtpro._dtypes.int64 data-toc-label="int_ " }[¶](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#int_-class-vectorbtprodtypesint64-data-toc-labelint "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-3-1)int64(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-3-2)    ...
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-3-3))
    

Signed integer type, compatible with Python `int` and C `long`.

:Character code: `'l'` :Canonical name: `numpy.int_` :Alias on this platform (Darwin arm64): `numpy.int64`: 64-bit signed integer (`-9_223_372_036_854_775_808` to `9_223_372_036_854_775_807`). :Alias on this platform (Darwin arm64): `numpy.intp`: Signed integer large enough to fit pointer, compatible with C `intptr_t`.

**Superclasses**

  * `numpy.generic`
  * `numpy.integer`
  * `numpy.number`
  * `numpy.signedinteger`



* * *

### bit_count method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_dtypes.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#vectorbtpro._dtypes.int64.bit_count "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-4-1)int64.bit_count(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-4-2)    ...
    [](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#__codelineno-4-3))
    

int64.bit_count() -> int

Computes the number of 1-bits in the absolute value of the input. Analogous to the builtin `int.bit_count` or `popcount` in C++.

## Examples[¶](https://vectorbt.pro/pvt_7a467f6b/api/_dtypes/#examples_1 "Permanent link")

> > > np.int64(127).bit_count() 7 np.int64(-127).bit_count() 7
