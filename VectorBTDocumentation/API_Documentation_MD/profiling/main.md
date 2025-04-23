profiling

#  profiling module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling "Permanent link")

Utilities for profiling time and memory.

* * *

## timeit function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L132-L158 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.timeit "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-0-1)timeit(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-0-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-0-3)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-0-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-0-5))
    

Run [timeit](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.timeit "vectorbtpro.utils.profiling.timeit") on a function.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-3)>>> def my_func():
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-4)...     sleep(1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-6)>>> elapsed = vbt.timeit(my_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-7)>>> print(elapsed)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-8)1.01 seconds
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-10)>>> vbt.timeit(my_func, readable=False)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-1-11)datetime.timedelta(seconds=1, microseconds=1870)
    

* * *

## with_memtracer function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L257-L299 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.with_memtracer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-2-1)with_memtracer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-2-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-2-3)    memtracer_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-2-4)    usage_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-2-5)    print_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-2-6)    print_format=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-2-7)    print_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-2-8))
    

Decorator to run a function with [MemTracer](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.MemTracer "vectorbtpro.utils.profiling.MemTracer").

* * *

## with_timeit function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L161-L198 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.with_timeit "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-3-1)with_timeit(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-3-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-3-3)    timeit_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-3-4)    print_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-3-5)    print_format=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-3-6)    print_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-3-7))
    

Decorator to run a function with [timeit](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.timeit "vectorbtpro.utils.profiling.timeit").

* * *

## with_timer function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L87-L129 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.with_timer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-4-1)with_timer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-4-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-4-3)    timer_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-4-4)    elapsed_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-4-5)    print_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-4-6)    print_format=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-4-7)    print_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-4-8))
    

Decorator to run a function with [Timer](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.Timer "vectorbtpro.utils.profiling.Timer").

* * *

## MemTracer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L201-L254 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.MemTracer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-5-1)MemTracer()
    

Context manager to trace peak and final memory usage using `tracemalloc`.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-3)>>> with vbt.MemTracer() as tracer:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-4)>>>     np.random.uniform(size=1000000)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-6)>>> print(tracer.peak_usage())
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-7)8.0 MB
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-9)>>> tracer.peak_usage(readable=False)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-6-10)8005360
    

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### final_usage method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L223-L233 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.MemTracer.final_usage "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-7-1)MemTracer.final_usage(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-7-2)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-7-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-7-4))
    

Get final memory usage.

`**kwargs` are passed to `humanize.naturalsize`.

* * *

### peak_usage method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L235-L245 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.MemTracer.peak_usage "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-8-1)MemTracer.peak_usage(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-8-2)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-8-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-8-4))
    

Get peak memory usage.

`**kwargs` are passed to `humanize.naturalsize`.

* * *

## Timer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L33-L84 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.Timer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-9-1)Timer()
    

Context manager to measure execution time using [timeit](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.timeit "vectorbtpro.utils.profiling.timeit").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-3)>>> with vbt.Timer() as timer:
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-4)>>>     sleep(1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-6)>>> print(timer.elapsed())
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-7)1.01 seconds
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-9)>>> timer.elapsed(readable=False)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-10-10)datetime.timedelta(seconds=1, microseconds=5110)
    

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### elapsed method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L67-L77 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.Timer.elapsed "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-11-1)Timer.elapsed(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-11-2)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-11-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#__codelineno-11-4))
    

Get elapsed time.

`**kwargs` are passed to `humanize.precisedelta`.

* * *

### end_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L60-L65 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.Timer.end_time "Permanent link")

End time.

* * *

### start_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/profiling.py#L55-L58 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.Timer.start_time "Permanent link")

Start time.
