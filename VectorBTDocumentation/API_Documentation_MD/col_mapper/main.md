col_mapper

#  col_mapper module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper "Permanent link")

Class for mapping column arrays.

* * *

## ColumnMapper class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L31-L253 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-0-1)ColumnMapper(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-0-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-0-3)    col_arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-0-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-0-5))
    

Used by [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records") and [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray") classes to make use of column and group metadata.

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
  * [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping")



**Inherited members**

  * [AttrResolverMixin.deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.deep_getattr "vectorbtpro.base.wrapping.Wrapping.deep_getattr")
  * [AttrResolverMixin.post_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.post_resolve_attr "vectorbtpro.base.wrapping.Wrapping.post_resolve_attr")
  * [AttrResolverMixin.pre_resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.pre_resolve_attr "vectorbtpro.base.wrapping.Wrapping.pre_resolve_attr")
  * [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.base.wrapping.Wrapping.resolve_attr")
  * [AttrResolverMixin.resolve_shortcut_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_shortcut_attr "vectorbtpro.base.wrapping.Wrapping.resolve_shortcut_attr")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.wrapping.Wrapping.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.wrapping.Wrapping.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.wrapping.Wrapping.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.wrapping.Wrapping.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.wrapping.Wrapping.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.wrapping.Wrapping.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.base.wrapping.Wrapping.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.base.wrapping.Wrapping.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.base.wrapping.Wrapping.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.base.wrapping.Wrapping.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.base.wrapping.Wrapping.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.base.wrapping.Wrapping.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.base.wrapping.Wrapping.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.base.wrapping.Wrapping.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.base.wrapping.Wrapping.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.base.wrapping.Wrapping.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.base.wrapping.Wrapping.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.base.wrapping.Wrapping.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.base.wrapping.Wrapping.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.base.wrapping.Wrapping.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.base.wrapping.Wrapping.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.base.wrapping.Wrapping.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.base.wrapping.Wrapping.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.base.wrapping.Wrapping.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.base.wrapping.Wrapping.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.base.wrapping.Wrapping.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.base.wrapping.Wrapping.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.base.wrapping.Wrapping.set_settings")
  * [HasWrapper.chunk](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk "vectorbtpro.base.wrapping.Wrapping.chunk")
  * [HasWrapper.chunk_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.chunk_apply "vectorbtpro.base.wrapping.Wrapping.chunk_apply")
  * [HasWrapper.get_item_keys](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.get_item_keys "vectorbtpro.base.wrapping.Wrapping.get_item_keys")
  * [HasWrapper.items](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.items "vectorbtpro.base.wrapping.Wrapping.items")
  * [HasWrapper.select_col](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col "vectorbtpro.base.wrapping.Wrapping.select_col")
  * [HasWrapper.select_col_from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.select_col_from_obj "vectorbtpro.base.wrapping.Wrapping.select_col_from_obj")
  * [HasWrapper.should_wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.should_wrap "vectorbtpro.base.wrapping.Wrapping.should_wrap")
  * [HasWrapper.split](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split "vectorbtpro.base.wrapping.Wrapping.split")
  * [HasWrapper.split_apply](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.split_apply "vectorbtpro.base.wrapping.Wrapping.split_apply")
  * [HasWrapper.ungroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.ungroup "vectorbtpro.base.wrapping.Wrapping.ungroup")
  * [IndexApplier.add_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.add_levels "vectorbtpro.base.wrapping.Wrapping.add_levels")
  * [IndexApplier.drop_duplicate_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_duplicate_levels "vectorbtpro.base.wrapping.Wrapping.drop_duplicate_levels")
  * [IndexApplier.drop_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_levels "vectorbtpro.base.wrapping.Wrapping.drop_levels")
  * [IndexApplier.drop_redundant_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.drop_redundant_levels "vectorbtpro.base.wrapping.Wrapping.drop_redundant_levels")
  * [IndexApplier.rename_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.rename_levels "vectorbtpro.base.wrapping.Wrapping.rename_levels")
  * [IndexApplier.select_levels](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.select_levels "vectorbtpro.base.wrapping.Wrapping.select_levels")
  * [IndexingBase.indexing_setter_func](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase.indexing_setter_func "vectorbtpro.base.wrapping.Wrapping.indexing_setter_func")
  * [ItemParamable.as_param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable.as_param "vectorbtpro.base.wrapping.Wrapping.as_param")
  * [PandasIndexer.xs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.xs "vectorbtpro.base.wrapping.Wrapping.xs")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.base.wrapping.Wrapping.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.base.wrapping.Wrapping.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.base.wrapping.Wrapping.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.base.wrapping.Wrapping.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.base.wrapping.Wrapping.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.base.wrapping.Wrapping.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.base.wrapping.Wrapping.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.base.wrapping.Wrapping.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.base.wrapping.Wrapping.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.base.wrapping.Wrapping.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.base.wrapping.Wrapping.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.base.wrapping.Wrapping.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.base.wrapping.Wrapping.pprint")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.wrapping.Wrapping.apply_to_index")
  * [Wrapping.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.base.wrapping.Wrapping.cls_dir")
  * [Wrapping.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.base.wrapping.Wrapping.column_only_select")
  * [Wrapping.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.base.wrapping.Wrapping.config")
  * [Wrapping.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.base.wrapping.Wrapping.group_select")
  * [Wrapping.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.base.wrapping.Wrapping.iloc")
  * [Wrapping.indexing_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.indexing_kwargs "vectorbtpro.base.wrapping.Wrapping.indexing_kwargs")
  * [Wrapping.loc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.loc "vectorbtpro.base.wrapping.Wrapping.loc")
  * [Wrapping.range_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.range_only_select "vectorbtpro.base.wrapping.Wrapping.range_only_select")
  * [Wrapping.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.base.wrapping.Wrapping.rec_state")
  * [Wrapping.regroup](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.regroup "vectorbtpro.base.wrapping.Wrapping.regroup")
  * [Wrapping.resample](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resample "vectorbtpro.base.wrapping.Wrapping.resample")
  * [Wrapping.resolve_column_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_column_stack_kwargs "vectorbtpro.base.wrapping.Wrapping.resolve_column_stack_kwargs")
  * [Wrapping.resolve_row_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_row_stack_kwargs "vectorbtpro.base.wrapping.Wrapping.resolve_row_stack_kwargs")
  * [Wrapping.resolve_self](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_self "vectorbtpro.base.wrapping.Wrapping.resolve_self")
  * [Wrapping.resolve_stack_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs "vectorbtpro.base.wrapping.Wrapping.resolve_stack_kwargs")
  * [Wrapping.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.base.wrapping.Wrapping.self_aliases")
  * [Wrapping.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.base.wrapping.Wrapping.unwrapped")
  * [Wrapping.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.base.wrapping.Wrapping.wrapper")
  * [Wrapping.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.base.wrapping.Wrapping.xloc")



* * *

### col_arr class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L179-L182 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.col_arr "Permanent link")

Column array.

* * *

### col_lens cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.col_lens "Permanent link")

Column lengths.

Faster than [ColumnMapper.col_map](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.col_map "vectorbtpro.records.col_mapper.ColumnMapper.col_map") but only compatible with sorted columns.

* * *

### col_map cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.col_map "Permanent link")

Column map.

More flexible than [ColumnMapper.col_lens](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.col_lens "vectorbtpro.records.col_mapper.ColumnMapper.col_lens"). More suited for mapped arrays.

* * *

### column_stack class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L79-L122 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.column_stack "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-1-1)ColumnMapper.column_stack(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-1-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-1-3)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-1-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-1-5))
    

Stack multiple [ColumnMapper](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper "vectorbtpro.records.col_mapper.ColumnMapper") instances along columns.

Uses [ArrayWrapper.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.column_stack "vectorbtpro.base.wrapping.ArrayWrapper.column_stack") to stack the wrappers.

Note

Will produce a column-sorted array.

* * *

### get_col_arr cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L184-L192 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.get_col_arr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-2-1)ColumnMapper.get_col_arr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-2-2)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-2-3))
    

Get group-aware column array.

* * *

### get_col_lens cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L202-L210 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.get_col_lens "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-3-1)ColumnMapper.get_col_lens(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-3-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-3-3)    jitted=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-3-4))
    

Get group-aware column lengths.

* * *

### get_col_map cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L221-L229 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.get_col_map "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-4-1)ColumnMapper.get_col_map(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-4-2)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-4-3)    jitted=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-4-4))
    

Get group-aware column map.

* * *

### get_new_id_arr cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L243-L253 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.get_new_id_arr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-5-1)ColumnMapper.get_new_id_arr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-5-2)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-5-3))
    

Generate a new group-aware id array.

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L170-L177 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-6-1)ColumnMapper.indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-6-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-6-3)    col_mapper_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-6-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-6-5))
    

Perform indexing on [ColumnMapper](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper "vectorbtpro.records.col_mapper.ColumnMapper").

* * *

### indexing_func_meta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L154-L168 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.indexing_func_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-7-1)ColumnMapper.indexing_func_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-7-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-7-3)    wrapper_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-7-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-7-5))
    

Perform indexing on [ColumnMapper](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper "vectorbtpro.records.col_mapper.ColumnMapper") and return metadata.

* * *

### is_sorted cached_method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L231-L235 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.is_sorted "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-8-1)ColumnMapper.is_sorted(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-8-2)    jitted=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-8-3))
    

Check whether column array is sorted.

* * *

### new_id_arr cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.new_id_arr "Permanent link")

Generate a new id array.

* * *

### row_stack class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L35-L77 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.row_stack "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-9-1)ColumnMapper.row_stack(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-9-2)    *objs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-9-3)    wrapper_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-9-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-9-5))
    

Stack multiple [ColumnMapper](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper "vectorbtpro.records.col_mapper.ColumnMapper") instances along rows.

Uses [ArrayWrapper.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.row_stack "vectorbtpro.base.wrapping.ArrayWrapper.row_stack") to stack the wrappers.

Note

Will produce a column-sorted array.

* * *

### select_cols method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/records/col_mapper.py#L132-L152 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper.select_cols "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-10-1)ColumnMapper.select_cols(
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-10-2)    col_idxs,
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-10-3)    jitted=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#__codelineno-10-4))
    

Select columns.

Returns indices and new column array. Automatically decides whether to use column lengths or column map.
