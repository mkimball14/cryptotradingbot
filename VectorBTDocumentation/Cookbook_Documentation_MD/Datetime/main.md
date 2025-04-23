# Datetime[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#datetime "Permanent link")

VBT loves flexibility, and so it allows us to construct various datetime-related objects from human-readable strings.


# Timestamps[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#timestamps "Permanent link")

Timestamps represent a single point in time, similar to a datetime object in Python's `datetime` module, but with enhanced functionality for data analysis and manipulation.

How to construct a timestamp
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-0-1)vbt.timestamp() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-0-2)vbt.utc_timestamp() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-0-3)vbt.local_timestamp() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-0-4)vbt.timestamp(tz="America/New_York") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-0-5)vbt.timestamp("1 Jul 2020") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-0-6)vbt.timestamp("7 days ago") 
 
[/code]

 1. 2. 3. 4. 5. 6. 


# Timezones[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#timezones "Permanent link")

Timezones can be used in timestamps, making it a powerful tool for global time-based data analysis.

How to construct a timezone
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-1-1)vbt.timezone() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-1-2)vbt.timezone("utc") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-1-3)vbt.timezone("America/New_York") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-1-4)vbt.timezone("+0500") 
 
[/code]

 1. 2. 3. 4. 


# Timedeltas[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#timedeltas "Permanent link")

Timedeltas deal with continuous time spans and precise time differences. They are commonly used for adding or subtracting durations from timestamps, or for measuring the difference between two timestamps.

How to construct a timedelta
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-2-1)vbt.timedelta() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-2-2)vbt.timedelta("7 days") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-2-3)vbt.timedelta("weekly")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-2-4)vbt.timedelta("Y", approximate=True) 
 
[/code]

 1. 2. 3. 


# Date offsets[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#date-offsets "Permanent link")

Date offsets handle calendar-specific offsets (e.g., adding a month, skipping weekends with business days). They are commonly used for calendar-aware adjustments and recurring periods.

How to construct a date offset
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-3-1)vbt.offset("Y") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-3-2)vbt.offset("YE") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-3-3)vbt.offset("weekstart") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-3-4)vbt.offset("monday")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/datetime/#__codelineno-3-5)vbt.offset("july") 
 
[/code]

 1. 2. 3. 4.