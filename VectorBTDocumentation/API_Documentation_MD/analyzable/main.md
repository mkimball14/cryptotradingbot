analyzable

#  analyzable module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/analyzable.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable "Permanent link")

Class for analyzing data.

* * *

## Analyzable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/analyzable.py#L31-L37 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-0-1)Analyzable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-0-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-0-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-0-4))
    

Class that can be analyzed by computing and plotting attributes of any kind.

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
  * [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
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
  * [PlotsBuilderMixin.build_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc")
  * [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots")
  * [PlotsBuilderMixin.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots_defaults "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots_defaults")
  * [PlotsBuilderMixin.resolve_plots_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.base.wrapping.Wrapping.pprint")
  * [StatsBuilderMixin.build_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc")
  * [StatsBuilderMixin.resolve_stats_setting](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting")
  * [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats")
  * [StatsBuilderMixin.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults")
  * [Wrapping.apply_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier.apply_to_index "vectorbtpro.base.wrapping.Wrapping.apply_to_index")
  * [Wrapping.cls_dir](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.cls_dir "vectorbtpro.base.wrapping.Wrapping.cls_dir")
  * [Wrapping.column_only_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.column_only_select "vectorbtpro.base.wrapping.Wrapping.column_only_select")
  * [Wrapping.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.column_stack "vectorbtpro.base.wrapping.Wrapping.column_stack")
  * [Wrapping.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.base.wrapping.Wrapping.config")
  * [Wrapping.group_select](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.group_select "vectorbtpro.base.wrapping.Wrapping.group_select")
  * [Wrapping.iloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer.iloc "vectorbtpro.base.wrapping.Wrapping.iloc")
  * [Wrapping.indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.indexing_func "vectorbtpro.base.wrapping.Wrapping.indexing_func")
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
  * [Wrapping.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.row_stack "vectorbtpro.base.wrapping.Wrapping.row_stack")
  * [Wrapping.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.base.wrapping.Wrapping.self_aliases")
  * [Wrapping.unwrapped](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.unwrapped "vectorbtpro.base.wrapping.Wrapping.unwrapped")
  * [Wrapping.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.HasWrapper.wrapper "vectorbtpro.base.wrapping.Wrapping.wrapper")
  * [Wrapping.xloc](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer.xloc "vectorbtpro.base.wrapping.Wrapping.xloc")



**Subclasses**

  * [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data "vectorbtpro.data.base.Data")
  * [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor "vectorbtpro.generic.accessors.GenericAccessor")
  * [IndicatorBase](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase "vectorbtpro.indicators.factory.IndicatorBase")
  * [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray")
  * [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio "vectorbtpro.portfolio.base.Portfolio")
  * [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer "vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer")
  * [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records")
  * [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter "vectorbtpro.generic.splitting.base.Splitter")



* * *

## MetaAnalyzable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/analyzable.py#L23-L25 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.MetaAnalyzable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-1-1)MetaAnalyzable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-1-2)    name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-1-3)    bases,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-1-4)    attrs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#__codelineno-1-5))
    

Metaclass for [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable").

**Superclasses**

  * [MetaConfigured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.MetaConfigured "vectorbtpro.utils.config.MetaConfigured")
  * [MetaPlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.MetaPlotsBuilderMixin "vectorbtpro.generic.plots_builder.MetaPlotsBuilderMixin")
  * [MetaStatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.MetaStatsBuilderMixin "vectorbtpro.generic.stats_builder.MetaStatsBuilderMixin")
  * `builtins.type`



**Inherited members**

  * [MetaPlotsBuilderMixin.subplots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.MetaPlotsBuilderMixin.subplots "vectorbtpro.generic.plots_builder.MetaPlotsBuilderMixin.subplots")
  * [MetaStatsBuilderMixin.metrics](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.MetaStatsBuilderMixin.metrics "vectorbtpro.generic.stats_builder.MetaStatsBuilderMixin.metrics")



**Subclasses**

  * [MetaData](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.MetaData "vectorbtpro.data.base.MetaData")
  * [MetaPortfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.MetaPortfolio "vectorbtpro.portfolio.base.MetaPortfolio")
  * [MetaRecords](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.MetaRecords "vectorbtpro.records.base.MetaRecords")


