settings

#  _settings module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings "Permanent link")

Global settings of vectorbtpro.

[settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.settings "vectorbtpro._settings.settings") config is also accessible via `vectorbtpro.settings`.

Note

All places in vectorbt import [settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.settings "vectorbtpro._settings.settings"), not `vectorbtpro.settings`. Overwriting `vectorbtpro.settings` only overwrites the reference created for the user. Consider updating the settings config instead of replacing it.

Here are the main properties of the [settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.settings "vectorbtpro._settings.settings") config:

  * It's a nested config, that is, a config that consists of multiple sub-configs. one per sub-package (e.g., 'data'), module (e.g., 'wrapping'), or even class (e.g., 'configured'). Each sub-config may consist of other sub-configs.
  * It has frozen keys - you cannot add other sub-configs or remove the existing ones, but you can modify them.
  * Each sub-config can be [frozen_cfg](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.frozen_cfg "vectorbtpro._settings.frozen_cfg") or [flex_cfg](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.flex_cfg "vectorbtpro._settings.flex_cfg"). The main reason for defining a flexible config is to allow adding new keys (e.g., 'plotting.layout').



For example, you can change default width and height of each plot:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-0-3)>>> vbt.settings['plotting']['layout']['width'] = 800
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-0-4)>>> vbt.settings['plotting']['layout']['height'] = 400
    

The main sub-configs such as for plotting can be also accessed/modified using the dot notation:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-1-1)>>> vbt.settings.plotting['layout']['width'] = 800
    

Some sub-configs allow the dot notation too but this depends on whether they are an instance of [frozen_cfg](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.frozen_cfg "vectorbtpro._settings.frozen_cfg"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-1)>>> type(vbt.settings)
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-2)vectorbtpro._settings.frozen_cfg
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-3)>>> vbt.settings.data  # ok
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-5)>>> type(vbt.settings.data)
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-6)vectorbtpro._settings.frozen_cfg
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-7)>>> vbt.settings.data.silence_warnings  # ok
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-9)>>> type(vbt.settings.data.custom)
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-10)vectorbtpro._settings.flex_cfg
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-11)>>> vbt.settings.data.custom.binance  # error
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-2-12)>>> vbt.settings.data.custom["binance"]  # ok
    

Since this is only visible when looking at the source code, the advice is to always use the bracket notation.

Note

Whether the change takes effect immediately depends upon the place that accesses the settings. For example, changing 'wrapping.freq` has an immediate effect because the value is resolved every time [ArrayWrapper.freq](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.freq "vectorbtpro.base.wrapping.ArrayWrapper.freq") is called. On the other hand, changing 'portfolio.fillna_close' has only effect on [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio "vectorbtpro.portfolio.base.Portfolio") instances created in the future, not the existing ones, because the value is resolved upon the object's construction. Moreover, some settings are only accessed when importing the package for the first time, such as 'jitting.jit_decorator'. In any case, make sure to check whether the update actually took place.

## Saving and loading[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#saving-and-loading "Permanent link")

Like any other class subclassing [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config"), we can persist settings to the disk, load it back, and replace in-place. There are several ways of how to update the settings.

### Binary file[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#binary-file "Permanent link")

Pickling will dump the entire settings object into a byte stream and save as a binary file. Supported file extensions are "pickle" (default) and "pkl".
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-3-1)>>> vbt.settings.save('my_settings')
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-3-2)>>> vbt.settings['caching']['disable'] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-3-3)>>> vbt.settings['caching']['disable']
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-3-4)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-3-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-3-6)>>> vbt.settings.load_update('my_settings', clear=True)  # replace in-place
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-3-7)>>> vbt.settings['caching']['disable']
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-3-8)False
    

Note

Argument `clear=True` will replace the entire settings object. Disable it to apply only a subset of settings (default).

### Config file[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#config-file "Permanent link")

We can also encode the settings object into a config and save as a text file that can be edited easily. Supported file extensions are "config" (default), "cfg", and "ini".
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-4-1)>>> vbt.settings.save('my_settings', file_format="config")
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-4-2)>>> vbt.settings['caching']['disable'] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-4-3)>>> vbt.settings['caching']['disable']
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-4-4)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-4-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-4-6)>>> vbt.settings.load_update('my_settings', file_format="config", clear=True)  # replace in-place
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-4-7)>>> vbt.settings['caching']['disable']
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-4-8)False
    

### On import[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#on-import "Permanent link")

Some settings (such as Numba-related ones) are applied only on import, so changing them during the runtime will have no effect. In this case, change the settings, save them to the disk, and then either rename the file to "vbt" (with extension) and place it in the working directory for it to be recognized automatically, or create an environment variable "VBT_SETTINGS_PATH" that holds the full path to the file - vectorbt will load it before any other module. You can also change the recognized file name using an environment variable "VBT_SETTINGS_NAME", which defaults to "vbt".

Note

Environment variables must be set before importing vectorbtpro.

For example, to set the default theme to dark, create the following "vbt.ini" file:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-5-1)[plotting]
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-5-2)default_theme = dark
    

* * *

## broadcasting frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.broadcasting "Permanent link")

Sub-config with settings applied to broadcasting functions across [vectorbtpro.base](https://vectorbt.pro/pvt_7a467f6b/api/base/ "vectorbtpro.base").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-2)    align_index=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-3)    align_columns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-4)    index_from='strict',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-5)    columns_from='stack',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-6)    ignore_sr_names=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-7)    check_index_names=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-8)    drop_duplicates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-9)    keep='last',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-10)    drop_redundant=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-11)    ignore_ranges=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-12)    keep_wrap_default=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-13)    keep_flex=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-14)    min_ndim=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-15)    expand_axis=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-16)    index_to_param=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-6-17))
    

* * *

## caching frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.caching "Permanent link")

Sub-config with settings applied across [vectorbtpro.registries.ca_registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/ "vectorbtpro.registries.ca_registry"), [vectorbtpro.utils.caching](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/ "vectorbtpro.utils.caching"), and cacheable decorators in [vectorbtpro.utils.decorators](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/ "vectorbtpro.utils.decorators").

Hint

Apply setting `register_lazily` on startup to register all unbound cacheables.

Setting `use_cached_accessors` is applied only on import.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-2)    disable=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-3)    disable_whitelist=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-4)    disable_machinery=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-5)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-6)    register_lazily=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-7)    ignore_args=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-8)        'jitted',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-9)        'chunked'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-10)    ],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-11)    use_cached_accessors=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-7-12))
    

* * *

## chunking frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.chunking "Permanent link")

Sub-config with settings applied across [vectorbtpro.registries.ch_registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/ "vectorbtpro.registries.ch_registry") and [vectorbtpro.utils.chunking](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/ "vectorbtpro.utils.chunking").

Note

Options (with `_options` suffix) and setting `disable_wrapping` are applied only on import.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-2)    disable=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-3)    disable_wrapping=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-4)    option=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-5)    chunker=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-6)    size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-7)    min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-8)    n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-9)    chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-10)    chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-11)    prepend_chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-12)    skip_single_chunk=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-13)    arg_take_spec=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-14)    template_context=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-15)    merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-16)    merge_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-17)    return_raw_chunks=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-18)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-19)    forward_kwargs_as=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-20)    execute_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-21)    replace_chunker=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-22)    merge_to_execute_kwargs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-23)    options=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-24)    override_setup_options=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-25)    override_options=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-8-26))
    

* * *

## config frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.config "Permanent link")

Sub-config with settings applied to [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-9-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-9-2)    options=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-9-3))
    

* * *

## configured frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.configured "Permanent link")

Sub-config with settings applied to [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-2)    check_expected_keys_=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-3)    config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-4)        options=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-5)            readonly=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-6)            nested=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-7)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-8)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-10-9))
    

* * *

## data frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.data "Permanent link")

Sub-config with settings applied across [vectorbtpro.data](https://vectorbt.pro/pvt_7a467f6b/api/data/ "vectorbtpro.data").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-2)    keys_are_features=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-3)    wrapper_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-4)    skip_on_error=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-5)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-6)    execute_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-7)    tz_localize='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-8)    tz_convert='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-9)    missing_index='nan',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-10)    missing_columns='raise',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-11)    custom=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-12)        synthetic=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-13)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-14)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-15)            timeframe=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-16)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-17)            normalize=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-18)            inclusive='left'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-19)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-20)        random=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-21)            start_value=100.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-22)            mean=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-23)            std=0.01,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-24)            symmetric=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-25)            seed=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-26)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-27)        random_ohlc=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-28)            n_ticks=50,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-29)            start_value=100.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-30)            mean=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-31)            std=0.001,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-32)            symmetric=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-33)            seed=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-34)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-35)        gbm=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-36)            start_value=100.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-37)            mean=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-38)            std=0.01,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-39)            dt=1.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-40)            seed=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-41)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-42)        gbm_ohlc=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-43)            n_ticks=50,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-44)            start_value=100.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-45)            mean=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-46)            std=0.001,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-47)            dt=1.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-48)            seed=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-49)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-50)        local=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-51)        file=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-52)            match_paths=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-53)            match_regex=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-54)            sort_paths=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-55)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-56)        csv=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-57)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-58)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-59)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-60)            start_row=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-61)            end_row=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-62)            header=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-63)            index_col=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-64)            parse_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-65)            chunk_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-66)            squeeze=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-67)            read_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-68)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-69)        hdf=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-70)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-71)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-72)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-73)            start_row=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-74)            end_row=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-75)            read_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-76)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-77)        feather=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-78)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-79)            index_col=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-80)            squeeze=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-81)            read_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-82)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-83)        parquet=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-84)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-85)            squeeze=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-86)            keep_partition_cols=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-87)            engine='auto',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-88)            read_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-89)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-90)        db=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-91)        sql=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-92)            engine=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-93)            engine_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-94)            engine_config=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-95)            schema=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-96)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-97)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-98)            align_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-99)            parse_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-100)            to_utc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-101)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-102)            start_row=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-103)            end_row=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-104)            keep_row_number=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-105)            row_number_column='row_number',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-106)            index_col=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-107)            columns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-108)            dtype=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-109)            chunksize=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-110)            chunk_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-111)            squeeze=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-112)            read_sql_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-113)            engines=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-114)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-115)        duckdb=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-116)            connection=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-117)            connection_config=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-118)            schema=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-119)            catalog=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-120)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-121)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-122)            align_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-123)            parse_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-124)            to_utc=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-125)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-126)            index_col=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-127)            squeeze=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-128)            df_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-129)            sql_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-130)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-131)        remote=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-132)        yf=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-133)            period='max',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-134)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-135)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-136)            timeframe='1d',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-137)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-138)            history_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-139)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-140)        binance=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-141)            client=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-142)            client_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-143)                api_key=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-144)                api_secret=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-145)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-146)            start=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-147)            end='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-148)            timeframe='1d',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-149)            tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-150)            klines_type='spot',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-151)            limit=1000,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-152)            delay=0.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-153)            show_progress=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-154)            pbar_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-155)            silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-156)            get_klines_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-157)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-158)        ccxt=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-159)            exchange=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-160)            exchange_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-161)                enableRateLimit=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-162)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-163)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-164)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-165)            timeframe='1d',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-166)            tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-167)            find_earliest_date=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-168)            limit=1000,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-169)            delay=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-170)            retries=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-171)            fetch_params=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-172)            show_progress=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-173)            pbar_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-174)            silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-175)            exchanges=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-176)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-177)        alpaca=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-178)            client=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-179)            client_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-180)            client_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-181)                api_key=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-182)                secret_key=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-183)                oauth_token=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-184)                paper=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-185)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-186)            start=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-187)            end='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-188)            timeframe='1d',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-189)            tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-190)            adjustment='raw',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-191)            feed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-192)            limit=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-193)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-194)        polygon=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-195)            client=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-196)            client_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-197)                api_key=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-198)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-199)            start=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-200)            end='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-201)            timeframe='1d',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-202)            tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-203)            adjusted=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-204)            limit=50000,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-205)            params=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-206)            delay=0.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-207)            retries=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-208)            show_progress=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-209)            pbar_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-210)            silence_warnings=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-211)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-212)        av=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-213)            use_parser=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-214)            apikey=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-215)            api_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-216)            category=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-217)            function=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-218)            timeframe=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-219)            tz=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-220)            adjusted=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-221)            extended=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-222)            slice='year1month1',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-223)            series_type='close',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-224)            time_period=10,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-225)            outputsize='full',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-226)            read_csv_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-227)                index_col=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-228)                parse_dates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-229)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-230)            match_params=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-231)            params=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-232)            silence_warnings=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-233)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-234)        ndl=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-235)            api_key=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-236)            data_format='dataset',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-237)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-238)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-239)            tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-240)            column_indices=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-241)            params=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-242)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-243)        tv=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-244)            client=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-245)            client_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-246)                username=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-247)                password=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-248)                auth_token=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-249)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-250)            exchange=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-251)            timeframe='D',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-252)            tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-253)            fut_contract=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-254)            adjustment='splits',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-255)            extended_session=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-256)            pro_data=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-257)            limit=20000,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-258)            delay=0.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-259)            retries=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-260)            search=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-261)                pages=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-262)                delay=0.5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-263)                retries=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-264)                show_progress=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-265)                pbar_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-266)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-267)            scanner=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-268)                markets=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-269)                fields=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-270)                filter_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-271)                groups=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-272)                template_context=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-273)                scanner_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-274)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-275)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-276)        bento=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-277)            client=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-278)            client_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-279)                key=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-280)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-281)            start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-282)            end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-283)            resolve_dates=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-284)            timeframe=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-285)            tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-286)            dataset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-287)            schema=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-288)            df_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-289)            params=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-290)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-291)        finpy=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-292)            market=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-293)            market_config=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-294)            config_manager=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-295)            config_manager_config=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-296)            start='one year ago',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-297)            end='now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-298)            timeframe='daily',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-299)            tz='utc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-300)            request_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-301)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-302)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-303)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-304)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-305)            is_feature_oriented=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-306)                filter_func=<function <lambda> at 0x11c55cea0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-307)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-308)            is_symbol_oriented=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-309)                filter_func=<function <lambda> at 0x11c55cd60>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-310)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-311)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-312)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-313)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-11-314))
    

**Binance**

See `binance.client.Client`.

**CCXT**

See [Configuring API Keys](https://ccxt.readthedocs.io/en/latest/manual.html#configuring-api-keys). Keys can be defined per exchange. If a key is defined at the root, it applies to all exchanges.

**Alpaca**

Sign up for Alpaca API keys under <https://app.alpaca.markets/signup.>

* * *

## datetime frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.datetime "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.datetime_](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/ "vectorbtpro.utils.datetime_").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-2)    naive_tz='tzlocal()',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-3)    to_fixed_offset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-4)    parse_with_dateparser=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-5)    index=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-6)        parse_index=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-7)        parse_with_dateparser=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-8)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-9)    dateparser_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-10)    freq_from_n=20,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-11)    tz_naive_ns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-12)    readable=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-13)        drop_tz=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-14)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-12-15))
    

* * *

## drawdowns frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.drawdowns "Permanent link")

Sub-config with settings applied to [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns "vectorbtpro.generic.drawdowns.Drawdowns").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-13-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-13-2)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-13-3)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-13-4)            incl_active=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-13-5)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-13-6)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-13-7)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-13-8))
    

* * *

## execution frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.execution "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.execution](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/ "vectorbtpro.utils.execution").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-2)    executor=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-3)    engine='SerialEngine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-4)    engine_config=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-5)    min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-6)    n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-7)    chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-8)    chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-9)    distribute='tasks',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-10)    warmup=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-11)    in_chunk_order=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-12)    cache_chunks=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-13)    chunk_cache_dir=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-14)    chunk_cache_save_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-15)        mkdir_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-16)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-17)    chunk_cache_load_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-18)    pre_clear_chunk_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-19)    post_clear_chunk_cache=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-20)    release_chunk_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-21)    chunk_clear_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-22)    chunk_collect_garbage=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-23)    chunk_delay=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-24)    pre_execute_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-25)    pre_execute_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-26)    pre_chunk_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-27)    pre_chunk_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-28)    post_chunk_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-29)    post_chunk_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-30)    post_execute_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-31)    post_execute_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-32)    post_execute_on_sorted=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-33)    filter_results=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-34)    raise_no_results=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-35)    merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-36)    merge_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-37)    template_context=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-38)    show_progress=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-39)    pbar_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-40)    replace_executor=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-41)    merge_to_engine_config=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-42)    engines=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-43)        serial=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-44)            cls='SerialEngine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-45)            show_progress=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-46)            pbar_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-47)            clear_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-48)            collect_garbage=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-49)            delay=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-50)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-51)        threadpool=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-52)            cls='ThreadPoolEngine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-53)            init_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-54)            timeout=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-55)            hide_inner_progress=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-56)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-57)        processpool=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-58)            cls='ProcessPoolEngine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-59)            init_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-60)            timeout=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-61)            hide_inner_progress=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-62)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-63)        pathos=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-64)            cls='PathosEngine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-65)            pool_type='process',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-66)            init_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-67)            timeout=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-68)            check_delay=0.001,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-69)            show_progress=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-70)            pbar_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-71)            hide_inner_progress=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-72)            join_pool=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-73)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-74)        mpire=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-75)            cls='MpireEngine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-76)            init_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-77)                use_dill=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-78)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-79)            apply_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-80)            hide_inner_progress=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-81)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-82)        dask=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-83)            cls='DaskEngine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-84)            compute_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-85)            hide_inner_progress=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-86)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-87)        ray=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-88)            cls='RayEngine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-89)            restart=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-90)            reuse_refs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-91)            del_refs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-92)            shutdown=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-93)            init_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-94)            remote_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-95)            hide_inner_progress=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-96)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-97)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-14-98))
    

* * *

## generic frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.generic "Permanent link")

Sub-config with settings applied to [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor "vectorbtpro.generic.accessors.GenericAccessor").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-2)    use_jitted=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-3)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-4)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-5)            has_mapping=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-6)                filter_func=<function <lambda> at 0x11c55d120>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-7)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-8)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-9)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-10)            incl_all_keys=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-11)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-12)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-13)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-15-14))
    

* * *

## importing frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.importing "Permanent link")

Sub-config with settings applied on importing.

Disabling these options will make vectorbt load faster, but will limit the flexibility of accessing various features of the package.

Note

If `auto_import` is False, you won't be able to access most important modules and objects such as via `vbt.Portfolio`, only by explicitly importing them such as via `from vectorbtpro.portfolio.base import Portfolio`.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-2)    clear_pycache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-3)    auto_import=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-4)    star_import='minimal',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-5)    plotly=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-6)    telegram=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-7)    quantstats=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-8)    sklearn=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-16-9))
    

* * *

## indexing frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.indexing "Permanent link")

Sub-config with settings applied to indexing functions across [vectorbtpro.base](https://vectorbt.pro/pvt_7a467f6b/api/base/ "vectorbtpro.base").

Note

Options `rotate_rows` and `rotate_cols` are applied only on import. 
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-17-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-17-2)    rotate_rows=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-17-3)    rotate_cols=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-17-4))
    

* * *

## jitting frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "Permanent link")

Sub-config with settings applied across [vectorbtpro.registries.jit_registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/ "vectorbtpro.registries.jit_registry") and [vectorbtpro.utils.jitting](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/ "vectorbtpro.utils.jitting").

Note

Options (with `_options` suffix) are applied only on import. 

Keyword arguments (with `_kwargs` suffix) are applied right away.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-2)    disable=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-3)    disable_wrapping=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-4)    disable_resolution=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-5)    option=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-6)    allow_new=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-7)    register_new=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-8)    jitters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-9)        nb=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-10)            cls='NumbaJitter',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-11)            aliases={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-12)                'numba'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-13)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-14)            options=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-15)            override_options=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-16)            resolve_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-17)            tasks=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-18)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-19)        np=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-20)            cls='NumPyJitter',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-21)            aliases={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-22)                'numpy'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-23)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-24)            options=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-25)            override_options=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-26)            resolve_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-27)            tasks=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-28)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-29)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-30)    template_context=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-18-31))
    

* * *

## knowledge frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.knowledge "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.knowledge](https://vectorbt.pro/pvt_7a467f6b/api/utils/knowledge/ "vectorbtpro.utils.knowledge").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-2)    cache=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-3)    cache_dir='./knowledge',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-4)    cache_mkdir_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-5)    clear_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-6)    asset_cache_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-7)        template="Path(cache_dir) / 'asset_cache'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-8)        context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-9)        strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-10)        context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-11)        eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-12)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-13)    max_cache_count=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-14)    save_cache_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-15)    load_cache_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-16)    per_path=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-17)    find_all=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-18)    keep_path=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-19)    skip_missing=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-20)    make_copy=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-21)    query_engine=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-22)    return_type='item',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-23)    return_path=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-24)    merge_matches=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-25)    merge_fields=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-26)    unique_matches=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-27)    unique_fields=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-28)    changed_only=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-29)    code=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-30)        language=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-31)        in_blocks=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-32)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-33)    dump_all=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-34)    dump_engine='yaml',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-35)    dump_engine_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-36)        nestedtext=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-37)            indent=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-38)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-39)        pyyaml=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-40)            sort_keys=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-41)            default_flow_style=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-42)            allow_unicode=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-43)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-44)        ruamel=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-45)            default_flow_style=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-46)            allow_unicode=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-47)            width=4096,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-48)            preserve_quotes=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-49)            indent=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-50)                mapping=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-51)                sequence=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-52)                offset=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-53)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-54)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-55)        json=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-56)            ensure_ascii=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-57)            indent=4
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-58)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-59)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-60)    in_dumps=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-61)    dump_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-62)    document_cls=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-63)    document_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-64)    merge_chunks=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-65)    sort_keys=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-66)    ignore_empty=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-67)    describe_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-68)        percentiles=[]
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-69)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-70)    uniform_groups=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-71)    prepend_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-72)    template_context=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-73)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-74)    show_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-75)    pbar_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-76)    execute_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-77)        filter_results=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-78)        raise_no_results=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-79)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-80)    open_browser=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-81)    to_markdown_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-82)    to_html_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-83)    format_html_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-84)    minimal_format_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-85)        to_html_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-86)            extensions=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-87)                'fenced_code',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-88)                'codehilite',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-89)                'admonition',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-90)                'tables',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-91)                'footnotes',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-92)                'md_in_html',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-93)                'toc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-94)                'pymdownx.tilde',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-95)                'pymdownx.superfences',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-96)                'pymdownx.magiclink',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-97)                'pymdownx.highlight',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-98)                'pymdownx.tasklist',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-99)                'pymdownx.arithmatex'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-100)            ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-101)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-102)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-103)    formatting=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-104)        remove_code_title=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-105)        even_indentation=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-106)        newline_before_list=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-107)        resolve_extensions=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-108)        make_links=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-109)        markdown_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-110)            extensions=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-111)                'fenced_code',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-112)                'codehilite',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-113)                'meta',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-114)                'admonition',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-115)                'def_list',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-116)                'attr_list',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-117)                'tables',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-118)                'footnotes',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-119)                'md_in_html',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-120)                'toc',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-121)                'abbr',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-122)                'pymdownx.tilde',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-123)                'pymdownx.keys',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-124)                'pymdownx.details',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-125)                'pymdownx.inlinehilite',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-126)                'pymdownx.snippets',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-127)                'pymdownx.superfences',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-128)                'pymdownx.tabbed',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-129)                'pymdownx.progressbar',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-130)                'pymdownx.magiclink',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-131)                'pymdownx.emoji',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-132)                'pymdownx.highlight',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-133)                'pymdownx.tasklist',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-134)                'pymdownx.arithmatex'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-135)            ],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-136)            extension_configs={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-137)                'codehilite': dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-138)                    css_class='highlight'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-139)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-140)                'pymdownx.superfences': dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-141)                    preserve_tabs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-142)                    custom_fences=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-143)                        dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-144)                            name='mermaid',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-145)                            class='mermaid',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-146)                            format=<function fence_code_format at 0x11c54a480>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-147)                        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-148)                    ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-149)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-150)                'pymdownx.tabbed': dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-151)                    alternate_style=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-152)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-153)                'pymdownx.magiclink': dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-154)                    repo_url_shorthand=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-155)                    user='polakowo',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-156)                    repo='vectorbt.pro'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-157)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-158)                'pymdownx.emoji': dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-159)                    emoji_index=<function twemoji at 0x11c549580>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-160)                    emoji_generator=<function to_svg at 0x11c5496c0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-161)                    alt='short',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-162)                    options=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-163)                        attributes=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-164)                            align='absmiddle',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-165)                            height='20px',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-166)                            width='20px'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-167)                        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-168)                    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-169)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-170)                'pymdownx.highlight': dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-171)                    css_class='highlight',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-172)                    guess_lang=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-173)                    anchor_linenums=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-174)                    line_spans='__span',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-175)                    pygments_lang_class=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-176)                    extend_pygments_lang=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-177)                        dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-178)                            name='pycon3',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-179)                            lang='pycon',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-180)                            options=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-181)                                python3=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-182)                            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-183)                        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-184)                    ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-185)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-186)                'pymdownx.arithmatex': dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-187)                    inline_syntax=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-188)                        'round'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-189)                    ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-190)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-191)            }
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-192)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-193)        use_pygments=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-194)        pygments_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-195)        html_template='<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <link rel="icon" href="https://vectorbt.pro/pvt_7a467f6b/assets/logo/favicon.png">\n    <title>$title</title>\n    <style>\n        body {\n            font-family: Arial, sans-serif;\n            padding: 40px;\n            line-height: 1.6;\n            background-color: #fff;\n            color: #000;\n        }\n        h1, h2, h3, h4, h5, h6 {\n            color: #333;\n        }\n        pre {\n            padding: 10px;\n            border: 1px solid rgba(0, 0, 0, 0.1);\n            border-radius: 4px;\n            overflow-x: auto;\n        }\n        .admonition {\n            background-color: #f9f9f9;\n            margin: 20px 0;\n            padding: 10px 20px;\n            border-left: 5px solid #ccc;\n            border-radius: 4px;\n        }\n        .admonition > p:first-child {\n            font-weight: bold;\n            margin-bottom: 5px;\n        }\n        .admonition.example {\n            background-color: #e7f5ff;\n            border-left-color: #339af0;\n        }\n        .admonition.hint {\n            background-color: #fff4e6;\n            border-left-color: #ffa940;\n        }\n        .admonition.important {\n            background-color: #ffe3e3;\n            border-left-color: #ff6b6b;\n        }\n        .admonition.info {\n            background-color: #e3f2fd;\n            border-left-color: #42a5f5;\n        }\n        .admonition.note {\n            background-color: #e8f5e9;\n            border-left-color: #66bb6a;\n        }\n        .admonition.question {\n            background-color: #f3e5f5;\n            border-left-color: #ab47bc;\n        }\n        .admonition.tip {\n            background-color: #fffde7;\n            border-left-color: #ffee58;\n        }\n        .admonition.warning {\n            background-color: #fff3cd;\n            border-left-color: #ffc107;\n        }\n        $style_extras\n    </style>\n    $head_extras\n</head>\n<body>\n    $html_metadata\n    $html_content\n    $body_extras\n</body>\n</html>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-196)        root_style_extras=[],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-197)        style_extras=[],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-198)        head_extras=[],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-199)        body_extras=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-200)            '<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-201)            '<script>window.mermaidConfig={startOnLoad:!1,theme:"default",flowchart:{htmlLabels:!1},er:{useMaxWidth:!1},sequence:{useMaxWidth:!1,noteFontWeight:"14px",actorFontSize:"14px",messageFontSize:"16px"}};</script>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-202)            '<script>const uml=async e=>{class t extends HTMLElement{constructor(){super();let e=this.attachShadow({mode:"open"}),t=document.createElement("style");t.textContent=`:host{display:block;line-height:initial;font-size:16px}div.diagram{margin:0;overflow:visible}`,e.appendChild(t)}}void 0===customElements.get("diagram-div")&&customElements.define("diagram-div",t);let i=e=>{let t="";for(let i=0;i<e.childNodes.length;i++){let a=e.childNodes[i];if("code"===a.tagName.toLowerCase())for(let d=0;d<a.childNodes.length;d++){let l=a.childNodes[d],o=/^\\s*$/;if("#text"===l.nodeName&&!o.test(l.nodeValue)){t=l.nodeValue;break}}}return t},a={startOnLoad:!1,theme:"default",flowchart:{htmlLabels:!1},er:{useMaxWidth:!1},sequence:{useMaxWidth:!1,noteFontWeight:"14px",actorFontSize:"14px",messageFontSize:"16px"}};mermaid.mermaidAPI.globalReset();let d="undefined"==typeof mermaidConfig?a:mermaidConfig;mermaid.initialize(d);let l=document.querySelectorAll(`pre.${e}, diagram-div`),o=document.querySelector("html body");for(let n=0;n<l.length;n++){let r=l[n],s="diagram-div"===r.tagName.toLowerCase()?r.shadowRoot.querySelector(`pre.${e}`):r,h=document.createElement("div");h.style.visibility="hidden",h.style.display="display",h.style.padding="0",h.style.margin="0",h.style.lineHeight="initial",h.style.fontSize="16px",o.appendChild(h);try{let m=await mermaid.render(`_diagram_${n}`,i(s),h),c=m.svg,p=m.bindFunctions,g=document.createElement("div");g.className=e,g.innerHTML=c,p&&p(g);let y=document.createElement("diagram-div");y.shadowRoot.appendChild(g),r.parentNode.insertBefore(y,r),s.style.display="none",y.shadowRoot.appendChild(s),s!==r&&r.parentNode.removeChild(r)}catch(u){}o.contains(h)&&o.removeChild(h)}};document.addEventListener("DOMContentLoaded",()=>{uml("mermaid")});</script>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-203)            '<script src="https://cdn.jsdelivr.net/npm/mathjax/es5/tex-mml-chtml.min.js"></script>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-204)            '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]],processEscapes:!0,processEnvironments:!0},options:{ignoreHtmlClass:".*|",processHtmlClass:"arithmatex"}},document$.subscribe(()=>{MathJax.startup.output.clearCache(),MathJax.typesetClear(),MathJax.texReset(),MathJax.typesetPromise()});</script>'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-205)        ],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-206)        invert_colors=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-207)        invert_colors_style=':root {\n    filter: invert(100%);\n}',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-208)        auto_scroll=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-209)        auto_scroll_body='<script>\nfunction scrollToBottom() {\n    window.scrollTo(0, document.body.scrollHeight);\n}\nfunction hasMetaRefresh() {\n    return document.querySelector(\'meta[http-equiv="refresh"]\') !== null;\n}\nwindow.onload = function() {\n    if (hasMetaRefresh()) {\n        scrollToBottom();\n        setInterval(scrollToBottom, 100);\n    }\n};\n</script>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-210)        show_spinner=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-211)        spinner_style=".loader {\n    width: 300px;\n    height: 5px;\n    margin: 0 auto;\n    display: block;\n    position: relative;\n    overflow: hidden;\n}\n.loader::after {\n    content: '';\n    width: 300px;\n    height: 5px;\n    background: blue;\n    position: absolute;\n    top: 0;\n    left: 0;\n    box-sizing: border-box;\n    animation: animloader 1s ease-in-out infinite;\n}\n@keyframes animloader {\n    0%, 5% {\n        left: 0;\n        transform: translateX(-100%);\n    }\n    95%, 100% {\n        left: 100%;\n        transform: translateX(0%);\n    }\n}\n    ",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-212)        spinner_body='<span class="loader"></span>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-213)        output_to=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-214)        flush_output=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-215)        buffer_output=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-216)        close_output=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-217)        update_interval=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-218)        minimal_format=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-219)        formatter='ipython_auto',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-220)        formatter_config=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-221)        formatter_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-222)            plain=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-223)            ipython=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-224)            ipython_markdown=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-225)            ipython_html=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-226)            html=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-227)                dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-228)                    template="Path(cache_dir) / 'html'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-229)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-230)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-231)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-232)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-233)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-234)                mkdir_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-235)                temp_files=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-236)                refresh_page=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-237)                file_prefix_len=20,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-238)                file_suffix_len=6,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-239)                auto_scroll=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-240)                show_spinner=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-241)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-242)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-243)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-244)    chat=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-245)        chat_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-246)            template="Path(cache_dir) / 'chat'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-247)            context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-248)            strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-249)            context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-250)            eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-251)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-252)        stream=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-253)        to_context_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-254)        incl_past_queries=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-255)        rank=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-256)        rank_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-257)            top_k=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-258)            min_top_k=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-259)            max_top_k=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-260)            cutoff=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-261)            return_chunks=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-262)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-263)        max_tokens=120000,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-264)        system_prompt='You are a helpful assistant. Given the context information and not prior knowledge, answer the query.',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-265)        system_as_user=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-266)        context_prompt='Context information is below.\n---------------------\n$context\n---------------------',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-267)        minimal_format=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-268)        tokenizer='tiktoken',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-269)        tokenizer_config=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-270)        tokenizer_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-271)            tiktoken=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-272)                encoding='model_or_o200k_base',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-273)                model=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-274)                tokens_per_message=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-275)                tokens_per_name=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-276)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-277)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-278)        embeddings='auto',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-279)        embeddings_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-280)            batch_size=512
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-281)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-282)        embeddings_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-283)            openai=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-284)                model='text-embedding-3-large',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-285)                dimensions=256
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-286)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-287)            litellm=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-288)                model='text-embedding-3-large',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-289)                dimensions=256
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-290)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-291)            llama_index=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-292)                embedding='openai',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-293)                embedding_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-294)                    openai=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-295)                        model='text-embedding-3-large',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-296)                        dimensions=256
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-297)                    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-298)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-299)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-300)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-301)        completions='auto',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-302)        completions_config=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-303)        completions_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-304)            openai=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-305)                model='gpt-4o'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-306)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-307)            litellm=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-308)                model='gpt-4o'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-309)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-310)            llama_index=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-311)                llm='openai',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-312)                llm_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-313)                    openai=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-314)                        model='gpt-4o'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-315)                    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-316)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-317)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-318)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-319)        text_splitter='segment',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-320)        text_splitter_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-321)            chunk_template='... (previous text omitted)\n            \n$chunk_text'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-322)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-323)        text_splitter_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-324)            token=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-325)                chunk_size=800,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-326)                chunk_overlap=400,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-327)                tokenizer='tiktoken',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-328)                tokenizer_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-329)                    encoding='cl100k_base'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-330)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-331)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-332)            segment=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-333)                separators=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-334)                    [
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-335)                        '\\n\\s*\\n',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-336)                        '(?<=[^\\s.?!])[.?!]+(?:\\s+|$)'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-337)                    ],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-338)                    '\\s+',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-339)                    None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-340)                ],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-341)                min_chunk_size=0.8,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-342)                fixed_overlap=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-343)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-344)            llama_index=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-345)                node_parser='sentence',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-346)                node_parser_configs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-347)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-348)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-349)        obj_store='memory',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-350)        obj_store_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-351)            store_id='default',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-352)            purge_on_open=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-353)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-354)        obj_store_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-355)            memory=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-356)            file=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-357)                dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-358)                    template="Path(cache_dir) / 'file_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-359)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-360)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-361)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-362)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-363)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-364)                compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-365)                save_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-366)                    mkdir_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-367)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-368)                load_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-369)                use_patching=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-370)                consolidate=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-371)                mirror=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-372)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-373)            lmdb=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-374)                dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-375)                    template="Path(cache_dir) / 'lmdb_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-376)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-377)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-378)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-379)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-380)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-381)                mkdir_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-382)                dumps_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-383)                loads_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-384)                mirror=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-385)                flag='c'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-386)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-387)            cached=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-388)                lazy_open=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-389)                mirror=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-390)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-391)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-392)        doc_ranker_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-393)            dataset_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-394)            cache_doc_store=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-395)            cache_emb_store=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-396)            doc_store_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-397)                memory=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-398)                    store_id='doc_default'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-399)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-400)                file=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-401)                    dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-402)                        template="Path(cache_dir) / 'doc_file_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-403)                        context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-404)                        strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-405)                        context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-406)                        eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-407)                    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-408)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-409)                lmdb=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-410)                    dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-411)                        template="Path(cache_dir) / 'doc_lmdb_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-412)                        context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-413)                        strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-414)                        context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-415)                        eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-416)                    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-417)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-418)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-419)            emb_store_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-420)                memory=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-421)                    store_id='emb_default'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-422)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-423)                file=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-424)                    dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-425)                        template="Path(cache_dir) / 'emb_file_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-426)                        context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-427)                        strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-428)                        context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-429)                        eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-430)                    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-431)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-432)                lmdb=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-433)                    dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-434)                        template="Path(cache_dir) / 'emb_lmdb_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-435)                        context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-436)                        strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-437)                        context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-438)                        eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-439)                    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-440)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-441)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-442)            score_func='cosine',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-443)            score_agg_func='mean'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-444)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-445)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-446)    assets=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-447)        vbt=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-448)            cache_dir='./knowledge/vbt/',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-449)            release_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-450)                template='(Path(cache_dir) / release_name) if release_name else cache_dir',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-451)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-452)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-453)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-454)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-455)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-456)            assets_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-457)                template="Path(release_dir) / 'assets'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-458)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-459)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-460)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-461)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-462)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-463)            markdown_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-464)                template="Path(release_dir) / 'markdown'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-465)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-466)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-467)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-468)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-469)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-470)            html_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-471)                template="Path(release_dir) / 'html'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-472)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-473)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-474)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-475)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-476)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-477)            release_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-478)            asset_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-479)            repo_owner='polakowo',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-480)            repo_name='vectorbt.pro',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-481)            token=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-482)            token_required=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-483)            use_pygithub=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-484)            chunk_size=8192,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-485)            document_cls=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-486)            document_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-487)                text_path='content',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-488)                excl_metadata=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-489)                    template="asset_cls.get_setting('minimize_keys')",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-490)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-491)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-492)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-493)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-494)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-495)                excl_embed_metadata=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-496)                split_text_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-497)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-498)            minimize_metadata=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-499)            minimize_keys=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-500)                'parent',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-501)                'children',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-502)                'type',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-503)                'icon',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-504)                'tags',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-505)                'block',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-506)                'thread',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-507)                'replies',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-508)                'mentions',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-509)                'reactions'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-510)            ],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-511)            minimize_links=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-512)            minimize_link_rules=flex_cfg({
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-513)                '(https://vectorbt\\.pro/pvt_[a-zA-Z0-9]+)': '$pvt_site',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-514)                '(https://vectorbt\\.pro)': '$pub_site',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-515)                '(https://discord\\.com/channels/[0-9]+)': '$discord',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-516)                '(https://github\\.com/polakowo/vectorbt\\.pro)': '$github'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-517)            }),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-518)            root_metadata_key=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-519)            aggregate_fields=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-520)            parent_links_only=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-521)            clean_metadata=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-522)            clean_metadata_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-523)            dump_metadata_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-524)            incl_base_attr=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-525)            incl_shortcuts=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-526)            incl_shortcut_access=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-527)            incl_shortcut_call=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-528)            incl_instances=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-529)            incl_custom=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-530)            is_custom_regex=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-531)            as_code=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-532)            as_regex=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-533)            allow_prefix=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-534)            allow_suffix=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-535)            merge_targets=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-536)            display=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-537)                html_template='<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <link rel="icon" href="https://vectorbt.pro/pvt_7a467f6b/assets/logo/favicon.png">\n    <title>$title</title>\n    <style>\n        * {\n            box-sizing: border-box;\n        }\n        body {\n            font-family: Arial, sans-serif;\n            padding: 40px;\n            line-height: 1.6;\n            background: #fff;\n            color: #000;\n            margin: 0;\n        }\n        .pagination {\n            text-align: center;\n            margin: 20px 0;\n            font-size: 14px;\n        }\n        .pagination ul {\n            display: inline-block;\n            list-style: none;\n            margin: 0;\n            padding: 0;\n        }\n        .pagination li {\n            display: inline;\n            margin: 0 4px;\n        }\n        .nav-btn,\n        .page-link {\n            text-decoration: none;\n            padding: 8px 12px;\n            border-radius: 4px;\n        }\n        .nav-btn {\n            background: transparent;\n            color: blue;\n            border: none;\n            cursor: pointer;\n        }\n        .nav-btn.disabled {\n            color: gray;\n            cursor: default;\n            pointer-events: none;\n        }\n        .nav-btn:hover:not(.disabled) {\n            background: rgba(0, 0, 255, 0.1);\n        }\n        .page-link {\n            color: #000;\n        }\n        .page-link:hover:not(.active) {\n            background: lightgray;\n        }\n        .page-link.active {\n            background: blue;\n            color: #fff;\n            cursor: default;\n        }\n        iframe {\n            width: 100%;\n            border: none;\n            display: block;\n        }\n        $style_extras\n    </style>\n    $head_extras\n</head>\n<body>\n    <div id="pagination-top" class="pagination"></div>\n    <iframe id="page-iframe" scrolling="no" onload="adjustIframeHeight(this)"></iframe>\n    <div id="pagination-bottom" class="pagination"></div>\n    <script>const pages=$pages;let currentPage=1,totalPages=pages.length;function base64DecodeUtf8(e){return decodeURIComponent(atob(e).split("").map(e=>"%"+("00"+e.charCodeAt(0).toString(16)).slice(-2)).join(""))}function showPage(e){e<1&&(e=1),e>totalPages&&(e=totalPages),currentPage=e,document.getElementById("page-iframe").srcdoc=base64DecodeUtf8(pages[e-1]),renderPagination(),adjustIframeHeight(document.getElementById("page-iframe"))}function prevPage(){showPage(currentPage-1)}function nextPage(){showPage(currentPage+1)}function renderPagination(){let e="<ul>";if(e+=1===currentPage?\'<li><span class="nav-btn disabled">&lt; Previous</span></li>\':\'<li><a href="#" class="nav-btn" onclick="prevPage()">&lt; Previous</a></li>\',totalPages<=7)for(let a=1;a<=totalPages;a++)e+=`<li><a href="#" data-page="${a}" class="page-link" onclick="showPage(${a})">${a}</a></li>`;else if(currentPage<=4){for(let t=1;t<=5;t++)e+=linkTpl(t);e+=" <li><span>…</span></li> "+linkTpl(totalPages)}else if(currentPage>=totalPages-3){e+=linkTpl(1)+" <li><span>…</span></li> ";for(let n=totalPages-4;n<=totalPages;n++)e+=linkTpl(n)}else e+=linkTpl(1)+" <li><span>…</span></li> "+linkTpl(currentPage-1)+linkTpl(currentPage)+linkTpl(currentPage+1)+" <li><span>…</span></li> "+linkTpl(totalPages);e+=currentPage===totalPages?\'<li><span class="nav-btn disabled">Next &gt;</span></li>\':\'<li><a href="#" class="nav-btn" onclick="nextPage()">Next &gt;</a></li>\',e+="</ul>",document.getElementById("pagination-top").innerHTML=e,document.getElementById("pagination-bottom").innerHTML=e,updateActiveLink()}function linkTpl(e){return`<li><a href="#" data-page="${e}" class="page-link" onclick="showPage(${e})">${e}</a></li>`}function updateActiveLink(){document.querySelectorAll(".page-link").forEach(e=>{e.classList.toggle("active",e.getAttribute("data-page")==currentPage)})}function adjustIframeHeight(e){try{let a=e.contentDocument||e.contentWindow.document;a.querySelectorAll(\'img[loading="lazy"]\').forEach(a=>a.addEventListener("load",()=>setTimeout(()=>adjustIframeHeight(e),100))),e.style.height=a.body.scrollHeight+"px",[...a.getElementsByTagName("a")].forEach(e=>e.target="_blank")}catch(t){}}window.addEventListener("DOMContentLoaded",()=>{totalPages>0&&showPage(1)});</script>\n    $body_extras\n</body>\n</html>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-538)                style_extras=[],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-539)                head_extras=[],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-540)                body_extras=[]
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-541)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-542)            chat=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-543)                chat_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-544)                    template="Path(release_dir) / 'chat'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-545)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-546)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-547)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-548)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-549)                ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-550)                system_prompt='You are a helpful assistant with access to VectorBT PRO (also called VBT or vectorbtpro) documentation and relevant Discord history. Use only this provided context to generate clear, accurate answers. Do not reference the open‑source vectorbt, as VectorBT PRO is a proprietary successor with significant differences.\\n\\nWhen coding in Python, use:\\n```python\\nimport vectorbtpro as vbt\\n```\\n\\nIf metadata includes links, reference them to support your answer. Do not include external or fabricated links, and exclude any information not present in the given context.\\n\\nFor each query, follow this structure:\\n1. Optionally restate the question in your own words.\\n2. Answer using only the available context.\\n3. Include any relevant links.',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-551)                doc_ranker_config=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-552)                    doc_store='lmdb',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-553)                    doc_store_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-554)                        file=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-555)                            dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-556)                                template="Path(release_dir) / 'doc_file_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-557)                                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-558)                                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-559)                                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-560)                                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-561)                            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-562)                        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-563)                        lmdb=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-564)                            dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-565)                                template="Path(release_dir) / 'doc_lmdb_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-566)                                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-567)                                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-568)                                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-569)                                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-570)                            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-571)                        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-572)                    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-573)                    emb_store='lmdb',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-574)                    emb_store_configs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-575)                        file=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-576)                            dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-577)                                template="Path(release_dir) / 'emb_file_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-578)                                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-579)                                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-580)                                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-581)                                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-582)                            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-583)                        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-584)                        lmdb=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-585)                            dir_path=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-586)                                template="Path(release_dir) / 'emb_lmdb_store'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-587)                                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-588)                                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-589)                                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-590)                                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-591)                            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-592)                        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-593)                    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-594)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-595)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-596)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-597)        pages=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-598)            assets_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-599)                template="Path(release_dir) / 'pages' / 'assets'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-600)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-601)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-602)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-603)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-604)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-605)            markdown_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-606)                template="Path(release_dir) / 'pages' / 'markdown'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-607)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-608)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-609)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-610)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-611)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-612)            html_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-613)                template="Path(release_dir) / 'pages' / 'html'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-614)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-615)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-616)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-617)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-618)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-619)            asset_name='pages.json.zip',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-620)            token_required=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-621)            append_obj_type=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-622)            append_github_link=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-623)            use_parent=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-624)            use_base_parents=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-625)            use_ref_parents=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-626)            incl_bases=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-627)            incl_ancestors=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-628)            incl_base_ancestors=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-629)            incl_refs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-630)            incl_descendants=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-631)            incl_ancestor_descendants=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-632)            incl_ref_descendants=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-633)            aggregate=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-634)            aggregate_ancestors=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-635)            aggregate_refs=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-636)            topo_sort=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-637)            incl_pages=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-638)            excl_pages=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-639)            page_find_mode='substring',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-640)            up_aggregate=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-641)            up_aggregate_th=0.6666666666666666,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-642)            up_aggregate_pages=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-643)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-644)        messages=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-645)            assets_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-646)                template="Path(release_dir) / 'messages' / 'assets'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-647)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-648)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-649)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-650)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-651)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-652)            markdown_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-653)                template="Path(release_dir) / 'messages' / 'markdown'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-654)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-655)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-656)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-657)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-658)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-659)            html_dir=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-660)                template="Path(release_dir) / 'messages' / 'html'",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-661)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-662)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-663)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-664)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-665)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-666)            asset_name='messages.json.zip',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-667)            token_required=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-668)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-669)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-19-670))
    

* * *

## logs frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.logs "Permanent link")

Sub-config with settings applied to [Logs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs "vectorbtpro.portfolio.logs.Logs").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-20-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-20-2)    stats=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-20-3))
    

* * *

## mapped_array frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.mapped_array "Permanent link")

Sub-config with settings applied to [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray "vectorbtpro.records.mapped_array.MappedArray").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-2)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-3)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-4)            has_mapping=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-5)                filter_func=<function <lambda> at 0x11c55d4e0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-6)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-7)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-8)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-9)            incl_all_keys=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-10)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-11)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-12)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-21-13))
    

* * *

## math frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.math "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.math_](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/ "vectorbtpro.utils.math_").

Note

All math settings are applied only on import.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-22-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-22-2)    use_tol=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-22-3)    rel_tol=1e-09,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-22-4)    abs_tol=1e-12,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-22-5)    use_round=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-22-6)    decimals=12
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-22-7))
    

* * *

## numba frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.numba "Permanent link")

Sub-config with Numba-related settings.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-23-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-23-2)    disable=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-23-3)    parallel=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-23-4)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-23-5)    check_func_type=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-23-6)    check_func_suffix=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-23-7))
    

* * *

## numpy frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.numpy "Permanent link")

Sub-config with NumPy-related settings.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-24-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-24-2)    float_=<class 'numpy.float64'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-24-3)    int_=<class 'numpy.int64'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-24-4))
    

* * *

## ohlcv frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.ohlcv "Permanent link")

Sub-config with settings applied across [vectorbtpro.ohlcv](https://vectorbt.pro/pvt_7a467f6b/api/ohlcv/ "vectorbtpro.ohlcv").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-25-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-25-2)    ohlc_type='candlestick',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-25-3)    feature_map=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-25-4)    stats=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-25-5)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-25-6))
    

* * *

## orders frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.orders "Permanent link")

Sub-config with settings applied to [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/orders/#vectorbtpro.portfolio.orders.Orders "vectorbtpro.portfolio.orders.Orders").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-26-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-26-2)    stats=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-26-3)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-26-4))
    

* * *

## params frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.params "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/ "vectorbtpro.utils.params").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-2)    parameterizer=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-3)    param_search_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-4)    skip_single_comb=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-5)    template_context=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-6)    build_grid=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-7)    grid_indices=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-8)    random_subset=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-9)    random_replace=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-10)    random_sort=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-11)    max_guesses=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-12)    max_misses=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-13)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-14)    clean_index_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-15)    name_tuple_to_str=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-16)    selection=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-17)    forward_kwargs_as=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-18)    mono_min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-19)    mono_n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-20)    mono_chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-21)    mono_chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-22)    mono_merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-23)    mono_merge_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-24)    mono_reduce=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-25)    filter_results=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-26)    raise_no_results=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-27)    merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-28)    merge_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-29)    return_meta=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-30)    return_param_index=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-31)    execute_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-32)    replace_parameterizer=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-33)    merge_to_execute_kwargs=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-27-34))
    

* * *

## path frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.path "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.path_](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/ "vectorbtpro.utils.path_").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-28-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-28-2)    mkdir=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-28-3)        mkdir=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-28-4)        mode=511,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-28-5)        parents=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-28-6)        exist_ok=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-28-7)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-28-8))
    

* * *

## pbar frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.pbar "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.pbar](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/ "vectorbtpro.utils.pbar").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-2)    disable=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-3)    disable_desc=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-4)    disable_registry=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-5)    disable_machinery=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-6)    type='tqdm_auto',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-7)    force_open_bar=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-8)    reuse=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-9)    kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-10)        delay=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-11)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-12)    desc_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-13)        as_postfix=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-14)        refresh=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-15)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-16)    silence_warnings=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-29-17))
    

* * *

## pfopt frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.pfopt "Permanent link")

Sub-config with settings applied across [vectorbtpro.portfolio.pfopt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/ "vectorbtpro.portfolio.pfopt").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-2)    pypfopt=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-3)        target='max_sharpe',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-4)        target_is_convex=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-5)        weights_sum_to_one=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-6)        target_constraints=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-7)        target_solver='SLSQP',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-8)        target_initial_guess=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-9)        objectives=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-10)        constraints=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-11)        sector_mapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-12)        sector_lower=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-13)        sector_upper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-14)        discrete_allocation=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-15)        allocation_method='lp_portfolio',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-16)        silence_warnings=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-17)        ignore_opt_errors=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-18)        ignore_errors=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-19)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-20)    riskfolio=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-21)        nan_to_zero=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-22)        dropna_rows=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-23)        dropna_cols=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-24)        dropna_any=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-25)        factors=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-26)        port=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-27)        port_cls=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-28)        opt_method=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-29)        stats_methods=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-30)        model=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-31)        asset_classes=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-32)        constraints_method=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-33)        constraints=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-34)        views_method=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-35)        views=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-36)        solvers=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-37)        sol_params=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-38)        freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-39)        year_freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-40)        pre_opt=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-41)        pre_opt_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-42)        pre_opt_as_w=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-43)        func_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-44)        silence_warnings=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-45)        return_port=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-46)        ignore_errors=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-47)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-48)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-49)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-50)            alloc_ranges=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-51)                filter_func=<function <lambda> at 0x11c55d800>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-52)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-53)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-54)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-55)    plots=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-56)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-57)            alloc_ranges=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-58)                filter_func=<function <lambda> at 0x11c55d760>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-59)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-60)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-61)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-30-62))
    

* * *

## pickling frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.pickling "Permanent link")

Sub-config with settings applied to [vectorbtpro.utils.pickling](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/ "vectorbtpro.utils.pickling").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-2)    pickle_classes=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-3)    file_format='pickle',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-4)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-5)    extensions=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-6)        serialization=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-7)            pickle={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-8)                'pkl',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-9)                'pickle',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-10)                'p'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-11)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-12)            config={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-13)                'cfg',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-14)                'ini',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-15)                'config'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-16)            }
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-17)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-18)        compression=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-19)            zip={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-20)                'zip'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-21)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-22)            bz2={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-23)                'bz2',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-24)                'bz',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-25)                'bzip2'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-26)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-27)            gzip={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-28)                'gzip',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-29)                'gz'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-30)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-31)            lzma={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-32)                'lzma',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-33)                'xz'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-34)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-35)            lz4={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-36)                'lz4'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-37)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-38)            blosc2={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-39)                'blosc2'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-40)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-41)            blosc1={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-42)                'blosc1'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-43)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-44)            blosc={
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-45)                'blosc'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-46)            }
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-47)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-48)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-31-49))
    

* * *

## plots_builder frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.plots_builder "Permanent link")

Sub-config with settings applied to [PlotsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/plots_builder/#vectorbtpro.generic.plots_builder.PlotsBuilderMixin "vectorbtpro.generic.plots_builder.PlotsBuilderMixin").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-2)    subplots='all',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-3)    tags='all',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-4)    per_column=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-5)    split_columns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-6)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-7)    template_context=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-8)    filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-9)        is_not_grouped=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-10)            filter_func=<function <lambda> at 0x11c55cf40>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-11)            warning_message=Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-12)                template="Subplot '$subplot_name' does not support grouped data",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-13)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-14)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-15)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-16)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-17)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-18)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-19)        has_freq=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-20)            filter_func=<function <lambda> at 0x11c55d080>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-21)            warning_message=Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-22)                template="Subplot '$subplot_name' requires frequency to be set",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-23)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-24)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-25)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-26)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-27)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-28)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-29)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-30)    settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-31)        use_caching=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-32)        hline_shape_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-33)            type='line',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-34)            line=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-35)                color='gray',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-36)                dash='dash'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-37)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-38)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-39)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-40)    subplot_settings=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-41)    show_titles=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-42)    show_legend=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-43)    show_column_label=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-44)    hide_id_labels=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-45)    group_id_labels=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-46)    make_subplots_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-47)    layout_kwargs=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-32-48))
    

* * *

## plotting frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.plotting "Permanent link")

Sub-config with settings applied to Plotly figures created from [vectorbtpro.utils.figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/ "vectorbtpro.utils.figure").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-2)    use_widgets=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-3)    use_resampler=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-4)    auto_rangebreaks=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-5)    pre_show_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-6)    show_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-7)    use_gl=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-8)    color_schema=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-9)        increasing='#26a69a',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-10)        decreasing='#ee534f',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-11)        lightblue='#6ca6cd',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-12)        lightpurple='#6c76cd',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-13)        lightpink='#cd6ca6',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-14)        blue='#1f77b4',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-15)        orange='#ff7f0e',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-16)        green='#2ca02c',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-17)        red='#dc3912',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-18)        purple='#9467bd',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-19)        brown='#8c564b',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-20)        pink='#e377c2',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-21)        gray='#7f7f7f',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-22)        yellow='#bcbd22',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-23)        cyan='#17becf'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-24)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-25)    contrast_color_schema=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-26)        blue='#4285F4',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-27)        orange='#FFAA00',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-28)        green='#37B13F',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-29)        red='#EA4335',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-30)        gray='#E2E2E2',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-31)        purple='#A661D5',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-32)        pink='#DD59AA'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-33)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-34)    themes=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-35)        light=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-36)            color_schema=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-37)                blue='#1f77b4',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-38)                orange='#ff7f0e',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-39)                green='#2ca02c',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-40)                red='#dc3912',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-41)                purple='#9467bd',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-42)                brown='#8c564b',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-43)                pink='#e377c2',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-44)                gray='#7f7f7f',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-45)                yellow='#bcbd22',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-46)                cyan='#17becf'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-47)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-48)            path='__name__/templates/light.json'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-49)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-50)        dark=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-51)            color_schema=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-52)                blue='#1f77b4',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-53)                orange='#ff7f0e',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-54)                green='#2ca02c',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-55)                red='#dc3912',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-56)                purple='#9467bd',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-57)                brown='#8c564b',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-58)                pink='#e377c2',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-59)                gray='#7f7f7f',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-60)                yellow='#bcbd22',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-61)                cyan='#17becf'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-62)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-63)            path='__name__/templates/dark.json'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-64)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-65)        seaborn=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-66)            color_schema=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-67)                blue='rgb(76,114,176)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-68)                orange='rgb(221,132,82)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-69)                green='rgb(85,168,104)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-70)                red='rgb(196,78,82)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-71)                purple='rgb(129,114,179)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-72)                brown='rgb(147,120,96)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-73)                pink='rgb(218,139,195)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-74)                gray='rgb(140,140,140)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-75)                yellow='rgb(204,185,116)',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-76)                cyan='rgb(100,181,205)'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-77)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-78)            path='__name__/templates/seaborn.json'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-79)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-80)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-81)    default_theme='light',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-82)    layout=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-83)        width=700,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-84)        height=350,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-85)        margin=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-86)            t=30,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-87)            b=30,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-88)            l=30,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-89)            r=30
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-90)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-91)        legend=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-92)            orientation='h',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-93)            yanchor='bottom',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-94)            y=1.02,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-95)            xanchor='right',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-96)            x=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-97)            traceorder='normal'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-98)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-99)        template='vbt_light'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-100)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-33-101))
    

* * *

## portfolio frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.portfolio "Permanent link")

Sub-config with settings applied to [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio "vectorbtpro.portfolio.base.Portfolio").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-2)    data=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-3)    open=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-4)    high=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-5)    low=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-6)    close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-7)    bm_close=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-8)    val_price='price',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-9)    init_cash=100.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-10)    init_position=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-11)    init_price=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-12)    cash_deposits=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-13)    cash_deposits_as_input=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-14)    cash_earnings=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-15)    cash_dividends=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-16)    cash_sharing=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-17)    ffill_val_price=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-18)    update_value=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-19)    save_state=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-20)    save_value=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-21)    save_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-22)    skip_empty=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-23)    fill_pos_info=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-24)    track_value=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-25)    row_wise=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-26)    seed=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-27)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-28)    broadcast_named_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-29)    broadcast_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-30)        require_kwargs=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-31)            requirements='W'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-32)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-33)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-34)    template_context=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-35)    keep_inout_flex=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-36)    from_ago=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-37)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-38)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-39)    call_seq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-40)    attach_call_seq=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-41)    max_order_records=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-42)    max_log_records=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-43)    jitted=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-44)    chunked=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-45)    staticized=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-46)    records=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-47)    size=np.inf,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-48)    size_type='amount',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-49)    direction='both',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-50)    price='close',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-51)    fees=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-52)    fixed_fees=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-53)    slippage=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-54)    min_size=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-55)    max_size=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-56)    size_granularity=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-57)    leverage=1.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-58)    leverage_mode='lazy',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-59)    reject_prob=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-60)    price_area_vio_mode='ignore',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-61)    allow_partial=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-62)    raise_reject=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-63)    log=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-64)    from_orders=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-65)    from_signals=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-66)        direction='longonly',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-67)        adjust_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-68)        adjust_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-69)        signal_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-70)        signal_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-71)        post_signal_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-72)        post_signal_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-73)        post_segment_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-74)        post_segment_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-75)        order_mode=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-76)        accumulate=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-77)        upon_long_conflict='ignore',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-78)        upon_short_conflict='ignore',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-79)        upon_dir_conflict='ignore',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-80)        upon_opposite_entry='reversereduce',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-81)        order_type='market',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-82)        limit_reverse=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-83)        limit_delta=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-84)        limit_tif=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-85)        limit_expiry=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-86)        limit_order_price='limit',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-87)        upon_adj_limit_conflict='keepignore',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-88)        upon_opp_limit_conflict='cancelexecute',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-89)        use_stops=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-90)        stop_ladder='disabled',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-91)        sl_stop=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-92)        tsl_th=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-93)        tsl_stop=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-94)        tp_stop=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-95)        td_stop=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-96)        dt_stop=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-97)        stop_entry_price='close',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-98)        stop_exit_price='stop',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-99)        stop_order_type='market',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-100)        stop_limit_delta=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-101)        stop_exit_type='close',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-102)        upon_stop_update='override',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-103)        upon_adj_stop_conflict='keepexecute',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-104)        upon_opp_stop_conflict='keepexecute',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-105)        delta_format='percent',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-106)        time_delta_format='index'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-107)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-108)    hold_direction='longonly',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-109)    close_at_end=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-110)    from_order_func=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-111)        segment_mask=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-112)        call_pre_segment=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-113)        call_post_segment=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-114)        pre_sim_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-115)        pre_sim_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-116)        post_sim_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-117)        post_sim_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-118)        pre_group_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-119)        pre_group_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-120)        post_group_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-121)        post_group_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-122)        pre_row_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-123)        pre_row_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-124)        post_row_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-125)        post_row_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-126)        pre_segment_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-127)        pre_segment_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-128)        post_segment_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-129)        post_segment_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-130)        order_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-131)        order_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-132)        flex_order_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-133)        flex_order_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-134)        post_order_func_nb=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-135)        post_order_args=(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-136)        row_wise=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-137)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-138)    from_def_order_func=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-139)        flexible=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-140)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-141)    freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-142)    year_freq=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-143)    use_in_outputs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-144)    fillna_close=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-145)    weights=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-146)    trades_type='exittrades',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-147)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-148)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-149)            has_year_freq=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-150)                filter_func=<function <lambda> at 0x11c55d3a0>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-151)                warning_message=Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-152)                    template="Metric '$metric_name' requires year frequency to be set",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-153)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-154)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-155)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-156)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-157)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-158)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-159)            has_bm_returns=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-160)                filter_func=<function <lambda> at 0x11c55d620>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-161)                warning_message=Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-162)                    template="Metric '$metric_name' requires bm_returns to be set",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-163)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-164)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-165)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-166)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-167)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-168)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-169)            has_cash_deposits=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-170)                filter_func=<function <lambda> at 0x11c55d6c0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-171)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-172)            has_cash_earnings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-173)                filter_func=<function <lambda> at 0x11c55d580>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-174)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-175)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-176)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-177)            use_asset_returns=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-178)            incl_open=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-179)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-180)        template_context=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-181)            incl_open_tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-182)                template="['open', 'closed'] if incl_open else ['closed']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-183)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-184)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-185)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-186)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-187)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-188)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-189)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-190)    plots=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-191)        subplots=[
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-192)            'orders',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-193)            'trade_pnl',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-194)            'cumulative_returns'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-195)        ],
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-196)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-197)            use_asset_returns=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-198)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-199)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-34-200))
    

* * *

## qs_adapter frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.qs_adapter "Permanent link")

Sub-config with settings applied to [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter "vectorbtpro.returns.qs_adapter.QSAdapter").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-35-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-35-2)    defaults=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-35-3))
    

* * *

## ranges frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.ranges "Permanent link")

Sub-config with settings applied to [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges "vectorbtpro.generic.ranges.Ranges").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-36-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-36-2)    stats=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-36-3)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-36-4))
    

* * *

## records frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.records "Permanent link")

Sub-config with settings applied to [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records "vectorbtpro.records.base.Records").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-37-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-37-2)    stats=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-37-3)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-37-4))
    

* * *

## resampling frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.resampling "Permanent link")

Sub-config with settings applied across [vectorbtpro.base.resampling](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/ "vectorbtpro.base.resampling").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-38-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-38-2)    silence_warnings=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-38-3))
    

* * *

## returns frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.returns "Permanent link")

Sub-config with settings applied to [ReturnsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor "vectorbtpro.returns.accessors.ReturnsAccessor").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-2)    inf_to_nan=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-3)    nan_to_zero=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-4)    year_freq='365 days',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-5)    bm_returns=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-6)    defaults=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-7)        start_value=1.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-8)        window=10,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-9)        minp=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-10)        ddof=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-11)        risk_free=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-12)        levy_alpha=2.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-13)        required_return=0.0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-14)        cutoff=0.05,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-15)        periods=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-16)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-17)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-18)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-19)            has_year_freq=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-20)                filter_func=<function <lambda> at 0x11c55d300>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-21)                warning_message=Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-22)                    template="Metric '$metric_name' requires year frequency to be set",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-23)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-24)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-25)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-26)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-27)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-28)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-29)            has_bm_returns=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-30)                filter_func=<function <lambda> at 0x11c55d440>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-31)                warning_message=Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-32)                    template="Metric '$metric_name' requires bm_returns to be set",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-33)                    context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-34)                    strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-35)                    context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-36)                    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-37)                )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-38)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-39)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-40)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-41)            check_is_not_grouped=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-42)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-43)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-44)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-39-45))
    

* * *

## search frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.search "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.search_](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/ "vectorbtpro.utils.search_").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-2)    traversal='DFS',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-3)    excl_types=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-4)        <class 'list'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-5)        <class 'set'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-6)        <class 'frozenset'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-7)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-8)    incl_types=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-9)    max_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-10)    max_depth=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-40-11))
    

* * *

## settings SettingsConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.settings "Permanent link")

Global settings config.

Combines all sub-configs defined in this module.

* * *

## signals frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.signals "Permanent link")

Sub-config with settings applied to [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor "vectorbtpro.signals.accessors.SignalsAccessor").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-2)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-3)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-4)            silent_has_target=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-5)                filter_func=<function <lambda> at 0x11c55cfe0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-6)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-7)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-8)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-9)            target=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-10)            target_name='Target',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-11)            relation='onemany'
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-12)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-14)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-41-15))
    

* * *

## splitter frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.splitter "Permanent link")

Sub-config with settings applied to [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter "vectorbtpro.generic.splitting.base.Splitter").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-2)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-3)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-4)            normalize=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-5)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-6)        filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-7)            has_multiple_sets=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-8)                filter_func=<function <lambda> at 0x11c55d1c0>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-9)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-10)            normalize=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-11)                filter_func=<function <lambda> at 0x11c55d260>
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-12)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-13)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-14)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-15)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-42-16))
    

* * *

## stats_builder frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.stats_builder "Permanent link")

Sub-config with settings applied to [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin "vectorbtpro.generic.stats_builder.StatsBuilderMixin").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-2)    metrics='all',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-3)    tags='all',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-4)    per_column=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-5)    split_columns=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-6)    dropna=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-7)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-8)    template_context=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-9)    filters=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-10)        is_not_grouped=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-11)            filter_func=<function <lambda> at 0x11c55ce00>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-12)            warning_message=Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-13)                template="Metric '$metric_name' does not support grouped data",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-14)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-15)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-16)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-17)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-18)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-19)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-20)        has_freq=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-21)            filter_func=<function <lambda> at 0x11c522f20>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-22)            warning_message=Sub(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-23)                template="Metric '$metric_name' requires frequency to be set",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-24)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-25)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-26)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-27)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-28)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-29)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-30)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-31)    settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-32)        to_timedelta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-33)        use_caching=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-35)    metric_settings=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-43-36))
    

* * *

## telegram frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.telegram "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.telegram](https://vectorbt.pro/pvt_7a467f6b/api/utils/telegram/ "vectorbtpro.utils.telegram").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-2)    bot=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-3)        token=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-4)        use_context=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-5)        persistence=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-6)        defaults=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-7)        drop_pending_updates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-8)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-9)    giphy=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-10)        api_key=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-11)        weirdness=5
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-12)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-44-13))
    

**python-telegram-bot**

Sub-config with settings applied to [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

Set `persistence` to string to use as `filename` in `telegram.ext.PicklePersistence`. For `defaults`, see `telegram.ext.Defaults`. Other settings will be distributed across `telegram.ext.Updater` and `telegram.ext.updater.Updater.start_polling`.

**GIPHY**

Sub-config with settings applied to [GIPHY Translate Endpoint](https://developers.giphy.com/docs/api/endpoint#translate).

* * *

## template frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.template "Permanent link")

Sub-config with settings applied across [vectorbtpro.utils.template](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/ "vectorbtpro.utils.template").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-45-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-45-2)    strict=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-45-3)    search_kwargs=flex_cfg(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-45-4)    context=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-45-5))
    

* * *

## trades frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.trades "Permanent link")

Sub-config with settings applied to [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades "vectorbtpro.portfolio.trades.Trades").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-2)    stats=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-3)        settings=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-4)            incl_open=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-5)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-6)        template_context=flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-7)            incl_open_tags=RepEval(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-8)                template="['open', 'closed'] if incl_open else ['closed']",
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-9)                context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-10)                strict=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-11)                context_merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-12)                eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-13)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-14)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-15)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-16)    plots=flex_cfg()
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-46-17))
    

* * *

## wrapping frozen_cfg[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.wrapping "Permanent link")

Sub-config with settings applied across [vectorbtpro.base.wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/ "vectorbtpro.base.wrapping").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-2)    column_only_select=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-3)    range_only_select=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-4)    group_select=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-5)    freq='auto',
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-6)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-7)    zero_to_none=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-8)    min_precision=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-9)    max_precision=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-10)    prec_float_only=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-11)    prec_check_bounds=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-12)    prec_strict=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-47-13))
    

When enabling `max_precision` and running your code for the first time, make sure to enable `prec_check_bounds`. After that, you can safely disable it to slightly increase performance.

* * *

## SettingsConfig class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L2716-L2821 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-48-1)SettingsConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-48-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-48-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-48-4))
    

Extends [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config") for global settings.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * `builtins.dict`
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Config.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Config.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Config.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Config.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Config.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Config.find_messages")
  * [Config.clear](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.clear "vectorbtpro.utils.config.Config.clear")
  * [Config.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.copy "vectorbtpro.utils.config.Config.copy")
  * [Config.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "vectorbtpro.utils.config.Config.equals")
  * [Config.get_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.get_option "vectorbtpro.utils.config.Config.get_option")
  * [Config.load_update](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "vectorbtpro.utils.config.Config.load_update")
  * [Config.make_checkpoint](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.make_checkpoint "vectorbtpro.utils.config.Config.make_checkpoint")
  * [Config.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.merge_with "vectorbtpro.utils.config.Config.merge_with")
  * [Config.options_](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.options_ "vectorbtpro.utils.config.Config.options_")
  * [Config.pop](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.pop "vectorbtpro.utils.config.Config.pop")
  * [Config.popitem](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.popitem "vectorbtpro.utils.config.Config.popitem")
  * [Config.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Config.prettify")
  * [Config.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Config.rec_state")
  * [Config.reset](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.reset "vectorbtpro.utils.config.Config.reset")
  * [Config.set_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.set_option "vectorbtpro.utils.config.Config.set_option")
  * [Config.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.to_dict "vectorbtpro.utils.config.Config.to_dict")
  * [Config.update](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.update "vectorbtpro.utils.config.Config.update")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Config.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Config.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Config.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Config.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Config.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Config.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Config.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Config.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Config.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Config.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Config.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Config.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Config.pprint")



* * *

### get method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L2781-L2792 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig.get "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-49-1)SettingsConfig.get(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-49-2)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-49-3)    default=_Missing.MISSING
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-49-4))
    

Get setting(s) under a path.

See [get_pathlike_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.get_pathlike_key "vectorbtpro.utils.search_.get_pathlike_key") for path format.

* * *

### register_template method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L2736-L2751 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig.register_template "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-50-1)SettingsConfig.register_template(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-50-2)    theme
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-50-3))
    

Register template of a theme.

* * *

### register_templates method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L2753-L2756 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig.register_templates "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-51-1)SettingsConfig.register_templates()
    

Register templates of all themes.

* * *

### reset_theme method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L2764-L2766 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig.reset_theme "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-52-1)SettingsConfig.reset_theme()
    

Reset to default theme.

* * *

### set method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L2794-L2821 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig.set "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-53-1)SettingsConfig.set(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-53-2)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-53-3)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-53-4)    default_config_type=vectorbtpro._settings.flex_cfg
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-53-5))
    

Set setting(s) under a path.

See [get_pathlike_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/search_/#vectorbtpro.utils.search_.get_pathlike_key "vectorbtpro.utils.search_.get_pathlike_key") for path format.

* * *

### set_theme method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L2758-L2762 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig.set_theme "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-54-1)SettingsConfig.set_theme(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-54-2)    theme
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-54-3))
    

Set default theme.

* * *

### substitute_sub_config_docs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L2768-L2779 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.SettingsConfig.substitute_sub_config_docs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-55-1)SettingsConfig.substitute_sub_config_docs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-55-2)    __pdoc__,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-55-3)    prettify_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-55-4))
    

Substitute templates in sub-config docs.

* * *

## flex_cfg class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L190-L208 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.flex_cfg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-56-1)flex_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-56-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-56-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-56-4))
    

Class representing a flexible sub-config.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * `builtins.dict`
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Config.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Config.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Config.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Config.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Config.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Config.find_messages")
  * [Config.clear](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.clear "vectorbtpro.utils.config.Config.clear")
  * [Config.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.copy "vectorbtpro.utils.config.Config.copy")
  * [Config.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "vectorbtpro.utils.config.Config.equals")
  * [Config.get_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.get_option "vectorbtpro.utils.config.Config.get_option")
  * [Config.load_update](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "vectorbtpro.utils.config.Config.load_update")
  * [Config.make_checkpoint](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.make_checkpoint "vectorbtpro.utils.config.Config.make_checkpoint")
  * [Config.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.merge_with "vectorbtpro.utils.config.Config.merge_with")
  * [Config.options_](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.options_ "vectorbtpro.utils.config.Config.options_")
  * [Config.pop](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.pop "vectorbtpro.utils.config.Config.pop")
  * [Config.popitem](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.popitem "vectorbtpro.utils.config.Config.popitem")
  * [Config.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Config.prettify")
  * [Config.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Config.rec_state")
  * [Config.reset](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.reset "vectorbtpro.utils.config.Config.reset")
  * [Config.set_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.set_option "vectorbtpro.utils.config.Config.set_option")
  * [Config.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.to_dict "vectorbtpro.utils.config.Config.to_dict")
  * [Config.update](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.update "vectorbtpro.utils.config.Config.update")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Config.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Config.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Config.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Config.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Config.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Config.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Config.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Config.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Config.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Config.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Config.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Config.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Config.pprint")



* * *

## frozen_cfg class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/_settings.py#L169-L187 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.frozen_cfg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-57-1)frozen_cfg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-57-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-57-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#__codelineno-57-4))
    

Class representing a frozen sub-config.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * `builtins.dict`
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Config.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Config.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Config.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Config.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Config.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Config.find_messages")
  * [Config.clear](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.clear "vectorbtpro.utils.config.Config.clear")
  * [Config.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.copy "vectorbtpro.utils.config.Config.copy")
  * [Config.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "vectorbtpro.utils.config.Config.equals")
  * [Config.get_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.get_option "vectorbtpro.utils.config.Config.get_option")
  * [Config.load_update](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "vectorbtpro.utils.config.Config.load_update")
  * [Config.make_checkpoint](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.make_checkpoint "vectorbtpro.utils.config.Config.make_checkpoint")
  * [Config.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.merge_with "vectorbtpro.utils.config.Config.merge_with")
  * [Config.options_](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.options_ "vectorbtpro.utils.config.Config.options_")
  * [Config.pop](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.pop "vectorbtpro.utils.config.Config.pop")
  * [Config.popitem](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.popitem "vectorbtpro.utils.config.Config.popitem")
  * [Config.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Config.prettify")
  * [Config.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Config.rec_state")
  * [Config.reset](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.reset "vectorbtpro.utils.config.Config.reset")
  * [Config.set_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.set_option "vectorbtpro.utils.config.Config.set_option")
  * [Config.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.to_dict "vectorbtpro.utils.config.Config.to_dict")
  * [Config.update](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.update "vectorbtpro.utils.config.Config.update")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Config.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Config.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Config.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Config.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Config.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Config.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Config.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Config.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Config.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Config.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Config.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Config.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Config.pprint")


