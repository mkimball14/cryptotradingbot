builders plots_builder

#  plots_builder module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder "Permanent link")

Mixin for building plots out of subplots.

* * *

## MetaPlotsBuilderMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py#L32-L38 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.MetaPlotsBuilderMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-0-1)MetaPlotsBuilderMixin(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-0-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-0-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-0-4))
    

Metaclass for [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin").

**Superclasses**

  * `builtins.type`



**Subclasses**

  * [MetaAnalyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.MetaAnalyzable "vectorbtpro.generic.analyzable.MetaAnalyzable")



* * *

### subplots class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py#L35-L38 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.MetaPlotsBuilderMixin.subplots "Permanent link")

Subplots supported by [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots").

* * *

## PlotsBuilderMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py#L41-L900 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-1-1)PlotsBuilderMixin()
    

Mixin that implements [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots").

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

### build_subplots_doc class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py#L886-L895 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-2-1)PlotsBuilderMixin.build_subplots_doc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-2-2)    source_cls=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-2-3))
    

Build subplots documentation.

* * *

### override_subplots_doc class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py#L897-L900 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-3-1)PlotsBuilderMixin.override_subplots_doc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-3-2)    __pdoc__,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-3-3)    source_cls=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-3-4))
    

Call this method on each subclass that overrides [PlotsBuilderMixin.subplots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.subplots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.subplots").

* * *

### plots method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py#L97-L882 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-1)PlotsBuilderMixin.plots(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-2)    subplots=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-3)    tags=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-4)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-5)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-6)    per_column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-7)    split_columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-8)    silence_warnings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-9)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-10)    settings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-11)    filters=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-12)    subplot_settings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-13)    show_titles=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-14)    show_legend=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-15)    show_column_label=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-16)    hide_id_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-17)    group_id_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-18)    make_subplots_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-19)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-20)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-4-21))
    

Plot various parts of this object.

**Args**

**`subplots`** : `str`, `tuple`, `iterable`, `or dict`
    

Subplots to plot.

Each element can be either:

  * Subplot name (see keys in [PlotsBuilderMixin.subplots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.subplots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.subplots"))
  * Tuple of a subplot name and a settings dict as in [PlotsBuilderMixin.subplots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.subplots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.subplots")
  * Tuple of a subplot name and a template of instance [CustomTemplate](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/#vectorbtpro.utils.template.CustomTemplate "vectorbtpro.utils.template.CustomTemplate")
  * Tuple of a subplot name and a list of settings dicts to be expanded into multiple subplots



The settings dict can contain the following keys:

  * `title`: Title of the subplot. Defaults to the name.
  * `plot_func` (required): Plotting function for custom subplots. Must write the supplied figure `fig` in-place and can return anything (it won't be used).
  * `xaxis_kwargs`: Layout keyword arguments for the x-axis. Defaults to `dict(title='Index')`.
  * `yaxis_kwargs`: Layout keyword arguments for the y-axis. Defaults to empty dict.
  * `tags`, `check_{filter}`, `inv_check_{filter}`, `resolve_plot_func`, `pass_{arg}`, `resolve_path_{arg}`, `resolve_{arg}` and `template_context`: The same as in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin") for `calc_func`.
  * Any other keyword argument that overrides the settings or is passed directly to `plot_func`.



If `resolve_plot_func` is True, the plotting function may "request" any of the following arguments by accepting them or if `pass_{arg}` was found in the settings dict:

  * Each of [AttrResolverMixin.self_aliases](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases "vectorbtpro.utils.attr_.AttrResolverMixin.self_aliases"): original object (ungrouped, with no column selected)
  * `group_by`: won't be passed if it was used in resolving the first attribute of `plot_func` specified as a path, use `pass_group_by=True` to pass anyway
  * `column`
  * `subplot_name`
  * `trace_names`: list with the subplot name, can't be used in templates
  * `add_trace_kwargs`: dict with subplot row and column index
  * `xref`
  * `yref`
  * `xaxis`
  * `yaxis`
  * `x_domain`
  * `y_domain`
  * `fig`
  * `silence_warnings`
  * Any argument from `settings`
  * Any attribute of this object if it meant to be resolved (see [AttrResolverMixin.resolve_attr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr "vectorbtpro.utils.attr_.AttrResolverMixin.resolve_attr"))



Note

Layout-related resolution arguments such as `add_trace_kwargs` are unavailable before filtering and thus cannot be used in any templates but can still be overridden.

Pass `subplots='all'` to plot all supported subplots.

**`tags`** : `str` or `iterable`
    See `tags` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`column`** : `str`
    See `column` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`group_by`** : `any`
    See `group_by` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`per_column`** : `bool`
    See `per_column` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`split_columns`** : `bool`
    See `split_columns` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`silence_warnings`** : `bool`
    See `silence_warnings` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`template_context`** : `mapping`
    

See `template_context` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").

Applied on `settings`, `make_subplots_kwargs`, and `layout_kwargs`, and then on each subplot settings.

**`filters`** : `dict`
    See `filters` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`settings`** : `dict`
    See `settings` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`subplot_settings`** : `dict`
    See `metric_settings` in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
**`show_titles`** : `bool`
    Whether to show the title of each subplot.
**`show_legend`** : `bool`
    

Whether to show legend.

If None and plotting per column, becomes False, otherwise True.

**`show_column_label`** : `bool`
    

Whether to show the column label next to each legend label.

If None and plotting per column, becomes True, otherwise False.

**`hide_id_labels`** : `bool`
    

Whether to hide identical legend labels.

Two labels are identical if their name, marker style and line style match.

**`group_id_labels`** : `bool`
    Whether to group identical legend labels.
**`make_subplots_kwargs`** : `dict`
    Keyword arguments passed to `plotly.subplots.make_subplots`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments used to update the layout of the figure.

Note

[PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin") and [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin") are very similar. Some artifacts follow the same concept, just named differently:

  * `plots_defaults` vs `stats_defaults`
  * `subplots` vs `metrics`
  * `subplot_settings` vs `metric_settings`



See further notes under [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").

* * *

### plots_defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py#L54-L57 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots_defaults "Permanent link")

Defaults for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots").

* * *

### resolve_plots_setting method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py#L59-L78 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.resolve_plots_setting "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-5-1)PlotsBuilderMixin.resolve_plots_setting(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-5-2)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-5-3)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-5-4)    merge=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-5-5))
    

Resolve a setting for [PlotsBuilderMixin.plots](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots "vectorbtpro.generic.plots_builder.PlotsBuilderMixin.plots").

* * *

### subplots property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plots_builder.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin.subplots "Permanent link")

Subplots supported by [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#__codelineno-6-1)HybridConfig()
    

Returns `PlotsBuilderMixin._subplots`, which gets (hybrid-) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `PlotsBuilderMixin._subplots`.
