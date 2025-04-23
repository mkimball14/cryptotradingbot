preparing

#  preparing module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing "Permanent link")

Classes for preparing portfolio simulations.

* * *

## base_arg_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.base_arg_config "Permanent link")

Argument config for [BasePFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer "vectorbtpro.portfolio.preparing.BasePFPreparer").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-2)    data=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-3)    open=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-4)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-5)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-6)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-7)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-8)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-9)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-10)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-11)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-12)    high=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-13)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-14)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-15)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-16)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-17)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-18)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-19)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-21)    low=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-22)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-23)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-24)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-25)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-26)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-27)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-28)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-29)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-30)    close=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-31)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-32)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-33)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-34)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-35)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-36)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-37)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-38)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-39)    bm_close=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-40)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-41)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-42)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-43)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-44)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-45)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-46)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-47)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-48)    cash_earnings=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-49)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-50)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-51)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-52)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-53)                fill_value=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-54)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-55)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-56)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-57)    init_cash=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-58)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-59)            enum=InitCashModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-60)                Auto=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-61)                AutoAlign=-2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-62)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-63)            look_for_type=<class 'str'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-64)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-65)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-66)    init_position=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-67)    init_price=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-68)    cash_deposits=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-69)    group_by=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-70)    cash_sharing=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-71)    freq=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-72)    sim_start=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-73)    sim_end=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-74)    call_seq=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-75)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-76)            enum=CallSeqTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-77)                Default=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-78)                Reversed=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-79)                Random=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-80)                Auto=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-81)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-82)            look_for_type=<class 'str'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-83)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-84)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-85)    attach_call_seq=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-86)    keep_inout_flex=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-87)    in_outputs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-88)        has_default=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-89)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-0-90))
    

* * *

## fdof_arg_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.fdof_arg_config "Permanent link")

Argument config for [FDOFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer "vectorbtpro.portfolio.preparing.FDOFPreparer").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-2)    val_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-3)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-4)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-5)            enum=ValPriceTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-6)                Latest=-np.inf,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-7)                Price=np.inf
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-8)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-9)            ignore_type=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-10)                <class 'int'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-11)                <class 'float'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-12)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-13)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-14)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-15)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-16)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-17)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-18)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-19)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-20)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-21)    flexible=dict()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-1-22))
    

* * *

## fo_arg_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.fo_arg_config "Permanent link")

Argument config for [FOPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer "vectorbtpro.portfolio.preparing.FOPreparer").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-2)    cash_dividends=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-3)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-4)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-5)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-6)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-7)                fill_value=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-8)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-9)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-10)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-11)    val_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-12)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-13)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-14)            enum=ValPriceTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-15)                Latest=-np.inf,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-16)                Price=np.inf
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-17)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-18)            ignore_type=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-19)                <class 'int'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-20)                <class 'float'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-21)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-22)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-23)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-24)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-25)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-26)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-27)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-28)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-29)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-30)    from_ago=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-31)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-32)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-33)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-34)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-35)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-36)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-37)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-38)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-39)    ffill_val_price=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-40)    update_value=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-41)    save_state=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-42)    save_value=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-43)    save_returns=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-44)    skip_empty=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-45)    max_order_records=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-46)    max_log_records=dict()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-2-47))
    

* * *

## fof_arg_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.fof_arg_config "Permanent link")

Argument config for [FOFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer "vectorbtpro.portfolio.preparing.FOFPreparer").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-2)    segment_mask=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-3)    call_pre_segment=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-4)    call_post_segment=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-5)    pre_sim_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-6)    pre_sim_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-7)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-8)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-9)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-10)    post_sim_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-11)    post_sim_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-12)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-13)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-14)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-15)    pre_group_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-16)    pre_group_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-17)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-18)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-19)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-20)    post_group_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-21)    post_group_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-22)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-23)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-24)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-25)    pre_row_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-26)    pre_row_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-27)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-28)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-29)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-30)    post_row_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-31)    post_row_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-32)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-33)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-35)    pre_segment_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-36)    pre_segment_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-37)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-38)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-39)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-40)    post_segment_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-41)    post_segment_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-42)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-43)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-44)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-45)    order_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-46)    order_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-47)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-48)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-49)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-50)    flex_order_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-51)    flex_order_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-52)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-53)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-54)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-55)    post_order_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-56)    post_order_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-57)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-58)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-59)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-60)    ffill_val_price=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-61)    update_value=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-62)    fill_pos_info=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-63)    track_value=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-64)    row_wise=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-65)    max_order_records=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-66)    max_log_records=dict()
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-3-67))
    

* * *

## fs_arg_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.fs_arg_config "Permanent link")

Argument config for [FSPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer "vectorbtpro.portfolio.preparing.FSPreparer").
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-2)    size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-3)        fill_default=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-4)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-5)    cash_dividends=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-6)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-7)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-8)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-9)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-10)                fill_value=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-11)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-12)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-13)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-14)    entries=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-15)        has_default=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-16)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-17)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-18)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-19)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-20)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-21)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-22)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-23)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-24)    exits=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-25)        has_default=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-26)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-27)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-28)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-29)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-30)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-31)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-32)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-33)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-34)    long_entries=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-35)        has_default=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-36)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-37)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-38)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-39)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-40)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-41)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-42)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-43)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-44)    long_exits=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-45)        has_default=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-46)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-47)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-48)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-49)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-50)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-51)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-52)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-53)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-54)    short_entries=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-55)        has_default=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-56)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-57)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-58)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-59)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-60)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-61)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-62)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-63)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-64)    short_exits=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-65)        has_default=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-66)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-67)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-68)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-69)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-70)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-71)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-72)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-73)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-74)    adjust_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-75)    adjust_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-76)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-77)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-78)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-79)    signal_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-80)    signal_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-81)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-82)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-83)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-84)    post_signal_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-85)    post_signal_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-86)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-87)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-88)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-89)    post_segment_func_nb=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-90)    post_segment_args=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-91)        type='args',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-92)        substitute_templates=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-93)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-94)    order_mode=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-95)    val_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-96)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-97)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-98)            enum=ValPriceTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-99)                Latest=-np.inf,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-100)                Price=np.inf
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-101)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-102)            ignore_type=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-103)                <class 'int'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-104)                <class 'float'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-105)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-106)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-107)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-108)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-109)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-110)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-111)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-112)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-113)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-114)    accumulate=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-115)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-116)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-117)            enum=AccumulationModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-118)                Disabled=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-119)                Both=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-120)                AddOnly=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-121)                RemoveOnly=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-122)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-123)            ignore_type=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-124)                <class 'int'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-125)                <class 'bool'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-126)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-127)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-128)        subdtype=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-129)            <class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-130)            <class 'numpy.bool_'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-131)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-132)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-133)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-134)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-135)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-136)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-137)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-138)    upon_long_conflict=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-139)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-140)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-141)            enum=ConflictModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-142)                Ignore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-143)                Entry=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-144)                Exit=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-145)                Adjacent=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-146)                Opposite=4
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-147)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-148)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-149)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-150)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-151)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-152)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-153)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-154)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-155)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-156)    upon_short_conflict=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-157)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-158)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-159)            enum=ConflictModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-160)                Ignore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-161)                Entry=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-162)                Exit=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-163)                Adjacent=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-164)                Opposite=4
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-165)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-166)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-167)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-168)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-169)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-170)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-171)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-172)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-173)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-174)    upon_dir_conflict=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-175)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-176)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-177)            enum=DirectionConflictModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-178)                Ignore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-179)                Long=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-180)                Short=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-181)                Adjacent=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-182)                Opposite=4
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-183)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-184)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-185)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-186)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-187)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-188)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-189)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-190)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-191)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-192)    upon_opposite_entry=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-193)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-194)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-195)            enum=OppositeEntryModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-196)                Ignore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-197)                Close=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-198)                CloseReduce=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-199)                Reverse=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-200)                ReverseReduce=4
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-201)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-202)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-203)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-204)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-205)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-206)                fill_value=4
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-207)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-208)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-209)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-210)    order_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-211)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-212)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-213)            enum=OrderTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-214)                Market=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-215)                Limit=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-216)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-217)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-218)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-219)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-220)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-221)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-222)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-223)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-224)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-225)    limit_delta=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-226)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-227)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-228)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-229)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-230)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-231)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-232)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-233)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-234)    limit_tif=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-235)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-236)        is_td=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-237)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-238)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-239)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-240)                fill_value=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-241)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-242)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-243)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-244)    limit_expiry=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-245)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-246)        is_dt=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-247)        last_before=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-248)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-249)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-250)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-251)                fill_value=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-252)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-253)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-254)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-255)    limit_reverse=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-256)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-257)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-258)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-259)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-260)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-261)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-262)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-263)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-264)    limit_order_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-265)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-266)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-267)            enum=LimitOrderPriceT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-268)                Limit=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-269)                HardLimit=-2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-270)                Close=-3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-271)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-272)            ignore_type=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-273)                <class 'int'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-274)                <class 'float'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-275)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-276)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-277)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-278)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-279)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-280)                fill_value=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-281)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-282)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-283)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-284)    upon_adj_limit_conflict=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-285)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-286)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-287)            enum=PendingConflictModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-288)                KeepIgnore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-289)                KeepExecute=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-290)                CancelIgnore=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-291)                CancelExecute=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-292)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-293)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-294)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-295)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-296)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-297)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-298)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-299)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-300)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-301)    upon_opp_limit_conflict=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-302)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-303)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-304)            enum=PendingConflictModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-305)                KeepIgnore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-306)                KeepExecute=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-307)                CancelIgnore=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-308)                CancelExecute=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-309)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-310)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-311)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-312)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-313)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-314)                fill_value=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-315)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-316)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-317)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-318)    use_stops=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-319)    stop_ladder=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-320)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-321)            enum=StopLadderModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-322)                Disabled=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-323)                Uniform=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-324)                Weighted=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-325)                AdaptUniform=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-326)                AdaptWeighted=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-327)                Dynamic=5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-328)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-329)            look_for_type=<class 'str'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-330)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-331)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-332)    sl_stop=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-333)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-334)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-335)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-336)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-337)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-338)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-339)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-340)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-341)    tsl_stop=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-342)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-343)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-344)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-345)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-346)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-347)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-348)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-349)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-350)    tsl_th=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-351)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-352)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-353)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-354)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-355)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-356)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-357)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-358)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-359)    tp_stop=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-360)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-361)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-362)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-363)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-364)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-365)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-366)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-367)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-368)    td_stop=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-369)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-370)        is_td=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-371)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-372)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-373)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-374)                fill_value=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-375)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-376)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-377)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-378)    dt_stop=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-379)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-380)        is_dt=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-381)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-382)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-383)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-384)                fill_value=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-385)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-386)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-387)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-388)    stop_entry_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-389)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-390)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-391)            enum=StopEntryPriceT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-392)                ValPrice=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-393)                Open=-2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-394)                Price=-3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-395)                FillPrice=-4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-396)                Close=-5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-397)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-398)            ignore_type=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-399)                <class 'int'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-400)                <class 'float'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-401)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-402)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-403)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-404)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-405)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-406)                fill_value=-5
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-407)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-408)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-409)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-410)    stop_exit_price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-411)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-412)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-413)            enum=StopExitPriceT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-414)                Stop=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-415)                HardStop=-2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-416)                Close=-3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-417)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-418)            ignore_type=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-419)                <class 'int'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-420)                <class 'float'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-421)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-422)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-423)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-424)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-425)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-426)                fill_value=-1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-427)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-428)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-429)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-430)    stop_exit_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-431)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-432)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-433)            enum=StopExitTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-434)                Close=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-435)                CloseReduce=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-436)                Reverse=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-437)                ReverseReduce=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-438)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-439)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-440)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-441)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-442)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-443)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-444)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-445)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-446)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-447)    stop_order_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-448)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-449)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-450)            enum=OrderTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-451)                Market=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-452)                Limit=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-453)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-454)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-455)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-456)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-457)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-458)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-459)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-460)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-461)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-462)    stop_limit_delta=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-463)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-464)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-465)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-466)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-467)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-468)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-469)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-470)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-471)    upon_stop_update=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-472)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-473)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-474)            enum=StopUpdateModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-475)                Keep=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-476)                Override=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-477)                OverrideNaN=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-478)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-479)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-480)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-481)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-482)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-483)                fill_value=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-484)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-485)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-486)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-487)    upon_adj_stop_conflict=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-488)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-489)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-490)            enum=PendingConflictModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-491)                KeepIgnore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-492)                KeepExecute=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-493)                CancelIgnore=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-494)                CancelExecute=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-495)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-496)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-497)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-498)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-499)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-500)                fill_value=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-501)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-502)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-503)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-504)    upon_opp_stop_conflict=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-505)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-506)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-507)            enum=PendingConflictModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-508)                KeepIgnore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-509)                KeepExecute=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-510)                CancelIgnore=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-511)                CancelExecute=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-512)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-513)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-514)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-515)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-516)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-517)                fill_value=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-518)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-519)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-520)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-521)    delta_format=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-522)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-523)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-524)            enum=DeltaFormatT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-525)                Absolute=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-526)                Percent=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-527)                Percent100=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-528)                Target=3
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-529)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-530)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-531)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-532)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-533)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-534)                fill_value=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-535)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-536)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-537)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-538)    time_delta_format=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-539)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-540)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-541)            enum=TimeDeltaFormatT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-542)                Rows=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-543)                Index=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-544)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-545)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-546)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-547)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-548)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-549)                fill_value=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-550)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-551)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-552)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-553)    from_ago=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-554)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-555)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-556)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-557)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-558)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-559)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-560)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-561)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-562)    ffill_val_price=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-563)    update_value=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-564)    fill_pos_info=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-565)    save_state=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-566)    save_value=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-567)    save_returns=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-568)    skip_empty=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-569)    max_order_records=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-570)    max_log_records=dict(),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-571)    records=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-572)        rename_fields=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-573)            entry='entries',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-574)            exit='exits',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-575)            long_entry='long_entries',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-576)            long_exit='long_exits',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-577)            short_entry='short_entries',
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-578)            short_exit='short_exits'
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-579)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-580)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-4-581))
    

* * *

## order_arg_config ReadonlyConfig[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.order_arg_config "Permanent link")

Argument config for order-related information.
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-1)ReadonlyConfig(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-2)    size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-3)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-4)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-5)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-6)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-7)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-8)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-9)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-10)        fill_default=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-11)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-12)    price=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-13)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-14)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-15)            enum=PriceTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-16)                Open=-np.inf,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-17)                Close=np.inf,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-18)                NextOpen=-1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-19)                NextClose=-2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-20)                NextValidOpen=-3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-21)                NextValidClose=-4
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-22)            ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-23)            ignore_type=(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-24)                <class 'int'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-25)                <class 'float'>
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-26)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-27)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-28)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-29)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-30)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-31)                fill_value=np.inf
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-32)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-33)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-34)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-35)    size_type=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-36)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-37)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-38)            enum=SizeTypeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-39)                Amount=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-40)                Value=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-41)                Percent=2,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-42)                Percent100=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-43)                ValuePercent=4,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-44)                ValuePercent100=5,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-45)                TargetAmount=6,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-46)                TargetValue=7,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-47)                TargetPercent=8,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-48)                TargetPercent100=9
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-49)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-50)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-51)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-52)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-53)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-54)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-55)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-56)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-57)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-58)    direction=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-59)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-60)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-61)            enum=DirectionT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-62)                LongOnly=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-63)                ShortOnly=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-64)                Both=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-65)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-66)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-67)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-68)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-69)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-70)                fill_value=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-71)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-72)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-73)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-74)    fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-75)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-76)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-77)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-78)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-79)                fill_value=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-80)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-81)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-82)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-83)    fixed_fees=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-84)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-85)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-86)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-87)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-88)                fill_value=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-89)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-90)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-91)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-92)    slippage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-93)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-94)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-95)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-96)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-97)                fill_value=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-98)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-99)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-100)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-101)    min_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-102)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-103)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-104)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-105)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-106)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-107)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-108)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-109)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-110)    max_size=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-111)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-112)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-113)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-114)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-115)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-116)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-117)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-118)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-119)    size_granularity=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-120)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-121)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-122)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-123)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-124)                fill_value=np.nan
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-125)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-126)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-127)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-128)    leverage=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-129)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-130)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-131)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-132)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-133)                fill_value=1.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-134)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-135)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-136)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-137)    leverage_mode=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-138)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-139)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-140)            enum=LeverageModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-141)                Lazy=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-142)                Eager=1
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-143)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-144)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-145)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-146)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-147)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-148)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-149)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-150)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-151)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-152)    reject_prob=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-153)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-154)        subdtype=<class 'numpy.number'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-155)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-156)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-157)                fill_value=0.0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-158)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-159)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-160)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-161)    price_area_vio_mode=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-162)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-163)        map_enum_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-164)            enum=PriceAreaVioModeT(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-165)                Ignore=0,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-166)                Cap=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-167)                Error=2
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-168)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-169)        ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-170)        subdtype=<class 'numpy.integer'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-171)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-172)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-173)                fill_value=0
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-174)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-175)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-176)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-177)    allow_partial=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-178)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-179)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-180)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-181)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-182)                fill_value=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-183)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-184)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-185)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-186)    raise_reject=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-187)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-188)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-189)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-190)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-191)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-192)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-193)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-194)    ),
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-195)    log=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-196)        broadcast=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-197)        subdtype=<class 'numpy.bool_'>,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-198)        broadcast_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-199)            reindex_kwargs=dict(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-200)                fill_value=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-201)            )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-202)        )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-203)    )
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-5-204))
    

* * *

## valid_price_from_ago_1d_nb function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L53-L65 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.valid_price_from_ago_1d_nb "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-6-1)valid_price_from_ago_1d_nb(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-6-2)    price
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-6-3))
    

Parse from_ago from a valid price.

* * *

## BasePFPreparer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L165-L576 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-7-1)BasePFPreparer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-7-2)    arg_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-7-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-7-4))
    

Base class for preparing portfolio simulations.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [BasePreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer "vectorbtpro.base.preparing.BasePreparer")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.base.preparing.BasePreparer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.base.preparing.BasePreparer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.base.preparing.BasePreparer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.base.preparing.BasePreparer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.base.preparing.BasePreparer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.base.preparing.BasePreparer.find_messages")
  * [BasePreparer.adapt_staticized_to_udf](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.adapt_staticized_to_udf "vectorbtpro.base.preparing.BasePreparer.adapt_staticized_to_udf")
  * [BasePreparer.args_to_broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.args_to_broadcast "vectorbtpro.base.preparing.BasePreparer.args_to_broadcast")
  * [BasePreparer.broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_kwargs "vectorbtpro.base.preparing.BasePreparer.broadcast_kwargs")
  * [BasePreparer.broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_named_args "vectorbtpro.base.preparing.BasePreparer.broadcast_named_args")
  * [BasePreparer.broadcast_result](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_result "vectorbtpro.base.preparing.BasePreparer.broadcast_result")
  * [BasePreparer.build_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.build_arg_config_doc "vectorbtpro.base.preparing.BasePreparer.build_arg_config_doc")
  * [BasePreparer.chunked](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.chunked "vectorbtpro.base.preparing.BasePreparer.chunked")
  * [BasePreparer.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.base.preparing.BasePreparer.config")
  * [BasePreparer.def_broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.def_broadcast_kwargs "vectorbtpro.base.preparing.BasePreparer.def_broadcast_kwargs")
  * [BasePreparer.dt_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.dt_arr_to_ns "vectorbtpro.base.preparing.BasePreparer.dt_arr_to_ns")
  * [BasePreparer.find_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.find_target_func "vectorbtpro.base.preparing.BasePreparer.find_target_func")
  * [BasePreparer.freq](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.freq "vectorbtpro.base.preparing.BasePreparer.freq")
  * [BasePreparer.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg "vectorbtpro.base.preparing.BasePreparer.get_arg")
  * [BasePreparer.get_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg_default "vectorbtpro.base.preparing.BasePreparer.get_arg_default")
  * [BasePreparer.get_raw_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg "vectorbtpro.base.preparing.BasePreparer.get_raw_arg")
  * [BasePreparer.get_raw_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg_default "vectorbtpro.base.preparing.BasePreparer.get_raw_arg_default")
  * [BasePreparer.idx_setters](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.idx_setters "vectorbtpro.base.preparing.BasePreparer.idx_setters")
  * [BasePreparer.index](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.index "vectorbtpro.base.preparing.BasePreparer.index")
  * [BasePreparer.jitted](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.jitted "vectorbtpro.base.preparing.BasePreparer.jitted")
  * [BasePreparer.map_enum_value](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.map_enum_value "vectorbtpro.base.preparing.BasePreparer.map_enum_value")
  * [BasePreparer.override_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.override_arg_config_doc "vectorbtpro.base.preparing.BasePreparer.override_arg_config_doc")
  * [BasePreparer.post_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_args "vectorbtpro.base.preparing.BasePreparer.post_args")
  * [BasePreparer.post_broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_broadcast_named_args "vectorbtpro.base.preparing.BasePreparer.post_broadcast_named_args")
  * [BasePreparer.pre_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.pre_args "vectorbtpro.base.preparing.BasePreparer.pre_args")
  * [BasePreparer.prepare_dt_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_arr "vectorbtpro.base.preparing.BasePreparer.prepare_dt_arr")
  * [BasePreparer.prepare_dt_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_obj "vectorbtpro.base.preparing.BasePreparer.prepare_dt_obj")
  * [BasePreparer.prepare_post_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_post_arg "vectorbtpro.base.preparing.BasePreparer.prepare_post_arg")
  * [BasePreparer.prepare_td_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_arr "vectorbtpro.base.preparing.BasePreparer.prepare_td_arr")
  * [BasePreparer.prepare_td_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_obj "vectorbtpro.base.preparing.BasePreparer.prepare_td_obj")
  * [BasePreparer.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.base.preparing.BasePreparer.rec_state")
  * [BasePreparer.records](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.records "vectorbtpro.base.preparing.BasePreparer.records")
  * [BasePreparer.resolve_dynamic_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.resolve_dynamic_target_func "vectorbtpro.base.preparing.BasePreparer.resolve_dynamic_target_func")
  * [BasePreparer.seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.seed "vectorbtpro.base.preparing.BasePreparer.seed")
  * [BasePreparer.set_seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.set_seed "vectorbtpro.base.preparing.BasePreparer.set_seed")
  * [BasePreparer.staticized](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.staticized "vectorbtpro.base.preparing.BasePreparer.staticized")
  * [BasePreparer.target_arg_map](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_arg_map "vectorbtpro.base.preparing.BasePreparer.target_arg_map")
  * [BasePreparer.target_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_args "vectorbtpro.base.preparing.BasePreparer.target_args")
  * [BasePreparer.target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_func "vectorbtpro.base.preparing.BasePreparer.target_func")
  * [BasePreparer.target_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_shape "vectorbtpro.base.preparing.BasePreparer.target_shape")
  * [BasePreparer.td_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.td_arr_to_ns "vectorbtpro.base.preparing.BasePreparer.td_arr_to_ns")
  * [BasePreparer.template_context](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.template_context "vectorbtpro.base.preparing.BasePreparer.template_context")
  * [BasePreparer.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.wrapper "vectorbtpro.base.preparing.BasePreparer.wrapper")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.base.preparing.BasePreparer.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.base.preparing.BasePreparer.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.base.preparing.BasePreparer.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.base.preparing.BasePreparer.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.base.preparing.BasePreparer.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.base.preparing.BasePreparer.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.base.preparing.BasePreparer.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.base.preparing.BasePreparer.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.base.preparing.BasePreparer.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.base.preparing.BasePreparer.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.base.preparing.BasePreparer.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.base.preparing.BasePreparer.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.base.preparing.BasePreparer.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.base.preparing.BasePreparer.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.base.preparing.BasePreparer.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.base.preparing.BasePreparer.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.base.preparing.BasePreparer.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.base.preparing.BasePreparer.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.base.preparing.BasePreparer.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.base.preparing.BasePreparer.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.base.preparing.BasePreparer.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.base.preparing.BasePreparer.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.base.preparing.BasePreparer.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.base.preparing.BasePreparer.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.base.preparing.BasePreparer.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.base.preparing.BasePreparer.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.base.preparing.BasePreparer.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.base.preparing.BasePreparer.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.base.preparing.BasePreparer.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.base.preparing.BasePreparer.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.base.preparing.BasePreparer.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.base.preparing.BasePreparer.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.base.preparing.BasePreparer.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.base.preparing.BasePreparer.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.base.preparing.BasePreparer.pprint")



**Subclasses**

  * [FOFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer "vectorbtpro.portfolio.preparing.FOFPreparer")
  * [FOPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer "vectorbtpro.portfolio.preparing.FOPreparer")
  * [FSPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer "vectorbtpro.portfolio.preparing.FSPreparer")



* * *

### align_pc_arr method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L349-L382 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.align_pc_arr "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-8-1)BasePFPreparer.align_pc_arr(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-8-2)    arr,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-8-3)    group_lens=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-8-4)    check_dtype=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-8-5)    cast_to_dtype=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-8-6)    reduce_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-8-7)    arg_name=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-8-8))
    

Align a per-column array.

* * *

### attach_call_seq cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.attach_call_seq "Permanent link")

Argument `attach_call_seq`.

* * *

### auto_call_seq cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_call_seq "Permanent link")

Whether automatic call sequence is enabled.

* * *

### auto_sim_end cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_end "Permanent link")

Get automatic `sim_end`

* * *

### auto_sim_start cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_start "Permanent link")

Get automatic `sim_start`

* * *

### bm_close cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.bm_close "Permanent link")

Argument `bm_close`.

* * *

### call_seq cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.call_seq "Permanent link")

Argument `call_seq`.

* * *

### cash_deposits cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_deposits "Permanent link")

Argument `cash_deposits`.

* * *

### cash_earnings cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_earnings "Permanent link")

Argument `cash_earnings`.

* * *

### cash_sharing cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_sharing "Permanent link")

Argument `cash_sharing`.

* * *

### close cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.close "Permanent link")

Argument `close`.

* * *

### cs_group_lens cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cs_group_lens "Permanent link")

Cash sharing aware group lengths.

* * *

### data cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.data "Permanent link")

Argument `data`.

* * *

### group_by cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_by "Permanent link")

Argument `group_by`.

* * *

### group_lens cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_lens "Permanent link")

Group lengths.

* * *

### high cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.high "Permanent link")

Argument `high`.

* * *

### in_outputs cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.in_outputs "Permanent link")

Argument `in_outputs`.

* * *

### init_cash cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash "Permanent link")

Argument `init_cash`.

* * *

### init_cash_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash_mode "Permanent link")

Initial cash mode.

* * *

### init_position cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_position "Permanent link")

Argument `init_position`.

* * *

### init_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_price "Permanent link")

Argument `init_price`.

* * *

### keep_inout_flex cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.keep_inout_flex "Permanent link")

Argument `keep_inout_flex`.

* * *

### low cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.low "Permanent link")

Argument `low`.

* * *

### open cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.open "Permanent link")

Argument `open`.

* * *

### parse_data class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L200-L219 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.parse_data "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-9-1)BasePFPreparer.parse_data(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-9-2)    data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-9-3)    all_ohlc=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-9-4))
    

Parse an instance with OHLC features.

* * *

### pf_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.pf_args "Permanent link")

Arguments to be passed to the portfolio.

* * *

### result cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.result "Permanent link")

Result as an instance of [PFPrepResult](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.PFPrepResult "vectorbtpro.portfolio.preparing.PFPrepResult").

* * *

### sim_end cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end "Permanent link")

Argument `sim_end`.

* * *

### sim_group_lens cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_group_lens "Permanent link")

Simulation group lengths.

* * *

### sim_start cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start "Permanent link")

Argument `sim_start`.

* * *

## FDOFPreparer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L2181-L2318 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-10-1)FDOFPreparer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-10-2)    arg_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-10-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-10-4))
    

Class for preparing [Portfolio.from_def_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_def_order_func "vectorbtpro.portfolio.base.Portfolio.from_def_order_func").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [BasePFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer "vectorbtpro.portfolio.preparing.BasePFPreparer")
  * [BasePreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer "vectorbtpro.base.preparing.BasePreparer")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [FOFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer "vectorbtpro.portfolio.preparing.FOFPreparer")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.portfolio.preparing.FOFPreparer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.portfolio.preparing.FOFPreparer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.portfolio.preparing.FOFPreparer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.portfolio.preparing.FOFPreparer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.portfolio.preparing.FOFPreparer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.portfolio.preparing.FOFPreparer.find_messages")
  * [BasePFPreparer.align_pc_arr](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.align_pc_arr "vectorbtpro.portfolio.preparing.FOFPreparer.align_pc_arr")
  * [BasePFPreparer.find_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.find_target_func "vectorbtpro.portfolio.preparing.FOFPreparer.find_target_func")
  * [BasePFPreparer.parse_data](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.parse_data "vectorbtpro.portfolio.preparing.FOFPreparer.parse_data")
  * [BasePFPreparer.sim_end](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end")
  * [BasePFPreparer.sim_start](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start")
  * [BasePFPreparer.target_arg_map](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_arg_map "vectorbtpro.portfolio.preparing.BasePFPreparer.target_arg_map")
  * [BasePFPreparer.target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.target_func")
  * [BasePreparer.adapt_staticized_to_udf](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.adapt_staticized_to_udf "vectorbtpro.portfolio.preparing.FOFPreparer.adapt_staticized_to_udf")
  * [BasePreparer.build_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.build_arg_config_doc "vectorbtpro.portfolio.preparing.FOFPreparer.build_arg_config_doc")
  * [BasePreparer.dt_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.dt_arr_to_ns "vectorbtpro.portfolio.preparing.FOFPreparer.dt_arr_to_ns")
  * [BasePreparer.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg "vectorbtpro.portfolio.preparing.FOFPreparer.get_arg")
  * [BasePreparer.get_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg_default "vectorbtpro.portfolio.preparing.FOFPreparer.get_arg_default")
  * [BasePreparer.get_raw_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg "vectorbtpro.portfolio.preparing.FOFPreparer.get_raw_arg")
  * [BasePreparer.get_raw_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg_default "vectorbtpro.portfolio.preparing.FOFPreparer.get_raw_arg_default")
  * [BasePreparer.map_enum_value](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.map_enum_value "vectorbtpro.portfolio.preparing.FOFPreparer.map_enum_value")
  * [BasePreparer.override_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.override_arg_config_doc "vectorbtpro.portfolio.preparing.FOFPreparer.override_arg_config_doc")
  * [BasePreparer.prepare_dt_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_arr "vectorbtpro.portfolio.preparing.FOFPreparer.prepare_dt_arr")
  * [BasePreparer.prepare_dt_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_obj "vectorbtpro.portfolio.preparing.FOFPreparer.prepare_dt_obj")
  * [BasePreparer.prepare_post_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_post_arg "vectorbtpro.portfolio.preparing.FOFPreparer.prepare_post_arg")
  * [BasePreparer.prepare_td_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_arr "vectorbtpro.portfolio.preparing.FOFPreparer.prepare_td_arr")
  * [BasePreparer.prepare_td_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_obj "vectorbtpro.portfolio.preparing.FOFPreparer.prepare_td_obj")
  * [BasePreparer.resolve_dynamic_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.resolve_dynamic_target_func "vectorbtpro.portfolio.preparing.FOFPreparer.resolve_dynamic_target_func")
  * [BasePreparer.set_seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.set_seed "vectorbtpro.portfolio.preparing.FOFPreparer.set_seed")
  * [BasePreparer.td_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.td_arr_to_ns "vectorbtpro.portfolio.preparing.FOFPreparer.td_arr_to_ns")
  * [BasePreparer.template_context](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.template_context "vectorbtpro.base.preparing.BasePreparer.template_context")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.portfolio.preparing.FOFPreparer.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.portfolio.preparing.FOFPreparer.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.portfolio.preparing.FOFPreparer.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.portfolio.preparing.FOFPreparer.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.portfolio.preparing.FOFPreparer.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.portfolio.preparing.FOFPreparer.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.portfolio.preparing.FOFPreparer.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.portfolio.preparing.FOFPreparer.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.portfolio.preparing.FOFPreparer.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.portfolio.preparing.FOFPreparer.update_config")
  * [FOFPreparer.args_to_broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.args_to_broadcast "vectorbtpro.portfolio.preparing.FOFPreparer.args_to_broadcast")
  * [FOFPreparer.attach_call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.attach_call_seq "vectorbtpro.portfolio.preparing.FOFPreparer.attach_call_seq")
  * [FOFPreparer.auto_call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_call_seq "vectorbtpro.portfolio.preparing.FOFPreparer.auto_call_seq")
  * [FOFPreparer.auto_sim_end](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_end "vectorbtpro.portfolio.preparing.FOFPreparer.auto_sim_end")
  * [FOFPreparer.auto_sim_start](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_start "vectorbtpro.portfolio.preparing.FOFPreparer.auto_sim_start")
  * [FOFPreparer.bm_close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.bm_close "vectorbtpro.portfolio.preparing.FOFPreparer.bm_close")
  * [FOFPreparer.broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_kwargs "vectorbtpro.portfolio.preparing.FOFPreparer.broadcast_kwargs")
  * [FOFPreparer.broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_named_args "vectorbtpro.portfolio.preparing.FOFPreparer.broadcast_named_args")
  * [FOFPreparer.broadcast_result](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_result "vectorbtpro.portfolio.preparing.FOFPreparer.broadcast_result")
  * [FOFPreparer.call_post_segment](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.call_post_segment "vectorbtpro.portfolio.preparing.FOFPreparer.call_post_segment")
  * [FOFPreparer.call_pre_segment](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.call_pre_segment "vectorbtpro.portfolio.preparing.FOFPreparer.call_pre_segment")
  * [FOFPreparer.call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.call_seq "vectorbtpro.portfolio.preparing.FOFPreparer.call_seq")
  * [FOFPreparer.cash_deposits](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_deposits "vectorbtpro.portfolio.preparing.FOFPreparer.cash_deposits")
  * [FOFPreparer.cash_earnings](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_earnings "vectorbtpro.portfolio.preparing.FOFPreparer.cash_earnings")
  * [FOFPreparer.cash_sharing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_sharing "vectorbtpro.portfolio.preparing.FOFPreparer.cash_sharing")
  * [FOFPreparer.chunked](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.chunked "vectorbtpro.portfolio.preparing.FOFPreparer.chunked")
  * [FOFPreparer.close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.close "vectorbtpro.portfolio.preparing.FOFPreparer.close")
  * [FOFPreparer.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.portfolio.preparing.FOFPreparer.config")
  * [FOFPreparer.cs_group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cs_group_lens "vectorbtpro.portfolio.preparing.FOFPreparer.cs_group_lens")
  * [FOFPreparer.data](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.data "vectorbtpro.portfolio.preparing.FOFPreparer.data")
  * [FOFPreparer.def_broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.def_broadcast_kwargs "vectorbtpro.portfolio.preparing.FOFPreparer.def_broadcast_kwargs")
  * [FOFPreparer.ffill_val_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.ffill_val_price "vectorbtpro.portfolio.preparing.FOFPreparer.ffill_val_price")
  * [FOFPreparer.fill_pos_info](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.fill_pos_info "vectorbtpro.portfolio.preparing.FOFPreparer.fill_pos_info")
  * [FOFPreparer.flex_order_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.flex_order_args "vectorbtpro.portfolio.preparing.FOFPreparer.flex_order_args")
  * [FOFPreparer.flex_order_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.flex_order_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.flex_order_func_nb")
  * [FOFPreparer.flexible](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.flexible "vectorbtpro.portfolio.preparing.FOFPreparer.flexible")
  * [FOFPreparer.freq](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.freq "vectorbtpro.portfolio.preparing.FOFPreparer.freq")
  * [FOFPreparer.group_by](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_by "vectorbtpro.portfolio.preparing.FOFPreparer.group_by")
  * [FOFPreparer.group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_lens "vectorbtpro.portfolio.preparing.FOFPreparer.group_lens")
  * [FOFPreparer.high](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.high "vectorbtpro.portfolio.preparing.FOFPreparer.high")
  * [FOFPreparer.idx_setters](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.idx_setters "vectorbtpro.portfolio.preparing.FOFPreparer.idx_setters")
  * [FOFPreparer.in_outputs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.in_outputs "vectorbtpro.portfolio.preparing.FOFPreparer.in_outputs")
  * [FOFPreparer.index](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.index "vectorbtpro.portfolio.preparing.FOFPreparer.index")
  * [FOFPreparer.init_cash](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash "vectorbtpro.portfolio.preparing.FOFPreparer.init_cash")
  * [FOFPreparer.init_cash_mode](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash_mode "vectorbtpro.portfolio.preparing.FOFPreparer.init_cash_mode")
  * [FOFPreparer.init_position](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_position "vectorbtpro.portfolio.preparing.FOFPreparer.init_position")
  * [FOFPreparer.init_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_price "vectorbtpro.portfolio.preparing.FOFPreparer.init_price")
  * [FOFPreparer.jitted](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.jitted "vectorbtpro.portfolio.preparing.FOFPreparer.jitted")
  * [FOFPreparer.keep_inout_flex](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.keep_inout_flex "vectorbtpro.portfolio.preparing.FOFPreparer.keep_inout_flex")
  * [FOFPreparer.low](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.low "vectorbtpro.portfolio.preparing.FOFPreparer.low")
  * [FOFPreparer.max_log_records](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.max_log_records "vectorbtpro.portfolio.preparing.FOFPreparer.max_log_records")
  * [FOFPreparer.max_order_records](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.max_order_records "vectorbtpro.portfolio.preparing.FOFPreparer.max_order_records")
  * [FOFPreparer.open](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.open "vectorbtpro.portfolio.preparing.FOFPreparer.open")
  * [FOFPreparer.order_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.order_args "vectorbtpro.portfolio.preparing.FOFPreparer.order_args")
  * [FOFPreparer.order_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.order_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.order_func_nb")
  * [FOFPreparer.pf_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.pf_args "vectorbtpro.portfolio.preparing.FOFPreparer.pf_args")
  * [FOFPreparer.post_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_args "vectorbtpro.portfolio.preparing.FOFPreparer.post_args")
  * [FOFPreparer.post_broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_broadcast_named_args "vectorbtpro.portfolio.preparing.FOFPreparer.post_broadcast_named_args")
  * [FOFPreparer.post_group_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_group_args "vectorbtpro.portfolio.preparing.FOFPreparer.post_group_args")
  * [FOFPreparer.post_group_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_group_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.post_group_func_nb")
  * [FOFPreparer.post_order_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_order_args "vectorbtpro.portfolio.preparing.FOFPreparer.post_order_args")
  * [FOFPreparer.post_order_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_order_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.post_order_func_nb")
  * [FOFPreparer.post_row_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_row_args "vectorbtpro.portfolio.preparing.FOFPreparer.post_row_args")
  * [FOFPreparer.post_row_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_row_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.post_row_func_nb")
  * [FOFPreparer.post_segment_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_segment_args "vectorbtpro.portfolio.preparing.FOFPreparer.post_segment_args")
  * [FOFPreparer.post_segment_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_segment_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.post_segment_func_nb")
  * [FOFPreparer.post_sim_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_sim_args "vectorbtpro.portfolio.preparing.FOFPreparer.post_sim_args")
  * [FOFPreparer.post_sim_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_sim_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.post_sim_func_nb")
  * [FOFPreparer.pre_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.pre_args "vectorbtpro.portfolio.preparing.FOFPreparer.pre_args")
  * [FOFPreparer.pre_group_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_group_args "vectorbtpro.portfolio.preparing.FOFPreparer.pre_group_args")
  * [FOFPreparer.pre_group_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_group_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.pre_group_func_nb")
  * [FOFPreparer.pre_row_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_row_args "vectorbtpro.portfolio.preparing.FOFPreparer.pre_row_args")
  * [FOFPreparer.pre_row_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_row_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.pre_row_func_nb")
  * [FOFPreparer.pre_segment_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_segment_args "vectorbtpro.portfolio.preparing.FOFPreparer.pre_segment_args")
  * [FOFPreparer.pre_segment_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_segment_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.pre_segment_func_nb")
  * [FOFPreparer.pre_sim_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_sim_args "vectorbtpro.portfolio.preparing.FOFPreparer.pre_sim_args")
  * [FOFPreparer.pre_sim_func_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_sim_func_nb "vectorbtpro.portfolio.preparing.FOFPreparer.pre_sim_func_nb")
  * [FOFPreparer.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.portfolio.preparing.FOFPreparer.rec_state")
  * [FOFPreparer.records](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.records "vectorbtpro.portfolio.preparing.FOFPreparer.records")
  * [FOFPreparer.result](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.result "vectorbtpro.portfolio.preparing.FOFPreparer.result")
  * [FOFPreparer.row_wise](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.row_wise "vectorbtpro.portfolio.preparing.FOFPreparer.row_wise")
  * [FOFPreparer.seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.seed "vectorbtpro.portfolio.preparing.FOFPreparer.seed")
  * [FOFPreparer.segment_mask](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.segment_mask "vectorbtpro.portfolio.preparing.FOFPreparer.segment_mask")
  * [FOFPreparer.sim_group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_group_lens "vectorbtpro.portfolio.preparing.FOFPreparer.sim_group_lens")
  * [FOFPreparer.staticized](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.staticized "vectorbtpro.portfolio.preparing.FOFPreparer.staticized")
  * [FOFPreparer.target_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_args "vectorbtpro.portfolio.preparing.FOFPreparer.target_args")
  * [FOFPreparer.target_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_shape "vectorbtpro.portfolio.preparing.FOFPreparer.target_shape")
  * [FOFPreparer.track_value](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.track_value "vectorbtpro.portfolio.preparing.FOFPreparer.track_value")
  * [FOFPreparer.update_value](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.update_value "vectorbtpro.portfolio.preparing.FOFPreparer.update_value")
  * [FOFPreparer.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.wrapper "vectorbtpro.portfolio.preparing.FOFPreparer.wrapper")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.portfolio.preparing.FOFPreparer.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.portfolio.preparing.FOFPreparer.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.portfolio.preparing.FOFPreparer.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.portfolio.preparing.FOFPreparer.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.portfolio.preparing.FOFPreparer.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.portfolio.preparing.FOFPreparer.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.portfolio.preparing.FOFPreparer.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.portfolio.preparing.FOFPreparer.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.portfolio.preparing.FOFPreparer.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.portfolio.preparing.FOFPreparer.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.portfolio.preparing.FOFPreparer.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.portfolio.preparing.FOFPreparer.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.portfolio.preparing.FOFPreparer.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.portfolio.preparing.FOFPreparer.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.portfolio.preparing.FOFPreparer.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.portfolio.preparing.FOFPreparer.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.portfolio.preparing.FOFPreparer.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.portfolio.preparing.FOFPreparer.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.portfolio.preparing.FOFPreparer.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.portfolio.preparing.FOFPreparer.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.portfolio.preparing.FOFPreparer.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.portfolio.preparing.FOFPreparer.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.portfolio.preparing.FOFPreparer.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.portfolio.preparing.FOFPreparer.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.portfolio.preparing.FOFPreparer.pprint")



* * *

### allow_partial cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.allow_partial "Permanent link")

Argument `allow_partial`.

* * *

### direction cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.direction "Permanent link")

Argument `direction`.

* * *

### fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.fees "Permanent link")

Argument `fees`.

* * *

### fixed_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.fixed_fees "Permanent link")

Argument `fixed_fees`.

* * *

### leverage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.leverage "Permanent link")

Argument `leverage`.

* * *

### leverage_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.leverage_mode "Permanent link")

Argument `leverage_mode`.

* * *

### log cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.log "Permanent link")

Argument `log`.

* * *

### max_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.max_size "Permanent link")

Argument `max_size`.

* * *

### min_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.min_size "Permanent link")

Argument `min_size`.

* * *

### price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.price "Permanent link")

Argument `price`.

* * *

### price_area_vio_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.price_area_vio_mode "Permanent link")

Argument `price_area_vio_mode`.

* * *

### raise_reject cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.raise_reject "Permanent link")

Argument `raise_reject`.

* * *

### reject_prob cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.reject_prob "Permanent link")

Argument `reject_prob`.

* * *

### size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.size "Permanent link")

Argument `size`.

* * *

### size_granularity cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.size_granularity "Permanent link")

Argument `size_granularity`.

* * *

### size_type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.size_type "Permanent link")

Argument `size_type`.

* * *

### slippage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.slippage "Permanent link")

Argument `slippage`.

* * *

### val_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer.val_price "Permanent link")

Argument `val_price`.

* * *

## FOFPreparer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L1863-L2155 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-11-1)FOFPreparer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-11-2)    arg_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-11-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-11-4))
    

Class for preparing [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func "vectorbtpro.portfolio.base.Portfolio.from_order_func").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [BasePFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer "vectorbtpro.portfolio.preparing.BasePFPreparer")
  * [BasePreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer "vectorbtpro.base.preparing.BasePreparer")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.portfolio.preparing.BasePFPreparer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.portfolio.preparing.BasePFPreparer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.portfolio.preparing.BasePFPreparer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.portfolio.preparing.BasePFPreparer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.portfolio.preparing.BasePFPreparer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.portfolio.preparing.BasePFPreparer.find_messages")
  * [BasePFPreparer.align_pc_arr](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.align_pc_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.align_pc_arr")
  * [BasePFPreparer.args_to_broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.args_to_broadcast "vectorbtpro.portfolio.preparing.BasePFPreparer.args_to_broadcast")
  * [BasePFPreparer.attach_call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.attach_call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.attach_call_seq")
  * [BasePFPreparer.auto_call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_call_seq")
  * [BasePFPreparer.auto_sim_end](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_end "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_end")
  * [BasePFPreparer.auto_sim_start](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_start "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_start")
  * [BasePFPreparer.bm_close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.bm_close "vectorbtpro.portfolio.preparing.BasePFPreparer.bm_close")
  * [BasePFPreparer.broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_kwargs")
  * [BasePFPreparer.broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_named_args "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_named_args")
  * [BasePFPreparer.broadcast_result](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_result "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_result")
  * [BasePFPreparer.call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.call_seq")
  * [BasePFPreparer.cash_deposits](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_deposits "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_deposits")
  * [BasePFPreparer.cash_earnings](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_earnings "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_earnings")
  * [BasePFPreparer.cash_sharing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_sharing "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_sharing")
  * [BasePFPreparer.chunked](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.chunked "vectorbtpro.portfolio.preparing.BasePFPreparer.chunked")
  * [BasePFPreparer.close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.close "vectorbtpro.portfolio.preparing.BasePFPreparer.close")
  * [BasePFPreparer.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.portfolio.preparing.BasePFPreparer.config")
  * [BasePFPreparer.cs_group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cs_group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.cs_group_lens")
  * [BasePFPreparer.data](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.data "vectorbtpro.portfolio.preparing.BasePFPreparer.data")
  * [BasePFPreparer.def_broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.def_broadcast_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.def_broadcast_kwargs")
  * [BasePFPreparer.find_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.find_target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.find_target_func")
  * [BasePFPreparer.freq](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.freq "vectorbtpro.portfolio.preparing.BasePFPreparer.freq")
  * [BasePFPreparer.group_by](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_by "vectorbtpro.portfolio.preparing.BasePFPreparer.group_by")
  * [BasePFPreparer.group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.group_lens")
  * [BasePFPreparer.high](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.high "vectorbtpro.portfolio.preparing.BasePFPreparer.high")
  * [BasePFPreparer.idx_setters](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.idx_setters "vectorbtpro.portfolio.preparing.BasePFPreparer.idx_setters")
  * [BasePFPreparer.in_outputs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.in_outputs "vectorbtpro.portfolio.preparing.BasePFPreparer.in_outputs")
  * [BasePFPreparer.index](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.index "vectorbtpro.portfolio.preparing.BasePFPreparer.index")
  * [BasePFPreparer.init_cash](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash "vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash")
  * [BasePFPreparer.init_cash_mode](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash_mode "vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash_mode")
  * [BasePFPreparer.init_position](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_position "vectorbtpro.portfolio.preparing.BasePFPreparer.init_position")
  * [BasePFPreparer.init_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_price "vectorbtpro.portfolio.preparing.BasePFPreparer.init_price")
  * [BasePFPreparer.jitted](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.jitted "vectorbtpro.portfolio.preparing.BasePFPreparer.jitted")
  * [BasePFPreparer.keep_inout_flex](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.keep_inout_flex "vectorbtpro.portfolio.preparing.BasePFPreparer.keep_inout_flex")
  * [BasePFPreparer.low](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.low "vectorbtpro.portfolio.preparing.BasePFPreparer.low")
  * [BasePFPreparer.open](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.open "vectorbtpro.portfolio.preparing.BasePFPreparer.open")
  * [BasePFPreparer.parse_data](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.parse_data "vectorbtpro.portfolio.preparing.BasePFPreparer.parse_data")
  * [BasePFPreparer.pf_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.pf_args "vectorbtpro.portfolio.preparing.BasePFPreparer.pf_args")
  * [BasePFPreparer.post_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_args "vectorbtpro.portfolio.preparing.BasePFPreparer.post_args")
  * [BasePFPreparer.post_broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_broadcast_named_args "vectorbtpro.portfolio.preparing.BasePFPreparer.post_broadcast_named_args")
  * [BasePFPreparer.pre_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.pre_args "vectorbtpro.portfolio.preparing.BasePFPreparer.pre_args")
  * [BasePFPreparer.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.portfolio.preparing.BasePFPreparer.rec_state")
  * [BasePFPreparer.records](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.records "vectorbtpro.portfolio.preparing.BasePFPreparer.records")
  * [BasePFPreparer.result](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.result "vectorbtpro.portfolio.preparing.BasePFPreparer.result")
  * [BasePFPreparer.seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.seed "vectorbtpro.portfolio.preparing.BasePFPreparer.seed")
  * [BasePFPreparer.sim_end](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end")
  * [BasePFPreparer.sim_group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_group_lens")
  * [BasePFPreparer.sim_start](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start")
  * [BasePFPreparer.staticized](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.staticized "vectorbtpro.portfolio.preparing.BasePFPreparer.staticized")
  * [BasePFPreparer.target_arg_map](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_arg_map "vectorbtpro.portfolio.preparing.BasePFPreparer.target_arg_map")
  * [BasePFPreparer.target_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_args "vectorbtpro.portfolio.preparing.BasePFPreparer.target_args")
  * [BasePFPreparer.target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.target_func")
  * [BasePFPreparer.target_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_shape "vectorbtpro.portfolio.preparing.BasePFPreparer.target_shape")
  * [BasePFPreparer.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.wrapper "vectorbtpro.portfolio.preparing.BasePFPreparer.wrapper")
  * [BasePreparer.adapt_staticized_to_udf](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.adapt_staticized_to_udf "vectorbtpro.portfolio.preparing.BasePFPreparer.adapt_staticized_to_udf")
  * [BasePreparer.build_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.build_arg_config_doc "vectorbtpro.portfolio.preparing.BasePFPreparer.build_arg_config_doc")
  * [BasePreparer.dt_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.dt_arr_to_ns "vectorbtpro.portfolio.preparing.BasePFPreparer.dt_arr_to_ns")
  * [BasePreparer.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.get_arg")
  * [BasePreparer.get_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg_default "vectorbtpro.portfolio.preparing.BasePFPreparer.get_arg_default")
  * [BasePreparer.get_raw_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.get_raw_arg")
  * [BasePreparer.get_raw_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg_default "vectorbtpro.portfolio.preparing.BasePFPreparer.get_raw_arg_default")
  * [BasePreparer.map_enum_value](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.map_enum_value "vectorbtpro.portfolio.preparing.BasePFPreparer.map_enum_value")
  * [BasePreparer.override_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.override_arg_config_doc "vectorbtpro.portfolio.preparing.BasePFPreparer.override_arg_config_doc")
  * [BasePreparer.prepare_dt_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_dt_arr")
  * [BasePreparer.prepare_dt_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_obj "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_dt_obj")
  * [BasePreparer.prepare_post_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_post_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_post_arg")
  * [BasePreparer.prepare_td_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_td_arr")
  * [BasePreparer.prepare_td_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_obj "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_td_obj")
  * [BasePreparer.resolve_dynamic_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.resolve_dynamic_target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_dynamic_target_func")
  * [BasePreparer.set_seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.set_seed "vectorbtpro.portfolio.preparing.BasePFPreparer.set_seed")
  * [BasePreparer.td_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.td_arr_to_ns "vectorbtpro.portfolio.preparing.BasePFPreparer.td_arr_to_ns")
  * [BasePreparer.template_context](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.template_context "vectorbtpro.base.preparing.BasePreparer.template_context")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.portfolio.preparing.BasePFPreparer.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.portfolio.preparing.BasePFPreparer.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.portfolio.preparing.BasePFPreparer.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.portfolio.preparing.BasePFPreparer.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.portfolio.preparing.BasePFPreparer.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.portfolio.preparing.BasePFPreparer.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.portfolio.preparing.BasePFPreparer.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.portfolio.preparing.BasePFPreparer.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.portfolio.preparing.BasePFPreparer.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.portfolio.preparing.BasePFPreparer.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.portfolio.preparing.BasePFPreparer.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.portfolio.preparing.BasePFPreparer.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.portfolio.preparing.BasePFPreparer.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.portfolio.preparing.BasePFPreparer.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.portfolio.preparing.BasePFPreparer.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.portfolio.preparing.BasePFPreparer.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.portfolio.preparing.BasePFPreparer.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.portfolio.preparing.BasePFPreparer.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.portfolio.preparing.BasePFPreparer.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.portfolio.preparing.BasePFPreparer.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.portfolio.preparing.BasePFPreparer.pprint")



**Subclasses**

  * [FDOFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FDOFPreparer "vectorbtpro.portfolio.preparing.FDOFPreparer")



* * *

### call_post_segment cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.call_post_segment "Permanent link")

Argument `call_post_segment`.

* * *

### call_pre_segment cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.call_pre_segment "Permanent link")

Argument `call_pre_segment`.

* * *

### ffill_val_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.ffill_val_price "Permanent link")

Argument `ffill_val_price`.

* * *

### fill_pos_info cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.fill_pos_info "Permanent link")

Argument `fill_pos_info`.

* * *

### flex_order_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.flex_order_args "Permanent link")

Argument `flex_order_args`.

* * *

### flex_order_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.flex_order_func_nb "Permanent link")

Argument `flex_order_func_nb`.

* * *

### flexible cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.flexible "Permanent link")

Whether the flexible mode is enabled.

* * *

### max_log_records cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.max_log_records "Permanent link")

Argument `max_log_records`.

* * *

### max_order_records cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.max_order_records "Permanent link")

Argument `max_order_records`.

* * *

### order_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.order_args "Permanent link")

Argument `order_args`.

* * *

### order_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.order_func_nb "Permanent link")

Argument `order_func_nb`.

* * *

### post_group_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_group_args "Permanent link")

Argument `post_group_args`.

* * *

### post_group_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_group_func_nb "Permanent link")

Argument `post_group_func_nb`.

* * *

### post_order_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_order_args "Permanent link")

Argument `post_order_args`.

* * *

### post_order_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_order_func_nb "Permanent link")

Argument `post_order_func_nb`.

* * *

### post_row_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_row_args "Permanent link")

Argument `post_row_args`.

* * *

### post_row_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_row_func_nb "Permanent link")

Argument `post_row_func_nb`.

* * *

### post_segment_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_segment_args "Permanent link")

Argument `post_segment_args`.

* * *

### post_segment_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_segment_func_nb "Permanent link")

Argument `post_segment_func_nb`.

* * *

### post_sim_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_sim_args "Permanent link")

Argument `post_sim_args`.

* * *

### post_sim_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.post_sim_func_nb "Permanent link")

Argument `post_sim_func_nb`.

* * *

### pre_group_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_group_args "Permanent link")

Argument `pre_group_args`.

* * *

### pre_group_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_group_func_nb "Permanent link")

Argument `pre_group_func_nb`.

* * *

### pre_row_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_row_args "Permanent link")

Argument `pre_row_args`.

* * *

### pre_row_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_row_func_nb "Permanent link")

Argument `pre_row_func_nb`.

* * *

### pre_segment_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_segment_args "Permanent link")

Argument `pre_segment_args`.

* * *

### pre_segment_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_segment_func_nb "Permanent link")

Argument `pre_segment_func_nb`.

* * *

### pre_sim_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_sim_args "Permanent link")

Argument `pre_sim_args`.

* * *

### pre_sim_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.pre_sim_func_nb "Permanent link")

Argument `pre_sim_func_nb`.

* * *

### row_wise cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.row_wise "Permanent link")

Argument `row_wise`.

* * *

### segment_mask cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.segment_mask "Permanent link")

Argument `segment_mask`.

* * *

### track_value cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.track_value "Permanent link")

Argument `track_value`.

* * *

### update_value cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOFPreparer.update_value "Permanent link")

Argument `update_value`.

* * *

## FOPreparer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L727-L902 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-12-1)FOPreparer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-12-2)    arg_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-12-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-12-4))
    

Class for preparing [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders "vectorbtpro.portfolio.base.Portfolio.from_orders").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [BasePFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer "vectorbtpro.portfolio.preparing.BasePFPreparer")
  * [BasePreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer "vectorbtpro.base.preparing.BasePreparer")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.portfolio.preparing.BasePFPreparer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.portfolio.preparing.BasePFPreparer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.portfolio.preparing.BasePFPreparer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.portfolio.preparing.BasePFPreparer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.portfolio.preparing.BasePFPreparer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.portfolio.preparing.BasePFPreparer.find_messages")
  * [BasePFPreparer.align_pc_arr](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.align_pc_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.align_pc_arr")
  * [BasePFPreparer.args_to_broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.args_to_broadcast "vectorbtpro.portfolio.preparing.BasePFPreparer.args_to_broadcast")
  * [BasePFPreparer.attach_call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.attach_call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.attach_call_seq")
  * [BasePFPreparer.auto_call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_call_seq")
  * [BasePFPreparer.auto_sim_end](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_end "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_end")
  * [BasePFPreparer.auto_sim_start](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_start "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_start")
  * [BasePFPreparer.bm_close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.bm_close "vectorbtpro.portfolio.preparing.BasePFPreparer.bm_close")
  * [BasePFPreparer.broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_kwargs")
  * [BasePFPreparer.broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_named_args "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_named_args")
  * [BasePFPreparer.broadcast_result](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_result "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_result")
  * [BasePFPreparer.call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.call_seq")
  * [BasePFPreparer.cash_deposits](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_deposits "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_deposits")
  * [BasePFPreparer.cash_earnings](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_earnings "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_earnings")
  * [BasePFPreparer.cash_sharing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_sharing "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_sharing")
  * [BasePFPreparer.chunked](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.chunked "vectorbtpro.portfolio.preparing.BasePFPreparer.chunked")
  * [BasePFPreparer.close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.close "vectorbtpro.portfolio.preparing.BasePFPreparer.close")
  * [BasePFPreparer.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.portfolio.preparing.BasePFPreparer.config")
  * [BasePFPreparer.cs_group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cs_group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.cs_group_lens")
  * [BasePFPreparer.data](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.data "vectorbtpro.portfolio.preparing.BasePFPreparer.data")
  * [BasePFPreparer.def_broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.def_broadcast_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.def_broadcast_kwargs")
  * [BasePFPreparer.find_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.find_target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.find_target_func")
  * [BasePFPreparer.freq](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.freq "vectorbtpro.portfolio.preparing.BasePFPreparer.freq")
  * [BasePFPreparer.group_by](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_by "vectorbtpro.portfolio.preparing.BasePFPreparer.group_by")
  * [BasePFPreparer.group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.group_lens")
  * [BasePFPreparer.high](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.high "vectorbtpro.portfolio.preparing.BasePFPreparer.high")
  * [BasePFPreparer.idx_setters](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.idx_setters "vectorbtpro.portfolio.preparing.BasePFPreparer.idx_setters")
  * [BasePFPreparer.in_outputs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.in_outputs "vectorbtpro.portfolio.preparing.BasePFPreparer.in_outputs")
  * [BasePFPreparer.index](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.index "vectorbtpro.portfolio.preparing.BasePFPreparer.index")
  * [BasePFPreparer.init_cash](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash "vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash")
  * [BasePFPreparer.init_cash_mode](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash_mode "vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash_mode")
  * [BasePFPreparer.init_position](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_position "vectorbtpro.portfolio.preparing.BasePFPreparer.init_position")
  * [BasePFPreparer.init_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_price "vectorbtpro.portfolio.preparing.BasePFPreparer.init_price")
  * [BasePFPreparer.jitted](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.jitted "vectorbtpro.portfolio.preparing.BasePFPreparer.jitted")
  * [BasePFPreparer.keep_inout_flex](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.keep_inout_flex "vectorbtpro.portfolio.preparing.BasePFPreparer.keep_inout_flex")
  * [BasePFPreparer.low](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.low "vectorbtpro.portfolio.preparing.BasePFPreparer.low")
  * [BasePFPreparer.open](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.open "vectorbtpro.portfolio.preparing.BasePFPreparer.open")
  * [BasePFPreparer.parse_data](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.parse_data "vectorbtpro.portfolio.preparing.BasePFPreparer.parse_data")
  * [BasePFPreparer.pf_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.pf_args "vectorbtpro.portfolio.preparing.BasePFPreparer.pf_args")
  * [BasePFPreparer.post_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_args "vectorbtpro.portfolio.preparing.BasePFPreparer.post_args")
  * [BasePFPreparer.post_broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_broadcast_named_args "vectorbtpro.portfolio.preparing.BasePFPreparer.post_broadcast_named_args")
  * [BasePFPreparer.pre_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.pre_args "vectorbtpro.portfolio.preparing.BasePFPreparer.pre_args")
  * [BasePFPreparer.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.portfolio.preparing.BasePFPreparer.rec_state")
  * [BasePFPreparer.records](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.records "vectorbtpro.portfolio.preparing.BasePFPreparer.records")
  * [BasePFPreparer.result](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.result "vectorbtpro.portfolio.preparing.BasePFPreparer.result")
  * [BasePFPreparer.seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.seed "vectorbtpro.portfolio.preparing.BasePFPreparer.seed")
  * [BasePFPreparer.sim_end](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end")
  * [BasePFPreparer.sim_group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_group_lens")
  * [BasePFPreparer.sim_start](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start")
  * [BasePFPreparer.staticized](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.staticized "vectorbtpro.portfolio.preparing.BasePFPreparer.staticized")
  * [BasePFPreparer.target_arg_map](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_arg_map "vectorbtpro.portfolio.preparing.BasePFPreparer.target_arg_map")
  * [BasePFPreparer.target_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_args "vectorbtpro.portfolio.preparing.BasePFPreparer.target_args")
  * [BasePFPreparer.target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.target_func")
  * [BasePFPreparer.target_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_shape "vectorbtpro.portfolio.preparing.BasePFPreparer.target_shape")
  * [BasePFPreparer.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.wrapper "vectorbtpro.portfolio.preparing.BasePFPreparer.wrapper")
  * [BasePreparer.adapt_staticized_to_udf](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.adapt_staticized_to_udf "vectorbtpro.portfolio.preparing.BasePFPreparer.adapt_staticized_to_udf")
  * [BasePreparer.build_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.build_arg_config_doc "vectorbtpro.portfolio.preparing.BasePFPreparer.build_arg_config_doc")
  * [BasePreparer.dt_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.dt_arr_to_ns "vectorbtpro.portfolio.preparing.BasePFPreparer.dt_arr_to_ns")
  * [BasePreparer.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.get_arg")
  * [BasePreparer.get_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg_default "vectorbtpro.portfolio.preparing.BasePFPreparer.get_arg_default")
  * [BasePreparer.get_raw_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.get_raw_arg")
  * [BasePreparer.get_raw_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg_default "vectorbtpro.portfolio.preparing.BasePFPreparer.get_raw_arg_default")
  * [BasePreparer.map_enum_value](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.map_enum_value "vectorbtpro.portfolio.preparing.BasePFPreparer.map_enum_value")
  * [BasePreparer.override_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.override_arg_config_doc "vectorbtpro.portfolio.preparing.BasePFPreparer.override_arg_config_doc")
  * [BasePreparer.prepare_dt_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_dt_arr")
  * [BasePreparer.prepare_dt_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_obj "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_dt_obj")
  * [BasePreparer.prepare_post_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_post_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_post_arg")
  * [BasePreparer.prepare_td_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_td_arr")
  * [BasePreparer.prepare_td_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_obj "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_td_obj")
  * [BasePreparer.resolve_dynamic_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.resolve_dynamic_target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_dynamic_target_func")
  * [BasePreparer.set_seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.set_seed "vectorbtpro.portfolio.preparing.BasePFPreparer.set_seed")
  * [BasePreparer.td_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.td_arr_to_ns "vectorbtpro.portfolio.preparing.BasePFPreparer.td_arr_to_ns")
  * [BasePreparer.template_context](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.template_context "vectorbtpro.base.preparing.BasePreparer.template_context")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.portfolio.preparing.BasePFPreparer.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.portfolio.preparing.BasePFPreparer.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.portfolio.preparing.BasePFPreparer.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.portfolio.preparing.BasePFPreparer.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.portfolio.preparing.BasePFPreparer.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.portfolio.preparing.BasePFPreparer.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.portfolio.preparing.BasePFPreparer.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.portfolio.preparing.BasePFPreparer.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.portfolio.preparing.BasePFPreparer.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.portfolio.preparing.BasePFPreparer.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.portfolio.preparing.BasePFPreparer.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.portfolio.preparing.BasePFPreparer.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.portfolio.preparing.BasePFPreparer.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.portfolio.preparing.BasePFPreparer.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.portfolio.preparing.BasePFPreparer.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.portfolio.preparing.BasePFPreparer.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.portfolio.preparing.BasePFPreparer.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.portfolio.preparing.BasePFPreparer.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.portfolio.preparing.BasePFPreparer.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.portfolio.preparing.BasePFPreparer.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.portfolio.preparing.BasePFPreparer.pprint")



* * *

### allow_partial cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.allow_partial "Permanent link")

Argument `allow_partial`.

* * *

### cash_dividends cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.cash_dividends "Permanent link")

Argument `cash_dividends`.

* * *

### direction cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.direction "Permanent link")

Argument `direction`.

* * *

### fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.fees "Permanent link")

Argument `fees`.

* * *

### ffill_val_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.ffill_val_price "Permanent link")

Argument `ffill_val_price`.

* * *

### fixed_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.fixed_fees "Permanent link")

Argument `fixed_fees`.

* * *

### from_ago cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.from_ago "Permanent link")

Argument `from_ago`.

* * *

### leverage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.leverage "Permanent link")

Argument `leverage`.

* * *

### leverage_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.leverage_mode "Permanent link")

Argument `leverage_mode`.

* * *

### log cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.log "Permanent link")

Argument `log`.

* * *

### max_log_records cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.max_log_records "Permanent link")

Argument `max_log_records`.

* * *

### max_order_records cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.max_order_records "Permanent link")

Argument `max_order_records`.

* * *

### max_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.max_size "Permanent link")

Argument `max_size`.

* * *

### min_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.min_size "Permanent link")

Argument `min_size`.

* * *

### price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.price "Permanent link")

Argument `price`.

* * *

### price_and_from_ago cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.price_and_from_ago "Permanent link")

Arguments `price` and `from_ago` after broadcasting.

* * *

### price_area_vio_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.price_area_vio_mode "Permanent link")

Argument `price_area_vio_mode`.

* * *

### raise_reject cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.raise_reject "Permanent link")

Argument `raise_reject`.

* * *

### reject_prob cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.reject_prob "Permanent link")

Argument `reject_prob`.

* * *

### save_returns cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.save_returns "Permanent link")

Argument `save_returns`.

* * *

### save_state cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.save_state "Permanent link")

Argument `save_state`.

* * *

### save_value cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.save_value "Permanent link")

Argument `save_value`.

* * *

### size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.size "Permanent link")

Argument `size`.

* * *

### size_granularity cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.size_granularity "Permanent link")

Argument `size_granularity`.

* * *

### size_type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.size_type "Permanent link")

Argument `size_type`.

* * *

### skip_empty cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.skip_empty "Permanent link")

Argument `skip_empty`.

* * *

### slippage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.slippage "Permanent link")

Argument `slippage`.

* * *

### update_value cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.update_value "Permanent link")

Argument `update_value`.

* * *

### val_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FOPreparer.val_price "Permanent link")

Argument `val_price`.

* * *

## FSPreparer class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L1176-L1810 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-13-1)FSPreparer(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-13-2)    arg_config=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-13-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-13-4))
    

Class for preparing [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals "vectorbtpro.portfolio.base.Portfolio.from_signals").

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [BasePFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer "vectorbtpro.portfolio.preparing.BasePFPreparer")
  * [BasePreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer "vectorbtpro.base.preparing.BasePreparer")
  * [Cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable "vectorbtpro.utils.caching.Cacheable")
  * [Chainable](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable "vectorbtpro.utils.chaining.Chainable")
  * [Comparable](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.Comparable "vectorbtpro.utils.checks.Comparable")
  * [Configured](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured "vectorbtpro.utils.config.Configured")
  * [HasSettings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings "vectorbtpro.utils.config.HasSettings")
  * [Pickleable](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable "vectorbtpro.utils.pickling.Pickleable")
  * [Prettified](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified "vectorbtpro.utils.formatting.Prettified")



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.portfolio.preparing.BasePFPreparer.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.portfolio.preparing.BasePFPreparer.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.portfolio.preparing.BasePFPreparer.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.portfolio.preparing.BasePFPreparer.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.portfolio.preparing.BasePFPreparer.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.portfolio.preparing.BasePFPreparer.find_messages")
  * [BasePFPreparer.align_pc_arr](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.align_pc_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.align_pc_arr")
  * [BasePFPreparer.args_to_broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.args_to_broadcast "vectorbtpro.portfolio.preparing.BasePFPreparer.args_to_broadcast")
  * [BasePFPreparer.attach_call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.attach_call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.attach_call_seq")
  * [BasePFPreparer.auto_call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_call_seq")
  * [BasePFPreparer.auto_sim_end](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_end "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_end")
  * [BasePFPreparer.auto_sim_start](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_start "vectorbtpro.portfolio.preparing.BasePFPreparer.auto_sim_start")
  * [BasePFPreparer.bm_close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.bm_close "vectorbtpro.portfolio.preparing.BasePFPreparer.bm_close")
  * [BasePFPreparer.broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_kwargs")
  * [BasePFPreparer.broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_named_args "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_named_args")
  * [BasePFPreparer.broadcast_result](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.broadcast_result "vectorbtpro.portfolio.preparing.BasePFPreparer.broadcast_result")
  * [BasePFPreparer.call_seq](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.call_seq "vectorbtpro.portfolio.preparing.BasePFPreparer.call_seq")
  * [BasePFPreparer.cash_deposits](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_deposits "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_deposits")
  * [BasePFPreparer.cash_earnings](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_earnings "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_earnings")
  * [BasePFPreparer.cash_sharing](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cash_sharing "vectorbtpro.portfolio.preparing.BasePFPreparer.cash_sharing")
  * [BasePFPreparer.chunked](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.chunked "vectorbtpro.portfolio.preparing.BasePFPreparer.chunked")
  * [BasePFPreparer.close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.close "vectorbtpro.portfolio.preparing.BasePFPreparer.close")
  * [BasePFPreparer.config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.config "vectorbtpro.portfolio.preparing.BasePFPreparer.config")
  * [BasePFPreparer.cs_group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.cs_group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.cs_group_lens")
  * [BasePFPreparer.data](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.data "vectorbtpro.portfolio.preparing.BasePFPreparer.data")
  * [BasePFPreparer.def_broadcast_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.def_broadcast_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.def_broadcast_kwargs")
  * [BasePFPreparer.find_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.find_target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.find_target_func")
  * [BasePFPreparer.freq](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.freq "vectorbtpro.portfolio.preparing.BasePFPreparer.freq")
  * [BasePFPreparer.group_by](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_by "vectorbtpro.portfolio.preparing.BasePFPreparer.group_by")
  * [BasePFPreparer.group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.group_lens")
  * [BasePFPreparer.high](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.high "vectorbtpro.portfolio.preparing.BasePFPreparer.high")
  * [BasePFPreparer.idx_setters](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.idx_setters "vectorbtpro.portfolio.preparing.BasePFPreparer.idx_setters")
  * [BasePFPreparer.in_outputs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.in_outputs "vectorbtpro.portfolio.preparing.BasePFPreparer.in_outputs")
  * [BasePFPreparer.index](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.index "vectorbtpro.portfolio.preparing.BasePFPreparer.index")
  * [BasePFPreparer.init_cash](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash "vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash")
  * [BasePFPreparer.init_cash_mode](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash_mode "vectorbtpro.portfolio.preparing.BasePFPreparer.init_cash_mode")
  * [BasePFPreparer.init_position](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_position "vectorbtpro.portfolio.preparing.BasePFPreparer.init_position")
  * [BasePFPreparer.init_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.init_price "vectorbtpro.portfolio.preparing.BasePFPreparer.init_price")
  * [BasePFPreparer.jitted](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.jitted "vectorbtpro.portfolio.preparing.BasePFPreparer.jitted")
  * [BasePFPreparer.keep_inout_flex](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.keep_inout_flex "vectorbtpro.portfolio.preparing.BasePFPreparer.keep_inout_flex")
  * [BasePFPreparer.low](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.low "vectorbtpro.portfolio.preparing.BasePFPreparer.low")
  * [BasePFPreparer.open](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.open "vectorbtpro.portfolio.preparing.BasePFPreparer.open")
  * [BasePFPreparer.parse_data](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.parse_data "vectorbtpro.portfolio.preparing.BasePFPreparer.parse_data")
  * [BasePFPreparer.pf_args](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.pf_args "vectorbtpro.portfolio.preparing.BasePFPreparer.pf_args")
  * [BasePFPreparer.post_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_args "vectorbtpro.portfolio.preparing.BasePFPreparer.post_args")
  * [BasePFPreparer.post_broadcast_named_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.post_broadcast_named_args "vectorbtpro.portfolio.preparing.BasePFPreparer.post_broadcast_named_args")
  * [BasePFPreparer.pre_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.pre_args "vectorbtpro.portfolio.preparing.BasePFPreparer.pre_args")
  * [BasePFPreparer.rec_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.rec_state "vectorbtpro.portfolio.preparing.BasePFPreparer.rec_state")
  * [BasePFPreparer.records](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.records "vectorbtpro.portfolio.preparing.BasePFPreparer.records")
  * [BasePFPreparer.result](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.result "vectorbtpro.portfolio.preparing.BasePFPreparer.result")
  * [BasePFPreparer.seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.seed "vectorbtpro.portfolio.preparing.BasePFPreparer.seed")
  * [BasePFPreparer.sim_end](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_end")
  * [BasePFPreparer.sim_group_lens](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_group_lens "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_group_lens")
  * [BasePFPreparer.sim_start](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start "vectorbtpro.portfolio.preparing.BasePFPreparer.sim_start")
  * [BasePFPreparer.staticized](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.staticized "vectorbtpro.portfolio.preparing.BasePFPreparer.staticized")
  * [BasePFPreparer.target_arg_map](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_arg_map "vectorbtpro.portfolio.preparing.BasePFPreparer.target_arg_map")
  * [BasePFPreparer.target_args](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_args "vectorbtpro.portfolio.preparing.BasePFPreparer.target_args")
  * [BasePFPreparer.target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.target_func")
  * [BasePFPreparer.target_shape](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.target_shape "vectorbtpro.portfolio.preparing.BasePFPreparer.target_shape")
  * [BasePFPreparer.wrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.wrapper "vectorbtpro.portfolio.preparing.BasePFPreparer.wrapper")
  * [BasePreparer.adapt_staticized_to_udf](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.adapt_staticized_to_udf "vectorbtpro.portfolio.preparing.BasePFPreparer.adapt_staticized_to_udf")
  * [BasePreparer.build_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.build_arg_config_doc "vectorbtpro.portfolio.preparing.BasePFPreparer.build_arg_config_doc")
  * [BasePreparer.dt_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.dt_arr_to_ns "vectorbtpro.portfolio.preparing.BasePFPreparer.dt_arr_to_ns")
  * [BasePreparer.get_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.get_arg")
  * [BasePreparer.get_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_arg_default "vectorbtpro.portfolio.preparing.BasePFPreparer.get_arg_default")
  * [BasePreparer.get_raw_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.get_raw_arg")
  * [BasePreparer.get_raw_arg_default](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.get_raw_arg_default "vectorbtpro.portfolio.preparing.BasePFPreparer.get_raw_arg_default")
  * [BasePreparer.map_enum_value](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.map_enum_value "vectorbtpro.portfolio.preparing.BasePFPreparer.map_enum_value")
  * [BasePreparer.override_arg_config_doc](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.override_arg_config_doc "vectorbtpro.portfolio.preparing.BasePFPreparer.override_arg_config_doc")
  * [BasePreparer.prepare_dt_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_dt_arr")
  * [BasePreparer.prepare_dt_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_dt_obj "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_dt_obj")
  * [BasePreparer.prepare_post_arg](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_post_arg "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_post_arg")
  * [BasePreparer.prepare_td_arr](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_arr "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_td_arr")
  * [BasePreparer.prepare_td_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.prepare_td_obj "vectorbtpro.portfolio.preparing.BasePFPreparer.prepare_td_obj")
  * [BasePreparer.resolve_dynamic_target_func](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.resolve_dynamic_target_func "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_dynamic_target_func")
  * [BasePreparer.set_seed](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.set_seed "vectorbtpro.portfolio.preparing.BasePFPreparer.set_seed")
  * [BasePreparer.td_arr_to_ns](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.td_arr_to_ns "vectorbtpro.portfolio.preparing.BasePFPreparer.td_arr_to_ns")
  * [BasePreparer.template_context](https://vectorbt.pro/pvt_7a467f6b/api/base/preparing/#vectorbtpro.base.preparing.BasePreparer.template_context "vectorbtpro.base.preparing.BasePreparer.template_context")
  * [Cacheable.get_ca_setup](https://vectorbt.pro/pvt_7a467f6b/api/utils/caching/#vectorbtpro.utils.caching.Cacheable.get_ca_setup "vectorbtpro.portfolio.preparing.BasePFPreparer.get_ca_setup")
  * [Chainable.chain](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.chain "vectorbtpro.portfolio.preparing.BasePFPreparer.chain")
  * [Chainable.pipe](https://vectorbt.pro/pvt_7a467f6b/api/utils/chaining/#vectorbtpro.utils.chaining.Chainable.pipe "vectorbtpro.portfolio.preparing.BasePFPreparer.pipe")
  * [Configured.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.copy "vectorbtpro.portfolio.preparing.BasePFPreparer.copy")
  * [Configured.equals](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.equals "vectorbtpro.portfolio.preparing.BasePFPreparer.equals")
  * [Configured.get_writeable_attrs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_writeable_attrs "vectorbtpro.portfolio.preparing.BasePFPreparer.get_writeable_attrs")
  * [Configured.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.prettify "vectorbtpro.portfolio.preparing.BasePFPreparer.prettify")
  * [Configured.replace](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.replace "vectorbtpro.portfolio.preparing.BasePFPreparer.replace")
  * [Configured.resolve_merge_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.resolve_merge_kwargs "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_merge_kwargs")
  * [Configured.update_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.update_config "vectorbtpro.portfolio.preparing.BasePFPreparer.update_config")
  * [HasSettings.get_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.get_path_setting")
  * [HasSettings.get_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_path_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.get_path_settings")
  * [HasSettings.get_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.get_setting")
  * [HasSettings.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.get_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.get_settings")
  * [HasSettings.has_path_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.has_path_setting")
  * [HasSettings.has_path_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_path_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.has_path_settings")
  * [HasSettings.has_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.has_setting")
  * [HasSettings.has_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.has_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.has_settings")
  * [HasSettings.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.reset_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.reset_settings")
  * [HasSettings.resolve_setting](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_setting "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_setting")
  * [HasSettings.resolve_settings_paths](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.resolve_settings_paths "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_settings_paths")
  * [HasSettings.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.HasSettings.set_settings "vectorbtpro.portfolio.preparing.BasePFPreparer.set_settings")
  * [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config "vectorbtpro.portfolio.preparing.BasePFPreparer.decode_config")
  * [Pickleable.decode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config_node "vectorbtpro.portfolio.preparing.BasePFPreparer.decode_config_node")
  * [Pickleable.dumps](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.dumps "vectorbtpro.portfolio.preparing.BasePFPreparer.dumps")
  * [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config "vectorbtpro.portfolio.preparing.BasePFPreparer.encode_config")
  * [Pickleable.encode_config_node](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config_node "vectorbtpro.portfolio.preparing.BasePFPreparer.encode_config_node")
  * [Pickleable.file_exists](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.file_exists "vectorbtpro.portfolio.preparing.BasePFPreparer.file_exists")
  * [Pickleable.getsize](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.getsize "vectorbtpro.portfolio.preparing.BasePFPreparer.getsize")
  * [Pickleable.load](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.load "vectorbtpro.portfolio.preparing.BasePFPreparer.load")
  * [Pickleable.loads](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.loads "vectorbtpro.portfolio.preparing.BasePFPreparer.loads")
  * [Pickleable.modify_state](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.modify_state "vectorbtpro.portfolio.preparing.BasePFPreparer.modify_state")
  * [Pickleable.resolve_file_path](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.resolve_file_path "vectorbtpro.portfolio.preparing.BasePFPreparer.resolve_file_path")
  * [Pickleable.save](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.save "vectorbtpro.portfolio.preparing.BasePFPreparer.save")
  * [Prettified.pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.Prettified.pprint "vectorbtpro.portfolio.preparing.BasePFPreparer.pprint")



* * *

### accumulate cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.accumulate "Permanent link")

Argument `accumulate`.

* * *

### adjust_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.adjust_args "Permanent link")

Argument `adjust_args`.

* * *

### adjust_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.adjust_func_nb "Permanent link")

Argument `adjust_func_nb`.

* * *

### allow_partial cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.allow_partial "Permanent link")

Argument `allow_partial`.

* * *

### basic_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.basic_mode "Permanent link")

Whether the basic mode is enabled.

* * *

### cash_dividends cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.cash_dividends "Permanent link")

Argument `cash_dividends`.

* * *

### combined_mask cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.combined_mask "Permanent link")

Signals combined using the OR rule into a mask.

* * *

### delta_format cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.delta_format "Permanent link")

Argument `delta_format`.

* * *

### direction cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.direction "Permanent link")

Argument `direction`.

* * *

### dt_stop cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.dt_stop "Permanent link")

Argument `dt_stop`.

* * *

### dynamic_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.dynamic_mode "Permanent link")

Whether the dynamic mode is enabled.

* * *

### entries cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.entries "Permanent link")

Argument `entries`.

* * *

### exits cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.exits "Permanent link")

Argument `exits`.

* * *

### explicit_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.explicit_mode "Permanent link")

Whether the explicit mode is enabled.

* * *

### fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.fees "Permanent link")

Argument `fees`.

* * *

### ffill_val_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.ffill_val_price "Permanent link")

Argument `ffill_val_price`.

* * *

### fill_pos_info cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.fill_pos_info "Permanent link")

Argument `fill_pos_info`.

* * *

### fixed_fees cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.fixed_fees "Permanent link")

Argument `fixed_fees`.

* * *

### from_ago cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.from_ago "Permanent link")

Argument `from_ago`.

* * *

### implicit_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.implicit_mode "Permanent link")

Whether the explicit mode is enabled.

* * *

### init_in_outputs class method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L1389-L1410 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.init_in_outputs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-14-1)FSPreparer.init_in_outputs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-14-2)    wrapper,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-14-3)    group_lens=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-14-4)    cash_sharing=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-14-5)    save_state=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-14-6)    save_value=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-14-7)    save_returns=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-14-8))
    

Initialize [FSInOutputs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.FSInOutputs "vectorbtpro.portfolio.enums.FSInOutputs").

* * *

### leverage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.leverage "Permanent link")

Argument `leverage`.

* * *

### leverage_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.leverage_mode "Permanent link")

Argument `leverage_mode`.

* * *

### limit_delta cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.limit_delta "Permanent link")

Argument `limit_delta`.

* * *

### limit_expiry cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.limit_expiry "Permanent link")

Argument `limit_expiry`.

* * *

### limit_order_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.limit_order_price "Permanent link")

Argument `limit_order_price`.

* * *

### limit_reverse cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.limit_reverse "Permanent link")

Argument `limit_reverse`.

* * *

### limit_tif cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.limit_tif "Permanent link")

Argument `limit_tif`.

* * *

### log cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.log "Permanent link")

Argument `log`.

* * *

### long_entries cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.long_entries "Permanent link")

Argument `long_entries`.

* * *

### long_exits cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.long_exits "Permanent link")

Argument `long_exits`.

* * *

### ls_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.ls_mode "Permanent link")

Whether direction-aware mode is enabled.

* * *

### max_log_records cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.max_log_records "Permanent link")

Argument `max_log_records`.

* * *

### max_order_records cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.max_order_records "Permanent link")

Argument `max_order_records`.

* * *

### max_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.max_size "Permanent link")

Argument `max_size`.

* * *

### min_size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.min_size "Permanent link")

Argument `min_size`.

* * *

### order_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.order_mode "Permanent link")

Argument `order_mode`.

* * *

### order_type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.order_type "Permanent link")

Argument `order_type`.

* * *

### post_segment_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.post_segment_args "Permanent link")

Argument `post_segment_args`.

* * *

### post_segment_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.post_segment_func_nb "Permanent link")

Argument `post_segment_func_nb`.

* * *

### post_signal_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.post_signal_args "Permanent link")

Argument `post_signal_args`.

* * *

### post_signal_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.post_signal_func_nb "Permanent link")

Argument `post_signal_func_nb`.

* * *

### price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.price "Permanent link")

Argument `price`.

* * *

### price_and_from_ago cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.price_and_from_ago "Permanent link")

Arguments `price` and `from_ago` after broadcasting.

* * *

### price_area_vio_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.price_area_vio_mode "Permanent link")

Argument `price_area_vio_mode`.

* * *

### raise_reject cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.raise_reject "Permanent link")

Argument `raise_reject`.

* * *

### reject_prob cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.reject_prob "Permanent link")

Argument `reject_prob`.

* * *

### save_returns cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.save_returns "Permanent link")

Argument `save_returns`.

* * *

### save_state cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.save_state "Permanent link")

Argument `save_state`.

* * *

### save_value cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.save_value "Permanent link")

Argument `save_value`.

* * *

### short_entries cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.short_entries "Permanent link")

Argument `short_entries`.

* * *

### short_exits cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.short_exits "Permanent link")

Argument `short_exits`.

* * *

### signal_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.signal_args "Permanent link")

Argument `signal_args`.

* * *

### signal_func_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.signal_func_mode "Permanent link")

Whether signal function mode is enabled.

* * *

### signal_func_nb cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.signal_func_nb "Permanent link")

Argument `signal_func_nb`.

* * *

### signals cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.signals "Permanent link")

Arguments `entries`, `exits`, `short_entries`, and `short_exits` after broadcasting.

* * *

### signals_mode cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.signals_mode "Permanent link")

Whether signals mode is enabled.

* * *

### size cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.size "Permanent link")

Argument `size`.

* * *

### size_granularity cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.size_granularity "Permanent link")

Argument `size_granularity`.

* * *

### size_type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.size_type "Permanent link")

Argument `size_type`.

* * *

### skip_empty cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.skip_empty "Permanent link")

Argument `skip_empty`.

* * *

### sl_stop cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.sl_stop "Permanent link")

Argument `sl_stop`.

* * *

### slippage cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.slippage "Permanent link")

Argument `slippage`.

* * *

### stop_entry_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.stop_entry_price "Permanent link")

Argument `stop_entry_price`.

* * *

### stop_exit_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.stop_exit_price "Permanent link")

Argument `stop_exit_price`.

* * *

### stop_exit_type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.stop_exit_type "Permanent link")

Argument `stop_exit_type`.

* * *

### stop_ladder cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.stop_ladder "Permanent link")

Argument `stop_ladder`.

* * *

### stop_limit_delta cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.stop_limit_delta "Permanent link")

Argument `stop_limit_delta`.

* * *

### stop_order_type cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.stop_order_type "Permanent link")

Argument `stop_order_type`.

* * *

### td_stop cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.td_stop "Permanent link")

Argument `td_stop`.

* * *

### time_delta_format cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.time_delta_format "Permanent link")

Argument `time_delta_format`.

* * *

### tp_stop cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.tp_stop "Permanent link")

Argument `tp_stop`.

* * *

### tsl_stop cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.tsl_stop "Permanent link")

Argument `tsl_stop`.

* * *

### tsl_th cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.tsl_th "Permanent link")

Argument `tsl_th`.

* * *

### update_value cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.update_value "Permanent link")

Argument `update_value`.

* * *

### upon_adj_limit_conflict cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_adj_limit_conflict "Permanent link")

Argument `upon_adj_limit_conflict`.

* * *

### upon_adj_stop_conflict cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_adj_stop_conflict "Permanent link")

Argument `upon_adj_stop_conflict`.

* * *

### upon_dir_conflict cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_dir_conflict "Permanent link")

Argument `upon_dir_conflict`.

* * *

### upon_long_conflict cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_long_conflict "Permanent link")

Argument `upon_long_conflict`.

* * *

### upon_opp_limit_conflict cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_opp_limit_conflict "Permanent link")

Argument `upon_opp_limit_conflict`.

* * *

### upon_opp_stop_conflict cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_opp_stop_conflict "Permanent link")

Argument `upon_opp_stop_conflict`.

* * *

### upon_opposite_entry cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_opposite_entry "Permanent link")

Argument `upon_opposite_entry`.

* * *

### upon_short_conflict cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_short_conflict "Permanent link")

Argument `upon_short_conflict`.

* * *

### upon_stop_update cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.upon_stop_update "Permanent link")

Argument `upon_stop_update`.

* * *

### use_limit_orders cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.use_limit_orders "Permanent link")

Whether to use limit orders.

* * *

### use_stops cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.use_stops "Permanent link")

Argument `use_stops`.

* * *

### val_price cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.FSPreparer.val_price "Permanent link")

Argument `val_price`.

* * *

## PFPrepResult class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py#L71-L102 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.PFPrepResult "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-15-1)PFPrepResult(
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-15-2)    target_func=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-15-3)    target_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-15-4)    pf_args=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-15-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#__codelineno-15-6))
    

Result of preparation.

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

### pf_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.PFPrepResult.pf_args "Permanent link")

Portfolio arguments.

* * *

### target_args cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.PFPrepResult.target_args "Permanent link")

Target arguments.

* * *

### target_func cached_property[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/portfolio/preparing.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/preparing/#vectorbtpro.portfolio.preparing.PFPrepResult.target_func "Permanent link")

Target function.
