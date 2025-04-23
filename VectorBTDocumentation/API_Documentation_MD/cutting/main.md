cutting

#  cutting module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/cutting.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting "Permanent link")

Utilities for cutting code.

* * *

## collect_blocks function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/cutting.py#L28-L46 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.collect_blocks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-0-1)collect_blocks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-0-2)    lines
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-0-3))
    

Collect blocks in the lines.

* * *

## cut_and_save function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/cutting.py#L207-L221 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.cut_and_save "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-1-1)cut_and_save(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-1-2)    code,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-1-3)    section_name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-1-4)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-1-5)    mkdir_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-1-6)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-1-7))
    

Cut an annotated section from the code and save to a file.

For arguments see [cut_from_code](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.cut_from_code "vectorbtpro.utils.cutting.cut_from_code").

* * *

## cut_and_save_func function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/cutting.py#L234-L244 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.cut_and_save_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-2-1)cut_and_save_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-2-2)    func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-2-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-2-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-2-5))
    

Cut an annotated function section from a module and save to a file.

For arguments see [cut_and_save](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.cut_and_save "vectorbtpro.utils.cutting.cut_and_save").

* * *

## cut_and_save_module function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/cutting.py#L224-L231 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.cut_and_save_module "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-3-1)cut_and_save_module(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-3-2)    module,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-3-3)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-3-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-3-5))
    

Cut an annotated section from a module and save to a file.

For arguments see [cut_and_save](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.cut_and_save "vectorbtpro.utils.cutting.cut_and_save").

* * *

## cut_from_code function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/cutting.py#L49-L186 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.cut_from_code "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-1)cut_from_code(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-2)    code,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-3)    section_name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-4)    prepend_lines=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-5)    append_lines=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-6)    out_lines_callback=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-7)    return_lines=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-8)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-4-9))
    

Parse and cut an annotated section from the code.

The section should start with `# % <section section_name>` and end with `# % </section>`.

You can also define blocks. Each block should start with `# % <block block_name>` and end with `# % </block>`. Blocks will be collected into the dictionary `blocks` before cutting and can be then inserted using Python expressions (see below).

To skip multiple lines of code, place them between `# % <skip [expression]>` and `# % </skip>`, where expression is optional.

To uncomment multiple lines of code, place them between `# % <uncomment [expression]>` and `# % </uncomment>`, where expression is optional.

Everything else after `# %` will be evaluated as a Python expression and should return either None (= skip), a string (= insert one line of code) or an iterable of strings (= insert multiple lines of code). The latter will be appended to the queue and parsed.

Every expression is evaluated strictly, that is, any evaluation error will raise an error and stop the program. To evaluate softly without raising any errors, prepend `?`. The context includes `lines`, `blocks`, `section_name`, `line`, `out_lines`, and `**kwargs`.

* * *

## suggest_module_path function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/cutting.py#L189-L204 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#vectorbtpro.utils.cutting.suggest_module_path "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-5-1)suggest_module_path(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-5-2)    section_name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-5-3)    path=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-5-4)    mkdir_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/#__codelineno-5-5))
    

Suggest a path to the target file.
