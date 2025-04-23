plotting

#  plotting module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting "Permanent link")

Base plotting functions.

Provides functions for visualizing data in an efficient and convenient way. Each creates a figure widget that is compatible with ipywidgets and enables interactive data visualization in Jupyter Notebook and JupyterLab environments. For more details on using Plotly, see [Getting Started with Plotly in Python](https://plotly.com/python/getting-started/).

Warning

Errors related to plotting in Jupyter environment usually appear in the logs, not under the cell.

* * *

## clean_labels function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L53-L63 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.clean_labels "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-0-1)clean_labels(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-0-2)    labels
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-0-3))
    

Clean labels.

Plotly doesn't support multi-indexes.

* * *

## Bar class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L229-L336 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Bar "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-1)Bar(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-2)    data=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-3)    trace_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-4)    x_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-5)    trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-6)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-7)    make_figure_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-8)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-9)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-1-10))
    

Bar plot.

**Args**

**`data`** : `array_like`
    

Data in any format that can be converted to NumPy.

Must be of shape (`x_labels`, `trace_names`).

**`trace_names`** : `str` or `list` of `str`
    Trace names, corresponding to columns in pandas.
**`x_labels`** : `array_like`
    X-axis labels, corresponding to index in pandas.
**`trace_kwargs`** : `dict` or `list` of `dict`
    

Keyword arguments passed to `plotly.graph_objects.Bar`.

Can be specified per trace as a sequence of dicts.

**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`make_figure_kwargs`** : `dict`
    Keyword arguments passed to [make_figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_figure "vectorbtpro.utils.figure.make_figure").
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-2-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-2-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-2-3)>>> bar = vbt.Bar(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-2-4)...     data=[[1, 2], [3, 4]],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-2-5)...     trace_names=['a', 'b'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-2-6)...     x_labels=['x', 'y']
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-2-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-2-8)>>> bar.fig.show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Bar.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Bar.dark.svg#only-dark)

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [TraceType](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "vectorbtpro.generic.plotting.TraceType")
  * [TraceUpdater](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "vectorbtpro.generic.plotting.TraceUpdater")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.plotting.TraceType.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.plotting.TraceType.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.plotting.TraceType.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.plotting.TraceType.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.plotting.TraceType.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.plotting.TraceType.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.plotting.TraceType.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.plotting.TraceType.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.plotting.TraceType.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.plotting.TraceType.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.plotting.TraceType.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.plotting.TraceType.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.plotting.TraceType.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.generic.plotting.TraceType.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.plotting.TraceType.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.plotting.TraceType.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.plotting.TraceType.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.plotting.TraceType.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.plotting.TraceType.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.plotting.TraceType.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.plotting.TraceType.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.plotting.TraceType.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.plotting.TraceType.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.plotting.TraceType.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.plotting.TraceType.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.plotting.TraceType.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.plotting.TraceType.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.plotting.TraceType.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.plotting.TraceType.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.plotting.TraceType.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.plotting.TraceType.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.plotting.TraceType.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.plotting.TraceType.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.plotting.TraceType.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.plotting.TraceType.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.plotting.TraceType.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.plotting.TraceType.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.plotting.TraceType.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.plotting.TraceType.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.plotting.TraceType.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.plotting.TraceType.pprint")
  * [TraceType.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.plotting.TraceType.config")
  * [TraceType.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.plotting.TraceType.rec_state")
  * [TraceUpdater.fig](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.fig "vectorbtpro.generic.plotting.TraceUpdater.fig")
  * [TraceUpdater.traces](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.traces "vectorbtpro.generic.plotting.TraceUpdater.traces")
  * [TraceUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update "vectorbtpro.generic.plotting.TraceUpdater.update")
  * [TraceUpdater.update_trace](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update_trace "vectorbtpro.generic.plotting.TraceUpdater.update_trace")



* * *

## Box class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L670-L829 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Box "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-1)Box(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-2)    data=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-3)    trace_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-4)    horizontal=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-5)    remove_nan=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-6)    from_quantile=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-7)    to_quantile=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-8)    trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-9)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-10)    make_figure_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-11)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-12)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-3-13))
    

Box plot.

For keyword arguments, see [Histogram](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Histogram "vectorbtpro.generic.plotting.Histogram").

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-4-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-4-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-4-3)>>> box = vbt.Box(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-4-4)...     data=[[1, 2], [3, 4], [2, 1]],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-4-5)...     trace_names=['a', 'b']
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-4-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-4-7)>>> box.fig.show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Box.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Box.dark.svg#only-dark)

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [TraceType](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "vectorbtpro.generic.plotting.TraceType")
  * [TraceUpdater](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "vectorbtpro.generic.plotting.TraceUpdater")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.plotting.TraceType.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.plotting.TraceType.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.plotting.TraceType.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.plotting.TraceType.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.plotting.TraceType.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.plotting.TraceType.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.plotting.TraceType.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.plotting.TraceType.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.plotting.TraceType.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.plotting.TraceType.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.plotting.TraceType.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.plotting.TraceType.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.plotting.TraceType.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.generic.plotting.TraceType.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.plotting.TraceType.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.plotting.TraceType.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.plotting.TraceType.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.plotting.TraceType.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.plotting.TraceType.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.plotting.TraceType.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.plotting.TraceType.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.plotting.TraceType.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.plotting.TraceType.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.plotting.TraceType.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.plotting.TraceType.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.plotting.TraceType.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.plotting.TraceType.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.plotting.TraceType.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.plotting.TraceType.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.plotting.TraceType.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.plotting.TraceType.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.plotting.TraceType.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.plotting.TraceType.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.plotting.TraceType.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.plotting.TraceType.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.plotting.TraceType.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.plotting.TraceType.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.plotting.TraceType.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.plotting.TraceType.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.plotting.TraceType.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.plotting.TraceType.pprint")
  * [TraceType.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.plotting.TraceType.config")
  * [TraceType.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.plotting.TraceType.rec_state")
  * [TraceUpdater.fig](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.fig "vectorbtpro.generic.plotting.TraceUpdater.fig")
  * [TraceUpdater.traces](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.traces "vectorbtpro.generic.plotting.TraceUpdater.traces")
  * [TraceUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update "vectorbtpro.generic.plotting.TraceUpdater.update")
  * [TraceUpdater.update_trace](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update_trace "vectorbtpro.generic.plotting.TraceUpdater.update_trace")



* * *

### from_quantile class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L777-L780 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Box.from_quantile "Permanent link")

Filter out data points before this quantile.

* * *

### horizontal class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L767-L770 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Box.horizontal "Permanent link")

Whether to plot horizontally.

* * *

### remove_nan class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L772-L775 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Box.remove_nan "Permanent link")

Whether to remove NaN values.

* * *

### to_quantile class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L782-L785 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Box.to_quantile "Permanent link")

Filter out data points after this quantile.

* * *

## Gauge class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L99-L226 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Gauge "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-1)Gauge(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-2)    value=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-3)    label=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-4)    value_range=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-5)    cmap_name='Spectral',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-6)    trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-7)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-8)    make_figure_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-9)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-10)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-5-11))
    

Gauge plot.

**Args**

**`value`** : `float`
    The value to be displayed.
**`label`** : `str`
    The label to be displayed.
**`value_range`** : `tuple` of `float`
    The value range of the gauge.
**`cmap_name`** : `str`
    

A matplotlib-compatible colormap name.

See the [list of available colormaps](https://matplotlib.org/tutorials/colors/colormaps.html).

**`trace_kwargs`** : `dict`
    Keyword arguments passed to the `plotly.graph_objects.Indicator`.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`make_figure_kwargs`** : `dict`
    Keyword arguments passed to [make_figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_figure "vectorbtpro.utils.figure.make_figure").
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-6-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-6-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-6-3)>>> gauge = vbt.Gauge(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-6-4)...     value=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-6-5)...     value_range=(1, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-6-6)...     label='My Gauge'
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-6-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-6-8)>>> gauge.fig.show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Gauge.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Gauge.dark.svg#only-dark)

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [TraceType](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "vectorbtpro.generic.plotting.TraceType")
  * [TraceUpdater](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "vectorbtpro.generic.plotting.TraceUpdater")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.plotting.TraceType.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.plotting.TraceType.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.plotting.TraceType.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.plotting.TraceType.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.plotting.TraceType.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.plotting.TraceType.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.plotting.TraceType.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.plotting.TraceType.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.plotting.TraceType.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.plotting.TraceType.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.plotting.TraceType.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.plotting.TraceType.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.plotting.TraceType.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.generic.plotting.TraceType.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.plotting.TraceType.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.plotting.TraceType.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.plotting.TraceType.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.plotting.TraceType.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.plotting.TraceType.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.plotting.TraceType.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.plotting.TraceType.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.plotting.TraceType.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.plotting.TraceType.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.plotting.TraceType.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.plotting.TraceType.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.plotting.TraceType.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.plotting.TraceType.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.plotting.TraceType.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.plotting.TraceType.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.plotting.TraceType.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.plotting.TraceType.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.plotting.TraceType.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.plotting.TraceType.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.plotting.TraceType.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.plotting.TraceType.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.plotting.TraceType.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.plotting.TraceType.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.plotting.TraceType.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.plotting.TraceType.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.plotting.TraceType.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.plotting.TraceType.pprint")
  * [TraceType.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.plotting.TraceType.config")
  * [TraceType.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.plotting.TraceType.rec_state")
  * [TraceUpdater.fig](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.fig "vectorbtpro.generic.plotting.TraceUpdater.fig")
  * [TraceUpdater.traces](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.traces "vectorbtpro.generic.plotting.TraceUpdater.traces")
  * [TraceUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update "vectorbtpro.generic.plotting.TraceUpdater.update")
  * [TraceUpdater.update_trace](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update_trace "vectorbtpro.generic.plotting.TraceUpdater.update_trace")



* * *

### cmap_name class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L194-L197 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Gauge.cmap_name "Permanent link")

A matplotlib-compatible colormap name.

* * *

### value_range class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L189-L192 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Gauge.value_range "Permanent link")

The value range of the gauge.

* * *

## Heatmap class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L832-L958 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Heatmap "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-1)Heatmap(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-2)    data=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-3)    x_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-4)    y_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-5)    is_x_category=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-6)    is_y_category=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-7)    trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-8)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-9)    make_figure_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-10)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-11)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-7-12))
    

Heatmap plot.

**Args**

**`data`** : `array_like`
    

Data in any format that can be converted to NumPy.

Must be of shape (`y_labels`, `x_labels`).

**`x_labels`** : `array_like`
    X-axis labels, corresponding to columns in pandas.
**`y_labels`** : `array_like`
    Y-axis labels, corresponding to index in pandas.
**`is_x_category`** : `bool`
    Whether X-axis is a categorical axis.
**`is_y_category`** : `bool`
    Whether Y-axis is a categorical axis.
**`trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Heatmap`.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`make_figure_kwargs`** : `dict`
    Keyword arguments passed to [make_figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_figure "vectorbtpro.utils.figure.make_figure").
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-8-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-8-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-8-3)>>> heatmap = vbt.Heatmap(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-8-4)...     data=[[1, 2], [3, 4]],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-8-5)...     x_labels=['a', 'b'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-8-6)...     y_labels=['x', 'y']
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-8-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-8-8)>>> heatmap.fig.show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Heatmap.dark.svg#only-dark)

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [TraceType](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "vectorbtpro.generic.plotting.TraceType")
  * [TraceUpdater](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "vectorbtpro.generic.plotting.TraceUpdater")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.plotting.TraceType.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.plotting.TraceType.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.plotting.TraceType.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.plotting.TraceType.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.plotting.TraceType.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.plotting.TraceType.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.plotting.TraceType.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.plotting.TraceType.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.plotting.TraceType.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.plotting.TraceType.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.plotting.TraceType.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.plotting.TraceType.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.plotting.TraceType.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.generic.plotting.TraceType.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.plotting.TraceType.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.plotting.TraceType.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.plotting.TraceType.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.plotting.TraceType.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.plotting.TraceType.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.plotting.TraceType.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.plotting.TraceType.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.plotting.TraceType.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.plotting.TraceType.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.plotting.TraceType.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.plotting.TraceType.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.plotting.TraceType.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.plotting.TraceType.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.plotting.TraceType.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.plotting.TraceType.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.plotting.TraceType.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.plotting.TraceType.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.plotting.TraceType.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.plotting.TraceType.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.plotting.TraceType.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.plotting.TraceType.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.plotting.TraceType.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.plotting.TraceType.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.plotting.TraceType.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.plotting.TraceType.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.plotting.TraceType.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.plotting.TraceType.pprint")
  * [TraceType.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.plotting.TraceType.config")
  * [TraceType.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.plotting.TraceType.rec_state")
  * [TraceUpdater.fig](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.fig "vectorbtpro.generic.plotting.TraceUpdater.fig")
  * [TraceUpdater.traces](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.traces "vectorbtpro.generic.plotting.TraceUpdater.traces")
  * [TraceUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update "vectorbtpro.generic.plotting.TraceUpdater.update")
  * [TraceUpdater.update_trace](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update_trace "vectorbtpro.generic.plotting.TraceUpdater.update_trace")



* * *

## Histogram class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L484-L667 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Histogram "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-1)Histogram(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-2)    data=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-3)    trace_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-4)    horizontal=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-5)    remove_nan=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-6)    from_quantile=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-7)    to_quantile=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-8)    trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-9)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-10)    make_figure_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-11)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-12)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-9-13))
    

Histogram plot.

**Args**

**`data`** : `array_like`
    

Data in any format that can be converted to NumPy.

Must be of shape (any, `trace_names`).

**`trace_names`** : `str` or `list` of `str`
    Trace names, corresponding to columns in pandas.
**`horizontal`** : `bool`
    Whether to plot horizontally.
**`remove_nan`** : `bool`
    Whether to remove NaN values.
**`from_quantile`** : `float`
    

Filter out data points before this quantile.

Must be in range `[0, 1]`.

**`to_quantile`** : `float`
    

Filter out data points after this quantile.

Must be in range `[0, 1]`.

**`trace_kwargs`** : `dict` or `list` of `dict`
    

Keyword arguments passed to `plotly.graph_objects.Histogram`.

Can be specified per trace as a sequence of dicts.

**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`make_figure_kwargs`** : `dict`
    Keyword arguments passed to [make_figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_figure "vectorbtpro.utils.figure.make_figure").
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-10-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-10-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-10-3)>>> hist = vbt.Histogram(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-10-4)...     data=[[1, 2], [3, 4], [2, 1]],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-10-5)...     trace_names=['a', 'b']
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-10-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-10-7)>>> hist.fig.show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Histogram.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Histogram.dark.svg#only-dark)

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [TraceType](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "vectorbtpro.generic.plotting.TraceType")
  * [TraceUpdater](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "vectorbtpro.generic.plotting.TraceUpdater")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.plotting.TraceType.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.plotting.TraceType.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.plotting.TraceType.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.plotting.TraceType.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.plotting.TraceType.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.plotting.TraceType.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.plotting.TraceType.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.plotting.TraceType.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.plotting.TraceType.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.plotting.TraceType.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.plotting.TraceType.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.plotting.TraceType.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.plotting.TraceType.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.generic.plotting.TraceType.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.plotting.TraceType.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.plotting.TraceType.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.plotting.TraceType.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.plotting.TraceType.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.plotting.TraceType.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.plotting.TraceType.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.plotting.TraceType.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.plotting.TraceType.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.plotting.TraceType.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.plotting.TraceType.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.plotting.TraceType.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.plotting.TraceType.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.plotting.TraceType.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.plotting.TraceType.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.plotting.TraceType.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.plotting.TraceType.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.plotting.TraceType.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.plotting.TraceType.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.plotting.TraceType.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.plotting.TraceType.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.plotting.TraceType.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.plotting.TraceType.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.plotting.TraceType.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.plotting.TraceType.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.plotting.TraceType.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.plotting.TraceType.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.plotting.TraceType.pprint")
  * [TraceType.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.plotting.TraceType.config")
  * [TraceType.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.plotting.TraceType.rec_state")
  * [TraceUpdater.fig](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.fig "vectorbtpro.generic.plotting.TraceUpdater.fig")
  * [TraceUpdater.traces](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.traces "vectorbtpro.generic.plotting.TraceUpdater.traces")
  * [TraceUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update "vectorbtpro.generic.plotting.TraceUpdater.update")
  * [TraceUpdater.update_trace](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update_trace "vectorbtpro.generic.plotting.TraceUpdater.update_trace")



* * *

### from_quantile class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L615-L618 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Histogram.from_quantile "Permanent link")

Filter out data points before this quantile.

* * *

### horizontal class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L605-L608 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Histogram.horizontal "Permanent link")

Whether to plot horizontally.

* * *

### remove_nan class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L610-L613 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Histogram.remove_nan "Permanent link")

Whether to remove NaN values.

* * *

### to_quantile class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L620-L623 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Histogram.to_quantile "Permanent link")

Filter out data points after this quantile.

* * *

## Scatter class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L339-L481 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Scatter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-1)Scatter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-2)    data=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-3)    trace_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-4)    x_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-5)    trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-6)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-7)    make_figure_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-8)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-9)    use_gl=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-10)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-11-11))
    

Scatter plot.

**Args**

**`data`** : `array_like`
    

Data in any format that can be converted to NumPy.

Must be of shape (`x_labels`, `trace_names`).

**`trace_names`** : `str` or `list` of `str`
    Trace names, corresponding to columns in pandas.
**`x_labels`** : `array_like`
    X-axis labels, corresponding to index in pandas.
**`trace_kwargs`** : `dict` or `list` of `dict`
    

Keyword arguments passed to `plotly.graph_objects.Scatter`.

Can be specified per trace as a sequence of dicts.

**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`make_figure_kwargs`** : `dict`
    Keyword arguments passed to [make_figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_figure "vectorbtpro.utils.figure.make_figure").
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`use_gl`** : `bool`
    

Whether to use `plotly.graph_objects.Scattergl`.

Defaults to the global setting. If the global setting is None, becomes True if there are more than 10,000 data points.

**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-12-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-12-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-12-3)>>> scatter = vbt.Scatter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-12-4)...     data=[[1, 2], [3, 4]],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-12-5)...     trace_names=['a', 'b'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-12-6)...     x_labels=['x', 'y']
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-12-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-12-8)>>> scatter.fig.show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Scatter.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Scatter.dark.svg#only-dark)

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [TraceType](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "vectorbtpro.generic.plotting.TraceType")
  * [TraceUpdater](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "vectorbtpro.generic.plotting.TraceUpdater")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.plotting.TraceType.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.plotting.TraceType.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.plotting.TraceType.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.plotting.TraceType.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.plotting.TraceType.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.plotting.TraceType.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.plotting.TraceType.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.plotting.TraceType.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.plotting.TraceType.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.plotting.TraceType.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.plotting.TraceType.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.plotting.TraceType.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.plotting.TraceType.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.generic.plotting.TraceType.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.plotting.TraceType.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.plotting.TraceType.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.plotting.TraceType.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.plotting.TraceType.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.plotting.TraceType.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.plotting.TraceType.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.plotting.TraceType.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.plotting.TraceType.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.plotting.TraceType.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.plotting.TraceType.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.plotting.TraceType.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.plotting.TraceType.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.plotting.TraceType.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.plotting.TraceType.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.plotting.TraceType.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.plotting.TraceType.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.plotting.TraceType.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.plotting.TraceType.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.plotting.TraceType.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.plotting.TraceType.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.plotting.TraceType.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.plotting.TraceType.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.plotting.TraceType.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.plotting.TraceType.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.plotting.TraceType.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.plotting.TraceType.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.plotting.TraceType.pprint")
  * [TraceType.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.plotting.TraceType.config")
  * [TraceType.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.plotting.TraceType.rec_state")
  * [TraceUpdater.fig](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.fig "vectorbtpro.generic.plotting.TraceUpdater.fig")
  * [TraceUpdater.traces](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.traces "vectorbtpro.generic.plotting.TraceUpdater.traces")
  * [TraceUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update "vectorbtpro.generic.plotting.TraceUpdater.update")
  * [TraceUpdater.update_trace](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update_trace "vectorbtpro.generic.plotting.TraceUpdater.update_trace")



* * *

## TraceType class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L66-L69 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-13-1)TraceType(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-13-2)    **config
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-13-3))
    

Class representing a trace type.

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

  * [Bar](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Bar "vectorbtpro.generic.plotting.Bar")
  * [Box](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Box "vectorbtpro.generic.plotting.Box")
  * [Gauge](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Gauge "vectorbtpro.generic.plotting.Gauge")
  * [Heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Heatmap "vectorbtpro.generic.plotting.Heatmap")
  * [Histogram](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Histogram "vectorbtpro.generic.plotting.Histogram")
  * [Scatter](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Scatter "vectorbtpro.generic.plotting.Scatter")
  * [Volume](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Volume "vectorbtpro.generic.plotting.Volume")



* * *

## TraceUpdater class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L72-L96 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-14-1)TraceUpdater(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-14-2)    fig,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-14-3)    traces
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-14-4))
    

Class for updating traces.

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

  * [Bar](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Bar "vectorbtpro.generic.plotting.Bar")
  * [Box](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Box "vectorbtpro.generic.plotting.Box")
  * [Gauge](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Gauge "vectorbtpro.generic.plotting.Gauge")
  * [Heatmap](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Heatmap "vectorbtpro.generic.plotting.Heatmap")
  * [Histogram](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Histogram "vectorbtpro.generic.plotting.Histogram")
  * [Scatter](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Scatter "vectorbtpro.generic.plotting.Scatter")
  * [Volume](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Volume "vectorbtpro.generic.plotting.Volume")



* * *

### fig class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L79-L82 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.fig "Permanent link")

Figure.

* * *

### traces class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L84-L87 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.traces "Permanent link")

Traces to update.

* * *

### update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L94-L96 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-15-1)TraceUpdater.update(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-15-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-15-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-15-4))
    

Update all traces using new data.

* * *

### update_trace class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L89-L92 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update_trace "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-16-1)TraceUpdater.update_trace(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-16-2)    trace,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-16-3)    data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-16-4)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-16-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-16-6))
    

Update one trace.

* * *

## Volume class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/plotting.py#L961-L1113 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Volume "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-1)Volume(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-2)    data=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-3)    x_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-4)    y_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-5)    z_labels=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-6)    trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-7)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-8)    scene_name='scene',
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-9)    make_figure_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-10)    fig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-11)    **layout_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-17-12))
    

Volume plot.

**Args**

**`data`** : `array_like`
    

Data in any format that can be converted to NumPy.

Must be a 3-dim array.

**`x_labels`** : `array_like`
    X-axis labels.
**`y_labels`** : `array_like`
    Y-axis labels.
**`z_labels`** : `array_like`
    Z-axis labels.
**`trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Volume`.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`scene_name`** : `str`
    Reference to the 3D scene.
**`make_figure_kwargs`** : `dict`
    Keyword arguments passed to [make_figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_figure "vectorbtpro.utils.figure.make_figure").
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

Note

Figure widgets have currently problems displaying NaNs. Use `.show()` method for rendering.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-3)>>> volume = vbt.Volume(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-4)...     data=np.random.randint(1, 10, size=(3, 3, 3)),
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-5)...     x_labels=['a', 'b', 'c'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-6)...     y_labels=['d', 'e', 'f'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-7)...     z_labels=['g', 'h', 'i']
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-8)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#__codelineno-18-9)>>> volume.fig.show()
    

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Volume.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/Volume.dark.svg#only-dark)

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * [TraceType](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceType "vectorbtpro.generic.plotting.TraceType")
  * [TraceUpdater](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater "vectorbtpro.generic.plotting.TraceUpdater")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.generic.plotting.TraceType.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.generic.plotting.TraceType.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.generic.plotting.TraceType.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.generic.plotting.TraceType.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.generic.plotting.TraceType.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.generic.plotting.TraceType.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.generic.plotting.TraceType.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.generic.plotting.TraceType.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.generic.plotting.TraceType.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.generic.plotting.TraceType.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.generic.plotting.TraceType.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.generic.plotting.TraceType.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.generic.plotting.TraceType.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.generic.plotting.TraceType.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.generic.plotting.TraceType.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.generic.plotting.TraceType.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.generic.plotting.TraceType.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.generic.plotting.TraceType.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.generic.plotting.TraceType.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.generic.plotting.TraceType.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.generic.plotting.TraceType.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.generic.plotting.TraceType.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.generic.plotting.TraceType.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.generic.plotting.TraceType.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.generic.plotting.TraceType.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.generic.plotting.TraceType.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.generic.plotting.TraceType.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.generic.plotting.TraceType.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.generic.plotting.TraceType.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.generic.plotting.TraceType.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.generic.plotting.TraceType.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.generic.plotting.TraceType.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.generic.plotting.TraceType.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.generic.plotting.TraceType.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.generic.plotting.TraceType.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.generic.plotting.TraceType.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.generic.plotting.TraceType.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.generic.plotting.TraceType.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.generic.plotting.TraceType.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.generic.plotting.TraceType.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.generic.plotting.TraceType.pprint")
  * [TraceType.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.generic.plotting.TraceType.config")
  * [TraceType.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.generic.plotting.TraceType.rec_state")
  * [TraceUpdater.fig](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.fig "vectorbtpro.generic.plotting.TraceUpdater.fig")
  * [TraceUpdater.traces](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.traces "vectorbtpro.generic.plotting.TraceUpdater.traces")
  * [TraceUpdater.update](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update "vectorbtpro.generic.plotting.TraceUpdater.update")
  * [TraceUpdater.update_trace](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.TraceUpdater.update_trace "vectorbtpro.generic.plotting.TraceUpdater.update_trace")


