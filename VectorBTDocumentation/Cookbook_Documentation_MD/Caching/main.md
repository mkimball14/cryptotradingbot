# Caching[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#caching "Permanent link")

Whenever some high-level task should be executed over and over again (for example, during a parameter optimization), it's recommended to occasionally clear the cache with [clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.clear_cache) and collect the memory garbage to avoid growing RAM consumption through cached and dead objects.

Clear cache and collect garbage once every 1000 iterations
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-0-1)for i in range(1_000_000):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-0-2) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-0-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-0-4) if i != 0 and i % 1000 == 0:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-0-5) vbt.flush() 
 
[/code]

 1. 2. 


* * *

+


* * *

To clear the cache of some particular class, method, or instance, pass it directly to the function.

Clear the cache associated with various objects
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-1-1)vbt.clear_cache(vbt.PF) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-1-2)vbt.clear_cache(vbt.PF.total_return) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-1-3)vbt.clear_cache(pf) 
 
[/code]

 1. 2. 3. 


* * *

+


* * *

To print various statistics on the currently stored cache, use [print_cache_stats](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.print_cache_stats).

Various way to print cache statistics
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-2-1)vbt.print_cache_stats() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-2-2)vbt.print_cache_stats(vbt.PF) 
 
[/code]

 1. 2. 


* * *

+


* * *

To disable or enable caching globally, use [disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.disable_caching) and [enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.enable_caching) respectively.

Disable caching globally
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-3-1)vbt.disable_caching()
 
[/code]


* * *

+


* * *

To disable or enable caching within a code block, use the context managers [CachingDisabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled) and [CachingEnabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled) respectively.

How to disable caching within a code block
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-4-1)with vbt.CachingDisabled(): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-4-2) ... 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-4-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-4-4)... 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-4-5)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-4-6)with vbt.CachingDisabled(vbt.PF): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/caching/#__codelineno-4-7) ...
 
[/code]

 1. 2. 3. 4.