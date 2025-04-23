base utils

#  base module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/base.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base "Permanent link")

Base class.

* * *

## Base class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/base.py#L18-L73 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-0-1)Base()
    

Base class for all VBT classes.

**Subclasses**

  * [Accessor](https://vectorbt.pro/pvt_7a467f6b/api/accessors/#vectorbtpro.accessors.Accessor "vectorbtpro.accessors.Accessor")
  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [AssetFunc](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/base_asset_funcs/#vectorbtpro.utils.knowledge.base_asset_funcs.AssetFunc "vectorbtpro.utils.knowledge.base_asset_funcs.AssetFunc")
  * [AssetPipeline](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/asset_pipelines/#vectorbtpro.utils.knowledge.asset_pipelines.AssetPipeline "vectorbtpro.utils.knowledge.asset_pipelines.AssetPipeline")
  * [AttrResolverMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin "vectorbtpro.utils.attr_.AttrResolverMixin")
  * [BaseDataMixin](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.BaseDataMixin "vectorbtpro.data.base.BaseDataMixin")
  * [BasePurgedCV](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/purged/#vectorbtpro.generic.splitting.purged.BasePurgedCV "vectorbtpro.generic.splitting.purged.BasePurgedCV")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry")
  * [CachedAccessor](https://vectorbt.pro/pvt_7a467f6b/api/accessors/#vectorbtpro.accessors.CachedAccessor "vectorbtpro.accessors.CachedAccessor")
  * [CachingDisabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled "vectorbtpro.registries.ca_registry.CachingDisabled")
  * [CachingEnabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled "vectorbtpro.registries.ca_registry.CachingEnabled")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [ChunkMetaGenerator](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator "vectorbtpro.utils.chunking.ChunkMetaGenerator")
  * [ChunkableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry "vectorbtpro.registries.ch_registry.ChunkableRegistry")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [CustomJob](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomJob "vectorbtpro.utils.schedule_.CustomJob")
  * [CustomScheduler](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.CustomScheduler "vectorbtpro.utils.schedule_.CustomScheduler")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [ExtSettingsPath](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.ExtSettingsPath "vectorbtpro.utils.config.ExtSettingsPath")
  * [FigureMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin "vectorbtpro.utils.figure.FigureMixin")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [IdxSetterFactory](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory "vectorbtpro.base.indexing.IdxSetterFactory")
  * [IdxrBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxrBase "vectorbtpro.base.indexing.IdxrBase")
  * [IndexApplier](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.IndexApplier "vectorbtpro.base.indexes.IndexApplier")
  * [IndexingBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IndexingBase "vectorbtpro.base.indexing.IndexingBase")
  * [Itemable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Itemable "vectorbtpro.utils.params.Itemable")
  * [JITRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry "vectorbtpro.registries.jit_registry.JITRegistry")
  * [LocBase](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LocBase "vectorbtpro.base.indexing.LocBase")
  * [LogHandler](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/#vectorbtpro.utils.telegram.LogHandler "vectorbtpro.utils.telegram.LogHandler")
  * [MemTracer](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.MemTracer "vectorbtpro.utils.profiling.MemTracer")
  * [PBarRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry "vectorbtpro.registries.pbar_registry.PBarRegistry")
  * [Paramable](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Paramable "vectorbtpro.utils.params.Paramable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [PrintsSuppressed](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.PrintsSuppressed "vectorbtpro.utils.parsing.PrintsSuppressed")
  * [ProgressBar](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar "vectorbtpro.utils.pbar.ProgressBar")
  * [ProgressHidden](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressHidden "vectorbtpro.utils.pbar.ProgressHidden")
  * [ProgressShown](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressShown "vectorbtpro.utils.pbar.ProgressShown")
  * [ScheduleManager](https://vectorbt.pro/pvt_7a467f6b/api/utils/schedule_/#vectorbtpro.utils.schedule_.ScheduleManager "vectorbtpro.utils.schedule_.ScheduleManager")
  * [SimRangeMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin "vectorbtpro.generic.sim_range.SimRangeMixin")
  * [SpecSettingsPath](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.SpecSettingsPath "vectorbtpro.utils.config.SpecSettingsPath")
  * [SplitterCV](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/sklearn_/#vectorbtpro.generic.splitting.sklearn_.SplitterCV "vectorbtpro.generic.splitting.sklearn_.SplitterCV")
  * [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin")
  * [Timer](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.Timer "vectorbtpro.utils.profiling.Timer")
  * [TraceUpdater](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "vectorbtpro.generic.plotting.TraceUpdater")
  * [WarningsFiltered](https://vectorbt.pro/pvt_7a467f6b/api/utils/warnings_/#vectorbtpro.utils.warnings_.WarningsFiltered "vectorbtpro.utils.warnings_.WarningsFiltered")
  * [class_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.class_property "vectorbtpro.utils.decorators.class_property")
  * [custom_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property "vectorbtpro.utils.decorators.custom_property")
  * [define](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.define "vectorbtpro.utils.attr_.define")
  * [hdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.hdict "vectorbtpro.utils.config.hdict")
  * [hybrid_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.hybrid_property "vectorbtpro.utils.decorators.hybrid_property")
  * `vectorbtpro.utils.decorators.hybrid_method`



* * *

### chat class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/base.py#L66-L73 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-1-1)Base.chat(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-1-2)    message,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-1-3)    chat_history=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-1-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-1-5))
    

Chat this class or one of its attributes.

Uses [chat_about](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.chat_about "vectorbtpro.utils.knowledge.custom_assets.chat_about").

* * *

### find_api class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/base.py#L21-L28 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-2-1)Base.find_api(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-2-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-2-3))
    

Find API pages and headings relevant to this class or one of its attributes.

Uses [find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.find_api "vectorbtpro.utils.knowledge.custom_assets.find_api").

* * *

### find_assets class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/base.py#L57-L64 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-3-1)Base.find_assets(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-3-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-3-3))
    

Find all assets relevant to this class or one of its attributes.

Uses [find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.find_assets "vectorbtpro.utils.knowledge.custom_assets.find_assets").

* * *

### find_docs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/base.py#L30-L37 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-4-1)Base.find_docs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-4-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-4-3))
    

Find documentation pages and headings relevant to this class or one of its attributes.

Uses [find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.find_docs "vectorbtpro.utils.knowledge.custom_assets.find_docs").

* * *

### find_examples class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/base.py#L48-L55 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-5-1)Base.find_examples(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-5-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-5-3))
    

Find (code) examples relevant to this class or one of its attributes.

Uses [find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.find_examples "vectorbtpro.utils.knowledge.custom_assets.find_examples").

* * *

### find_messages class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/base.py#L39-L46 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-6-1)Base.find_messages(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-6-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#__codelineno-6-3))
    

Find messages relevant to this class or one of its attributes.

Uses [find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/custom_assets/#vectorbtpro.utils.knowledge.custom_assets.find_messages "vectorbtpro.utils.knowledge.custom_assets.find_messages").
