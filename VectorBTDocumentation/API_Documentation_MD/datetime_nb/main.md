datetime_nb

#  datetime_nb module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb "Permanent link")

Numba-compiled utilities for working with dates and time.

* * *

## DTCS namedtuple[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCS "Permanent link")

Status returned by [within_fixed_dtc_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.within_fixed_dtc_nb "vectorbtpro.utils.datetime_nb.within_fixed_dtc_nb") and [within_periodic_dtc_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.within_periodic_dtc_nb "vectorbtpro.utils.datetime_nb.within_periodic_dtc_nb").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-0-1)DTCST(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-0-2)    SU=-3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-0-3)    EU=-2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-0-4)    U=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-0-5)    O=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-0-6)    I=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-0-7))
    

**Attributes**

**`SU`**
    Start matched, rest unknown. Move down the stack.
**`EU`**
    End matched, rest unknown. Move down the stack.
**`U`**
    Unknown. Move down the stack.
**`O`**
    Outside
**`I`**
    Inside

* * *

## d_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.d_ns "Permanent link")

Day in nanoseconds.

* * *

## d_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.d_td "Permanent link")

Day as a timedelta.

* * *

## h_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.h_ns "Permanent link")

Hour in nanoseconds.

* * *

## h_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.h_td "Permanent link")

Hour as a timedelta.

* * *

## m_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.m_ns "Permanent link")

Minute in nanoseconds.

* * *

## m_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.m_td "Permanent link")

Minute as a timedelta.

* * *

## mo_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.mo_ns "Permanent link")

Month in nanoseconds.

* * *

## mo_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.mo_td "Permanent link")

Month as a timedelta.

* * *

## ms_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.ms_ns "Permanent link")

Millisecond in nanoseconds.

* * *

## ms_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.ms_td "Permanent link")

Millisecond as a timedelta.

* * *

## ns_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.ns_td "Permanent link")

Nanosecond as a timedelta.

* * *

## q_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.q_ns "Permanent link")

Quarter in nanoseconds.

* * *

## q_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.q_td "Permanent link")

Quarter as a timedelta.

* * *

## s_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.s_ns "Permanent link")

Second in nanoseconds.

* * *

## s_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.s_td "Permanent link")

Second as a timedelta.

* * *

## semi_mo_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.semi_mo_ns "Permanent link")

Semi-month in nanoseconds.

* * *

## semi_mo_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.semi_mo_td "Permanent link")

Semi-month as a timedelta.

* * *

## unix_epoch_dt datetime64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.unix_epoch_dt "Permanent link")

Unix epoch (datetime).

* * *

## us_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.us_ns "Permanent link")

Microsecond in nanoseconds.

* * *

## us_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.us_td "Permanent link")

Microsecond as a timedelta.

* * *

## w_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.w_ns "Permanent link")

Week in nanoseconds.

* * *

## w_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.w_td "Permanent link")

Week as a timedelta.

* * *

## y_ns int[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.y_ns "Permanent link")

Year in nanoseconds.

* * *

## y_td timedelta64[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.y_td "Permanent link")

Year as a timedelta.

* * *

## day_changed_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L224-L227 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.day_changed_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-1-1)day_changed_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-1-2)    ts1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-1-3)    ts2
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-1-4))
    

Whether the day changed.

* * *

## day_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L211-L215 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.day_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-2-1)day_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-2-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-2-3))
    

Get the day of the month.

* * *

## day_of_year_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L286-L291 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.day_of_year_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-3-1)day_of_year_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-3-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-3-3))
    

Get the day of the year.

* * *

## days_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L169-L172 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.days_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-4-1)days_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-4-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-4-3))
    

Get the number of days.

* * *

## from_civil_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L191-L200 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.from_civil_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-5-1)from_civil_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-5-2)    y,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-5-3)    m,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-5-4)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-5-5))
    

Convert a year, month, and day into the timestamp.

* * *

## future_weekday_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L278-L283 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.future_weekday_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-6-1)future_weekday_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-6-2)    ts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-6-3)    weekday,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-6-4)    zero_start=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-6-5))
    

Get the timestamp of a weekday in the future.

* * *

## hour_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L163-L166 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.hour_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-7-1)hour_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-7-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-7-3))
    

Get the hour.

* * *

## hours_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L157-L160 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.hours_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-8-1)hours_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-8-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-8-3))
    

Get the number of hours.

* * *

## index_matches_dtc_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L372-L389 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.index_matches_dtc_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-9-1)index_matches_dtc_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-9-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-9-3)    other_dtc
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-9-4))
    

Run [matches_dtc_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.matches_dtc_nb "vectorbtpro.utils.datetime_nb.matches_dtc_nb") on each element in an index and return a mask.

* * *

## index_within_dtc_range_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L851-L880 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.index_within_dtc_range_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-10-1)index_within_dtc_range_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-10-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-10-3)    start_dtc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-10-4)    end_dtc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-10-5)    closed_start=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-10-6)    closed_end=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-10-7))
    

Run [within_dtc_range_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.within_dtc_range_nb "vectorbtpro.utils.datetime_nb.within_dtc_range_nb") on each element in an index and return a mask.

* * *

## is_leap_year_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L314-L317 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.is_leap_year_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-11-1)is_leap_year_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-11-2)    y
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-11-3))
    

Get whether the year is a leap year.

* * *

## last_day_of_month_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L320-L347 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.last_day_of_month_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-12-1)last_day_of_month_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-12-2)    y,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-12-3)    m
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-12-4))
    

Get the last day of the month.

* * *

## matches_date_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L203-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.matches_date_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-13-1)matches_date_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-13-2)    ts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-13-3)    y,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-13-4)    m,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-13-5)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-13-6))
    

Check whether the timestamp match the date provided in the civil format.

* * *

## matches_dtc_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L350-L369 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.matches_dtc_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-14-1)matches_dtc_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-14-2)    dtc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-14-3)    other_dtc
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-14-4))
    

Return whether one or more datetime components match other components.

* * *

## microsecond_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L115-L118 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.microsecond_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-15-1)microsecond_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-15-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-15-3))
    

Get the microsecond.

* * *

## microseconds_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L109-L112 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.microseconds_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-16-1)microseconds_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-16-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-16-3))
    

Get the number of microseconds.

* * *

## midnight_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L218-L221 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.midnight_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-17-1)midnight_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-17-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-17-3))
    

Get the midnight of this day.

* * *

## millisecond_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L127-L130 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.millisecond_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-18-1)millisecond_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-18-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-18-3))
    

Get the millisecond.

* * *

## milliseconds_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L121-L124 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.milliseconds_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-19-1)milliseconds_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-19-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-19-3))
    

Get the number of milliseconds.

* * *

## minute_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L151-L154 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.minute_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-20-1)minute_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-20-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-20-3))
    

Get the minute.

* * *

## minutes_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L145-L148 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.minutes_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-21-1)minutes_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-21-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-21-3))
    

Get the number of minutes.

* * *

## month_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L300-L304 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.month_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-22-1)month_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-22-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-22-3))
    

Get the month of the year.

* * *

## must_resolve_dtc_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L591-L602 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.must_resolve_dtc_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-23-1)must_resolve_dtc_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-23-2)    c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-23-3)    start_c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-23-4)    end_c=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-23-5))
    

Return whether the component must be resolved.

* * *

## nanosecond_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L103-L106 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.nanosecond_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-24-1)nanosecond_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-24-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-24-3))
    

Get the nanosecond.

* * *

## past_weekday_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L270-L275 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.past_weekday_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-25-1)past_weekday_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-25-2)    ts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-25-3)    weekday,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-25-4)    zero_start=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-25-5))
    

Get the timestamp of a weekday in the past.

* * *

## second_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L139-L142 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.second_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-26-1)second_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-26-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-26-3))
    

Get the seconds.

* * *

## second_remainder_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L97-L100 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.second_remainder_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-27-1)second_remainder_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-27-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-27-3))
    

Get the nanosecond remainder after the second.

* * *

## seconds_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L133-L136 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.seconds_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-28-1)seconds_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-28-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-28-3))
    

Get the number of seconds.

* * *

## start_dtc_eq_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L621-L634 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.start_dtc_eq_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-29-1)start_dtc_eq_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-29-2)    c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-29-3)    start_c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-29-4)    end_c=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-29-5))
    

Return whether the start component equals to the end component.

* * *

## start_dtc_gt_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L637-L650 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.start_dtc_gt_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-30-1)start_dtc_gt_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-30-2)    c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-30-3)    start_c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-30-4)    end_c=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-30-5))
    

Return whether the start component is greater than the end component.

* * *

## start_dtc_lt_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L605-L618 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.start_dtc_lt_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-31-1)start_dtc_lt_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-31-2)    c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-31-3)    start_c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-31-4)    end_c=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-31-5))
    

Return whether the start component is less than the end component.

* * *

## to_civil_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L175-L188 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.to_civil_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-32-1)to_civil_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-32-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-32-3))
    

Convert a timestamp into a tuple of the year, month, and day.

* * *

## week_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L294-L297 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.week_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-33-1)week_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-33-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-33-3))
    

Get the week of the year.

* * *

## weekday_diff_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L251-L267 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.weekday_diff_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-34-1)weekday_diff_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-34-2)    weekday1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-34-3)    weekday2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-34-4)    zero_start=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-34-5))
    

Get the difference in days between two weekdays.

* * *

## weekday_from_days_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L230-L240 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.weekday_from_days_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-35-1)weekday_from_days_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-35-2)    days,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-35-3)    zero_start=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-35-4))
    

Get the weekday from the total number of days.

Weekdays are ranging from 0 (Monday) to 6 (Sunday).

* * *

## weekday_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L243-L248 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.weekday_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-36-1)weekday_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-36-2)    ts,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-36-3)    zero_start=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-36-4))
    

Get the weekday.

Weekdays are ranging from 0 (Monday) to 6 (Sunday).

* * *

## within_dtc_range_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L653-L848 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.within_dtc_range_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-37-1)within_dtc_range_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-37-2)    dtc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-37-3)    start_dtc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-37-4)    end_dtc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-37-5)    closed_start=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-37-6)    closed_end=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-37-7))
    

Return whether one or more datetime components are within a range.

* * *

## within_fixed_dtc_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L420-L510 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.within_fixed_dtc_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-1)within_fixed_dtc_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-2)    c,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-3)    start_c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-4)    end_c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-5)    prev_status=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-6)    closed_start=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-7)    closed_end=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-8)    is_last=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-38-9))
    

Return whether a single datetime component is within a fixed range.

Returns a status of the type [DTCS](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCS "vectorbtpro.utils.datetime_nb.DTCS").

* * *

## within_periodic_dtc_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L513-L588 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.within_periodic_dtc_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-1)within_periodic_dtc_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-2)    c,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-3)    start_c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-4)    end_c=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-5)    prev_status=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-6)    closed_start=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-7)    closed_end=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-8)    overflow_later=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-9)    is_last=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-39-10))
    

Return whether a single datetime component is within a periodic range.

Returns a status of the type [DTCS](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCS "vectorbtpro.utils.datetime_nb.DTCS").

* * *

## year_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L307-L311 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.year_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-40-1)year_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-40-2)    ts
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-40-3))
    

Get the year.

* * *

## DTCST class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py#L392-L397 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCST "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-41-1)DTCST(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-41-2)    SU=-3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-41-3)    EU=-2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-41-4)    U=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-41-5)    O=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-41-6)    I=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#__codelineno-41-7))
    

DTCST(SU, EU, U, O, I)

**Superclasses**

  * `builtins.tuple`



* * *

### EU field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCST.EU "Permanent link")

Alias for field number 1

* * *

### I field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCST.I "Permanent link")

Alias for field number 4

* * *

### O field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCST.O "Permanent link")

Alias for field number 3

* * *

### SU field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCST.SU "Permanent link")

Alias for field number 0

* * *

### U field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_nb.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/#vectorbtpro.utils.datetime_nb.DTCST.U "Permanent link")

Alias for field number 2
