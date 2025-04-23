# Compilation[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#compilation "Permanent link")

Numba can be disabled globally by setting an environment variable, or by changing the config (see [Environment variables](https://numba.readthedocs.io/en/stable/reference/envvars.html)).

Disable Numba via an environment variable
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-0-1)import os
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-0-3)os.environ["NUMBA_DISABLE_JIT"] = "1"
 
[/code]

Disable Numba via the config
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-1-1)from numba import config
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-1-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-1-3)config.DISABLE_JIT = True
 
[/code]


* * *

+


* * *

Same can be done by creating a [configuration](https://vectorbt.pro/pvt_7a467f6b/cookbook/configuration/#settings) file (such as `vbt.config`) with the following content:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-2-1)[numba]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-2-2)disable = True
 
[/code]

Note

All the commands above have to be done before importing VBT.


* * *

+


* * *

To check whether Numba is enabled, use [is_numba_enabled](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_numba_enabled).

Check whether Numba is enabled
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/compilation/#__codelineno-3-1)print(vbt.is_numba_enabled())
 
[/code]