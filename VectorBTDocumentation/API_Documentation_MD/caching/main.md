caching

#  caching module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/caching.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching "Permanent link")

Utilities for caching.

* * *

## clear_pycache function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/caching.py#L24-L31 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.clear_pycache "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#__codelineno-0-1)clear_pycache()
    

Clear **pycache** folders and .pyc files.

* * *

## Cacheable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/caching.py#L34-L61 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#__codelineno-1-1)Cacheable()
    

Class that contains cacheable properties and methods.

Required to register [cacheable_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property "vectorbtpro.utils.decorators.cacheable_property") and [cacheable_method](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_method "vectorbtpro.utils.decorators.cacheable_method").

See [vectorbtpro.registries.ca_registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/ "vectorbtpro.registries.ca_registry") for details on the caching procedure.

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

  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")



* * *

### get_ca_setup class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/caching.py#L53-L61 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#__codelineno-2-1)Cacheable.get_ca_setup()
    

Get instance setup of type [CAInstanceSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAInstanceSetup "vectorbtpro.registries.ca_registry.CAInstanceSetup") if the instance method was called and class setup of type [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup "vectorbtpro.registries.ca_registry.CAClassSetup") otherwise.
