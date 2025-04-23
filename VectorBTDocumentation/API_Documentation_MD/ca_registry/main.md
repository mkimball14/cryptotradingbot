ca_registry caching

#  ca_registry module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry "Permanent link")

Global registry for cacheables.

Caching in vectorbt is achieved through a combination of decorators and the registry. Cacheable decorators such as [cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable "vectorbtpro.utils.decorators.cacheable") take a function and wrap it with another function that behaves like the wrapped function but also takes care of all caching modalities.

But unlike other implementations such as that of `functools.lru_cache`, the actual caching procedure doesn't happen nor are the results stored inside the decorators themselves: decorators just register a so-called "setup" for the wrapped function at the registry (see [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup")).

## Runnable setups[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#runnable-setups "Permanent link")

The actual magic happens within a runnable setup: it takes the function that should be called and the arguments that should be passed to this function, looks whether the result should be cached, runs the function, stores the result in the cache, updates the metrics, etc. It then returns the resulting object to the wrapping function, which in turn returns it to the user. Each setup is stateful - it stores the cache, the number of hits and misses, and other metadata. Thus, there can be only one registered setup per each cacheable function globally at a time. To avoid creating new setups for the same function over and over again, each setup can be uniquely identified by its function through hashing:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-3)>>> my_func = lambda: np.random.uniform(size=1000000)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-5)>>> # Decorator returns a wrapper
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-6)>>> my_ca_func = vbt.cached(my_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-8)>>> # Wrapper registers a new setup
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-9)>>> my_ca_func.get_ca_setup()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-10)CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<function <lambda> at 0x7fe14e94cae8>, instance=None, max_size=None, ignore_args=None, cache={})
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-12)>>> # Another call won't register a new setup but return the existing one
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-13)>>> my_ca_func.get_ca_setup()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-14)CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<function <lambda> at 0x7fe14e94cae8>, instance=None, max_size=None, ignore_args=None, cache={})
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-16)>>> # Only one CARunSetup object per wrapper and optionally the instance the wrapper is bound to
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-17)>>> hash(my_ca_func.get_ca_setup()) == hash((my_ca_func, None))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-0-18)True
    

When we call `my_ca_func`, it takes the setup from the registry and calls [CARunSetup.run](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.run "vectorbtpro.registries.ca_registry.CARunSetup.run"). The caching happens by the setup itself and isn't in any way visible to `my_ca_func`. To access the cache or any metric of interest, we can ask the setup:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-1)>>> my_setup = my_ca_func.get_ca_setup()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-3)>>> # Cache is empty
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-4)>>> my_setup.get_stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-5){
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-6)    'hash': 4792160544297109364,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-7)    'string': '<bound func __main__.<lambda>>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-8)    'use_cache': True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-9)    'whitelist': False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-10)    'caching_enabled': True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-11)    'hits': 0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-12)    'misses': 0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-13)    'total_size': '0 Bytes',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-14)    'total_elapsed': None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-15)    'total_saved': None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-16)    'first_run_time': None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-17)    'last_run_time': None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-18)    'first_hit_time': None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-19)    'last_hit_time': None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-20)    'creation_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-21)    'last_update_time': None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-22)}
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-23)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-24)>>> # The result is cached
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-25)>>> my_ca_func()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-26)>>> my_setup.get_stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-27){
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-28)    'hash': 4792160544297109364,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-29)    'string': '<bound func __main__.<lambda>>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-30)    'use_cache': True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-31)    'whitelist': False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-32)    'caching_enabled': True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-33)    'hits': 0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-34)    'misses': 1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-35)    'total_size': '8.0 MB',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-36)    'total_elapsed': '11.33 milliseconds',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-37)    'total_saved': '0 milliseconds',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-38)    'first_run_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-39)    'last_run_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-40)    'first_hit_time': None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-41)    'last_hit_time': None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-42)    'creation_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-43)    'last_update_time': None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-44)}
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-45)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-46)>>> # The cached result is retrieved
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-47)>>> my_ca_func()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-48)>>> my_setup.get_stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-49){
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-50)    'hash': 4792160544297109364,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-51)    'string': '<bound func __main__.<lambda>>',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-52)    'use_cache': True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-53)    'whitelist': False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-54)    'caching_enabled': True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-55)    'hits': 1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-56)    'misses': 1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-57)    'total_size': '8.0 MB',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-58)    'total_elapsed': '11.33 milliseconds',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-59)    'total_saved': '11.33 milliseconds',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-60)    'first_run_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-61)    'last_run_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-62)    'first_hit_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-63)    'last_hit_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-64)    'creation_time': 'now',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-65)    'last_update_time': None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-1-66)}
    

## Enabling/disabling caching[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#enablingdisabling-caching "Permanent link")

To enable or disable caching, we can invoke [CABaseSetup.enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching "vectorbtpro.registries.ca_registry.CARunSetup.enable_caching") and [CABaseSetup.disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching "vectorbtpro.registries.ca_registry.CARunSetup.disable_caching") respectively. This will set [CARunSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CARunSetup.use_cache") flag to True or False. Even though we expressed our disire to change caching rules, the final decision also depends on the global settings and whether the setup is whitelisted in case caching is disabled globally. This decision is available via [CARunSetup.caching_enabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled "vectorbtpro.registries.ca_registry.CARunSetup.caching_enabled"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-1)>>> my_setup.disable_caching()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-2)>>> my_setup.caching_enabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-3)False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-5)>>> my_setup.enable_caching()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-6)>>> my_setup.caching_enabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-7)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-9)>>> vbt.settings.caching['disable'] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-10)>>> my_setup.caching_enabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-11)False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-13)>>> my_setup.enable_caching()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-14)UserWarning: This operation has no effect: caching is disabled globally and this setup is not whitelisted
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-16)>>> my_setup.enable_caching(force=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-17)>>> my_setup.caching_enabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-18)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-19)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-20)>>> vbt.settings.caching['disable_whitelist'] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-21)>>> my_setup.caching_enabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-22)False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-23)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-24)>>> my_setup.enable_caching(force=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-2-25)UserWarning: This operation has no effect: caching and whitelisting are disabled globally
    

To disable registration of new setups completely, use `disable_machinery`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-3-1)>>> vbt.settings.caching['disable_machinery'] = True
    

## Setup hierarchy[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#setup-hierarchy "Permanent link")

But what if we wanted to change caching rules for an entire instance or class at once? Even if we changed the setup of every cacheable function declared in the class, how do we make sure that each future subclass or instance inherits the changes that we applied? To account for this, vectorbt provides us with a set of setups that both are stateful and can delegate various operations to their child setups, all the way down to [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup"). The setup hierarchy follows the inheritance hierarchy in OOP:

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/setup_hierarchy.svg)

For example, calling `B.get_ca_setup().disable_caching()` would disable caching for each current and future subclass and instance of `B`, but it won't disable caching for `A` or any other superclass of `B`. In turn, each instance of `B` would then disable caching for each cacheable property and method in that instance. As we see, the propagation of this operation is happening from top to bottom.

The reason why unbound setups are stretching outside of their classes in the diagram is because there is no easy way to derive the class when calling a cacheable decorator, thus their functions are considered to be living on their own. When calling `B.f.get_ca_setup().disable_caching()`, we are disabling caching for the function `B.f` for each current and future subclass and instance of `B`, while all other functions remain untouched.

But what happens when we enable caching for the class `B` and disable caching for the unbound function `B.f`? Would the future method `b2.f` be cached or not? Quite easy: it would then inherit the state from the setup that has been updated more recently.

Here is another illustration of how operations are propagated from parents to children:

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/api/setup_propagation.svg)

The diagram above depicts the following setup hierarchy:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-1)>>> # Populate setups at init
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-2)>>> vbt.settings.caching.reset()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-3)>>> vbt.settings.caching['register_lazily'] = False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-5)>>> class A(vbt.Cacheable):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-6)...     @vbt.cached_property
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-7)...     def f1(self): pass
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-9)>>> class B(A):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-10)...     def f2(self): pass
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-12)>>> class C(A):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-13)...     @vbt.cached_method
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-14)...     def f2(self): pass
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-16)>>> b1 = B()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-17)>>> c1 = C()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-18)>>> c2 = C()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-19)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-20)>>> print(vbt.prettify(A.get_ca_setup().get_setup_hierarchy()))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-21)[
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-22)    {
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-23)        "parent": "<class __main__.B>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-24)        "children": [
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-25)            {
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-26)                "parent": "<instance of __main__.B>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-27)                "children": [
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-28)                    "<instance property __main__.B.f1>"
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-29)                ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-30)            }
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-31)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-32)    },
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-33)    {
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-34)        "parent": "<class __main__.C>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-35)        "children": [
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-36)            {
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-37)                "parent": "<instance of __main__.C>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-38)                "children": [
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-39)                    "<instance method __main__.C.f2>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-40)                    "<instance property __main__.C.f1>"
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-41)                ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-42)            },
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-43)            {
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-44)                "parent": "<instance of __main__.C>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-45)                "children": [
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-46)                    "<instance method __main__.C.f2>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-47)                    "<instance property __main__.C.f1>"
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-48)                ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-49)            }
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-50)        ]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-51)    }
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-52)]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-53)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-54)>>> print(vbt.prettify(A.f1.get_ca_setup().get_setup_hierarchy()))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-55)[
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-56)    "<instance property __main__.C.f1>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-57)    "<instance property __main__.C.f1>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-58)    "<instance property __main__.B.f1>"
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-59)]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-60)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-61)>>> print(vbt.prettify(C.f2.get_ca_setup().get_setup_hierarchy()))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-62)[
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-63)    "<instance method __main__.C.f2>",
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-64)    "<instance method __main__.C.f2>"
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-4-65)]
    

Let's disable caching for the entire `A` class:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-5-1)>>> A.get_ca_setup().disable_caching()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-5-2)>>> A.get_ca_setup().use_cache
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-5-3)False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-5-4)>>> B.get_ca_setup().use_cache
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-5-5)False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-5-6)>>> C.get_ca_setup().use_cache
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-5-7)False
    

This disabled caching for `A`, subclasses `B` and `C`, their instances, and any instance function. But it didn't touch unbound functions such as `C.f1` and `C.f2`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-6-1)>>> C.f1.get_ca_setup().use_cache
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-6-2)True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-6-3)>>> C.f2.get_ca_setup().use_cache
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-6-4)True
    

This is because unbound functions are not children of the classes they are declared in! Still, any future instance method of `C` won't be cached because it looks which parent has been updated more recently: the class or the unbound function. In our case, the class had a more recent update.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-7-1)>>> c3 = C()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-7-2)>>> C.f2.get_ca_setup(c3).use_cache
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-7-3)False
    

In fact, if we want to disable an entire class but leave one function untouched, we need to perform two operations in a particular order: 1) disable caching on the class and 2) enable caching on the unbound function.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-8-1)>>> A.get_ca_setup().disable_caching()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-8-2)>>> C.f2.get_ca_setup().enable_caching()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-8-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-8-4)>>> c4 = C()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-8-5)>>> C.f2.get_ca_setup(c4).use_cache
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-8-6)True
    

## Getting statistics[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#getting-statistics "Permanent link")

The main advantage of having a central registry of setups is that we can easily find any setup registered in any part of vectorbt that matches some condition using [CacheableRegistry.match_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.match_setups "vectorbtpro.registries.ca_registry.CacheableRegistry.match_setups").

Note

By default, all setups are registered lazily - no setup is registered until it's run or explicitly called. To change this behavior, set `register_lazily` in the global settings to False.

For example, let's look which setups have been registered so far:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-1)>>> vbt.ca_reg.match_setups(kind=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-2){
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-3)    CAClassSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=None, whitelist=None, cls=<class '__main__.B'>),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-4)    CAClassSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=None, whitelist=None, cls=<class '__main__.C'>),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-5)    CAInstanceSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=None, whitelist=None, instance=<weakref at 0x7fe14e9d83b8; to 'B' at 0x7fe14e944978>),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-6)    CAInstanceSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=None, whitelist=None, instance=<weakref at 0x7fe14e9d84f8; to 'C' at 0x7fe14e9448d0>),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-7)    CAInstanceSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=None, whitelist=None, instance=<weakref at 0x7fe14e9d8688; to 'C' at 0x7fe1495111d0>),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-8)    CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<function <lambda> at 0x7fe14e94cae8>, instance=None, max_size=None, ignore_args=None, cache={}),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-9)    CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<function C.f2 at 0x7fe13959ee18>, instance=<weakref at 0x7fe14e9d85e8; to 'C' at 0x7fe14e9448d0>, max_size=None, ignore_args=None, cache={}),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-10)    CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<function C.f2 at 0x7fe13959ee18>, instance=<weakref at 0x7fe14e9d8728; to 'C' at 0x7fe1495111d0>, max_size=None, ignore_args=None, cache={}),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-11)    CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<vectorbtpro.utils.decorators.cached_property object at 0x7fe118045408>, instance=<weakref at 0x7fe14e9d8458; to 'B' at 0x7fe14e944978>, max_size=None, ignore_args=None, cache={}),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-12)    CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<vectorbtpro.utils.decorators.cached_property object at 0x7fe118045408>, instance=<weakref at 0x7fe14e9d8598; to 'C' at 0x7fe14e9448d0>, max_size=None, ignore_args=None, cache={}),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-13)    CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<vectorbtpro.utils.decorators.cached_property object at 0x7fe118045408>, instance=<weakref at 0x7fe14e9d86d8; to 'C' at 0x7fe1495111d0>, max_size=None, ignore_args=None, cache={}),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-14)    CAUnboundSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<function C.f2 at 0x7fe13959ee18>),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-15)    CAUnboundSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<vectorbtpro.utils.decorators.cached_property object at 0x7fe118045408>)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-9-16)}
    

Let's get the runnable setup of any property and method called `f2`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-10-1)>>> vbt.ca_reg.match_setups('f2', kind='runnable')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-10-2){
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-10-3)    CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<function C.f2 at 0x7fe13959ee18>, instance=<weakref at 0x7fe14e9d85e8; to 'C' at 0x7fe14e9448d0>, max_size=None, ignore_args=None, cache={}),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-10-4)    CARunSetup(registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object at 0x7fe14c27df60>, use_cache=True, whitelist=False, cacheable=<function C.f2 at 0x7fe13959ee18>, instance=<weakref at 0x7fe14e9d8728; to 'C' at 0x7fe1495111d0>, max_size=None, ignore_args=None, cache={})
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-10-5)}
    

But there is a better way to get the stats: [CASetupDelegatorMixin.get_stats](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_stats "vectorbtpro.registries.ca_registry.CAQueryDelegator.get_stats"). It returns a DataFrame with setup stats as rows:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-1)>>> vbt.CAQueryDelegator('f2', kind='runnable').get_stats()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-2)                                               string  use_cache  whitelist  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-3)hash
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-4) 3506416602224216137  <instance method __main__.C.f2>       True      False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-5)-4747092115268118855  <instance method __main__.C.f2>       True      False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-6)-4748466030718995055  <instance method __main__.C.f2>       True      False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-8)                      caching_enabled  hits  misses total_size total_elapsed  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-9)hash
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-10) 3506416602224216137             True     0       0    0 Bytes          None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-11)-4747092115268118855             True     0       0    0 Bytes          None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-12)-4748466030718995055             True     0       0    0 Bytes          None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-13)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-14)                     total_saved first_run_time last_run_time first_hit_time  \
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-15)hash
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-16) 3506416602224216137        None           None          None           None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-17)-4747092115268118855        None           None          None           None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-18)-4748466030718995055        None           None          None           None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-19)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-20)                     last_hit_time  creation_time last_update_time
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-21)hash
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-22) 3506416602224216137          None  9 minutes ago    9 minutes ago
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-23)-4747092115268118855          None  9 minutes ago    9 minutes ago
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-11-24)-4748466030718995055          None  9 minutes ago    9 minutes ago
    

## Clearing up[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#clearing-up "Permanent link")

Instance and runnable setups hold only weak references to their instances such that deleting those instances won't keep them in memory and will automatically remove the setups.

To clear all caches:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-12-1)>>> vbt.CAQueryDelegator().clear_cache()
    

## Resetting[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#resetting "Permanent link")

To reset global caching flags:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-13-1)>>> vbt.settings.caching.reset()
    

To remove all setups:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-14-1)>>> vbt.CAQueryDelegator(kind=None).deregister()
    

* * *

## ca_reg CacheableRegistry[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.ca_reg "Permanent link")

Default registry of type [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry").

* * *

## clear_cache function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2534-L2536 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.clear_cache "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-15-1)clear_cache(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-15-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-15-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-15-4))
    

Clear cache globally or of an object.

* * *

## collect_garbage function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2539-L2543 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.collect_garbage "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-16-1)collect_garbage()
    

Collect garbage.

* * *

## disable_caching function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2552-L2563 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.disable_caching "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-17-1)disable_caching(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-17-2)    clear_cache=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-17-3))
    

Disable caching globally.

* * *

## enable_caching function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2566-L2574 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.enable_caching "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-18-1)enable_caching()
    

Enable caching globally.

* * *

## flush function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2546-L2549 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.flush "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-19-1)flush()
    

Clear cache and collect garbage.

* * *

## get_cache_stats function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2513-L2526 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.get_cache_stats "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-20-1)get_cache_stats(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-20-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-20-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-20-4))
    

Get cache stats globally or of an object.

* * *

## get_obj_id function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L496-L498 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.get_obj_id "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-21-1)get_obj_id(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-21-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-21-3))
    

Get id of an instance.

* * *

## is_bindable_cacheable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L486-L488 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.is_bindable_cacheable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-22-1)is_bindable_cacheable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-22-2)    cacheable
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-22-3))
    

Check if `cacheable` is a cacheable that can be bound to an instance.

* * *

## is_cacheable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L491-L493 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.is_cacheable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-23-1)is_cacheable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-23-2)    cacheable
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-23-3))
    

Check if `cacheable` is a cacheable.

* * *

## is_cacheable_function function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L459-L467 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.is_cacheable_function "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-24-1)is_cacheable_function(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-24-2)    cacheable
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-24-3))
    

Check if `cacheable` is a cacheable function.

* * *

## is_cacheable_method function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L475-L483 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.is_cacheable_method "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-25-1)is_cacheable_method(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-25-2)    cacheable
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-25-3))
    

Check if `cacheable` is a cacheable method.

* * *

## is_cacheable_property function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L470-L472 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.is_cacheable_property "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-26-1)is_cacheable_property(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-26-2)    cacheable
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-26-3))
    

Check if `cacheable` is a cacheable property.

* * *

## print_cache_stats function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2529-L2531 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.print_cache_stats "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-27-1)print_cache_stats(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-27-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-27-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-27-4))
    

Print cache stats globally or of an object.

* * *

## with_caching_disabled function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2746-L2761 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.with_caching_disabled "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-28-1)with_caching_disabled(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-28-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-28-3)    **caching_disabled_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-28-4))
    

Decorator to run a function with [CachingDisabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled "vectorbtpro.registries.ca_registry.CachingDisabled").

* * *

## with_caching_enabled function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2933-L2948 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.with_caching_enabled "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-29-1)with_caching_enabled(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-29-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-29-3)    **caching_enabled_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-29-4))
    

Decorator to run a function with [CachingEnabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled "vectorbtpro.registries.ca_registry.CachingEnabled").

* * *

## CABaseDelegatorSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1599-L1630 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-30-1)CABaseDelegatorSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-30-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-30-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-30-4))
    

Base class acting as a stateful setup that delegates cache management to child setups.

First delegates the work and only then changes its own state.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")
  * [CASetupDelegatorMixin](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.registries.ca_registry.CABaseSetup.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.registries.ca_registry.CABaseSetup.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.registries.ca_registry.CABaseSetup.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.registries.ca_registry.CABaseSetup.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.registries.ca_registry.CABaseSetup.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.registries.ca_registry.CABaseSetup.find_messages")
  * [CABaseSetup.activate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.activate "vectorbtpro.registries.ca_registry.CABaseSetup.activate")
  * [CABaseSetup.active](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.active "vectorbtpro.registries.ca_registry.CABaseSetup.active")
  * [CABaseSetup.caching_enabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled "vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled")
  * [CABaseSetup.clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache "vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache")
  * [CABaseSetup.creation_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.creation_time "vectorbtpro.registries.ca_registry.CABaseSetup.creation_time")
  * [CABaseSetup.deactivate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deactivate "vectorbtpro.registries.ca_registry.CABaseSetup.deactivate")
  * [CABaseSetup.deregister](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deregister "vectorbtpro.registries.ca_registry.CABaseSetup.deregister")
  * [CABaseSetup.disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching "vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching")
  * [CABaseSetup.disable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist")
  * [CABaseSetup.enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching "vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching")
  * [CABaseSetup.enable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist")
  * [CABaseSetup.enforce_rules](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enforce_rules "vectorbtpro.registries.ca_registry.CABaseSetup.enforce_rules")
  * [CABaseSetup.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.registries.ca_registry.CABaseSetup.fields")
  * [CABaseSetup.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.registries.ca_registry.CABaseSetup.fields_dict")
  * [CABaseSetup.first_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "vectorbtpro.registries.ca_registry.CABaseSetup.first_hit_time")
  * [CABaseSetup.first_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "vectorbtpro.registries.ca_registry.CABaseSetup.first_run_time")
  * [CABaseSetup.get_stats](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.get_stats "vectorbtpro.registries.ca_registry.CABaseSetup.get_stats")
  * [CABaseSetup.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.registries.ca_registry.CABaseSetup.hash")
  * [CABaseSetup.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.registries.ca_registry.CABaseSetup.hash_key")
  * [CABaseSetup.hits](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "vectorbtpro.registries.ca_registry.CABaseSetup.hits")
  * [CABaseSetup.last_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "vectorbtpro.registries.ca_registry.CABaseSetup.last_hit_time")
  * [CABaseSetup.last_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "vectorbtpro.registries.ca_registry.CABaseSetup.last_run_time")
  * [CABaseSetup.last_update_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.last_update_time "vectorbtpro.registries.ca_registry.CABaseSetup.last_update_time")
  * [CABaseSetup.metrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "vectorbtpro.registries.ca_registry.CABaseSetup.metrics")
  * [CABaseSetup.misses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "vectorbtpro.registries.ca_registry.CABaseSetup.misses")
  * [CABaseSetup.position_among_similar](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.position_among_similar "vectorbtpro.registries.ca_registry.CABaseSetup.position_among_similar")
  * [CABaseSetup.query](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.query "vectorbtpro.registries.ca_registry.CABaseSetup.query")
  * [CABaseSetup.readable_name](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_name "vectorbtpro.registries.ca_registry.CABaseSetup.readable_name")
  * [CABaseSetup.readable_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_str "vectorbtpro.registries.ca_registry.CABaseSetup.readable_str")
  * [CABaseSetup.register](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.register "vectorbtpro.registries.ca_registry.CABaseSetup.register")
  * [CABaseSetup.registered](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registered "vectorbtpro.registries.ca_registry.CABaseSetup.registered")
  * [CABaseSetup.registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registry "vectorbtpro.registries.ca_registry.CABaseSetup.registry")
  * [CABaseSetup.same_type_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.same_type_setups "vectorbtpro.registries.ca_registry.CABaseSetup.same_type_setups")
  * [CABaseSetup.short_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.short_str "vectorbtpro.registries.ca_registry.CABaseSetup.short_str")
  * [CABaseSetup.total_elapsed](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "vectorbtpro.registries.ca_registry.CABaseSetup.total_elapsed")
  * [CABaseSetup.total_saved](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "vectorbtpro.registries.ca_registry.CABaseSetup.total_saved")
  * [CABaseSetup.total_size](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "vectorbtpro.registries.ca_registry.CABaseSetup.total_size")
  * [CABaseSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseSetup.use_cache")
  * [CABaseSetup.use_cache_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache_lut "vectorbtpro.registries.ca_registry.CABaseSetup.use_cache_lut")
  * [CABaseSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.whitelist")
  * [CABaseSetup.whitelist_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist_lut "vectorbtpro.registries.ca_registry.CABaseSetup.whitelist_lut")
  * [CASetupDelegatorMixin.delegate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.delegate "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.delegate")
  * [CASetupDelegatorMixin.get_setup_hierarchy](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_setup_hierarchy "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_setup_hierarchy")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.registries.ca_registry.CABaseSetup.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.registries.ca_registry.CABaseSetup.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.registries.ca_registry.CABaseSetup.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.registries.ca_registry.CABaseSetup.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.registries.ca_registry.CABaseSetup.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.registries.ca_registry.CABaseSetup.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.registries.ca_registry.CABaseSetup.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.registries.ca_registry.CABaseSetup.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.registries.ca_registry.CABaseSetup.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.registries.ca_registry.CABaseSetup.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.registries.ca_registry.CABaseSetup.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.registries.ca_registry.CABaseSetup.get_hash")



**Subclasses**

  * [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup")
  * [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup")
  * [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup")



* * *

### child_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1604-L1607 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.child_setups "Permanent link")

Get child setups that match [CABaseDelegatorSetup.query](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.query "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.query").

* * *

## CABaseSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1150-L1405 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-31-1)CABaseSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-31-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-31-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-31-4))
    

Base class that exposes properties and methods for cache management.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.registries.ca_registry.CAMetrics.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.registries.ca_registry.CAMetrics.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.registries.ca_registry.CAMetrics.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.registries.ca_registry.CAMetrics.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.registries.ca_registry.CAMetrics.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.registries.ca_registry.CAMetrics.find_messages")
  * [CAMetrics.first_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time")
  * [CAMetrics.first_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "vectorbtpro.registries.ca_registry.CAMetrics.first_run_time")
  * [CAMetrics.hits](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "vectorbtpro.registries.ca_registry.CAMetrics.hits")
  * [CAMetrics.last_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time")
  * [CAMetrics.last_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "vectorbtpro.registries.ca_registry.CAMetrics.last_run_time")
  * [CAMetrics.metrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "vectorbtpro.registries.ca_registry.CAMetrics.metrics")
  * [CAMetrics.misses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "vectorbtpro.registries.ca_registry.CAMetrics.misses")
  * [CAMetrics.total_elapsed](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed")
  * [CAMetrics.total_saved](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "vectorbtpro.registries.ca_registry.CAMetrics.total_saved")
  * [CAMetrics.total_size](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "vectorbtpro.registries.ca_registry.CAMetrics.total_size")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.attr_.DefineMixin.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing")
  * [DefineMixin.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.attr_.DefineMixin.fields")
  * [DefineMixin.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.attr_.DefineMixin.fields_dict")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.attr_.DefineMixin.get_field")
  * [DefineMixin.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.attr_.DefineMixin.hash")
  * [DefineMixin.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.attr_.DefineMixin.hash_key")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.attr_.DefineMixin.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.attr_.DefineMixin.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.attr_.DefineMixin.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.attr_.DefineMixin.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.attr_.DefineMixin.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.attr_.DefineMixin.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.attr_.DefineMixin.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



**Subclasses**

  * [CABaseDelegatorSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup")
  * [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup")



* * *

### activate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1221-L1223 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.activate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-32-1)CABaseSetup.activate()
    

Activate.

* * *

### active field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.active "Permanent link")

Whether to register and/or return setup when requested.

* * *

### caching_enabled field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1176-L1201 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled "Permanent link")

Whether caching is enabled in this setup.

Caching is disabled when any of the following apply:

  * [CARunSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CARunSetup.use_cache") is False
  * Caching is disabled globally and [CARunSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CARunSetup.whitelist") is False
  * Caching and whitelisting are disabled globally



Returns None if [CABaseSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseSetup.use_cache") or [CABaseSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.whitelist") is None.

* * *

### clear_cache method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1295-L1297 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-33-1)CABaseSetup.clear_cache()
    

Clear the cache.

* * *

### creation_time field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1269-L1272 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.creation_time "Permanent link")

Time when this setup was created.

* * *

### deactivate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1225-L1227 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deactivate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-34-1)CABaseSetup.deactivate()
    

Deactivate.

* * *

### deregister method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1207-L1209 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deregister "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-35-1)CABaseSetup.deregister()
    

Register setup using [CacheableRegistry.deregister_setup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.deregister_setup "vectorbtpro.registries.ca_registry.CacheableRegistry.deregister_setup").

* * *

### disable_caching method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1260-L1267 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-36-1)CABaseSetup.disable_caching(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-36-2)    clear_cache=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-36-3))
    

Disable caching.

Set [clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.clear_cache "vectorbtpro.registries.ca_registry.clear_cache") to True to also clear the cache.

* * *

### disable_whitelist method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1234-L1237 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-37-1)CABaseSetup.disable_whitelist()
    

Disable whitelisting.

* * *

### enable_caching method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1239-L1258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-38-1)CABaseSetup.enable_caching(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-38-2)    force=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-38-3)    silence_warnings=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-38-4))
    

Enable caching.

Set `force` to True to whitelist this setup.

* * *

### enable_whitelist method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1229-L1232 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-39-1)CABaseSetup.enable_whitelist()
    

Enable whitelisting.

* * *

### enforce_rules method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1216-L1219 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enforce_rules "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-40-1)CABaseSetup.enforce_rules()
    

Enforce registry rules.

* * *

### get_stats method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1332-L1405 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.get_stats "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-41-1)CABaseSetup.get_stats(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-41-2)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-41-3)    short_str=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-41-4))
    

Get stats of the setup as a dict with metrics.

* * *

### last_update_time field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1284-L1293 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.last_update_time "Permanent link")

Last time any of [CABaseSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseSetup.use_cache") and [CABaseSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.whitelist") were updated.

* * *

### position_among_similar field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1314-L1325 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.position_among_similar "Permanent link")

Get position among all similar setups.

Ordered by creation time.

* * *

### query field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1171-L1174 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.query "Permanent link")

Query to match this setup.

* * *

### readable_name field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1309-L1312 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_name "Permanent link")

Get a readable name of the object the setup is bound to.

* * *

### readable_str field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1327-L1330 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_str "Permanent link")

Convert this setup into a readable string.

* * *

### register method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1203-L1205 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.register "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-42-1)CABaseSetup.register()
    

Register setup using [CacheableRegistry.register_setup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.register_setup "vectorbtpro.registries.ca_registry.CacheableRegistry.register_setup").

* * *

### registered field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1211-L1214 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registered "Permanent link")

Return whether setup is registered.

* * *

### registry field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registry "Permanent link")

Registry of type [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry").

* * *

### same_type_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1299-L1302 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.same_type_setups "Permanent link")

Setups of the same type.

* * *

### short_str field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1304-L1307 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.short_str "Permanent link")

Convert this setup into a short string.

* * *

### use_cache field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "Permanent link")

Whether caching is enabled.

* * *

### use_cache_lut field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1274-L1277 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache_lut "Permanent link")

Last time [CABaseSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseSetup.use_cache") was updated.

* * *

### whitelist field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "Permanent link")

Whether to cache even if caching was disabled globally.

* * *

### whitelist_lut field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1279-L1282 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist_lut "Permanent link")

Last time [CABaseSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.whitelist") was updated.

* * *

## CAClassSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1642-L1829 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-43-1)CAClassSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-43-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-43-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-43-4))
    

Class that represents a setup of a cacheable class.

The provided class must subclass [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable").

Delegates cache management to its child subclass setups of type [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup") and child instance setups of type [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup").

If `use_cash` or `whitelist` are None, inherits a non-empty value from its superclass setups using the method resolution order (MRO).

Note

Unbound setups are not children of class setups. See notes on [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CABaseDelegatorSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup")
  * [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")
  * [CASetupDelegatorMixin](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_messages")
  * [CABaseDelegatorSetup.active](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.active "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.active")
  * [CABaseDelegatorSetup.caching_enabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.caching_enabled")
  * [CABaseDelegatorSetup.child_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.child_setups "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.child_setups")
  * [CABaseDelegatorSetup.clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.clear_cache")
  * [CABaseDelegatorSetup.creation_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.creation_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.creation_time")
  * [CABaseDelegatorSetup.deregister](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deregister "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.deregister")
  * [CABaseDelegatorSetup.disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.disable_caching")
  * [CABaseDelegatorSetup.disable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.disable_whitelist")
  * [CABaseDelegatorSetup.enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enable_caching")
  * [CABaseDelegatorSetup.enable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enable_whitelist")
  * [CABaseDelegatorSetup.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.fields")
  * [CABaseDelegatorSetup.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.fields_dict")
  * [CABaseDelegatorSetup.first_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.first_hit_time")
  * [CABaseDelegatorSetup.first_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.first_run_time")
  * [CABaseDelegatorSetup.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hash")
  * [CABaseDelegatorSetup.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hash_key")
  * [CABaseDelegatorSetup.hits](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hits")
  * [CABaseDelegatorSetup.last_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_hit_time")
  * [CABaseDelegatorSetup.last_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_run_time")
  * [CABaseDelegatorSetup.last_update_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.last_update_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_update_time")
  * [CABaseDelegatorSetup.metrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.metrics")
  * [CABaseDelegatorSetup.misses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.misses")
  * [CABaseDelegatorSetup.position_among_similar](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.position_among_similar "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.position_among_similar")
  * [CABaseDelegatorSetup.query](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.query "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.query")
  * [CABaseDelegatorSetup.readable_name](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_name "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.readable_name")
  * [CABaseDelegatorSetup.readable_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_str "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.readable_str")
  * [CABaseDelegatorSetup.registered](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registered "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.registered")
  * [CABaseDelegatorSetup.registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registry "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.registry")
  * [CABaseDelegatorSetup.same_type_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.same_type_setups "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.same_type_setups")
  * [CABaseDelegatorSetup.short_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.short_str "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.short_str")
  * [CABaseDelegatorSetup.total_elapsed](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_elapsed")
  * [CABaseDelegatorSetup.total_saved](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_saved")
  * [CABaseDelegatorSetup.total_size](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_size")
  * [CABaseDelegatorSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.use_cache")
  * [CABaseDelegatorSetup.use_cache_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache_lut "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.use_cache_lut")
  * [CABaseDelegatorSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.whitelist")
  * [CABaseDelegatorSetup.whitelist_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist_lut "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.whitelist_lut")
  * [CABaseSetup.activate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.activate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.activate")
  * [CABaseSetup.deactivate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deactivate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.deactivate")
  * [CABaseSetup.enforce_rules](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enforce_rules "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enforce_rules")
  * [CABaseSetup.get_stats](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.get_stats "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_stats")
  * [CABaseSetup.register](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.register "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.register")
  * [CASetupDelegatorMixin.delegate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.delegate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.delegate")
  * [CASetupDelegatorMixin.get_setup_hierarchy](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_setup_hierarchy "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_setup_hierarchy")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_hash")



* * *

### any_use_cache_lut field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1791-L1799 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.any_use_cache_lut "Permanent link")

Last time [CABaseSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseSetup.use_cache") was updated in this class or any of its superclasses.

* * *

### any_whitelist_lut field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1801-L1809 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.any_whitelist_lut "Permanent link")

Last time [CABaseSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.whitelist") was updated in this class or any of its superclasses.

* * *

### cls field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.cls "Permanent link")

Cacheable class.

* * *

### get class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1718-L1744 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-44-1)CAClassSetup.get(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-44-2)    cls_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-44-3)    registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-44-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-44-5))
    

Get setup from [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry") or register a new one.

`**kwargs` are passed to [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup").

* * *

### get_cacheable_subclasses static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1683-L1692 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_cacheable_subclasses "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-45-1)CAClassSetup.get_cacheable_subclasses(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-45-2)    cls
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-45-3))
    

Get an ordered list of the cacheable subclasses of a class.

* * *

### get_cacheable_superclasses static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1664-L1672 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_cacheable_superclasses "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-46-1)CAClassSetup.get_cacheable_superclasses(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-46-2)    cls
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-46-3))
    

Get an ordered list of the cacheable superclasses of a class.

* * *

### get_subclass_setups static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1694-L1701 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_subclass_setups "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-47-1)CAClassSetup.get_subclass_setups(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-47-2)    registry,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-47-3)    cls
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-47-4))
    

Setups of type [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup") of each in [CAClassSetup.get_cacheable_subclasses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_cacheable_subclasses "vectorbtpro.registries.ca_registry.CAClassSetup.get_cacheable_subclasses").

* * *

### get_superclass_setups static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1674-L1681 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_superclass_setups "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-48-1)CAClassSetup.get_superclass_setups(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-48-2)    registry,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-48-3)    cls
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-48-4))
    

Setups of type [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup") of each in [CAClassSetup.get_cacheable_superclasses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_cacheable_superclasses "vectorbtpro.registries.ca_registry.CAClassSetup.get_cacheable_superclasses").

* * *

### get_unbound_cacheables static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1703-L1707 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_unbound_cacheables "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-49-1)CAClassSetup.get_unbound_cacheables(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-49-2)    cls
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-49-3))
    

Get a set of the unbound cacheables of a class.

* * *

### get_unbound_setups static method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1709-L1716 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_unbound_setups "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-50-1)CAClassSetup.get_unbound_setups(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-50-2)    registry,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-50-3)    cls
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-50-4))
    

Setups of type [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup") of each in [CAClassSetup.get_unbound_cacheables](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_unbound_cacheables "vectorbtpro.registries.ca_registry.CAClassSetup.get_unbound_cacheables").

* * *

### instance_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1782-L1789 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.instance_setups "Permanent link")

Setups of type [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup") of instances of the class.

* * *

### subclass_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1772-L1775 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.subclass_setups "Permanent link")

See [CAClassSetup.get_subclass_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_subclass_setups "vectorbtpro.registries.ca_registry.CAClassSetup.get_subclass_setups").

* * *

### superclass_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1767-L1770 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.superclass_setups "Permanent link")

See [CAClassSetup.get_superclass_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_superclass_setups "vectorbtpro.registries.ca_registry.CAClassSetup.get_superclass_setups").

* * *

### unbound_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1777-L1780 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.unbound_setups "Permanent link")

See [CAClassSetup.get_unbound_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup.get_unbound_setups "vectorbtpro.registries.ca_registry.CAClassSetup.get_unbound_setups").

* * *

## CAInstanceSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1835-L1960 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-51-1)CAInstanceSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-51-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-51-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-51-4))
    

Class that represents a setup of an instance that has cacheables bound to it.

The provided instance must be of [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable").

Delegates cache management to its child setups of type [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup").

If `use_cash` or `whitelist` are None, inherits a non-empty value from its parent class setup.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CABaseDelegatorSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup")
  * [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")
  * [CASetupDelegatorMixin](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_messages")
  * [CABaseDelegatorSetup.active](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.active "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.active")
  * [CABaseDelegatorSetup.caching_enabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.caching_enabled")
  * [CABaseDelegatorSetup.child_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.child_setups "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.child_setups")
  * [CABaseDelegatorSetup.clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.clear_cache")
  * [CABaseDelegatorSetup.creation_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.creation_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.creation_time")
  * [CABaseDelegatorSetup.deregister](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deregister "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.deregister")
  * [CABaseDelegatorSetup.disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.disable_caching")
  * [CABaseDelegatorSetup.disable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.disable_whitelist")
  * [CABaseDelegatorSetup.enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enable_caching")
  * [CABaseDelegatorSetup.enable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enable_whitelist")
  * [CABaseDelegatorSetup.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.fields")
  * [CABaseDelegatorSetup.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.fields_dict")
  * [CABaseDelegatorSetup.first_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.first_hit_time")
  * [CABaseDelegatorSetup.first_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.first_run_time")
  * [CABaseDelegatorSetup.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hash")
  * [CABaseDelegatorSetup.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hash_key")
  * [CABaseDelegatorSetup.hits](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hits")
  * [CABaseDelegatorSetup.last_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_hit_time")
  * [CABaseDelegatorSetup.last_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_run_time")
  * [CABaseDelegatorSetup.last_update_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.last_update_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_update_time")
  * [CABaseDelegatorSetup.metrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.metrics")
  * [CABaseDelegatorSetup.misses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.misses")
  * [CABaseDelegatorSetup.position_among_similar](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.position_among_similar "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.position_among_similar")
  * [CABaseDelegatorSetup.query](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.query "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.query")
  * [CABaseDelegatorSetup.readable_name](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_name "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.readable_name")
  * [CABaseDelegatorSetup.readable_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_str "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.readable_str")
  * [CABaseDelegatorSetup.registered](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registered "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.registered")
  * [CABaseDelegatorSetup.registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registry "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.registry")
  * [CABaseDelegatorSetup.same_type_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.same_type_setups "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.same_type_setups")
  * [CABaseDelegatorSetup.short_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.short_str "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.short_str")
  * [CABaseDelegatorSetup.total_elapsed](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_elapsed")
  * [CABaseDelegatorSetup.total_saved](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_saved")
  * [CABaseDelegatorSetup.total_size](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_size")
  * [CABaseDelegatorSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.use_cache")
  * [CABaseDelegatorSetup.use_cache_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache_lut "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.use_cache_lut")
  * [CABaseDelegatorSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.whitelist")
  * [CABaseDelegatorSetup.whitelist_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist_lut "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.whitelist_lut")
  * [CABaseSetup.activate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.activate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.activate")
  * [CABaseSetup.deactivate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deactivate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.deactivate")
  * [CABaseSetup.enforce_rules](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enforce_rules "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enforce_rules")
  * [CABaseSetup.get_stats](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.get_stats "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_stats")
  * [CABaseSetup.register](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.register "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.register")
  * [CASetupDelegatorMixin.delegate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.delegate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.delegate")
  * [CASetupDelegatorMixin.get_setup_hierarchy](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_setup_hierarchy "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_setup_hierarchy")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_hash")



* * *

### class_setup field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1913-L1918 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup.class_setup "Permanent link")

Setup of type [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup") of the cacheable class of the instance.

* * *

### contains_garbage field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1908-L1911 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup.contains_garbage "Permanent link")

Whether instance was destroyed.

* * *

### get class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1852-L1878 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup.get "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-52-1)CAInstanceSetup.get(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-52-2)    instance,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-52-3)    registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-52-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-52-5))
    

Get setup from [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry") or register a new one.

`**kwargs` are passed to [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup").

* * *

### instance field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup.instance "Permanent link")

Cacheable instance.

* * *

### instance_obj field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1901-L1906 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup.instance_obj "Permanent link")

Instance object.

* * *

### run_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1927-L1936 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup.run_setups "Permanent link")

Setups of type [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup") of cacheables bound to the instance.

* * *

### unbound_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1920-L1925 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup.unbound_setups "Permanent link")

Setups of type [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup") of unbound cacheables declared in the class of the instance.

* * *

## CAMetrics class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1086-L1147 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-53-1)CAMetrics()
    

Abstract class that exposes various metrics related to caching.

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

  * [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup")
  * [CASetupDelegatorMixin](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin")



* * *

### first_hit_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1124-L1127 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "Permanent link")

Time of the first hit.

* * *

### first_run_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1114-L1117 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "Permanent link")

Time of the first run.

* * *

### hits class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1089-L1092 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "Permanent link")

Number of hits.

* * *

### last_hit_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1129-L1132 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "Permanent link")

Time of the last hit.

* * *

### last_run_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1119-L1122 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "Permanent link")

Time of the last run.

* * *

### metrics class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1134-L1147 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "Permanent link")

Dict with all metrics.

* * *

### misses class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1094-L1097 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "Permanent link")

Number of misses.

* * *

### total_elapsed class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1104-L1107 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "Permanent link")

Total number of seconds elapsed during running the function.

* * *

### total_saved class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1109-L1112 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "Permanent link")

Total number of seconds saved by using the cache.

* * *

### total_size class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1099-L1102 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "Permanent link")

Total size of cached objects.

* * *

## CAQuery class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L513-L751 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-54-1)CAQuery(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-54-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-54-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-54-4))
    

Data class that represents a query for matching and ranking setups.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.attr_.DefineMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.attr_.DefineMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.attr_.DefineMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.attr_.DefineMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.attr_.DefineMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.attr_.DefineMixin.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.attr_.DefineMixin.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing")
  * [DefineMixin.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.attr_.DefineMixin.fields")
  * [DefineMixin.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.attr_.DefineMixin.fields_dict")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.attr_.DefineMixin.get_field")
  * [DefineMixin.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.attr_.DefineMixin.hash")
  * [DefineMixin.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.attr_.DefineMixin.hash_key")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.attr_.DefineMixin.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.attr_.DefineMixin.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.attr_.DefineMixin.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.attr_.DefineMixin.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.attr_.DefineMixin.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.attr_.DefineMixin.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.attr_.DefineMixin.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### base_cls field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.base_cls "Permanent link")

Base class of the instance or its name (case-sensitive) [CAQuery.cacheable](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.cacheable "vectorbtpro.registries.ca_registry.CAQuery.cacheable") is bound to.

* * *

### cacheable field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.cacheable "Permanent link")

Cacheable object or its name (case-sensitive).

* * *

### cls field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.cls "Permanent link")

Class of the instance or its name (case-sensitive) [CAQuery.cacheable](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.cacheable "vectorbtpro.registries.ca_registry.CAQuery.cacheable") is bound to.

* * *

### instance field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.instance "Permanent link")

Weak reference to the instance [CAQuery.cacheable](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.cacheable "vectorbtpro.registries.ca_registry.CAQuery.cacheable") is bound to.

* * *

### instance_obj field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L600-L607 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.instance_obj "Permanent link")

Instance object.

* * *

### matches_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L609-L741 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.matches_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-55-1)CAQuery.matches_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-55-2)    setup
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-55-3))
    

Return whether the setup matches this query.

**Usage**

Let's evaluate various queries:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-1)>>> class A(vbt.Cacheable):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-2)...     @vbt.cached_method(my_option=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-3)...     def f(self):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-4)...         return None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-6)>>> class B(A):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-7)...     pass
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-9)>>> @vbt.cached(my_option=False)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-10)... def f():
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-11)...     return None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-13)>>> a = A()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-14)>>> b = B()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-16)>>> def match_query(query):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-17)...     matched = []
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-18)...     if query.matches_setup(A.f.get_ca_setup()):  # unbound method
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-19)...         matched.append('A.f')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-20)...     if query.matches_setup(A.get_ca_setup()):  # class
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-21)...         matched.append('A')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-22)...     if query.matches_setup(a.get_ca_setup()):  # instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-23)...         matched.append('a')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-24)...     if query.matches_setup(A.f.get_ca_setup(a)):  # instance method
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-25)...         matched.append('a.f')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-26)...     if query.matches_setup(B.f.get_ca_setup()):  # unbound method
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-27)...         matched.append('B.f')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-28)...     if query.matches_setup(B.get_ca_setup()):  # class
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-29)...         matched.append('B')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-30)...     if query.matches_setup(b.get_ca_setup()):  # instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-31)...         matched.append('b')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-32)...     if query.matches_setup(B.f.get_ca_setup(b)):  # instance method
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-33)...         matched.append('b.f')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-34)...     if query.matches_setup(f.get_ca_setup()):  # function
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-35)...         matched.append('f')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-36)...     return matched
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-37)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-38)>>> match_query(vbt.CAQuery())
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-39)['A.f', 'A', 'a', 'a.f', 'B.f', 'B', 'b', 'b.f', 'f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-40)>>> match_query(vbt.CAQuery(cacheable=A.f))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-41)['A.f', 'a.f', 'B.f', 'b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-42)>>> match_query(vbt.CAQuery(cacheable=B.f))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-43)['A.f', 'a.f', 'B.f', 'b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-44)>>> match_query(vbt.CAQuery(cls=A))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-45)['A', 'a', 'a.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-46)>>> match_query(vbt.CAQuery(cls=B))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-47)['B', 'b', 'b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-48)>>> match_query(vbt.CAQuery(cls=vbt.Regex('[A-B]')))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-49)['A', 'a', 'a.f', 'B', 'b', 'b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-50)>>> match_query(vbt.CAQuery(base_cls=A))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-51)['A', 'a', 'a.f', 'B', 'b', 'b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-52)>>> match_query(vbt.CAQuery(base_cls=B))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-53)['B', 'b', 'b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-54)>>> match_query(vbt.CAQuery(instance=a))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-55)['a', 'a.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-56)>>> match_query(vbt.CAQuery(instance=b))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-57)['b', 'b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-58)>>> match_query(vbt.CAQuery(instance=a, cacheable='f'))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-59)['a.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-60)>>> match_query(vbt.CAQuery(instance=b, cacheable='f'))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-61)['b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-62)>>> match_query(vbt.CAQuery(options=dict(my_option=True)))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-63)['A.f', 'a.f', 'B.f', 'b.f']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-64)>>> match_query(vbt.CAQuery(options=dict(my_option=False)))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-56-65)['f']
    

* * *

### options field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.options "Permanent link")

Options to match.

* * *

### parse class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L532-L598 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.parse "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-57-1)CAQuery.parse(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-57-2)    query_like,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-57-3)    use_base_cls=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-57-4))
    

Parse a query-like object.

Note

Not all attribute combinations can be safely parsed by this function. For example, you cannot combine cacheable together with options.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-1)>>> vbt.CAQuery.parse(lambda x: x)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-2)CAQuery(cacheable=<function <lambda> at 0x7fd4766c7730>, instance=None, cls=None, base_cls=None, options=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-4)>>> vbt.CAQuery.parse("a")
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-5)CAQuery(cacheable='a', instance=None, cls=None, base_cls=None, options=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-7)>>> vbt.CAQuery.parse("A.a")
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-8)CAQuery(cacheable='a', instance=None, cls=None, base_cls='A', options=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-10)>>> vbt.CAQuery.parse("A")
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-11)CAQuery(cacheable=None, instance=None, cls=None, base_cls='A', options=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-13)>>> vbt.CAQuery.parse("A", use_base_cls=False)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-14)CAQuery(cacheable=None, instance=None, cls='A', base_cls=None, options=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-16)>>> vbt.CAQuery.parse(vbt.Regex("[A-B]"))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-17)CAQuery(cacheable=None, instance=None, cls=None, base_cls=Regex(pattern='[A-B]', flags=0), options=None)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-18)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-19)>>> vbt.CAQuery.parse(dict(my_option=100))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-58-20)CAQuery(cacheable=None, instance=None, cls=None, base_cls=None, options={'my_option': 100})
    

* * *

## CAQueryDelegator class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2481-L2510 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQueryDelegator "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-59-1)CAQueryDelegator(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-59-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-59-3)    registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-59-4)    collapse=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-59-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-59-6))
    

Class that delegates any setups that match a query.

`*args`, `collapse`, and `**kwargs` are passed to [CacheableRegistry.match_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.match_setups "vectorbtpro.registries.ca_registry.CacheableRegistry.match_setups").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")
  * [CASetupDelegatorMixin](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.find_messages")
  * [CASetupDelegatorMixin.clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.clear_cache "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.clear_cache")
  * [CASetupDelegatorMixin.delegate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.delegate "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.delegate")
  * [CASetupDelegatorMixin.deregister](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.deregister "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.deregister")
  * [CASetupDelegatorMixin.disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.disable_caching "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.disable_caching")
  * [CASetupDelegatorMixin.disable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.disable_whitelist "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.disable_whitelist")
  * [CASetupDelegatorMixin.enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.enable_caching "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.enable_caching")
  * [CASetupDelegatorMixin.enable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.enable_whitelist "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.enable_whitelist")
  * [CASetupDelegatorMixin.first_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.first_hit_time")
  * [CASetupDelegatorMixin.first_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.first_run_time")
  * [CASetupDelegatorMixin.get_setup_hierarchy](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_setup_hierarchy "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_setup_hierarchy")
  * [CASetupDelegatorMixin.get_stats](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_stats "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_stats")
  * [CASetupDelegatorMixin.hits](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.hits")
  * [CASetupDelegatorMixin.last_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.last_hit_time")
  * [CASetupDelegatorMixin.last_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.last_run_time")
  * [CASetupDelegatorMixin.metrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.metrics")
  * [CASetupDelegatorMixin.misses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.misses")
  * [CASetupDelegatorMixin.total_elapsed](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.total_elapsed")
  * [CASetupDelegatorMixin.total_saved](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.total_saved")
  * [CASetupDelegatorMixin.total_size](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.total_size")



* * *

### args class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2492-L2495 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQueryDelegator.args "Permanent link")

Arguments.

* * *

### child_setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2507-L2510 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQueryDelegator.child_setups "Permanent link")

Get child setups by matching them using [CacheableRegistry.match_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.match_setups "vectorbtpro.registries.ca_registry.CacheableRegistry.match_setups").

* * *

### kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2497-L2500 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQueryDelegator.kwargs "Permanent link")

Keyword arguments.

* * *

### registry class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2502-L2505 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQueryDelegator.registry "Permanent link")

Registry of type [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry").

* * *

## CARule class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L754-L821 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-60-1)CARule(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-60-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-60-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-60-4))
    

Data class that represents a rule that should be enforced on setups that match a query.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.attr_.DefineMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.attr_.DefineMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.attr_.DefineMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.attr_.DefineMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.attr_.DefineMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.attr_.DefineMixin.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.attr_.DefineMixin.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing")
  * [DefineMixin.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.attr_.DefineMixin.fields")
  * [DefineMixin.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.attr_.DefineMixin.fields_dict")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.attr_.DefineMixin.get_field")
  * [DefineMixin.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.attr_.DefineMixin.hash")
  * [DefineMixin.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.attr_.DefineMixin.hash_key")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.attr_.DefineMixin.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.attr_.DefineMixin.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.attr_.DefineMixin.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.attr_.DefineMixin.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.attr_.DefineMixin.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.attr_.DefineMixin.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.attr_.DefineMixin.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### enforce method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L808-L811 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.enforce "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-61-1)CARule.enforce(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-61-2)    setup
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-61-3))
    

Run [CARule.enforce_func](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.enforce_func "vectorbtpro.registries.ca_registry.CARule.enforce_func") on the setup if it has been matched.

* * *

### enforce_func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.enforce_func "Permanent link")

Function to run on the setup if it has been matched.

* * *

### exclude field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.exclude "Permanent link")

One or multiple setups to exclude.

* * *

### filter_func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.filter_func "Permanent link")

Function to filter out a setup.

* * *

### kind field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.kind "Permanent link")

Kind of a setup to match.

* * *

### matches_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L773-L806 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.matches_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-62-1)CARule.matches_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-62-2)    setup
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-62-3))
    

Return whether the setup matches the rule.

* * *

### query field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.query "Permanent link")

[CAQuery](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery "vectorbtpro.registries.ca_registry.CAQuery") used in matching.

* * *

## CARunResult class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2068-L2130 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-63-1)CARunResult(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-63-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-63-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-63-4))
    

Class that represents a cached result of a run.

Note

Hashed solely by the hash of the arguments `args_hash`.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.attr_.DefineMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.attr_.DefineMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.attr_.DefineMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.attr_.DefineMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.attr_.DefineMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.attr_.DefineMixin.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.attr_.DefineMixin.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing")
  * [DefineMixin.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.attr_.DefineMixin.fields")
  * [DefineMixin.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.attr_.DefineMixin.fields_dict")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.attr_.DefineMixin.get_field")
  * [DefineMixin.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.attr_.DefineMixin.hash")
  * [DefineMixin.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.attr_.DefineMixin.hash_key")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.attr_.DefineMixin.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.attr_.DefineMixin.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.attr_.DefineMixin.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.attr_.DefineMixin.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.attr_.DefineMixin.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.attr_.DefineMixin.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.attr_.DefineMixin.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.attr_.DefineMixin.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### args_hash field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.args_hash "Permanent link")

Hash of the arguments.

* * *

### first_hit_time field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2109-L2112 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.first_hit_time "Permanent link")

Time of the first hit.

* * *

### hit method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2119-L2126 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.hit "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-64-1)CARunResult.hit()
    

Hit the result.

* * *

### hits field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2104-L2107 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.hits "Permanent link")

Number of hits.

* * *

### last_hit_time field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2114-L2117 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.last_hit_time "Permanent link")

Time of the last hit.

* * *

### result field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.result "Permanent link")

Result of the run.

* * *

### result_size field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2094-L2097 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.result_size "Permanent link")

Get size of the result in memory.

* * *

### run_time field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2099-L2102 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.run_time "Permanent link")

Time of the run.

* * *

### timer field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult.timer "Permanent link")

Timer used to measure the execution time.

* * *

## CARunSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2133-L2478 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-65-1)CARunSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-65-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-65-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-65-4))
    

Class that represents a runnable cacheable setup.

Takes care of running functions and caching the results using [CARunSetup.run](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.run "vectorbtpro.registries.ca_registry.CARunSetup.run").

Accepts as `cacheable` either [cacheable_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property "vectorbtpro.utils.decorators.cacheable_property"), [cacheable_method](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_method "vectorbtpro.utils.decorators.cacheable_method"), or [cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable "vectorbtpro.utils.decorators.cacheable").

Hashed by the callable and optionally the id of the instance its bound to. This way, it can be uniquely identified among all setups.

Note

Cacheable properties and methods must provide an instance.

Only one instance per each unique combination of `cacheable` and `instance` can exist at a time.

If `use_cash` or `whitelist` are None, inherits a non-empty value either from its parent instance setup or its parent unbound setup. If both setups have non-empty values, takes the one that has been updated more recently.

Note

Use [CARunSetup.get](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.get "vectorbtpro.registries.ca_registry.CARunSetup.get") class method instead of [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup") to create a setup. The class method first checks whether a setup with the same hash has already been registered, and if so, returns it. Otherwise, creates and registers a new one. Using [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup") will throw an error if there is a setup with the same hash.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.registries.ca_registry.CABaseSetup.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.registries.ca_registry.CABaseSetup.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.registries.ca_registry.CABaseSetup.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.registries.ca_registry.CABaseSetup.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.registries.ca_registry.CABaseSetup.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.registries.ca_registry.CABaseSetup.find_messages")
  * [CABaseSetup.activate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.activate "vectorbtpro.registries.ca_registry.CABaseSetup.activate")
  * [CABaseSetup.active](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.active "vectorbtpro.registries.ca_registry.CABaseSetup.active")
  * [CABaseSetup.caching_enabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled "vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled")
  * [CABaseSetup.clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache "vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache")
  * [CABaseSetup.creation_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.creation_time "vectorbtpro.registries.ca_registry.CABaseSetup.creation_time")
  * [CABaseSetup.deactivate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deactivate "vectorbtpro.registries.ca_registry.CABaseSetup.deactivate")
  * [CABaseSetup.deregister](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deregister "vectorbtpro.registries.ca_registry.CABaseSetup.deregister")
  * [CABaseSetup.disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching "vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching")
  * [CABaseSetup.disable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist")
  * [CABaseSetup.enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching "vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching")
  * [CABaseSetup.enable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist")
  * [CABaseSetup.enforce_rules](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enforce_rules "vectorbtpro.registries.ca_registry.CABaseSetup.enforce_rules")
  * [CABaseSetup.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.registries.ca_registry.CABaseSetup.fields")
  * [CABaseSetup.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.registries.ca_registry.CABaseSetup.fields_dict")
  * [CABaseSetup.first_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "vectorbtpro.registries.ca_registry.CABaseSetup.first_hit_time")
  * [CABaseSetup.first_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "vectorbtpro.registries.ca_registry.CABaseSetup.first_run_time")
  * [CABaseSetup.get_stats](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.get_stats "vectorbtpro.registries.ca_registry.CABaseSetup.get_stats")
  * [CABaseSetup.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.registries.ca_registry.CABaseSetup.hash")
  * [CABaseSetup.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.registries.ca_registry.CABaseSetup.hash_key")
  * [CABaseSetup.hits](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "vectorbtpro.registries.ca_registry.CABaseSetup.hits")
  * [CABaseSetup.last_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "vectorbtpro.registries.ca_registry.CABaseSetup.last_hit_time")
  * [CABaseSetup.last_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "vectorbtpro.registries.ca_registry.CABaseSetup.last_run_time")
  * [CABaseSetup.last_update_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.last_update_time "vectorbtpro.registries.ca_registry.CABaseSetup.last_update_time")
  * [CABaseSetup.metrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "vectorbtpro.registries.ca_registry.CABaseSetup.metrics")
  * [CABaseSetup.misses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "vectorbtpro.registries.ca_registry.CABaseSetup.misses")
  * [CABaseSetup.position_among_similar](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.position_among_similar "vectorbtpro.registries.ca_registry.CABaseSetup.position_among_similar")
  * [CABaseSetup.query](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.query "vectorbtpro.registries.ca_registry.CABaseSetup.query")
  * [CABaseSetup.readable_name](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_name "vectorbtpro.registries.ca_registry.CABaseSetup.readable_name")
  * [CABaseSetup.readable_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_str "vectorbtpro.registries.ca_registry.CABaseSetup.readable_str")
  * [CABaseSetup.register](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.register "vectorbtpro.registries.ca_registry.CABaseSetup.register")
  * [CABaseSetup.registered](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registered "vectorbtpro.registries.ca_registry.CABaseSetup.registered")
  * [CABaseSetup.registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registry "vectorbtpro.registries.ca_registry.CABaseSetup.registry")
  * [CABaseSetup.same_type_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.same_type_setups "vectorbtpro.registries.ca_registry.CABaseSetup.same_type_setups")
  * [CABaseSetup.short_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.short_str "vectorbtpro.registries.ca_registry.CABaseSetup.short_str")
  * [CABaseSetup.total_elapsed](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "vectorbtpro.registries.ca_registry.CABaseSetup.total_elapsed")
  * [CABaseSetup.total_saved](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "vectorbtpro.registries.ca_registry.CABaseSetup.total_saved")
  * [CABaseSetup.total_size](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "vectorbtpro.registries.ca_registry.CABaseSetup.total_size")
  * [CABaseSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseSetup.use_cache")
  * [CABaseSetup.use_cache_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache_lut "vectorbtpro.registries.ca_registry.CABaseSetup.use_cache_lut")
  * [CABaseSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.whitelist")
  * [CABaseSetup.whitelist_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist_lut "vectorbtpro.registries.ca_registry.CABaseSetup.whitelist_lut")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.registries.ca_registry.CABaseSetup.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.registries.ca_registry.CABaseSetup.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.registries.ca_registry.CABaseSetup.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.registries.ca_registry.CABaseSetup.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.registries.ca_registry.CABaseSetup.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.registries.ca_registry.CABaseSetup.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.registries.ca_registry.CABaseSetup.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.registries.ca_registry.CABaseSetup.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.registries.ca_registry.CABaseSetup.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.registries.ca_registry.CABaseSetup.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.registries.ca_registry.CABaseSetup.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.registries.ca_registry.CABaseSetup.get_hash")



* * *

### cache field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.cache "Permanent link")

Dict of cached [CARunResult](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult "vectorbtpro.registries.ca_registry.CARunResult") instances by their hash.

* * *

### cacheable field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.cacheable "Permanent link")

Cacheable object.

* * *

### contains_garbage field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2281-L2284 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.contains_garbage "Permanent link")

Whether instance was destroyed.

* * *

### get class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2179-L2206 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.get "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-66-1)CARunSetup.get(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-66-2)    cacheable,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-66-3)    instance=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-66-4)    registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-66-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-66-6))
    

Get setup from [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry") or register a new one.

`**kwargs` are passed to [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup").

* * *

### get_args_hash method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2370-L2392 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.get_args_hash "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-67-1)CARunSetup.get_args_hash(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-67-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-67-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-67-4))
    

Get the hash of the passed arguments.

[CARunSetup.ignore_args](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.ignore_args "vectorbtpro.registries.ca_registry.CARunSetup.ignore_args") gets extended with `ignore_args` under [caching](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.caching "vectorbtpro._settings.caching").

If no arguments were passed, hashes None.

* * *

### ignore_args field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.ignore_args "Permanent link")

Arguments to ignore when hashing.

* * *

### instance field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.instance "Permanent link")

Cacheable instance.

* * *

### instance_obj field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2274-L2279 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.instance_obj "Permanent link")

Instance object.

* * *

### instance_setup field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2286-L2291 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.instance_setup "Permanent link")

Setup of type [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup") of the instance this cacheable is bound to.

* * *

### max_size field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.max_size "Permanent link")

Maximum number of entries in [CARunSetup.cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.cache "vectorbtpro.registries.ca_registry.CARunSetup.cache").

* * *

### run method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2412-L2422 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.run "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-68-1)CARunSetup.run(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-68-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-68-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-68-4))
    

Run the setup and cache it depending on a range of conditions.

Runs [CARunSetup.run_func](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.run_func "vectorbtpro.registries.ca_registry.CARunSetup.run_func") if caching is disabled or arguments are not hashable, and [CARunSetup.run_func_and_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.run_func_and_cache "vectorbtpro.registries.ca_registry.CARunSetup.run_func_and_cache") otherwise.

* * *

### run_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2364-L2368 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.run_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-69-1)CARunSetup.run_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-69-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-69-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-69-4))
    

Run the setup's function without caching.

* * *

### run_func_and_cache method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2394-L2410 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.run_func_and_cache "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-70-1)CARunSetup.run_func_and_cache(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-70-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-70-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-70-4))
    

Run the setup's function and cache the result.

Hashes the arguments using [CARunSetup.get_args_hash](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.get_args_hash "vectorbtpro.registries.ca_registry.CARunSetup.get_args_hash"), runs the function using [CARunSetup.run_func](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.run_func "vectorbtpro.registries.ca_registry.CARunSetup.run_func"), wraps the result using [CARunResult](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult "vectorbtpro.registries.ca_registry.CARunResult"), and uses the hash as a key to store the instance of [CARunResult](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunResult "vectorbtpro.registries.ca_registry.CARunResult") into [CARunSetup.cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.cache "vectorbtpro.registries.ca_registry.CARunSetup.cache") for later retrieval.

* * *

### unbound_setup field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2293-L2296 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup.unbound_setup "Permanent link")

Setup of type [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup") of the unbound cacheable.

* * *

## CASetupDelegatorMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1408-L1596 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-71-1)CASetupDelegatorMixin()
    

Mixin class that delegates cache management to child setups.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.registries.ca_registry.CAMetrics.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.registries.ca_registry.CAMetrics.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.registries.ca_registry.CAMetrics.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.registries.ca_registry.CAMetrics.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.registries.ca_registry.CAMetrics.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.registries.ca_registry.CAMetrics.find_messages")
  * [CAMetrics.first_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time")
  * [CAMetrics.first_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "vectorbtpro.registries.ca_registry.CAMetrics.first_run_time")
  * [CAMetrics.hits](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "vectorbtpro.registries.ca_registry.CAMetrics.hits")
  * [CAMetrics.last_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time")
  * [CAMetrics.last_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "vectorbtpro.registries.ca_registry.CAMetrics.last_run_time")
  * [CAMetrics.metrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "vectorbtpro.registries.ca_registry.CAMetrics.metrics")
  * [CAMetrics.misses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "vectorbtpro.registries.ca_registry.CAMetrics.misses")
  * [CAMetrics.total_elapsed](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed")
  * [CAMetrics.total_saved](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "vectorbtpro.registries.ca_registry.CAMetrics.total_saved")
  * [CAMetrics.total_size](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "vectorbtpro.registries.ca_registry.CAMetrics.total_size")



**Subclasses**

  * [CABaseDelegatorSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup")
  * [CAQueryDelegator](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQueryDelegator "vectorbtpro.registries.ca_registry.CAQueryDelegator")



* * *

### child_setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1411-L1414 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.child_setups "Permanent link")

Child setups.

* * *

### clear_cache method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1475-L1477 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.clear_cache "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-72-1)CASetupDelegatorMixin.clear_cache(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-72-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-72-3))
    

Calls [CABaseSetup.clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache "vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache") on each child setup.

* * *

### delegate method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1432-L1453 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.delegate "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-73-1)CASetupDelegatorMixin.delegate(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-73-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-73-3)    exclude=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-73-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-73-5))
    

Delegate a function to all child setups.

`func` must take the setup and return nothing. If the setup is an instance of [CASetupDelegatorMixin](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin"), it must additionally accept `exclude`.

* * *

### deregister method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1455-L1457 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.deregister "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-74-1)CASetupDelegatorMixin.deregister(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-74-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-74-3))
    

Calls [CABaseSetup.deregister](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deregister "vectorbtpro.registries.ca_registry.CABaseSetup.deregister") on each child setup.

* * *

### disable_caching method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1471-L1473 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.disable_caching "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-75-1)CASetupDelegatorMixin.disable_caching(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-75-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-75-3))
    

Calls [CABaseSetup.disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching "vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching") on each child setup.

* * *

### disable_whitelist method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1463-L1465 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.disable_whitelist "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-76-1)CASetupDelegatorMixin.disable_whitelist(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-76-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-76-3))
    

Calls [CABaseSetup.disable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist") on each child setup.

* * *

### enable_caching method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1467-L1469 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.enable_caching "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-77-1)CASetupDelegatorMixin.enable_caching(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-77-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-77-3))
    

Calls [CABaseSetup.enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching "vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching") on each child setup.

* * *

### enable_whitelist method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1459-L1461 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.enable_whitelist "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-78-1)CASetupDelegatorMixin.enable_whitelist(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-78-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-78-3))
    

Calls [CABaseSetup.enable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist "vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist") on each child setup.

* * *

### get_setup_hierarchy method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1416-L1430 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_setup_hierarchy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-79-1)CASetupDelegatorMixin.get_setup_hierarchy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-79-2)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-79-3)    short_str=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-79-4))
    

Get the setup hierarchy by recursively traversing the child setups.

* * *

### get_stats method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1559-L1596 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_stats "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-80-1)CASetupDelegatorMixin.get_stats(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-80-2)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-80-3)    short_str=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-80-4)    index_by_hash=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-80-5)    filter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-80-6)    include=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-80-7)    exclude=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-80-8))
    

Get a DataFrame out of stats dicts of child setups.

* * *

## CAUnboundSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1966-L2062 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-81-1)CAUnboundSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-81-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-81-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-81-4))
    

Class that represents a setup of an unbound cacheable property or method.

An unbound callable is a callable that was declared in a class but is not bound to any instance (just yet).

Note

Unbound callables are just regular functions - they have no parent setups. Even though they are formally declared in a class, there is no easy way to get a reference to the class from the decorator itself. Thus, searching for child setups of a specific class won't return unbound setups.

Delegates cache management to its child setups of type [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup"). One unbound cacheable property or method can be bound to multiple instances, thus there is one-to-many relationship between [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup") and [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup") instances.

Hint

Use class attributes instead of instance attributes to access unbound callables.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [CABaseDelegatorSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup")
  * [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup")
  * [CAMetrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics "vectorbtpro.registries.ca_registry.CAMetrics")
  * [CASetupDelegatorMixin](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.find_messages")
  * [CABaseDelegatorSetup.active](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.active "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.active")
  * [CABaseDelegatorSetup.caching_enabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.caching_enabled "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.caching_enabled")
  * [CABaseDelegatorSetup.child_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.child_setups "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.child_setups")
  * [CABaseDelegatorSetup.clear_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.clear_cache "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.clear_cache")
  * [CABaseDelegatorSetup.creation_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.creation_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.creation_time")
  * [CABaseDelegatorSetup.deregister](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deregister "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.deregister")
  * [CABaseDelegatorSetup.disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_caching "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.disable_caching")
  * [CABaseDelegatorSetup.disable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.disable_whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.disable_whitelist")
  * [CABaseDelegatorSetup.enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_caching "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enable_caching")
  * [CABaseDelegatorSetup.enable_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enable_whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enable_whitelist")
  * [CABaseDelegatorSetup.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.fields")
  * [CABaseDelegatorSetup.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.fields_dict")
  * [CABaseDelegatorSetup.first_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_hit_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.first_hit_time")
  * [CABaseDelegatorSetup.first_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.first_run_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.first_run_time")
  * [CABaseDelegatorSetup.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hash")
  * [CABaseDelegatorSetup.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hash_key")
  * [CABaseDelegatorSetup.hits](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.hits "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.hits")
  * [CABaseDelegatorSetup.last_hit_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_hit_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_hit_time")
  * [CABaseDelegatorSetup.last_run_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.last_run_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_run_time")
  * [CABaseDelegatorSetup.last_update_time](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.last_update_time "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.last_update_time")
  * [CABaseDelegatorSetup.metrics](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.metrics "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.metrics")
  * [CABaseDelegatorSetup.misses](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.misses "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.misses")
  * [CABaseDelegatorSetup.position_among_similar](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.position_among_similar "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.position_among_similar")
  * [CABaseDelegatorSetup.query](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.query "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.query")
  * [CABaseDelegatorSetup.readable_name](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_name "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.readable_name")
  * [CABaseDelegatorSetup.readable_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.readable_str "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.readable_str")
  * [CABaseDelegatorSetup.registered](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registered "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.registered")
  * [CABaseDelegatorSetup.registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.registry "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.registry")
  * [CABaseDelegatorSetup.same_type_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.same_type_setups "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.same_type_setups")
  * [CABaseDelegatorSetup.short_str](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.short_str "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.short_str")
  * [CABaseDelegatorSetup.total_elapsed](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_elapsed "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_elapsed")
  * [CABaseDelegatorSetup.total_saved](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_saved "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_saved")
  * [CABaseDelegatorSetup.total_size](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAMetrics.total_size "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.total_size")
  * [CABaseDelegatorSetup.use_cache](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.use_cache")
  * [CABaseDelegatorSetup.use_cache_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.use_cache_lut "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.use_cache_lut")
  * [CABaseDelegatorSetup.whitelist](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.whitelist")
  * [CABaseDelegatorSetup.whitelist_lut](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.whitelist_lut "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.whitelist_lut")
  * [CABaseSetup.activate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.activate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.activate")
  * [CABaseSetup.deactivate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.deactivate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.deactivate")
  * [CABaseSetup.enforce_rules](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.enforce_rules "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.enforce_rules")
  * [CABaseSetup.get_stats](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.get_stats "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_stats")
  * [CABaseSetup.register](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup.register "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.register")
  * [CASetupDelegatorMixin.delegate](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.delegate "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.delegate")
  * [CASetupDelegatorMixin.get_setup_hierarchy](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.get_setup_hierarchy "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_setup_hierarchy")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.registries.ca_registry.CABaseDelegatorSetup.get_hash")



* * *

### cacheable field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup.cacheable "Permanent link")

Cacheable object.

* * *

### get class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L1993-L2019 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup.get "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-82-1)CAUnboundSetup.get(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-82-2)    cacheable,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-82-3)    registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-82-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-82-5))
    

Get setup from [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry") or register a new one.

`**kwargs` are passed to [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup").

* * *

### run_setups field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2031-L2038 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup.run_setups "Permanent link")

Setups of type [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup") of bound cacheables.

* * *

## CacheableRegistry class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L824-L1079 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-83-1)CacheableRegistry()
    

Class for registering setups of cacheables.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### class_setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L834-L837 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.class_setups "Permanent link")

Dict of registered [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup") instances by their hash.

* * *

### deregister_rule method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L917-L919 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.deregister_rule "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-84-1)CacheableRegistry.deregister_rule(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-84-2)    rule
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-84-3))
    

Deregister a rule of type [CARule](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule "vectorbtpro.registries.ca_registry.CARule").

* * *

### deregister_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L894-L911 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.deregister_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-85-1)CacheableRegistry.deregister_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-85-2)    setup
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-85-3))
    

Deregister a new setup of type [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup").

Removes the setup from its respective collection.

To also deregister its children, call the [CASetupDelegatorMixin.deregister](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.deregister "vectorbtpro.registries.ca_registry.CASetupDelegatorMixin.deregister") method.

* * *

### get_class_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L945-L947 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.get_class_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-86-1)CacheableRegistry.get_class_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-86-2)    cls
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-86-3))
    

Get a setup of type [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup") with this class or return None.

* * *

### get_instance_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L937-L943 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.get_instance_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-87-1)CacheableRegistry.get_instance_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-87-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-87-3))
    

Get a setup of type [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup") with this instance or return None.

* * *

### get_run_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L921-L931 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.get_run_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-88-1)CacheableRegistry.get_run_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-88-2)    cacheable,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-88-3)    instance=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-88-4))
    

Get a setup of type [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup") with this cacheable and instance, or return None.

* * *

### get_setup_by_hash method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L864-L874 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.get_setup_by_hash "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-89-1)CacheableRegistry.get_setup_by_hash(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-89-2)    hash_
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-89-3))
    

Get the setup by its hash.

* * *

### get_unbound_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L933-L935 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.get_unbound_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-90-1)CacheableRegistry.get_unbound_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-90-2)    cacheable
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-90-3))
    

Get a setup of type [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup") with this cacheable or return None.

* * *

### instance_setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L839-L842 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.instance_setups "Permanent link")

Dict of registered [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup") instances by their hash.

* * *

### match_setups method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L949-L1079 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.match_setups "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-91-1)CacheableRegistry.match_setups(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-91-2)    query_like=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-91-3)    collapse=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-91-4)    kind=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-91-5)    exclude=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-91-6)    exclude_children=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-91-7)    filter_func=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-91-8))
    

Match all setups registered in this registry against `query_like`.

`query_like` can be one or more query-like objects that will be parsed using [CAQuery.parse](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.parse "vectorbtpro.registries.ca_registry.CAQuery.parse").

Set `collapse` to True to remove child setups that belong to any matched parent setup.

`kind` can be one or multiple of the following:

  * 'class' to only return class setups (instances of [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup"))
  * 'instance' to only return instance setups (instances of [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup"))
  * 'unbound' to only return unbound setups (instances of [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup"))
  * 'runnable' to only return runnable setups (instances of [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup"))



Set `exclude` to one or multiple setups to exclude. To not exclude their children, set `exclude_children` to False.

Note

`exclude_children` is applied only when `collapse` is True.

`filter_func` can be used to filter out setups. For example, `lambda setup: setup.caching_enabled` includes only those setups that have caching enabled. It must take a setup and return a boolean of whether to include this setup in the final results.

* * *

### register_rule method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L913-L915 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.register_rule "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-92-1)CacheableRegistry.register_rule(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-92-2)    rule
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-92-3))
    

Register a new rule of type [CARule](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule "vectorbtpro.registries.ca_registry.CARule").

* * *

### register_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L880-L892 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.register_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-93-1)CacheableRegistry.register_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-93-2)    setup
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-93-3))
    

Register a new setup of type [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup").

* * *

### rules class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L859-L862 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.rules "Permanent link")

List of registered [CARule](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule "vectorbtpro.registries.ca_registry.CARule") instances.

* * *

### run_setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L849-L852 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.run_setups "Permanent link")

Dict of registered [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup") instances by their hash.

* * *

### setup_registered method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L876-L878 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.setup_registered "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-94-1)CacheableRegistry.setup_registered(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-94-2)    setup
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-94-3))
    

Return whether the setup is registered.

* * *

### setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L854-L857 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.setups "Permanent link")

Dict of registered [CABaseSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CABaseSetup "vectorbtpro.registries.ca_registry.CABaseSetup") instances by their hash.

* * *

### unbound_setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L844-L847 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry.unbound_setups "Permanent link")

Dict of registered [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup") instances by their hash.

* * *

## CachingDisabled class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2577-L2743 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-1)CachingDisabled(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-2)    query_like=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-3)    use_base_cls=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-4)    kind=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-5)    exclude=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-6)    filter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-7)    registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-8)    disable_whitelist=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-9)    disable_machinery=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-10)    clear_cache=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-11)    silence_warnings=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-95-12))
    

Context manager to disable caching.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### clear_cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2648-L2651 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.clear_cache "Permanent link")

Whether to clear global cache when entering or local cache when disabling caching.

* * *

### disable_machinery class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2643-L2646 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.disable_machinery "Permanent link")

Whether to disable machinery.

* * *

### disable_whitelist class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2638-L2641 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.disable_whitelist "Permanent link")

Whether to disable whitelist.

* * *

### exclude class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2623-L2626 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.exclude "Permanent link")

See [CARule.exclude](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.exclude "vectorbtpro.registries.ca_registry.CARule.exclude").

* * *

### filter_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2628-L2631 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.filter_func "Permanent link")

See [CARule.filter_func](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.filter_func "vectorbtpro.registries.ca_registry.CARule.filter_func").

* * *

### init_settings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2663-L2666 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.init_settings "Permanent link")

Initial caching settings.

* * *

### init_setup_settings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2668-L2671 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.init_setup_settings "Permanent link")

Initial setup settings.

* * *

### kind class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2618-L2621 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.kind "Permanent link")

See [CARule.kind](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.kind "vectorbtpro.registries.ca_registry.CARule.kind").

* * *

### query_like class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2608-L2611 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.query_like "Permanent link")

See [CAQuery.parse](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.parse "vectorbtpro.registries.ca_registry.CAQuery.parse").

* * *

### registry class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2633-L2636 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.registry "Permanent link")

Registry of type [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry").

* * *

### rule class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2658-L2661 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.rule "Permanent link")

Rule.

* * *

### silence_warnings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2653-L2656 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.silence_warnings "Permanent link")

Whether to silence warnings.

* * *

### use_base_cls class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2613-L2616 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled.use_base_cls "Permanent link")

See [CAQuery.parse](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.parse "vectorbtpro.registries.ca_registry.CAQuery.parse").

* * *

## CachingEnabled class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2764-L2930 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-1)CachingEnabled(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-2)    query_like=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-3)    use_base_cls=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-4)    kind=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-5)    exclude=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-6)    filter_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-7)    registry=<vectorbtpro.registries.ca_registry.CacheableRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-8)    enable_whitelist=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-9)    enable_machinery=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-10)    clear_cache=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-11)    silence_warnings=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#__codelineno-96-12))
    

Context manager to enable caching.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



* * *

### clear_cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2835-L2838 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.clear_cache "Permanent link")

Whether to clear global cache when exiting or local cache when disabling caching.

* * *

### enable_machinery class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2830-L2833 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.enable_machinery "Permanent link")

Whether to enable machinery.

* * *

### enable_whitelist class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2825-L2828 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.enable_whitelist "Permanent link")

Whether to enable whitelist.

* * *

### exclude class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2810-L2813 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.exclude "Permanent link")

See [CARule.exclude](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.exclude "vectorbtpro.registries.ca_registry.CARule.exclude").

* * *

### filter_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2815-L2818 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.filter_func "Permanent link")

See [CARule.filter_func](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.filter_func "vectorbtpro.registries.ca_registry.CARule.filter_func").

* * *

### init_settings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2850-L2853 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.init_settings "Permanent link")

Initial caching settings.

* * *

### init_setup_settings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2855-L2858 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.init_setup_settings "Permanent link")

Initial setup settings.

* * *

### kind class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2805-L2808 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.kind "Permanent link")

See [CARule.kind](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARule.kind "vectorbtpro.registries.ca_registry.CARule.kind").

* * *

### query_like class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2795-L2798 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.query_like "Permanent link")

See [CAQuery.parse](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.parse "vectorbtpro.registries.ca_registry.CAQuery.parse").

* * *

### registry class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2820-L2823 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.registry "Permanent link")

Registry of type [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry "vectorbtpro.registries.ca_registry.CacheableRegistry").

* * *

### rule class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2845-L2848 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.rule "Permanent link")

Rule.

* * *

### silence_warnings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2840-L2843 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.silence_warnings "Permanent link")

Whether to silence warnings.

* * *

### use_base_cls class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/ca_registry.py#L2800-L2803 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled.use_base_cls "Permanent link")

See [CAQuery.parse](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAQuery.parse "vectorbtpro.registries.ca_registry.CAQuery.parse").
