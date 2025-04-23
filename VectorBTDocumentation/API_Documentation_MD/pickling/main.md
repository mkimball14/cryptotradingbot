pickling

#  pickling module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling "Permanent link")

Utilities for pickling.

* * *

## rec_info_registry dict[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.rec_info_registry "Permanent link")

Registry with instances of [RecInfo](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo "vectorbtpro.utils.pickling.RecInfo") keyed by [RecInfo.id_](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo.id_ "vectorbtpro.utils.pickling.RecInfo.id_").

Populate with the required information if any instance cannot be unpickled.

* * *

## compress function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L71-L153 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.compress "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-0-1)compress(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-0-2)    bytes_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-0-3)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-0-4)    file_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-0-5)    **compress_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-0-6))
    

Compress bytes.

For compression options, see `extensions.compression` under [pickling](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.pickling "vectorbtpro._settings.pickling").

Keyword arguments `compress_kwargs` are passed to the [compress](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.compress "vectorbtpro.utils.pickling.compress") method of the compressing package.

* * *

## decompress function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L156-L241 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.decompress "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-1-1)decompress(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-1-2)    bytes_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-1-3)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-1-4)    file_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-1-5)    **decompress_kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-1-6))
    

Decompress bytes.

For compression options, see `extensions.compression` under [pickling](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.pickling "vectorbtpro._settings.pickling").

Keyword arguments `decompress_kwargs` are passed to the [decompress](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.decompress "vectorbtpro.utils.pickling.decompress") method of the decompressing package.

* * *

## dumps function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L244-L267 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.dumps "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-2-1)dumps(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-2-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-2-3)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-2-4)    compress_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-2-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-2-6))
    

Pickle an object to a byte stream.

Uses `dill` when available.

Compression is done with [compress](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.compress "vectorbtpro.utils.pickling.compress").

Other keyword arguments are passed to the [dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.dumps "vectorbtpro.utils.pickling.dumps") method of the pickling package.

* * *

## get_class_from_id function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L461-L470 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.get_class_from_id "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-3-1)get_class_from_id(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-3-2)    class_id
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-3-3))
    

Get the class from a class id.

* * *

## get_compression_extensions function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L60-L68 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.get_compression_extensions "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-4-1)get_compression_extensions(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-4-2)    cls_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-4-3))
    

Get all supported compression extensions from [vectorbtpro._settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/ "vectorbtpro._settings").

* * *

## get_id_from_class function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L438-L458 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.get_id_from_class "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-5-1)get_id_from_class(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-5-2)    obj
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-5-3))
    

Get the class id from a class.

If the object is an instance or a subclass of [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable") and `Pickleable._rec_id` is not None, uses the reconstruction id. Otherwise, returns the path to the class definition with [find_class](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module_.find_class "vectorbtpro.utils.module_.find_class").

* * *

## get_serialization_extensions function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L49-L57 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.get_serialization_extensions "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-6-1)get_serialization_extensions(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-6-2)    cls_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-6-3))
    

Get all supported serialization extensions from [vectorbtpro._settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/ "vectorbtpro._settings").

* * *

## load function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L383-L397 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.load "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-7-1)load(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-7-2)    path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-7-3)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-7-4)    decompress_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-7-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-7-6))
    

Read a byte stream from a file and unpickle.

Uses [load_bytes](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.load_bytes "vectorbtpro.utils.pickling.load_bytes") for reading and decompression and [loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.loads "vectorbtpro.utils.pickling.loads") for deserialization.

* * *

## load_bytes function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L339-L354 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.load_bytes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-8-1)load_bytes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-8-2)    path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-8-3)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-8-4)    decompress_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-8-5))
    

Read a byte stream from a file.

Can recognize the compression algorithm based on the extension.

* * *

## loads function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L270-L293 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.loads "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-9-1)loads(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-9-2)    bytes_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-9-3)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-9-4)    decompress_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-9-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-9-6))
    

Unpickle an object from a byte stream.

Uses `dill` when available.

Decompression is done with [decompress](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.decompress "vectorbtpro.utils.pickling.decompress").

Other keyword arguments are passed to the [loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.loads "vectorbtpro.utils.pickling.loads") method of the pickling package.

* * *

## reconstruct function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L473-L507 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.reconstruct "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-10-1)reconstruct(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-10-2)    cls,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-10-3)    rec_state
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-10-4))
    

Reconstruct an instance using a class and a reconstruction state.

* * *

## save function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L357-L380 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.save "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-11-1)save(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-11-2)    obj,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-11-3)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-11-4)    mkdir_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-11-5)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-11-6)    compress_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-11-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-11-8))
    

Pickle an object to a byte stream and write to a file.

Uses [dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.dumps "vectorbtpro.utils.pickling.dumps") for serialization and [save_bytes](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.save_bytes "vectorbtpro.utils.pickling.save_bytes") for compression and writing.

* * *

## save_bytes function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L306-L336 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.save_bytes "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-12-1)save_bytes(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-12-2)    bytes_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-12-3)    path,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-12-4)    mkdir_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-12-5)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-12-6)    compress_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-12-7))
    

Write a byte stream to a file.

Can recognize the compression algorithm based on the extension.

* * *

## suggest_compression function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L296-L303 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.suggest_compression "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-13-1)suggest_compression(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-13-2)    file_name
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-13-3))
    

Suggest compression based on the file name.

* * *

## Pickleable class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L510-L1258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-14-1)Pickleable()
    

Superclass that defines abstract properties and methods for pickle-able classes.

If any subclass cannot be pickled, override the [Pickleable.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.pickling.Pickleable.rec_state") property to return an instance of [RecState](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState "vectorbtpro.utils.pickling.RecState") to be used in reconstruction. If the class definition cannot be pickled (e.g., created dynamically), override its `_rec_id` with an arbitrary id string, dump/save the class, and before loading, map this id to the class in `rec_id_map`. This will use the mapped class to construct a new instance.

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
  * [pdict](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "vectorbtpro.utils.pickling.pdict")



* * *

### decode_config class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L720-L1010 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-1)Pickleable.decode_config(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-2)    str_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-3)    parse_literals=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-4)    run_code=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-5)    pack_objects=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-6)    use_refs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-7)    use_class_ids=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-8)    code_context=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-9)    parser_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-10)    check_type=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-11)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-15-12))
    

Decode an instance from a config string.

Can parse configs without sections. Sections can also become sub-dicts if their names use the dot notation. For example, section `a.b` will become a sub-dict of the section `a` and section `a.b.c` will become a sub-dict of the section `a.b`. You don't have to define the section `a` explicitly, it will automatically become the outermost key.

If a section contains only one pair `_ = _`, it will become an empty dict.

If `parse_literals` is True, will detect any Python literals and containers such as `True` and `[]`. Will also understand `np.nan`, `np.inf`, and `-np.inf`.

If `run_code` is True, will run any Python code prepended with `!`. Will use the context `code_context` together with already defined `np` (NumPy), `pd` (Pandas), and `vbt` (vectorbtpro).

Warning

Unpickling byte streams and running code has important security implications. Don't attempt to parse configs coming from untrusted sources as those can contain malicious code!

If `pack_objects` is True, will look for class paths prepended with `@` in section names, construct an instance of [RecState](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState "vectorbtpro.utils.pickling.RecState") (any other keyword arguments will be included to `init_kwargs`), and finally use [reconstruct](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.reconstruct "vectorbtpro.utils.pickling.reconstruct") to reconstruct the unpacked object.

If `use_refs` is True, will substitute references prepended with `&` for actual objects. Constructs a DAG using [graphlib](https://docs.python.org/3/library/graphlib.html).

If `use_class_ids` is True, will substitute any class ids prepended with `@` with the corresponding class.

Other keyword arguments are forwarded to [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.pickling.Pickleable.decode_config_node").

**Usage**

  * File `types.ini`:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-1)string = 'hello world'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-2)boolean = False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-3)int = 123
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-4)float = 123.45
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-5)exp_float = 1e-10
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-6)nan = np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-7)inf = np.inf
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-8)numpy = !np.array([1, 2, 3])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-9)pandas = !pd.Series([1, 2, 3])
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-10)expression = !dict(sub_dict2=dict(some="value"))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-16-11)mult_expression = !import math; math.floor(1.5)
    
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-3)>>> vbt.pprint(vbt.pdict.load("types.ini"))
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-4)pdict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-5)    string='hello world',
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-6)    boolean=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-7)    int=123,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-8)    float=123.45,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-9)    exp_float=1e-10,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-10)    nan=np.nan,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-11)    inf=np.inf,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-12)    numpy=<numpy.ndarray object at 0x7fe1bf84f690 of shape (3,)>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-13)    pandas=<pandas.core.series.Series object at 0x7fe1c9a997f0 of shape (3,)>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-14)    expression=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-15)        sub_dict2=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-16)            some='value'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-17)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-18)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-19)    mult_expression=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-17-20))
    

  * File `refs.ini`:


    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-1)[top]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-2)sr = &top.sr
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-3)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-4)[top.sr @pandas.Series]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-5)data = [10756.12, 10876.76, 11764.33]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-6)index = &top.sr.index
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-7)name = 'Open time'
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-8)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-9)[top.sr.index @pandas.DatetimeIndex]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-18-10)data = ["2023-01-01", "2023-01-02", "2023-01-03"]
    
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-19-1)>>> vbt.pdict.load("refs.ini")["sr"]
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-19-2)2023-01-01    10756.12
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-19-3)2023-01-02    10876.76
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-19-4)2023-01-03    11764.33
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-19-5)Name: Open time, dtype: float64
    

* * *

### decode_config_node class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L548-L551 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-20-1)Pickleable.decode_config_node(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-20-2)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-20-3)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-20-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-20-5))
    

Decode a config node.

* * *

### dumps method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L522-L532 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-21-1)Pickleable.dumps(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-21-2)    rec_state_only=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-21-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-21-4))
    

Pickle the instance to a byte stream.

Optionally, you can set `rec_state_only` to True if the instance will be later unpickled directly by the class.

* * *

### encode_config method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L553-L718 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-1)Pickleable.encode_config(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-2)    top_name=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-3)    unpack_objects=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-4)    compress_unpacked=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-5)    use_refs=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-6)    use_class_ids=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-7)    nested=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-8)    to_dict=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-9)    parser_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-10)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-22-11))
    

Encode the instance to a config string.

Based on [Pickleable.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.pickling.Pickleable.rec_state"). Raises an error if None.

Encodes to a format that is guaranteed to be parsed using [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.pickling.Pickleable.decode_config"). Otherwise, an error will be thrown. If any object cannot be represented using a string, uses [dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.dumps "vectorbtpro.utils.pickling.dumps") to convert it to a byte stream.

When `unpack_objects` is True and an object is an instance of [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable"), saves its reconstruction state to a separate section rather than the byte stream. Appends `@` and class name to the section name. If `compress_unpacked` is True, will hide keys in [RecState](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState "vectorbtpro.utils.pickling.RecState") that have empty values. Keys in [RecState](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState "vectorbtpro.utils.pickling.RecState") will be appended with `~` to avoid collision with user-defined keys having the same name.

If `use_refs` is True, out of unhashable objects sharing the same id, only the first one will be defined while others will store the reference (`&` \+ key path) to the first one.

Note

The initial order of keys can be preserved only by using references.

If `use_class_ids` is True, substitutes any class defined as a value by its id instead of pickling its definition. If [get_id_from_class](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.get_id_from_class "vectorbtpro.utils.pickling.get_id_from_class") returns None, will pickle the definition.

If the instance is nested, set `nested` to True to represent each sub-dict as a section.

Other keyword arguments are forwarded to [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.pickling.Pickleable.encode_config_node").

* * *

### encode_config_node method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L544-L546 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-23-1)Pickleable.encode_config_node(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-23-2)    key,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-23-3)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-23-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-23-5))
    

Encode a config node.

* * *

### file_exists class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1157-L1166 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-24-1)Pickleable.file_exists(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-24-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-24-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-24-4))
    

Return whether a file already exists.

Resolves the file path using [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.pickling.Pickleable.resolve_file_path").

* * *

### getsize method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1233-L1237 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-25-1)Pickleable.getsize(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-25-2)    readable=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-25-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-25-4))
    

Get size of this object.

* * *

### load class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1202-L1228 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-26-1)Pickleable.load(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-26-2)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-26-3)    file_format=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-26-4)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-26-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-26-6))
    

Unpickle/decode the instance from a file.

Resolves the file path using [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.pickling.Pickleable.resolve_file_path").

* * *

### loads class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L534-L542 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-27-1)Pickleable.loads(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-27-2)    bytes_,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-27-3)    check_type=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-27-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-27-5))
    

Unpickle an instance from a byte stream.

* * *

### modify_state class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1244-L1247 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-28-1)Pickleable.modify_state(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-28-2)    rec_state
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-28-3))
    

Modify the reconstruction state before reconstruction.

* * *

### rec_state class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1239-L1242 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "Permanent link")

Reconstruction state of the type [RecState](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState "vectorbtpro.utils.pickling.RecState").

* * *

### resolve_file_path class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1012-L1155 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-29-1)Pickleable.resolve_file_path(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-29-2)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-29-3)    file_format=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-29-4)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-29-5)    for_save=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-29-6))
    

Resolve a file path.

A file must have either one or two extensions: file format (required) and compression (optional). For file format options, see `pickle_extensions` and `config_extensions`. For compression options, see `compression_extensions`. Each can be provided either via a suffix in `path`, or via the argument `file_format` and `compression` respectively.

When saving, uses `file_format` and `compression` from [pickling](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.pickling "vectorbtpro._settings.pickling") as default options. When loading, searches for matching files in the current directory.

Path can be also None or directory, in such a case the file name will be set to the class name.

* * *

### save method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1168-L1200 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-30-1)Pickleable.save(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-30-2)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-30-3)    file_format=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-30-4)    compression=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-30-5)    mkdir_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-30-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-30-7))
    

Pickle/encode the instance and save to a file.

Resolves the file path using [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.pickling.Pickleable.resolve_file_path").

* * *

## RecInfo class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L414-L429 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-31-1)RecInfo(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-31-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-31-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-31-4))
    

Class that represents information needed to reconstruct an instance.

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

### cls field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo.cls "Permanent link")

Class.

* * *

### id_ field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo.id_ "Permanent link")

Identifier.

* * *

### modify_state field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo.modify_state "Permanent link")

Callback to modify the reconstruction state.

* * *

### register method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L427-L429 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecInfo.register "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-32-1)RecInfo.register()
    

Register self in [rec_info_registry](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.rec_info_registry "vectorbtpro.utils.pickling.rec_info_registry").

* * *

## RecState class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L400-L411 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-33-1)RecState(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-33-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-33-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-33-4))
    

Class that represents a state used to reconstruct an instance.

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

### attr_dct field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState.attr_dct "Permanent link")

Dictionary with names and values of writeable attributes.

* * *

### init_args field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState.init_args "Permanent link")

Positional arguments used in initialization.

* * *

### init_kwargs field[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState.init_kwargs "Permanent link")

Keyword arguments used in initialization.

* * *

## pdict class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1264-L1313 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-34-1)pdict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-34-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-34-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-34-4))
    

Pickleable dict.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")
  * `builtins.dict`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.checks.Comparable.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.checks.Comparable.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.checks.Comparable.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.checks.Comparable.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.checks.Comparable.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.checks.Comparable.find_messages")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.utils.pickling.Pickleable.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.utils.pickling.Pickleable.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.utils.pickling.Pickleable.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.utils.pickling.Pickleable.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.utils.pickling.Pickleable.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.utils.pickling.Pickleable.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.utils.pickling.Pickleable.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.utils.pickling.Pickleable.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.utils.pickling.Pickleable.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.utils.pickling.Pickleable.modify_state")
  * [Pickleable.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.utils.pickling.Pickleable.rec_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.utils.pickling.Pickleable.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.utils.pickling.Pickleable.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.utils.formatting.Prettified.pprint")
  * [Prettified.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.utils.formatting.Prettified.prettify")



**Subclasses**

  * [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config "vectorbtpro.utils.config.Config")
  * [atomic_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.atomic_dict "vectorbtpro.utils.config.atomic_dict")
  * [child_dict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.child_dict "vectorbtpro.utils.config.child_dict")
  * [index_dict](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.index_dict "vectorbtpro.base.indexing.index_dict")
  * [key_dict](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.key_dict "vectorbtpro.data.base.key_dict")
  * [pfopt_func_dict](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.pfopt_func_dict "vectorbtpro.portfolio.pfopt.base.pfopt_func_dict")
  * [run_arg_dict](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.run_arg_dict "vectorbtpro.data.base.run_arg_dict")
  * [run_func_dict](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.run_func_dict "vectorbtpro.data.base.run_func_dict")



* * *

### equals method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1284-L1307 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.equals "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-35-1)pdict.equals(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-35-2)    other,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-35-3)    check_types=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-35-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-35-5))
    

Check two objects for equality.

* * *

### load_update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pickling.py#L1267-L1271 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.pdict.load_update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-36-1)pdict.load_update(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-36-2)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-36-3)    clear=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-36-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#__codelineno-36-5))
    

Load dumps from a file and update this instance in-place.
