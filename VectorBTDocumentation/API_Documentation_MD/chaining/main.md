chaining

#  chaining module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chaining.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining "Permanent link")

Utilities for chaining.

* * *

## Chainable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chaining.py#L24-L77 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-0-1)Chainable()
    

Class representing an object that can be chained.

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

### chain class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chaining.py#L63-L77 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-1-1)Chainable.chain(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-1-2)    tasks
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-1-3))
    

Chain multiple tasks with [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.chaining.Chainable.pipe").

* * *

### pipe class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chaining.py#L27-L61 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-2-1)Chainable.pipe(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-2-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-2-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-2-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#__codelineno-2-5))
    

Apply a chainable function that expects a [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable") instance.

Can be called as a class method, but then will pass only `*args` and `**kwargs`.

Argument `func` can be a function, a string denoting a (deep) attribute to be resolved with [deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.deep_getattr "vectorbtpro.utils.attr_.deep_getattr"), or a tuple where the first element is one of the above and the second element is a positional argument or keyword argument where to pass the instance. If not a tuple, passes the instance as the first positional argument. If a string and the target function is an instance method, won't pass the instance since it's already bound to this instance.
