# Persistence[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#persistence "Permanent link")

Any Python object can be serialized and saved to disk as a pickle file with [save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.save).

Save a dict to a file
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-0-1)cache = dict(data=data, indicator=indicator, pf=pf)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-0-2)vbt.save(cache, "cache.pickle")
 
[/code]

Important

If a file with the same name already exists, it will be overridden.


* * *

+


* * *

A pickle file can then be loaded back and deserialized with [load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.load).

Load the dict back
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-1-1)cache = vbt.load("cache.pickle")
 
[/code]

Note

The file can be read in another Python environment and even on another machine (such as in cloud), just make sure that the Python and package versions on both ends are approximately the same.


* * *

+


* * *

Pickle files usually take a considerable amount of space, to reduce it compression can be used. The most recommended compression algorithm for binary files is [blosc](https://github.com/Blosc/c-blosc). To later load the compressed file, pass the `compression` argument in the exact same way to the loader, or simply append the ".blosc" extension to the filename for the loader to recognize it automatically. The supported algorithms and their possible extensions are listed under `extensions` in [settings.pickling](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.pickling).

Specify the compression explicitly
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-2-1)vbt.save(cache, "cache.pickle", compression="blosc")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-2-2)cache = vbt.load("cache.pickle", compression="blosc")
 
[/code]

Specify the compression implicitly
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-3-1)vbt.save(cache, "cache.pickle.blosc")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-3-2)cache = vbt.load("cache.pickle.blosc")
 
[/code]


* * *

+


* * *

Those VBT objects that subclass [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable) can also be saved individually. Benefit: the name of the class and optionally the compression algorithm will be packed into the filename by default to simplify loading. The object can be loaded back using the `load()` method of the object's class.

Save a portfolio under 'Portfolio.pickle.blosc' and load it back
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-4-1)pf.save(compression="blosc")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-4-2)pf = vbt.PF.load()
 
[/code]


* * *

+


* * *

If a VBT object was saved with an older package version and upon loading with a newer version an error is thrown (for example, due to a different order of the arguments), the object can still be reconstructed by creating and registering a [RecInfo](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo) instance before loading.

Reconstruct an older BinanceData instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-1)def modify_state(rec_state): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-2) return vbt.RecState(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-3) init_args=rec_state.init_args,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-4) init_kwargs=rec_state.init_kwargs,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-5) attr_dct=rec_state.attr_dct,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-6) )
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-8)rec_info = vbt.RecInfo(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-9) vbt.get_id_from_class(vbt.BinanceData),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-10) vbt.BinanceData,
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-11) modify_state
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-12))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-13)rec_info.register()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-5-14)data = vbt.BinanceData.load()
 
[/code]

 1. 


* * *

+


* * *

If there are issues with saving an instance of a specific class, set the reconstruction id `_rec_id` with any string and then reconstruct the object using this id (first argument of `RecInfo`).

Set a custom identifier to a class and reconstruct its instance using another class
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-1)class MyClass1(vbt.Configured): 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-2) _rec_id = "MyClass"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-3) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-5)my_obj = MyClass1()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-6)vbt.save(my_obj, "my_obj")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-7)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-8)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-10)class MyClass2(vbt.Configured):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-11) ...
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-13)rec_info = vbt.RecInfo("MyClass", MyClass2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-14)rec_info.register()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/persistence/#__codelineno-6-15)my_obj = vbt.load("my_obj") 
 
[/code]

 1. 2. 3.