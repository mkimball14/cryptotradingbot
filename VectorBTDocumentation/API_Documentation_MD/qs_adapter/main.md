qs_adapter

#  qs_adapter module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter "Permanent link")

Adapter class for QuantStats.

Note

Accessors do not utilize caching.

We can access the adapter from `ReturnsAccessor`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-2)>>> import quantstats as qs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-4)>>> np.random.seed(42)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-5)>>> rets = pd.Series(np.random.uniform(-0.1, 0.1, size=(100,)))
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-6)>>> bm_returns = pd.Series(np.random.uniform(-0.1, 0.1, size=(100,)))
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-8)>>> rets.vbt.returns.qs.r_squared(benchmark=bm_returns)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-0-9)0.0011582111228735541
    

Which is the same as:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-1-1)>>> qs.stats.r_squared(rets, bm_returns)
    

So why not just using `qs.stats`?

First, we can define all parameters such as benchmark returns once and avoid passing them repeatedly to every function. Second, vectorbt automatically translates parameters passed to `ReturnsAccessor` for the use in quantstats.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-1)>>> # Defaults that vectorbt understands
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-2)>>> ret_acc = rets.vbt.returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-3)...     bm_returns=bm_returns,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-4)...     freq='d',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-5)...     year_freq='365d',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-6)...     defaults=dict(risk_free=0.001)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-9)>>> ret_acc.qs.r_squared()
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-10)0.0011582111228735541
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-12)>>> ret_acc.qs.sharpe()
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-13)-1.9158923252075455
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-14)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-15)>>> # Defaults that only quantstats understands
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-16)>>> qs_defaults = dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-17)...     benchmark=bm_returns,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-18)...     periods=365,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-19)...     rf=0.001
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-20)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-21)>>> ret_acc_qs = rets.vbt.returns.qs(defaults=qs_defaults)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-22)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-23)>>> ret_acc_qs.r_squared()
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-24)0.0011582111228735541
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-25)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-26)>>> ret_acc_qs.sharpe()
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-2-27)-1.9158923252075455
    

The adapter automatically passes the returns to the particular function. It also merges the defaults defined in the settings, the defaults passed to `ReturnsAccessor`, and the defaults passed to [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter "vectorbtpro.returns.qs_adapter.QSAdapter") itself, and matches them with the argument names listed in the function's signature.

For example, the `periods` argument defaults to the annualization factor `ReturnsAccessor.ann_factor`, which itself is based on the `freq` argument. This makes the results produced by quantstats and vectorbt at least somewhat similar.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-3-1)>>> vbt.settings.wrapping['freq'] = 'h'
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-3-2)>>> vbt.settings.returns['year_freq'] = '365d'
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-3-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-3-4)>>> rets.vbt.returns.sharpe_ratio()  # ReturnsAccessor
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-3-5)-9.38160953971508
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-3-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-3-7)>>> rets.vbt.returns.qs.sharpe()  # quantstats via QSAdapter
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-3-8)-9.38160953971508
    

We can still override any argument by overriding its default or by passing it directly to the function:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-4-1)>>> rets.vbt.returns.qs(defaults=dict(periods=252)).sharpe()
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-4-2)-1.5912029345745982
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-4-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-4-4)>>> rets.vbt.returns.qs.sharpe(periods=252)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-4-5)-1.5912029345745982
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-4-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-4-7)>>> qs.stats.sharpe(rets)
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-4-8)-1.5912029345745982
    

* * *

## attach_qs_methods function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L125-L232 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.attach_qs_methods "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-5-1)attach_qs_methods(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-5-2)    cls,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-5-3)    replace_signature=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-5-4))
    

Class decorator to attach quantstats methods.

* * *

## QSAdapter class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L238-L279 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-6-1)QSAdapter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-6-2)    returns_acc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-6-3)    defaults=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-6-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-6-5))
    

Adapter class for quantstats.

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



* * *

### adjusted_sortino method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.adjusted_sortino "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-7-1)QSAdapter.adjusted_sortino(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-7-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-7-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-7-4)    rf=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-7-5)    periods=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-7-6)    annualize=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-7-7)    smart=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-7-8))
    

See `quantstats.stats.adjusted_sortino`.

* * *

### aggregate_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.aggregate_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-8-1)QSAdapter.aggregate_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-8-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-8-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-8-4)    period=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-8-5)    compounded=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-8-6))
    

See `quantstats.utils.aggregate_returns`.

* * *

### autocorr_penalty method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.autocorr_penalty "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-9-1)QSAdapter.autocorr_penalty(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-9-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-9-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-9-4)    prepare_returns=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-9-5))
    

See `quantstats.stats.autocorr_penalty`.

* * *

### avg_loss method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.avg_loss "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-10-1)QSAdapter.avg_loss(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-10-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-10-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-10-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-10-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-10-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-10-7))
    

See `quantstats.stats.avg_loss`.

* * *

### avg_return method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.avg_return "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-11-1)QSAdapter.avg_return(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-11-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-11-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-11-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-11-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-11-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-11-7))
    

See `quantstats.stats.avg_return`.

* * *

### avg_win method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.avg_win "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-12-1)QSAdapter.avg_win(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-12-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-12-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-12-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-12-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-12-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-12-7))
    

See `quantstats.stats.avg_win`.

* * *

### basic_report method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.basic_report "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-1)QSAdapter.basic_report(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-5)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-6)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-7)    figsize=(8, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-8)    display=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-9)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-10)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-11)    match_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-12)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-13-13))
    

See `quantstats.reports.basic`.

* * *

### best method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.best "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-14-1)QSAdapter.best(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-14-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-14-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-14-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-14-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-14-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-14-7))
    

See `quantstats.stats.best`.

* * *

### cagr method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.cagr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-15-1)QSAdapter.cagr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-15-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-15-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-15-4)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-15-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-15-6)    periods=252
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-15-7))
    

See `quantstats.stats.cagr`.

* * *

### calmar method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.calmar "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-16-1)QSAdapter.calmar(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-16-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-16-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-16-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-16-5))
    

See `quantstats.stats.calmar`.

* * *

### common_sense_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.common_sense_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-17-1)QSAdapter.common_sense_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-17-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-17-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-17-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-17-5))
    

See `quantstats.stats.common_sense_ratio`.

* * *

### comp method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.comp "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-18-1)QSAdapter.comp(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-18-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-18-3)    column=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-18-4))
    

See `quantstats.stats.comp`.

* * *

### compare method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.compare "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-1)QSAdapter.compare(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-4)    benchmark,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-5)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-6)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-7)    round_vals=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-8)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-19-9))
    

See `quantstats.stats.compare`.

* * *

### compsum method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.compsum "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-20-1)QSAdapter.compsum(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-20-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-20-3)    column=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-20-4))
    

See `quantstats.stats.compsum`.

* * *

### conditional_value_at_risk method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.conditional_value_at_risk "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-21-1)QSAdapter.conditional_value_at_risk(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-21-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-21-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-21-4)    sigma=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-21-5)    confidence=0.95,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-21-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-21-7))
    

See `quantstats.stats.conditional_value_at_risk`.

* * *

### consecutive_losses method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.consecutive_losses "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-22-1)QSAdapter.consecutive_losses(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-22-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-22-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-22-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-22-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-22-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-22-7))
    

See `quantstats.stats.consecutive_losses`.

* * *

### consecutive_wins method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.consecutive_wins "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-23-1)QSAdapter.consecutive_wins(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-23-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-23-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-23-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-23-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-23-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-23-7))
    

See `quantstats.stats.consecutive_wins`.

* * *

### cpc_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.cpc_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-24-1)QSAdapter.cpc_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-24-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-24-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-24-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-24-5))
    

See `quantstats.stats.cpc_index`.

* * *

### cvar method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.cvar "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-25-1)QSAdapter.cvar(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-25-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-25-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-25-4)    sigma=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-25-5)    confidence=0.95,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-25-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-25-7))
    

See `quantstats.stats.cvar`.

* * *

### defaults class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L265-L279 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.defaults "Permanent link")

Defaults for [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter "vectorbtpro.returns.qs_adapter.QSAdapter").

Merges `defaults` from [qs_adapter](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.qs_adapter "vectorbtpro._settings.qs_adapter"), `returns_acc.defaults` (with adapted naming), and `defaults` from [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter "vectorbtpro.returns.qs_adapter.QSAdapter").

* * *

### defaults_mapping class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L260-L263 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.defaults_mapping "Permanent link")

Common argument names in quantstats mapped to `ReturnsAccessor.defaults`.

* * *

### distribution method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.distribution "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-26-1)QSAdapter.distribution(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-26-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-26-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-26-4)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-26-5)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-26-6))
    

See `quantstats.stats.distribution`.

* * *

### expected_return method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.expected_return "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-27-1)QSAdapter.expected_return(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-27-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-27-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-27-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-27-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-27-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-27-7))
    

See `quantstats.stats.expected_return`.

* * *

### expected_shortfall method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.expected_shortfall "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-28-1)QSAdapter.expected_shortfall(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-28-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-28-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-28-4)    sigma=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-28-5)    confidence=0.95
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-28-6))
    

See `quantstats.stats.expected_shortfall`.

* * *

### exponential_stdev method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.exponential_stdev "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-29-1)QSAdapter.exponential_stdev(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-29-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-29-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-29-4)    window=30,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-29-5)    is_halflife=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-29-6))
    

See `quantstats.utils.exponential_stdev`.

* * *

### exposure method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.exposure "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-30-1)QSAdapter.exposure(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-30-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-30-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-30-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-30-5))
    

See `quantstats.stats.exposure`.

* * *

### full_report method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.full_report "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-1)QSAdapter.full_report(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-5)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-6)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-7)    figsize=(8, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-8)    display=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-9)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-10)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-11)    match_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-12)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-31-13))
    

See `quantstats.reports.full`.

* * *

### gain_to_pain_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.gain_to_pain_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-32-1)QSAdapter.gain_to_pain_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-32-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-32-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-32-4)    rf=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-32-5)    resolution='D'
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-32-6))
    

See `quantstats.stats.gain_to_pain_ratio`.

* * *

### geometric_mean method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.geometric_mean "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-33-1)QSAdapter.geometric_mean(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-33-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-33-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-33-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-33-5)    compounded=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-33-6))
    

See `quantstats.stats.geometric_mean`.

* * *

### ghpr method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.ghpr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-34-1)QSAdapter.ghpr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-34-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-34-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-34-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-34-5)    compounded=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-34-6))
    

See `quantstats.stats.ghpr`.

* * *

### greeks method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.greeks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-35-1)QSAdapter.greeks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-35-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-35-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-35-4)    benchmark,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-35-5)    periods=252.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-35-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-35-7))
    

See `quantstats.stats.greeks`.

* * *

### group_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.group_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-36-1)QSAdapter.group_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-36-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-36-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-36-4)    groupby,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-36-5)    compounded=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-36-6))
    

See `quantstats.utils.group_returns`.

* * *

### html_report method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.html_report "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-1)QSAdapter.html_report(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-5)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-6)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-7)    title='Strategy Tearsheet',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-8)    output=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-9)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-10)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-11)    download_filename='quantstats-tearsheet.html',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-12)    figfmt='svg',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-13)    template_path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-14)    match_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-15)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-37-16))
    

See `quantstats.reports.html`.

* * *

### implied_volatility method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.implied_volatility "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-38-1)QSAdapter.implied_volatility(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-38-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-38-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-38-4)    periods=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-38-5)    annualize=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-38-6))
    

See `quantstats.stats.implied_volatility`.

* * *

### information_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.information_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-39-1)QSAdapter.information_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-39-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-39-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-39-4)    benchmark,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-39-5)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-39-6))
    

See `quantstats.stats.information_ratio`.

* * *

### kelly_criterion method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.kelly_criterion "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-40-1)QSAdapter.kelly_criterion(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-40-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-40-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-40-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-40-5))
    

See `quantstats.stats.kelly_criterion`.

* * *

### kurtosis method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.kurtosis "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-41-1)QSAdapter.kurtosis(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-41-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-41-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-41-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-41-5))
    

See `quantstats.stats.kurtosis`.

* * *

### log_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.log_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-42-1)QSAdapter.log_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-42-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-42-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-42-4)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-42-5)    nperiods=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-42-6))
    

See `quantstats.utils.log_returns`.

* * *

### make_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.make_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-43-1)QSAdapter.make_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-43-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-43-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-43-4)    rebalance='1M',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-43-5)    period='max',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-43-6)    returns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-43-7)    match_dates=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-43-8))
    

See `quantstats.utils.make_index`.

* * *

### make_portfolio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.make_portfolio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-44-1)QSAdapter.make_portfolio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-44-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-44-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-44-4)    start_balance=100000.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-44-5)    mode='comp',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-44-6)    round_to=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-44-7))
    

See `quantstats.utils.make_portfolio`.

* * *

### metrics_report method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.metrics_report "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-1)QSAdapter.metrics_report(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-5)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-6)    display=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-7)    mode='basic',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-8)    sep=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-9)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-10)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-11)    prepare_returns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-12)    match_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-13)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-45-14))
    

See `quantstats.reports.metrics`.

* * *

### monthly_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.monthly_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-46-1)QSAdapter.monthly_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-46-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-46-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-46-4)    eoy=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-46-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-46-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-46-7))
    

See `quantstats.stats.monthly_returns`.

* * *

### omega method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.omega "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-47-1)QSAdapter.omega(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-47-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-47-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-47-4)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-47-5)    required_return=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-47-6)    periods=252
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-47-7))
    

See `quantstats.stats.omega`.

* * *

### outlier_loss_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.outlier_loss_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-48-1)QSAdapter.outlier_loss_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-48-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-48-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-48-4)    quantile=0.01,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-48-5)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-48-6))
    

See `quantstats.stats.outlier_loss_ratio`.

* * *

### outlier_win_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.outlier_win_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-49-1)QSAdapter.outlier_win_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-49-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-49-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-49-4)    quantile=0.99,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-49-5)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-49-6))
    

See `quantstats.stats.outlier_win_ratio`.

* * *

### outliers method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.outliers "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-50-1)QSAdapter.outliers(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-50-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-50-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-50-4)    quantile=0.95
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-50-5))
    

See `quantstats.stats.outliers`.

* * *

### payoff_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.payoff_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-51-1)QSAdapter.payoff_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-51-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-51-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-51-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-51-5))
    

See `quantstats.stats.payoff_ratio`.

* * *

### plot_daily_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_daily_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-1)QSAdapter.plot_daily_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-4)    benchmark,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-5)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-6)    figsize=(10, 4),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-7)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-8)    lw=0.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-9)    log_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-10)    ylabel='Returns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-11)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-12)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-13)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-14)    prepare_returns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-15)    active=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-52-16))
    

See `quantstats.plots.daily_returns`.

* * *

### plot_distribution method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_distribution "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-1)QSAdapter.plot_distribution(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-4)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-5)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-6)    ylabel=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-7)    figsize=(10, 6),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-8)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-9)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-10)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-11)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-12)    title=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-13)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-53-14))
    

See `quantstats.plots.distribution`.

* * *

### plot_drawdown method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_drawdown "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-1)QSAdapter.plot_drawdown(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-4)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-5)    figsize=(10, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-6)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-7)    lw=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-8)    log_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-9)    match_volatility=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-10)    compound=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-11)    ylabel='Drawdown',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-12)    resample=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-13)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-14)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-15)    show=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-54-16))
    

See `quantstats.plots.drawdown`.

* * *

### plot_drawdowns_periods method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_drawdowns_periods "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-1)QSAdapter.plot_drawdowns_periods(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-4)    periods=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-5)    lw=1.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-6)    log_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-7)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-8)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-9)    title=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-10)    figsize=(10, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-11)    ylabel=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-12)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-13)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-14)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-15)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-16)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-55-17))
    

See `quantstats.plots.drawdowns_periods`.

* * *

### plot_earnings method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_earnings "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-1)QSAdapter.plot_earnings(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-4)    start_balance=100000.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-5)    mode='comp',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-6)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-7)    figsize=(10, 6),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-8)    title='Portfolio Earnings',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-9)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-10)    lw=1.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-11)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-12)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-13)    show=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-56-14))
    

See `quantstats.plots.earnings`.

* * *

### plot_histogram method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_histogram "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-1)QSAdapter.plot_histogram(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-5)    resample='ME',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-6)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-7)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-8)    figsize=(10, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-9)    ylabel=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-10)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-11)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-12)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-13)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-14)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-57-15))
    

See `quantstats.plots.histogram`.

* * *

### plot_log_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_log_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-1)QSAdapter.plot_log_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-5)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-6)    figsize=(10, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-7)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-8)    lw=1.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-9)    match_volatility=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-10)    compound=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-11)    cumulative=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-12)    resample=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-13)    ylabel='Cumulative Returns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-14)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-15)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-16)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-17)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-58-18))
    

See `quantstats.plots.log_returns`.

* * *

### plot_monthly_heatmap method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_monthly_heatmap "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-1)QSAdapter.plot_monthly_heatmap(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-5)    annot_size=13,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-6)    figsize=(8, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-7)    cbar=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-8)    square=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-9)    returns_label='Strategy',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-10)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-11)    eoy=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-12)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-13)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-14)    ylabel=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-15)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-16)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-17)    active=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-59-18))
    

See `quantstats.plots.monthly_heatmap`.

* * *

### plot_monthly_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_monthly_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-1)QSAdapter.plot_monthly_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-4)    annot_size=9,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-5)    figsize=(10, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-6)    cbar=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-7)    square=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-8)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-9)    eoy=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-10)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-11)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-12)    ylabel=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-13)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-14)    show=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-60-15))
    

See `quantstats.plots.monthly_returns`.

* * *

### plot_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-1)QSAdapter.plot_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-5)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-6)    figsize=(10, 6),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-7)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-8)    lw=1.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-9)    match_volatility=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-10)    compound=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-11)    cumulative=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-12)    resample=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-13)    ylabel='Cumulative Returns',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-14)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-15)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-16)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-17)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-61-18))
    

See `quantstats.plots.returns`.

* * *

### plot_rolling_beta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_rolling_beta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-1)QSAdapter.plot_rolling_beta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-4)    benchmark,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-5)    window1=126,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-6)    window1_label='6-Months',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-7)    window2=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-8)    window2_label='12-Months',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-9)    lw=1.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-10)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-11)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-12)    figsize=(10, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-13)    ylabel=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-14)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-15)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-16)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-17)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-62-18))
    

See `quantstats.plots.rolling_beta`.

* * *

### plot_rolling_sharpe method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_rolling_sharpe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-1)QSAdapter.plot_rolling_sharpe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-5)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-6)    period=126,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-7)    period_label='6-Months',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-8)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-9)    lw=1.25,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-10)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-11)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-12)    figsize=(10, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-13)    ylabel='Sharpe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-14)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-15)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-16)    show=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-63-17))
    

See `quantstats.plots.rolling_sharpe`.

* * *

### plot_rolling_sortino method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_rolling_sortino "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-1)QSAdapter.plot_rolling_sortino(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-5)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-6)    period=126,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-7)    period_label='6-Months',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-8)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-9)    lw=1.25,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-10)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-11)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-12)    figsize=(10, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-13)    ylabel='Sortino',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-14)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-15)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-16)    show=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-64-17))
    

See `quantstats.plots.rolling_sortino`.

* * *

### plot_rolling_volatility method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_rolling_volatility "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-1)QSAdapter.plot_rolling_volatility(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-5)    period=126,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-6)    period_label='6-Months',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-7)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-8)    lw=1.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-9)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-10)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-11)    figsize=(10, 3),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-12)    ylabel='Volatility',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-13)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-14)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-15)    show=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-65-16))
    

See `quantstats.plots.rolling_volatility`.

* * *

### plot_snapshot method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_snapshot "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-1)QSAdapter.plot_snapshot(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-4)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-5)    figsize=(10, 8),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-6)    title='Portfolio Summary',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-7)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-8)    lw=1.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-9)    mode='comp',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-10)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-11)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-12)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-13)    log_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-14)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-66-15))
    

See `quantstats.plots.snapshot`.

* * *

### plot_yearly_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plot_yearly_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-1)QSAdapter.plot_yearly_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-5)    fontname='Arial',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-6)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-7)    hlw=1.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-8)    hlcolor='red',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-9)    hllabel='',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-10)    match_volatility=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-11)    log_scale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-12)    figsize=(10, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-13)    ylabel=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-14)    subtitle=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-15)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-16)    savefig=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-17)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-18)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-67-19))
    

See `quantstats.plots.yearly_returns`.

* * *

### plots_report method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.plots_report "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-1)QSAdapter.plots_report(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-4)    benchmark=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-5)    grayscale=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-6)    figsize=(8, 5),
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-7)    mode='basic',
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-8)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-9)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-10)    prepare_returns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-11)    match_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-12)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-68-13))
    

See `quantstats.reports.plots`.

* * *

### profit_factor method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.profit_factor "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-69-1)QSAdapter.profit_factor(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-69-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-69-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-69-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-69-5))
    

See `quantstats.stats.profit_factor`.

* * *

### profit_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.profit_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-70-1)QSAdapter.profit_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-70-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-70-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-70-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-70-5))
    

See `quantstats.stats.profit_ratio`.

* * *

### r2 method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.r2 "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-71-1)QSAdapter.r2(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-71-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-71-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-71-4)    benchmark
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-71-5))
    

See `quantstats.stats.r2`.

* * *

### r_squared method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.r_squared "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-72-1)QSAdapter.r_squared(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-72-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-72-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-72-4)    benchmark,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-72-5)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-72-6))
    

See `quantstats.stats.r_squared`.

* * *

### rar method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.rar "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-73-1)QSAdapter.rar(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-73-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-73-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-73-4)    rf=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-73-5))
    

See `quantstats.stats.rar`.

* * *

### recovery_factor method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.recovery_factor "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-74-1)QSAdapter.recovery_factor(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-74-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-74-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-74-4)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-74-5)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-74-6))
    

See `quantstats.stats.recovery_factor`.

* * *

### remove_outliers method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.remove_outliers "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-75-1)QSAdapter.remove_outliers(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-75-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-75-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-75-4)    quantile=0.95
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-75-5))
    

See `quantstats.stats.remove_outliers`.

* * *

### returns_acc class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L255-L258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.returns_acc "Permanent link")

Returns accessor.

* * *

### risk_of_ruin method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.risk_of_ruin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-76-1)QSAdapter.risk_of_ruin(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-76-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-76-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-76-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-76-5))
    

See `quantstats.stats.risk_of_ruin`.

* * *

### risk_return_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.risk_return_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-77-1)QSAdapter.risk_return_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-77-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-77-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-77-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-77-5))
    

See `quantstats.stats.risk_return_ratio`.

* * *

### rolling_greeks method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.rolling_greeks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-78-1)QSAdapter.rolling_greeks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-78-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-78-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-78-4)    benchmark,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-78-5)    periods=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-78-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-78-7))
    

See `quantstats.stats.rolling_greeks`.

* * *

### rolling_sharpe method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.rolling_sharpe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-1)QSAdapter.rolling_sharpe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-4)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-5)    rolling_period=126,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-6)    annualize=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-7)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-8)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-79-9))
    

See `quantstats.stats.rolling_sharpe`.

* * *

### rolling_sortino method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.rolling_sortino "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-1)QSAdapter.rolling_sortino(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-4)    rf=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-5)    rolling_period=126,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-6)    annualize=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-7)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-80-9))
    

See `quantstats.stats.rolling_sortino`.

* * *

### rolling_volatility method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.rolling_volatility "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-81-1)QSAdapter.rolling_volatility(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-81-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-81-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-81-4)    rolling_period=126,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-81-5)    periods_per_year=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-81-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-81-7))
    

See `quantstats.stats.rolling_volatility`.

* * *

### ror method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.ror "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-82-1)QSAdapter.ror(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-82-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-82-3)    column=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-82-4))
    

See `quantstats.stats.ror`.

* * *

### serenity_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.serenity_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-83-1)QSAdapter.serenity_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-83-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-83-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-83-4)    rf=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-83-5))
    

See `quantstats.stats.serenity_index`.

* * *

### sharpe method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.sharpe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-84-1)QSAdapter.sharpe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-84-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-84-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-84-4)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-84-5)    periods=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-84-6)    annualize=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-84-7)    smart=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-84-8))
    

See `quantstats.stats.sharpe`.

* * *

### skew method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.skew "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-85-1)QSAdapter.skew(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-85-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-85-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-85-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-85-5))
    

See `quantstats.stats.skew`.

* * *

### smart_sharpe method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.smart_sharpe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-86-1)QSAdapter.smart_sharpe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-86-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-86-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-86-4)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-86-5)    periods=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-86-6)    annualize=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-86-7))
    

See `quantstats.stats.smart_sharpe`.

* * *

### smart_sortino method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.smart_sortino "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-87-1)QSAdapter.smart_sortino(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-87-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-87-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-87-4)    rf=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-87-5)    periods=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-87-6)    annualize=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-87-7))
    

See `quantstats.stats.smart_sortino`.

* * *

### sortino method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.sortino "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-88-1)QSAdapter.sortino(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-88-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-88-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-88-4)    rf=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-88-5)    periods=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-88-6)    annualize=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-88-7)    smart=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-88-8))
    

See `quantstats.stats.sortino`.

* * *

### tail_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.tail_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-89-1)QSAdapter.tail_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-89-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-89-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-89-4)    cutoff=0.95,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-89-5)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-89-6))
    

See `quantstats.stats.tail_ratio`.

* * *

### to_drawdown_series method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.to_drawdown_series "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-90-1)QSAdapter.to_drawdown_series(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-90-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-90-3)    column=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-90-4))
    

See `quantstats.stats.to_drawdown_series`.

* * *

### to_excess_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.to_excess_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-91-1)QSAdapter.to_excess_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-91-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-91-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-91-4)    rf,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-91-5)    nperiods=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-91-6))
    

See `quantstats.utils.to_excess_returns`.

* * *

### to_log_returns method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.to_log_returns "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-92-1)QSAdapter.to_log_returns(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-92-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-92-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-92-4)    rf=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-92-5)    nperiods=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-92-6))
    

See `quantstats.utils.to_log_returns`.

* * *

### to_prices method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.to_prices "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-93-1)QSAdapter.to_prices(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-93-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-93-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-93-4)    base=100000.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-93-5))
    

See `quantstats.utils.to_prices`.

* * *

### treynor_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.treynor_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-94-1)QSAdapter.treynor_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-94-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-94-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-94-4)    benchmark,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-94-5)    periods=252.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-94-6)    rf=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-94-7))
    

See `quantstats.stats.treynor_ratio`.

* * *

### ulcer_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.ulcer_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-95-1)QSAdapter.ulcer_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-95-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-95-3)    column=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-95-4))
    

See `quantstats.stats.ulcer_index`.

* * *

### ulcer_performance_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.ulcer_performance_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-96-1)QSAdapter.ulcer_performance_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-96-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-96-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-96-4)    rf=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-96-5))
    

See `quantstats.stats.ulcer_performance_index`.

* * *

### upi method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.upi "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-97-1)QSAdapter.upi(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-97-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-97-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-97-4)    rf=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-97-5))
    

See `quantstats.stats.upi`.

* * *

### value_at_risk method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.value_at_risk "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-98-1)QSAdapter.value_at_risk(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-98-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-98-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-98-4)    sigma=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-98-5)    confidence=0.95,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-98-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-98-7))
    

See `quantstats.stats.value_at_risk`.

* * *

### var method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.var "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-99-1)QSAdapter.var(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-99-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-99-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-99-4)    sigma=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-99-5)    confidence=0.95,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-99-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-99-7))
    

See `quantstats.stats.var`.

* * *

### volatility method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.volatility "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-100-1)QSAdapter.volatility(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-100-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-100-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-100-4)    periods=252,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-100-5)    annualize=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-100-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-100-7))
    

See `quantstats.stats.volatility`.

* * *

### win_loss_ratio method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.win_loss_ratio "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-101-1)QSAdapter.win_loss_ratio(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-101-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-101-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-101-4)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-101-5))
    

See `quantstats.stats.win_loss_ratio`.

* * *

### win_rate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.win_rate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-102-1)QSAdapter.win_rate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-102-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-102-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-102-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-102-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-102-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-102-7))
    

See `quantstats.stats.win_rate`.

* * *

### worst method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/returns/qs_adapter.py#L141-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter.worst "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-103-1)QSAdapter.worst(
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-103-2)    *,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-103-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-103-4)    aggregate=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-103-5)    compounded=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-103-6)    prepare_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#__codelineno-103-7))
    

See `quantstats.stats.worst`.
