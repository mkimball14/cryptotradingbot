saver scheduling

#  saver module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver "Permanent link")

Classes for scheduling data saves.

* * *

## CSVDataSaver class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L122-L151 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.CSVDataSaver "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-0-1)CSVDataSaver(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-0-2)    data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-0-3)    save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-0-4)    init_save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-0-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-0-6))
    

Subclass of [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver") for saving data with [Data.to_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_csv "vectorbtpro.data.base.Data.to_csv").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver")
  * [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "vectorbtpro.data.updater.DataUpdater")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.data.saver.DataSaver.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.data.saver.DataSaver.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.data.saver.DataSaver.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.data.saver.DataSaver.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.data.saver.DataSaver.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.data.saver.DataSaver.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.data.saver.DataSaver.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.data.saver.DataSaver.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.data.saver.DataSaver.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.data.saver.DataSaver.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.data.saver.DataSaver.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.data.saver.DataSaver.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.data.saver.DataSaver.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.data.saver.DataSaver.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.data.saver.DataSaver.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.data.saver.DataSaver.update_config")
  * [DataSaver.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.data.saver.DataSaver.config")
  * [DataSaver.data](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.data "vectorbtpro.data.saver.DataSaver.data")
  * [DataSaver.init_save_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_kwargs "vectorbtpro.data.saver.DataSaver.init_save_kwargs")
  * [DataSaver.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.data.saver.DataSaver.rec_state")
  * [DataSaver.save_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_kwargs "vectorbtpro.data.saver.DataSaver.save_kwargs")
  * [DataSaver.schedule_manager](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.schedule_manager "vectorbtpro.data.saver.DataSaver.schedule_manager")
  * [DataSaver.update](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update "vectorbtpro.data.saver.DataSaver.update")
  * [DataSaver.update_every](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update_every "vectorbtpro.data.saver.DataSaver.update_every")
  * [DataSaver.update_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update_kwargs "vectorbtpro.data.saver.DataSaver.update_kwargs")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.data.saver.DataSaver.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.data.saver.DataSaver.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.data.saver.DataSaver.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.data.saver.DataSaver.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.data.saver.DataSaver.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.data.saver.DataSaver.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.data.saver.DataSaver.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.data.saver.DataSaver.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.data.saver.DataSaver.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.data.saver.DataSaver.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.data.saver.DataSaver.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.data.saver.DataSaver.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.data.saver.DataSaver.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.data.saver.DataSaver.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.data.saver.DataSaver.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.data.saver.DataSaver.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.data.saver.DataSaver.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.data.saver.DataSaver.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.data.saver.DataSaver.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.data.saver.DataSaver.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.data.saver.DataSaver.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.data.saver.DataSaver.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.data.saver.DataSaver.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.data.saver.DataSaver.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.data.saver.DataSaver.pprint")



* * *

### init_save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L125-L136 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.CSVDataSaver.init_save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-1-1)CSVDataSaver.init_save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-1-2)    **to_csv_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-1-3))
    

Save initial data.

* * *

### save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L138-L151 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.CSVDataSaver.save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-2-1)CSVDataSaver.save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-2-2)    **to_csv_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-2-3))
    

Save data.

By default, appends new data without header.

* * *

## DataSaver class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L31-L119 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-3-1)DataSaver(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-3-2)    data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-3-3)    save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-3-4)    init_save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-3-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-3-6))
    

Base class for scheduling data saves.

Subclasses [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "vectorbtpro.data.updater.DataUpdater").

**Args**

**`data`** : `Data`
    Data instance.
**`save_kwargs`** : `dict`
    Default keyword arguments for [DataSaver.init_save_data](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_data "vectorbtpro.data.saver.DataSaver.init_save_data") and [DataSaver.save_data](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_data "vectorbtpro.data.saver.DataSaver.save_data").
**`init_save_kwargs`** : `dict`
    Default keyword arguments overriding `save_kwargs` for [DataSaver.init_save_data](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_data "vectorbtpro.data.saver.DataSaver.init_save_data").
**`**kwargs`**
    Keyword arguments passed to the constructor of `DataUpdater`.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "vectorbtpro.data.updater.DataUpdater")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.data.updater.DataUpdater.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.data.updater.DataUpdater.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.data.updater.DataUpdater.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.data.updater.DataUpdater.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.data.updater.DataUpdater.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.data.updater.DataUpdater.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.data.updater.DataUpdater.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.data.updater.DataUpdater.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.data.updater.DataUpdater.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.data.updater.DataUpdater.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.data.updater.DataUpdater.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.data.updater.DataUpdater.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.data.updater.DataUpdater.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.data.updater.DataUpdater.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.data.updater.DataUpdater.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.data.updater.DataUpdater.update_config")
  * [DataUpdater.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.data.updater.DataUpdater.config")
  * [DataUpdater.data](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.data "vectorbtpro.data.updater.DataUpdater.data")
  * [DataUpdater.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.data.updater.DataUpdater.rec_state")
  * [DataUpdater.schedule_manager](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.schedule_manager "vectorbtpro.data.updater.DataUpdater.schedule_manager")
  * [DataUpdater.update_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update_kwargs "vectorbtpro.data.updater.DataUpdater.update_kwargs")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.data.updater.DataUpdater.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.data.updater.DataUpdater.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.data.updater.DataUpdater.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.data.updater.DataUpdater.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.data.updater.DataUpdater.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.data.updater.DataUpdater.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.data.updater.DataUpdater.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.data.updater.DataUpdater.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.data.updater.DataUpdater.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.data.updater.DataUpdater.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.data.updater.DataUpdater.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.data.updater.DataUpdater.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.data.updater.DataUpdater.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.data.updater.DataUpdater.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.data.updater.DataUpdater.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.data.updater.DataUpdater.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.data.updater.DataUpdater.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.data.updater.DataUpdater.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.data.updater.DataUpdater.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.data.updater.DataUpdater.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.data.updater.DataUpdater.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.data.updater.DataUpdater.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.data.updater.DataUpdater.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.data.updater.DataUpdater.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.data.updater.DataUpdater.pprint")



**Subclasses**

  * [CSVDataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.CSVDataSaver "vectorbtpro.data.saver.CSVDataSaver")
  * [DuckDBDataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DuckDBDataSaver "vectorbtpro.data.saver.DuckDBDataSaver")
  * [HDFDataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.HDFDataSaver "vectorbtpro.data.saver.HDFDataSaver")
  * [SQLDataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.SQLDataSaver "vectorbtpro.data.saver.SQLDataSaver")



* * *

### init_save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L70-L74 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-4-1)DataSaver.init_save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-4-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-4-3))
    

Save initial data.

This is an abstract method - override it to define custom logic.

* * *

### init_save_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L65-L68 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_kwargs "Permanent link")

Keyword arguments passed to [DataSaver.init_save_data](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_data "vectorbtpro.data.saver.DataSaver.init_save_data").

* * *

### save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L76-L80 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-5-1)DataSaver.save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-5-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-5-3))
    

Save data.

This is an abstract method - override it to define custom logic.

* * *

### save_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L60-L63 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_kwargs "Permanent link")

Keyword arguments passed to [DataSaver.save_data](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_data "vectorbtpro.data.saver.DataSaver.save_data").

* * *

### update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L82-L100 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-6-1)DataSaver.update(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-6-2)    save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-6-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-6-4))
    

Update and save data using [DataSaver.save_data](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_data "vectorbtpro.data.saver.DataSaver.save_data").

Override to do pre- and postprocessing.

To stop this method from running again, raise [CancelledError](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CancelledError "vectorbtpro.utils.schedule_.CancelledError").

* * *

### update_every method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L102-L119 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update_every "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-7-1)DataSaver.update_every(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-7-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-7-3)    save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-7-4)    init_save=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-7-5)    init_save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-7-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-7-7))
    

Overrides [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "vectorbtpro.data.updater.DataUpdater") to save initial data prior to updating.

* * *

## DuckDBDataSaver class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L218-L247 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DuckDBDataSaver "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-8-1)DuckDBDataSaver(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-8-2)    data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-8-3)    save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-8-4)    init_save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-8-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-8-6))
    

Subclass of [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver") for saving data with [Data.to_duckdb](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_duckdb "vectorbtpro.data.base.Data.to_duckdb").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver")
  * [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "vectorbtpro.data.updater.DataUpdater")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.data.saver.DataSaver.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.data.saver.DataSaver.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.data.saver.DataSaver.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.data.saver.DataSaver.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.data.saver.DataSaver.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.data.saver.DataSaver.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.data.saver.DataSaver.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.data.saver.DataSaver.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.data.saver.DataSaver.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.data.saver.DataSaver.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.data.saver.DataSaver.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.data.saver.DataSaver.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.data.saver.DataSaver.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.data.saver.DataSaver.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.data.saver.DataSaver.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.data.saver.DataSaver.update_config")
  * [DataSaver.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.data.saver.DataSaver.config")
  * [DataSaver.data](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.data "vectorbtpro.data.saver.DataSaver.data")
  * [DataSaver.init_save_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_kwargs "vectorbtpro.data.saver.DataSaver.init_save_kwargs")
  * [DataSaver.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.data.saver.DataSaver.rec_state")
  * [DataSaver.save_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_kwargs "vectorbtpro.data.saver.DataSaver.save_kwargs")
  * [DataSaver.schedule_manager](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.schedule_manager "vectorbtpro.data.saver.DataSaver.schedule_manager")
  * [DataSaver.update](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update "vectorbtpro.data.saver.DataSaver.update")
  * [DataSaver.update_every](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update_every "vectorbtpro.data.saver.DataSaver.update_every")
  * [DataSaver.update_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update_kwargs "vectorbtpro.data.saver.DataSaver.update_kwargs")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.data.saver.DataSaver.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.data.saver.DataSaver.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.data.saver.DataSaver.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.data.saver.DataSaver.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.data.saver.DataSaver.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.data.saver.DataSaver.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.data.saver.DataSaver.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.data.saver.DataSaver.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.data.saver.DataSaver.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.data.saver.DataSaver.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.data.saver.DataSaver.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.data.saver.DataSaver.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.data.saver.DataSaver.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.data.saver.DataSaver.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.data.saver.DataSaver.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.data.saver.DataSaver.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.data.saver.DataSaver.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.data.saver.DataSaver.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.data.saver.DataSaver.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.data.saver.DataSaver.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.data.saver.DataSaver.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.data.saver.DataSaver.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.data.saver.DataSaver.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.data.saver.DataSaver.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.data.saver.DataSaver.pprint")



* * *

### init_save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L221-L232 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DuckDBDataSaver.init_save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-9-1)DuckDBDataSaver.init_save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-9-2)    **to_duckdb_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-9-3))
    

Save initial data.

* * *

### save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L234-L247 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DuckDBDataSaver.save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-10-1)DuckDBDataSaver.save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-10-2)    **to_duckdb_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-10-3))
    

Save data.

By default, appends new data without header.

* * *

## HDFDataSaver class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L154-L183 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.HDFDataSaver "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-11-1)HDFDataSaver(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-11-2)    data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-11-3)    save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-11-4)    init_save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-11-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-11-6))
    

Subclass of [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver") for saving data with [Data.to_hdf](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_hdf "vectorbtpro.data.base.Data.to_hdf").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver")
  * [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "vectorbtpro.data.updater.DataUpdater")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.data.saver.DataSaver.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.data.saver.DataSaver.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.data.saver.DataSaver.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.data.saver.DataSaver.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.data.saver.DataSaver.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.data.saver.DataSaver.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.data.saver.DataSaver.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.data.saver.DataSaver.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.data.saver.DataSaver.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.data.saver.DataSaver.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.data.saver.DataSaver.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.data.saver.DataSaver.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.data.saver.DataSaver.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.data.saver.DataSaver.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.data.saver.DataSaver.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.data.saver.DataSaver.update_config")
  * [DataSaver.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.data.saver.DataSaver.config")
  * [DataSaver.data](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.data "vectorbtpro.data.saver.DataSaver.data")
  * [DataSaver.init_save_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_kwargs "vectorbtpro.data.saver.DataSaver.init_save_kwargs")
  * [DataSaver.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.data.saver.DataSaver.rec_state")
  * [DataSaver.save_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_kwargs "vectorbtpro.data.saver.DataSaver.save_kwargs")
  * [DataSaver.schedule_manager](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.schedule_manager "vectorbtpro.data.saver.DataSaver.schedule_manager")
  * [DataSaver.update](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update "vectorbtpro.data.saver.DataSaver.update")
  * [DataSaver.update_every](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update_every "vectorbtpro.data.saver.DataSaver.update_every")
  * [DataSaver.update_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update_kwargs "vectorbtpro.data.saver.DataSaver.update_kwargs")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.data.saver.DataSaver.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.data.saver.DataSaver.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.data.saver.DataSaver.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.data.saver.DataSaver.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.data.saver.DataSaver.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.data.saver.DataSaver.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.data.saver.DataSaver.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.data.saver.DataSaver.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.data.saver.DataSaver.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.data.saver.DataSaver.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.data.saver.DataSaver.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.data.saver.DataSaver.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.data.saver.DataSaver.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.data.saver.DataSaver.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.data.saver.DataSaver.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.data.saver.DataSaver.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.data.saver.DataSaver.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.data.saver.DataSaver.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.data.saver.DataSaver.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.data.saver.DataSaver.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.data.saver.DataSaver.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.data.saver.DataSaver.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.data.saver.DataSaver.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.data.saver.DataSaver.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.data.saver.DataSaver.pprint")



* * *

### init_save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L157-L168 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.HDFDataSaver.init_save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-12-1)HDFDataSaver.init_save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-12-2)    **to_hdf_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-12-3))
    

Save initial data.

* * *

### save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L170-L183 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.HDFDataSaver.save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-13-1)HDFDataSaver.save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-13-2)    **to_hdf_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-13-3))
    

Save data.

By default, appends new data in a table format.

* * *

## SQLDataSaver class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L186-L215 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.SQLDataSaver "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-14-1)SQLDataSaver(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-14-2)    data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-14-3)    save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-14-4)    init_save_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-14-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-14-6))
    

Subclass of [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver") for saving data with [Data.to_sql](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_sql "vectorbtpro.data.base.Data.to_sql").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver "vectorbtpro.data.saver.DataSaver")
  * [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater "vectorbtpro.data.updater.DataUpdater")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.data.saver.DataSaver.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.data.saver.DataSaver.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.data.saver.DataSaver.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.data.saver.DataSaver.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.data.saver.DataSaver.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.data.saver.DataSaver.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.data.saver.DataSaver.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.data.saver.DataSaver.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.data.saver.DataSaver.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.data.saver.DataSaver.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.data.saver.DataSaver.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.data.saver.DataSaver.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.data.saver.DataSaver.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.data.saver.DataSaver.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.data.saver.DataSaver.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.data.saver.DataSaver.update_config")
  * [DataSaver.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.data.saver.DataSaver.config")
  * [DataSaver.data](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.data "vectorbtpro.data.saver.DataSaver.data")
  * [DataSaver.init_save_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.init_save_kwargs "vectorbtpro.data.saver.DataSaver.init_save_kwargs")
  * [DataSaver.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.data.saver.DataSaver.rec_state")
  * [DataSaver.save_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.save_kwargs "vectorbtpro.data.saver.DataSaver.save_kwargs")
  * [DataSaver.schedule_manager](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.schedule_manager "vectorbtpro.data.saver.DataSaver.schedule_manager")
  * [DataSaver.update](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update "vectorbtpro.data.saver.DataSaver.update")
  * [DataSaver.update_every](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver.update_every "vectorbtpro.data.saver.DataSaver.update_every")
  * [DataSaver.update_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater.update_kwargs "vectorbtpro.data.saver.DataSaver.update_kwargs")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.data.saver.DataSaver.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.data.saver.DataSaver.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.data.saver.DataSaver.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.data.saver.DataSaver.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.data.saver.DataSaver.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.data.saver.DataSaver.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.data.saver.DataSaver.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.data.saver.DataSaver.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.data.saver.DataSaver.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.data.saver.DataSaver.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.data.saver.DataSaver.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.data.saver.DataSaver.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.data.saver.DataSaver.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.data.saver.DataSaver.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.data.saver.DataSaver.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.data.saver.DataSaver.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.data.saver.DataSaver.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.data.saver.DataSaver.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.data.saver.DataSaver.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.data.saver.DataSaver.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.data.saver.DataSaver.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.data.saver.DataSaver.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.data.saver.DataSaver.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.data.saver.DataSaver.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.data.saver.DataSaver.pprint")



* * *

### init_save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L189-L200 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.SQLDataSaver.init_save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-15-1)SQLDataSaver.init_save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-15-2)    **to_sql_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-15-3))
    

Save initial data.

* * *

### save_data method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/data/saver.py#L202-L215 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.SQLDataSaver.save_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-16-1)SQLDataSaver.save_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-16-2)    **to_sql_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#__codelineno-16-3))
    

Save data.

By default, appends new data without header.
