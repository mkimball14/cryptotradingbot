pbar_registry

#  pbar_registry module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry "Permanent link")

Global registry for progress bars.

* * *

## pbar_reg PBarRegistry[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.pbar_reg "Permanent link")

Default registry of type [PBarRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry "vectorbtpro.registries.pbar_registry.PBarRegistry").

* * *

## PBarRegistry class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L29-L140 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-0-1)PBarRegistry()
    

Class for registering [ProgressBar](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar "vectorbtpro.utils.pbar.ProgressBar") instances.

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

### clear_instances method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L138-L140 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.clear_instances "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-1-1)PBarRegistry.clear_instances()
    

Clear instances.

* * *

### deregister_instance method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L49-L52 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.deregister_instance "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-2-1)PBarRegistry.deregister_instance(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-2-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-2-3))
    

Deregister an instance.

* * *

### generate_bar_id class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L32-L35 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.generate_bar_id "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-3-1)PBarRegistry.generate_bar_id()
    

Generate a unique bar id.

* * *

### get_child_instances method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L129-L136 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.get_child_instances "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-4-1)PBarRegistry.get_child_instances(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-4-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-4-3))
    

Get child (active or pending) instances of an instance.

* * *

### get_first_pending_instance method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L74-L86 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.get_first_pending_instance "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-5-1)PBarRegistry.get_first_pending_instance()
    

Get the first pending instance.

* * *

### get_last_active_instance method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L63-L72 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.get_last_active_instance "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-6-1)PBarRegistry.get_last_active_instance()
    

Get the last active instance.

* * *

### get_parent_instance method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L119-L127 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.get_parent_instance "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-7-1)PBarRegistry.get_parent_instance(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-7-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-7-3))
    

Get the (active) parent instance of an instance.

* * *

### get_parent_instances method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L110-L117 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.get_parent_instances "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-8-1)PBarRegistry.get_parent_instances(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-8-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-8-3))
    

Get the (active) parent instances of an instance.

* * *

### get_pending_instance method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L88-L108 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.get_pending_instance "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-9-1)PBarRegistry.get_pending_instance(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-9-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-9-3))
    

Get the pending instance.

If the bar id is not None, searches for the same id in the dictionary.

* * *

### has_conflict method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L54-L61 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.has_conflict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-10-1)PBarRegistry.has_conflict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-10-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-10-3))
    

Return whether there is an (active) instance with the same bar id.

* * *

### instances class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L40-L43 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.instances "Permanent link")

Dict of registered instances by their bar id.

* * *

### register_instance method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/pbar_registry.py#L45-L47 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry.register_instance "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-11-1)PBarRegistry.register_instance(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-11-2)    instance
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#__codelineno-11-3))
    

Register an instance.
