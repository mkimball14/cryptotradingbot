# Release notes for 2023[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#release-notes-for-2023 "Permanent link")

All notable changes in reverse chronological order.


# Version 2023.12.23[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-20231223 "Permanent link")

 * Implemented [DuckDBDataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DuckDBDataSaver) for periodically storing data in a DuckDB database
 * Fixed performance of [PathosEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine)
 * Fixed [fit_pattern_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/patterns/#vectorbtpro.generic.nb.patterns.fit_pattern_nb)
 * Fixed staticization in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals)
 * Implemented a merging function `"imageio"` that merges Plotly figures and generates and saves a GIF animation
 * UTC is no more the default timezone in [AVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/av/#vectorbtpro.data.custom.av.AVData)
 * Made all indicator packages optional in [IndicatorFactory.list_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_indicators)
 * Fixed processing of `benchmark` in [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter)
 * Custom indicator can now be registered with [IndicatorFactory.register_custom_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.register_custom_indicator), listed with [IndicatorFactory.list_custom_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_custom_indicators), and retrieved with [IndicatorFactory.get_custom_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.get_custom_indicator). Any registered custom indicator will be visible in [IndicatorFactory.list_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_indicators).
 * Outsourced creation of projection bands to [GenericDFAccessor.band](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.band)
 * Implemented a function [ptable](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.ptable) to pretty-print a DataFrame of any size. Displays HTML when run in a notebook.
 * Developed annotation functionality in [utils.annotations](https://vectorbt.pro/pvt_7a467f6b/api/utils/annotations/) that is now being used by many VBT parts to control behavior of function arguments
 * Chunk taking specification `arg_take_spec` can be parsed from function annotations
 * Sizer (argument `size` in [@chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked)) doesn't necessarily have to be provided anymore as it can be reliably parsed from most [ChunkTaker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkTaker) instances
 * Standardized merging functionality and created a new module [utils.merging](https://vectorbt.pro/pvt_7a467f6b/api/utils/merging/). Keyword arguments can now be distributed across multiple merging functions when provided as a tuple. Also, merging functions can be specified via annotations (strings work too!)
 * [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized) can parse [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) instances from function annotations
 * [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply) and its decorators can parse [Takeable](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Takeable) instances from function annotations
 * Refactored the chunking functionality by moving most of the logic from [@chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked) to a new class [Chunker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker), which stores the function to be chunked and the chunking configuration. By calling [Chunker.run](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker.run), the pipeline is run on the supplied arguments. Thus, the same pipeline can be run on different sets of arguments. The main reason for this class is that it can be easily subclassed to change the default chunking behavior; the new class can be passed (or set globally) as `chunker_cls`.
 * Developed new user-friendly classes for chunking, such as [ChunkedArray](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.ChunkedArray). They can be used in `arg_take_spec`, annotations, and even passed as arguments for the chunk taking specification to be parsed on the fly.
 * Argument `minp` in the exponential mean and standard deviation functions now refers to the minimum number of observations in `span`, rather than from the start as it was previously
 * [TVData.list_symbols](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVData.list_symbols) can optionally return other fields besides symbols
 * Fixed a DST issue that results in a duplicated index in [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter)
 * Standardized the process of searching for objects in arguments. This functionality resides in [utils.search](https://vectorbt.pro/pvt_7a467f6b/api/utils/search/) and is being used by parameterization and templating.
 * Similarly to [Chunker](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.Chunker) being based on [@chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked), there's now an equivalent class [Parameterizer](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Parameterizer) being based on [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized)
 * Extended [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params) to preferably generate parameter combinations lazily rather than to pick them from a (potentially large) materialized grid. This significantly reduces the overhead of generating parameter combinations when `random_subset` is provided. For example, if the user wants to select 10 random combinations from three parameters with 1000 values each, VBT won't build a grid of 1000000000 parameter combinations anymore ![👌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f44c.svg)
 * Adapted [AVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/av/#vectorbtpro.data.custom.av.AVData) to use [alpha_vantage](https://github.com/RomelTorres/alpha_vantage) library by default (if installed). The API documentation parser can still be used by passing `use_parser=True`.
 * Implemented a new data class [BentoData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/bento/#vectorbtpro.data.custom.bento.BentoData) for [Databento](https://databento.com/)
 * Fixed [SQLData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData) for Pandas < 2.0
 * Added functions [disable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.disable_caching) and [enable_caching](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.enable_caching) to globally disable and enable caching respectively. Also, implemented context managers [CachingDisabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingDisabled) and [CachingEnabled](https://vectorbt.pro/pvt_7a467f6b/api/registries/ca_registry/#vectorbtpro.registries.ca_registry.CachingEnabled) to disable and enable caching within a code block respectively. Optionally, they can take a class, instance, method, or any other cacheable object, and switch the caching behavior only for this particular object. Moreover, implemented so-called "caching rules" that can be registered globally and applied to any new setups automatically, making passive cache management possible (up to now, rules could be enforced only to setups that were already registered). Finally, renamed any methods with the suffix `status` or `status_overview` to just `stats`.
 * [NDLData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/ndl/#vectorbtpro.data.custom.ndl.NDLData) supports datatables by passing `data_format="datatable"`
 * Wrote [Forecast future price trends (with projections)](https://pyquantnews.com/forecast-future-price-trends-with-projections/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)
 * Wrote [Easily cross-validate parameters to boost your trading strategy](https://pyquantnews.com/easily-cross-validate-parameters-boost-strategy/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 2023.10.20[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-20231020 "Permanent link")

 * Implemented [Data.to_feather](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_feather) for storing data in Feather files and [FeatherData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/feather/#vectorbtpro.data.custom.feather.FeatherData) for loading data from Feather files using PyArrow
 * Implemented [Data.to_parquet](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_parquet) for storing data in Parquet files and [ParquetData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/parquet/#vectorbtpro.data.custom.parquet.ParquetData) for loading data from Parquet files using PyArrow or FastParquet
 * Implemented [Data.to_sql](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_sql) for storing data in a SQL database, [SQLDataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.SQLDataSaver) for periodically storing data in a SQL database, and [SQLData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/sql/#vectorbtpro.data.custom.sql.SQLData) for loading data from a SQL database using SQLAlchemy
 * Implemented [Data.to_duckdb](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_duckdb) for storing data in a DuckDB database and [DuckDBData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/duckdb/#vectorbtpro.data.custom.duckdb.DuckDBData) for loading data from a DuckDB database
 * Implemented [Data.sql](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.sql) to run analytical SQL queries on entire data instances using DuckDB
 * Improved file discovery in [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) and [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData)
 * Extended the market scanning functionality of [TVClient](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVClient) to allow filtering by market(s) as well as additional information such as capitalization
 * Redesigned [Data.transform](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.transform) to attach correct feature/symbol classes depending on the selected mode
 * Redesigned setting resolution in various classes
 * Added a new execution engine [MpireEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.MpireEngine) based on [mpire](https://github.com/sybrenjansen/mpire)
 * Refactored some execution engines such as [PathosEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine)
 * Implemented classes methods [PortfolioOptimizer.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.row_stack) and [PortfolioOptimizer.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.column_stack)
 * Optimized [PortfolioOptimizer.from_allocations](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocations) and added [PortfolioOptimizer.from_initial](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_initial)
 * Added an option `settings.plotting.auto_rangebreaks` to automatically skip date ranges with no data when plotting with `fig.show`, `fig.show_png`, and `fig.show_svg`
 * Added an argument `fit_ranges` in [PatternRanges.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.plot) to zoom in on one or more ranges
 * State, value, and returns can be saved in dynamic from-signals as well
 * Fixed [SIGDET](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/sigdet/#vectorbtpro.indicators.custom.sigdet.SIGDET) on two-dimensional data
 * Fixed division-by-zero errors in pattern similarity calculation
 * Renamed `latest_at_index` to `realign`, `resample_opening` to `realign_opening`, and `resample_closing` to `realign_closing`
 * Added support for [Blosc2](https://github.com/Blosc/python-blosc2) as the new default Blosc implementation
 * Added option `HardStop` in [StopExitPrice](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.StopExitPrice) to ignore open price check when executing a stop order
 * Fixed Common Sense Ratio ([ReturnsAccessor.common_sense_ratio](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor.common_sense_ratio))
 * Implemented a method to resample returns - [ReturnsAccessor.resample_returns](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor.resample_returns)
 * Fixed merging when a single object is passed
 * Enabled negative `cash_earnings` to be lower than the current (free) cash balance
 * Made parsing of timestamps and datetime indexes with `dateparser` optional
 * Added an option `settings.importing.clear_pycache` to clear Python cache on startup
 * Optimized accessors to initialize a [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping) instance only once
 * Fixed parsing of `technical` indicators
 * Fixed and redesigned selection based on datetime components. Slices such as `"14:30":"15:45"` are working properly now.
 * Switched to date based release segments
 * Migrated from `setup.py` to `pyproject.toml`


# Version 1.14.0 (1 Sep, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1140-1-sep-2023 "Permanent link")

 * Optimized simulation methods for better performance. Both [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) and [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) have become faster when the number of orders/signals is relatively low. This is achieved by letting them not execute a large chunk of the simulation logic whenever a NaN order or no signal is encountered. 
 * Implemented an ultrafast simulation method based on signals - [from_basic_signals_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/from_signals/#vectorbtpro.portfolio.nb.from_signals.from_basic_signals_nb) \- which is used automatically if you don't use stop and limit orders
 * Implemented a module [portfolio.nb.ctx_helpers](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/ctx_helpers/) with helper functions to be used in callbacks such as `signal_func_nb`. For example, to get the current SL target price use `vbt.pf_nb.get_sl_target_price_nb(c)`.
 * Introduced a new callback `post_signal_func_nb` to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals). Identically to `post_order_func_nb` in [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func), it gets called right after an order has been executed, regardless of its success.
 * Adjustment function now also runs in [Portfolio.from_holding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_holding)
 * Renamed `max_orders` to `max_order_records` and `max_logs` to `max_log_records` in [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio)
 * Introduced an argument `ignore_errors` to ignore just about any error when optimizing with PyPortfolioOpt and Riskfolio-Lib
 * Implemented a new [Splitter.from_n_rolling](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_n_rolling) configuration that by taking `length="optimize"` optimizes the window length with SciPy such that splits cover the most of the index and test ranges don't overlap (or any other set specified via `optimize_anchor_set`)
 * Renamed `skip_minus_one` to `skip_not_found` in point- and range-based indexing
 * Added the following 4 callbacks to [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute):
 * `pre_execute_func`: gets called only once before executing all calls/chunks
 * `pre_chunk_func`: gets called before executing a chunk (chunking must be enabled!)
 * `post_chunk_func`: gets called after executing a chunk (chunking must be enabled!)
 * `post_execute_func`: gets called only once after executing all calls/chunks
 * [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized), [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply) (along with the corresponding decorators), and [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run) allow the function to return `vbt.NoResult` for any iteration that should be skipped
 * Redesigned custom indicators ![🏁](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f3c1.svg)
 * Each indicator now has a 1-dimensional Numba-compiled function and the corresponding 2-dimensional parallelizable, chunkable function. The latter function also accepts parameters as flexible arrays, which makes possible providing one parameter value per column.
 * Removed the caching functionality to avoid too much specialization
 * Indicator classes were outsourced into their respective modules under the new sub-package [indicators.custom](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/)
 * Implemented an [ADX](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/adx/#vectorbtpro.indicators.custom.adx.ADX) indicator
 * To quickly run and plot a TA-Lib indicator on a single set of parameter values without using the indicator factory, [talib_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/talib_/#vectorbtpro.indicators.talib.talib_func) and [talib_plot_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/talib_/#vectorbtpro.indicators.talib.talib_plot_func) can be used. They take the name of an indicator and return a function that can run/plot it. In contrast to the official TA-Lib implementation, they can properly handle DataFrames, NaNs, broadcasting, and resampling. The indicator factory's both `from_talib` and `from_expr` are based on these two functions.
 * All indicators implemented with [IndicatorFactory.with_apply_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_apply_func) accept the argument `split_columns` to run only one column at a time by retaining the dimensionality, and the argument `skipna` to automatically skip NaN (requires `split_columns`)
 * When passing a column full of NaN to TA-Lib, it will raise the "inputs are all NaN" error - no longer! It will simply return an output array full of NaN.
 * Indicators can return raw outputs instead of an indicator instance by passing the option `return_raw="outputs"`. It can be used to return NumPy arrays directly if the Pandas format is not needed, but also to return arrays of arbitrary shapes since wrapping is no more needed. It also has less overhead since the instance preparation step is skipped.
 * Fixed treatment of NaN in [IndicatorFactory.from_wqa101](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_wqa101)
 * Fixed the issue of not being able to run all World Quant Alpha indicators in one go (it's possible now)
 * Redesigned label generators ![🏁](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f3c1.svg)
 * Each generator now has a 1-dimensional Numba-compiled function and the corresponding 2-dimensional parallelizable, chunkable function. The latter function also accepts parameters as flexible arrays, which makes possible providing one parameter value per column.
 * Adapted the pivot generation function to be consistent with [PIVOTINFO](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/pivotinfo/#vectorbtpro.indicators.custom.pivotinfo.PIVOTINFO)
 * Most functions were adapted to accept `high` and `low` instead of just `close`. If you don't have `high` and `low`, pass `close` two times.
 * Generator classes were outsourced into their respective modules under the new sub-package [labels.generators](https://vectorbt.pro/pvt_7a467f6b/api/labels/generators/)
 * Redesigned signal generators ![🏁](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f3c1.svg)
 * Variable arguments such as `*args`were converted into regular arguments such as `place_args`
 * Generator classes were outsourced into their respective modules under the new sub-package [signals.generators](https://vectorbt.pro/pvt_7a467f6b/api/signals/generators/)
 * Implemented a method [SignalsAccessor.distance_from_last](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.distance_from_last) to measure the distance from the last n-th signal to the current element
 * Redesigned the [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) class ![🏁](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f3c1.svg)
 * Data and any accompanied information can be also stored by features rather than symbols by wrapping the dictionary with [feature_dict](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.feature_dict). In this case, the information is said to be feature-oriented where features are keys and symbols are columns. A data instance becomes feature-oriented if [Data.data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.data) is feature-oriented.
 * Behavior of features and symbols is interchangeable. For example, [Data.select](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.select) will select a symbol if the instance is symbol-oriented and a feature if the instance is feature-oriented, while indexing a column will select a feature if the instance is symbol-oriented and a symbol otherwise.
 * [Data.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.pull) can run [Data.fetch_feature](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.fetch_feature) to fetch features instead of symbols, same for [Data.update](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.update). To switch to features, pass `keys` (first argument) with `keys_are_features=True` or `features`.
 * Any instance can be switched to the opposite orientation with [Data.invert](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.invert)
 * Renamed the method `Data.fetch` to `Data.pull` since fetching is just downloading while pulling involves merging. The method `Data.fetch` still exists for backward compatibility and calls the new `Data.pull` under the hood.
 * Renamed `column_config` to `feature_config` since columns are symbols in a feature-oriented instance
 * Renamed `single_symbol` to `single_key` since keys are features in a feature-oriented instance
 * Renamed `symbol_classes` to `classes` since keys are features in a feature-oriented instance
 * Data classes were outsourced into their respective modules under the new sub-package [data.custom](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/)
 * Redesigned unit tests for more extensive testing
 * [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run) uses [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) to run a sequence of functions. This can be used to parallelize feature engineering.
 * Removed hard-coded timeframes from [TVClient](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVClient) to be able to use custom timeframes such as "30 seconds"
 * Token argument in [TVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVData) has been renamed from just `token` to `auth_token` to be consistent with TradingView
 * [OHLCVDFAccessor](https://vectorbt.pro/pvt_7a467f6b/api/ohlcv/accessors/#vectorbtpro.ohlcv.accessors.OHLCVDFAccessor) and [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) share the same functionality for managing OHLCV-based features - no more duplicated code. Also, `column_map` has been renamed to `feature_map` and now works in the opposite way: custom column names must point to standardized column names.
 * Split [OHLCVDFAccessor.plot](https://vectorbt.pro/pvt_7a467f6b/api/ohlcv/accessors/#vectorbtpro.ohlcv.accessors.OHLCVDFAccessor.plot) to [OHLCVDFAccessor.plot_ohlc](https://vectorbt.pro/pvt_7a467f6b/api/ohlcv/accessors/#vectorbtpro.ohlcv.accessors.OHLCVDFAccessor.plot_ohlc) and [OHLCVDFAccessor.plot_volume](https://vectorbt.pro/pvt_7a467f6b/api/ohlcv/accessors/#vectorbtpro.ohlcv.accessors.OHLCVDFAccessor.plot_volume)
 * A custom function located under `vbt.settings.plotting.pre_show_func` can be called on a figure each time before a figure is shown. Useful for figure preparations.
 * New debugging tool: to check how two complex VBT objects differ, use `obj1.equals(obj2, debug=True)`
 * Fixed issues with time-based stop orders for 32-bit Python on Windows


# Version 1.13.1 (10 Jul, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1131-10-jul-2023 "Permanent link")

 * Enabled changing `cash_sharing` in [Portfolio.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.column_stack)
 * Removed the size types `MNTargetValue`, `MNTargetPercent`, and `MNTargetPercent100`. The corresponding regular size types can be used for a market-neutral behavior, see [this](https://discord.com/channels/918629562441695344/1127185180386394145) discussion on Discord.
 * Created the alias `grouped_index` for [Grouper.get_index](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/#vectorbtpro.base.grouping.base.Grouper.get_index)
 * The simulation methods of [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) such as `from_signals` now accept a symbol as the first argument, such as "BTC-USD", which will fetch this symbol using [YFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/yf/#vectorbtpro.data.custom.yf.YFData) (or provide the name of the class as well using `class_name:symbol`) and use as data. Designed for quick backtesting.
 * Fixed a regular expression error appearing on Python 3.11
 * Improved error handling when authenticating with [TVClient](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVClient)


# Version 1.13.0 (04 Jul, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1130-04-jul-2023 "Permanent link")

 * Added Python 3.11 support
 * Rewrote all functions implemented with `numba.generated_jit` (deprecated) to use overloading
 * Fixed backward compatibility for Pandas 1.*
 * Conversion of datetimes and timedeltas to integer timestamps has been standardized across the entire codebase using [to_ns](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.to_ns)
 * Fixed handling of duplicate allocation indices in [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer)
 * Index column can be disabled in [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData)
 * [Data.transform](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.transform) can be run per symbol
 * Replaced the field `peak_idx` by `start_idx` and `peak_val` by `start_val` in [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns) for better compatibility. Also, renamed `drawdown_ranges` to `decline_ranges`.
 * More methods for working with indexes support [ExceptLevel](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.ExceptLevel)
 * [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades) can plot multiple columns at once if `group_by=True` is provided to the method
 * Implemented [ExtPandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ExtPandasIndexer) as an extension class to [PandasIndexer](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.PandasIndexer), which adds an additional indexing property `xloc` utilizing [get_idxs](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.get_idxs)
 * Argument `fps` in [save_animation](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#vectorbtpro.utils.image_.save_animation) is automatically converted to `duration`
 * Arguments `td_stop` and `dt_stop` can be accepted as parameters with multiple strings, such as `vbt.Param(["daily", "weekly", "monthly"])`
 * Range breaks can be determined and applied automatically with `fig.auto_rangebreaks()`
 * Cumulative returns can be plotted in percentage scale by enabling `pct_scale`
 * Drawdowns can be plotted in absolute scale by disabling `pct_scale`
 * Changed the default start value for all Numba-compiled return functions from 0 to 1
 * Fixed `bm_close` not being resolved property in [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func)
 * Switched parameter selection in [@cv_split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.cv_split) from `argmin` and `argmax` to `nanargmin` and `nanargmax` respectively
 * Symbols in [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) can be tuples. Level name(s) can be provided via `level_name`.
 * Fixed dynamic resolution of stop entry price
 * Implemented product of indexes ([cross_indexes](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.cross_indexes)) and product of DataFrames ([BaseAccessor.cross](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.cross), also as [BaseAccessor.x](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.x))
 * Implemented periodic datetime indexing through datetime components ([DTC](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.DTC)) and Numba functions. The new indexer class [DTCIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DTCIdxr) can receive a datetime component or a sequence/slice of such and translate them into positions. Can also parse datetime-like strings such as "12:00", "thursday", or "january 1st" using `dateutil.parser`.
 * Multiple indexers of the same type can be combined using logical operations, such as `vbt.autoidx(...) & vbt.autoidx(...)`. Both operands will be used as masks.
 * Indexers can be used to modify data. This feature is supported by [BaseAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor), which can modify the object in-place, for example with `obj.vbt.iloc[...] = ...`.
 * Added `rescale_to` argument to [PortfolioOptimizer.from_allocate_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocate_func) and [PortfolioOptimizer.from_optimize_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_optimize_func) to rescale all weights generated by the callback to a given min-max range
 * Numba functions implementing crossovers can take the second array as a scalar or of any other flexible format
 * Implemented a method ([Data.realign](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.realign)) to align data to any frequency or custom index. By default, open price is aligned with [GenericAccessor.realign_opening](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_opening) and any other feature is aligned with [GenericAccessor.realign_closing](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign_closing). Useful when symbols are scattered across different times/timezones.
 * Extended the [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized) decorator with _mono-chunks_ \- parameter combinations can be split into chunks and each chunk can be merged to allow passing multiple parameter combinations as a single array and thus making use of column stacking. This approach means trading in more RAM for more performance. The function itself must be adapted to take arrays rather than single values.
 * Added `warmup` argument to [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) to dry-run one function call
 * Fixed behavior of [Portfolio.get_market_value](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.get_market_value) when there's a column that consists entirely of NaN
 * [Data.to_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_csv) and [Data.to_hdf](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.to_hdf) can take `path_or_buf` and `key` as templates
 * Added `run_arg_dict` to specify keyword arguments per function name in [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run) (as an alternative to `run_func_dict` where we specify function arguments per argument name)
 * Wrote the first part of [Cookbook](https://vectorbt.pro/pvt_7a467f6b/cookbook/) ![🥗](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f957.svg)


# Version 1.12.0 (25 Apr, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1120-25-apr-2023 "Permanent link")

 * [Data.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.pull) also accepts as the first argument a dictionary where symbols are keys and keyword arguments are values
 * [CCXTData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/ccxt/#vectorbtpro.data.custom.ccxt.CCXTData) also accepts symbols in the format `EXCHANGE:SYMBOL`
 * Added support for broadcasting along one axis in [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast)
 * Added support for wrapping multiple arrays with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) and broadcasting them in [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast). Arrays of various shapes are stacked along columns and automatically expanded to the biggest shape by padding. Previously, only single-value parameters could be tested.
 * Renamed the key "alpha_vantage" to "av" in [settings.data](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.data)
 * Renamed `capture` to `capture_ratio` in [ReturnsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor)
 * Added `user_agent` argument to [TVClient](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVClient)
 * Fixed [unstack_to_array](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.unstack_to_array) producing incorrect mappings when sorting is disabled
 * Added merging functions "reset_column_stack", "from_start_column_stack", and "from_end_column_stack"
 * Fixed the error in [Trades.plot_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.plot_running_edge_ratio)
 * Implemented stop laddering in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals). By enabling `stop_ladder` (or using an option from [StopLadderMode](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.StopLadderMode)), **each** stop type will behave like a ladder. That is, multiple ladder steps can be provided as an array (either one-dimensional, or two-dimensional with ladder steps defined per column). Moreover, ladders of different sizes can be wrapped with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) to test arbitrary combinations. Defining a ladder per row is not supported (this is possible only dynamically!). Ladders with a single value will behave like previously.
 * Implemented [GenericSRAccessor.to_renko_ohlc](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.to_renko_ohlc) to convert a Series into an OHLC DataFrame in the Renko format
 * Parameters wrapped with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) have got a flag `hide` for the parameter to be hidden from the product index, and an argument `map_template` to generate its values dynamically
 * With automatic initial cash and no expenses, the determined initial cash will become 1 instead of 0 for a correct calculation of returns
 * Implemented market-neutral size types `MNTargetValue`, `MNTargetPercent`, and `MNTargetPercent100`
 * Method [Splitter.take_range](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take_range) takes an argument `point_wise` that when True selects an index at a time and return a tuple of the selected values
 * Implemented classes for preparing functions and arguments. These classes take arguments, pre-process them, broadcast them, post-process them, substitute templates, prepare the target function, and build the target set of arguments. All these steps happen inside cached properties, such that none of them are executed twice. The result of a preparation can be easily changed and passed for execution: all portfolio methods accept as the first argument the preparer or its result. The following classes were implemented:
 * [BasePreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.preparing.BasePreparer): base class for vectorbtpro
 * [BasePFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.portfolio.preparing.BasePFPreparer): base class for [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio)
 * [FOPreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.portfolio.preparing.FOPreparer): for preparing [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders)
 * [FSPreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.portfolio.preparing.FSPreparer): for preparing [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals)
 * [FOFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.portfolio.preparing.FOFPreparer): for preparing [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func)
 * [FDOFPreparer](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.portfolio.preparing.FDOFPreparer): for preparing [Portfolio.from_def_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_def_order_func)
 * When providing keyword arguments, they are mostly merged with default keyword arguments to override them. But how to completely remove a key from the default keyword arguments? For this, pass [unsetkey](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.unsetkey) as the value of the key you want to remove!
 * Complex VBT objects such as [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper) sometimes take other VBT objects such as [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/#vectorbtpro.base.grouping.base.Grouper) as arguments. To change something deep inside the object, we have to manually and recursively rebuild the objects. For example: `wrapper.replace(grouper=wrapper.grouper.replace(group_by=True))` to enable the grouping. To simplify this, the user can now pass `nested_=True` and provide the specification as a nested dict. For example: `wrapper.replace(grouper=dict(group_by=True), nested_=True)`.
 * Fixed `pivots` and `modes` in [PIVOTINFO](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/pivotinfo/#vectorbtpro.indicators.custom.pivotinfo.PIVOTINFO)
 * Added an argument `delisted` to [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data). Symbols with this argument enabled won't get updated.
 * Object in [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take) can be a template. For example, you can do `splitter.take(vbt.RepEval("x.iloc[range_]", context=dict(x=x))`.
 * Switched to the newer paging feature in [TVClient.search_symbols](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVClient.search_symbols) to download the complete set of symbols
 * Completely refactored indexing. Instead of converting complex indexing specifications to integer positions in a single method `get_indices`, each kind of indexing (also called "indexer") is implemented in its own class. For example, [LabelIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.LabelIdxr) is an indexer for labels while [DatetimeIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.DatetimeIdxr) is an indexer for datetime. The indexer [AutoIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.AutoIdxr) determines the kind automatically. Such indexers are generic and can be passed to [RowIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr) to notify vecotrbtpro that we want to select a row, and [ColIdxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr) to select a column. The indexer [Idxr](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.Idxr) takes any of the above, or a row and column indexer. For example, `vbt.Idxr(0)` will select the first row and all columns, while `vbt.Idxr(0, "BTC-USD")` will select the first row of the column with the label "BTC-USD" only.

Note

In your code, replace `RowIdx` to `rowidx`, `ColIdx` to `colidx`, `RowPoints` to `pointidx`, `RowRanges` to `rangeidx`, and `ElemIdx` to `idx`.

 * Implemented a class [IdxSetter](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter), which takes a list of tuples with indices (see above) and values, creates a new array, and modifies it according to the list by setting each value at the corresponding index. Previously, this was implemented by `ArrayWrapper.fill_using_index_dict`. Also, renamed `fill_using_index_dict` to [ArrayWrapper.fill_and_set](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.fill_and_set).
 * Implemented a class [IdxSetterFactory](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetterFactory), which can generate one to multiple [IdxSetter](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.IdxSetter) instances from an index dictionary, Series, DataFrame, or a sequence of records. This makes possible passing the argument `records` to any [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) method to unfold one to multiple arguments from it.
 * [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) accepts new arguments `long_entries` and `long_exits`, which can replace (or enhance) `entries` and `exits` respectively
 * When any broadcastable argument in [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) is provided as an index dictionary, the default value is now taken from the global settings rather than hard-coded (apart from the argument `size` in [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders), which is always NaN when a new array is created or an existing array is reindexed)
 * Added the argument `layout` to the methods of the plotly express accessor to change the layout of any figure
 * Removed the argument `date_parser` from [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) since it's incompatible with Pandas 2.0
 * Added support for Pandas 2.0 ![🛸](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f6f8.svg)
 * Updated the dark theme of the website and graphs ![🌒](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f312.svg)


# Version 1.11.1 (18 Mar, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1111-18-mar-2023 "Permanent link")

 * Fixed the staticization paths on Windows
 * Renamed class methods of [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory) from `get_indicators` to `list_indicators`
 * Renamed class methods of [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) from `get_symbols` to `list_symbols`
 * Implemented various methods for a better indicator search: 
 * [IndicatorFactory.list_vbt_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_vbt_indicators) to list all vectorbt indicator names
 * [IndicatorFactory.list_indicators](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.list_indicators) to list all supported indicator names
 * [IndicatorFactory.get_indicator](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.get_indicator) and its shortcut `vbt.indicator` to find and return any indicator by its name
 * Enhanced indicators by the following:
 * [IndicatorBase.param_defaults](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase.param_defaults) to get the parameter defaults of an indicator
 * [IndicatorBase.unpack](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase.unpack) to return the outputs of an indicator as a tuple
 * [IndicatorBase.to_dict](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase.to_dict) to return the outputs of an indicator as a dict
 * [IndicatorBase.to_frame](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase.to_frame) to return the outputs of an indicator as a DataFrame
 * Refactored [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run) to use the new indicator search
 * Providing `tz` to [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) will localize/convert each date to this timezone. Especially useful when data contains dates with various timezones (due to daylight savings, for example).
 * All record classes subclassing [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords) have received new fields describing the bar of the record. For example, you can now get the low price of the bar of each order using `pf.orders.bar_low`.
 * Implemented [MappedArray.to_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_readable), which is an equivalent to [Records.records_readable](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.records_readable)
 * Implemented [Orders.price_status](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.orders.Orders.price_status) that returns whether the price of each order exceeds the bar's OHLC
 * Fixed `call_seq` being materialized even with `attach_cal_seq=False` in [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func)
 * Added a progress bar to [PathosEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine). Disabled by default, to enable pass `engine_config=dict(show_progress=True)`.
 * Implemented [Ranges.crop](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.crop) to remove irrelevant OHLC data from records, which is especially useful for plotting high-granular data


# Version 1.11.0 (15 Mar, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1110-15-mar-2023 "Permanent link")

 * Made `run_pipeline` a class method of [IndicatorBase](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase) so it can be overridden by the user
 * Implemented an accessor method [GenericAccessor.groupby_transform](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.groupby_transform) to group and then transform a Series or DataFrame
 * Implemented new trade properties and methods:
 * [Trades.best_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.best_price_idx)
 * [Trades.worst_price_idx](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.worst_price_idx)
 * [Trades.expanding_best_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_best_price)
 * [Trades.expanding_worst_price](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_worst_price)
 * [Trades.expanding_mfe](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mfe) with `plot_` and `_returns` versions
 * [Trades.expanding_mae](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.expanding_mae) with `plot_` and `_returns` versions
 * Data classes that work with the file system and can discover file paths subclass a special data class [FileData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData)
 * Moved [RemoteData.from_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/remote/#vectorbtpro.data.custom.remote.RemoteData.from_csv) and [RemoteData.from_hdf](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/remote/#vectorbtpro.data.custom.remote.RemoteData.from_hdf) to [Data.from_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.from_csv) and [Data.from_hdf](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.from_hdf) respectively
 * [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) supports new time-based stop orders that can be provided via two arguments: `td_stop` for timedelta-like inputs and `dt_stop` for datetime-like inputs. Both are very similar to `limit_tif` and `limit_expiry` respectively, with a distinction that a time-based stop is executed at a tick before the actual deadline.
 * Greatly improved the resolution of `dt_stop` and `limit_expiry`, which now can distinguish between timedelta and datetime strings. They can also take ISO time strings such as "16:00".
 * Renamed simulator functions:
 * `simulate_from_orders_nb` → `from_orders_nb`
 * `simulate_from_signals_nb` → `from_signals_nb`
 * `simulate_from_signal_func_nb` → `from_signal_func_nb`
 * `simulate_nb` → `from_order_func_nb`
 * `simulate_row_wise_nb` → `from_order_func_rw_nb`
 * `flex_simulate_nb` → `from_flex_order_func_nb`
 * `flex_simulate_row_wise_nb` → `from_flex_order_func_rw_nb`
 * Arguments `order_func_nb` and `order_args` have become optional in [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func). Also, the argument `flexible` has been removed in favor of `flex_order_func_nb` and `flex_order_args`.
 * Integrated order mode (`order_mode=True`) directly into [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals). to make possible using target sizes instead of signals. Under the hood, it will use a dynamic signal function that translates orders into signals.
 * Class methods in [SignalsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor) that take `shape` as the first argument can also take an array wrapper via this argument
 * Scheduler supports zero_offset for seconds
 * Previously, trailing target price was updated in accordance to a percentage stop. Now, it's updated in accordance to an absolute stop.
 * [SignalContext](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.SignalContext) has a field `fill_pos_info` of the type [trade_dt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.trade_dt) that holds information on the current position such as the average entry/exit price and open statistics
 * Fixed stop exit price provided as a floating array
 * Each stop can define its own exit size and size type via `exit_size` and `exit_size_type` respectively. Can be used only dynamically.
 * Each stop can define its own ladder. By setting `ladder=True` in the information record, the stop won't be cleared after execution. Upon execution, the current ladder step index and row are automatically updated in `step` and `step_idx` respectively, such that they can be used to update the current step with new information. Can be used only dynamically.
 * Fixed the time resolution of stop orders among themselves. For example, previously, if an SL stop was marked for execution at the closing price and a TP stop was marked for execution at the opening price, the SL stop was executed (pessimistically). Now, the TP stop will be executed since it precedes the SL stop in time.
 * Implemented [TVClient.scan_symbols](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVClient.scan_symbols) and the corresponding argument `market` in [TVData.list_symbols](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVData.list_symbols) to scan a market and return the full list of symbols being traded in that market
 * **Important!** To avoid confusion, passing an index (`pd.Index`) to the broadcaster won't behave like a parameter ([Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param)) any longer. An index will be converted into a Series with the same index and values.

Example

If you previously used `pd.Index([0.1, 0.2])` to test multiple values, now use `vbt.Param([0.1, 0.2])`.

 * Implemented a module ([utils.cutting](https://vectorbt.pro/pvt_7a467f6b/api/utils/cutting/)) that is specialized in "cutting" annotated sections from any code. Not only it can cut out a block of code, but also transform it based on special commands annotated using comments in that code. This way, there's no more need to duplicate a lengthy code since one can just copy, transform, and paste it to any Python file, in a fully automated fashion.
 * Thanks to the cutting feature, [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) and [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func) can now be instructed to transform their non-cacheable code to a cacheable one! This process is called "staticization" and can be enabled simply by passing `staticized=True`. For this to work, all Numba simulation functions that take callbacks as arguments were annotated beforehand - by me ![✌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/270c.svg) After extraction and transformation, the new cacheable code is saved to a Python file in the same directory (by default). Built-in callbacks will be automatically included in the file as well. User-defined callbacks are automatically imported at the beginning of the file, given that they were defined in a Python file and not in a Jupyter notebook.


# Version 1.10.3 (26 Feb, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1103-26-feb-2023 "Permanent link")

 * Added `adjustment` argument to [TVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVData)
 * Disabled searching for the earliest date in [CCXTData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/ccxt/#vectorbtpro.data.custom.ccxt.CCXTData), you can still enable it by passing `find_earliest_date=True`. Also, `start` and `end` are both None now since some exchanges don't like 0 as a start timestamp to be passed.
 * Added various helper functions for working with the file system in [utils.path_](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/)
 * Added `log_returns`, `daily_returns`, `daily_log_returns` in both [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) and [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio)
 * Scattergl is disabled by default since it causes problems when one trace has it enabled and another not. You can still enable `use_gl` globally under `vbt.settings.plotting`.
 * Fixed a circular import error when attempting to load a configuration file with pickled data on startup
 * Fixed size granularity not being properly applied due to round-off errors
 * Fixed positions not being properly reversed when size granularity is enabled
 * [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) can now take `sim_out` as the second argument and extract order records and other arrays from it
 * Added `random_subset` argument to [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) to select a random subset from a single parameter
 * Added [Optuna](https://optuna.org/) as an optional dependency
 * Fixed split and set selection in [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take) and [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply)
 * Fixed the calculation of the grouped gross exposure for both directions
 * Fixed an issue with the infinite leverage and order fees greater than the available free cash
 * Implemented NB and SP rolling z-score ([GenericAccessor.rolling_zscore](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_zscore))
 * Wrote [Pairs trading](https://vectorbt.pro/pvt_7a467f6b/tutorials/pairs-trading) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.10.2 (15 Feb, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1102-15-feb-2023 "Permanent link")

 * Fixed cases where size type is not being checked properly when resolving signals


# Version 1.10.1 (15 Feb, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1101-15-feb-2023 "Permanent link")

 * Fixed cases where leverage is not being applied when reversing positions
 * Timezones are now parsed with Pandas rather than `zoneinfo` to avoid issues with Python 3.8


# Version 1.10.0 (14 Feb, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-1100-14-feb-2023 "Permanent link")

 * Added an argument `use_class_ids` to represent classes by their ids rather than convert them into a stream of bytes when saving to or loading from a config file
 * Fixed the error "expected return exceeding the risk-free rate" in the newest PyPortfolioOpt
 * Fixed timezone in [TVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVData)
 * Renamed `AlphaVantageData` to `AVData`
 * Made grid lines darker in the dark theme 
 * Outputs of [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run) can now directly return indicator outputs instead of indicator instances
 * Price types "nextopen" and "nextclose" can now be provided per column
 * Bar skipping in [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) happens automatically
 * Fixed the color schema in the Seaborn theme
 * Added a signal function that can translate target size types into signals. Also, added an option `pf_method` in [Portfolio.from_optimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_optimizer) to rebalance using [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals).
 * Added warnings whenever `init_position` without `init_price` is provided
 * Made accessors wrap their own objects much faster
 * Added a new execution engine [PathosEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.PathosEngine) that uses [pathos pools](https://pathos.readthedocs.io/en/latest/pathos.html#module-pathos.pools) with better pickling.
 * Renamed `SequenceEngine` and its identifier "sequence" to `SerialEngine` and "serial" respectively
 * Fixed resolution of asset classes in [riskfolio_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.riskfolio_optimize) after dropping NaN columns
 * Entirely refactored importing mechanics. For instance, auto-import can disabled in the settings to load vectorbt in under one second. Also, whether to make an object available via `vbt.[object]` is now decided by the module itself where the object is defined using `__all__`. This also greatly improves type hints in IDEs.
 * There are two new shortcuts: 
 * `vbt.PF` for `Portfolio`
 * `vbt.PFO` for `PortfolioOptimizer`
 * Fixed best and worst price in [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades) to also include the entry and exit price. This also improves the (running) edge ratio, MAE, and MFE metrics.
 * Renamed the argument `stop_price` to `init_price` in `check_stop_hit_nb`
 * Merged the `OLS` and `OLSS` indicators into just `OLS`
 * Datetime-like strings will now be parsed largely using Pandas than the `dateparser` package
 * Made weekdays start from 0 in Numba methods by default (same as in Pandas)
 * Added three new methods for more convenience (all support integer and timedelta lookback periods):
 * [GenericAccessor.ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.ago) \- get value `n` periods ago
 * [GenericAccessor.any_ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.any_ago) \- whether a condition was True at any time in the last `n` periods
 * [GenericAccessor.all_ago](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.all_ago) \- whether a condition was True at all times in the last `n` periods
 * Simplified signal generation. There is no more need to manually set the signal in `out`, returning its (relative) index is enough. Also, entry signal generators have got new options `only_once` and `wait` for full compatibility with exit signal generators.
 * Completely refactored [RandomOHLCData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/random/#vectorbtpro.data.custom.random.RandomData) and [GBMOHLCData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/gbm_ohlc/#vectorbtpro.data.custom.gbm_ohlc.GBMOHLCData). There's no more need to explicitly specify the frequency for resampling, it will now default to 50 ticks per bar. Also, the number of ticks per bar can be specified as an array for best flexibility.
 * Limit and stop values in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) can now be provided as a target price when `delta_format="target"`
 * Greatly improved approximation of order values for automatic call sequences
 * [BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO) and [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) have been split to become totally independent of each other
 * Dropped Python 3.7 support
 * Default timezone can be now set using `tz` when fetching data, this will do two things: 1) every `start` and `end` date provided as a string without timezone will be assumed to be in this default timezone, and 2) output data will be converted to this timezone.
 * Timeframe will be converted into frequency and persisted in the wrapper when fetching data. This way, if the fetched data has gaps, vectorbt objects such as portfolio will still know the true frequency.
 * There's no more need to build a resampler to resample to a target index: passing the target index directly will work too
 * Renamed `fill_state` to `save_state`, `fill_returns` to `save_returns`, and added an argument `save_value` to save the portfolio value in [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) and [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals)
 * Refactored parameter generation. Function [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params) can now be used to generate parameters without building the index. Also, filtering of conditional parameters and selecting a random subset have become much faster (especially when used together).
 * Renamed `entry_place_func` to `entry_place_func_nb` and `exit_place_func` to `exit_place_func_nb`
 * Function [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) can now put multiple calls into the same chunk using `distribute="chunks"`, execute them serially, and distribute the chunks themselves. This makes certain engines such as those for multiprocessing much more effective. Also, `tasks` can be provided as a template that gets substituted once chunking metadata is available (requires `size`).
 * Reduced memory footprint when indicators are executing many parameter combinations
 * Refactored the jitted loop in the indicator factory. Multiple parameter combinations can be put into a single jitted loop, while multiple jitted loops can be distributed using [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute). The argument `jitted_loop` can now be toggled when running an indicator. There's a new argument `jitted_warmup` to run one parameter combination to compile everything before running everything else.
 * Datetime is now mainly parsed using `pd.Timestamp` instead of `pd.to_datetime`
 * Improved parsing of datetime-like and timezone-like objects
 * Implemented a function [pdir](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.pdir) that beautifully prints the attributes of any Python object (including packages and modules!). Use this function in conjunction with `phelp` and `pprint` to discover objects.
 * Added an option `dropna` when calculating crossovers to ignore NaNs (default is to keep them)
 * Enhanced [BaseAccessor.eval](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.eval) with multiline expressions
 * Added support for a variety of pickle compression algorithms. Each algorithm has its own set of file extensions that can be automatically recognized to decompress the saved data. For example, pickling with the compression `blosc` will add the extension `.pickle.blosc`.
 * Added the ability to select a date range with `start` and `end` in local data classes. This can be done before loading data in [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData) (efficient) and only after loading data in [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) (not so).
 * The default PyTables format is now "table"
 * [YFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/yf/#vectorbtpro.data.custom.yf.YFData) now automatically recognizes the timezone of each ticker and uses it. If tickers have different timezones, either fetch them separately, or provide a unified timezone with `tz_convert`.
 * Not only vectorbt will check whether some optional packages are installed, but it will also verify whether their versions match the required ones for full compatibility
 * Renamed `deep_substitute` to `substitute_templates`
 * Iterating over symbols when fetching or updating data is now done with [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) such that it can be distributed. For example, using `execute_kwargs=dict(cooldown=1)` will sleep for one second after fetching each symbol since it's now executed with [SerialEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine).
 * Updated [Features](https://vectorbt.pro/pvt_7a467f6b/features) with dozens of new examples ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.9.0 (15 Jan, 2023)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#version-190-15-jan-2023 "Permanent link")

 * Implemented leverage. Two leverage modes are supported:
 * `Lazy` ![🐌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f40c.svg): Uses the available cash whenever possible, and only if it's not enough to fulfill the whole operation, uses leverage. This allows for effectively increasing the available cash with debt.
 * `Eager` ![🐇](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f407.svg): Uses leverage even if the whole operation can be fulfilled using the available cash. This is similar to opening a micro-account with a subset of the available cash and using the lazy leverage on it.
 * Leverage can also be infinite (`leverage=np.inf`) to fulfill any position size requirement as long as there's at least some free cash. The user is the one responsible for choosing a proper position size.
 * Refactored the lowest-level simulation logic:
 * Added [AccountState.locked_cash](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.AccountState.locked_cash) that together with [AccountState.debt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.AccountState.debt) keep track of the current leverage and shorting state. Used both in the long and short direction. Don't forget to initialize it with zeros and add to [AccountState](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.AccountState) and [ExecState](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.ExecState).
 * Buy and sell functionality is now distributed over four distinct functions (neither of them supports position reversal):
 * [long_buy_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/core/#vectorbtpro.portfolio.nb.core.long_buy_nb)
 * [long_sell_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/core/#vectorbtpro.portfolio.nb.core.long_sell_nb)
 * [short_sell_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/core/#vectorbtpro.portfolio.nb.core.short_sell_nb)
 * [short_buy_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/core/#vectorbtpro.portfolio.nb.core.short_buy_nb)
 * The functions [buy_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/core/#vectorbtpro.portfolio.nb.core.buy_nb) and [sell_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/core/#vectorbtpro.portfolio.nb.core.sell_nb) orchestrate them to enable position reversal
 * Regular cash ([AccountState.cash](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.AccountState.cash)) won't be used in buy and sell operations anymore, only in equity calculations. This is because it can go below zero when leverage is used. Transactions now use solely free cash ([AccountState.free_cash](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.AccountState.free_cash)). This also means that free cash (and not regular one) must be greater than zero to allow most operations.
 * Free cash isn't guaranteed to be zero or above. Some operations such that those partially closing leverage positions or short positions can make it become negative, thus offsetting costs to other columns.
 * The order in which account/execution state and order result are returned has been reversed (that is, `order_result, new_account_state` instead of `new_account_state, order_result`)
 * Renamed and reordered log fields
 * When reversing positions, [SizeType.Percent](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.SizeType.Percent) now refers to the available resources after the current position is closed (that is, in a long position that can be reversed, 50% means _close the current position and open a short one by using 50% of the available free cash left after closing it_)
 * The limitation of [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) being unable to reverse positions when [SizeType](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.SizeType) is `Percent` or `Percent100` has been lifted
 * Some simulation functions accept an argument `fill_state` that can fill position, cash, debt, and other fields from [AccountState](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.AccountState) as arrays to avoid reconstructing them later

Note

Reconstruction of free cash would only yield the same result as during the simulation if leverage is disabled. For enabled leverage, use `fill_state` to pre-compute the array.

 * Returns for negative positions won't be flipped anymore to make them consistent with `pct_change`. This will also make equity and cumulative returns produce the same plot when equity dips below zero.
 * Refactored flexible indexing due to an unresolved Numba bug:
 * There's no more `flex_select_auto_nb`, but an entire module [base.flex_indexing](https://vectorbt.pro/pvt_7a467f6b/api/base/flex_indexing/) with Numba functions tailored to different array formats
 * Removed `flex_2d` argument completely
 * It's not more required to wrap scalars with zero-dimensional NumPy arrays - most Numba functions will convert any input into a one-dimensional or two-dimensional NumPy array. Here are the general rules depending on the annotation of an argument:
 * `FlexArray1dLike`: can be passed as scalar or array that can broadcast to one dimension
 * `FlexArray2dLike`: can be passed as scalar or array that can broadcast to two dimensions
 * `FlexArray1d`: must be passed as a flexible one-dimensional array
 * `FlexArray2d`: must be passed as a flexible two-dimensional array
 * **Important!** From now on, one-dimensional arrays will always broadcast against rows since we're primarily working on time-series data. This makes vectorbt's broadcasting mechanism different from the NumPy's mechanism! Created a range of helper functions for broadcasting both arrays and shapes in the module [base.reshaping](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/). Also ensured that all vectorbt functions use in-house broadcasting functions, and not NumPy ones.

Example

Previously, if a list `["longonly", "shortonly", "both"]` was applied per column and could be used to test multiple position directions, now the same list will be applied per row, thus use `[["longonly", "shortonly", "both"]]`

 * Made data typing errors more descriptive in portfolio
 * [Splitter.from_rolling](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_rolling) has now an option to roll backwards
 * Fixed [Resampler.map_bounds_to_source_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.map_bounds_to_source_ranges) returning garbage values when `skip_not_found=True`
 * Renamed the argument `to_py_timezone` to `to_fixed_offset`
 * Series names are automatically stringified in [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter)
 * The author of [tvdatafeed](https://github.com/StreamAlpha/tvdatafeed) has pulled the package from PyPi such that it cannot be installed with `pip` anymore, thus the package has been integrated directly into vectorbt (see [data.custom.tv](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/)) and additionally refactored
 * The TradingView client [TVClient](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVClient) now uses the pro data feed by default, making it possible to pull 20,000 data points at once, even without signing in. If you want to sign in, you can use username and password, or manually parse the token from the TradingView's website and use it (for example, if proper authentication requires you to complete a captcha).
 * Implemented functions [pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.pprint) and [phelp](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.phelp) that do `print` and `help` but beautifully
 * Earliest date detection in [CCXTData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/ccxt/#vectorbtpro.data.custom.ccxt.CCXTData) was (at least somewhat) fixed for exchanges that return the latest data point and not the earliest one when `limit=1` is used
 * Calculating and plotting allocations doesn't require grouping
 * Input arrays in indicators built with [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory) aren't cacheable by default to enable pickling of indicator class definitions
 * The argument `order_records` now comes before the argument `close` in the constructor method of the [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio). Make sure to use keyword arguments to avoid problems!
 * [MappedArray.to_pd](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_pd) can take a reducing function or its name to automatically aggregate data points that fall into the same row. This is especially convenient for resampling P&L where `reduce_func_nb="sum"` can be provided.
 * Package [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for building Telegram bots has released the version 2.0.0, which introduces a lot of breaking changes. Even though the vectorbt's adaptation to this version was successful, the bot cannot run in background due to `asyncio` (if you know the fix, ping me!). If you need this functionality, install the latest `python-telegram-bot` version before 2.0.0 and vectorbt will switch to the previous functionality automatically. The tutorial still requires the previous version until the limitation is fixed.
 * Fixed errors when no symbol could be fetched in custom data classes
 * Refactored configs and pickling (persisting on disk):
 * Config options cannot longer be passed directly to config, they need to be packed as `options_`
 * Most vectorbt objects can now be pickled and unpickled using `pickle` or `dill`, without the need to prepare them. The mechanism is rather simple: each object defines its own reconstruction state of the type [RecState](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.RecState), which is a tuple of positional arguments, keyword arguments, and attributes required to create an identical instance. Only this state is pickled, unpickled, and together with the class used to reconstruct the object using [reconstruct](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.reconstruct). This allows for highest flexibility because vectorbt objects can now be saved in lists, dicts, and even as values of DataFrames!
 * No more need to pickle class definitions: only the path to the class is pickled, thus making dumps more light-weight but also more robust to API changes
 * There's a new functionality that allows the user to change how a pickled object is reconstructed in a case where its class or arguments have changed

Warning

If you have any vectorbt objects pickled by the previous versions of vectorbt, they won't be unpickled by the newer version. It's advised to either recalculate them using the newer version, or first unpickle them using the previous version, save their components separately, and then import and connect them using the newer version. Ping me if you meet any issues.

 * Not only vectorbt objects can be seamlessly converted into a stream of bytes (i.e., pickled), but they now also be converted into regular configuration files with extensions `.config`, `.cfg`, and `.ini`! For this, vectorbt extends the `configparser` functionality with its own parsing rules (see [Pickleable.encode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.encode_config) and [Pickleable.decode_config](https://vectorbt.pro/pvt_7a467f6b/api/utils/pickling/#vectorbtpro.utils.pickling.Pickleable.decode_config)). Since most vectorbt objects can be represented using dictionaries, configuration files are an ideal text format where sections represent (sub-) dictionaries and key-value pairs represent dictionary items. In addition, the following features were implemented:
 * Parsing of literals (strings `"True"` and `"100.0"` are recognized as a bool and float respectively)
 * Nested dictionaries (section `[a.b]` becomes a sub-dict of the section `[a]`)
 * References (a key can reference another value in another section or even the section itself, such that a reference `&a.b` will be substituted for the value of the key `b` in the dict `a`)
 * Single and multi-line expressions (`yf_data = !vbt.YFData.pull("BTC-USD")` will download the data and put it under the key `yf_data`)
 * Round trip (a successful round-trip consists of converting an object to text and then back again to an object without losing information)
 * Upon importing, vectorbt can automatically detect a file with the name "vbt" and any supported extension in the current working directory, and update the settings. This makes setting the default theme like a breeze:

vbt.ini
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#__codelineno-0-1)[plotting]
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2023/#__codelineno-0-2)default_theme = dark
 
[/code]