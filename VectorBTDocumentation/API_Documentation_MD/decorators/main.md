decorators

#  decorators module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators "Permanent link")

Class and function decorators.

* * *

## cacheable function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L274-L332 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-0-1)cacheable(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-0-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-0-3)    use_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-0-4)    whitelist=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-0-5)    max_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-0-6)    ignore_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-0-7)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-0-8))
    

Cacheable function decorator.

See notes on [cacheable_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property "vectorbtpro.utils.decorators.cacheable_property").

Note

To decorate an instance method, use [cacheable_method](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_method "vectorbtpro.utils.decorators.cacheable_method").

* * *

## cacheable_method function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L389-L442 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_method "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-1-1)cacheable_method(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-1-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-1-3)    use_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-1-4)    whitelist=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-1-5)    max_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-1-6)    ignore_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-1-7)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-1-8))
    

Cacheable method decorator.

See notes on [cacheable_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property "vectorbtpro.utils.decorators.cacheable_property").

* * *

## cached function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L335-L340 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cached "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-2-1)cached(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-2-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-2-3)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-2-4))
    

[cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable "vectorbtpro.utils.decorators.cacheable") with `use_cache` set to True.

Note

To decorate an instance method, use [cached_method](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cached_method "vectorbtpro.utils.decorators.cached_method").

* * *

## cached_method function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L445-L447 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cached_method "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-3-1)cached_method(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-3-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-3-3)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-3-4))
    

[cacheable_method](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_method "vectorbtpro.utils.decorators.cacheable_method") with `use_cache` set to True.

* * *

## custom_function function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L238-L263 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_function "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-4-1)custom_function(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-4-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-4-3)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-4-4))
    

Custom function decorator.

* * *

## custom_method function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L354-L379 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_method "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-5-1)custom_method(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-5-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-5-3)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-5-4))
    

Custom method decorator.

* * *

## memoized_method function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L38-L53 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.memoized_method "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-6-1)memoized_method(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-6-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-6-3))
    

Dead-simple memoization decorator for methods.

* * *

## cacheable_property class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L163-L210 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-7-1)cacheable_property(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-7-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-7-3)    use_cache=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-7-4)    whitelist=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-7-5)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-7-6))
    

Extends [custom_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property "vectorbtpro.utils.decorators.custom_property") for cacheable properties.

Note

Assumes that the instance (provided as `self`) won't change. If calculation depends upon object attributes that can be changed, it won't notice the change.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `builtins.property`
  * [custom_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property "vectorbtpro.utils.decorators.custom_property")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.decorators.custom_property.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.decorators.custom_property.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.decorators.custom_property.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.decorators.custom_property.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.decorators.custom_property.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.decorators.custom_property.find_messages")
  * [custom_property.func](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.func "vectorbtpro.utils.decorators.custom_property.func")
  * [custom_property.name](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.name "vectorbtpro.utils.decorators.custom_property.name")
  * [custom_property.options](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.options "vectorbtpro.utils.decorators.custom_property.options")



**Subclasses**

  * [cached_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cached_property "vectorbtpro.utils.decorators.cached_property")



* * *

### get_ca_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L192-L202 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property.get_ca_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-8-1)cacheable_property.get_ca_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-8-2)    instance=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-8-3))
    

Get setup of type [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup "vectorbtpro.registries.ca_registry.CARunSetup") if instance is known, or [CAUnboundSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAUnboundSetup "vectorbtpro.registries.ca_registry.CAUnboundSetup") otherwise.

See [vectorbtpro.registries.ca_registry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/ "vectorbtpro.registries.ca_registry") for details on the caching procedure.

* * *

### init_use_cache class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L182-L185 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property.init_use_cache "Permanent link")

Initial value for `use_cache`.

* * *

### init_whitelist class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L187-L190 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property.init_whitelist "Permanent link")

Initial value for `whitelist`.

* * *

## cached_property class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L213-L217 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cached_property "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-9-1)cached_property(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-9-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-9-3)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-9-4))
    

[cacheable_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property "vectorbtpro.utils.decorators.cacheable_property") with `use_cache` set to True.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `builtins.property`
  * [cacheable_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property "vectorbtpro.utils.decorators.cacheable_property")
  * [custom_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property "vectorbtpro.utils.decorators.custom_property")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.decorators.cacheable_property.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.decorators.cacheable_property.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.decorators.cacheable_property.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.decorators.cacheable_property.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.decorators.cacheable_property.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.decorators.cacheable_property.find_messages")
  * [cacheable_property.func](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.func "vectorbtpro.utils.decorators.cacheable_property.func")
  * [cacheable_property.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property.get_ca_setup "vectorbtpro.utils.decorators.cacheable_property.get_ca_setup")
  * [cacheable_property.init_use_cache](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property.init_use_cache "vectorbtpro.utils.decorators.cacheable_property.init_use_cache")
  * [cacheable_property.init_whitelist](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property.init_whitelist "vectorbtpro.utils.decorators.cacheable_property.init_whitelist")
  * [cacheable_property.name](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.name "vectorbtpro.utils.decorators.cacheable_property.name")
  * [cacheable_property.options](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.options "vectorbtpro.utils.decorators.cacheable_property.options")



* * *

## class_property class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L56-L72 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.class_property "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-10-1)class_property(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-10-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-10-3))
    

Property that can be called on a class.

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

### func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L63-L66 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.class_property.func "Permanent link")

Wrapped function.

* * *

## custom_property class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L111-L160 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-11-1)custom_property(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-11-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-11-3)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-11-4))
    

Custom extensible property that stores function and options as attributes.

Note

[custom_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property "vectorbtpro.utils.decorators.custom_property") instances belong to classes, not class instances. Thus changing the property will do the same for each instance of the class where the property has been defined initially.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * `builtins.property`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.base.Base.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.base.Base.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.base.Base.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.base.Base.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.base.Base.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.base.Base.find_messages")



**Subclasses**

  * [cacheable_property](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable_property "vectorbtpro.utils.decorators.cacheable_property")



* * *

### func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L133-L136 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.func "Permanent link")

Wrapped function.

* * *

### name class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L138-L141 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.name "Permanent link")

Wrapped function name.

* * *

### options class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L143-L146 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.custom_property.options "Permanent link")

Options.

* * *

## hybrid_property class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L75-L94 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.hybrid_property "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-12-1)hybrid_property(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-12-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#__codelineno-12-3))
    

Property that binds `self` to a class if the function is called as class method, otherwise to an instance.

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

### func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/decorators.py#L83-L86 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.hybrid_property.func "Permanent link")

Wrapped function.
