# Release notes for 2021[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#release-notes-for-2021 "Permanent link")

All notable changes in reverse chronological order.


# Version 1.0.2 (31 Dec, 2021)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#version-102-31-dec-2021 "Permanent link")

 * Added Alpaca data source ([#31](https://github.com/polakowo/vectorbt.pro/issues/31 "GitHub Issue: polakowo/vectorbt.pro #31")). In contrast to the open-source version, additionally allows passing a pre-configured REST object to the [AlpacaData.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/alpaca/#vectorbtpro.data.custom.alpaca.AlpacaData.pull) method.
 * Changed the default index field of [EntryTrades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades) from `exit_idx` to `entry_idx`
 * Dropped JSON and implemented a custom formatting engine that represents objects in Python format. This perfectly aligns with the switch to dataclasses VBT has made. Here's a comparison of a wrapper being printed out by the open-source version and JSON, and VBT with the new engine:

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-1)ArrayWrapper(**Config({
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-2) "index": "<RangeIndex at 0x1045815e8> of shape (3,)",
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-3) "columns": "<Int64Index at 0x1045815e8> of shape (1,)",
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-4) "ndim": 1,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-5) "freq": null,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-6) "column_only_select": null,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-7) "group_select": null,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-8) "grouped_ndim": null,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-9) "group_by": null,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-10) "allow_enable": true,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-11) "allow_disable": true,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-12) "allow_modify": true
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-0-13)}))
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-1)ArrayWrapper(
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-2) index=<RangeIndex at 0x1045815e8 of shape (3,)>,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-3) columns=<Int64Index at 0x1045815e8 of shape (1,)>,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-4) ndim=1,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-5) freq=None,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-6) column_only_select=None,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-7) group_select=None,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-8) grouped_ndim=None,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-9) grouper=Grouper(
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-10) index=<Int64Index at 0x1045815e8 of shape (1,)>,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-11) group_by=None,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-12) allow_enable=True,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-13) allow_disable=True,
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-14) allow_modify=True
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-15) )
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#__codelineno-1-16))
 
[/code]


# Version 1.0.1 (21 Dec, 2021)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#version-101-21-dec-2021 "Permanent link")

 * Adapted the codebase to the new documentation format
 * Upgraded the documentation website generator from pdoc3 to MkDocs (Material Insiders). API is being automatically converted to Markdown files by a modified version of pdoc3 that resides in a private repository of [@polakowo](https://github.com/polakowo "GitHub User: polakowo").


# Version 1.0.0 (13 Dec, 2021)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#version-100-13-dec-2021 "Permanent link")

Info

This section briefly describes major changes made to the open-source version. For more details, see commits.


# Execution[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#execution "Permanent link")

 * Parallelized most functions that take 2-dimensional arrays using [Explicit Parallel Loops](https://numba.pydata.org/numba-doc/0.37.0/user/parallel.html#explicit-parallel-loops)
 * Built an infrastructure for chunking. Any Python function can be wrapped with the [@chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked) decorator, which returns a new function with the identical signature but capable of 1) splitting passed positional and keyword arguments into multiple chunks, 2) executing each chunk of arguments using the wrapped function, and 3) merging back the results. The rules by which the arguments are split and the results are merged must be explicitly provided using `arg_take_spec` and `merge_func` respectively. The chunk taking and merging specification is provided to most of the Numba-compiled functions that take 2-dimensional arrays. To only chunk functions by request, the decorator [register_chunkable](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.register_chunkable) was created, which leaves the Python function unwrapped and registers a so-called "setup" with all specifications by the global registry [ChunkableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ch_registry/#vectorbtpro.registries.ch_registry.ChunkableRegistry). Additionally, there are multiple present engines for executing chunks: [SerialEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine) (a simple queue), [DaskEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.DaskEngine) (mainly for multithreading), and [RayEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.RayEngine) (mainly for multiprocessing).
 * Built an infrastructure for wrapping and running JIT-able functions. At the heart of it is the [register_jitted](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.register_jitted) decorator, which registers a Python function and the instructions on how to JIT compile it at the global registry [JITRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/jit_registry/#vectorbtpro.registries.jit_registry.JITRegistry). The registry, once instructed, finds the function's setup and passes the function to a jitting class (aka "jitter") for wrapping. Preset jitters include [NumPyJitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumPyJitter) for NumPy implementations and [NumbaJitter](https://vectorbt.pro/pvt_7a467f6b/api/utils/jitting/#vectorbtpro.utils.jitting.NumbaJitter) for Numba-compiled functions. The registry can also register tasks (by task id) and capture multiple jitter candidates for the same task. The user can then switch between different implementations by specifying `jitter`.


# Generic[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#generic "Permanent link")

 * Refactored many methods that take UDFs (such as [GenericAccessor.rolling_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_apply)) by converting each into both a class (meta) and an instance (regular) method using [class_or_instancemethod](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.class_or_instancemethod). If the method was called on an instance, its UDFs do not have to take any metadata apart from (a part of) the array, such as `apply_func_nb(window, *args)`. If the method was called on the class, it iterates over an abstract shape and its UDFs must take metadata of each iteration, which can be used to select a part of any custom array passed as a variable argument, such as `apply_func_nb(from_i, to_i, col, *args)`. Previously, UDFs had to accept both the metadata and the array, even if the metadata was not used.
 * Most of the functions that take custom UDFs and variable arguments, such as [GenericAccessor.rolling_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_apply), received support for [utils.templates](https://vectorbt.pro/pvt_7a467f6b/api/utils/template/). The same goes for broadcasting named arguments - a practice initially introduced in [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio).
 * Made crossovers more resilient to NaN and moved them to [GenericAccessor.crossed_above](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_above) and [GenericAccessor.crossed_below](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.crossed_below)
 * Added [BaseAccessor.eval](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.eval), which is similar to `pd.eval` but broadcasts inputs prior to evaluation and can switch between NumPy and NumExpr
 * Improved conflict control in [MappedArray](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray). Multiple elements pointing to the same timestamp can be reduced using [Mapped.reduce_segments](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.reduce_segments). They can also be safely converted to Pandas by repeating index.
 * Made tolerance checks and values for Numba math functions such as [is_less_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/math_/#vectorbtpro.utils.math_.is_less_nb) globally adjustable. Disabling tolerance checks increases performance but can lead to round-off errors.
 * Implemented context managers for profiling time ([Timer](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.Timer)) and memory ([MemTracer](https://vectorbt.pro/pvt_7a467f6b/api/utils/profiling/#vectorbtpro.utils.profiling.MemTracer))
 * Added support for [Scattergl](https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Scattergl.html) for plotting big datasets with increased speed. Used by default on more than 10,000 points.


# Broadcasting[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#broadcasting "Permanent link")

 * Refactored broadcasting mechanism inside of [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast). Added [BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO) dataclass, whose instances can be passed to change broadcasting behavior for individual objects. Introduced a possibility to build a Cartesian product of scalar-like parameters and other broadcastable objects (both using `BCO` and `pd.Index` as a shortcut) using operation trees and [generate_param_combs](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.generate_param_combs). Additionally, a random subset of parameter combinations can be automatically selected to emulate random search. [Default](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Default) and [Ref](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.Ref) and the surrounding logic were moved to this module.


# Data[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#data "Permanent link")

 * Implemented data classes for working with local files: [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) for CSV files and [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData) for HDF files and keys. Both support efficient updates without having to read the entire file. To make this possible, symbol fetching methods can return a state, which are preserved for the use in data updates.
 * Refactored [RandomData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/random/#vectorbtpro.data.custom.random.RandomData) and [GBMData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/gbm/#vectorbtpro.data.custom.gbm.GBMData)
 * Better handling of missing data. Made [BinanceData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/binance/#vectorbtpro.data.custom.binance.BinanceData) and [CCXTData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/ccxt/#vectorbtpro.data.custom.ccxt.CCXTData) more error-resilient: in case of connectivity issues, data won't be lost but returned, so it can be updated later.
 * Moved progress bar logic into a separate module to standardize handling of all progress bars across vectorbt. Added progress bar for symbols in [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data).
 * Renamed `download` to `fetch` everywhere since not all data sources reside online


# Portfolio[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#portfolio "Permanent link")

 * Added a new simulation method [Portfolio.from_def_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_def_order_func) that combines [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) and [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func). It uses a custom order function to transform array-like objects into orders and allows attaching and overriding user-defined callbacks to change and monitor simulation.
 * Added support for in-output simulation objects. Instead of creating various arrays during the simulation, they can be manually created by the user (or automatically created and broadcasted by utilizing templates) outside the simulation, passed as regular arguments, and modified in-place. They are then conveniently stored in [Portfolio.in_outputs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.in_outputs) for further analysis. In addition, [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) can detect when an in-output array shadows a regular portfolio attribute and takes this array instead of reconstructing the attribute, which is the new way to efficiently precompute various artifacts such as returns.
 * Implemented shortcut properties for [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) and [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records), which are cacheable properties that call their respective getter methods with default arguments. This enables dot notation such as `pf.trades.winning.pnl.count()`, where `trades` and `winning` are cached properties that call the [Portfolio.get_trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.get_trades) and [Trades.get_winning](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_winning) method respectively. In [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio), shortcut properties can also utilize in-outputs.
 * Made various portfolio attributes (such as [Portfolio.get_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.get_returns)) flexible by converting each into both a class and an instance method using [class_or_instancemethod](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.class_or_instancemethod). If the method was called on the class, the operation is run using the passed arguments only. If the method was called on an instance, the operation is run on the data from the instance, which can be overridden by setting any of the arguments.
 * Introduced extra validation of arguments passed to simulation. For instance, passing arrays that look boolean but have object data type raises an (informative) error.
 * Not only [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) but all the simulation functions accept `open`, `high`, and `low` (all optional). This enables various interesting automatisms: order price of `-np.inf` gets automatically replaced by the opening price and `np.inf` (default everywhere) by the closing price. The highest and lowest prices are being used for bar boundary checks.
 * Added the following arguments:
 * `cash_deposits`: cash deposits/withdrawals at the beginning of each time step
 * `cash_earnings`: cash earnings (independent of position) at the end of each time step
 * `cash_dividends`: dividends (relative to position) at the end of each time step
 * `init_position`: the initial position
 * `stop_signal_priority`: which signal to prioritize: stop or user?
 * Allowed price of `0`. This allows for P&L-effective insertion and removal of cash and assets. For instance, to periodically charge a fee, one can create a range of orders with zero price and non-zero fees. They are visible as regular trades and appear in records.
 * Allowed `max_order_records=0` and `max_log_records=0` to disable filling records - for example, if the performance is assessed during the simulation and there is no need to save this data for post-simulation analysis. Also, for parallelization reasons, both of the numbers refer to the maximal number of records **per column** rather than per entire input.
 * Allowed negative fees (-0.05 means that you earn 0.05% per trade instead of paying a fee)
 * Converted simulation outputs to named tuples of type [SimulationOutput](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.SimulationOutput)


# Returns[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#returns "Permanent link")

 * Updated metrics based on returns to take into account datetime-like properties. For instance, having two data points with the timestamps "2020-01-01" and "2021-01-01" are considered as a full year rather than 2 days as it was previously. See [ArrayWrapper.dt_period](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.dt_period).
 * Rolling metrics such as [ReturnsAccessor.rolling_sortino_ratio](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor.rolling_sortino_ratio) were made much faster by refactoring their Numba-compiled functions


# Caching[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#caching "Permanent link")

 * Completely refactored caching. Previously, caching was managed by specialized property and method decorators. Once the user invoked such a property or method, it checked for global settings to see whether it's blacklisted, and stored the cache on the instance it's bound to. Cached attributes weren't easily discoverable, which led to less transparency. In the new approach, caching is being managed by a global registry [CacheableRegistry](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CacheableRegistry), which registers so-called "setups" for all cacheable objects, such as functions, properties, methods, instances, and even classes. They all build a well-connected hierarchy that can propagate actions. For instance, disabling caching in a class setup of type [CAClassSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CAClassSetup) will disable caching across all of its child setups, down to [CARunSetup](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CARunSetup), which takes care of actual caching. Cacheable decorators such as [cacheable](https://vectorbt.pro/pvt_7a467f6b/api/utils/decorators/#vectorbtpro.utils.decorators.cacheable) communicate with the registry and do all actions on their particular setup. The user can easily find the setup for any (cacheable) object to, for example, display various caching statistics.
 * Removed caching of attributes that return DataFrames (apart from a few exceptions) to avoid wasting memory


# Design[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2021/#design "Permanent link")

 * Restructured the project and reformatted the codebase. Most notably, Numba-compiled simulation functions were distributed across multiple modules.
 * Some previously required packages such as Plotly and Dill were made optional to make the core of vectorbt even more lightweight. Optional packages are tracked in [utils.opt_packages](https://vectorbt.pro/pvt_7a467f6b/api/utils/opt_packages/) and whenever a code that requires a package is accessed but the package is missing, an error is raised with instructions on how to install it.
 * Converted minimalistic classes to dataclasses using [attrs](https://www.attrs.org/en/stable/)
 * Refactored [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config), which shrank initialization time of various vectorbt objects by 25%. Config respects Liskov substitution principle and similar to a dict, can be initialized by using both positional and keyword arguments. Also, created read-only and hybrid preset classes to unify configs created across vectorbt.
 * Removed expected key checks, which makes subclassing vectorbt classes easier but removes dynamic checks of keyword arguments passed to the initializer (which is an overkill anyway)
 * Accessors were made cached by default (which can be changed in the settings) to avoid repeated initialization, and all options for changing data in-place were removed
 * Made [_settings](https://vectorbt.pro/pvt_7a467f6b/api/_settings/) more modular and better embeddable into documentation. Additionally, upon import, vectorbt looks for an environment variable that contains the path to a settings file and updates/replaces the current settings in-place.
 * Created and set up a private repository ![🎇](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f387.svg)