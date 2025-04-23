chunking

#  chunking module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking "Permanent link")

Utilities for chunking.

* * *

## chunked function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1820-L2164 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-0-1)chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-0-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-0-3)    chunker=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-0-4)    replace_chunker=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-0-5)    merge_to_execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-0-6)    prepend_chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-0-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-0-8))
    

Decorator that chunks the inputs of a function using [Chunker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker "vectorbtpro.utils.chunking.Chunker").

Returns a new function with the same signature as the passed one.

Each option can be modified in the `options` attribute of the wrapper function or directly passed as a keyword argument with a leading underscore.

Chunking can be disabled using `disable` argument. Additionally, the entire wrapping mechanism can be disabled by using the global setting `disable_wrapping` (=> returns the wrapped function).

Keyword arguments not listed in [Chunker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker "vectorbtpro.utils.chunking.Chunker") and `execute_kwargs` are merged into `execute_kwargs` if `merge_to_execute_kwargs` is True, otherwise, they are passed directly to [Chunker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker "vectorbtpro.utils.chunking.Chunker").

If a chunker instance is provided and `replace_chunker` is True, will create a new [Chunker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker "vectorbtpro.utils.chunking.Chunker") instance by replacing any arguments that are not None.

**Usage**

For testing purposes, let's divide the input array into 2 chunks and compute the mean in a sequential manner:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-3)>>> @vbt.chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-4)...     n_chunks=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-5)...     size=vbt.LenSizer(arg_query='a'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-6)...     arg_take_spec=dict(a=vbt.ChunkSlicer())
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-8)... def f(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-9)...     return np.mean(a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-11)>>> f(np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-1-12)[2.0, 7.0]
    

Same can be done using annotations:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-2-1)>>> @vbt.chunked(n_chunks=2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-2-2)... def f(a: vbt.LenSizer() | vbt.ChunkSlicer()):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-2-3)...     return np.mean(a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-2-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-2-5)>>> f(np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-2-6)[2.0, 7.0]
    

Sizer can be omitted most of the time:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-3-1)>>> @vbt.chunked(n_chunks=2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-3-2)... def f(a: vbt.ChunkSlicer()):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-3-3)...     return np.mean(a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-3-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-3-5)>>> f(np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-3-6)[2.0, 7.0]
    

Another way is by using specialized [Chunker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker "vectorbtpro.utils.chunking.Chunker") subclasses that depend on the type of the argument:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-4-1)>>> @vbt.chunked(n_chunks=2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-4-2)... def f(a: vbt.ChunkedArray()):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-4-3)...     return np.mean(a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-4-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-4-5)>>> f(np.arange(10))
    

Also, instead of specifying the chunk taking specification beforehand, it can be passed dynamically by wrapping each value to be chunked with [Chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked "vectorbtpro.utils.chunking.Chunked") or any of its subclasses:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-5-1)>>> @vbt.chunked(n_chunks=2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-5-2)... def f(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-5-3)...     return np.mean(a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-5-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-5-5)>>> f(vbt.ChunkedArray(np.arange(10)))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-5-6)[2.0, 7.0]
    

The [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked") function is a decorator that takes `f` and creates a function that splits passed arguments, runs each chunk using an engine, and optionally, merges the results. It has the same signature as the original function:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-6-1)>>> f
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-6-2)<function __main__.f(a)>
    

We can change any option at any time:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-1)>>> # Change the option directly on the function
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-2)>>> f.options.n_chunks = 3
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-4)>>> f(np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-5)[1.5, 5.0, 8.0]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-6)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-7)>>> # Pass a new option with a leading underscore
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-8)>>> f(np.arange(10), _n_chunks=4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-7-9)[1.0, 4.0, 6.5, 8.5]
    

When we run the wrapped function, it first generates a list of chunk metadata of type [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta"). Chunk metadata contains the chunk index that can be used to split any input:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-8-1)>>> list(vbt.iter_chunk_meta(n_chunks=2))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-8-2)[ChunkMeta(uuid='84d64eed-fbac-41e7-ad61-c917e809b3b8', idx=0, start=None, end=None, indices=None),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-8-3) ChunkMeta(uuid='577817c4-fdee-4ceb-ab38-dcd663d9ab11', idx=1, start=None, end=None, indices=None)]
    

Additionally, it may contain the start and end index of the space we want to split. The space can be defined by the length of an input array, for example. In our case:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-9-1)>>> list(vbt.iter_chunk_meta(n_chunks=2, size=10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-9-2)[ChunkMeta(uuid='c1593842-dc31-474c-a089-e47200baa2be', idx=0, start=0, end=5, indices=None),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-9-3) ChunkMeta(uuid='6d0265e7-1204-497f-bc2c-c7b7800ec57d', idx=1, start=5, end=10, indices=None)]
    

If we know the size of the space in advance, we can pass it as an integer constant. Otherwise, we need to tell [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked") to derive the size from the inputs dynamically by passing any subclass of [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer"). In the example above, we instruct the wrapped function to derive the size from the length of the input array `a`.

Once all chunks are generated, the wrapped function attempts to split inputs into chunks. The specification for this operation can be provided by the `arg_take_spec` argument, which in most cases is a dictionary of [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker") instances keyed by the input name. Here's an example of a complex specification:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-1)>>> arg_take_spec = dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-2)...     a=vbt.ChunkSelector(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-3)...     args=vbt.ArgsTaker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-4)...         None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-5)...         vbt.ChunkSelector()
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-6)...     ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-7)...     b=vbt.SequenceTaker([
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-8)...         None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-9)...         vbt.ChunkSelector()
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-10)...     ]),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-11)...     kwargs=vbt.KwargsTaker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-12)...         c=vbt.MappingTaker(dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-13)...             d=vbt.ChunkSelector(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-14)...             e=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-15)...         ))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-16)...     )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-17)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-18)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-19)>>> @vbt.chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-20)...     n_chunks=vbt.LenSizer(arg_query='a'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-21)...     arg_take_spec=arg_take_spec
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-22)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-23)... def f(a, *args, b=None, **kwargs):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-24)...     return a + sum(args) + sum(b) + sum(kwargs['c'].values())
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-25)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-26)>>> f([1, 2, 3], 10, [1, 2, 3], b=(100, [1, 2, 3]), c=dict(d=[1, 2, 3], e=1000))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-10-27)[1114, 1118, 1122]
    

After splitting all inputs into chunks, the wrapped function forwards them to the engine function. The engine argument can be either the name of a supported engine, or a callable. Once the engine has finished all tasks and returned a list of results, we can merge them back using `merge_func`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-1)>>> @vbt.chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-2)...     n_chunks=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-3)...     size=vbt.LenSizer(arg_query='a'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-4)...     arg_take_spec=dict(a=vbt.ChunkSlicer()),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-5)...     merge_func="concat"
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-7)... def f(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-8)...     return a
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-10)>>> f(np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-11-11)array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    

The same using annotations:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-12-1)>>> @vbt.chunked(n_chunks=2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-12-2)... def f(a: vbt.ChunkSlicer()) -> vbt.MergeFunc("concat"):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-12-3)...     return a
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-12-4)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-12-5)>>> f(np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-12-6)array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    

Instead of (or in addition to) specifying `arg_take_spec`, we can define our function with the first argument being `chunk_meta` to be able to split the arguments during the execution. The [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked") decorator will automatically recognize and replace it with the actual [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta") object:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-1)>>> @vbt.chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-2)...     n_chunks=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-3)...     size=vbt.LenSizer(arg_query='a'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-4)...     arg_take_spec=dict(a=None),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-5)...     merge_func="concat"
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-7)... def f(chunk_meta, a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-8)...     return a[chunk_meta.start:chunk_meta.end]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-10)>>> f(np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-13-11)array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    

This may be a good idea in multi-threading, but a bad idea in multi-processing.

The same can be accomplished by using templates (here we tell [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked") to not replace the first argument by setting `prepend_chunk_meta` to False):
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-1)>>> @vbt.chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-2)...     n_chunks=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-3)...     size=vbt.LenSizer(arg_query='a'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-4)...     arg_take_spec=dict(a=None),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-5)...     merge_func="concat",
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-6)...     prepend_chunk_meta=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-7)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-8)... def f(chunk_meta, a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-9)...     return a[chunk_meta.start:chunk_meta.end]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-10)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-11)>>> f(vbt.Rep('chunk_meta'), np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-14-12)array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    

Templates in arguments are substituted right before taking a chunk from them.

Keyword arguments to the engine can be provided using `execute_kwargs`:
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-1)>>> @vbt.chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-2)...     n_chunks=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-3)...     size=vbt.LenSizer(arg_query='a'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-4)...     arg_take_spec=dict(a=vbt.ChunkSlicer()),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-5)...     show_progress=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-6)... )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-7)... def f(a):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-8)...     return np.mean(a)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-9)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-10)>>> f(np.arange(10))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-11)100% |█████████████████████████████████| 2/2 [00:00<00:00, 81.11it/s]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-15-12)[2.0, 7.0]
    

* * *

## get_chunk_meta_key function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L358-L366 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.get_chunk_meta_key "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-16-1)get_chunk_meta_key(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-16-2)    chunk_meta
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-16-3))
    

Get key corresponding to chunk meta.

* * *

## iter_chunk_meta function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L284-L355 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-17-1)iter_chunk_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-17-2)    size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-17-3)    min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-17-4)    n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-17-5)    chunk_len=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-17-6))
    

Yield meta of each successive chunk from a sequence with a number of elements.

**Args**

**`size`** : `int`
    Size of the space to split.
**`min_size`** : `int`
    

Minimum size.

If `size` is lower than this number, returns a single chunk.

**`n_chunks`** : `int` or `str`
    

Number of chunks.

If "auto", becomes the number of cores.

**`chunk_len`** : `int` or `str`
    

Length of each chunk.

If "auto", becomes the number of cores.

If `size`, `n_chunks`, and `chunk_len` are None (after resolving them from settings), returns a single chunk. If only `n_chunks` and `chunk_len` are None, sets `n_chunks` to "auto".

* * *

## resolve_chunked function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L2208-L2221 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.resolve_chunked "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-18-1)resolve_chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-18-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-18-3)    option=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-18-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-18-5))
    

Decorate with [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked") based on an option.

* * *

## resolve_chunked_option function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L2170-L2196 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.resolve_chunked_option "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-19-1)resolve_chunked_option(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-19-2)    option=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-19-3))
    

Return keyword arguments for [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked").

`option` can be:

  * True: Chunk using default settings
  * None or False: Do not chunk
  * string: Use `option` as the name of an execution engine (see [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute "vectorbtpro.utils.execution.execute"))
  * dict: Use `option` as keyword arguments passed to [chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked "vectorbtpro.utils.chunking.chunked")



For defaults, see `option` in [chunking](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.chunking "vectorbtpro._settings.chunking").

* * *

## specialize_chunked_option function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L2199-L2205 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.specialize_chunked_option "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-20-1)specialize_chunked_option(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-20-2)    option=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-20-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-20-4))
    

Resolve `option` and merge it with `kwargs` if it's not None so the dict can be passed as an option to other functions.

* * *

## ArgChunkMeta class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L264-L268 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgChunkMeta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-21-1)ArgChunkMeta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-21-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-21-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-21-4))
    

Class for generating chunk metadata from an argument.

**Superclasses**

  * [ArgGetter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "vectorbtpro.utils.chunking.ArgGetter")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkMetaGenerator](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator "vectorbtpro.utils.chunking.ChunkMetaGenerator")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [ArgGetter.arg_query](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.arg_query "vectorbtpro.utils.chunking.ArgGetter.arg_query")
  * [ArgGetter.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ArgGetter.fields")
  * [ArgGetter.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ArgGetter.fields_dict")
  * [ArgGetter.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.get_arg "vectorbtpro.utils.chunking.ArgGetter.get_arg")
  * [ArgGetter.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ArgGetter.hash")
  * [ArgGetter.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ArgGetter.hash_key")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ChunkMetaGenerator.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ChunkMetaGenerator.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ChunkMetaGenerator.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ChunkMetaGenerator.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ChunkMetaGenerator.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ChunkMetaGenerator.find_messages")
  * [ChunkMetaGenerator.get_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator.get_chunk_meta "vectorbtpro.utils.chunking.ChunkMetaGenerator.get_chunk_meta")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ArgGetter.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ArgGetter.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ArgGetter.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ArgGetter.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ArgGetter.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ArgGetter.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ArgGetter.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ArgGetter.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ArgGetter.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ArgGetter.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ArgGetter.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ArgGetter.get_hash")



**Subclasses**

  * [LenChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.LenChunkMeta "vectorbtpro.utils.chunking.LenChunkMeta")



* * *

## ArgGetter class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L75-L86 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-22-1)ArgGetter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-22-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-22-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-22-4))
    

Class for getting an argument from annotated arguments.

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



**Subclasses**

  * [ArgChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgChunkMeta "vectorbtpro.utils.chunking.ArgChunkMeta")
  * [ArgSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer "vectorbtpro.utils.chunking.ArgSizer")
  * [GroupIdxsMapper](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupIdxsMapper "vectorbtpro.base.chunking.GroupIdxsMapper")
  * [GroupLensMapper](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupLensMapper "vectorbtpro.base.chunking.GroupLensMapper")



* * *

### arg_query field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.arg_query "Permanent link")

Query for annotated argument to derive the size from.

* * *

### get_arg method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L82-L86 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.get_arg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-23-1)ArgGetter.get_arg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-23-2)    ann_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-23-3))
    

Get argument using [match_ann_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.match_ann_arg "vectorbtpro.utils.parsing.match_ann_arg").

* * *

## ArgSizer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L126-L141 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-24-1)ArgSizer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-24-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-24-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-24-4))
    

Class for getting the size from an argument.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [ArgGetter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "vectorbtpro.utils.chunking.ArgGetter")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer")



**Inherited members**

  * [ArgGetter.arg_query](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.arg_query "vectorbtpro.utils.chunking.ArgGetter.arg_query")
  * [ArgGetter.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ArgGetter.fields")
  * [ArgGetter.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ArgGetter.fields_dict")
  * [ArgGetter.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.get_arg "vectorbtpro.utils.chunking.ArgGetter.get_arg")
  * [ArgGetter.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ArgGetter.hash")
  * [ArgGetter.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ArgGetter.hash_key")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.Sizer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.Sizer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.Sizer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.Sizer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.Sizer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.Sizer.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ArgGetter.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ArgGetter.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ArgGetter.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ArgGetter.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ArgGetter.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ArgGetter.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ArgGetter.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ArgGetter.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ArgGetter.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ArgGetter.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ArgGetter.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.Sizer.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ArgGetter.get_hash")
  * [Sizer.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.apply "vectorbtpro.utils.chunking.Sizer.apply")
  * [Sizer.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.eval_id "vectorbtpro.utils.chunking.Sizer.eval_id")
  * [Sizer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.get_size "vectorbtpro.utils.chunking.Sizer.get_size")



**Subclasses**

  * [CountSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.CountSizer "vectorbtpro.utils.chunking.CountSizer")
  * [GroupLensSizer](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupLensSizer "vectorbtpro.base.chunking.GroupLensSizer")
  * [LenSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.LenSizer "vectorbtpro.utils.chunking.LenSizer")
  * [ShapeSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSizer "vectorbtpro.utils.chunking.ShapeSizer")



* * *

### single_type field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer.single_type "Permanent link")

One or multiple types to consider as a single value.

* * *

## ArgsTaker class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L849-L865 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgsTaker "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-25-1)ArgsTaker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-25-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-25-3)    single_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-25-4)    ignore_none=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-25-5)    mapper=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-25-6))
    

Class for taking from a variable arguments container.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [ContainerTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker "vectorbtpro.utils.chunking.ContainerTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [SequenceTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.SequenceTaker "vectorbtpro.utils.chunking.SequenceTaker")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.SequenceTaker.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.SequenceTaker.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.SequenceTaker.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.SequenceTaker.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.SequenceTaker.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.SequenceTaker.find_messages")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.SequenceTaker.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.SequenceTaker.should_take")
  * [ContainerTaker.check_cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.check_cont_take_spec "vectorbtpro.utils.chunking.SequenceTaker.check_cont_take_spec")
  * [ContainerTaker.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.SequenceTaker.get_size")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.SequenceTaker.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.SequenceTaker.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.SequenceTaker.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.SequenceTaker.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.SequenceTaker.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.SequenceTaker.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.SequenceTaker.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.SequenceTaker.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.SequenceTaker.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.SequenceTaker.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.SequenceTaker.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.SequenceTaker.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.SequenceTaker.get_hash")
  * [SequenceTaker.adapt_cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.SequenceTaker.adapt_cont_take_spec "vectorbtpro.utils.chunking.SequenceTaker.adapt_cont_take_spec")
  * [SequenceTaker.cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec "vectorbtpro.utils.chunking.SequenceTaker.cont_take_spec")
  * [SequenceTaker.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.SequenceTaker.eval_id")
  * [SequenceTaker.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.SequenceTaker.fields")
  * [SequenceTaker.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.SequenceTaker.fields_dict")
  * [SequenceTaker.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.SequenceTaker.hash")
  * [SequenceTaker.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.SequenceTaker.hash_key")
  * [SequenceTaker.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.SequenceTaker.ignore_none")
  * [SequenceTaker.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.SequenceTaker.mapper")
  * [SequenceTaker.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.SequenceTaker.single_type")
  * [SequenceTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.SequenceTaker.suggest_size")
  * [SequenceTaker.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.SequenceTaker.take")



* * *

## ArraySelector class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L582-L612 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArraySelector "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-26-1)ArraySelector(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-26-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-26-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-26-4))
    

Class for selecting one element from an array's axis based on the chunk index.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [AxisSpecifier](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier "vectorbtpro.utils.chunking.AxisSpecifier")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSelector "vectorbtpro.utils.chunking.ChunkSelector")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [DimRetainer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer "vectorbtpro.utils.chunking.DimRetainer")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [ShapeSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSelector "vectorbtpro.utils.chunking.ShapeSelector")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ShapeSelector.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ShapeSelector.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ShapeSelector.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ShapeSelector.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ShapeSelector.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ShapeSelector.find_messages")
  * [ChunkSelector.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ShapeSelector.suggest_size")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ShapeSelector.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ShapeSelector.should_take")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ShapeSelector.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ShapeSelector.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ShapeSelector.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ShapeSelector.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ShapeSelector.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ShapeSelector.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ShapeSelector.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ShapeSelector.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ShapeSelector.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ShapeSelector.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ShapeSelector.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ShapeSelector.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ShapeSelector.get_hash")
  * [ShapeSelector.axis](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier.axis "vectorbtpro.utils.chunking.ShapeSelector.axis")
  * [ShapeSelector.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ShapeSelector.eval_id")
  * [ShapeSelector.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ShapeSelector.fields")
  * [ShapeSelector.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ShapeSelector.fields_dict")
  * [ShapeSelector.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ShapeSelector.get_size")
  * [ShapeSelector.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ShapeSelector.hash")
  * [ShapeSelector.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ShapeSelector.hash_key")
  * [ShapeSelector.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ShapeSelector.ignore_none")
  * [ShapeSelector.keep_dims](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer.keep_dims "vectorbtpro.utils.chunking.ShapeSelector.keep_dims")
  * [ShapeSelector.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ShapeSelector.mapper")
  * [ShapeSelector.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ShapeSelector.single_type")
  * [ShapeSelector.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ShapeSelector.take")



**Subclasses**

  * [FlexArraySelector](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.FlexArraySelector "vectorbtpro.base.chunking.FlexArraySelector")



* * *

## ArraySizer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L200-L226 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArraySizer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-27-1)ArraySizer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-27-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-27-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-27-4))
    

Class for getting the size from the length of an axis in an array.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [ArgGetter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "vectorbtpro.utils.chunking.ArgGetter")
  * [ArgSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer "vectorbtpro.utils.chunking.ArgSizer")
  * [AxisSpecifier](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier "vectorbtpro.utils.chunking.AxisSpecifier")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [ShapeSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSizer "vectorbtpro.utils.chunking.ShapeSizer")
  * [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer")



**Inherited members**

  * [ArgGetter.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.get_arg "vectorbtpro.utils.chunking.ShapeSizer.get_arg")
  * [ArgSizer.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.apply "vectorbtpro.utils.chunking.ShapeSizer.apply")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ShapeSizer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ShapeSizer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ShapeSizer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ShapeSizer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ShapeSizer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ShapeSizer.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ShapeSizer.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ShapeSizer.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ShapeSizer.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ShapeSizer.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ShapeSizer.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ShapeSizer.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ShapeSizer.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ShapeSizer.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ShapeSizer.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ShapeSizer.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ShapeSizer.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ShapeSizer.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ShapeSizer.get_hash")
  * [ShapeSizer.arg_query](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.arg_query "vectorbtpro.utils.chunking.ShapeSizer.arg_query")
  * [ShapeSizer.axis](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier.axis "vectorbtpro.utils.chunking.ShapeSizer.axis")
  * [ShapeSizer.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.eval_id "vectorbtpro.utils.chunking.ShapeSizer.eval_id")
  * [ShapeSizer.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ShapeSizer.fields")
  * [ShapeSizer.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ShapeSizer.fields_dict")
  * [ShapeSizer.get_obj_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSizer.get_obj_size "vectorbtpro.utils.chunking.ShapeSizer.get_obj_size")
  * [ShapeSizer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.get_size "vectorbtpro.utils.chunking.ShapeSizer.get_size")
  * [ShapeSizer.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ShapeSizer.hash")
  * [ShapeSizer.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ShapeSizer.hash_key")
  * [ShapeSizer.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer.single_type "vectorbtpro.utils.chunking.ShapeSizer.single_type")



**Subclasses**

  * [FlexArraySizer](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.FlexArraySizer "vectorbtpro.base.chunking.FlexArraySizer")



* * *

## ArraySlicer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L615-L645 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArraySlicer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-28-1)ArraySlicer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-28-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-28-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-28-4))
    

Class for slicing multiple elements from an array's axis based on the chunk range.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [AxisSpecifier](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier "vectorbtpro.utils.chunking.AxisSpecifier")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkSlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSlicer "vectorbtpro.utils.chunking.ChunkSlicer")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [ShapeSlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSlicer "vectorbtpro.utils.chunking.ShapeSlicer")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ShapeSlicer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ShapeSlicer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ShapeSlicer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ShapeSlicer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ShapeSlicer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ShapeSlicer.find_messages")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ShapeSlicer.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ShapeSlicer.should_take")
  * [ChunkTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ShapeSlicer.suggest_size")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ShapeSlicer.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ShapeSlicer.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ShapeSlicer.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ShapeSlicer.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ShapeSlicer.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ShapeSlicer.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ShapeSlicer.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ShapeSlicer.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ShapeSlicer.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ShapeSlicer.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ShapeSlicer.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ShapeSlicer.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ShapeSlicer.get_hash")
  * [ShapeSlicer.axis](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier.axis "vectorbtpro.utils.chunking.ShapeSlicer.axis")
  * [ShapeSlicer.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ShapeSlicer.eval_id")
  * [ShapeSlicer.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ShapeSlicer.fields")
  * [ShapeSlicer.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ShapeSlicer.fields_dict")
  * [ShapeSlicer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ShapeSlicer.get_size")
  * [ShapeSlicer.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ShapeSlicer.hash")
  * [ShapeSlicer.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ShapeSlicer.hash_key")
  * [ShapeSlicer.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ShapeSlicer.ignore_none")
  * [ShapeSlicer.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ShapeSlicer.mapper")
  * [ShapeSlicer.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ShapeSlicer.single_type")
  * [ShapeSlicer.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ShapeSlicer.take")



**Subclasses**

  * [FlexArraySlicer](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.FlexArraySlicer "vectorbtpro.base.chunking.FlexArraySlicer")



* * *

## AxisSpecifier class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L89-L94 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-29-1)AxisSpecifier(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-29-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-29-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-29-4))
    

Class with an attribute for specifying an axis.

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



**Subclasses**

  * [ShapeSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSelector "vectorbtpro.utils.chunking.ShapeSelector")
  * [ShapeSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSizer "vectorbtpro.utils.chunking.ShapeSizer")
  * [ShapeSlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSlicer "vectorbtpro.utils.chunking.ShapeSlicer")



* * *

### axis field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier.axis "Permanent link")

Axis of the argument to take from.

* * *

## ChunkMapper class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L372-L403 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-30-1)ChunkMapper(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-30-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-30-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-30-4))
    

Abstract class for mapping chunk metadata.

Implements the abstract [ChunkMapper.map](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper.map "vectorbtpro.utils.chunking.ChunkMapper.map") method.

Supports caching of each pair of incoming and outgoing [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta") instances.

Note

Use [ChunkMapper.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper.apply "vectorbtpro.utils.chunking.ChunkMapper.apply") instead of [ChunkMapper.map](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper.map "vectorbtpro.utils.chunking.ChunkMapper.map").

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



**Subclasses**

  * [GroupIdxsMapper](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupIdxsMapper "vectorbtpro.base.chunking.GroupIdxsMapper")
  * [GroupLensMapper](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupLensMapper "vectorbtpro.base.chunking.GroupLensMapper")



* * *

### apply method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L389-L397 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper.apply "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-31-1)ChunkMapper.apply(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-31-2)    chunk_meta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-31-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-31-4))
    

Apply the mapper.

* * *

### chunk_meta_cache field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper.chunk_meta_cache "Permanent link")

Cache for outgoing [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta") instances keyed by UUID of the incoming ones.

* * *

### map method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L399-L403 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper.map "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-32-1)ChunkMapper.map(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-32-2)    chunk_meta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-32-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-32-4))
    

Abstract method for mapping chunk metadata.

Takes the chunk metadata of type [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta") and returns a new chunk metadata of the same type.

* * *

### should_cache field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper.should_cache "Permanent link")

Whether should cache.

* * *

## ChunkMeta class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L232-L253 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-33-1)ChunkMeta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-33-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-33-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-33-4))
    

Class that represents a chunk metadata.

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

### end field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta.end "Permanent link")

End of the chunk range (excluding). Can be None.

* * *

### idx field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta.idx "Permanent link")

Chunk index.

* * *

### indices field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta.indices "Permanent link")

Indices included in the chunk range. Can be None.

Has priority over [ChunkMeta.start](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta.start "vectorbtpro.utils.chunking.ChunkMeta.start") and [ChunkMeta.end](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta.end "vectorbtpro.utils.chunking.ChunkMeta.end").

* * *

### start field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta.start "Permanent link")

Start of the chunk range (including). Can be None.

* * *

### uuid field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta.uuid "Permanent link")

Unique identifier of the chunk.

Used for caching.

* * *

## ChunkMetaGenerator class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L256-L261 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-34-1)ChunkMetaGenerator()
    

Abstract class for generating chunk metadata from annotated arguments.

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

  * [ArgChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgChunkMeta "vectorbtpro.utils.chunking.ArgChunkMeta")



* * *

### get_chunk_meta method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L259-L261 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator.get_chunk_meta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-35-1)ChunkMetaGenerator.get_chunk_meta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-35-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-35-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-35-4))
    

Get chunk metadata.

* * *

## ChunkSelector class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L472-L485 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSelector "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-36-1)ChunkSelector(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-36-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-36-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-36-4))
    

Class for selecting one element based on the chunk index.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [DimRetainer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer "vectorbtpro.utils.chunking.DimRetainer")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ChunkTaker.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ChunkTaker.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ChunkTaker.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ChunkTaker.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ChunkTaker.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ChunkTaker.find_messages")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ChunkTaker.apply")
  * [ChunkTaker.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ChunkTaker.eval_id")
  * [ChunkTaker.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ChunkTaker.fields")
  * [ChunkTaker.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ChunkTaker.fields_dict")
  * [ChunkTaker.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ChunkTaker.get_size")
  * [ChunkTaker.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ChunkTaker.hash")
  * [ChunkTaker.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ChunkTaker.hash_key")
  * [ChunkTaker.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ChunkTaker.ignore_none")
  * [ChunkTaker.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ChunkTaker.mapper")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ChunkTaker.should_take")
  * [ChunkTaker.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ChunkTaker.single_type")
  * [ChunkTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ChunkTaker.suggest_size")
  * [ChunkTaker.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ChunkTaker.take")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ChunkTaker.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ChunkTaker.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ChunkTaker.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ChunkTaker.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ChunkTaker.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ChunkTaker.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ChunkTaker.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ChunkTaker.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ChunkTaker.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ChunkTaker.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ChunkTaker.resolve_field")
  * [DimRetainer.keep_dims](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer.keep_dims "vectorbtpro.utils.chunking.DimRetainer.keep_dims")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ChunkTaker.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ChunkTaker.get_hash")



**Subclasses**

  * [ShapeSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSelector "vectorbtpro.utils.chunking.ShapeSelector")



* * *

## ChunkSlicer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L488-L497 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSlicer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-37-1)ChunkSlicer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-37-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-37-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-37-4))
    

Class for slicing multiple elements based on the chunk range.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ChunkTaker.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ChunkTaker.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ChunkTaker.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ChunkTaker.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ChunkTaker.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ChunkTaker.find_messages")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ChunkTaker.apply")
  * [ChunkTaker.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ChunkTaker.eval_id")
  * [ChunkTaker.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ChunkTaker.fields")
  * [ChunkTaker.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ChunkTaker.fields_dict")
  * [ChunkTaker.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ChunkTaker.get_size")
  * [ChunkTaker.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ChunkTaker.hash")
  * [ChunkTaker.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ChunkTaker.hash_key")
  * [ChunkTaker.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ChunkTaker.ignore_none")
  * [ChunkTaker.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ChunkTaker.mapper")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ChunkTaker.should_take")
  * [ChunkTaker.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ChunkTaker.single_type")
  * [ChunkTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ChunkTaker.suggest_size")
  * [ChunkTaker.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ChunkTaker.take")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ChunkTaker.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ChunkTaker.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ChunkTaker.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ChunkTaker.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ChunkTaker.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ChunkTaker.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ChunkTaker.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ChunkTaker.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ChunkTaker.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ChunkTaker.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ChunkTaker.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ChunkTaker.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ChunkTaker.get_hash")



**Subclasses**

  * [CountAdapter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.CountAdapter "vectorbtpro.utils.chunking.CountAdapter")
  * [GroupLensSlicer](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupLensSlicer "vectorbtpro.base.chunking.GroupLensSlicer")
  * [GroupMapSlicer](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.GroupMapSlicer "vectorbtpro.base.chunking.GroupMapSlicer")
  * [ShapeSlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSlicer "vectorbtpro.utils.chunking.ShapeSlicer")



* * *

## ChunkTaker class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L417-L469 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-38-1)ChunkTaker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-38-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-38-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-38-4))
    

Abstract class for taking one or more elements based on the chunk index or range.

Note

Use [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ChunkTaker.apply") instead of [ChunkTaker.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ChunkTaker.take").

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.eval_.Evaluable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.eval_.Evaluable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.eval_.Evaluable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.eval_.Evaluable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.eval_.Evaluable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.eval_.Evaluable.find_messages")
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
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.eval_.Evaluable.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



**Subclasses**

  * [ChunkSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSelector "vectorbtpro.utils.chunking.ChunkSelector")
  * [ChunkSlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSlicer "vectorbtpro.utils.chunking.ChunkSlicer")
  * [ContainerTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker "vectorbtpro.utils.chunking.ContainerTaker")



* * *

### apply method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L455-L461 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-39-1)ChunkTaker.apply(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-39-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-39-3)    chunk_meta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-39-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-39-5))
    

Apply the taker.

* * *

### eval_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "Permanent link")

One or more identifiers at which to evaluate this instance.

* * *

### get_size method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L436-L438 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-40-1)ChunkTaker.get_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-40-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-40-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-40-4))
    

Get the actual size of the argument.

* * *

### ignore_none field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "Permanent link")

Whether to ignore None.

* * *

### mapper field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "Permanent link")

Chunk mapper of type [ChunkMapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMapper "vectorbtpro.utils.chunking.ChunkMapper").

* * *

### should_take method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L446-L453 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-41-1)ChunkTaker.should_take(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-41-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-41-3)    chunk_meta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-41-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-41-5))
    

Check whether to take a chunk or leave the argument as it is.

* * *

### single_type field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "Permanent link")

One or multiple types to consider as a single value.

* * *

### suggest_size method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L440-L444 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-42-1)ChunkTaker.suggest_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-42-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-42-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-42-4))
    

Suggest a global size based on the argument's size.

* * *

### take method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L463-L469 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-43-1)ChunkTaker.take(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-43-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-43-3)    chunk_meta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-43-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-43-5))
    

Abstract method for taking subset of data.

Takes the argument object, the chunk meta (tuple out of the index, start index, and end index of the chunk), and other keyword arguments passed down the stack, such as `chunker` and `silence_warnings`.

* * *

## Chunkable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L890-L899 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-44-1)Chunkable()
    

Abstract class representing a value and a chunk taking specification.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.eval_.Evaluable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.eval_.Evaluable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.eval_.Evaluable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.eval_.Evaluable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.eval_.Evaluable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.eval_.Evaluable.find_messages")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.eval_.Evaluable.meets_eval_id")



**Subclasses**

  * [Chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked "vectorbtpro.utils.chunking.Chunked")



* * *

### get_take_spec method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L897-L899 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_take_spec "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-45-1)Chunkable.get_take_spec()
    

Get the chunk taking specification.

* * *

### get_value method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L893-L895 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_value "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-46-1)Chunkable.get_value()
    

Get the value.

* * *

## Chunked class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L902-L978 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-47-1)Chunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-47-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-47-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-47-4))
    

Class representing a chunkable value.

Can take a variable number of keyword arguments, which will be used as [Chunked.take_spec_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_kwargs "vectorbtpro.utils.chunking.Chunked.take_spec_kwargs").

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Chunkable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable "vectorbtpro.utils.chunking.Chunkable")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.Chunkable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.Chunkable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.Chunkable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.Chunkable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.Chunkable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.Chunkable.find_messages")
  * [Chunkable.get_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_take_spec "vectorbtpro.utils.chunking.Chunkable.get_take_spec")
  * [Chunkable.get_value](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_value "vectorbtpro.utils.chunking.Chunkable.get_value")
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
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.Chunkable.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



**Subclasses**

  * [ChunkedArray](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedArray "vectorbtpro.utils.chunking.ChunkedArray")
  * [ChunkedCount](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedCount "vectorbtpro.utils.chunking.ChunkedCount")
  * [ChunkedFlexArray](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.ChunkedFlexArray "vectorbtpro.base.chunking.ChunkedFlexArray")
  * [ChunkedGroupLens](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.ChunkedGroupLens "vectorbtpro.base.chunking.ChunkedGroupLens")
  * [ChunkedGroupMap](https://vectorbt.pro/pvt_7a467f6b/api/base/chunking/#vectorbtpro.base.chunking.ChunkedGroupMap "vectorbtpro.base.chunking.ChunkedGroupMap")
  * [ChunkedShape](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedShape "vectorbtpro.utils.chunking.ChunkedShape")



* * *

### eval_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.eval_id "Permanent link")

One or more identifiers at which to evaluate this instance.

* * *

### resolve_take_spec method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L957-L963 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.resolve_take_spec "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-48-1)Chunked.resolve_take_spec()
    

Resolve `take_spec`.

* * *

### select field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.select "Permanent link")

Whether to chunk by selection.

* * *

### take_spec field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec "Permanent link")

Chunk taking specification.

* * *

### take_spec_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_kwargs "Permanent link")

Keyword arguments passed to the respective [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker") subclass.

If [Chunked.take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec "vectorbtpro.utils.chunking.Chunked.take_spec") is an instance rather than a class, will "evolve" it.

* * *

### take_spec_missing field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L952-L955 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_missing "Permanent link")

Check whether [Chunked.take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec "vectorbtpro.utils.chunking.Chunked.take_spec") is missing.

* * *

### value field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.value "Permanent link")

Value.

* * *

## ChunkedArray class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1001-L1021 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedArray "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-49-1)ChunkedArray(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-49-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-49-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-49-4))
    

Class representing a chunkable array.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Chunkable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable "vectorbtpro.utils.chunking.Chunkable")
  * [Chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked "vectorbtpro.utils.chunking.Chunked")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.Chunked.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.Chunked.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.Chunked.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.Chunked.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.Chunked.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.Chunked.find_messages")
  * [Chunked.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.eval_id "vectorbtpro.utils.chunking.Chunked.eval_id")
  * [Chunked.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.Chunked.fields")
  * [Chunked.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.Chunked.fields_dict")
  * [Chunked.get_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_take_spec "vectorbtpro.utils.chunking.Chunked.get_take_spec")
  * [Chunked.get_value](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_value "vectorbtpro.utils.chunking.Chunked.get_value")
  * [Chunked.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.Chunked.hash")
  * [Chunked.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.Chunked.hash_key")
  * [Chunked.resolve_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.resolve_take_spec "vectorbtpro.utils.chunking.Chunked.resolve_take_spec")
  * [Chunked.select](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.select "vectorbtpro.utils.chunking.Chunked.select")
  * [Chunked.take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec "vectorbtpro.utils.chunking.Chunked.take_spec")
  * [Chunked.take_spec_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_kwargs "vectorbtpro.utils.chunking.Chunked.take_spec_kwargs")
  * [Chunked.take_spec_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_missing "vectorbtpro.utils.chunking.Chunked.take_spec_missing")
  * [Chunked.value](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.value "vectorbtpro.utils.chunking.Chunked.value")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.Chunked.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.Chunked.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.Chunked.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.Chunked.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.Chunked.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.Chunked.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.Chunked.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.Chunked.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.Chunked.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.Chunked.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.Chunked.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.Chunked.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.Chunked.get_hash")



* * *

### flex field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedArray.flex "Permanent link")

Whether the array is flexible.

* * *

## ChunkedCount class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L981-L987 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedCount "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-50-1)ChunkedCount(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-50-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-50-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-50-4))
    

Class representing a chunkable count.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Chunkable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable "vectorbtpro.utils.chunking.Chunkable")
  * [Chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked "vectorbtpro.utils.chunking.Chunked")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.Chunked.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.Chunked.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.Chunked.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.Chunked.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.Chunked.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.Chunked.find_messages")
  * [Chunked.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.eval_id "vectorbtpro.utils.chunking.Chunked.eval_id")
  * [Chunked.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.Chunked.fields")
  * [Chunked.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.Chunked.fields_dict")
  * [Chunked.get_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_take_spec "vectorbtpro.utils.chunking.Chunked.get_take_spec")
  * [Chunked.get_value](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_value "vectorbtpro.utils.chunking.Chunked.get_value")
  * [Chunked.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.Chunked.hash")
  * [Chunked.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.Chunked.hash_key")
  * [Chunked.resolve_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.resolve_take_spec "vectorbtpro.utils.chunking.Chunked.resolve_take_spec")
  * [Chunked.select](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.select "vectorbtpro.utils.chunking.Chunked.select")
  * [Chunked.take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec "vectorbtpro.utils.chunking.Chunked.take_spec")
  * [Chunked.take_spec_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_kwargs "vectorbtpro.utils.chunking.Chunked.take_spec_kwargs")
  * [Chunked.take_spec_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_missing "vectorbtpro.utils.chunking.Chunked.take_spec_missing")
  * [Chunked.value](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.value "vectorbtpro.utils.chunking.Chunked.value")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.Chunked.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.Chunked.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.Chunked.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.Chunked.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.Chunked.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.Chunked.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.Chunked.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.Chunked.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.Chunked.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.Chunked.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.Chunked.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.Chunked.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.Chunked.get_hash")



* * *

## ChunkedShape class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L990-L998 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedShape "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-51-1)ChunkedShape(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-51-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-51-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-51-4))
    

Class representing a chunkable shape.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Chunkable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable "vectorbtpro.utils.chunking.Chunkable")
  * [Chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked "vectorbtpro.utils.chunking.Chunked")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.Chunked.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.Chunked.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.Chunked.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.Chunked.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.Chunked.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.Chunked.find_messages")
  * [Chunked.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.eval_id "vectorbtpro.utils.chunking.Chunked.eval_id")
  * [Chunked.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.Chunked.fields")
  * [Chunked.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.Chunked.fields_dict")
  * [Chunked.get_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_take_spec "vectorbtpro.utils.chunking.Chunked.get_take_spec")
  * [Chunked.get_value](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunkable.get_value "vectorbtpro.utils.chunking.Chunked.get_value")
  * [Chunked.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.Chunked.hash")
  * [Chunked.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.Chunked.hash_key")
  * [Chunked.resolve_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.resolve_take_spec "vectorbtpro.utils.chunking.Chunked.resolve_take_spec")
  * [Chunked.select](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.select "vectorbtpro.utils.chunking.Chunked.select")
  * [Chunked.take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec "vectorbtpro.utils.chunking.Chunked.take_spec")
  * [Chunked.take_spec_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_kwargs "vectorbtpro.utils.chunking.Chunked.take_spec_kwargs")
  * [Chunked.take_spec_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.take_spec_missing "vectorbtpro.utils.chunking.Chunked.take_spec_missing")
  * [Chunked.value](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunked.value "vectorbtpro.utils.chunking.Chunked.value")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.Chunked.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.Chunked.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.Chunked.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.Chunked.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.Chunked.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.Chunked.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.Chunked.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.Chunked.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.Chunked.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.Chunked.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.Chunked.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.Chunked.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.Chunked.get_hash")



* * *

## Chunker class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1027-L1817 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-1)Chunker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-2)    size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-3)    min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-4)    n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-5)    chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-6)    chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-7)    prepend_chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-8)    skip_single_chunk=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-9)    arg_take_spec=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-10)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-11)    merge_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-12)    merge_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-13)    return_raw_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-14)    silence_warnings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-15)    forward_kwargs_as=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-16)    execute_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-17)    disable=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-18)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-52-19))
    

Class responsible for chunking arguments of a function and running the function.

Does the following:

  1. Generates chunk metadata by passing `n_chunks`, `size`, `min_size`, `chunk_len`, and `chunk_meta` to [Chunker.get_chunk_meta_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args "vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args").
  2. Splits arguments and keyword arguments by passing chunk metadata, `arg_take_spec`, and `template_context` to [Chunker.iter_tasks](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.iter_tasks "vectorbtpro.utils.chunking.Chunker.iter_tasks"), which yields one chunk at a time.
  3. Executes all chunks by passing `**execute_kwargs` to [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute "vectorbtpro.utils.execution.execute").
  4. Optionally, post-processes and merges the results by passing them and `**merge_kwargs` to `merge_func`.



For defaults, see [chunking](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.chunking "vectorbtpro._settings.chunking").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.config.Configured.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.config.Configured.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.config.Configured.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.config.Configured.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.config.Configured.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.config.Configured.find_messages")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.utils.config.Configured.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.utils.config.Configured.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.utils.config.Configured.pipe")
  * [Configured.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.utils.config.Configured.config")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.utils.config.Configured.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.utils.config.Configured.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.utils.config.Configured.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.config.Configured.prettify")
  * [Configured.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.config.Configured.rec_state")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.utils.config.Configured.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.utils.config.Configured.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.utils.config.Configured.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.utils.config.Configured.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.utils.config.Configured.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.utils.config.Configured.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.utils.config.Configured.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.utils.config.Configured.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.utils.config.Configured.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.utils.config.Configured.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.utils.config.Configured.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.utils.config.Configured.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.utils.config.Configured.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.utils.config.Configured.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.utils.config.Configured.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.config.Configured.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.config.Configured.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.config.Configured.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.config.Configured.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.config.Configured.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.config.Configured.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.config.Configured.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.config.Configured.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.config.Configured.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.config.Configured.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.config.Configured.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.config.Configured.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.config.Configured.pprint")



* * *

### adapt_ann_args class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1600-L1624 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.adapt_ann_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-53-1)Chunker.adapt_ann_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-53-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-53-3)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-53-4))
    

Adapt annotated arguments.

* * *

### arg_take_spec class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1139-L1142 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.arg_take_spec "Permanent link")

See `iter_tasks`.

* * *

### chunk_len class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1117-L1120 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.chunk_len "Permanent link")

See [Chunker.get_chunk_meta_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args "vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args").

* * *

### chunk_meta class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1122-L1125 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.chunk_meta "Permanent link")

See [Chunker.get_chunk_meta_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args "vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args").

* * *

### disable class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1187-L1190 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.disable "Permanent link")

Whether to disable chunking.

* * *

### execute_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1182-L1185 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.execute_kwargs "Permanent link")

Keyword arguments passed to [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute "vectorbtpro.utils.execution.execute").

* * *

### fill_arg_take_spec class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1591-L1598 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.fill_arg_take_spec "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-54-1)Chunker.fill_arg_take_spec(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-54-2)    arg_take_spec,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-54-3)    ann_args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-54-4))
    

Fill the chunk taking specification with None to avoid warnings.

* * *

### find_take_spec class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1292-L1339 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.find_take_spec "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-55-1)Chunker.find_take_spec(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-55-2)    i,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-55-3)    ann_arg_name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-55-4)    ann_arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-55-5)    arg_take_spec
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-55-6))
    

Resolve the specification for an argument.

* * *

### forward_kwargs_as class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1175-L1180 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.forward_kwargs_as "Permanent link")

Map to rename keyword arguments.

Can also pass any variable from the scope of [Chunker.run](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.run "vectorbtpro.utils.chunking.Chunker.run")

* * *

### get_chunk_meta_from_args class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1192-L1253 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-1)Chunker.get_chunk_meta_from_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-3)    size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-4)    min_size=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-5)    n_chunks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-6)    chunk_len=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-7)    chunk_meta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-56-9))
    

Get chunk metadata from annotated arguments.

**Args**

**`ann_args`** : `dict`
    Arguments annotated with [annotate_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.annotate_args "vectorbtpro.utils.parsing.annotate_args").
**`size`** : `int`, [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer"), `or callable`
    

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

Can be an integer, an instance of [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer"), or a callable taking the annotated arguments and returning a value.

**`min_size`** : `int`
    See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").
**`n_chunks`** : `int`, `str`, [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer"), `or callable`
    

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

Can be an integer, a string, an instance of [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer"), or a callable taking the annotated arguments and other keyword arguments and returning a value.

**`chunk_len`** : `int`, `str`, [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer"), `or callable`
    

See [iter_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.iter_chunk_meta "vectorbtpro.utils.chunking.iter_chunk_meta").

Can be an integer, a string, an instance of [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer"), or a callable taking the annotated arguments and returning a value.

**`chunk_meta`** : `iterable` of [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta"), [ChunkMetaGenerator](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator "vectorbtpro.utils.chunking.ChunkMetaGenerator"), `or callable`
    

Chunk meta.

Can be an iterable of [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta"), an instance of [ChunkMetaGenerator](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator "vectorbtpro.utils.chunking.ChunkMetaGenerator"), or a callable taking the annotated arguments and other arguments and returning an iterable.

**`**kwargs`**
    Other keyword arguments passed to any callable.

* * *

### iter_tasks class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1390-L1446 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.iter_tasks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-57-1)Chunker.iter_tasks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-57-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-57-3)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-57-4)    chunk_meta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-57-5)    arg_take_spec=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-57-6)    template_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-57-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-57-8))
    

Split annotated arguments into chunks using [Chunker.take_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_args "vectorbtpro.utils.chunking.Chunker.take_from_args") and yield each chunk as a task.

**Args**

**`func`** : `callable`
    Callable.
**`ann_args`** : `dict`
    Arguments annotated with [annotate_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.annotate_args "vectorbtpro.utils.parsing.annotate_args").
**`chunk_meta`** : `iterable` of [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta")
    Chunk metadata.
**`arg_take_spec`** : `mapping`, `sequence`, `callable`, `or CustomTemplate`
    

Chunk taking specification.

Can be a dictionary (see [Chunker.take_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_args "vectorbtpro.utils.chunking.Chunker.take_from_args")), or a sequence that will be converted into a dictionary. If a callable, will be called instead of [Chunker.take_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_args "vectorbtpro.utils.chunking.Chunker.take_from_args"), thus it must have the same arguments apart from `arg_take_spec`.

**`template_context`** : `mapping`
    Context used to substitute templates in arguments and specification.
**`**kwargs`**
    Keyword arguments passed to [Chunker.take_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_args "vectorbtpro.utils.chunking.Chunker.take_from_args") or to `arg_take_spec` if it's a callable.

* * *

### merge_func class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1153-L1158 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.merge_func "Permanent link")

Merging function.

Resolved using [resolve_merge_func](https://vectorbt.pro/pvt_7a467f6b/api/base/merging/#vectorbtpro.base.merging.resolve_merge_func "vectorbtpro.base.merging.resolve_merge_func").

* * *

### merge_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1160-L1163 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.merge_kwargs "Permanent link")

Keyword arguments passed to the merging function.

* * *

### min_size class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1107-L1110 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.min_size "Permanent link")

See [Chunker.get_chunk_meta_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args "vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args").

* * *

### n_chunks class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1112-L1115 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.n_chunks "Permanent link")

See [Chunker.get_chunk_meta_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args "vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args").

* * *

### parse_sizer_from_func class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1448-L1470 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.parse_sizer_from_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-58-1)Chunker.parse_sizer_from_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-58-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-58-3)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-58-4))
    

Parse the sizer from a function.

* * *

### parse_spec_from_annotations class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1472-L1495 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.parse_spec_from_annotations "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-59-1)Chunker.parse_spec_from_annotations(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-59-2)    annotations,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-59-3)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-59-4))
    

Parse the chunk taking specification from annotations.

* * *

### parse_spec_from_args class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1550-L1589 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.parse_spec_from_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-60-1)Chunker.parse_spec_from_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-60-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-60-3)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-60-4))
    

Parse the chunk taking specification from (annotated) arguments.

* * *

### parse_spec_from_func class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1497-L1548 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.parse_spec_from_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-61-1)Chunker.parse_spec_from_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-61-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-61-3)    eval_id=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-61-4))
    

Parse the chunk taking specification from a function.

* * *

### prepend_chunk_meta class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1127-L1132 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.prepend_chunk_meta "Permanent link")

Whether to prepend an instance of [ChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMeta "vectorbtpro.utils.chunking.ChunkMeta") to the arguments.

If None, prepends automatically if the first argument is named 'chunk_meta'.

* * *

### resolve_take_spec class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1255-L1264 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.resolve_take_spec "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-62-1)Chunker.resolve_take_spec(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-62-2)    take_spec
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-62-3))
    

Resolve the chunk taking specification.

* * *

### return_raw_chunks class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1165-L1168 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.return_raw_chunks "Permanent link")

Whether to return chunks in a raw format.

* * *

### run method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1656-L1817 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.run "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-63-1)Chunker.run(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-63-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-63-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-63-4)    eval_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-63-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-63-6))
    

Chunk arguments and run the function.

* * *

### silence_warnings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1170-L1173 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.silence_warnings "Permanent link")

Whether to silence any warnings.

* * *

### size class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1102-L1105 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.size "Permanent link")

See [Chunker.get_chunk_meta_from_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args "vectorbtpro.utils.chunking.Chunker.get_chunk_meta_from_args").

* * *

### skip_single_chunk class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1134-L1137 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.skip_single_chunk "Permanent link")

Whether to execute the function directly if there's only one chunk.

* * *

### suggest_size class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1626-L1654 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.suggest_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-64-1)Chunker.suggest_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-64-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-64-3)    arg_take_spec,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-64-4)    eval_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-64-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-64-6))
    

Suggest a global size given the annotated arguments and the chunk taking specification.

* * *

### take_from_arg class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1266-L1290 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_arg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-65-1)Chunker.take_from_arg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-65-2)    arg,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-65-3)    take_spec,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-65-4)    chunk_meta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-65-5)    eval_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-65-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-65-7))
    

Take from the argument given the specification `take_spec`.

If `take_spec` is None or it's an instance of [NotChunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.NotChunked "vectorbtpro.utils.chunking.NotChunked"), returns the original object. Otherwise, must be an instance of [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker").

`**kwargs` are passed to [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ChunkTaker.apply").

* * *

### take_from_args class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1341-L1388 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-66-1)Chunker.take_from_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-66-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-66-3)    arg_take_spec,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-66-4)    chunk_meta,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-66-5)    silence_warnings=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-66-6)    eval_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-66-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-66-8))
    

Take from each in the annotated arguments given the specification using [Chunker.take_from_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_arg "vectorbtpro.utils.chunking.Chunker.take_from_arg").

Additionally, passes to [Chunker.take_from_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_arg "vectorbtpro.utils.chunking.Chunker.take_from_arg") as keyword arguments `ann_args` and `arg_take_spec`.

`arg_take_spec` must be a dictionary, with keys being argument positions or names as generated by [annotate_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/parsing/#vectorbtpro.utils.parsing.annotate_args "vectorbtpro.utils.parsing.annotate_args"). For values, see [Chunker.take_from_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_arg "vectorbtpro.utils.chunking.Chunker.take_from_arg").

Returns arguments and keyword arguments that can be directly passed to the function using `func(*args, **kwargs)`.

* * *

### template_context class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L1144-L1151 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.template_context "Permanent link")

Template context.

Any template in both `execute_kwargs` and `merge_kwargs` will be substituted. You can use the keys `ann_args`, `chunk_meta`, `arg_take_spec`, and `tasks` to be replaced by the actual objects.

* * *

## ContainerTaker class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L648-L681 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-67-1)ContainerTaker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-67-2)    cont_take_spec=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-67-3)    single_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-67-4)    ignore_none=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-67-5)    mapper=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-67-6))
    

Class for taking from a container with other chunk takers.

Accepts the specification of the container.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ChunkTaker.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ChunkTaker.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ChunkTaker.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ChunkTaker.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ChunkTaker.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ChunkTaker.find_messages")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ChunkTaker.apply")
  * [ChunkTaker.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ChunkTaker.eval_id")
  * [ChunkTaker.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ChunkTaker.fields")
  * [ChunkTaker.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ChunkTaker.fields_dict")
  * [ChunkTaker.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ChunkTaker.get_size")
  * [ChunkTaker.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ChunkTaker.hash")
  * [ChunkTaker.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ChunkTaker.hash_key")
  * [ChunkTaker.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ChunkTaker.ignore_none")
  * [ChunkTaker.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ChunkTaker.mapper")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ChunkTaker.should_take")
  * [ChunkTaker.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ChunkTaker.single_type")
  * [ChunkTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ChunkTaker.suggest_size")
  * [ChunkTaker.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ChunkTaker.take")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ChunkTaker.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ChunkTaker.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ChunkTaker.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ChunkTaker.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ChunkTaker.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ChunkTaker.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ChunkTaker.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ChunkTaker.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ChunkTaker.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ChunkTaker.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ChunkTaker.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ChunkTaker.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ChunkTaker.get_hash")



**Subclasses**

  * [MappingTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.MappingTaker "vectorbtpro.utils.chunking.MappingTaker")
  * [SequenceTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.SequenceTaker "vectorbtpro.utils.chunking.SequenceTaker")



* * *

### check_cont_take_spec method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L675-L678 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.check_cont_take_spec "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-68-1)ContainerTaker.check_cont_take_spec()
    

Check that [ContainerTaker.cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec "vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec") is not None.

* * *

### cont_take_spec field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec "Permanent link")

Specification of the container.

* * *

## CountAdapter class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L500-L515 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.CountAdapter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-69-1)CountAdapter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-69-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-69-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-69-4))
    

Class for adapting a count based on the chunk range.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkSlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSlicer "vectorbtpro.utils.chunking.ChunkSlicer")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ChunkSlicer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ChunkSlicer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ChunkSlicer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ChunkSlicer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ChunkSlicer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ChunkSlicer.find_messages")
  * [ChunkSlicer.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ChunkSlicer.eval_id")
  * [ChunkSlicer.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ChunkSlicer.fields")
  * [ChunkSlicer.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ChunkSlicer.fields_dict")
  * [ChunkSlicer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ChunkSlicer.get_size")
  * [ChunkSlicer.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ChunkSlicer.hash")
  * [ChunkSlicer.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ChunkSlicer.hash_key")
  * [ChunkSlicer.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ChunkSlicer.ignore_none")
  * [ChunkSlicer.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ChunkSlicer.mapper")
  * [ChunkSlicer.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ChunkSlicer.single_type")
  * [ChunkSlicer.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ChunkSlicer.take")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ChunkSlicer.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ChunkSlicer.should_take")
  * [ChunkTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ChunkSlicer.suggest_size")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ChunkSlicer.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ChunkSlicer.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ChunkSlicer.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ChunkSlicer.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ChunkSlicer.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ChunkSlicer.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ChunkSlicer.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ChunkSlicer.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ChunkSlicer.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ChunkSlicer.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ChunkSlicer.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ChunkSlicer.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ChunkSlicer.get_hash")



* * *

## CountSizer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L144-L156 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.CountSizer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-70-1)CountSizer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-70-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-70-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-70-4))
    

Class for getting the size from a count.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [ArgGetter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "vectorbtpro.utils.chunking.ArgGetter")
  * [ArgSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer "vectorbtpro.utils.chunking.ArgSizer")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer")



**Inherited members**

  * [ArgGetter.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.get_arg "vectorbtpro.utils.chunking.ArgSizer.get_arg")
  * [ArgSizer.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.apply "vectorbtpro.utils.chunking.ArgSizer.apply")
  * [ArgSizer.arg_query](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.arg_query "vectorbtpro.utils.chunking.ArgSizer.arg_query")
  * [ArgSizer.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.eval_id "vectorbtpro.utils.chunking.ArgSizer.eval_id")
  * [ArgSizer.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ArgSizer.fields")
  * [ArgSizer.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ArgSizer.fields_dict")
  * [ArgSizer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.get_size "vectorbtpro.utils.chunking.ArgSizer.get_size")
  * [ArgSizer.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ArgSizer.hash")
  * [ArgSizer.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ArgSizer.hash_key")
  * [ArgSizer.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer.single_type "vectorbtpro.utils.chunking.ArgSizer.single_type")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ArgSizer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ArgSizer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ArgSizer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ArgSizer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ArgSizer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ArgSizer.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ArgSizer.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ArgSizer.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ArgSizer.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ArgSizer.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ArgSizer.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ArgSizer.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ArgSizer.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ArgSizer.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ArgSizer.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ArgSizer.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ArgSizer.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ArgSizer.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ArgSizer.get_hash")



* * *

### get_obj_size class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L147-L153 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.CountSizer.get_obj_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-71-1)CountSizer.get_obj_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-71-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-71-3)    single_type=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-71-4))
    

Get size of an object.

* * *

## DimRetainer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L97-L102 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-72-1)DimRetainer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-72-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-72-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-72-4))
    

Class with an attribute for retaining dimensions.

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



**Subclasses**

  * [ChunkSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSelector "vectorbtpro.utils.chunking.ChunkSelector")



* * *

### keep_dims field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer.keep_dims "Permanent link")

Whether to retain dimensions.

* * *

## KwargsTaker class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L868-L884 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.KwargsTaker "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-73-1)KwargsTaker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-73-2)    single_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-73-3)    ignore_none=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-73-4)    mapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-73-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-73-6))
    

Class for taking from a variable keyword arguments container.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [ContainerTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker "vectorbtpro.utils.chunking.ContainerTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [MappingTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.MappingTaker "vectorbtpro.utils.chunking.MappingTaker")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.MappingTaker.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.MappingTaker.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.MappingTaker.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.MappingTaker.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.MappingTaker.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.MappingTaker.find_messages")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.MappingTaker.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.MappingTaker.should_take")
  * [ContainerTaker.check_cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.check_cont_take_spec "vectorbtpro.utils.chunking.MappingTaker.check_cont_take_spec")
  * [ContainerTaker.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.MappingTaker.get_size")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.MappingTaker.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.MappingTaker.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.MappingTaker.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.MappingTaker.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.MappingTaker.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.MappingTaker.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.MappingTaker.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.MappingTaker.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.MappingTaker.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.MappingTaker.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.MappingTaker.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.MappingTaker.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.MappingTaker.get_hash")
  * [MappingTaker.adapt_cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.MappingTaker.adapt_cont_take_spec "vectorbtpro.utils.chunking.MappingTaker.adapt_cont_take_spec")
  * [MappingTaker.cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec "vectorbtpro.utils.chunking.MappingTaker.cont_take_spec")
  * [MappingTaker.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.MappingTaker.eval_id")
  * [MappingTaker.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.MappingTaker.fields")
  * [MappingTaker.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.MappingTaker.fields_dict")
  * [MappingTaker.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.MappingTaker.hash")
  * [MappingTaker.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.MappingTaker.hash_key")
  * [MappingTaker.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.MappingTaker.ignore_none")
  * [MappingTaker.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.MappingTaker.mapper")
  * [MappingTaker.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.MappingTaker.single_type")
  * [MappingTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.MappingTaker.suggest_size")
  * [MappingTaker.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.MappingTaker.take")



* * *

## LenChunkMeta class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L271-L281 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.LenChunkMeta "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-74-1)LenChunkMeta(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-74-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-74-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-74-4))
    

Class for generating chunk metadata from a sequence of chunk lengths.

**Superclasses**

  * [ArgChunkMeta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgChunkMeta "vectorbtpro.utils.chunking.ArgChunkMeta")
  * [ArgGetter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "vectorbtpro.utils.chunking.ArgGetter")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkMetaGenerator](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator "vectorbtpro.utils.chunking.ChunkMetaGenerator")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [ArgChunkMeta.arg_query](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.arg_query "vectorbtpro.utils.chunking.ArgChunkMeta.arg_query")
  * [ArgChunkMeta.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ArgChunkMeta.fields")
  * [ArgChunkMeta.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ArgChunkMeta.fields_dict")
  * [ArgChunkMeta.get_chunk_meta](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkMetaGenerator.get_chunk_meta "vectorbtpro.utils.chunking.ArgChunkMeta.get_chunk_meta")
  * [ArgChunkMeta.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ArgChunkMeta.hash")
  * [ArgChunkMeta.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ArgChunkMeta.hash_key")
  * [ArgGetter.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.get_arg "vectorbtpro.utils.chunking.ArgChunkMeta.get_arg")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ArgChunkMeta.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ArgChunkMeta.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ArgChunkMeta.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ArgChunkMeta.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ArgChunkMeta.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ArgChunkMeta.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ArgChunkMeta.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ArgChunkMeta.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ArgChunkMeta.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ArgChunkMeta.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ArgChunkMeta.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ArgChunkMeta.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ArgChunkMeta.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ArgChunkMeta.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ArgChunkMeta.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ArgChunkMeta.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ArgChunkMeta.resolve_field")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ArgChunkMeta.get_hash")



* * *

## LenSizer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L159-L171 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.LenSizer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-75-1)LenSizer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-75-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-75-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-75-4))
    

Class for getting the size from the length of an argument.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [ArgGetter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "vectorbtpro.utils.chunking.ArgGetter")
  * [ArgSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer "vectorbtpro.utils.chunking.ArgSizer")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer")



**Inherited members**

  * [ArgGetter.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.get_arg "vectorbtpro.utils.chunking.ArgSizer.get_arg")
  * [ArgSizer.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.apply "vectorbtpro.utils.chunking.ArgSizer.apply")
  * [ArgSizer.arg_query](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.arg_query "vectorbtpro.utils.chunking.ArgSizer.arg_query")
  * [ArgSizer.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.eval_id "vectorbtpro.utils.chunking.ArgSizer.eval_id")
  * [ArgSizer.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ArgSizer.fields")
  * [ArgSizer.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ArgSizer.fields_dict")
  * [ArgSizer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.get_size "vectorbtpro.utils.chunking.ArgSizer.get_size")
  * [ArgSizer.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ArgSizer.hash")
  * [ArgSizer.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ArgSizer.hash_key")
  * [ArgSizer.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer.single_type "vectorbtpro.utils.chunking.ArgSizer.single_type")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ArgSizer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ArgSizer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ArgSizer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ArgSizer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ArgSizer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ArgSizer.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ArgSizer.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ArgSizer.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ArgSizer.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ArgSizer.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ArgSizer.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ArgSizer.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ArgSizer.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ArgSizer.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ArgSizer.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ArgSizer.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ArgSizer.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ArgSizer.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ArgSizer.get_hash")



* * *

### get_obj_size class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L162-L168 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.LenSizer.get_obj_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-76-1)LenSizer.get_obj_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-76-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-76-3)    single_type=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-76-4))
    

Get size of an object.

* * *

## MappingTaker class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L766-L846 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.MappingTaker "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-77-1)MappingTaker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-77-2)    cont_take_spec=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-77-3)    single_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-77-4)    ignore_none=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-77-5)    mapper=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-77-6))
    

Class for taking from a mapping container.

Calls [Chunker.take_from_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_arg "vectorbtpro.utils.chunking.Chunker.take_from_arg") on each element.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [ContainerTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker "vectorbtpro.utils.chunking.ContainerTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ContainerTaker.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ContainerTaker.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ContainerTaker.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ContainerTaker.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ContainerTaker.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ContainerTaker.find_messages")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ContainerTaker.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ContainerTaker.should_take")
  * [ChunkTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ContainerTaker.suggest_size")
  * [ContainerTaker.check_cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.check_cont_take_spec "vectorbtpro.utils.chunking.ContainerTaker.check_cont_take_spec")
  * [ContainerTaker.cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec "vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec")
  * [ContainerTaker.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ContainerTaker.eval_id")
  * [ContainerTaker.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ContainerTaker.fields")
  * [ContainerTaker.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ContainerTaker.fields_dict")
  * [ContainerTaker.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ContainerTaker.get_size")
  * [ContainerTaker.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ContainerTaker.hash")
  * [ContainerTaker.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ContainerTaker.hash_key")
  * [ContainerTaker.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ContainerTaker.ignore_none")
  * [ContainerTaker.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ContainerTaker.mapper")
  * [ContainerTaker.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ContainerTaker.single_type")
  * [ContainerTaker.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ContainerTaker.take")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ContainerTaker.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ContainerTaker.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ContainerTaker.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ContainerTaker.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ContainerTaker.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ContainerTaker.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ContainerTaker.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ContainerTaker.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ContainerTaker.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ContainerTaker.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ContainerTaker.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ContainerTaker.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ContainerTaker.get_hash")



**Subclasses**

  * [KwargsTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.KwargsTaker "vectorbtpro.utils.chunking.KwargsTaker")



* * *

### adapt_cont_take_spec method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L771-L784 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.MappingTaker.adapt_cont_take_spec "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-78-1)MappingTaker.adapt_cont_take_spec(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-78-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-78-3))
    

Prepare the specification of the container to the object.

* * *

## NotChunked class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L409-L414 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.NotChunked "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-79-1)NotChunked(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-79-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-79-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-79-4))
    

Class that represents an argument that shouldn't be chunked.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.eval_.Evaluable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.eval_.Evaluable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.eval_.Evaluable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.eval_.Evaluable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.eval_.Evaluable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.eval_.Evaluable.find_messages")
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
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.eval_.Evaluable.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.attr_.DefineMixin.get_hash")



* * *

### eval_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.NotChunked.eval_id "Permanent link")

One or more identifiers at which to evaluate this instance.

* * *

## SequenceTaker class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L684-L763 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.SequenceTaker "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-80-1)SequenceTaker(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-80-2)    cont_take_spec=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-80-3)    single_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-80-4)    ignore_none=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-80-5)    mapper=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-80-6))
    

Class for taking from a sequence container.

Calls [Chunker.take_from_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.take_from_arg "vectorbtpro.utils.chunking.Chunker.take_from_arg") on each element.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [ContainerTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker "vectorbtpro.utils.chunking.ContainerTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ContainerTaker.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ContainerTaker.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ContainerTaker.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ContainerTaker.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ContainerTaker.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ContainerTaker.find_messages")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ContainerTaker.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ContainerTaker.should_take")
  * [ChunkTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ContainerTaker.suggest_size")
  * [ContainerTaker.check_cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.check_cont_take_spec "vectorbtpro.utils.chunking.ContainerTaker.check_cont_take_spec")
  * [ContainerTaker.cont_take_spec](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec "vectorbtpro.utils.chunking.ContainerTaker.cont_take_spec")
  * [ContainerTaker.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ContainerTaker.eval_id")
  * [ContainerTaker.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ContainerTaker.fields")
  * [ContainerTaker.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ContainerTaker.fields_dict")
  * [ContainerTaker.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ContainerTaker.get_size")
  * [ContainerTaker.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ContainerTaker.hash")
  * [ContainerTaker.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ContainerTaker.hash_key")
  * [ContainerTaker.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ContainerTaker.ignore_none")
  * [ContainerTaker.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ContainerTaker.mapper")
  * [ContainerTaker.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ContainerTaker.single_type")
  * [ContainerTaker.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ContainerTaker.take")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ContainerTaker.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ContainerTaker.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ContainerTaker.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ContainerTaker.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ContainerTaker.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ContainerTaker.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ContainerTaker.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ContainerTaker.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ContainerTaker.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ContainerTaker.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ContainerTaker.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ContainerTaker.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ContainerTaker.get_hash")



**Subclasses**

  * [ArgsTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgsTaker "vectorbtpro.utils.chunking.ArgsTaker")



* * *

### adapt_cont_take_spec method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L689-L697 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.SequenceTaker.adapt_cont_take_spec "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-81-1)SequenceTaker.adapt_cont_take_spec(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-81-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-81-3))
    

Prepare the specification of the container to the object.

* * *

## ShapeSelector class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L518-L545 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSelector "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-82-1)ShapeSelector(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-82-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-82-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-82-4))
    

Class for selecting one element from a shape's axis based on the chunk index.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [AxisSpecifier](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier "vectorbtpro.utils.chunking.AxisSpecifier")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkSelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSelector "vectorbtpro.utils.chunking.ChunkSelector")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [DimRetainer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer "vectorbtpro.utils.chunking.DimRetainer")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [AxisSpecifier.axis](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier.axis "vectorbtpro.utils.chunking.AxisSpecifier.axis")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ChunkSelector.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ChunkSelector.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ChunkSelector.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ChunkSelector.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ChunkSelector.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ChunkSelector.find_messages")
  * [ChunkSelector.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ChunkSelector.eval_id")
  * [ChunkSelector.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ChunkSelector.fields")
  * [ChunkSelector.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ChunkSelector.fields_dict")
  * [ChunkSelector.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ChunkSelector.get_size")
  * [ChunkSelector.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ChunkSelector.hash")
  * [ChunkSelector.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ChunkSelector.hash_key")
  * [ChunkSelector.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ChunkSelector.ignore_none")
  * [ChunkSelector.keep_dims](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.DimRetainer.keep_dims "vectorbtpro.utils.chunking.ChunkSelector.keep_dims")
  * [ChunkSelector.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ChunkSelector.mapper")
  * [ChunkSelector.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ChunkSelector.single_type")
  * [ChunkSelector.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ChunkSelector.suggest_size")
  * [ChunkSelector.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ChunkSelector.take")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ChunkSelector.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ChunkSelector.should_take")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ChunkSelector.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ChunkSelector.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ChunkSelector.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ChunkSelector.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ChunkSelector.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ChunkSelector.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ChunkSelector.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ChunkSelector.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ChunkSelector.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ChunkSelector.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ChunkSelector.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ChunkSelector.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ChunkSelector.get_hash")



**Subclasses**

  * [ArraySelector](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArraySelector "vectorbtpro.utils.chunking.ArraySelector")



* * *

## ShapeSizer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L174-L197 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSizer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-83-1)ShapeSizer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-83-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-83-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-83-4))
    

Class for getting the size from the length of an axis in a shape.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [ArgGetter](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter "vectorbtpro.utils.chunking.ArgGetter")
  * [ArgSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer "vectorbtpro.utils.chunking.ArgSizer")
  * [AxisSpecifier](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier "vectorbtpro.utils.chunking.AxisSpecifier")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")
  * [Sizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "vectorbtpro.utils.chunking.Sizer")



**Inherited members**

  * [ArgGetter.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.get_arg "vectorbtpro.utils.chunking.ArgSizer.get_arg")
  * [ArgSizer.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.apply "vectorbtpro.utils.chunking.ArgSizer.apply")
  * [ArgSizer.arg_query](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgGetter.arg_query "vectorbtpro.utils.chunking.ArgSizer.arg_query")
  * [ArgSizer.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.eval_id "vectorbtpro.utils.chunking.ArgSizer.eval_id")
  * [ArgSizer.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ArgSizer.fields")
  * [ArgSizer.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ArgSizer.fields_dict")
  * [ArgSizer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.get_size "vectorbtpro.utils.chunking.ArgSizer.get_size")
  * [ArgSizer.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ArgSizer.hash")
  * [ArgSizer.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ArgSizer.hash_key")
  * [ArgSizer.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer.single_type "vectorbtpro.utils.chunking.ArgSizer.single_type")
  * [AxisSpecifier.axis](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier.axis "vectorbtpro.utils.chunking.AxisSpecifier.axis")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ArgSizer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ArgSizer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ArgSizer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ArgSizer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ArgSizer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ArgSizer.find_messages")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ArgSizer.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ArgSizer.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ArgSizer.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ArgSizer.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ArgSizer.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ArgSizer.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ArgSizer.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ArgSizer.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ArgSizer.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ArgSizer.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ArgSizer.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ArgSizer.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ArgSizer.get_hash")



**Subclasses**

  * [ArraySizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArraySizer "vectorbtpro.utils.chunking.ArraySizer")



* * *

### get_obj_size class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L178-L194 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSizer.get_obj_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-84-1)ShapeSizer.get_obj_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-84-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-84-3)    axis,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-84-4)    single_type=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-84-5))
    

Get size of an object.

* * *

## ShapeSlicer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L548-L579 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ShapeSlicer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-85-1)ShapeSlicer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-85-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-85-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-85-4))
    

Class for slicing multiple elements from a shape's axis based on the chunk range.

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [AxisSpecifier](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier "vectorbtpro.utils.chunking.AxisSpecifier")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [ChunkSlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkSlicer "vectorbtpro.utils.chunking.ChunkSlicer")
  * [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker "vectorbtpro.utils.chunking.ChunkTaker")
  * [DefineMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin "vectorbtpro.utils.attr_.DefineMixin")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")
  * [Hashable](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable "vectorbtpro.utils.hashing.Hashable")



**Inherited members**

  * [AxisSpecifier.axis](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.AxisSpecifier.axis "vectorbtpro.utils.chunking.AxisSpecifier.axis")
  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.chunking.ChunkSlicer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.chunking.ChunkSlicer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.chunking.ChunkSlicer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.chunking.ChunkSlicer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.chunking.ChunkSlicer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.chunking.ChunkSlicer.find_messages")
  * [ChunkSlicer.eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.eval_id "vectorbtpro.utils.chunking.ChunkSlicer.eval_id")
  * [ChunkSlicer.fields](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields "vectorbtpro.utils.chunking.ChunkSlicer.fields")
  * [ChunkSlicer.fields_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.fields_dict "vectorbtpro.utils.chunking.ChunkSlicer.fields_dict")
  * [ChunkSlicer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.get_size "vectorbtpro.utils.chunking.ChunkSlicer.get_size")
  * [ChunkSlicer.hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash "vectorbtpro.utils.chunking.ChunkSlicer.hash")
  * [ChunkSlicer.hash_key](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.hash_key "vectorbtpro.utils.chunking.ChunkSlicer.hash_key")
  * [ChunkSlicer.ignore_none](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.ignore_none "vectorbtpro.utils.chunking.ChunkSlicer.ignore_none")
  * [ChunkSlicer.mapper](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.mapper "vectorbtpro.utils.chunking.ChunkSlicer.mapper")
  * [ChunkSlicer.single_type](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.single_type "vectorbtpro.utils.chunking.ChunkSlicer.single_type")
  * [ChunkSlicer.take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.take "vectorbtpro.utils.chunking.ChunkSlicer.take")
  * [ChunkTaker.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.apply "vectorbtpro.utils.chunking.ChunkSlicer.apply")
  * [ChunkTaker.should_take](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.should_take "vectorbtpro.utils.chunking.ChunkSlicer.should_take")
  * [ChunkTaker.suggest_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker.suggest_size "vectorbtpro.utils.chunking.ChunkSlicer.suggest_size")
  * [DefineMixin.asdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.asdict "vectorbtpro.utils.chunking.ChunkSlicer.asdict")
  * [DefineMixin.assert_field_not_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.assert_field_not_missing "vectorbtpro.utils.chunking.ChunkSlicer.assert_field_not_missing")
  * [DefineMixin.get_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.get_field "vectorbtpro.utils.chunking.ChunkSlicer.get_field")
  * [DefineMixin.is_field_missing](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_missing "vectorbtpro.utils.chunking.ChunkSlicer.is_field_missing")
  * [DefineMixin.is_field_optional](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_optional "vectorbtpro.utils.chunking.ChunkSlicer.is_field_optional")
  * [DefineMixin.is_field_required](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.is_field_required "vectorbtpro.utils.chunking.ChunkSlicer.is_field_required")
  * [DefineMixin.merge_over](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_over "vectorbtpro.utils.chunking.ChunkSlicer.merge_over")
  * [DefineMixin.merge_with](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.merge_with "vectorbtpro.utils.chunking.ChunkSlicer.merge_with")
  * [DefineMixin.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.replace "vectorbtpro.utils.chunking.ChunkSlicer.replace")
  * [DefineMixin.resolve](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve "vectorbtpro.utils.chunking.ChunkSlicer.resolve")
  * [DefineMixin.resolve_field](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.DefineMixin.resolve_field "vectorbtpro.utils.chunking.ChunkSlicer.resolve_field")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.chunking.ChunkSlicer.meets_eval_id")
  * [Hashable.get_hash](https://vectorbt.pro/pvt_7a467f6b/api/utils/hashing/#vectorbtpro.utils.hashing.Hashable.get_hash "vectorbtpro.utils.chunking.ChunkSlicer.get_hash")



**Subclasses**

  * [ArraySlicer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArraySlicer "vectorbtpro.utils.chunking.ArraySlicer")



* * *

## Sizer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L108-L123 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-86-1)Sizer()
    

Abstract class for getting the size from annotated arguments.

Note

Use [Sizer.apply](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.apply "vectorbtpro.utils.chunking.Sizer.apply") instead of [Sizer.get_size](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.get_size "vectorbtpro.utils.chunking.Sizer.get_size").

**Superclasses**

  * [Annotatable](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/#vectorbtpro.utils.annotations.Annotatable "vectorbtpro.utils.annotations.Annotatable")
  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Evaluable](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable "vectorbtpro.utils.eval_.Evaluable")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.eval_.Evaluable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.eval_.Evaluable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.eval_.Evaluable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.eval_.Evaluable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.eval_.Evaluable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.eval_.Evaluable.find_messages")
  * [Evaluable.meets_eval_id](https://vectorbt.pro/pvt_7a467f6b/api/utils/eval_/#vectorbtpro.utils.eval_.Evaluable.meets_eval_id "vectorbtpro.utils.eval_.Evaluable.meets_eval_id")



**Subclasses**

  * [ArgSizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ArgSizer "vectorbtpro.utils.chunking.ArgSizer")



* * *

### apply method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L121-L123 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.apply "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-87-1)Sizer.apply(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-87-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-87-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-87-4))
    

Apply the sizer.

* * *

### eval_id field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.eval_id "Permanent link")

One or more identifiers at which to evaluate this instance.

* * *

### get_size method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/chunking.py#L117-L119 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Sizer.get_size "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-88-1)Sizer.get_size(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-88-2)    ann_args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-88-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#__codelineno-88-4))
    

Get the size given the annotated arguments.
