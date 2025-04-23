scheduling updater

#  updater module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/updater.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater "Permanent link")

Classes for scheduling data updates.

* * *

## DataUpdater class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/updater.py#L27-L123 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-0-1)DataUpdater(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-0-2)    data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-0-3)    schedule_manager=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-0-4)    update_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-0-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-0-6))
    

Base class for scheduling data updates.

**Args**

**`data`** : `Data`
    Data instance.
**`update_kwargs`** : `dict`
    Default keyword arguments for `DataSaver.update`.
**`**kwargs`**
    Keyword arguments passed to the constructor of `Configured`.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Configured.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Configured.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Configured.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Configured.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Configured.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Configured.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.config.Configured.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.config.Configured.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.config.Configured.pipe")
  * [Configured.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.config.Configured.config")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.config.Configured.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.config.Configured.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.config.Configured.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Configured.prettify")
  * [Configured.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Configured.rec_state")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.config.Configured.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.config.Configured.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.config.Configured.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.config.Configured.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.config.Configured.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.config.Configured.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.config.Configured.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.config.Configured.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.config.Configured.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.config.Configured.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.config.Configured.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.config.Configured.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.config.Configured.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.config.Configured.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.config.Configured.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Configured.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Configured.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Configured.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Configured.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Configured.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Configured.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Configured.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Configured.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Configured.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Configured.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Configured.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Configured.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Configured.pprint")



**Subclasses**

  * [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver")



* * *

### data class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/updater.py#L57-L62 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.data "Permanent link")

Data instance.

See [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data "vectorbtpro.data.base.Data").

* * *

### schedule_manager class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/updater.py#L64-L69 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.schedule_manager "Permanent link")

Schedule manager instance.

See [ScheduleManager](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager "vectorbtpro.utils.schedule_.ScheduleManager").

* * *

### update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/updater.py#L76-L88 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-1-1)DataUpdater.update(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-1-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-1-3))
    

Method that updates data.

Override to do pre- and postprocessing.

To stop this method from running again, raise [CancelledError](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CancelledError "vectorbtpro.utils.schedule_.CancelledError").

* * *

### update_every method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/updater.py#L90-L123 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update_every "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-1)DataUpdater.update_every(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-3)    to=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-4)    tags=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-5)    in_background=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-6)    replace=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-7)    start=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-8)    start_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-9)    **update_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#__codelineno-2-10))
    

Schedule [DataUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update "vectorbtpro.data.updater.DataUpdater.update") as a job.

For `*args`, `to` and `tags`, see [ScheduleManager.every](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.every "vectorbtpro.utils.schedule_.ScheduleManager.every").

If `in_background` is set to True, starts in the background as an `asyncio` task. The task can be stopped with [ScheduleManager.stop](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager.stop "vectorbtpro.utils.schedule_.ScheduleManager.stop").

If `replace` is True, will delete scheduled jobs with the same tags, or all jobs if tags are omitted.

If `start` is False, will add the job to the scheduler without starting.

`**update_kwargs` are merged over [DataUpdater.update_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update_kwargs "vectorbtpro.data.updater.DataUpdater.update_kwargs") and passed to [DataUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update "vectorbtpro.data.updater.DataUpdater.update").

* * *

### update_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/updater.py#L71-L74 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update_kwargs "Permanent link")

Keyword arguments passed to `DataSaver.update`.
