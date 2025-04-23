datetime_

#  datetime_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_ "Permanent link")

Utilities for working with dates and time.

* * *

## fuzzy_freq_str_config HybridConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.fuzzy_freq_str_config "Permanent link")

Config for fuzzy frequency mapping.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-2)    n='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-3)    ns='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-4)    nano='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-5)    nanos='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-6)    nanosecond='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-7)    nanoseconds='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-8)    u='us',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-9)    us='us',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-10)    micro='us',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-11)    micros='us',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-12)    microsecond='us',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-13)    microseconds='us',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-14)    l='ms',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-15)    ms='ms',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-16)    milli='ms',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-17)    millis='ms',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-18)    millisecond='ms',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-19)    milliseconds='ms',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-20)    s='s',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-21)    sec='s',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-22)    secs='s',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-23)    second='s',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-24)    seconds='s',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-25)    t='m',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-26)    min='m',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-27)    mins='m',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-28)    minute='m',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-29)    minutes='m',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-30)    h='h',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-31)    hour='h',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-32)    hours='h',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-33)    hourly='h',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-34)    d='D',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-35)    day='D',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-36)    days='D',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-37)    daily='D',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-38)    w='W',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-39)    wk='W',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-40)    wks='W',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-41)    week='W',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-42)    weeks='W',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-43)    weekly='W',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-44)    mo='M',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-45)    month='M',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-46)    months='M',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-47)    monthly='M',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-48)    q='Q',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-49)    quarter='Q',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-50)    quarters='Q',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-51)    quarterly='Q',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-52)    y='Y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-53)    year='Y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-54)    years='Y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-55)    yearly='Y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-56)    annual='Y',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-57)    annually='Y'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-0-58))
    

* * *

## sharp_freq_str_config HybridConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.sharp_freq_str_config "Permanent link")

Config for sharp frequency mapping.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-1-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-1-2)    m='m',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-1-3)    M='M'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-1-4))
    

* * *

## to_local_datetime partial function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_local_datetime "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-2-1)to_local_datetime(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-2-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-2-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-2-4))
    

Alias for [to_datetime](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_datetime "vectorbtpro.utils.datetime_.to_datetime") with `tz="tzlocal()"`.

* * *

## to_local_timestamp partial function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_local_timestamp "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-1)to_local_timestamp(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-3)    parse_with_dateparser=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-4)    dateparser_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-5)    unit='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-6)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-7)    tz='tzlocal()',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-8)    to_fixed_offset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-9)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-3-10))
    

Alias for [to_timestamp](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timestamp "vectorbtpro.utils.datetime_.to_timestamp") with `tz="tzlocal()"`.

* * *

## to_utc_datetime partial function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_utc_datetime "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-4-1)to_utc_datetime(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-4-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-4-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-4-4))
    

Alias for [to_datetime](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_datetime "vectorbtpro.utils.datetime_.to_datetime") with `tz="utc"`.

* * *

## to_utc_timestamp partial function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_utc_timestamp "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-1)to_utc_timestamp(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-3)    parse_with_dateparser=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-4)    dateparser_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-5)    unit='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-6)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-7)    tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-8)    to_fixed_offset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-9)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-5-10))
    

Alias for [to_timestamp](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timestamp "vectorbtpro.utils.datetime_.to_timestamp") with `tz="utc"`.

* * *

## auto_detect_freq function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1436-L1445 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.auto_detect_freq "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-6-1)auto_detect_freq(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-6-2)    index
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-6-3))
    

Auto-detect frequency from a datetime index.

Returns the minimal frequency if it's being encountered in most of the index.

* * *

## convert_naive_time function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L856-L860 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.convert_naive_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-7-1)convert_naive_time(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-7-2)    t,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-7-3)    tz_out
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-7-4))
    

Return as naive time.

`datetime.time` must not have `tzinfo` set.

* * *

## convert_tzaware_time function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L835-L839 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.convert_tzaware_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-8-1)convert_tzaware_time(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-8-2)    t,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-8-3)    tz_out
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-8-4))
    

Return as non-naive time.

`datetime.time` must have `tzinfo` set.

* * *

## date_range function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1259-L1324 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.date_range "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-1)date_range(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-2)    start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-3)    end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-4)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-5)    periods=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-6)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-7)    tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-8)    inclusive='left',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-9)    timestamp_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-10)    freq_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-11)    timezone_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-12)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-9-13))
    

Same as `pd.date_range` but preprocesses `start` and `end` with [to_timestamp](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timestamp "vectorbtpro.utils.datetime_.to_timestamp"), `freq` with [to_freq](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_freq "vectorbtpro.utils.datetime_.to_freq"), and `tz` with [to_timezone](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timezone "vectorbtpro.utils.datetime_.to_timezone").

If `start` and `periods` are None, will set `start` to the beginning of the Unix epoch. Same if pf `periods` is not None but `start` and `end` are None.

If `end` and `periods` are None, will set `end` to the current date and time.

* * *

## datetime_to_ms function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1189-L1192 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.datetime_to_ms "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-10-1)datetime_to_ms(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-10-2)    dt
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-10-3))
    

Convert a datetime to milliseconds.

* * *

## fix_timedelta_precision function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L497-L501 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.fix_timedelta_precision "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-11-1)fix_timedelta_precision(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-11-2)    freq
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-11-3))
    

Fix the precision of timedelta.

* * *

## freq_depends_on_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1461-L1469 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.freq_depends_on_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-12-1)freq_depends_on_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-12-2)    freq
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-12-3))
    

Return whether frequency depends on index.

* * *

## get_dt_index_gaps function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1526-L1567 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.get_dt_index_gaps "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-13-1)get_dt_index_gaps(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-13-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-13-3)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-13-4)    skip_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-13-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-13-6))
    

Get gaps in a datetime index.

Returns two indexes: start indexes (inclusive) and end indexes (exclusive).

Keyword arguments are passed to [prepare_dt_index](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.prepare_dt_index "vectorbtpro.utils.datetime_.prepare_dt_index").

* * *

## get_local_tz function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L828-L832 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.get_local_tz "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-14-1)get_local_tz(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-14-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-14-3))
    

Get local timezone.

* * *

## get_min_td_component function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1098-L1115 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.get_min_td_component "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-15-1)get_min_td_component(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-15-2)    td
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-15-3))
    

Get index of the smallest timedelta component.

* * *

## get_rangebreaks function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1570-L1573 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.get_rangebreaks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-16-1)get_rangebreaks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-16-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-16-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-16-4))
    

Get `rangebreaks` based on [get_dt_index_gaps](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.get_dt_index_gaps "vectorbtpro.utils.datetime_.get_dt_index_gaps").

* * *

## get_utc_tz function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L821-L825 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.get_utc_tz "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-17-1)get_utc_tz(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-17-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-17-3))
    

Get UTC timezone.

* * *

## infer_index_freq function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1472-L1523 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.infer_index_freq "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-18-1)infer_index_freq(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-18-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-18-3)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-18-4)    allow_offset=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-18-5)    allow_numeric=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-18-6)    freq_from_n=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-18-7))
    

Infer frequency of a datetime index if `freq` is None, otherwise convert `freq`.

If `freq` is "auto", uses [auto_detect_freq](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.auto_detect_freq "vectorbtpro.utils.datetime_.auto_detect_freq"). If `freq` is "index_[method_name]", applies the method to the `pd.TimedeltaIndex` resulting from the difference between each pair of index points. If `freq_from_n` is a positive or negative number, limits the index to the first or the last N index points respectively.

For defaults, see [datetime](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.datetime "vectorbtpro._settings.datetime").

* * *

## interval_to_ms function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1195-L1206 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.interval_to_ms "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-19-1)interval_to_ms(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-19-2)    interval
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-19-3))
    

Convert an interval string to milliseconds.

* * *

## is_tz_aware function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L863-L868 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.is_tz_aware "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-20-1)is_tz_aware(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-20-2)    dt
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-20-3))
    

Whether datetime is timezone-aware.

* * *

## naive_to_tzaware_time function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L849-L853 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.naive_to_tzaware_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-21-1)naive_to_tzaware_time(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-21-2)    t,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-21-3)    tz_out
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-21-4))
    

Return as non-naive time.

`datetime.time` must not have `tzinfo` set.

* * *

## offset_to_timedelta function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L445-L494 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.offset_to_timedelta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-22-1)offset_to_timedelta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-22-2)    offset
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-22-3))
    

Convert offset to a timedelta.

* * *

## parse_index_freq function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1448-L1458 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.parse_index_freq "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-23-1)parse_index_freq(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-23-2)    index
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-23-3))
    

Parse frequency from a datetime index.

* * *

## prepare_dt_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1327-L1406 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.prepare_dt_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-24-1)prepare_dt_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-24-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-24-3)    parse_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-24-4)    parse_with_dateparser=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-24-5)    dateparser_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-24-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-24-7))
    

Try converting an index to a datetime index.

If `parse_index` is True and the object has an object data type, will parse with Pandas (`parse_index` must be True) and dateparser (in addition `parse_with_dateparser` must be True).

`dateparser_kwargs` are passed to `dateparser.parse` while `**kwargs` are passed to `pd.to_datetime`.

For defaults, see [datetime](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.datetime "vectorbtpro._settings.datetime").

* * *

## prepare_offset_str function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L197-L395 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.prepare_offset_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-25-1)prepare_offset_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-25-2)    offset_str,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-25-3)    allow_space=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-25-4))
    

Prepare offset frequency string.

To include multiple units, separate them with comma, semicolon, or space if `allow_space` is True. The output becomes comma-separated.

* * *

## prepare_timedelta_str function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L407-L442 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.prepare_timedelta_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-26-1)prepare_timedelta_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-26-2)    timedelta_str,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-26-3)    allow_space=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-26-4))
    

Prepare timedelta frequency string.

To include multiple units, separate them with comma, semicolon, or space if `allow_space` is True. The output becomes comma-separated.

* * *

## readable_datetime function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1118-L1183 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.readable_datetime "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-27-1)readable_datetime(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-27-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-27-3)    drop_tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-27-4)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-27-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-27-6))
    

Get a human-readable datetime string.

* * *

## split_freq_str function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L131-L194 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.split_freq_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-28-1)split_freq_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-28-2)    freq_str,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-28-3)    sharp_mapping=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-28-4)    fuzzy_mapping=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-28-5))
    

Split (human-readable) frequency into multiplier and unambiguous unit.

Can be used both as offset and timedelta.

For mappings, see [sharp_freq_str_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.sharp_freq_str_config "vectorbtpro.utils.datetime_.sharp_freq_str_config") and [fuzzy_freq_str_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.fuzzy_freq_str_config "vectorbtpro.utils.datetime_.fuzzy_freq_str_config"). Sharp (case-sensitive) mappings are considered first, fuzzy (case-insensitive) mappings second. If a mapping returns None, will return the original unit.

The following case-sensitive units are returned: * "ns" for nanosecond * "us" for microsecond * "ms" for millisecond * "s" for second * "m" for minute * "h" for hour * "D" for day * "W" for week * "M" for month * "Q" for quarter * "Y" for year

If a unit isn't recognized, will return the original unit.

* * *

## time_to_timedelta function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L799-L818 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.time_to_timedelta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-29-1)time_to_timedelta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-29-2)    t,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-29-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-29-4))
    

Convert a time-like object into `pd.Timedelta`.

* * *

## to_datetime function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1064-L1070 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_datetime "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-30-1)to_datetime(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-30-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-30-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-30-4))
    

Parse the datetime as a `datetime.datetime`.

Uses [to_timestamp](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timestamp "vectorbtpro.utils.datetime_.to_timestamp").

* * *

## to_freq function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L549-L569 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_freq "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-31-1)to_freq(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-31-2)    freq,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-31-3)    allow_offset=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-31-4)    keep_offset=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-31-5))
    

Convert a frequency-like object to `pd.DateOffset` or `pd.Timedelta`.

* * *

## to_naive_datetime function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1089-L1095 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_naive_datetime "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-32-1)to_naive_datetime(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-32-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-32-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-32-4))
    

Parse the datetime as a timezone-naive `datetime.datetime`.

Uses [to_naive_timestamp](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_naive_timestamp "vectorbtpro.utils.datetime_.to_naive_timestamp").

* * *

## to_naive_timestamp function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1059-L1061 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_naive_timestamp "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-33-1)to_naive_timestamp(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-33-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-33-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-33-4))
    

Parse the datetime as a timezone-naive `pd.Timestamp`.

* * *

## to_ns function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1209-L1253 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_ns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-34-1)to_ns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-34-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-34-3)    tz_naive_ns=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-34-4))
    

Convert a datetime, timedelta, integer, or any array-like object to nanoseconds since Unix Epoch.

* * *

## to_offset function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L398-L404 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_offset "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-35-1)to_offset(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-35-2)    freq
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-35-3))
    

Convert a frequency-like object to `pd.DateOffset`.

* * *

## to_timedelta function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L504-L535 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timedelta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-36-1)to_timedelta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-36-2)    freq=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-36-3)    approximate=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-36-4))
    

Convert a frequency-like object to `pd.Timedelta`.

* * *

## to_timedelta64 function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L538-L546 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timedelta64 "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-37-1)to_timedelta64(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-37-2)    freq=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-37-3))
    

Convert a frequency-like object to `np.timedelta64`.

* * *

## to_timestamp function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L928-L1019 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timestamp "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-1)to_timestamp(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-3)    parse_with_dateparser=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-4)    dateparser_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-5)    unit='ns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-6)    tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-7)    to_fixed_offset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-38-9))
    

Parse the datetime as a `pd.Timestamp`.

If the object is a string, will parse with Pandas and dateparser (`parse_with_dateparser` must be True).

`dateparser_kwargs` are passed to `dateparser.parse` while `**kwargs` are passed to `pd.Timestamp`.

For defaults, see [datetime](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.datetime "vectorbtpro._settings.datetime").

* * *

## to_timezone function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L871-L925 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timezone "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-39-1)to_timezone(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-39-2)    tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-39-3)    to_fixed_offset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-39-4)    parse_with_dateparser=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-39-5)    dateparser_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-39-6))
    

Parse the timezone.

If the object is None, returns the local timezone. If a string, will parse with Pandas and dateparser (`parse_with_dateparser` must be True).

If `to_fixed_offset` is set to True, will convert to `datetime.timezone`. See global settings.

`dateparser_kwargs` are passed to `dateparser.parse`.

For defaults, see [datetime](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.datetime "vectorbtpro._settings.datetime").

* * *

## to_tzaware_datetime function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1080-L1086 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_tzaware_datetime "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-40-1)to_tzaware_datetime(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-40-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-40-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-40-4))
    

Parse the datetime as a timezone-aware `datetime.datetime`.

Uses [to_tzaware_timestamp](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_tzaware_timestamp "vectorbtpro.utils.datetime_.to_tzaware_timestamp").

* * *

## to_tzaware_timestamp function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1029-L1056 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_tzaware_timestamp "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-41-1)to_tzaware_timestamp(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-41-2)    dt='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-41-3)    naive_tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-41-4)    tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-41-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-41-6))
    

Parse the datetime as a timezone-aware `pd.Timestamp`.

Uses [to_timestamp](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timestamp "vectorbtpro.utils.datetime_.to_timestamp").

Raw timestamps are localized to UTC, while naive datetime is localized to `naive_tz`. Set `naive_tz` to None to use the default value defined under [datetime](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.datetime "vectorbtpro._settings.datetime"). To explicitly convert the datetime to a timezone, use `tz` (uses [to_timezone](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timezone "vectorbtpro.utils.datetime_.to_timezone")).

For defaults, see [datetime](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.datetime "vectorbtpro._settings.datetime").

* * *

## try_align_dt_to_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1422-L1433 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.try_align_dt_to_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-42-1)try_align_dt_to_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-42-2)    dt,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-42-3)    target_index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-42-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-42-5))
    

Try aligning a datetime-like object to another datetime index.

Keyword arguments are passed to [to_timestamp](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_timestamp "vectorbtpro.utils.datetime_.to_timestamp").

* * *

## try_align_to_dt_index function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L1409-L1419 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.try_align_to_dt_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-43-1)try_align_to_dt_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-43-2)    source_index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-43-3)    target_index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-43-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-43-5))
    

Try aligning an index to another datetime index.

Keyword arguments are passed to [prepare_dt_index](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.prepare_dt_index "vectorbtpro.utils.datetime_.prepare_dt_index").

* * *

## tzaware_to_naive_time function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L842-L846 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.tzaware_to_naive_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-44-1)tzaware_to_naive_time(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-44-2)    t,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-44-3)    tz_out
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-44-4))
    

Return as naive time.

`datetime.time` must have `tzinfo` set.

* * *

## DTC class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L603-L796 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-45-1)DTC(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-45-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-45-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-45-4))
    

Class representing one or more datetime components.

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

### day field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.day "Permanent link")

Day of month.

* * *

### from_date class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L652-L655 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.from_date "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-46-1)DTC.from_date(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-46-2)    d
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-46-3))
    

Get [DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "vectorbtpro.utils.datetime_.DTC") instance from a `datetime.date` object.

* * *

### from_datetime class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L631-L650 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.from_datetime "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-47-1)DTC.from_datetime(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-47-2)    dt
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-47-3))
    

Get [DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "vectorbtpro.utils.datetime_.DTC") instance from a `datetime.datetime` object.

* * *

### from_namedtuple class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L683-L695 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.from_namedtuple "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-48-1)DTC.from_namedtuple(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-48-2)    dtc
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-48-3))
    

Get [DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "vectorbtpro.utils.datetime_.DTC") instance from a named tuple of the type [DTCNT](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT "vectorbtpro.utils.datetime_.DTCNT").

* * *

### from_time class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L657-L660 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.from_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-49-1)DTC.from_time(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-49-2)    t
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-49-3))
    

Get [DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "vectorbtpro.utils.datetime_.DTC") instance from a `datetime.time` object.

* * *

### has_date method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L739-L741 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.has_date "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-50-1)DTC.has_date()
    

Whether any date component is set.

* * *

### has_full_date method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L743-L745 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.has_full_date "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-51-1)DTC.has_full_date()
    

Whether all date components are set.

* * *

### has_full_datetime method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L766-L768 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.has_full_datetime "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-52-1)DTC.has_full_datetime()
    

Whether all components are set.

* * *

### has_full_time method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L757-L764 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.has_full_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-53-1)DTC.has_full_time()
    

Whether all time components are set.

* * *

### has_time method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L751-L755 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.has_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-54-1)DTC.has_time()
    

Whether any time component is set.

* * *

### has_weekday method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L747-L749 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.has_weekday "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-55-1)DTC.has_weekday()
    

Whether the weekday component is set.

* * *

### hour field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.hour "Permanent link")

Hour.

* * *

### is_not_none method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L770-L772 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.is_not_none "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-56-1)DTC.is_not_none()
    

Check whether any component is set.

* * *

### is_parsable class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L720-L737 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.is_parsable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-57-1)DTC.is_parsable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-57-2)    dtc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-57-3)    check_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-57-4)    **parse_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-57-5))
    

Check whether a datetime-component-like object is parsable.

* * *

### minute field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.minute "Permanent link")

Minute.

* * *

### month field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.month "Permanent link")

Month.

* * *

### nanosecond field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.nanosecond "Permanent link")

Nanosecond.

* * *

### parse class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L697-L718 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.parse "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-58-1)DTC.parse(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-58-2)    dtc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-58-3)    **parse_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-58-4))
    

Parse [DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "vectorbtpro.utils.datetime_.DTC") instance from a datetime-component-like object.

* * *

### parse_time_str class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L662-L681 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.parse_time_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-59-1)DTC.parse_time_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-59-2)    time_str,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-59-3)    **parse_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-59-4))
    

Parse [DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "vectorbtpro.utils.datetime_.DTC") instance from a time string.

* * *

### second field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.second "Permanent link")

Second.

* * *

### to_namedtuple method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L785-L796 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.to_namedtuple "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-60-1)DTC.to_namedtuple()
    

Convert to a named tuple.

* * *

### to_time method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py#L774-L783 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.to_time "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-61-1)DTC.to_time()
    

Convert to a `datetime.time` instance.

Fields that are None will become 0.

* * *

### weekday field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.weekday "Permanent link")

Day of week.

* * *

### year field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC.year "Permanent link")

Year.

* * *

## DTCNT class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-1)DTCNT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-2)    year='year',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-3)    month='month',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-4)    day='day',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-5)    weekday='weekday',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-6)    hour='hour',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-7)    minute='minute',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-8)    second='second',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-9)    nanosecond='nanosecond'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#__codelineno-62-10))
    

A named tuple version of [DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC "vectorbtpro.utils.datetime_.DTC").

**Superclasses**

  * `builtins.tuple`



* * *

### day field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT.day "Permanent link")

Alias for field number 2

* * *

### hour field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT.hour "Permanent link")

Alias for field number 4

* * *

### minute field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT.minute "Permanent link")

Alias for field number 5

* * *

### month field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT.month "Permanent link")

Alias for field number 1

* * *

### nanosecond field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT.nanosecond "Permanent link")

Alias for field number 7

* * *

### second field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT.second "Permanent link")

Alias for field number 6

* * *

### weekday field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT.weekday "Permanent link")

Alias for field number 3

* * *

### year field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/datetime_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTCNT.year "Permanent link")

Alias for field number 0
