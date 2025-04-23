jit_registry jitting

#  jit_registry module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry "Permanent link")

Global registry for jittables.

Jitting is a process of just-in-time compiling functions to make their execution faster. A jitter is a decorator that wraps a regular Python function and returns the decorated function. Depending upon a jitter, this decorated function has the same or at least a similar signature to the function that has been decorated. Jitters take various jitter-specific options to change the behavior of execution; that is, a single regular Python function can be decorated by multiple jitter instances (for example, one jitter for decorating a function with `numba.jit` and another jitter for doing the same with `parallel=True` flag).

In addition to jitters, vectorbt introduces the concept of tasks. One task can be executed by multiple jitter types (such as NumPy, Numba, and JAX). For example, one can create a task that converts price into returns and implements it using NumPy and Numba. Those implementations are registered by [JITRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry "vectorbtpro.registries.jit_registry.JITRegistry") as [JitableSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup "vectorbtpro.registries.jit_registry.JitableSetup") instances, are stored in [JITRegistry.jitable_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.jitable_setups "vectorbtpro.registries.jit_registry.JITRegistry.jitable_setups"), and can be uniquely identified by the task id and jitter type. Note that [JitableSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup "vectorbtpro.registries.jit_registry.JitableSetup") instances contain only information on how to decorate a function.

The decorated function itself and the jitter that has been used are registered as a [JittedSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JittedSetup "vectorbtpro.registries.jit_registry.JittedSetup") instance and stored in [JITRegistry.jitted_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.jitted_setups "vectorbtpro.registries.jit_registry.JITRegistry.jitted_setups"). It acts as a cache to quickly retrieve an already decorated function and to avoid recompilation.

Let's implement a task that takes a sum over an array using both NumPy and Numba:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-3)>>> @vbt.register_jitted(task_id_or_func='sum')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-4)... def sum_np(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-5)...     return a.sum()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-7)>>> @vbt.register_jitted(task_id_or_func='sum')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-8)... def sum_nb(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-9)...     out = 0.
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-10)...     for i in range(a.shape[0]):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-11)...         out += a[i]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-0-12)...     return out
    

We can see that two new jitable setups were registered:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-1-1)>>> vbt.jit_reg.jitable_setups['sum']
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-1-2){'np': JitableSetup(task_id='sum', jitter_id='np', py_func=<function sum_np at 0x7fea215b1e18>, jitter_kwargs={}, tags=None),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-1-3) 'nb': JitableSetup(task_id='sum', jitter_id='nb', py_func=<function sum_nb at 0x7fea273d41e0>, jitter_kwargs={}, tags=None)}
    

Moreover, two jitted setups were registered for our decorated functions:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-1)>>> from vectorbtpro.registries.jit_registry import JitableSetup
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-3)>>> hash_np = JitableSetup.get_hash('sum', 'np')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-4)>>> vbt.jit_reg.jitted_setups[hash_np]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-5){3527539: JittedSetup(jitter=<vectorbtpro.utils.jitting.NumPyJitter object at 0x7fea21506080>, jitted_func=<function sum_np at 0x7fea215b1e18>)}
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-7)>>> hash_nb = JitableSetup.get_hash('sum', 'nb')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-8)>>> vbt.jit_reg.jitted_setups[hash_nb]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-2-9){6326224984503844995: JittedSetup(jitter=<vectorbtpro.utils.jitting.NumbaJitter object at 0x7fea214d0ba8>, jitted_func=CPUDispatcher(<function sum_nb at 0x7fea273d41e0>))}
    

These setups contain decorated functions with the options passed during the registration. When we call [JITRegistry.resolve](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve "vectorbtpro.registries.jit_registry.JITRegistry.resolve") without any additional keyword arguments, [JITRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry "vectorbtpro.registries.jit_registry.JITRegistry") returns exactly these functions:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-3-1)>>> jitted_func = vbt.jit_reg.resolve('sum', jitter='nb')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-3-2)>>> jitted_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-3-3)CPUDispatcher(<function sum_nb at 0x7fea273d41e0>)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-3-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-3-5)>>> jitted_func.targetoptions
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-3-6){'nopython': True, 'nogil': True, 'parallel': False, 'boundscheck': False}
    

Once we pass any other option, the Python function will be redecorated, and another `JittedOption` instance will be registered:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-1)>>> jitted_func = vbt.jit_reg.resolve('sum', jitter='nb', nopython=False)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-2)>>> jitted_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-3)CPUDispatcher(<function sum_nb at 0x7fea273d41e0>)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-5)>>> jitted_func.targetoptions
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-6){'nopython': False, 'nogil': True, 'parallel': False, 'boundscheck': False}
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-8)>>> vbt.jit_reg.jitted_setups[hash_nb]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-9){6326224984503844995: JittedSetup(jitter=<vectorbtpro.utils.jitting.NumbaJitter object at 0x7fea214d0ba8>, jitted_func=CPUDispatcher(<function sum_nb at 0x7fea273d41e0>)),
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-4-10) -2979374923679407948: JittedSetup(jitter=<vectorbtpro.utils.jitting.NumbaJitter object at 0x7fea00bf94e0>, jitted_func=CPUDispatcher(<function sum_nb at 0x7fea273d41e0>))}
    

## Templates[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#templates "Permanent link")

Templates can be used to, based on the current context, dynamically select the jitter or keyword arguments for jitting. For example, let's pick the NumPy jitter over any other jitter if there are more than two of them for a given task:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-5-1)>>> vbt.jit_reg.resolve('sum', jitter=vbt.RepEval("'nb' if 'nb' in task_setups else None"))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-5-2)CPUDispatcher(<function sum_nb at 0x7fea273d41e0>)
    

## Disabling[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#disabling "Permanent link")

In the case we want to disable jitting, we can simply pass `disable=True` to [JITRegistry.resolve](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve "vectorbtpro.registries.jit_registry.JITRegistry.resolve"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-6-1)>>> py_func = vbt.jit_reg.resolve('sum', jitter='nb', disable=True)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-6-2)>>> py_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-6-3)<function __main__.sum_nb(a)>
    

We can also disable jitting globally:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-7-1)>>> vbt.settings.jitting['disable'] = True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-7-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-7-3)>>> vbt.jit_reg.resolve('sum', jitter='nb')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-7-4)<function __main__.sum_nb(a)>
    

Hint

If we don't plan to use any additional options and we have only one jitter registered per task, we can also disable resolution to increase performance.

Warning

Disabling jitting globally only applies to functions resolved using [JITRegistry.resolve](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve "vectorbtpro.registries.jit_registry.JITRegistry.resolve"). Any decorated function that is being called directly will be executed as usual.

## Jitted option[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#jitted-option "Permanent link")

Since most functions that call other jitted functions in vectorbt have a `jitted` argument, you can pass `jitted` as a dictionary with options, as a string denoting the jitter, or False to disable jitting (see [resolve_jitted_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitted_option "vectorbtpro.utils.jitting.resolve_jitted_option")):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-1)>>> def sum_arr(arr, jitted=None):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-2)...     func = vbt.jit_reg.resolve_option('sum', jitted)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-3)...     return func(arr)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-5)>>> arr = np.random.uniform(size=1000000)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-7)>>> %timeit sum_arr(arr, jitted='np')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-8)319 µs ± 3.35 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-10)>>> %timeit sum_arr(arr, jitted='nb')
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-11)1.09 ms ± 4.13 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-13)>>> %timeit sum_arr(arr, jitted=dict(jitter='nb', disable=True))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-8-14)133 ms ± 2.32 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    

Hint

A good rule of thumb is: whenever a caller function accepts a `jitted` argument, the jitted functions it calls are most probably resolved using [JITRegistry.resolve_option](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve_option "vectorbtpro.registries.jit_registry.JITRegistry.resolve_option").

## Changing options upon registration[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#changing-options-upon-registration "Permanent link")

Options are usually specified upon registration using [register_jitted](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.register_jitted "vectorbtpro.registries.jit_registry.register_jitted"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-1)>>> from numba import prange
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-3)>>> @vbt.register_jitted(parallel=True, tags={'can_parallel'})
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-4)... def sum_parallel_nb(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-5)...     out = np.empty(a.shape[1])
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-6)...     for col in prange(a.shape[1]):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-7)...         total = 0.
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-8)...         for i in range(a.shape[0]):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-9)...             total += a[i, col]
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-10)...         out[col] = total
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-11)...     return out
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-12)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-13)>>> sum_parallel_nb.targetoptions
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-9-14){'nopython': True, 'nogil': True, 'parallel': True, 'boundscheck': False}
    

But what if we wanted to change the registration options of vectorbt's own jitable functions, such as [diff_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/base/#vectorbtpro.generic.nb.base.diff_nb "vectorbtpro.generic.nb.base.diff_nb")? For example, let's disable caching for all Numba functions.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-10-1)>>> vbt.settings.jitting.jitters['nb']['override_options'] = dict(cache=False)
    

Since all functions have already been registered, the above statement has no effect:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-11-1)>>> vbt.jit_reg.jitable_setups['vectorbtpro.generic.nb.base.diff_nb']['nb'].jitter_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-11-2){'cache': True}
    

In order for them to be applied, we need to save the settings to a file and load them before all functions are imported:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-12-1)>>> vbt.settings.save('my_settings')
    

Let's restart the runtime and instruct vectorbt to load the file with settings before anything else:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-13-1)>>> import os
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-13-2)>>> os.environ['VBT_SETTINGS_PATH'] = "my_settings"
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-13-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-13-4)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-13-5)>>> vbt.jit_reg.jitable_setups['vectorbtpro.generic.nb.base.diff_nb']['nb'].jitter_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-13-6){'cache': False}
    

We can also change the registration options for some specific tasks, and even replace Python functions. For example, we can change the implementation in the deepest places of the core. Let's change the default `ddof` from 0 to 1 in [nanstd_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/base/#vectorbtpro.generic.nb.base.nanstd_1d_nb "vectorbtpro.generic.nb.base.nanstd_1d_nb") and disable caching with Numba:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-1)>>> vbt.nb.nanstd_1d_nb(np.array([1, 2, 3]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-2)0.816496580927726
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-4)>>> def new_nanstd_1d_nb(arr, ddof=1):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-5)...     return np.sqrt(vbt.nb.nanvar_1d_nb(arr, ddof=ddof))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-7)>>> vbt.settings.jitting.jitters['nb']['tasks']['vectorbtpro.generic.nb.base.nanstd_1d_nb'] = dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-8)...     replace_py_func=new_nanstd_1d_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-9)...     override_options=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-10)...         cache=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-11)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-12)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-13)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-14-14)>>> vbt.settings.save('my_settings')
    

After restarting the runtime:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-15-1)>>> import os
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-15-2)>>> os.environ['VBT_SETTINGS_PATH'] = "my_settings"
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-15-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-15-4)>>> vbt.nb.nanstd_1d_nb(np.array([1, 2, 3]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-15-5)1.0
    

Note

All of the above examples require saving the setting to a file, restarting the runtime, setting the path to the file to an environment variable, and only then importing vectorbtpro.

## Changing options upon resolution[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#changing-options-upon-resolution "Permanent link")

Another approach but without the need to restart the runtime is by changing the options upon resolution using [JITRegistry.resolve_option](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve_option "vectorbtpro.registries.jit_registry.JITRegistry.resolve_option"):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-1)>>> # On specific Numba function
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-2)>>> vbt.settings.jitting.jitters['nb']['tasks']['vectorbtpro.generic.nb.base.diff_nb'] = dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-3)...     resolve_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-4)...         nogil=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-5)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-7)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-8)>>> # disabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-9)>>> vbt.jit_reg.resolve('vectorbtpro.generic.nb.base.diff_nb', jitter='nb').targetoptions
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-10){'nopython': True, 'nogil': False, 'parallel': False, 'boundscheck': False}
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-11)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-12)>>> # still enabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-13)>>> vbt.jit_reg.resolve('sum', jitter='nb').targetoptions
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-14){'nopython': True, 'nogil': True, 'parallel': False, 'boundscheck': False}
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-15)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-16)>>> # On each Numba function
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-17)>>> vbt.settings.jitting.jitters['nb']['resolve_kwargs'] = dict(nogil=False)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-18)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-19)>>> # disabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-20)>>> vbt.jit_reg.resolve('vectorbtpro.generic.nb.base.diff_nb', jitter='nb').targetoptions
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-21){'nopython': True, 'nogil': False, 'parallel': False, 'boundscheck': False}
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-22)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-23)>>> # disabled
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-24)>>> vbt.jit_reg.resolve('sum', jitter='nb').targetoptions
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-16-25){'nopython': True, 'nogil': False, 'parallel': False, 'boundscheck': False}
    

## Building custom jitters[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#building-custom-jitters "Permanent link")

Let's build a custom jitter on top of [NumbaJitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter "vectorbtpro.utils.jitting.NumbaJitter") that converts any argument that contains a Pandas object to a 2-dimensional NumPy array prior to decoration:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-1)>>> from functools import wraps
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-2)>>> from vectorbtpro.utils.jitting import NumbaJitter
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-4)>>> class SafeNumbaJitter(NumbaJitter):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-5)...     def decorate(self, py_func, tags=None):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-6)...         if self.wrapping_disabled:
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-7)...             return py_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-8)...
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-9)...         @wraps(py_func)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-10)...         def wrapper(*args, **kwargs):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-11)...             new_args = ()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-12)...             for arg in args:
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-13)...                 if isinstance(arg, pd.Series):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-14)...                     arg = np.expand_dims(arg.values, 1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-15)...                 elif isinstance(arg, pd.DataFrame):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-16)...                     arg = arg.values
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-17)...                 new_args += (arg,)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-18)...             new_kwargs = dict()
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-19)...             for k, v in kwargs.items():
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-20)...                 if isinstance(v, pd.Series):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-21)...                     v = np.expand_dims(v.values, 1)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-22)...                 elif isinstance(v, pd.DataFrame):
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-23)...                     v = v.values
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-24)...                 new_kwargs[k] = v
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-25)...             return NumbaJitter.decorate(self, py_func, tags=tags)(*new_args, **new_kwargs)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-17-26)...         return wrapper
    

After we have defined our jitter class, we need to register it globally:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-18-1)>>> vbt.settings.jitting.jitters['safe_nb'] = dict(cls=SafeNumbaJitter)
    

Finally, we can execute any Numba function by specifying our new jitter:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-19-1)>>> func = vbt.jit_reg.resolve(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-19-2)...     task_id_or_func=vbt.generic.nb.diff_nb,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-19-3)...     jitter='safe_nb',
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-19-4)...     allow_new=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-19-5)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-19-6)>>> func(pd.DataFrame([[1, 2], [3, 4]]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-19-7)array([[nan, nan],
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-19-8)       [ 2.,  2.]])
    

Whereas executing the same func using the vanilla Numba jitter causes an error:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-20-1)>>> func = vbt.jit_reg.resolve(task_id_or_func=vbt.generic.nb.diff_nb)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-20-2)>>> func(pd.DataFrame([[1, 2], [3, 4]]))
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-20-3)Failed in nopython mode pipeline (step: nopython frontend)
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-20-4)non-precise type pyobject
    

Note

Make sure to pass a function as `task_id_or_func` if the jitted function hasn't been registered yet.

This jitter cannot be used for decorating Numba functions that should be called from other Numba functions since the convertion operation is done using Python.

* * *

## jit_reg JITRegistry[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.jit_reg "Permanent link")

Default registry of type [JITRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry "vectorbtpro.registries.jit_registry.JITRegistry").

* * *

## get_func_full_name function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L377-L379 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.get_func_full_name "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-21-1)get_func_full_name(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-21-2)    func
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-21-3))
    

Get full name of the func to be used as task id.

* * *

## register_jitted function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L719-L786 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.register_jitted "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-22-1)register_jitted(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-22-2)    py_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-22-3)    task_id_or_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-22-4)    registry=<vectorbtpro.registries.jit_registry.JITRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-22-5)    tags=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-22-6)    **options
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-22-7))
    

Decorate and register a jitable function using [JITRegistry.decorate_and_register](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.decorate_and_register "vectorbtpro.registries.jit_registry.JITRegistry.decorate_and_register").

If `task_id_or_func` is a callable, gets replaced by the callable's module name and function name. Additionally, the function name may contain a suffix pointing at the jitter (such as `_nb`).

Options are merged in the following order:

  * `jitters.{jitter_id}.options` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting")
  * `jitters.{jitter_id}.tasks.{task_id}.options` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting")
  * `options`
  * `jitters.{jitter_id}.override_options` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting")
  * `jitters.{jitter_id}.tasks.{task_id}.override_options` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting")



`py_func` can also be overridden using `jitters.your_jitter.tasks.your_task.replace_py_func` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting").

* * *

## JITRegistry class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L436-L712 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-23-1)JITRegistry()
    

Class for registering jitted functions.

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

### decorate_and_register method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L491-L509 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.decorate_and_register "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-24-1)JITRegistry.decorate_and_register(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-24-2)    task_id,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-24-3)    py_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-24-4)    jitter=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-24-5)    jitter_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-24-6)    tags=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-24-7))
    

Decorate a jitable function and register both jitable and jitted setups.

* * *

### jitable_setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L443-L446 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.jitable_setups "Permanent link")

Dict of registered [JitableSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup "vectorbtpro.registries.jit_registry.JitableSetup") instances by `task_id` and `jitter_id`.

* * *

### jitted_setups class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L448-L451 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.jitted_setups "Permanent link")

Nested dict of registered [JittedSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JittedSetup "vectorbtpro.registries.jit_registry.JittedSetup") instances by hash of their [JitableSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup "vectorbtpro.registries.jit_registry.JitableSetup") instance.

* * *

### match_jitable_setups method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L511-L528 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.match_jitable_setups "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-25-1)JITRegistry.match_jitable_setups(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-25-2)    expression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-25-3)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-25-4))
    

Match jitable setups against an expression with each setup being a context.

* * *

### match_jitted_setups method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L530-L547 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.match_jitted_setups "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-26-1)JITRegistry.match_jitted_setups(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-26-2)    jitable_setup,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-26-3)    expression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-26-4)    context=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-26-5))
    

Match jitted setups of a jitable setup against an expression with each setup a context.

* * *

### register_jitable_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L453-L473 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.register_jitable_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-27-1)JITRegistry.register_jitable_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-27-2)    task_id,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-27-3)    jitter_id,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-27-4)    py_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-27-5)    jitter_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-27-6)    tags=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-27-7))
    

Register a jitable setup.

* * *

### register_jitted_setup method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L475-L489 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.register_jitted_setup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-28-1)JITRegistry.register_jitted_setup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-28-2)    jitable_setup,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-28-3)    jitter,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-28-4)    jitted_func
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-28-5))
    

Register a jitted setup.

* * *

### resolve method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L549-L700 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-1)JITRegistry.resolve(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-2)    task_id_or_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-3)    jitter=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-4)    disable=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-5)    disable_resolution=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-6)    allow_new=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-7)    register_new=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-8)    return_missing_task=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-9)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-10)    tags=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-11)    **jitter_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-29-12))
    

Resolve jitted function for the given task id.

For details on the format of `task_id_or_func`, see [register_jitted](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.register_jitted "vectorbtpro.registries.jit_registry.register_jitted").

Jitter keyword arguments are merged in the following order:

  * `jitable_setup.jitter_kwargs`
  * `jitter.your_jitter.resolve_kwargs` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting")
  * `jitter.your_jitter.tasks.your_task.resolve_kwargs` in [jitting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.jitting "vectorbtpro._settings.jitting")
  * `jitter_kwargs`



Templates are substituted in `jitter`, `disable`, and `jitter_kwargs`.

Set `disable` to True to return the Python function without decoration. If `disable_resolution` is enabled globally, `task_id_or_func` is returned unchanged.

Note

`disable` is only being used by [JITRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry "vectorbtpro.registries.jit_registry.JITRegistry"), not [vectorbtpro.utils.jitting](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/ "vectorbtpro.utils.jitting").

Note

If there are more than one jitted setups registered for a single task id, make sure to provide a jitter.

If no jitted setup of type [JittedSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JittedSetup "vectorbtpro.registries.jit_registry.JittedSetup") was found and `allow_new` is True, decorates and returns the function supplied as `task_id_or_func` (otherwise throws an error).

Set `return_missing_task` to True to return `task_id_or_func` if it cannot be found in [JITRegistry.jitable_setups](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.jitable_setups "vectorbtpro.registries.jit_registry.JITRegistry.jitable_setups").

* * *

### resolve_option method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L702-L712 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve_option "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-30-1)JITRegistry.resolve_option(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-30-2)    task_id,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-30-3)    option,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-30-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-30-5))
    

Resolve `option` using [resolve_jitted_option](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitted_option "vectorbtpro.utils.jitting.resolve_jitted_option") and call [JITRegistry.resolve](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry.resolve "vectorbtpro.registries.jit_registry.JITRegistry.resolve").

* * *

## JitableSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L382-L410 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-31-1)JitableSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-31-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-31-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-31-4))
    

Class that represents a jitable setup.

Note

Hashed solely by `task_id` and `jitter_id`.

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

### jitter_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup.jitter_id "Permanent link")

Jitter id.

* * *

### jitter_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup.jitter_kwargs "Permanent link")

Keyword arguments passed to [resolve_jitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.resolve_jitter "vectorbtpro.utils.jitting.resolve_jitter").

* * *

### py_func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup.py_func "Permanent link")

Python function to be jitted.

* * *

### tags field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup.tags "Permanent link")

Set of tags.

* * *

### task_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JitableSetup.task_id "Permanent link")

Task id.

* * *

## JittedSetup class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py#L413-L433 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JittedSetup "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-32-1)JittedSetup(
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-32-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-32-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#__codelineno-32-4))
    

Class that represents a jitted setup.

Note

Hashed solely by sorted config of `jitter`. That is, two jitters with the same config will yield the same hash and the function won't be re-decorated.

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

### jitted_func field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JittedSetup.jitted_func "Permanent link")

Decorated function.

* * *

### jitter field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/registries/jit_registry.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JittedSetup.jitter "Permanent link")

Jitter that decorated the function.
