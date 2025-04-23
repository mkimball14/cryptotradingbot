factory

#  factory module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/factory.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#vectorbtpro.signals.factory "Permanent link")

Factory for building signal generators.

The signal factory class [SignalFactory](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#vectorbtpro.signals.factory.SignalFactory "vectorbtpro.signals.factory.SignalFactory") extends [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory "vectorbtpro.indicators.factory.IndicatorFactory") to offer a convenient way to create signal generators of any complexity. By providing it with information such as entry and exit functions and the names of inputs, parameters, and outputs, it will create a stand-alone class capable of generating signals for an arbitrary combination of inputs and parameters.

* * *

## SignalFactory class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/factory.py#L41-L955 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#vectorbtpro.signals.factory.SignalFactory "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-0-1)SignalFactory(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-0-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-0-3)    mode=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-0-4)    input_names=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-0-5)    attr_settings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-0-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-0-7))
    

A factory for building signal generators.

Extends [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory "vectorbtpro.indicators.factory.IndicatorFactory") with place functions.

Generates a fixed number of outputs (depending upon `mode`). If you need to generate other outputs, use in-place outputs (via `in_output_names`).

See [FactoryMode](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.FactoryMode "vectorbtpro.signals.enums.FactoryMode") for supported generation modes.

Other arguments are passed to [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory "vectorbtpro.indicators.factory.IndicatorFactory").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory "vectorbtpro.indicators.factory.IndicatorFactory")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.indicators.factory.IndicatorFactory.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.indicators.factory.IndicatorFactory.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.indicators.factory.IndicatorFactory.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.indicators.factory.IndicatorFactory.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.indicators.factory.IndicatorFactory.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.indicators.factory.IndicatorFactory.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.indicators.factory.IndicatorFactory.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.indicators.factory.IndicatorFactory.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.indicators.factory.IndicatorFactory.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.indicators.factory.IndicatorFactory.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.indicators.factory.IndicatorFactory.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.indicators.factory.IndicatorFactory.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.indicators.factory.IndicatorFactory.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.indicators.factory.IndicatorFactory.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.indicators.factory.IndicatorFactory.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.indicators.factory.IndicatorFactory.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.indicators.factory.IndicatorFactory.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.indicators.factory.IndicatorFactory.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.indicators.factory.IndicatorFactory.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.indicators.factory.IndicatorFactory.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.indicators.factory.IndicatorFactory.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.indicators.factory.IndicatorFactory.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.indicators.factory.IndicatorFactory.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.indicators.factory.IndicatorFactory.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.indicators.factory.IndicatorFactory.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.indicators.factory.IndicatorFactory.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.indicators.factory.IndicatorFactory.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.indicators.factory.IndicatorFactory.set_settings")
  * [IndicatorFactory.Indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.Indicator "vectorbtpro.indicators.factory.IndicatorFactory.Indicator")
  * [IndicatorFactory.attr_settings](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.attr_settings "vectorbtpro.indicators.factory.IndicatorFactory.attr_settings")
  * [IndicatorFactory.class_docstring](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.class_docstring "vectorbtpro.indicators.factory.IndicatorFactory.class_docstring")
  * [IndicatorFactory.class_name](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.class_name "vectorbtpro.indicators.factory.IndicatorFactory.class_name")
  * [IndicatorFactory.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.indicators.factory.IndicatorFactory.config")
  * [IndicatorFactory.custom_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.custom_indicators "vectorbtpro.indicators.factory.IndicatorFactory.custom_indicators")
  * [IndicatorFactory.deregister_custom_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.deregister_custom_indicator "vectorbtpro.indicators.factory.IndicatorFactory.deregister_custom_indicator")
  * [IndicatorFactory.find_smc_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.find_smc_indicator "vectorbtpro.indicators.factory.IndicatorFactory.find_smc_indicator")
  * [IndicatorFactory.find_ta_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.find_ta_indicator "vectorbtpro.indicators.factory.IndicatorFactory.find_ta_indicator")
  * [IndicatorFactory.find_technical_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.find_technical_indicator "vectorbtpro.indicators.factory.IndicatorFactory.find_technical_indicator")
  * [IndicatorFactory.from_custom_techcon](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_custom_techcon "vectorbtpro.indicators.factory.IndicatorFactory.from_custom_techcon")
  * [IndicatorFactory.from_expr](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_expr "vectorbtpro.indicators.factory.IndicatorFactory.from_expr")
  * [IndicatorFactory.from_pandas_ta](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_pandas_ta "vectorbtpro.indicators.factory.IndicatorFactory.from_pandas_ta")
  * [IndicatorFactory.from_smc](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_smc "vectorbtpro.indicators.factory.IndicatorFactory.from_smc")
  * [IndicatorFactory.from_ta](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_ta "vectorbtpro.indicators.factory.IndicatorFactory.from_ta")
  * [IndicatorFactory.from_talib](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_talib "vectorbtpro.indicators.factory.IndicatorFactory.from_talib")
  * [IndicatorFactory.from_techcon](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_techcon "vectorbtpro.indicators.factory.IndicatorFactory.from_techcon")
  * [IndicatorFactory.from_technical](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_technical "vectorbtpro.indicators.factory.IndicatorFactory.from_technical")
  * [IndicatorFactory.from_wqa101](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_wqa101 "vectorbtpro.indicators.factory.IndicatorFactory.from_wqa101")
  * [IndicatorFactory.get_custom_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.get_custom_indicator "vectorbtpro.indicators.factory.IndicatorFactory.get_custom_indicator")
  * [IndicatorFactory.get_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.get_indicator "vectorbtpro.indicators.factory.IndicatorFactory.get_indicator")
  * [IndicatorFactory.in_output_names](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.in_output_names "vectorbtpro.indicators.factory.IndicatorFactory.in_output_names")
  * [IndicatorFactory.input_names](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.input_names "vectorbtpro.indicators.factory.IndicatorFactory.input_names")
  * [IndicatorFactory.lazy_outputs](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.lazy_outputs "vectorbtpro.indicators.factory.IndicatorFactory.lazy_outputs")
  * [IndicatorFactory.list_builtin_locations](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_builtin_locations "vectorbtpro.indicators.factory.IndicatorFactory.list_builtin_locations")
  * [IndicatorFactory.list_custom_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_custom_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_custom_indicators")
  * [IndicatorFactory.list_custom_locations](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_custom_locations "vectorbtpro.indicators.factory.IndicatorFactory.list_custom_locations")
  * [IndicatorFactory.list_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_indicators")
  * [IndicatorFactory.list_locations](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_locations "vectorbtpro.indicators.factory.IndicatorFactory.list_locations")
  * [IndicatorFactory.list_pandas_ta_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_pandas_ta_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_pandas_ta_indicators")
  * [IndicatorFactory.list_smc_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_smc_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_smc_indicators")
  * [IndicatorFactory.list_ta_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_ta_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_ta_indicators")
  * [IndicatorFactory.list_talib_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_talib_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_talib_indicators")
  * [IndicatorFactory.list_techcon_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_techcon_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_techcon_indicators")
  * [IndicatorFactory.list_technical_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_technical_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_technical_indicators")
  * [IndicatorFactory.list_vbt_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_vbt_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_vbt_indicators")
  * [IndicatorFactory.list_wqa101_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_wqa101_indicators "vectorbtpro.indicators.factory.IndicatorFactory.list_wqa101_indicators")
  * [IndicatorFactory.match_location](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.match_location "vectorbtpro.indicators.factory.IndicatorFactory.match_location")
  * [IndicatorFactory.metrics](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.metrics "vectorbtpro.indicators.factory.IndicatorFactory.metrics")
  * [IndicatorFactory.module_name](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.module_name "vectorbtpro.indicators.factory.IndicatorFactory.module_name")
  * [IndicatorFactory.output_flags](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.output_flags "vectorbtpro.indicators.factory.IndicatorFactory.output_flags")
  * [IndicatorFactory.output_names](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.output_names "vectorbtpro.indicators.factory.IndicatorFactory.output_names")
  * [IndicatorFactory.param_names](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.param_names "vectorbtpro.indicators.factory.IndicatorFactory.param_names")
  * [IndicatorFactory.parse_pandas_ta_config](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.parse_pandas_ta_config "vectorbtpro.indicators.factory.IndicatorFactory.parse_pandas_ta_config")
  * [IndicatorFactory.parse_smc_config](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.parse_smc_config "vectorbtpro.indicators.factory.IndicatorFactory.parse_smc_config")
  * [IndicatorFactory.parse_ta_config](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.parse_ta_config "vectorbtpro.indicators.factory.IndicatorFactory.parse_ta_config")
  * [IndicatorFactory.parse_technical_config](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.parse_technical_config "vectorbtpro.indicators.factory.IndicatorFactory.parse_technical_config")
  * [IndicatorFactory.plots_defaults](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.plots_defaults "vectorbtpro.indicators.factory.IndicatorFactory.plots_defaults")
  * [IndicatorFactory.prepend_name](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.prepend_name "vectorbtpro.indicators.factory.IndicatorFactory.prepend_name")
  * [IndicatorFactory.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.indicators.factory.IndicatorFactory.rec_state")
  * [IndicatorFactory.register_custom_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.register_custom_indicator "vectorbtpro.indicators.factory.IndicatorFactory.register_custom_indicator")
  * [IndicatorFactory.short_name](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.short_name "vectorbtpro.indicators.factory.IndicatorFactory.short_name")
  * [IndicatorFactory.split_indicator_name](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.split_indicator_name "vectorbtpro.indicators.factory.IndicatorFactory.split_indicator_name")
  * [IndicatorFactory.stats_defaults](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.stats_defaults "vectorbtpro.indicators.factory.IndicatorFactory.stats_defaults")
  * [IndicatorFactory.subplots](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.subplots "vectorbtpro.indicators.factory.IndicatorFactory.subplots")
  * [IndicatorFactory.with_apply_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.with_apply_func "vectorbtpro.indicators.factory.IndicatorFactory.with_apply_func")
  * [IndicatorFactory.with_custom_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.with_custom_func "vectorbtpro.indicators.factory.IndicatorFactory.with_custom_func")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.indicators.factory.IndicatorFactory.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.indicators.factory.IndicatorFactory.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.indicators.factory.IndicatorFactory.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.indicators.factory.IndicatorFactory.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.indicators.factory.IndicatorFactory.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.indicators.factory.IndicatorFactory.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.indicators.factory.IndicatorFactory.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.indicators.factory.IndicatorFactory.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.indicators.factory.IndicatorFactory.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.indicators.factory.IndicatorFactory.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.indicators.factory.IndicatorFactory.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.indicators.factory.IndicatorFactory.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.indicators.factory.IndicatorFactory.pprint")



* * *

### mode class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/factory.py#L208-L211 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#vectorbtpro.signals.factory.SignalFactory.mode "Permanent link")

Factory mode.

* * *

### with_place_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/signals/factory.py#L213-L955 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#vectorbtpro.signals.factory.SignalFactory.with_place_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-1)SignalFactory.with_place_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-2)    entry_place_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-3)    exit_place_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-4)    generate_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-5)    generate_ex_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-6)    generate_enex_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-7)    cache_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-8)    entry_settings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-9)    exit_settings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-10)    cache_settings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-11)    jit_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-12)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-13)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-1-14))
    

Build signal generator class around entry and exit placement functions.

A placement function is simply a function that places signals. There are two types of it: entry placement function and exit placement function. Each placement function takes broadcast time series, broadcast in-place output time series, broadcast parameter arrays, and other arguments, and returns an array of indices corresponding to chosen signals. See [generate_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_nb "vectorbtpro.signals.nb.generate_nb").

**Args**

**`entry_place_func_nb`** : `callable`
    

`place_func_nb` that returns indices of entries.

Defaults to [first_place_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.first_place_nb "vectorbtpro.signals.nb.first_place_nb") for `FactoryMode.Chain`.

**`exit_place_func_nb`** : `callable`
    `place_func_nb` that returns indices of exits.
**`generate_func_nb`** : `callable`
    

Entry generation function.

Defaults to [generate_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_nb "vectorbtpro.signals.nb.generate_nb").

**`generate_ex_func_nb`** : `callable`
    

Exit generation function.

Defaults to [generate_ex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_ex_nb "vectorbtpro.signals.nb.generate_ex_nb").

**`generate_enex_func_nb`** : `callable`
    

Entry and exit generation function.

Defaults to [generate_enex_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/nb/#vectorbtpro.signals.nb.generate_enex_nb "vectorbtpro.signals.nb.generate_enex_nb").

**`cache_func`** : `callable`
    

A caching function to preprocess data beforehand.

All returned objects will be passed as last arguments to placement functions.

**`entry_settings`** : `dict`
    Settings dict for `entry_place_func_nb`.
**`exit_settings`** : `dict`
    Settings dict for `exit_place_func_nb`.
**`cache_settings`** : `dict`
    Settings dict for `cache_func`.
**`jit_kwargs`** : `dict`
    

Keyword arguments passed to `@njit` decorator of the parameter selection function.

By default, has `nogil` set to True.

**`jitted`** : `any`
    

See [resolve_jitted_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitted_option "vectorbtpro.utils.jitting.resolve_jitted_option").

Gets applied to generation functions only. If the respective generation function is not jitted, then the apply function won't be jitted as well.

**`**kwargs`**
    Keyword arguments passed to `IndicatorFactory.with_custom_func`.

Note

Choice functions must be Numba-compiled.

Which inputs, parameters and arguments to pass to each function must be explicitly indicated in the function's settings dict. By default, nothing is passed.

Passing keyword arguments directly to the placement functions is not supported. Use `pass_kwargs` in a settings dict to pass keyword arguments as positional.

Settings dict of each function can have the following keys:

**Attributes**

**`pass_inputs`** : `list` of `str`
    

Input names to pass to the placement function.

Defaults to []. Order matters. Each name must be in `input_names`.

**`pass_in_outputs`** : `list` of `str`
    

In-place output names to pass to the placement function.

Defaults to []. Order matters. Each name must be in `in_output_names`.

**`pass_params`** : `list` of `str`
    

Parameter names to pass to the placement function.

Defaults to []. Order matters. Each name must be in `param_names`.

**`pass_kwargs`** : `dict`, `list` of `str` or `list` of `tuple`
    

Keyword arguments from `kwargs` dict to pass as positional arguments to the placement function.

Defaults to []. Order matters.

If any element is a tuple, must contain the name and the default value. If any element is a string, the default value is None.

Built-in keys include:

  * `input_shape`: Input shape if no input time series passed. Default is provided by the pipeline if `pass_input_shape` is True.
  * `wait`: Number of ticks to wait before placing signals. Default is 1.
  * `until_next`: Whether to place signals up to the next entry signal. Default is True. Applied in `generate_ex_func_nb` only.
  * `skip_until_exit`: Whether to skip processing entry signals until the next exit. Default is False. Applied in `generate_ex_func_nb` only.
  * `pick_first`: Whether to stop as soon as the first exit signal is found. Default is False with `FactoryMode.Entries`, otherwise is True.
  * `temp_idx_arr`: Empty integer array used to temporarily store indices. Default is an automatically generated array of shape `input_shape[0]`. You can also pass `temp_idx_arr1`, `temp_idx_arr2`, etc. to generate multiple.


**`pass_cache`** : `bool`
    

Whether to pass cache from `cache_func` to the placement function.

Defaults to False. Cache is passed unpacked.

The following arguments can be passed to `run` and `run_combs` methods:

**Args**

**`*args`**
    Can be used instead of `place_args`.
**`place_args`** : `tuple`
    Arguments passed to any placement function (depending on the mode).
**`entry_place_args`** : `tuple`
    Arguments passed to the entry placement function.
**`exit_place_args`** : `tuple`
    Arguments passed to the exit placement function.
**`entry_args`** : `tuple`
    Alias for `entry_place_args`.
**`exit_args`** : `tuple`
    Alias for `exit_place_args`.
**`cache_args`** : `tuple`
    Arguments passed to the cache function.
**`entry_kwargs`** : `tuple`
    Settings for the entry placement function. Also contains arguments passed as positional if in `pass_kwargs`.
**`exit_kwargs`** : `tuple`
    Settings for the exit placement function. Also contains arguments passed as positional if in `pass_kwargs`.
**`cache_kwargs`** : `tuple`
    Settings for the cache function. Also contains arguments passed as positional if in `pass_kwargs`.
**`return_cache`** : `bool`
    Whether to return only cache.
**`use_cache`** : `any`
    Cache to use.
**`**kwargs`**
    Default keyword arguments (depending on the mode).

For more arguments, see [IndicatorBase.run_pipeline](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase.run_pipeline "vectorbtpro.indicators.factory.IndicatorBase.run_pipeline").

**Usage**

  * The simplest signal indicator that places True at the very first index:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-3)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-4)... def entry_place_func_nb(c):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-5)...     c.out[0] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-6)...     return 0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-8)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-9)... def exit_place_func_nb(c):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-10)...     c.out[0] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-11)...     return 0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-13)>>> MySignals = vbt.SignalFactory().with_place_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-14)...     entry_place_func_nb=entry_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-15)...     exit_place_func_nb=exit_place_func_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-16)...     entry_kwargs=dict(wait=1),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-17)...     exit_kwargs=dict(wait=1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-18)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-19)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-20)>>> my_sig = MySignals.run(input_shape=(3, 3))
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-21)>>> my_sig.entries
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-22)       0      1      2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-23)0   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-24)1  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-25)2   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-26)>>> my_sig.exits
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-27)       0      1      2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-28)0  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-29)1   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-2-30)2  False  False  False
    

  * Take the first entry and place an exit after waiting `n` ticks. Find the next entry and repeat. Test three different `n` values.


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-1)>>> from vectorbtpro.signals.factory import SignalFactory
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-3)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-4)... def wait_place_nb(c, n):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-5)...     if n < len(c.out):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-6)...         c.out[n] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-7)...         return n
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-8)...     return -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-10)>>> # Build signal generator
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-11)>>> MySignals = SignalFactory(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-12)...     mode='chain',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-13)...     param_names=['n']
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-14)... ).with_place_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-15)...     exit_place_func_nb=wait_place_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-16)...     exit_settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-17)...         pass_params=['n']
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-18)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-19)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-20)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-21)>>> # Run signal generator
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-22)>>> entries = [True, True, True, True, True]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-23)>>> my_sig = MySignals.run(entries, [0, 1, 2])
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-24)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-25)>>> my_sig.entries  # input entries
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-26)custom_n     0     1     2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-27)0         True  True  True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-28)1         True  True  True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-29)2         True  True  True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-30)3         True  True  True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-31)4         True  True  True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-32)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-33)>>> my_sig.new_entries  # output entries
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-34)custom_n      0      1      2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-35)0          True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-36)1         False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-37)2          True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-38)3         False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-39)4          True  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-40)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-41)>>> my_sig.exits  # output exits
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-42)custom_n      0      1      2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-43)0         False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-44)1          True  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-45)2         False   True  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-46)3          True  False   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-3-47)4         False  False  False
    

  * To combine multiple iterative signals, you would need to create a custom placement function. Here is an example of combining two random generators using "OR" rule (the first signal wins):


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-1)>>> from vectorbtpro.indicators.configs import flex_elem_param_config
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-2)>>> from vectorbtpro.signals.factory import SignalFactory
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-3)>>> from vectorbtpro.signals.nb import rand_by_prob_place_nb
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-5)>>> # Enum to distinguish random generators
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-6)>>> RandType = namedtuple('RandType', ['R1', 'R2'])(0, 1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-8)>>> # Define exit placement function
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-9)>>> @njit
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-10)... def rand_exit_place_nb(c, rand_type, prob1, prob2):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-11)...     for out_i in range(len(c.out)):
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-12)...         if np.random.uniform(0, 1) < prob1:
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-13)...             c.out[out_i] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-14)...             rand_type[c.from_i + out_i] = RandType.R1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-15)...             return out_i
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-16)...         if np.random.uniform(0, 1) < prob2:
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-17)...             c.out[out_i] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-18)...             rand_type[c.from_i + out_i] = RandType.R2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-19)...             return out_i
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-20)...     return -1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-21)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-22)>>> # Build signal generator
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-23)>>> MySignals = SignalFactory(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-24)...     mode='chain',
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-25)...     in_output_names=['rand_type'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-26)...     param_names=['prob1', 'prob2'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-27)...     attr_settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-28)...         rand_type=dict(dtype=RandType)  # creates rand_type_readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-29)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-30)... ).with_place_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-31)...     exit_place_func_nb=rand_exit_place_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-32)...     exit_settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-33)...         pass_in_outputs=['rand_type'],
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-34)...         pass_params=['prob1', 'prob2']
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-35)...     ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-36)...     param_settings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-37)...         prob1=flex_elem_param_config,  # param per frame/row/col/element
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-38)...         prob2=flex_elem_param_config
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-39)...     ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-40)...     rand_type=-1  # fill with this value
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-41)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-42)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-43)>>> # Run signal generator
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-44)>>> entries = [True, True, True, True, True]
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-45)>>> my_sig = MySignals.run(entries, [0., 1.], [0., 1.], param_product=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-46)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-47)>>> my_sig.new_entries
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-48)custom_prob1           0.0           1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-49)custom_prob2    0.0    1.0    0.0    1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-50)0              True   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-51)1             False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-52)2             False   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-53)3             False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-54)4             False   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-55)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-56)>>> my_sig.exits
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-57)custom_prob1           0.0           1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-58)custom_prob2    0.0    1.0    0.0    1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-59)0             False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-60)1             False   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-61)2             False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-62)3             False   True   True   True
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-63)4             False  False  False  False
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-64)
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-65)>>> my_sig.rand_type_readable
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-66)custom_prob1     0.0     1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-67)custom_prob2 0.0 1.0 0.0 1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-68)0
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-69)1                 R2  R1  R1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-70)2
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-71)3                 R2  R1  R1
    [](https://vectorbt.pro/pvt_7a467f6b/api/signals/factory/#__codelineno-4-72)4
    
