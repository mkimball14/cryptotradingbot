sim_range

#  sim_range module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range "Permanent link")

Mixin class for working with simulation ranges.

* * *

## SimRangeMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L30-L658 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-0-1)SimRangeMixin(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-0-2)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-0-3)    sim_end=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-0-4))
    

Mixin class for working with simulation ranges.

Should be subclassed by a subclass of [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping "vectorbtpro.base.wrapping.Wrapping").

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

  * [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio "vectorbtpro.portfolio.base.Portfolio")
  * [ReturnsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor "vectorbtpro.returns.accessors.ReturnsAccessor")



* * *

### column_stack_sim_end class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L112-L146 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.column_stack_sim_end "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-1-1)SimRangeMixin.column_stack_sim_end(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-1-2)    new_wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-1-3)    *objs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-1-4))
    

Column-stack simulation end.

* * *

### column_stack_sim_start class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L76-L110 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.column_stack_sim_start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-2-1)SimRangeMixin.column_stack_sim_start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-2-2)    new_wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-2-3)    *objs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-2-4))
    

Column-stack simulation start.

* * *

### fit_fig_to_sim_range class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L594-L658 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.fit_fig_to_sim_range "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-1)SimRangeMixin.fit_fig_to_sim_range(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-2)    fig,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-3)    column=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-4)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-5)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-6)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-7)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-8)    xref=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-3-9))
    

Fit figure to simulation range.

* * *

### get_sim_duration class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L557-L587 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_duration "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-4-1)SimRangeMixin.get_sim_duration(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-4-2)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-4-3)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-4-4)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-4-5)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-4-6)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-4-7))
    

Get duration of simulation range.

* * *

### get_sim_end class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L420-L448 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_end "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-5-1)SimRangeMixin.get_sim_end(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-5-2)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-5-3)    keep_flex=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-5-4)    allow_none=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-5-5)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-5-6)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-5-7)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-5-8))
    

Get simulation end.

* * *

### get_sim_end_index class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L501-L550 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_end_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-6-1)SimRangeMixin.get_sim_end_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-6-2)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-6-3)    allow_none=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-6-4)    inclusive=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-6-5)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-6-6)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-6-7)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-6-8))
    

Get index of simulation end.

* * *

### get_sim_start class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L385-L413 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-7-1)SimRangeMixin.get_sim_start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-7-2)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-7-3)    keep_flex=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-7-4)    allow_none=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-7-5)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-7-6)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-7-7)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-7-8))
    

Get simulation start.

* * *

### get_sim_start_index class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L455-L494 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_start_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-8-1)SimRangeMixin.get_sim_start_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-8-2)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-8-3)    allow_none=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-8-4)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-8-5)    group_by=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-8-6)    wrap_kwargs=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-8-7))
    

Get index of simulation start.

* * *

### resample_sim_end method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L212-L231 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.resample_sim_end "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-9-1)SimRangeMixin.resample_sim_end(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-9-2)    new_wrapper
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-9-3))
    

Resample simulation end.

* * *

### resample_sim_start method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L191-L210 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.resample_sim_start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-10-1)SimRangeMixin.resample_sim_start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-10-2)    new_wrapper
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-10-3))
    

Resample simulation start.

* * *

### resolve_sim_end class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L325-L383 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.resolve_sim_end "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-11-1)SimRangeMixin.resolve_sim_end(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-11-2)    sim_end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-11-3)    allow_none=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-11-4)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-11-5)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-11-6))
    

Resolve simulation end.

* * *

### resolve_sim_end_value class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L249-L263 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.resolve_sim_end_value "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-12-1)SimRangeMixin.resolve_sim_end_value(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-12-2)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-12-3)    wrapper=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-12-4))
    

Resolve a single value of simulation end.

* * *

### resolve_sim_start class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L265-L323 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.resolve_sim_start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-13-1)SimRangeMixin.resolve_sim_start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-13-2)    sim_start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-13-3)    allow_none=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-13-4)    wrapper=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-13-5)    group_by=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-13-6))
    

Resolve simulation start.

* * *

### resolve_sim_start_value class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L233-L247 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.resolve_sim_start_value "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-14-1)SimRangeMixin.resolve_sim_start_value(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-14-2)    value,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-14-3)    wrapper=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-14-4))
    

Resolve a single value of simulation start.

* * *

### row_stack_sim_end class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L55-L74 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.row_stack_sim_end "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-15-1)SimRangeMixin.row_stack_sim_end(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-15-2)    new_wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-15-3)    *objs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-15-4))
    

Row-stack simulation end.

* * *

### row_stack_sim_start class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L35-L53 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.row_stack_sim_start "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-16-1)SimRangeMixin.row_stack_sim_start(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-16-2)    new_wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-16-3)    *objs
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-16-4))
    

Row-stack simulation start.

* * *

### sim_duration class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L589-L592 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.sim_duration "Permanent link")

[SimRangeMixin.get_sim_duration](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_duration "vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_duration") with default arguments.

* * *

### sim_end class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L450-L453 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.sim_end "Permanent link")

[SimRangeMixin.get_sim_end](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_end "vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_end") with default arguments.

* * *

### sim_end_index class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L552-L555 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.sim_end_index "Permanent link")

[SimRangeMixin.get_sim_end_index](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_end_index "vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_end_index") with default arguments.

* * *

### sim_end_indexing_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L175-L189 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.sim_end_indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-17-1)SimRangeMixin.sim_end_indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-17-2)    wrapper_meta
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-17-3))
    

Indexing function for simulation end.

* * *

### sim_start class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L415-L418 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.sim_start "Permanent link")

[SimRangeMixin.get_sim_start](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_start "vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_start") with default arguments.

* * *

### sim_start_index class property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L496-L499 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.sim_start_index "Permanent link")

[SimRangeMixin.get_sim_start_index](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_start_index "vectorbtpro.generic.sim_range.SimRangeMixin.get_sim_start_index") with default arguments.

* * *

### sim_start_indexing_func method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/generic/sim_range.py#L159-L173 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#vectorbtpro.generic.sim_range.SimRangeMixin.sim_start_indexing_func "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-18-1)SimRangeMixin.sim_start_indexing_func(
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-18-2)    wrapper_meta
    [](https://vectorbt.pro/pvt_7a467f6b/api/generic/sim_range/#__codelineno-18-3))
    

Indexing function for simulation start.
