builders stats_builder

#  stats_builder module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder "Permanent link")

Mixin for building statistics out of performance metrics.

* * *

## MetaStatsBuilderMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py#L34-L40 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.MetaStatsBuilderMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-0-1)MetaStatsBuilderMixin(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-0-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-0-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-0-4))
    

Metaclass for [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").

**Superclasses**

  * `builtins.type`



**Subclasses**

  * [MetaAnalyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.MetaAnalyzable "vectorbtpro.generic.analyzable.MetaAnalyzable")



* * *

### metrics class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py#L37-L40 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.MetaStatsBuilderMixin.metrics "Permanent link")

Metrics supported by [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats").

* * *

## StatsBuilderMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py#L43-L794 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-1-1)StatsBuilderMixin()
    

Mixin that implements [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats").

Required to be a subclass of [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



**Subclasses**

  * [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable "vectorbtpro.generic.analyzable.Analyzable")



* * *

### build_metrics_doc class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py#L780-L789 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-2-1)StatsBuilderMixin.build_metrics_doc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-2-2)    source_cls=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-2-3))
    

Build metrics documentation.

* * *

### metrics property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.metrics "Permanent link")

Metrics supported by [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-1)HybridConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-2)    start_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-3)        title='Start Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-4)        calc_func=<function StatsBuilderMixin.<lambda> at 0x11e1d5b20>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-5)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-6)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-8)    end_index=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-9)        title='End Index',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-10)        calc_func=<function StatsBuilderMixin.<lambda> at 0x11e1d5bc0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-11)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-12)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-14)    total_duration=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-15)        title='Total Duration',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-16)        calc_func=<function StatsBuilderMixin.<lambda> at 0x11e1d5c60>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-17)        apply_to_timedelta=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-18)        agg_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-19)        tags='wrapper'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-20)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-3-21))
    

Returns `StatsBuilderMixin._metrics`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `StatsBuilderMixin._metrics`.

* * *

### override_metrics_doc class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py#L791-L794 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-4-1)StatsBuilderMixin.override_metrics_doc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-4-2)    __pdoc__,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-4-3)    source_cls=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-4-4))
    

Call this method on each subclass that overrides [StatsBuilderMixin.metrics](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.metrics "vectorbtpro.generic.stats_builder.StatsBuilderMixin.metrics").

* * *

### resolve_stats_setting method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py#L61-L80 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.resolve_stats_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-5-1)StatsBuilderMixin.resolve_stats_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-5-2)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-5-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-5-4)    merge=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-5-5))
    

Resolve a setting for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats").

* * *

### stats method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py#L121-L776 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-1)StatsBuilderMixin.stats(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-2)    metrics=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-3)    tags=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-4)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-5)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-6)    per_column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-7)    split_columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-8)    agg_func=<function mean>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-9)    dropna=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-10)    silence_warnings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-11)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-12)    settings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-13)    filters=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-14)    metric_settings=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#__codelineno-6-15))
    

Compute various metrics on this object.

**Args**

**`metrics`** : `str`, `tuple`, `iterable`, `or dict`
    

Metrics to calculate.

Each element can be either:

  * Metric name (see keys in [StatsBuilderMixin.metrics](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.metrics "vectorbtpro.generic.stats_builder.StatsBuilderMixin.metrics"))
  * Tuple of a metric name and a settings dict as in [StatsBuilderMixin.metrics](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.metrics "vectorbtpro.generic.stats_builder.StatsBuilderMixin.metrics")
  * Tuple of a metric name and a template of instance [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * Tuple of a metric name and a list of settings dicts to be expanded into multiple metrics



The settings dict can contain the following keys:

  * `title`: Title of the metric. Defaults to the name.
  * `tags`: Single or multiple tags to associate this metric with. If any of these tags is in `tags`, keeps this metric.
  * `check_{filter}` and `inv_check_{filter}`: Whether to check this metric against a filter defined in `filters`. True (or False for inverse) means to keep this metric.
  * `calc_func` (required): Calculation function for custom metrics. Must return either a scalar for one column/group, pd.Series for multiple columns/groups, or a dict of such for multiple sub-metrics.
  * `resolve_calc_func`: whether to resolve `calc_func`. If the function can be accessed by traversing attributes of this object, you can specify the path to this function as a string (see [deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.deep_getattr "vectorbtpro.utils.attr_.deep_getattr") for the path format). If `calc_func` is a function, arguments from merged metric settings are matched with arguments in the signature (see below). If `resolve_calc_func` is False, `calc_func` must accept (resolved) self and dictionary of merged metric settings. Defaults to True.
  * `use_shortcuts`: Whether to use shortcut properties whenever possible when resolving `calc_func`. Defaults to True.
  * `post_calc_func`: Function to post-process the result of `calc_func`. Must accept (resolved) self, output of `calc_func`, and dictionary of merged metric settings, and return whatever is acceptable to be returned by `calc_func`. Defaults to None.
  * `fill_wrap_kwargs`: Whether to fill `wrap_kwargs` with `to_timedelta` and `silence_warnings`. Defaults to False.
  * `apply_to_timedelta`: Whether to apply [ArrayWrapper.arr_to_timedelta](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.arr_to_timedelta "vectorbtpro.base.wrapping.ArrayWrapper.arr_to_timedelta") on the result. To disable this globally, pass `to_timedelta=False` in `settings`. Defaults to False.
  * `pass_{arg}`: Whether to pass any argument from the settings (see below). Defaults to True if this argument was found in the function's signature. Set to False to not pass. If argument to be passed was not found, `pass_{arg}` is removed.
  * `resolve_path_{arg}`: Whether to resolve an argument that is meant to be an attribute of this object and is the first part of the path of `calc_func`. Passes only optional arguments. Defaults to True. See [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr").
  * `resolve_{arg}`: Whether to resolve an argument that is meant to be an attribute of this object and is present in the function's signature. Defaults to False. See [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr").
  * `use_shortcuts_{arg}`: Whether to use shortcut properties whenever possible when resolving an argument. Defaults to True.
  * `select_col_{arg}`: Whether to select the column from an argument that is meant to be an attribute of this object. Defaults to False.
  * `template_context`: Mapping to replace templates in metric settings. Used across all settings.
  * Any other keyword argument that overrides the settings or is passed directly to `calc_func`.



If `resolve_calc_func` is True, the calculation function may "request" any of the following arguments by accepting them or if `pass_{arg}` was found in the settings dict:

  * Each of [AttrResolverMixin.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases"): original object (ungrouped, with no column selected)
  * `group_by`: won't be passed if it was used in resolving the first attribute of `calc_func` specified as a path, use `pass_group_by=True` to pass anyway
  * `column`
  * `metric_name`
  * `agg_func`
  * `silence_warnings`
  * `to_timedelta`: replaced by True if None and frequency is set
  * Any argument from `settings`
  * Any attribute of this object if it meant to be resolved (see [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr"))



Pass `metrics='all'` to calculate all supported metrics.

**`tags`** : `str` or `iterable`
    

Tags to select.

See [match_tags](https://vectorbt.pro/pvt_7a467f6b/api/utils/tagging/#vectorbtpro.utils.tagging.match_tags "vectorbtpro.utils.tagging.match_tags").

**`column`** : `str`
    

Name of the column/group.

Hint

There are two ways to select a column: `obj['a'].stats()` and `obj.stats(column='a')`. They both accomplish the same thing but in different ways: `obj['a'].stats()` computes statistics of the column 'a' only, while `obj.stats(column='a')` computes statistics of all columns first and only then selects the column 'a'. The first method is preferred when you have a lot of data or caching is disabled. The second method is preferred when most attributes have already been cached.

**`group_by`** : `any`
    Group or ungroup columns. See [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/base/#vectorbtpro.base.grouping.base.Grouper "vectorbtpro.base.grouping.base.Grouper").
**`per_column`** : `bool`
    Whether to compute per column and then stack along columns.
**`split_columns`** : `bool`
    

Whether to split this instance into multiple columns when `per_column` is True.

Otherwise, iterates over columns and passes `column` to the whole instance.

**`agg_func`** : `callable`
    

Aggregation function to aggregate statistics across all columns. By default, takes the mean of all columns. If None, returns all columns as a DataFrame.

Must take `pd.Series` and return a const.

Takes effect if `column` was specified or this object contains only one column of data.

If `agg_func` has been overridden by a metric:

  * Takes effect if global `agg_func` is not None
  * Raises a warning if it's None but the result of calculation has multiple values


**`dropna`** : `bool`
    Whether to hide metrics that are all NaN.
**`silence_warnings`** : `bool`
    Whether to silence all warnings.
**`template_context`** : `mapping`
    

Context used to substitute templates.

Gets merged over `template_context` from [stats_builder](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.stats_builder "vectorbtpro._settings.stats_builder") and [StatsBuilderMixin.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults").

Applied on `settings` and then on each metric settings.

**`filters`** : `dict`
    

Filters to apply.

Each item consists of the filter name and settings dict.

The settings dict can contain the following keys:

  * `filter_func`: Filter function that must accept resolved self and merged settings for a metric, and return either True or False.
  * `warning_message`: Warning message to be shown when skipping a metric. Can be a template that will be substituted using merged metric settings as context. Defaults to None.
  * `inv_warning_message`: Same as `warning_message` but for inverse checks.



Gets merged over `filters` from [stats_builder](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.stats_builder "vectorbtpro._settings.stats_builder") and [StatsBuilderMixin.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults").

**`settings`** : `dict`
    

Global settings and resolution arguments.

Extends/overrides `settings` from [stats_builder](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.stats_builder "vectorbtpro._settings.stats_builder") and [StatsBuilderMixin.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults"). Gets extended/overridden by metric settings.

**`metric_settings`** : `dict`
    

Keyword arguments for each metric.

Extends/overrides all global and metric settings.

For template logic, see [vectorbtpro.utils.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/ "vectorbtpro.utils.template").

For defaults, see [stats_builder](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.stats_builder "vectorbtpro._settings.stats_builder") and [StatsBuilderMixin.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults").

Hint

There are two types of arguments: optional (or resolution) and mandatory arguments. Optional arguments are only passed if they are found in the function's signature. Mandatory arguments are passed regardless of this. Optional arguments can only be defined using `settings` (that is, globally), while mandatory arguments can be defined both using default metric settings and `{metric_name}_kwargs`. Overriding optional arguments using default metric settings or `{metric_name}_kwargs` won't turn them into mandatory. For this, pass `pass_{arg}=True`.

Hint

Make sure to resolve and then to re-use as many object attributes as possible to utilize built-in caching (even if global caching is disabled).

* * *

### stats_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/stats_builder.py#L56-L59 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats_defaults "Permanent link")

Defaults for [StatsBuilderMixin.stats](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats "vectorbtpro.generic.stats_builder.StatsBuilderMixin.stats").
