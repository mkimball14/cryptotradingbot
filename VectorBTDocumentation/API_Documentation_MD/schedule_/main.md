schedule_ scheduling

#  schedule_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_ "Permanent link")

Utilities for scheduling jobs.

* * *

## AsyncJob class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L105-L116 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncJob "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-0-1)AsyncJob(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-0-2)    interval,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-0-3)    scheduler=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-0-4))
    

Async [CustomJob](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob "vectorbtpro.utils.schedule_.CustomJob").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CustomJob](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob "vectorbtpro.utils.schedule_.CustomJob")
  * `schedule.Job`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.schedule_.CustomJob.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.schedule_.CustomJob.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.schedule_.CustomJob.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.schedule_.CustomJob.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.schedule_.CustomJob.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.schedule_.CustomJob.find_messages")
  * [CustomJob.force_missed_run](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob.force_missed_run "vectorbtpro.utils.schedule_.CustomJob.force_missed_run")
  * [CustomJob.modulo](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob.modulo "vectorbtpro.utils.schedule_.CustomJob.modulo")
  * [CustomJob.zero_offset](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob.zero_offset "vectorbtpro.utils.schedule_.CustomJob.zero_offset")



* * *

### async_run method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L108-L116 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncJob.async_run "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-1-1)AsyncJob.async_run()
    

Async `CustomJob.run`.

* * *

## AsyncScheduler class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L119-L143 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncScheduler "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-2-1)AsyncScheduler()
    

Async [CustomScheduler](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomScheduler "vectorbtpro.utils.schedule_.CustomScheduler").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CustomScheduler](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomScheduler "vectorbtpro.utils.schedule_.CustomScheduler")
  * `schedule.Scheduler`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.schedule_.CustomScheduler.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.schedule_.CustomScheduler.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.schedule_.CustomScheduler.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.schedule_.CustomScheduler.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.schedule_.CustomScheduler.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.schedule_.CustomScheduler.find_messages")



* * *

### async_run_all method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L127-L132 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncScheduler.async_run_all "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-3-1)AsyncScheduler.async_run_all(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-3-2)    delay_seconds=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-3-3))
    

Async `CustomScheduler.run_all`.

* * *

### async_run_pending method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L122-L125 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncScheduler.async_run_pending "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-4-1)AsyncScheduler.async_run_pending()
    

Async `CustomScheduler.run_pending`.

* * *

### every method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L140-L143 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncScheduler.every "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-5-1)AsyncScheduler.every(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-5-2)    interval=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-5-3))
    

Schedule a new periodic job of type [AsyncJob](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncJob "vectorbtpro.utils.schedule_.AsyncJob").

* * *

## CancelledError class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L99-L102 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CancelledError "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-6-1)CancelledError(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-6-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-6-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-6-4))
    

Thrown for the operation to be cancelled.

**Superclasses**

  * `asyncio.exceptions.CancelledError`
  * `builtins.BaseException`



* * *

## CustomJob class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L46-L96 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-7-1)CustomJob(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-7-2)    interval,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-7-3)    scheduler=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-7-4))
    

Custom job.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `schedule.Job`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



**Subclasses**

  * [AsyncJob](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncJob "vectorbtpro.utils.schedule_.AsyncJob")



* * *

### force_missed_run class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L61-L65 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob.force_missed_run "Permanent link")

Set whether to force a missed run.

* * *

### modulo class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L67-L77 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob.modulo "Permanent link")

Module based on the next run's unit and interval.

* * *

### zero_offset class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L55-L59 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob.zero_offset "Permanent link")

Set offset to zero.

* * *

## CustomScheduler class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L36-L40 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomScheduler "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-8-1)CustomScheduler()
    

Custom scheduler.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `schedule.Scheduler`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



**Subclasses**

  * [AsyncScheduler](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.AsyncScheduler "vectorbtpro.utils.schedule_.AsyncScheduler")



* * *

## ScheduleManager class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L146-L400 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-9-1)ScheduleManager(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-9-2)    scheduler=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-9-3))
    

Class that manages [CustomScheduler](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomScheduler "vectorbtpro.utils.schedule_.CustomScheduler").

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

### async_start method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L359-L370 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.async_start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-10-1)ScheduleManager.async_start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-10-2)    sleep=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-10-3)    clear_after=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-10-4))
    

Async run pending jobs in a loop.

* * *

### async_task class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L187-L190 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.async_task "Permanent link")

Current async task.

* * *

### async_task_running class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L383-L386 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.async_task_running "Permanent link")

Whether the async task is running.

* * *

### clear_jobs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L393-L400 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.clear_jobs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-11-1)ScheduleManager.clear_jobs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-11-2)    tags=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-11-3))
    

Delete scheduled jobs with the given tags, or all jobs if tag is omitted.

* * *

### done_callback method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L372-L374 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.done_callback "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-12-1)ScheduleManager.done_callback(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-12-2)    async_task
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-12-3))
    

Callback run when the async task is finished.

* * *

### every method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L192-L345 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.every "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-13-1)ScheduleManager.every(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-13-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-13-3)    to=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-13-4)    zero_offset=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-13-5)    force_missed_run=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-13-6)    tags=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-13-7))
    

Create a new job that runs every `interval` units of time.

`*args` can include at most four different arguments: `interval`, `unit`, `start_day`, and `at`, in the strict order:

  * `interval`: integer or `datetime.timedelta`
  * `unit`: [ScheduleManager.units](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.units "vectorbtpro.utils.schedule_.ScheduleManager.units")
  * `start_day`: [ScheduleManager.weekdays](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.weekdays "vectorbtpro.utils.schedule_.ScheduleManager.weekdays")
  * `at`: string or `datetime.time`.



See the package `schedule` for more details.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-3)>>> def job_func(message="I'm working..."):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-4)...     print(message)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-6)>>> my_manager = vbt.ScheduleManager()
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-8)>>> # add jobs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-9)>>> my_manager.every().do(job_func, message="Hello")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-10)Every 1 second do job_func(message='Hello') (last run: [never], next run: 2021-03-18 19:06:47)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-12)>>> my_manager.every(10, 'minutes').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-13)Every 10 minutes do job_func() (last run: [never], next run: 2021-03-18 19:16:46)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-15)>>> my_manager.every(10, 'minutes', ':00', zero_offset=True).do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-16)Every 10 minutes at 00:00:00 do job_func() (last run: [never], next run: 2022-08-18 16:10:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-17)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-18)>>> my_manager.every('hour').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-19)Every 1 hour do job_func() (last run: [never], next run: 2021-03-18 20:06:46)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-21)>>> my_manager.every('hour', '00:00').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-22)Every 1 hour at 00:00:00 do job_func() (last run: [never], next run: 2021-03-18 20:00:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-23)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-24)>>> my_manager.every(4, 'hours', '00:00').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-25)Every 4 hours at 00:00:00 do job_func() (last run: [never], next run: 2021-03-19 00:00:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-27)>>> my_manager.every('10:30').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-28)Every 1 day at 10:30:00 do job_func() (last run: [never], next run: 2021-03-19 10:30:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-29)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-30)>>> my_manager.every('hour', '00:00').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-31)Every 1 hour at 00:00:00 do job_func() (last run: [never], next run: 2021-03-19 10:30:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-32)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-33)>>> my_manager.every(4, 'hour', '00:00').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-34)Every 4 hours at 00:00:00 do job_func() (last run: [never], next run: 2021-03-19 10:30:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-35)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-36)>>> my_manager.every('day', '10:30').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-37)Every 1 day at 10:30:00 do job_func() (last run: [never], next run: 2021-03-19 10:30:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-38)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-39)>>> my_manager.every('day', time(9, 30, tzinfo="utc")).do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-40)Every 1 day at 10:30:00 do job_func() (last run: [never], next run: 2021-03-19 10:30:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-41)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-42)>>> my_manager.every('monday').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-43)Every 1 week do job_func() (last run: [never], next run: 2021-03-22 19:06:46)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-44)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-45)>>> my_manager.every('wednesday', '13:15').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-46)Every 1 week at 13:15:00 do job_func() (last run: [never], next run: 2021-03-24 13:15:00)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-47)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-48)>>> my_manager.every('minute', ':17').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-49)Every 1 minute at 00:00:17 do job_func() (last run: [never], next run: 2021-03-18 19:07:17)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-50)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-14-51)>>> my_manager.start()
    

You can still use the chained approach as done by `schedule`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-15-1)>>> my_manager.every().minute.at(':17').do(job_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-15-2)Every 1 minute at 00:00:17 do job_func() (last run: [never], next run: 2021-03-18 19:07:17)
    

* * *

### scheduler class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L182-L185 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.scheduler "Permanent link")

Scheduler.

* * *

### start method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L347-L357 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-16-1)ScheduleManager.start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-16-2)    sleep=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-16-3)    clear_after=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-16-4))
    

Run pending jobs in a loop.

* * *

### start_in_background method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L376-L381 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.start_in_background "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-17-1)ScheduleManager.start_in_background(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-17-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-17-3))
    

Run [ScheduleManager.async_start](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.async_start "vectorbtpro.utils.schedule_.ScheduleManager.async_start") in the background.

* * *

### stop method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py#L388-L391 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.stop "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#__codelineno-18-1)ScheduleManager.stop()
    

Stop the async task.

* * *

### units tuple[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.units "Permanent link")

Units.

* * *

### weekdays tuple[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/schedule_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.weekdays "Permanent link")

Weekdays.
