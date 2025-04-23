wrapping

#  wrapping module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping "Permanent link")

Classes for wrapping NumPy arrays into Series/DataFrames.

* * *

## ArrayWrapper class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L431-L2123 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-1)ArrayWrapper(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-2)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-3)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-4)    ndim=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-5)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-6)    parse_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-7)    column_only_select=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-8)    range_only_select=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-9)    group_select=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-10)    grouped_ndim=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-11)    grouper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-12)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-0-13))
    

Class that stores index, columns, and shape metadata for wrapping NumPy arrays. Tightly integrated with [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/base/#vectorbtpro.base.grouping.base.Grouper "vectorbtpro.base.grouping.base.Grouper") for grouping columns.

If the underlying object is a Series, pass `[sr.name]` as `columns`.

`**kwargs` are passed to [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/base/#vectorbtpro.base.grouping.base.Grouper "vectorbtpro.base.grouping.base.Grouper").

Note

This class is meant to be immutable. To change any attribute, use [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.base.wrapping.ArrayWrapper.replace").

Use methods that begin with `get_` to get group-aware results.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")
  * [IndexApplier](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "vectorbtpro.base.indexes.IndexApplier")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
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
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.base.wrapping.HasWrapper.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.base.wrapping.HasWrapper.chunk_apply")
  * [HasWrapper.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.base.wrapping.HasWrapper.column_only_select")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.base.wrapping.HasWrapper.get_item_keys")
  * [HasWrapper.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.base.wrapping.HasWrapper.group_select")
  * [HasWrapper.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.base.wrapping.HasWrapper.iloc")
  * [HasWrapper.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.base.wrapping.HasWrapper.indexing_kwargs")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.base.wrapping.HasWrapper.items")
  * [HasWrapper.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.base.wrapping.HasWrapper.loc")
  * [HasWrapper.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.base.wrapping.HasWrapper.range_only_select")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.base.wrapping.HasWrapper.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.base.wrapping.HasWrapper.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.base.wrapping.HasWrapper.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.base.wrapping.HasWrapper.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.base.wrapping.HasWrapper.ungroup")
  * [HasWrapper.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.base.wrapping.HasWrapper.unwrapped")
  * [HasWrapper.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.base.wrapping.HasWrapper.wrapper")
  * [HasWrapper.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.base.wrapping.HasWrapper.xloc")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.base.indexes.IndexApplier.add_levels")
  * [IndexApplier.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.indexes.IndexApplier.apply_to_index")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.base.indexes.IndexApplier.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.base.indexes.IndexApplier.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.base.indexes.IndexApplier.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.base.wrapping.HasWrapper.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.base.wrapping.HasWrapper.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.base.wrapping.HasWrapper.xs")
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



* * *

### any_freq class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1339-L1342 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.any_freq "Permanent link")

See [BaseIDXAccessor.any_freq](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.any_freq "vectorbtpro.base.accessors.BaseIDXAccessor.any_freq").

* * *

### arr_to_timedelta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1354-L1356 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.arr_to_timedelta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-1-1)ArrayWrapper.arr_to_timedelta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-1-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-1-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-1-4))
    

See [BaseIDXAccessor.arr_to_timedelta](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.arr_to_timedelta "vectorbtpro.base.accessors.BaseIDXAccessor.arr_to_timedelta").

* * *

### column_stack class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L661-L823 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.column_stack "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-1)ArrayWrapper.column_stack(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-2)    *wrappers,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-3)    index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-4)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-5)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-6)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-7)    union_index=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-8)    col_concat_method='append',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-9)    group_concat_method=('append', 'factorize_each'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-10)    keys=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-11)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-12)    verify_integrity=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-13)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-2-14))
    

Stack multiple [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") instances along columns.

If indexes are the same in each wrapper index, will use that index. If indexes differ and `union_index` is True, they will be merged into a single one by the set union operation. Otherwise, an error will be raised. The merged index must have no duplicates or mixed data, and must be monotonically increasing. A custom index can be provided via `index`.

Frequency must be the same across all indexes. A custom frequency can be provided via `freq`.

Concatenates columns and groups using [concat_indexes](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.concat_indexes "vectorbtpro.base.indexes.concat_indexes").

If any of the instances has `column_only_select` being enabled, the final wrapper will also enable it. If any of the instances has `group_select` or other grouping-related flags being disabled, the final wrapper will also disable them.

All instances must contain the same keys and values in their configs and configs of their grouper instances, apart from those arguments provided explicitly via `kwargs`.

* * *

### column_stack_arrs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1736-L1772 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.column_stack_arrs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-3-1)ArrayWrapper.column_stack_arrs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-3-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-3-3)    reindex_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-3-4)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-3-5)    wrap=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-3-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-3-7))
    

Stack objects along columns and wrap the final object.

`reindex_kwargs` will be passed to [pandas.DataFrame.reindex](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reindex.html).

* * *

### columns class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1272-L1275 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.columns "Permanent link")

Columns.

* * *

### concat_arrs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1683-L1705 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.concat_arrs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-4-1)ArrayWrapper.concat_arrs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-4-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-4-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-4-4)    wrap=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-4-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-4-6))
    

Stack reduced objects along columns and wrap the final object.

* * *

### dt_periods class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1349-L1352 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.dt_periods "Permanent link")

See [BaseIDXAccessor.dt_periods](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.dt_periods "vectorbtpro.base.accessors.BaseIDXAccessor.dt_periods").

* * *

### dummy method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1774-L1777 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.dummy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-5-1)ArrayWrapper.dummy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-5-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-5-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-5-4))
    

Create a dummy Series/DataFrame.

* * *

### extract_init_kwargs static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L486-L495 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.extract_init_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-6-1)ArrayWrapper.extract_init_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-6-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-6-3))
    

Extract keyword arguments that can be passed to [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") or `Grouper`.

* * *

### fill method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1779-L1782 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.fill "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-7-1)ArrayWrapper.fill(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-7-2)    fill_value=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-7-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-7-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-7-5))
    

Fill a Series/DataFrame.

* * *

### fill_and_set method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1814-L2123 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.fill_and_set "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-8-1)ArrayWrapper.fill_and_set(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-8-2)    idx_setter,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-8-3)    keep_flex=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-8-4)    fill_value=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-8-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-8-6))
    

Fill a new array using an index object such as [index_dict](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.index_dict "vectorbtpro.base.indexing.index_dict").

Will be wrapped with [IdxSetter](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter "vectorbtpro.base.indexing.IdxSetter") if not already.

Will call [IdxSetter.fill_and_set](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter.fill_and_set "vectorbtpro.base.indexing.IdxSetter.fill_and_set").

**Usage**

  * Set a single row:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-3)>>> index = pd.date_range("2020", periods=5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-4)>>> columns = pd.Index(["a", "b", "c"])
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-5)>>> wrapper = vbt.ArrayWrapper(index, columns)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-7)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-8)...     1: 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-9)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-10)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-11)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-12)2020-01-02  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-13)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-14)2020-01-04  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-15)2020-01-05  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-16)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-17)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-18)...     "2020-01-02": 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-19)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-20)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-21)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-22)2020-01-02  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-23)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-24)2020-01-04  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-25)2020-01-05  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-27)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-28)...     "2020-01-02": [1, 2, 3]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-29)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-30)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-31)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-32)2020-01-02  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-33)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-34)2020-01-04  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-9-35)2020-01-05  NaN  NaN  NaN
    

  * Set multiple rows:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-1)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-2)...     (1, 3): [2, 3]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-3)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-4)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-5)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-6)2020-01-02  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-7)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-8)2020-01-04  3.0  3.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-9)2020-01-05  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-11)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-12)...     ("2020-01-02", "2020-01-04"): [[1, 2, 3], [4, 5, 6]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-13)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-14)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-15)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-16)2020-01-02  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-17)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-18)2020-01-04  4.0  5.0  6.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-19)2020-01-05  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-21)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-22)...     ("2020-01-02", "2020-01-04"): [[1, 2, 3]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-23)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-24)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-25)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-26)2020-01-02  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-27)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-28)2020-01-04  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-10-29)2020-01-05  NaN  NaN  NaN
    

  * Set rows using slices:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-1)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-2)...     vbt.hslice(1, 3): 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-3)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-4)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-5)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-6)2020-01-02  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-7)2020-01-03  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-8)2020-01-04  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-9)2020-01-05  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-11)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-12)...     vbt.hslice("2020-01-02", "2020-01-04"): 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-13)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-14)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-15)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-16)2020-01-02  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-17)2020-01-03  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-18)2020-01-04  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-19)2020-01-05  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-21)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-22)...     ((0, 2), (3, 5)): [[1], [2]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-23)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-24)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-25)2020-01-01  1.0  1.0  1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-26)2020-01-02  1.0  1.0  1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-27)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-28)2020-01-04  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-29)2020-01-05  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-30)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-31)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-32)...     ((0, 2), (3, 5)): [[1, 2, 3], [4, 5, 6]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-33)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-34)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-35)2020-01-01  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-36)2020-01-02  1.0  2.0  3.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-37)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-38)2020-01-04  4.0  5.0  6.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-11-39)2020-01-05  4.0  5.0  6.0
    

  * Set rows using index points:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-1)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-2)...     vbt.pointidx(every="2D"): 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-3)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-4)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-5)2020-01-01  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-6)2020-01-02  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-7)2020-01-03  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-8)2020-01-04  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-12-9)2020-01-05  2.0  2.0  2.0
    

  * Set rows using index ranges:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-1)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-2)...     vbt.rangeidx(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-3)...         start=("2020-01-01", "2020-01-03"),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-4)...         end=("2020-01-02", "2020-01-05")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-5)...     ): 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-6)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-7)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-8)2020-01-01  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-9)2020-01-02  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-10)2020-01-03  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-11)2020-01-04  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-13-12)2020-01-05  NaN  NaN  NaN
    

  * Set column indices:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-1)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-2)...     vbt.colidx("a"): 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-3)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-4)              a   b   c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-5)2020-01-01  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-6)2020-01-02  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-7)2020-01-03  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-8)2020-01-04  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-9)2020-01-05  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-11)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-12)...     vbt.colidx(("a", "b")): [1, 2]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-13)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-14)              a    b   c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-15)2020-01-01  1.0  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-16)2020-01-02  1.0  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-17)2020-01-03  1.0  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-18)2020-01-04  1.0  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-19)2020-01-05  1.0  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-21)>>> multi_columns = pd.MultiIndex.from_arrays(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-22)...     [["a", "a", "b", "b"], [1, 2, 1, 2]],
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-23)...     names=["c1", "c2"]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-24)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-25)>>> multi_wrapper = vbt.ArrayWrapper(index, multi_columns)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-26)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-27)>>> multi_wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-28)...     vbt.colidx(("a", 2)): 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-29)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-30)c1           a        b
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-31)c2           1    2   1   2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-32)2020-01-01 NaN  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-33)2020-01-02 NaN  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-34)2020-01-03 NaN  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-35)2020-01-04 NaN  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-36)2020-01-05 NaN  2.0 NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-37)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-38)>>> multi_wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-39)...     vbt.colidx("b", level="c1"): [3, 4]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-40)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-41)c1           a        b
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-42)c2           1   2    1    2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-43)2020-01-01 NaN NaN  3.0  4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-44)2020-01-02 NaN NaN  3.0  4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-45)2020-01-03 NaN NaN  3.0  4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-46)2020-01-04 NaN NaN  3.0  4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-14-47)2020-01-05 NaN NaN  3.0  4.0
    

  * Set row and column indices:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-1)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-2)...     vbt.idx(2, 2): 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-3)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-4)             a   b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-5)2020-01-01 NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-6)2020-01-02 NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-7)2020-01-03 NaN NaN  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-8)2020-01-04 NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-9)2020-01-05 NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-11)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-12)...     vbt.idx(("2020-01-01", "2020-01-03"), 2): [1, 2]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-13)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-14)             a   b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-15)2020-01-01 NaN NaN  1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-16)2020-01-02 NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-17)2020-01-03 NaN NaN  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-18)2020-01-04 NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-19)2020-01-05 NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-21)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-22)...     vbt.idx(("2020-01-01", "2020-01-03"), (0, 2)): [[1, 2], [3, 4]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-23)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-24)              a   b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-25)2020-01-01  1.0 NaN  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-26)2020-01-02  NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-27)2020-01-03  3.0 NaN  4.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-28)2020-01-04  NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-29)2020-01-05  NaN NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-30)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-31)>>> multi_wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-32)...     vbt.idx(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-33)...         vbt.pointidx(every="2d"),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-34)...         vbt.colidx(1, level="c2")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-35)...     ): [[1, 2]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-36)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-37)c1            a        b
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-38)c2            1   2    1   2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-39)2020-01-01  1.0 NaN  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-40)2020-01-02  NaN NaN  NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-41)2020-01-03  1.0 NaN  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-42)2020-01-04  NaN NaN  NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-43)2020-01-05  1.0 NaN  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-44)
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-45)>>> multi_wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-46)...     vbt.idx(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-47)...         vbt.pointidx(every="2d"),
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-48)...         vbt.colidx(1, level="c2")
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-49)...     ): [[1], [2], [3]]
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-50)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-51)c1            a        b
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-52)c2            1   2    1   2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-53)2020-01-01  1.0 NaN  1.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-54)2020-01-02  NaN NaN  NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-55)2020-01-03  2.0 NaN  2.0 NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-56)2020-01-04  NaN NaN  NaN NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-15-57)2020-01-05  3.0 NaN  3.0 NaN
    

  * Set rows using a template:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-1)>>> wrapper.fill_and_set(vbt.index_dict({
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-2)...     vbt.RepEval("index.day % 2 == 0"): 2
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-3)... }))
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-4)              a    b    c
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-5)2020-01-01  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-6)2020-01-02  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-7)2020-01-03  NaN  NaN  NaN
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-8)2020-01-04  2.0  2.0  2.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-16-9)2020-01-05  NaN  NaN  NaN
    

* * *

### fill_reduced method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1784-L1787 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.fill_reduced "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-17-1)ArrayWrapper.fill_reduced(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-17-2)    fill_value=nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-17-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-17-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-17-5))
    

Fill a reduced Series/DataFrame.

* * *

### flip method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1428-L1432 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.flip "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-18-1)ArrayWrapper.flip(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-18-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-18-3))
    

Flip index and columns.

* * *

### freq class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1329-L1332 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.freq "Permanent link")

See [BaseIDXAccessor.freq](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.freq "vectorbtpro.base.accessors.BaseIDXAccessor.freq").

* * *

### from_obj class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L444-L464 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.from_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-19-1)ArrayWrapper.from_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-19-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-19-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-19-4))
    

Derive metadata from an object.

* * *

### from_shape class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L466-L484 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.from_shape "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-20-1)ArrayWrapper.from_shape(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-20-2)    shape,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-20-3)    index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-20-4)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-20-5)    ndim=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-20-6)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-20-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-20-8))
    

Derive metadata from shape.

* * *

### get_columns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1277-L1279 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_columns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-21-1)ArrayWrapper.get_columns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-21-2)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-21-3))
    

Get group-aware [ArrayWrapper.columns](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.columns "vectorbtpro.base.wrapping.ArrayWrapper.columns").

* * *

### get_freq method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1325-L1327 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_freq "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-22-1)ArrayWrapper.get_freq(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-22-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-22-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-22-4))
    

See [BaseIDXAccessor.get_freq](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.get_freq "vectorbtpro.base.accessors.BaseIDXAccessor.get_freq").

* * *

### get_index_grouper method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1449-L1451 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_grouper "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-23-1)ArrayWrapper.get_index_grouper(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-23-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-23-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-23-4))
    

See [BaseIDXAccessor.get_grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.get_grouper "vectorbtpro.base.accessors.BaseIDXAccessor.get_grouper").

* * *

### get_index_points method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1806-L1808 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-24-1)ArrayWrapper.get_index_points(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-24-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-24-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-24-4))
    

See [BaseIDXAccessor.get_points](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.get_points "vectorbtpro.base.accessors.BaseIDXAccessor.get_points").

* * *

### get_index_ranges method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1810-L1812 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_ranges "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-25-1)ArrayWrapper.get_index_ranges(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-25-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-25-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-25-4))
    

See [BaseIDXAccessor.get_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.get_ranges "vectorbtpro.base.accessors.BaseIDXAccessor.get_ranges").

* * *

### get_name method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1290-L1292 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_name "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-26-1)ArrayWrapper.get_name(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-26-2)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-26-3))
    

Get group-aware [ArrayWrapper.name](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.name "vectorbtpro.base.wrapping.ArrayWrapper.name").

* * *

### get_ndim method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1299-L1301 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_ndim "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-27-1)ArrayWrapper.get_ndim(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-27-2)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-27-3))
    

Get group-aware [ArrayWrapper.ndim](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.ndim "vectorbtpro.base.wrapping.ArrayWrapper.ndim").

* * *

### get_period_ns_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1268-L1270 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_period_ns_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-28-1)ArrayWrapper.get_period_ns_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-28-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-28-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-28-4))
    

See [BaseIDXAccessor.to_period_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.to_period_ns "vectorbtpro.base.accessors.BaseIDXAccessor.to_period_ns").

* * *

### get_resampler method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1219-L1221 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_resampler "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-29-1)ArrayWrapper.get_resampler(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-29-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-29-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-29-4))
    

See [BaseIDXAccessor.get_resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.get_resampler "vectorbtpro.base.accessors.BaseIDXAccessor.get_resampler").

* * *

### get_shape method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1310-L1312 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_shape "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-30-1)ArrayWrapper.get_shape(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-30-2)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-30-3))
    

Get group-aware [ArrayWrapper.shape](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.shape "vectorbtpro.base.wrapping.ArrayWrapper.shape").

* * *

### get_shape_2d method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1321-L1323 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_shape_2d "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-31-1)ArrayWrapper.get_shape_2d(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-31-2)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-31-3))
    

Get group-aware [ArrayWrapper.shape_2d](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.shape_2d "vectorbtpro.base.wrapping.ArrayWrapper.shape_2d").

* * *

### grouped_ndim class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1403-L1410 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.grouped_ndim "Permanent link")

Number of dimensions under column grouping.

* * *

### grouper class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1398-L1401 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.grouper "Permanent link")

Column grouper.

* * *

### index class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1251-L1254 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.index "Permanent link")

Index.

* * *

### index_acc cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.index_acc "Permanent link")

Get index accessor of the type [BaseIDXAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor "vectorbtpro.base.accessors.BaseIDXAccessor").

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1171-L1173 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-32-1)ArrayWrapper.indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-32-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-32-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-32-4))
    

Perform indexing on [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper").

* * *

### indexing_func_meta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L891-L1169 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.indexing_func_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-1)ArrayWrapper.indexing_func_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-2)    pd_indexing_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-3)    index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-4)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-5)    column_only_select=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-6)    range_only_select=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-7)    group_select=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-8)    return_slices=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-9)    return_none_slices=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-10)    return_scalars=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-11)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-12)    wrapper_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-33-13))
    

Perform indexing on [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") and also return metadata.

Takes into account column grouping.

Flipping rows and columns is not allowed. If one row is selected, the result will still be a Series when indexing a Series and a DataFrame when indexing a DataFrame.

Set `column_only_select` to True to index the array wrapper as a Series of columns/groups. This way, selection of index (axis 0) can be avoided. Set `range_only_select` to True to allow selection of rows only using slices. Set `group_select` to True to allow selection of groups. Otherwise, indexing is performed on columns, even if grouping is enabled. Takes effect only if grouping is enabled.

Returns the new array wrapper, row indices, column indices, and group indices. If `return_slices` is True (default), indices will be returned as a slice if they were identified as a range. If `return_none_slices` is True (default), indices will be returned as a slice `(None, None, None)` if the axis hasn't been changed.

Note

If `column_only_select` is True, make sure to index the array wrapper as a Series of columns rather than a DataFrame. For example, the operation `.iloc[:, :2]` should become `.iloc[:2]`. Operations are not allowed if the object is already a Series and thus has only one column/group.

* * *

### name class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1281-L1288 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.name "Permanent link")

Name.

* * *

### ndim class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1294-L1297 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.ndim "Permanent link")

Number of dimensions.

* * *

### ns_freq class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1334-L1337 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.ns_freq "Permanent link")

See [BaseIDXAccessor.ns_freq](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.ns_freq "vectorbtpro.base.accessors.BaseIDXAccessor.ns_freq").

* * *

### ns_index class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1263-L1266 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.ns_index "Permanent link")

See [BaseIDXAccessor.to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.to_ns "vectorbtpro.base.accessors.BaseIDXAccessor.to_ns").

* * *

### parse_index class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1358-L1363 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.parse_index "Permanent link")

Whether to try to convert the index into a datetime index.

Applied during the initialization and passed to [prepare_dt_index](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.prepare_dt_index "vectorbtpro.utils.datetime_.prepare_dt_index").

* * *

### periods class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1344-L1347 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.periods "Permanent link")

See [BaseIDXAccessor.periods](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.periods "vectorbtpro.base.accessors.BaseIDXAccessor.periods").

* * *

### regroup cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1412-L1426 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.regroup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-34-1)ArrayWrapper.regroup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-34-2)    group_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-34-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-34-4))
    

Regroup this instance.

Only creates a new instance if grouping has changed, otherwise returns itself.

* * *

### resample method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1241-L1245 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.resample "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-35-1)ArrayWrapper.resample(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-35-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-35-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-35-4))
    

Perform resampling on [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper").

Uses [ArrayWrapper.resample_meta](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.resample_meta "vectorbtpro.base.wrapping.ArrayWrapper.resample_meta").

* * *

### resample_meta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1223-L1239 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.resample_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-36-1)ArrayWrapper.resample_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-36-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-36-3)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-36-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-36-5))
    

Perform resampling on [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") and also return metadata.

`*args` and `**kwargs` are passed to [ArrayWrapper.get_resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_resampler "vectorbtpro.base.wrapping.ArrayWrapper.get_resampler").

* * *

### resolve cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1434-L1447 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.resolve "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-37-1)ArrayWrapper.resolve(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-37-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-37-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-37-4))
    

Resolve this instance.

Replaces columns and other metadata with groups.

* * *

### resolve_stack_kwargs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L497-L537 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.resolve_stack_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-38-1)ArrayWrapper.resolve_stack_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-38-2)    *wrappers,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-38-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-38-4))
    

Resolve keyword arguments for initializing [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") after stacking.

* * *

### row_stack class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L539-L659 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.row_stack "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-1)ArrayWrapper.row_stack(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-2)    *wrappers,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-3)    index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-4)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-5)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-6)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-7)    stack_columns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-8)    index_concat_method='append',
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-9)    keys=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-10)    clean_index_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-11)    verify_integrity=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-12)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-39-13))
    

Stack multiple [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") instances along rows.

Concatenates indexes using [concat_indexes](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.concat_indexes "vectorbtpro.base.indexes.concat_indexes").

Frequency must be the same across all indexes. A custom frequency can be provided via `freq`.

If column levels in some instances differ, they will be stacked upon each other. Custom columns can be provided via `columns`.

If `group_by` is None, all instances must be either grouped or not, and they must contain the same group values and labels.

All instances must contain the same keys and values in their configs and configs of their grouper instances, apart from those arguments provided explicitly via `kwargs`.

* * *

### row_stack_arrs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1707-L1734 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.row_stack_arrs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-40-1)ArrayWrapper.row_stack_arrs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-40-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-40-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-40-4)    wrap=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-40-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-40-6))
    

Stack objects along rows and wrap the final object.

* * *

### select_from_flex_array static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1175-L1217 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.select_from_flex_array "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-1)ArrayWrapper.select_from_flex_array(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-3)    row_idxs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-4)    col_idxs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-5)    rows_changed=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-6)    columns_changed=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-7)    rotate_rows=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-8)    rotate_cols=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-41-9))
    

Select rows and columns from a flexible array.

Always returns a 2-dim NumPy array.

* * *

### shape class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1303-L1308 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.shape "Permanent link")

Shape.

* * *

### shape_2d class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1314-L1319 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.shape_2d "Permanent link")

Shape as if the instance was two-dimensional.

* * *

### wrap method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1453-L1568 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.wrap "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-1)ArrayWrapper.wrap(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-4)    index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-5)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-6)    zero_to_none=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-7)    force_2d=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-8)    fillna=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-9)    dtype=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-10)    min_precision=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-11)    max_precision=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-12)    prec_float_only=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-13)    prec_check_bounds=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-14)    prec_strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-15)    to_timedelta=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-16)    to_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-17)    silence_warnings=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-42-18))
    

Wrap a NumPy array using the stored metadata.

Runs the following pipeline:

1) Converts to NumPy array 2) Fills NaN (optional) 3) Wraps using index, columns, and dtype (optional) 4) Converts to index (optional) 5) Converts to timedelta using [ArrayWrapper.arr_to_timedelta](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.arr_to_timedelta "vectorbtpro.base.wrapping.ArrayWrapper.arr_to_timedelta") (optional)

* * *

### wrap_reduced method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L1570-L1681 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.wrap_reduced "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-1)ArrayWrapper.wrap_reduced(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-4)    name_or_index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-5)    columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-6)    force_1d=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-7)    fillna=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-8)    dtype=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-9)    to_timedelta=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-10)    to_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-11)    silence_warnings=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-43-12))
    

Wrap result of reduction.

`name_or_index` can be the name of the resulting series if reducing to a scalar per column, or the index of the resulting series/dataframe if reducing to an array per column. `columns` can be set to override object's default columns.

See [ArrayWrapper.wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.wrap "vectorbtpro.base.wrapping.ArrayWrapper.wrap") for the pipeline.

* * *

## HasWrapper class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L51-L425 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-44-1)HasWrapper(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-44-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-44-3))
    

Abstract class that manages a wrapper.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.indexing.ExtPandasIndexer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.indexing.ExtPandasIndexer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.indexing.ExtPandasIndexer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.indexing.ExtPandasIndexer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.indexing.ExtPandasIndexer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.indexing.ExtPandasIndexer.find_messages")
  * [ExtPandasIndexer.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.base.indexing.ExtPandasIndexer.iloc")
  * [ExtPandasIndexer.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.base.indexing.ExtPandasIndexer.indexing_kwargs")
  * [ExtPandasIndexer.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.base.indexing.ExtPandasIndexer.loc")
  * [ExtPandasIndexer.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.base.indexing.ExtPandasIndexer.xloc")
  * [IndexingBase.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_func "vectorbtpro.base.indexing.ExtPandasIndexer.indexing_func")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.base.indexing.ExtPandasIndexer.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.utils.params.ItemParamable.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.base.indexing.ExtPandasIndexer.xs")



**Subclasses**

  * [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper")
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



* * *

### chunk method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L273-L313 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-1)HasWrapper.chunk(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-2)    axis=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-3)    min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-4)    n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-5)    chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-6)    chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-7)    select=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-8)    wrap=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-9)    return_chunk_meta=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-45-10))
    

Chunk this instance.

If `axis` is None, becomes 0 if the instance is one-dimensional and 1 otherwise.

For arguments related to chunking meta, see [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

* * *

### chunk_apply method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L315-L345 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-46-1)HasWrapper.chunk_apply(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-46-2)    apply_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-46-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-46-4)    chunk_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-46-5)    execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-46-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-46-7))
    

Chunk this instance and apply a function to each chunk.

If `apply_func` is a string, becomes the method name.

For arguments related to chunking, see [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.base.wrapping.Wrapping.chunk").

* * *

### column_only_select class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L69-L72 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "Permanent link")

Whether to perform indexing on columns only.

* * *

### get_item_keys method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L349-L354 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-47-1)HasWrapper.get_item_keys(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-47-2)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-47-3))
    

Get keys for [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.base.wrapping.Wrapping.items").

* * *

### group_select class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L79-L82 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "Permanent link")

Whether to allow indexing on groups.

* * *

### items method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L356-L425 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-48-1)HasWrapper.items(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-48-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-48-3)    apply_group_by=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-48-4)    keep_2d=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-48-5)    key_as_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-48-6)    wrap=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-48-7))
    

Iterate over columns or groups (if grouped and [Wrapping.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.base.wrapping.Wrapping.group_select") is True).

If `apply_group_by` is False, `group_by` becomes a grouping instruction for the iteration, not for the final object. In this case, will raise an error if the instance is grouped and that grouping must be changed.

* * *

### range_only_select class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L74-L77 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "Permanent link")

Whether to perform indexing on rows using slices only.

* * *

### regroup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L84-L86 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.regroup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-49-1)HasWrapper.regroup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-49-2)    group_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-49-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-49-4))
    

Regroup this instance.

* * *

### select_col method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L94-L146 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-50-1)HasWrapper.select_col(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-50-2)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-50-3)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-50-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-50-5))
    

Select one column/group.

`column` can be a label-based position as well as an integer position (if label fails).

* * *

### select_col_from_obj class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L148-L226 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-51-1)HasWrapper.select_col_from_obj(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-51-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-51-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-51-4)    obj_ungrouped=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-51-5)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-51-6)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-51-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-51-8))
    

Select one column/group from a Pandas object.

`column` can be a label-based position as well as an integer position (if label fails).

* * *

### should_wrap class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L59-L62 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-52-1)HasWrapper.should_wrap()
    

Whether to wrap where applicable.

* * *

### split method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L230-L247 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-53-1)HasWrapper.split(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-53-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-53-3)    splitter_cls=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-53-4)    wrap=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-53-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-53-6))
    

Split this instance.

Uses [Splitter.split_and_take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_and_take "vectorbtpro.generic.splitting.base.Splitter.split_and_take").

* * *

### split_apply method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L249-L269 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-54-1)HasWrapper.split_apply(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-54-2)    apply_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-54-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-54-4)    splitter_cls=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-54-5)    wrap=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-54-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-54-7))
    

Split this instance and apply a function to each split.

Uses [Splitter.split_and_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.split_and_apply "vectorbtpro.generic.splitting.base.Splitter.split_and_apply").

* * *

### ungroup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L88-L90 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-55-1)HasWrapper.ungroup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-55-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-55-3))
    

Ungroup this instance.

* * *

### unwrapped class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L54-L57 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "Permanent link")

Unwrapped object.

* * *

### wrapper class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L64-L67 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "Permanent link")

Array wrapper of the type [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper").

* * *

## Wrapping class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2129-L2292 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-56-1)Wrapping(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-56-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-56-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-56-4))
    

Class that uses [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper "vectorbtpro.base.wrapping.ArrayWrapper") globally.

**Superclasses**

  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer "vectorbtpro.base.indexing.ExtPandasIndexer")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [HasWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper "vectorbtpro.base.wrapping.HasWrapper")
  * [IndexApplier](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "vectorbtpro.base.indexes.IndexApplier")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [ItemParamable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.ItemParamable "vectorbtpro.utils.params.ItemParamable")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer "vectorbtpro.base.indexing.PandasIndexer")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [AttrResolverMixin.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir")
  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr")
  * [AttrResolverMixin.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases")
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
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.base.wrapping.HasWrapper.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.base.wrapping.HasWrapper.chunk_apply")
  * [HasWrapper.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.base.wrapping.HasWrapper.column_only_select")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.base.wrapping.HasWrapper.get_item_keys")
  * [HasWrapper.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.base.wrapping.HasWrapper.group_select")
  * [HasWrapper.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.base.wrapping.HasWrapper.iloc")
  * [HasWrapper.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.base.wrapping.HasWrapper.indexing_kwargs")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.base.wrapping.HasWrapper.items")
  * [HasWrapper.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.base.wrapping.HasWrapper.loc")
  * [HasWrapper.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.base.wrapping.HasWrapper.range_only_select")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.base.wrapping.HasWrapper.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.base.wrapping.HasWrapper.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.base.wrapping.HasWrapper.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.base.wrapping.HasWrapper.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.base.wrapping.HasWrapper.ungroup")
  * [HasWrapper.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.base.wrapping.HasWrapper.unwrapped")
  * [HasWrapper.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.base.wrapping.HasWrapper.wrapper")
  * [HasWrapper.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.base.wrapping.HasWrapper.xloc")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.base.indexes.IndexApplier.add_levels")
  * [IndexApplier.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.indexes.IndexApplier.apply_to_index")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.base.indexes.IndexApplier.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.base.indexes.IndexApplier.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.base.indexes.IndexApplier.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.base.wrapping.HasWrapper.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.base.wrapping.HasWrapper.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.base.wrapping.HasWrapper.xs")
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

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")
  * [BaseAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor "vectorbtpro.base.accessors.BaseAccessor")
  * [ColumnMapper](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper "vectorbtpro.records.col_mapper.ColumnMapper")



* * *

### column_stack class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2161-L2171 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.column_stack "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-57-1)Wrapping.column_stack(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-57-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-57-3)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-57-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-57-5))
    

Stack multiple [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping") instances along columns.

Should use [ArrayWrapper.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.column_stack "vectorbtpro.base.wrapping.ArrayWrapper.column_stack").

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2181-L2190 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-58-1)Wrapping.indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-58-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-58-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-58-4))
    

Perform indexing on [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping").

* * *

### regroup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2243-L2252 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-59-1)Wrapping.regroup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-59-2)    group_by,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-59-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-59-4))
    

Regroup this instance.

Only creates a new instance if grouping has changed, otherwise returns itself.

`**kwargs` will be passed to [ArrayWrapper.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.regroup "vectorbtpro.base.wrapping.ArrayWrapper.regroup").

* * *

### resample method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2192-L2197 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resample "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-60-1)Wrapping.resample(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-60-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-60-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-60-4))
    

Perform resampling on [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping").

When overriding, make sure to create a resampler by passing `*args` and `**kwargs` to [ArrayWrapper.get_resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_resampler "vectorbtpro.base.wrapping.ArrayWrapper.get_resampler").

* * *

### resolve_column_stack_kwargs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2137-L2140 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_column_stack_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-61-1)Wrapping.resolve_column_stack_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-61-2)    *wrappings,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-61-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-61-4))
    

Resolve keyword arguments for initializing [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping") after stacking along columns.

* * *

### resolve_row_stack_kwargs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2132-L2135 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_row_stack_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-62-1)Wrapping.resolve_row_stack_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-62-2)    *wrappings,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-62-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-62-4))
    

Resolve keyword arguments for initializing [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping") after stacking along rows.

* * *

### resolve_self method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2254-L2292 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-63-1)Wrapping.resolve_self(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-63-2)    cond_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-63-3)    custom_arg_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-63-4)    impacts_caching=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-63-5)    silence_warnings=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-63-6))
    

Resolve self.

Creates a copy of this instance if a different `freq` can be found in `cond_kwargs`.

* * *

### resolve_stack_kwargs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2142-L2147 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-64-1)Wrapping.resolve_stack_kwargs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-64-2)    *wrappings,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-64-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-64-4))
    

Resolve keyword arguments for initializing [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping") after stacking.

Should be called after [Wrapping.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_row_stack_kwargs "vectorbtpro.base.wrapping.Wrapping.resolve_row_stack_kwargs") or [Wrapping.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_column_stack_kwargs "vectorbtpro.base.wrapping.Wrapping.resolve_column_stack_kwargs").

* * *

### row_stack class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/base/wrapping.py#L2149-L2159 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.row_stack "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-65-1)Wrapping.row_stack(
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-65-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-65-3)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-65-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#__codelineno-65-5))
    

Stack multiple [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping") instances along rows.

Should use [ArrayWrapper.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.row_stack "vectorbtpro.base.wrapping.ArrayWrapper.row_stack").
