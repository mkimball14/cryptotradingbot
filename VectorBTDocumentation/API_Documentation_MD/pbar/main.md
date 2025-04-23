pbar

#  pbar module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar "Permanent link")

Utilities for progress bars.

* * *

## with_progress_hidden function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L601-L616 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.with_progress_hidden "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-0-1)with_progress_hidden(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-0-2)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-0-3))
    

Decorator to run a function with [ProgressHidden](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressHidden "vectorbtpro.utils.pbar.ProgressHidden").

* * *

## with_progress_shown function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L669-L684 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.with_progress_shown "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-1-1)with_progress_shown(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-1-2)    *args
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-1-3))
    

Decorator to run a function with [ProgressShown](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressShown "vectorbtpro.utils.pbar.ProgressShown").

* * *

## ProgressBar class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L35-L548 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-1)ProgressBar(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-2)    iterable=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-3)    bar_id=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-4)    bar_type=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-5)    force_open_bar=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-6)    reuse=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-7)    disable=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-8)    show_progress=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-9)    show_progress_desc=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-10)    prefix=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-11)    postfix=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-12)    desc_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-13)    registry=<vectorbtpro.registries.pbar_registry.PBarRegistry object>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-14)    silence_warnings=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-15)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-2-16))
    

Context manager to manage a progress bar.

Supported types:

  * 'tqdm_auto'
  * 'tqdm_notebook'
  * 'tqdm_gui'
  * 'tqdm'



For defaults, see [pbar](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.pbar "vectorbtpro._settings.pbar").

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

### active class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L290-L293 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.active "Permanent link")

Whether the bar is active.

* * *

### after_update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L374-L377 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.after_update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-3-1)ProgressBar.after_update()
    

Do something after an update.

* * *

### bar class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L189-L192 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.bar "Permanent link")

Bar.

* * *

### bar_id class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L132-L135 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.bar_id "Permanent link")

Bar id.

* * *

### bar_type class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L137-L140 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.bar_type "Permanent link")

Bar type.

* * *

### before_update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L347-L357 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.before_update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-4-1)ProgressBar.before_update()
    

Do something before an update.

* * *

### close method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L266-L288 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.close "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-5-1)ProgressBar.close(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-5-2)    reuse=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-5-3)    close_children=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-5-4))
    

Close the bar.

* * *

### close_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L209-L212 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.close_time "Permanent link")

Time the bar was closed.

* * *

### desc_kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L172-L175 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.desc_kwargs "Permanent link")

Keyword arguments passed to [ProgressBar.set_description](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_description "vectorbtpro.utils.pbar.ProgressBar.set_description").

* * *

### disabled class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L300-L316 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.disabled "Permanent link")

Whether the bar is disabled.

* * *

### displayed class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L318-L328 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.displayed "Permanent link")

Whether the bar is displayed.

* * *

### enter method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L504-L508 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.enter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-6-1)ProgressBar.enter(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-6-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-6-3))
    

Enter the bar.

* * *

### exit method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L513-L515 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.exit "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-7-1)ProgressBar.exit(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-7-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-7-3))
    

Exit the bar.

* * *

### force_open_bar class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L142-L145 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.force_open_bar "Permanent link")

Whether to force-open a bar even if progress is not shown.

* * *

### format_num class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L379-L384 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.format_num "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-8-1)ProgressBar.format_num(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-8-2)    n
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-8-3))
    

Format a number.

* * *

### iter method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L526-L529 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.iter "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-9-1)ProgressBar.iter()
    

Get iterator over [ProgressBar.iterable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.iterable "vectorbtpro.utils.pbar.ProgressBar.iterable").

* * *

### iterable class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L157-L160 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.iterable "Permanent link")

Iterable.

* * *

### kwargs class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L162-L165 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.kwargs "Permanent link")

Keyword arguments passed to initialize the bar.

* * *

### open method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L233-L264 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.open "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-10-1)ProgressBar.open(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-10-2)    reuse=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-10-3))
    

Open the bar.

* * *

### open_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L194-L197 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.open_time "Permanent link")

Time the bar was opened.

* * *

### pending class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L295-L298 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.pending "Permanent link")

Whether the bar is pending.

* * *

### prepare_desc class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L386-L414 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.prepare_desc "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-11-1)ProgressBar.prepare_desc(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-11-2)    desc
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-11-3))
    

Prepare description.

* * *

### refresh method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L342-L345 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.refresh "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-12-1)ProgressBar.refresh()
    

Refresh the bar.

* * *

### refresh_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L204-L207 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.refresh_time "Permanent link")

Time the bar was refreshed.

* * *

### registry class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L177-L182 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.registry "Permanent link")

Registry of type [PBarRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/pbar_registry/#vectorbtpro.registries.pbar_registry.PBarRegistry "vectorbtpro.registries.pbar_registry.PBarRegistry").

If None, registry is disabled.

* * *

### remove_bar method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L220-L222 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.remove_bar "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-13-1)ProgressBar.remove_bar()
    

Remove the bar.

* * *

### reset method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L224-L231 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.reset "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-14-1)ProgressBar.reset()
    

Reset the bar.

* * *

### reuse class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L147-L150 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.reuse "Permanent link")

Whether the bar can be reused.

* * *

### set_bar method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L214-L218 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_bar "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-15-1)ProgressBar.set_bar(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-15-2)    bar=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-15-3))
    

Set the bar.

* * *

### set_description method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L462-L481 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_description "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-16-1)ProgressBar.set_description(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-16-2)    desc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-16-3)    as_postfix=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-16-4)    refresh=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-16-5))
    

Set description.

Uses the method [ProgressBar.set_prefix](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_prefix "vectorbtpro.utils.pbar.ProgressBar.set_prefix") if `as_postfix=True` in [ProgressBar.desc_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.desc_kwargs "vectorbtpro.utils.pbar.ProgressBar.desc_kwargs"). Otherwise, uses the method [ProgressBar.set_postfix](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_postfix "vectorbtpro.utils.pbar.ProgressBar.set_postfix").

Uses [ProgressBar.desc_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.desc_kwargs "vectorbtpro.utils.pbar.ProgressBar.desc_kwargs") as keyword arguments.

* * *

### set_description_str method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L483-L502 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_description_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-17-1)ProgressBar.set_description_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-17-2)    desc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-17-3)    as_postfix=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-17-4)    refresh=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-17-5))
    

Set description without preparation.

Uses the method [ProgressBar.set_prefix_str](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_prefix_str "vectorbtpro.utils.pbar.ProgressBar.set_prefix_str") if `as_postfix=True` in [ProgressBar.desc_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.desc_kwargs "vectorbtpro.utils.pbar.ProgressBar.desc_kwargs"). Otherwise, uses the method [ProgressBar.set_postfix_str](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_postfix_str "vectorbtpro.utils.pbar.ProgressBar.set_postfix_str").

Uses [ProgressBar.desc_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.desc_kwargs "vectorbtpro.utils.pbar.ProgressBar.desc_kwargs") as keyword arguments.

* * *

### set_postfix method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L439-L450 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_postfix "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-18-1)ProgressBar.set_postfix(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-18-2)    desc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-18-3)    refresh=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-18-4))
    

Set postfix.

Prepares it with [ProgressBar.prepare_desc](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.prepare_desc "vectorbtpro.utils.pbar.ProgressBar.prepare_desc").

* * *

### set_postfix_str method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L452-L460 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_postfix_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-19-1)ProgressBar.set_postfix_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-19-2)    desc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-19-3)    refresh=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-19-4))
    

Set postfix without preparation.

* * *

### set_prefix method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L416-L427 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_prefix "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-20-1)ProgressBar.set_prefix(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-20-2)    desc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-20-3)    refresh=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-20-4))
    

Set prefix.

Prepares it with [ProgressBar.prepare_desc](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.prepare_desc "vectorbtpro.utils.pbar.ProgressBar.prepare_desc").

* * *

### set_prefix_str method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L429-L437 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.set_prefix_str "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-21-1)ProgressBar.set_prefix_str(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-21-2)    desc,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-21-3)    refresh=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-21-4))
    

Set prefix without preparation.

* * *

### should_display class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L330-L340 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.should_display "Permanent link")

Whether the bar should be displayed.

* * *

### show_progress class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L152-L155 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.show_progress "Permanent link")

Whether to show the bar.

* * *

### show_progress_desc class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L167-L170 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.show_progress_desc "Permanent link")

Whether show the bar description.

* * *

### silence_warnings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L184-L187 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.silence_warnings "Permanent link")

Whether to silence warnings.

* * *

### update method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L359-L366 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.update "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-22-1)ProgressBar.update(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-22-2)    n=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-22-3))
    

Update with one or more iterations.

* * *

### update_time class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L199-L202 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.update_time "Permanent link")

Time the bar was updated.

* * *

### update_to method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L368-L372 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar.update_to "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-23-1)ProgressBar.update_to(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-23-2)    n
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-23-3))
    

Update to a specific number.

* * *

## ProgressHidden class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L551-L598 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressHidden "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-24-1)ProgressHidden(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-24-2)    disable_registry=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-24-3)    disable_machinery=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-24-4))
    

Context manager to hide progress.

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

### disable_machinery class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L564-L567 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressHidden.disable_machinery "Permanent link")

Whether to disable machinery.

* * *

### disable_registry class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L559-L562 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressHidden.disable_registry "Permanent link")

Whether to disable registry.

* * *

### init_settings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L569-L572 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressHidden.init_settings "Permanent link")

Initial settings.

* * *

## ProgressShown class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L619-L666 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressShown "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-25-1)ProgressShown(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-25-2)    enable_registry=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-25-3)    enable_machinery=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#__codelineno-25-4))
    

Context manager to show progress.

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

### enable_machinery class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L632-L635 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressShown.enable_machinery "Permanent link")

Whether to enable machinery.

* * *

### enable_registry class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L627-L630 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressShown.enable_registry "Permanent link")

Whether to enable registry.

* * *

### init_settings class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/pbar.py#L637-L640 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressShown.init_settings "Permanent link")

Initial settings.
