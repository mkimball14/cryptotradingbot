math_

#  math_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_ "Permanent link")

Math utilities.

* * *

## add_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py#L117-L122 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.add_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-0-1)add_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-0-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-0-3)    b,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-0-4)    use_tol=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-0-5)    rel_tol=1e-09,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-0-6)    abs_tol=1e-12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-0-7))
    

Add two floats.

* * *

## is_addition_zero_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py#L101-L114 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.is_addition_zero_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-1-1)is_addition_zero_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-1-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-1-3)    b,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-1-4)    use_tol=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-1-5)    rel_tol=1e-09,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-1-6)    abs_tol=1e-12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-1-7))
    

Tell whether addition of two values yields zero.

* * *

## is_close_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py#L27-L42 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.is_close_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-2-1)is_close_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-2-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-2-3)    b,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-2-4)    use_tol=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-2-5)    rel_tol=1e-09,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-2-6)    abs_tol=1e-12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-2-7))
    

Tell whether two values are approximately equal.

* * *

## is_close_or_greater_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py#L73-L84 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.is_close_or_greater_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-3-1)is_close_or_greater_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-3-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-3-3)    b,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-3-4)    use_tol=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-3-5)    rel_tol=1e-09,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-3-6)    abs_tol=1e-12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-3-7))
    

Tell whether the first value is approximately equal to or greater than the second value.

* * *

## is_close_or_less_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py#L59-L70 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.is_close_or_less_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-4-1)is_close_or_less_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-4-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-4-3)    b,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-4-4)    use_tol=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-4-5)    rel_tol=1e-09,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-4-6)    abs_tol=1e-12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-4-7))
    

Tell whether the first value is approximately equal to or less than the second value.

* * *

## is_greater_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py#L87-L98 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.is_greater_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-5-1)is_greater_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-5-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-5-3)    b,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-5-4)    use_tol=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-5-5)    rel_tol=1e-09,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-5-6)    abs_tol=1e-12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-5-7))
    

Tell whether the first value is approximately greater than the second value.

* * *

## is_less_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py#L45-L56 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.is_less_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-6-1)is_less_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-6-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-6-3)    b,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-6-4)    use_tol=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-6-5)    rel_tol=1e-09,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-6-6)    abs_tol=1e-12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-6-7))
    

Tell whether the first value is approximately less than the second value.

* * *

## round_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/math_.py#L125-L130 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.round_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-7-1)round_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-7-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-7-3)    use_round=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-7-4)    decimals=12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#__codelineno-7-5))
    

Round a float to a number of decimals.
