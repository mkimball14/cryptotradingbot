# Configuration[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#configuration "Permanent link")


# Objects[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#objects "Permanent link")

Question

Learn more in [Building blocks - Configuring documentation](https://vectorbt.pro/pvt_7a467f6b/documentation/building-blocks/#configuring).

Those VBT objects that subclass [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Configured) (which make up the majority of the implemented classes) store the keyword arguments that were passed to their initializer, available under `config`. Copying an object simply means passing the same config to the class to create a new instance, which can be done automatically with the `copy()` method.

Copy a Portfolio instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-0-1)new_pf = pf.copy()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-0-2)new_pf = vbt.PF(**pf.config) 
 
[/code]

 1. 


* * *

+


* * *

Since changing any information in-place is strongly discouraged due to caching reasons, replacing something means copying the config, changing it, and passing to the class, which can be done automatically with the `replace()` method.

Replace initial capital in a Portfolio instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-1-1)new_pf = pf.replace(init_cash=1_000_000)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-1-2)new_pf = vbt.PF(**vbt.merge_dicts(pf.config, dict(init_cash=1_000_000)) 
 
[/code]

 1. 


* * *

+


* * *

In many cases, one VBT object contains other VBT objects. To make changes to some deep vectorbtpro object, we can enable the `nested_` flag and pass the instruction as a nested dict.

Enable grouping in the wrapper of a Portfolio instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-2-1)new_pf = pf.replace(wrapper=dict(group_by=True), nested_=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-2-2)new_pf = pf.replace(wrapper=pf.wrapper.replace(group_by=True)) 
 
[/code]

 1. 


* * *

+


* * *

The same VBT objects can be saved as config files for effortless editing. Such a config file has a format that is very similar to the [INI format](https://en.wikipedia.org/wiki/INI_file) but enriched with various extensions such as code expressions and nested dictionaries, which allows representation of objects of any complexity.

Save a Portfolio instance to a config file and load it back
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-3-1)pf.save(file_format="config")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-3-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-3-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-3-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-3-5)pf = vbt.PF.load()
 
[/code]

 1. 


# Settings[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#settings "Permanent link")

Settings that control the default behavior of most functionalities across VBT are located under [_settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings). Each functionality has its own config; for example, [settings.portfolio](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.portfolio) defines the defaults around the [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) class. All configs are then consolidated into a single config that can be accessed via `vbt.settings`.

Set the default initial cash
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-4-1)vbt.settings.portfolio.init_cash = 1_000_000
 
[/code]


* * *

+


* * *

The initial state of any config can be accessed via `options_["reset_dct"]`.

Get the default initial cash before any changes
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-5-1)print(vbt.settings.portfolio.options_["reset_dct"]["init_cash"]) 
 
[/code]

 1. 


* * *

+


* * *

Any config can be reset to its initial state by using the `reset()` method.

Reset the Portfolio config
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-6-1)vbt.settings.portfolio.reset()
 
[/code]


* * *

+


* * *

For more convenience, settings can be defined in a text file that will be loaded automatically the next time VBT is imported. The file should be placed in the directory of the script that is importing the package, and named `vbt.ini` or `vbt.config`. Or, the path to the settings file can be also provided by setting the environment variable `VBT_SETTINGS_PATH`. It must have the [INI format](https://en.wikipedia.org/wiki/INI_file#Format) that has been extended by vectorbtpro, see [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config) for examples.

Configuration file that defines the default initial cash
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-7-1)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-7-2)[portfolio]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-7-3)init_cash = 1_000_000
 
[/code]

 1. 


* * *

+


* * *

This is especially useful for changing the settings that take into effect only once on import, such as various Numba-related settings and caching and chunking machineries.

Configuration file that disables Numba
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-8-1)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-8-2)[numba]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-8-3)disable = True
 
[/code]

 1. 


* * *

+


* * *

To save all settings or some specific config to a text file, modify it, and let VBT load it on import (or do it manually), use the `save()` method with `file_format="config"`.

Save Portfolio config and import it automatically
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-9-1)vbt.settings.portfolio.save("vbt.config", top_name="portfolio")
 
[/code]

Save Portfolio config and import it manually
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-10-1)vbt.settings.portfolio.save("portfolio.config")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-10-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-10-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-10-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-10-5)vbt.settings.portfolio.load_update("portfolio.config")
 
[/code]

 1. 


* * *

+


* * *

If readability of the file is not of relevance, settings can be modified in place and then saved to a Pickle file in one Python session to be automatically imported in the next session.

Disable Numba in the next Python session
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-11-1)vbt.settings.numba.disable = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#__codelineno-11-2)vbt.settings.save("vbt")
 
[/code]

Warning

This approach is discouraged if you plan to upgrade VBT frequently, as each new release may introduce changes to the settings.