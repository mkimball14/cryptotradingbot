# Release notes for 2022[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#release-notes-for-2022 "Permanent link")

All notable changes in reverse chronological order.


# Version 1.8.2 (3 Dec, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-182-3-dec-2022 "Permanent link")

 * Implemented methods for plotting trades as signals - [EntryTrades.plot_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.EntryTrades.plot_signals), [ExitTrades.plot_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.ExitTrades.plot_signals), and [Portfolio.plot_trade_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.plot_trade_signals)
 * Implemented a method for plotting ranges as shapes - [Ranges.plot_shapes](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_shapes)
 * Fixed creation of three-dimensional `splits_arr` in [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter), now the array will always be two-dimensional and have the data type `object`
 * Added support for timestamps and timedeltas in [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter)
 * Fixed [Trades.get_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_edge_ratio) and [Trades.get_running_edge_ratio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades.get_running_edge_ratio) when `high` and/or `low` are not provided; in this case, rolling volatility instead of ATR will be used.
 * Method [Splitter.plot_coverage](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.plot_coverage) will return a stacked area plot by default
 * Implemented a method [Splitter.get_overlap_matrix](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.get_overlap_matrix) for calculation of an overlapping coverage matrix
 * Implemented a method [GenericAccessor.proximity_apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.proximity_apply) for rolling and reducing a two-dimensional window of neighboring elements
 * Refactored [ArrayWrapper.indexing_func_meta](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.indexing_func_meta) to make indexing operations on vectorbt objects more flexible and efficient
 * Enabled row stacking in [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take)
 * Implemented methods [Splitter.shuffle_splits](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.shuffle_splits) and [Splitter.break_up_splits](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.break_up_splits) for shuffling and breaking up splits respectively
 * Fixed bound attachment in [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take) and [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply)
 * The method [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run) can now run multiple indicators by passing a sequence, and even all indicators by adding the suffix `_all` to a library name, and stack outputs along columns into a single DataFrame
 * The simulation method [Portfolio.from_holding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_holding) is now cached by default (use `dynamic_mode=True` to use a signal function)
 * Made the method [ReturnsAccessor.deflated_sharpe_ratio](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor.deflated_sharpe_ratio) more robust to invalid Sharpe values (`np.nan` and `np.inf`)
 * Implemented a method for calculating the Probabilistic Sharpe Ratio - [ReturnsAccessor.prob_sharpe_ratio](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor.prob_sharpe_ratio)
 * Wrote [Cross validation](https://vectorbt.pro/pvt_7a467f6b/tutorials/cross-validation) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.8.1 (15 Nov, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-181-15-nov-2022 "Permanent link")

 * Fixed an error in pattern fitting when `max_error_interp_mode` is not set
 * Data dictionary can be constructed from data keyed by feature instead of symbol, which can enabled using the argument `columns_are_symbols`
 * Replaced an argument name `stretch` in favor of `extend` in projection context
 * Implemented a decorator for splitting - [@split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.split)
 * Implemented a decorator for cross-validated splitting - [@cv_split](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/decorators/#vectorbtpro.generic.splitting.decorators.cv_split)
 * Fixed formatting of auto-generated record attributes
 * Parameters of the type [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) can conditionally depend on other parameters. For example, `param1 > param2` will select only the parameter combinations where the value of the first parameter is greater than that of the second parameter.
 * Iterative portfolio Numba-compiled functions can override `i`, `col`, and `flex_2d` provided via the context
 * Fixed exit signal generation with `skip_until_exit`
 * Implemented [Edge Ratio](https://tradingtact.com/edge-ratio/) in [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades)
 * Introduced a one-to-one mapping between orders and trades: each trade record includes the ID of the order that opened and closed the trade (not the other way around)
 * Implemented a method [Portfolio.get_trade_history](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.get_trade_history), which merges orders and trades and returns the information as a human-readable DataFrame
 * [TVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVData) has got an update method
 * Implemented squeezing of splits and sets in [Splitter.take](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.take) and [Splitter.apply](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.apply)
 * Implemented a splitter class method ([Splitter.from_grouper](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter.from_grouper)) that can build a splitter based on grouping/resampling with vectorbt or Pandas (for example, "M" for monthly periodicity)
 * Each [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper) and [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping) instance has a convenient method `split`
 * Updated the notebooks that used outdated splitting API


# Version 1.8.0 (24 Oct, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-180-24-oct-2022 "Permanent link")

 * Created an accessor for Pandas Indexes, [BaseIDXAccessor](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor). Migrated some index-related functionality from [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper) such as [BaseIDXAccessor.get_grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseIDXAccessor.get_grouper). Also, created methods for many functions from the [base.indexes](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/) module.
 * Added `clear_cache` and `collect_garbage` arguments to [SerialEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.SerialEngine), such that it can clear the cache and collect the garbage (globally) after each iteration
 * Implemented a method for preparing returns ([prepare_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.prepare_returns)). The function [riskfolio_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.riskfolio_optimize) now prepares the returns automatically (for example, it can remove columns that are all NaN or zero).
 * Implemented a base module for merging arrays - [base.merging](https://vectorbt.pro/pvt_7a467f6b/api/base/merging/). Also, unified merging functionality across the [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized) and [@chunked](https://vectorbt.pro/pvt_7a467f6b/api/utils/chunking/#vectorbtpro.utils.chunking.chunked) decorators.
 * Added two new execution engines: [ThreadPoolEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ThreadPoolEngine) and [ProcessPoolEngine](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.ProcessPoolEngine), which are lightweight alternatives to Dask and Ray respectively
 * Fixed an issue where using the Plotly Express accessor raised an error
 * Implemented a method for fitting a pattern [GenericSRAccessor.fit_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.fit_pattern)
 * Updated [TVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVData) to `tvdatafeed>=2.1.0`
 * Made vectorbt load much faster by outsourcing import statements to the functions that actually need them. Auto-import of many optional functionalities can now be controlled from [settings.importing](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.importing), disabling all options brings the loading time to around one second and half.
 * Fixed an issue where selecting a date range from a signal portfolio raised an error
 * Fixed [PolygonData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/polygon/#vectorbtpro.data.custom.polygon.PolygonData)
 * Implemented a new signal detection indicator, [SIGDET](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/sigdet/#vectorbtpro.indicators.custom.sigdet.SIGDET) (see <https://stackoverflow.com/a/22640362>)
 * Fixed many potential division by zero conditions in records
 * Fixed the calculation of gross exposure for short positions
 * Redesigned accessors to take an array wrapper as the first argument and accept arbitrary array-like objects
 * Implemented [Splitter](https://vectorbt.pro/pvt_7a467f6b/api/generic/splitting/base/#vectorbtpro.generic.splitting.base.Splitter) ![💥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4a5.svg)


# Version 1.7.1 (23 Sep, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-171-23-sep-2022 "Permanent link")

 * Data stored before `1.7.0` can be unpicked again after this release. Made pickled vectorbt objects more resistant to API changes.
 * Fixed wrong `min_size` and `max_size` defaults
 * Fixed division by zero in the VIDYA indicator
 * Merged `ZIGZAG` indicator into [PIVOTINFO](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/pivotinfo/#vectorbtpro.indicators.custom.pivotinfo.PIVOTINFO)
 * Plotting accessor methods now also accept DataFrames with the ability to select a column to plot
 * Added the streaming [SUPERTREND](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/supertrend/#vectorbtpro.indicators.custom.supertrend.SUPERTREND) indicator from the tutorial
 * Added the streaming [ReturnsAccessor.rolling_sharpe_ratio](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor.rolling_sharpe_ratio) method from the tutorial
 * Removed `apply` and `custom` prefixes from the Numba-compiled indicator functions. Also added chunking specifications.


# Version 1.7.0 (20 Sep, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-170-20-sep-2022 "Permanent link")

 * Implemented a portfolio method (and its corresponding property) for calculating real allocations - [Portfolio.get_allocations](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.get_allocations)
 * Implemented a portfolio method (and its corresponding property) for calculating asset PnL, which is similar to asset returns but in notional terms - [Portfolio.get_asset_pnl](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.get_asset_pnl)
 * Fixed asset returns being improperly calculated when position is being reversed 
 * Improved plotting of allocations in [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) such that there are no more diagonal lines, looks like bars but takes considerably less time to draw
 * Implemented (NB and SP) [VIDYA](https://www.metatrader5.com/en/terminal/help/indicators/trend_indicators/vida) and made it available as a window type in custom indicators
 * [CCXTData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/ccxt/#vectorbtpro.data.custom.ccxt.CCXTData) has got a class method to find the earliest date of any symbol on any exchange. Gets called automatically.
 * Lifted the limitation of merging only different symbols. If two data instances have the same symbols, their dataframes will be merged across rows and columns.
 * Extended `ConflictMode.Opposite` to issue an entry signal when not in position
 * Added some convenience methods to custom data classes. For example, instead of calling `DataClass.set_settings(path_id="custom", ...)` to change the settings of any class globally, we can simply call `DataClass.set_custom_settings(...)`. Also, there are new methods [RemoteData.from_csv](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/remote/#vectorbtpro.data.custom.remote.RemoteData.from_csv) and [RemoteData.from_hdf](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/remote/#vectorbtpro.data.custom.remote.RemoteData.from_hdf) that pull data from a CSV and HDF file respectively, and set up the class. This is a better alternative to using local data classes when data updates are wanted.
 * Enabled random search in indicators by introducing an argument `random_subset`, which selects a subset of parameter combinations randomly
 * Integrated the freqtrade's [technical](https://github.com/freqtrade/technical) library as both technical indicators (`vbt.technical(...)`) and consensus indicators (`vbt.techcon(...)`)
 * Kaleido is now one of the optional dependencies
 * Implemented a [ZIGZAG](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/zigzag/#vectorbtpro.indicators.custom.zigzag.ZIGZAG) indicator, inspired by the following implementation: <https://github.com/jbn/ZigZag> (best used for plotting, note that the first pivot is computed by looking into the future!)
 * Implemented a [PIVOTINFO](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/pivotinfo/#vectorbtpro.indicators.custom.pivotinfo.PIVOTINFO) indicator, which has a similar implementation but is look-ahead bias resistant and contains lots of useful information such as the last confirmed pivot type, index, and value, but also the most recent (not confirmed yet) pivot type, index, and value.
 * Added global options (available under [settings.wrapping](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.wrapping) with the prefix `prec_`) to set a minimum and maximum integer and floating precision of wrapped arrays. Depending on the platform, Numba mostly returns 64-bit numbers. When those arrays are wrapped with Pandas using [ArrayWrapper.wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.wrap), vectorbt can cast them to 32 bits or lower to save memory. Note that Numba does not support 16-bit numbers (yet), but we can still use them with Pandas.
 * Implemented an accessor method [GenericSRAccessor.to_renko](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.to_renko) that converts any time series into [the Renko format](https://www.investopedia.com/terms/r/renkochart.asp). Note that Renko data may contain irregular, duplicate datetime index, and shouldn't be used for anything that requires a frequency (such as Sharpe).
 * Order arguments `min_size` and `max_size` now depend on `size_type`. For example, specifying `min_size` of 10% when `size_type` is `SizeType.TargetPercent` won't execute the order if the requested order size is less than 10% of the current portfolio value.
 * Profit factor, expectancy, and SQN can be also computed from returns rather than PnL (see the respective [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades) property but with the prefix `rel_`)
 * Implemented a decorator [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized), which can wrap any Python function and parameterize its inputs either with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) or with special parameter configs. This way, even though the original function can process only one combination of parameters at a time, the wrapped function looks the same from the outside but can handle unlimited number of combinations!
 * Class methods [PortfolioOptimizer.from_allocate_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocate_func) and [PortfolioOptimizer.from_optimize_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_optimize_func) were completely refactored and are now based on parameters (similar workings to the [@parameterized](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.parameterized) decorator)
 * Argument `product_idx` in [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) and [BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO) was renamed to `level`
 * Added support for symbol classes in [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data). They can be specified when fetching using `classes`. Upon preparing the data, one or more column levels will be created. Useful for attaching information on industries, sectors, and other asset classes.
 * Integrated [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib) in a similar fashion as PyPortfolioOpt: there is now a function [riskfolio_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.riskfolio_optimize) and an infrastructure around it to run arbitrary optimization models from Riskfolio-Lib with a single function call. Rebalancing is done by [PortfolioOptimizer.from_riskfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_riskfolio).
 * Fixed the incompatibility issue between NumPy and TA-Lib in the Dockerfile. Also, included the installation of universal-portfolios.
 * Lifted the limit of 10k fetched data points in [AlpacaData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/alpaca/#vectorbtpro.data.custom.alpaca.AlpacaData)
 * Implemented a method `list_symbols` for a range of local and remote data classes to get the list of all available symbols (and automatically filter it using regular expressions and other conditions)
 * Updated [Portfolio optimization](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)
 * Wrote [Stop signals](https://vectorbt.pro/pvt_7a467f6b/tutorials/stop-signals) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.6.1 (20 Aug, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-161-20-aug-2022 "Permanent link")

 * Scheduler accepts two new arguments: `zero_offset` and `force_missed_run`
 * Migrated the website to another private repository to respect separation of concerns
 * Website is now divided into a public part and a private part (for members only). Most documentation and API documentation have been made exclusive. Added a new getting started guide for members. Each documentation and tutorial page can be auto-converted into a Python code.


# Version 1.6.0 (15 Aug, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-160-15-aug-2022 "Permanent link")

 * Fixed conversion of datetime indexes into nanosecond format on Windows by replacing `int_` to `np.int64`. In addition, implemented the methods [Wrapping.ns_index](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.ns_index), [Wrapping.get_period_ns_index](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.get_period_ns_index), and [Wrapping.ns_freq](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.ns_freq) that do this automatically.
 * Added missing layout keyword arguments to [GenericSRAccessor.plot_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.plot_pattern)
 * Unified the timeframe format across the entire codebase, including custom data classes. This allows for passing human-readable strings such as "15 minutes".
 * Switched the third-party package of [AlpacaData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/alpaca/#vectorbtpro.data.custom.alpaca.AlpacaData) from the outdated `alpaca-trade-api-python` to the newest `alpaca-py`
 * Added configuration examples under the API documentation of each custom data class
 * Added functionality for the configured classes to talk to their globally defined settings, which includes the methods [Configured.get_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.get_settings), [Configured.set_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.set_settings), and [Configured.reset_settings](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Configured.reset_settings). The key pointing towards the global settings is stored in the class variable `_settings_key`. This allows to seamlessly change the settings of custom data classes, for example.
 * Fixed forced import of dill
 * Enabled using mappings in [MappedArray.to_pd](https://vectorbt.pro/pvt_7a467f6b/api/records/mapped_array/#vectorbtpro.records.mapped_array.MappedArray.to_pd)
 * Renamed the default key `_default` to `_def` everywhere ([BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO) instances, index dictionaries, etc.)
 * Fixed getting the duration of range-like records when the index is not datetime-like
 * [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.orders.Orders) has got two new fields: `signed_size` and `value`
 * Refactored iterative helper functions for portfolio. For instance, `get_elem_nb` has been renamed to `select_nb`. Added iterative above and crossover functions. All such functions have been put into the module [portfolio.nb.iter_](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/iter_/).
 * Implemented iterative above and crossover functions in [generic.nb.iter_](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/iter_/)
 * Added methods [Data.switch_class](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.switch_class) and [Data.update_fetch_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.update_fetch_kwargs) to switch between data classes more easily
 * Fixed the Basic RSI tutorial, documentation, and label generators to use the newest `wtype` argument
 * Changed the default start value for cumulative returns from 0 to 1
 * Refactored [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) once again:
 * Renamed `StopExitMode` and `upon_stop_exit` to `StopExitType` and `stop_exit_type` respectively
 * Renamed the suffix of index fields in limit and stop order records from `i` to `idx`
 * Added exit price, exit type, and order type to stop order records. The information is now being pulled from the entry point rather than exit point!
 * Disabled bound checking globally as the vectorbt's functionality has been thoroughly tested. You can still add `boundscheck=True` to the `@njit` decorator to enable bound checking in your function.
 * In-outputs in the flexible mode are now being handled the same as in [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func). Argument `fill_returns` has been disabled for that mode.
 * Delayed the resolution of the arguments `limit_tif` and `limit_expiry` to after broadcasting
 * Simulation iterates in the group-major order in the flexible mode regardless of cash sharing
 * Argument `stop_exit_price` can take a custom price
 * In a group with cash sharing, orders are additionally sorted by bar zone if automatic call sequence is disabled
 * Added a variety of convenient functions for working in callbacks, such as [set_limit_info_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/from_signals/#vectorbtpro.portfolio.nb.from_signals.set_limit_info_nb)
 * Groups are now being valuated strictly using the valuation price (which is mostly the opening price) to avoid the look-ahead bias when working with limit and stop orders
 * Fixed the scenario where the valuation price was set to the order price in limit and stop orders
 * Added a convenient function `vbt.clear_pycache()` to clear the cache of the entire package
 * Added Python 3.10 support ![🥳](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f973.svg)
 * Wrote documentation on [From signals](https://vectorbt.pro/pvt_7a467f6b/documentation/portfolio/from-signals/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.5.0 (29 Jul, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-150-29-jul-2022 "Permanent link")

 * Implemented [from_signals_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/from_signals/#vectorbtpro.portfolio.nb.from_signals.from_signals_nb), which is a cached version that gets used automatically by [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) if none of the `adjust_func_nb`, `signal_func_nb`, and `post_segment_func_nb` were provided. This way, we can avoid repeated compilation in each new runtime.
 * Added a post-segment function to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals). It can be used, for example, for pre-computing custom metrics during the simulation.
 * Created the method [Records.prepare_customdata](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.prepare_customdata), which prepares custom data to be showed when hovering over a Plotly trace, given only the options specified in the field config. This method is utilized in all record classes, such as [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades), so the user can subclass them, define their own custom fields, and they will be displayed on hover automatically.
 * Implemented numerous functions and classes for pattern detection:
 * NB function [interp_resize_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/patterns/#vectorbtpro.generic.nb.patterns.interp_resize_1d_nb) for interpolating values of an array
 * NB function [pattern_similarity_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/patterns/#vectorbtpro.generic.nb.patterns.pattern_similarity_nb) for calculating the similarity score between two arrays
 * NB function [rolling_pattern_similarity_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.rolling_pattern_similarity_nb) and accessor method [GenericAccessor.rolling_pattern_similarity](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_pattern_similarity) for calculating the rolling similarity score between two arrays
 * NB function [find_pattern_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.find_pattern_nb) for searching and storing patterns as range records
 * Class [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges) for holding, analyzing, and plotting the results of one to multiple pattern searches
 * Method [PatternRanges.from_pattern_search](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.from_pattern_search) as a parameterizable interface to [find_pattern_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.find_pattern_nb) that wraps the filled range records with [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges). Works similarly to an indicator.
 * Indicator [PATSIM](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/patsim/#vectorbtpro.indicators.custom.patsim.PATSIM) based on [rolling_pattern_similarity_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.rolling_pattern_similarity_nb)
 * Implemented numerous functions for projections:
 * NB function [map_ranges_to_projections_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.map_ranges_to_projections_nb) and method [Ranges.get_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.get_projections) for mapping (the price during) ranges of any type to projections
 * Accessor method [GenericDFAccessor.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericDFAccessor.plot_projections) for plotting projections from any DataFrame
 * Method [Ranges.plot_projections](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot_projections) for generating and plotting projections using the two methods above
 * Implemented an NB function [get_ranges_from_delta_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.get_ranges_from_delta_nb), the class method [Ranges.from_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.from_delta), and the instance method [Ranges.with_delta](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.with_delta) to map records/mapped arrays/index arrays to ranges of the type [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges) that start at a specific index and last a specific duration. Useful for converting pattern ranges to be able to build projections.
 * Added the argument `klines_type` to [BinanceData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/binance/#vectorbtpro.data.custom.binance.BinanceData) to be able to fetch futures data
 * Implemented an indicator [VWAP](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/vwap/#vectorbtpro.indicators.custom.vwap.VWAP) for calculating VWAP with any frequency-like anchor (daily by default)
 * Refactored custom indicators and their plotting methods:
 * Removed the argument `ewm` in favor of the enumerated argument `wtype` (window type) of the type [WType](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.WType), which allows the moving average and standard deviation to be computed using the new NB functions [ma_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.ma_nb) and [msd_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.msd_nb) respectively
 * Renamed `MSTD` to `MSD` (Moving Standard Deviation)
 * Enumerated types are displayed in the column hierarchy using their field names
 * Switched [RSI](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/rsi/#vectorbtpro.indicators.custom.rsi.RSI) to the Wilder's moving average by default and reimplemented its NB function to be SP
 * Reimplemented [STOCH](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/stoch/#vectorbtpro.indicators.custom.stoch.STOCH) to return fast %K, slow %K, and slow %D
 * Switched [MACD](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/macd/#vectorbtpro.indicators.custom.macd.MACD) to the exponential moving average by default
 * The functionality to combine parameters has been outsourced from [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast) to [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params), and generalized. It can be used by the user to parameterize any function by accepting instances of [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param), as it's done by [PatternRanges.from_pattern_search](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.from_pattern_search). Additionally, [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) instances can now be passed to [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast).
 * Implemented a method [Data.run](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.run), which takes a function or the name of an indicator (all third-party indicators supported), automatically recognizes what features the function accepts (for example, `close` and `volume`), and runs the indicator on that features. This way we can run indicators quickly, as there is no need more to manually search for input names.
 * Drawdowns can now be built from OHLC data, not only close
 * [ArrayWrapper.wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.wrap) supports complex broadcasting
 * Disabled Plotly resampler globally (can be enabled in settings) as it doesn't fit all graphs
 * Enabled bound checking globally (can be disabled in settings) as it makes finding indexing errors easier for the user while making the execution just a bit slower
 * Various record classes allow to be converted into [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges) for range analysis. For example, the class [Drawdowns](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns) has the method [Drawdowns.get_recovery_ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/drawdowns/#vectorbtpro.generic.drawdowns.Drawdowns.get_recovery_ranges) and the auto-generated property `recovery_ranges` to build ranges between the valley point and the recovery point.
 * Created methods for getting a number of the first ([Records.first_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.first_n)), last ([Records.last_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.last_n)), and random ([Records.random_n](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records.random_n)) records
 * Improved formatting of dicts and configs in the API documentation
 * Added flags such as `plot_close` to disable plotting of various traces in ranges, drawdowns, orders, and trades
 * Wrote [Patterns and projections](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.4.2 (28 Jun, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-142-28-jun-2022 "Permanent link")

 * Integrated [plotly-resampler](https://predict-idlab.github.io/plotly-resampler/). If installed, resampled figures/widgets will be used automatically. If not, will fall back to regular Plotly figures/widgets. Can be force-enabled or disabled in the global settings. Only scatter traces are supported.
 * Hit detection of limit order price in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) can be reversed using the argument `limit_reverse`
 * Previously, not expected arguments that were passed to any class method were "swallowed" by the class. Now, passing such arguments will raise an error. No more mistyping arguments!
 * Created a Dockerfile that runs JupyterLab and includes VBT and most of its optional dependencies


# Version 1.4.1 (25 Jun, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-141-25-jun-2022 "Permanent link")

 * Fixed error when providing any stop in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) as an index or a [BCO](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.BCO) instance
 * Added new argument `from_ago` to [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) and [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals), which controls how many bars ago the order information should be taken from. This feature can be used instead of shifting arrays manually. For example, setting `from_ago=1` will shift order information by one bar and thus execute using the next close by default.
 * [PriceType](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.PriceType) has been extended and `price` can now be provided as `nextopen` and `nextclose`, which will set `from_ago` to 1 automatically. Those types cannot be used as part of arrays.
 * Limit signals, stop signals, and user signals in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) can be better distinguished where exactly in a bar they execute. Limit signals can be executed at open and in the middle of the bar. Stop signals can be executed at open, in the middle of the bar, or postponed to close. User signals can be executed at open, in the middle of the bar, and at close. Knowing this allows us to build an accurate execution chain that respects the timing of each signal.


# Version 1.4.0 (21 Jun, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-140-21-jun-2022 "Permanent link")

 * Completely refactored [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals):
 * Signal function `signal_func_nb` takes the context [SignalContext](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.SignalContext) with much more useful information than previously. User-defined arguments are not included in the context but you can always forward them to the function using templates.
 * Preset signal functions take as argument an adjustment function `adjust_func_nb` that allows changing any current information prior to returning the signals, which is especially useful for adjusting limits and stops
 * When there is no signal in any of the columns of a group, the group won't be executed, which results in a great speedup for sparsely-distributed signals
 * Stop loss has been split into two separate stop orders: SL (`sl_stop`) and TSL (`tsl_stop`)
 * TTP has been integrated into TSL by adding a threshold option (`tsl_th`)
 * Added an option for specifying the format of any delta (`delta_format` of type [DeltaFormat](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.DeltaFormat)), which makes possible providing stop values in absolute terms
 * Information on each stop order is now stored in one record array - one record per column, not separate arrays. For example, stop loss information is represented by a record array of data type [sl_info_dt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.sl_info_dt).
 * Added limit order support. Whenever a signal of the limit order type is placed, it's first checked against the current bar information (OHLC if signal was placed at open, only C otherwise). It's then stored in a record array of type [limit_info_dt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.limit_info_dt) that gets propagated throughout time and checked whether the limit has been hit or expired at each bar. Only one active limit order is allowed at a time.
 * Similarly to stop orders, a limit delta can be specified to represent a distance between the initial price (`price`) and the target price. For example, a delta of 0.1 will place a limit order with the target price of 10% above/below the initial price when selling/buying.
 * Limit orders can expire after a time delta (`limit_tif`) or at a specific time (`limit_expiry`). The format of both is controlled by `time_delta_format` of type [TimeDeltaFormat](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.TimeDeltaFormat). If the format is based on index, time deltas and expiry times will be converted into integer, nanosecond format. If the input is a timedelta/datetime-like Series/DataFrame, the pre-processing will remove the timezone and convert to integer format automatically.
 * Previously, stop orders were pure market orders. Now, they can create a limit order once their stop has been hit. They also have their own limit delta.
 * Added options for resolving conflicts between executable and pending signals. For example, providing `upon_opp_limit_conflict="cancelexecute"` will cancel any pending limit order and execute the user-defined signal if it's sign is opposite to the limit order's sign. The same for pending stop orders, which can be cancelled by executable limit/user signals.
 * Order records generated by [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) were extended with the timestamp of signal (`signal_idx`), timestamp of (stop/limit) order creation (`creation_idx`), order type (`type`), and stop type (`stop_type`). The new data type is [fs_order_dt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.fs_order_dt). The new order type can be analyzed using [FSOrders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.orders.FSOrders), which is a subclass of [Orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.orders.Orders). Other simulation methods, such as [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders), still generate records of the type [order_dt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.order_dt).
 * [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) allows providing custom record classes. For example, one can create a custom subclass of [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades) and pass it as `trades_cls` for portfolio to use it by default.
 * Added `ValuePercent` \- a new size type for ordering a percentage of the current group value. But also, `Percent`, `ValuePercent`, and `TargetPercent` have alternatives for provision of percentages in a human-readable format (1.0 = 1%).
 * Instead of passing `-np.inf` or `np.inf` as order/valuation price to represent open/latest and close/price, enumerated values [PriceType](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.PriceType)/ [ValPriceType](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.ValPriceType) can be used. For example, to specify that the opening price should be used as order price, pass `price="open"`.
 * [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter) will also remove the timezone from benchmark returns, and will force the user to select one column (by offering a `column` argument) since quantstats can use only one benchmark column at a time.
 * OHLC chart ([OHLCVDFAccessor.plot](https://vectorbt.pro/pvt_7a467f6b/api/ohlcv/accessors/#vectorbtpro.ohlcv.accessors.OHLCVDFAccessor.plot)) has been updated to match the style of TradingView
 * Specifying the filename when saving or loading any vectorbt object is no longer necessary - vectorbt will use the class name by default
 * Fixed the situation where chunking lots of parameter combinations resulted in a progressive slowdown
 * Fixed handling of input arrays of the data type `float32` in generic NB functions
 * Implemented [TVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/tv/#vectorbtpro.data.custom.tv.TVData), which wraps [tvdatafeed](https://github.com/StreamAlpha/tvdatafeed)
 * Removed the "Close time" column from any DataFrame returned by Binance


# Version 1.3.0 (4 Jun, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-130-4-jun-2022 "Permanent link")

 * Added default resamplers for trade count and VWAP in [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) and resamplers for stock splits, dividends, and other columns in custom data classes
 * Fixed resampling of the open price with NaN values
 * Improved data type handling when wrapping, which previously threw an error when trying to cast a floating array with NaN values to an integer data type. Data type is now being cast softly.
 * Fixed the implementation of VWAP: the indicator now resets with each day or any custom frequency
 * Implemented a method [ArrayWrapper.get_index_grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_grouper), which similarly to [ArrayWrapper.get_resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_resampler) can be passed to any accelerated method in vectorbt that makes use of row grouping
 * Added the ability to generate log returns and daily returns (or both) along with simple returns, such as by using `pf.get_returns(log_returns=True)`. Also, every metric in [ReturnsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor) can natively work on log returns. Since the accessor cannot identify whether the passed return series is simple or log, passing the flag `log_returns=True` is required, which is done automatically by [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio). For instance, to get the accessor with log returns, use `pf.get_returns_acc(log_returns=True)`. To use log/daily returns in portfolio stats, define the corresponding flag in the `settings` dictionary.
 * Implemented NB and SP rolling linear regression using OLS ([GenericAccessor.rolling_linreg](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_linreg)) that returns two arrays: slope and intercept. The implemented algorithm can be used in cointegration tests and is 1100x faster than [RollingOLS](https://www.statsmodels.org/dev/generated/statsmodels.regression.rolling.RollingOLS.html) ![🔥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f525.svg)
 * Implemented two new indicators:
 1. [OLS](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/ols/#vectorbtpro.indicators.custom.ols.OLS) for computing and plotting the rolling linear regression between two time series
 2. [OLSS](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/olss/#vectorbtpro.indicators.custom.ols.OLSS) for computing and plotting the spread and the z-score of the spread of the linear regression between two time series (for cointegration)
 * Added `minp` argument to all custom indicators
 * Updated [PolygonData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/polygon/#vectorbtpro.data.custom.polygon.PolygonData) for `polygon==1.0.0`
 * Implemented row ([Wrapping.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.row_stack)) and column ([Wrapping.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.column_stack)) stacking for vectorbt objects of arbitrary complexity. Since every vectorbt object wraps a bunch of arrays, multiple objects can be effectively merged by stacking their arrays stored internally and unifying other input information. Under the hood, the stacking first takes place between wrappers of all objects using [ArrayWrapper.row_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.row_stack) and [ArrayWrapper.column_stack](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.column_stack). While some objects can be stacked easily, such as [ReturnsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor), stacking records and portfolios is a complex process and requires some assumptions to be made (see the corresponding methods).
 * Refactored the indexing mechanism in [ArrayWrapper](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper) to also return slices whenever possible (because data can be selected faster using slices than index arrays).
 * Lifted the limitation of objects combined together being required to have the same index! Previously, an error was thrown as soon as one of the objects had a different index. Now, similarly to how Pandas does it, indexes of all objects are aligned using a "union" set operation and missing values are set to NaN or any other user-defined value specified in `reindex_kwargs`. Additionally, each broadcastable argument in all the simulation methods of [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio), such as `size` in [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders), have sensible fill values.
 * Fixed axis labels in the [Volume](https://vectorbt.pro/pvt_7a467f6b/api/generic/plotting/#vectorbtpro.generic.plotting.Volume) widget
 * Changed the representation of index ranges from one two-dimensional array to a tuple of one-dimensional arrays, which are easier to manage
 * Deprecated pytz, now using [zoneinfo](https://docs.python.org/3/library/zoneinfo.html)
 * Implemented an entirely new way of creating arrays using index dictionaries. Instead of building an array and setting its data manually, index dictionaries allow providing row and column information as keys and data as values. The function [get_indices](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.get_indices) converts each key of such a dictionary into integer indices, while the method [ArrayWrapper.fill_and_set](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.fill_and_set) sets the corresponding values at those indices by taking into account flexible indexing requirements. This makes it almost too easy to provide data such as order size at specific timestamps or even time intervals. For example, to deposit $100 monthly, provide the following to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals): `cash_deposits=vbt.index_dict({vbt.pointidx(every="M"): 100})` (see the [base.indexing](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/) module). Also, all arguments passed to the broadcaster can be passed as templates to be created using the final shape instead of taking part in actual broadcasting. This means, passing the following to [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) or any other method now works: `size=vbt.RepEval("size = wrapper.fill(); size.iloc[0] = np.inf; size")`, which waits until all other arrays were successfully broadcast and the final wrapper was built, and only then creates an array and fills the first row with `np.inf`.
 * Enabled row selection in all vectorbt objects except [ColumnMapper](https://vectorbt.pro/pvt_7a467f6b/api/records/col_mapper/#vectorbtpro.records.col_mapper.ColumnMapper). In objects with complex data, such as records and portfolios, only slices (that is, non-interrupting ranges) are allowed. For example, selecting a date range from a portfolio means taking the last cash, position, and close prior to the first point in the new slice, and using them as `init_cash`, `init_position`, and `init_price` respectively.
 * Made every simulation method in [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) accept an instance of [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) as `close`. Open, high, low, and close price series will be extracted automatically.
 * [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) now stores and makes use of OHLC data. Moreover, all records from [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges) to [Logs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/logs/#vectorbtpro.portfolio.logs.Logs) also take OHLC data by subclassing a new class [PriceRecords](https://vectorbt.pro/pvt_7a467f6b/api/generic/price_records/#vectorbtpro.generic.price_records.PriceRecords).
 * Implemented MFE and MAE metrics and plots in [Trades](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/trades/#vectorbtpro.portfolio.trades.Trades)
 * Fixed [Portfolio.from_holding](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_holding), which previously set the entry signal at the first timestamp, but since not all assets may start from the first timestamp, the entry signal may be ignored. Now, the entry signal is set dynamically using a signal function whenever a new valid value in `close` is encountered.
 * Optimized indexer in [ArrayWrapper.get_index_points](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points) and [ArrayWrapper.get_index_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_ranges) by adding `indexer_tolerance` argument to the first method and removing `indexer_method` argument from the second method


# Version 1.2.3 (7 May, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-123-7-may-2022 "Permanent link")

 * Fixed marker color in [OHLCVDFAccessor.plot](https://vectorbt.pro/pvt_7a467f6b/api/ohlcv/accessors/#vectorbtpro.ohlcv.accessors.OHLCVDFAccessor.plot) when one of the price points is NaN
 * Ordering in the long-only direction from a short position and short-only direction from a long position is now allowed
 * Fixed output parsing in [IndicatorFactory.from_expr](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_expr)
 * Renamed `plot_as_entry_markers` to [SignalsSRAccessor.plot_as_entries](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_entries) and `plot_as_exit_markers` to [SignalsSRAccessor.plot_as_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_exits). Created two more methods for marking entries ([SignalsSRAccessor.plot_as_entry_marks](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_entry_marks)) and exits ([SignalsSRAccessor.plot_as_exit_marks](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsSRAccessor.plot_as_exit_marks)).
 * Rolling apply can now run on variable, frequency-based windows, such as `7d`
 * Implemented [BaseAccessor.ago](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.ago) for getting the values some periods ago
 * Implemented NB and SP rolling "any" ([GenericAccessor.rolling_any](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_any)) and "all" ([GenericAccessor.rolling_all](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_all))
 * Updated the MTF tutorial with a section on forward filling
 * Indicator parameters can now be manually mapped to an index level using `post_index_func` specified in `param_settings`
 * Complex objects are now counted per type rather than based on their position in [param_to_index](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.utils.params.param_to_index)
 * Implemented an entire module [utils.datetime_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_nb/) with Numba-compiled functions for operations on (mostly integer-formatted) date and time
 * Added contexts [GenEnContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext), [GenExContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext), and [GenEnExContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.GenEnContext) to signal generation functions
 * Signal placement functions are now forced to return the local position of the last placed signal to make the generation (a lot) faster
 * Completely refactored [SignalsAccessor.generate_stop_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_stop_exits) to accept the inputs `entry_ts` and `follow_ts`, and write the in-output `stop_ts_out`. This enables far more options in generating uni-directional stops.
 * Completely refactored [SignalsAccessor.generate_ohlc_exits](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_ohlc_exits) to separate the entry price (`entry_price`) from the open price (`open`), and to better represent and be able to simultaneously process 4 different stop types: SL, TSL, TP, and TTP (new). Also, updated the enum [StopType](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.StopType) according to the new stop types.
 * Refactored ranking. Added the argument `after_reset` to [SignalsAccessor.rank_nb](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.rank_nb) to be able to remove any signal that comes before the first resetting signal. Added the argument `reset_wait` to postpone resetting the position by a number of ticks. Removed `prepare_func` in favor of templates. Also made the function contextualized by adding the context [RankContext](https://vectorbt.pro/pvt_7a467f6b/api/signals/enums/#vectorbtpro.signals.enums.RankContext) with lots of useful information.
 * Implemented after-reset versions for various signal selection functions, such as [SignalsAccessor.first_after](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first_after) for [SignalsAccessor.first](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.first). Also, implemented the method [SignalsAccessor.to_nth](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.to_nth) to select the first `n` signals.
 * Accessor methods in [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor) that accept a UDF now also accept the name of any UDF from [generic.nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/)
 * Fixed casting the column "Trade count" to the integer data type in custom data classes
 * By enabling the `parse_index` flag in [settings.datetime](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.datetime), any index with human-readable datetime strings passed to an array wrapper will be automatically parsed and converted to a Pandas index
 * Added time components to the methods [ArrayWrapper.get_index_points](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points) and [ArrayWrapper.get_index_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_ranges). This, for example, allows signals to be placed and portfolios to be optimized during specific times of the day.
 * Reimplemented the method [SignalsAccessor.clean](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.clean) to take the arguments `force_first`, `keep_conflicts`, and `reverse_order` for a better control of the cleaning process.
 * Implemented a method [Data.transform](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.transform) to transform the underlying data with a UDF and replace the instance
 * Wrote [Signal development](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.2.2 (21 Apr, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-122-21-apr-2022 "Permanent link")

 * Made the call sequence array entirely optional. Prior to this change, the user had to create an array of the same size as the target shape, which is pretty unnecessary and consumes lots of memory. Now, setting `call_seq` to None or `auto` won't require a user-defined array anymore, and only the call sequence for the current row is being kept in memory.
 * The close price in [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) won't broadcast to the full shape anymore. Since all methods deploy flexible indexing, there is no need to expand and materialize the close price. Instead, it keeps its original shape while the broadcasting operation returns a wrapper that holds the target shape and other Pandas metadata. This has one big advantage: lower memory footprint.
 * Disabled `flex_2d` everywhere for more consistency across the codebase. Passing one-dimensional arrays will treat them per-row by default.
 * Fixed the shape in the wrapper returned by [broadcast](https://vectorbt.pro/pvt_7a467f6b/api/base/reshaping/#vectorbtpro.base.reshaping.broadcast)
 * When specifying enum fields such as "targetamount", the mapper will ignore all non-alphanumeric characters by default, thus "Target Amount" can now be passed as well
 * Added the option `incl_doc` to show/hide the docstring of the function when using [phelp](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.phelp)
 * [ArrayWrapper.wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.wrap) will broadcast the to-be-wrapped array using NumPy rules if its shape doesn't match the shape of the wrapper. This way, smaller arrays can expand to the target shape once this is really required - good for memory.
 * Added the option `indexer_method` to specify the indexer method in [BaseAccessor.set](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set) and [BaseAccessor.set_between](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set_between) to control which timestamp (previous or next?) should be used if there is no exact match
 * Cash deposits and cash earnings now respect the cash balance in [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) and [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals). But also, cash deposits now behave the same way as cash earnings: a full array will be created during the simulation if any element of the passed cash deposits is not zero; this array will be overridden in-place at each row and group, and then returned as a part of the simulation output.
 * Added the option `skipna` in [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) for skipping rows where the size in all columns of a group is NaN
 * Wrote documentation on [From orders](https://vectorbt.pro/pvt_7a467f6b/documentation/portfolio/from-orders/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.2.1 (10 Apr, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-121-10-apr-2022 "Permanent link")

 * Fixed check for zero size in [buy_nb](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/nb/core/#vectorbtpro.portfolio.nb.core.buy_nb)
 * Fixed [is_numba_func](https://vectorbt.pro/pvt_7a467f6b/api/utils/checks/#vectorbtpro.utils.checks.is_numba_func) when Numba is disabled globally
 * Use record counts (`order_counts` and `log_counts`) instead of last indices (`last_oidx` and `last_lidx`) in simulation methods with order functions
 * Added `inplace` argument for [BaseAccessor.set](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set) and [BaseAccessor.set_between](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set_between)
 * Fixed `ndim` in [Data.get_symbol_wrapper](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.get_symbol_wrapper)
 * Renamed `ExecuteOrderState` to [AccountState](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.AccountState) and `ProcessOrderState` to [ExecState](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/enums/#vectorbtpro.portfolio.enums.ExecState)
 * Rotational indexing is disabled by default and can be enabled globally using settings
 * Order approximation function takes an instance of `ExecState` instead of state variables
 * Created classes [RandomOHLCData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/random/#vectorbtpro.data.custom.random.RandomData) and [GBMOHLCData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/gbm_ohlc/#vectorbtpro.data.custom.gbm_ohlc.GBMOHLCData) for generation of random OHLC data
 * Made numeric tests more precise by reducing tolerance values
 * Fixed documentation where argument `interval` was used instead of `timeframe`
 * Wrote documentation on [Portfolio simulation](https://vectorbt.pro/pvt_7a467f6b/documentation/portfolio/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.2.0 (3 Apr, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-120-3-apr-2022 "Permanent link")

 * Integrated [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/en/latest/): implemented the function [pypfopt_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.pypfopt_optimize) and an infrastructure around it to run arbitrary optimization models from PyPortfolioOpt with a single function call.
 * Split generation and reduction of resampling metadata. The generation part now resides in [base.resampling.nb](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/nb/), while the reduction part takes place in [generic.nb.apply_reduce](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/apply_reduce/).
 * Implemented wrapper methods for generation of index points ([ArrayWrapper.get_index_points](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_points)) and index ranges ([ArrayWrapper.get_index_ranges](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.get_index_ranges)) from human-readable queries. This helps tremendously in rebalancing.
 * Implemented a [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) class, which is capable of portfolio optimization at regular and irregular intervals, storing the generated allocation data in a compressed format, and analyzing and plotting it. Supports the following input modes:
 1. Custom allocation function ([PortfolioOptimizer.from_allocate_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocate_func))
 2. Custom optimization function ([PortfolioOptimizer.from_optimize_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_optimize_func))
 3. Custom allocations ([PortfolioOptimizer.from_allocations](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_allocations))
 4. Custom filled allocations ([PortfolioOptimizer.from_filled_allocations](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_filled_allocations))
 5. Random allocation ([PortfolioOptimizer.from_random](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_random))
 6. Uniform allocation ([PortfolioOptimizer.from_uniform](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_uniform))
 7. PyPortfolioOpt ([PortfolioOptimizer.from_pypfopt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_pypfopt))
 8. Universal Portfolios ([PortfolioOptimizer.from_universal_algo](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_universal_algo))
 * Added time frames as a parameter to TA-Lib indicators. This will downsample the input data (such as the close price), run the indicator, and upsample it back to the original time frame. Multiple time frame combinations are supported out of the box.
 * Implemented convenience methods [BaseAccessor.set](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set) and [BaseAccessor.set_between](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.set_between) for setting data based on index points and ranges respectively
 * Added an attribute class [ExceptLevel](https://vectorbt.pro/pvt_7a467f6b/api/base/indexes/#vectorbtpro.base.indexes.ExceptLevel) that can be used to specify the level by which **not** to group in `group_by`. This is handy when there are many levels and there is a need to group by all levels except assets, for example.
 * Wrote [Portfolio optimization](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.1.2 (12 Mar, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-112-12-mar-2022 "Permanent link")

 * Added option `skipna` to run a TA-Lib indicator on non-NA values only (TA-Lib hates NaN)
 * Implemented a range of (NB and SP) resampling functions for
 1. Getting the latest information at each timestamp, supporting bar data ([GenericAccessor.realign](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.realign))
 2. Resampling to a custom index, both as a regular and meta method ([GenericAccessor.resample_to_index](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_to_index))
 3. Resampling between custom bounds, both as a regular and meta method ([GenericAccessor.resample_between_bounds](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.resample_between_bounds))
 * Implemented a [Resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler) class, which acts as a mapper between the source and target index for best flexibility. It can parse a resampler from Pandas. Also, implemented a range of helper functions for
 1. Generating a datetime index from frequency (NB)
 2. Getting the right bound of a datetime index
 3. Mapping one datetime index to another (NB, [Resampler.map_to_target_index](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.map_to_target_index))
 4. Getting datetime index difference (NB, [Resampler.index_difference](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.index_difference))
 * Implemented an interface for resampling complex vectorbt objects in form of an abstract method [Wrapping.resample](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping.resample). Also, defined resampling logic for all classes whose Pandas objects can be resampled:
 1. [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data)
 2. [OHLCVDFAccessor](https://vectorbt.pro/pvt_7a467f6b/api/ohlcv/accessors/#vectorbtpro.ohlcv.accessors.OHLCVDFAccessor)
 3. [ReturnsAccessor](https://vectorbt.pro/pvt_7a467f6b/api/returns/accessors/#vectorbtpro.returns.accessors.ReturnsAccessor)
 4. [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio)
 5. [Records](https://vectorbt.pro/pvt_7a467f6b/api/records/base/#vectorbtpro.records.base.Records) and all its subclasses
 * Introduced the feature config [Data.feature_config](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.feature_config), which can be used to define resampling function for each custom column in [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data). OHLCV data is resampled automatically.
 * Completely refactored handling of in-outputs in [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio). Introduced the in-output config [Portfolio.in_output_config](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.in_output_config), which can be used to define the layout, array type, and resampling function for each custom in-output. Appending suffixes (such as `_pcg`) to in-output names is now optional. The suffix `_pcgs` has been renamed to `_cs`. The resolution mechanism for in-outputs has been distributed over multiple class methods and made more transparent.
 * The in-output name for returns has been changed from `returns_pcgs` to just `returns`
 * Added argument `init_price` to specify the original entry price of `init_position`. This makes calculation of P&L and other metrics more precise and flexible.
 * Fixed the issue where only the first row in `cash_deposits` was applied in [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) and [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals)
 * Distributed generic Numba-compiled functions across multiple files
 * Enabled passing additional keyword arguments to `get_klines` in [BinanceData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/binance/#vectorbtpro.data.custom.binance.BinanceData)
 * Wrote [MTF analysis](https://vectorbt.pro/pvt_7a467f6b/tutorials/mtf-analysis) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.1.1 (25 Feb, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-111-25-feb-2022 "Permanent link")

 * [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) now removes duplicates in index while keeping only the last entry
 * Added option `concat` to [Data.update](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.update) for being able to disable concatenation of new data with existing data and to only return new data
 * Added support for chunking in [CSVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/csv/#vectorbtpro.data.custom.csv.CSVData) and [HDFData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/hdf/#vectorbtpro.data.custom.hdf.HDFData) using `chunk_func`
 * Implemented class [DataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.DataSaver) that can periodically collect and save data to disk, and two its subclasses: [CSVDataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.CSVDataSaver) for writing to CSV files and [HDFDataSaver](https://vectorbt.pro/pvt_7a467f6b/api/data/saver/#vectorbtpro.data.saver.HDFDataSaver) for writing to HDF files. This way, one can gradually collect and persist any data from any data provider!
 * Fixed unpickling of [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config)
 * Fixed scheduling in [DataUpdater](https://vectorbt.pro/pvt_7a467f6b/api/data/updater/#vectorbtpro.data.updater.DataUpdater) such that repeatedly stopping and starting the same updater won't trigger the same job more than once
 * [QSAdapter](https://vectorbt.pro/pvt_7a467f6b/api/returns/qs_adapter/#vectorbtpro.returns.qs_adapter.QSAdapter) will now remove timezone info automatically to prevent issues in QuantStats
 * Implemented three new data classes:
 1. [PolygonData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/polygon/#vectorbtpro.data.custom.polygon.PolygonData) for [Polygon.io](https://polygon.io/). Can load data of any size in bunches and respects the API rate limits.
 2. [AVData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/av/#vectorbtpro.data.custom.av.AVData) for [Alpha Vantage](https://www.alphavantage.co/). Does not use the `alpha_vantage` library, which isn't actively developed. Instead, it implements a parser of the Alpha Vantage's documentation website and handles communication with the API using the parsed metadata. This enables instant reaction to any changes in the Alpha Vantage's API. The user can still disable the parsing and specify every bit of information manually.
 3. [NDLData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/ndl/#vectorbtpro.data.custom.ndl.NDLData) for [Nasdaq Data Link](https://data.nasdaq.com/). Supports (time-series) datasets. 
 * Fixed the condition for a backward fill in [fbfill_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/base/#vectorbtpro.generic.nb.base.fbfill_nb)
 * Fixed passing `execute_kwargs` in [IndicatorFactory.with_apply_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_apply_func). Also, whenever `apply_func` is Numba compiled, makes the parameter selection function Numba compiled as well (`jit_select_params=True`) and also releases the GIL (`nogil=True`), so the indicator can be used in multithreading right away.


# Version 1.1.0 (20 Feb, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-110-20-feb-2022 "Permanent link")

 * Removed support for Python 3.6. Wanted to add support for Python 3.10 but stumbled upon issues that can be followed in [numba/numba#7812](https://github.com/numba/numba/issues/7812 "GitHub Issue: numba/numba #7812") and [numba/numba#7839](https://github.com/numba/numba/issues/7839 "GitHub Issue: numba/numba #7839").
 * Removed [Bottleneck](https://github.com/pydata/bottleneck) from optional requirements as it causes installation issues, but it can still be installed manually
 * Formatted the entire codebase with [Black](https://black.readthedocs.io/en/stable/) ![⬛](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/2b1b.svg)
 * One or more symbols can be selected from a [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) instance
 * Refactored [Data.fetch_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.fetch_kwargs) into a symbol dictionary. Getting the keyword arguments used for fetching a specific symbol is now as simple as `fetch_kwargs[symbol]`.
 * Implemented a method [Data.merge](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.merge) for merging multiple [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) instances
 * One or more symbols can be renamed in a [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) instance
 * Improved aggregation of metrics in [StatsBuilderMixin](https://vectorbt.pro/pvt_7a467f6b/api/generic/stats_builder/#vectorbtpro.generic.stats_builder.StatsBuilderMixin)
 * Removed `ohlc` accessor to avoid confusion. The only accessor is now `ohlcv`.
 * [Data.plot](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.plot) automatically plots the data as a candlestick chart if it can find the right price columns, otherwise, it plots each column as a separate line (as it was previously). Also, one can now select a symbol to plot using the `symbol` argument.
 * One metric/subplot can be expanded into multiple metrics/subplots using templates. This enables displaying a variable number of metrics/subplots.
 * [Data.plots](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.plots) now plots one subplot per symbol
 * Delimiter is recognized automatically when dealing with CSV and TSV files
 * Implemented a function for pretty-printing directory trees - [tree](https://vectorbt.pro/pvt_7a467f6b/api/utils/path_/#vectorbtpro.utils.path_.tree)
 * Refactored the path matching mechanism for CSV and HDF files. In particular:
 * Path unfolding has been renamed to path matching
 * Wildcards (`*`) are now supported for groups and keys in HDF files
 * Paths can be further filtered using a regex pattern `match_regex`
 * Functions for path matching have become class methods for seamless inheritance
 * The argument `parse_paths` in [FileData.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.pull) has been renamed to `match_paths`
 * The argument `path` in [FileData.pull](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData.pull) has been renamed to `paths`
 * Symbols that return `None` or an empty array are skipped. When `raise_on_error` is True, any symbol raising an error is skipped as well.
 * Similar to the Python's `help` command, vectorbt now has a function [phelp](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.phelp) that pretty-prints the arguments and docstring of any function. It's main advantage is the ability to skip annotations, which sometimes reduce readability when exploring more complex vectorbt functions using `help`.
 * Settings have been refactored once again: it's now clearly visible which key can be accessed via the dot notation (_hint_ : it must be of type [ChildDict](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.ChildDict)). Also, the argument `convert_dicts_` in [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config) has been renamed to `convert_children_`.
 * Moved default values of various [Data](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data) classes from the [data.custom](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/) module to [settings.data](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.data) to be able to set them globally
 * Minor fixes and enhancements across the project
 * Wrote documentation on [Data](https://vectorbt.pro/pvt_7a467f6b/documentation/data/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.0.10 (11 Feb, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-1010-11-feb-2022 "Permanent link")

 * Moved the `per_column` logic from [IndicatorBase.run_pipeline](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorBase.run_pipeline) to the indicator function (`custom_func`). Previously, the indicator function received only one column and parameter combination at a time, which created issues for caching. Now, the pipeline passes all columns and parameter combinations, so it's the responsibility of the indicator function to distribute the combinations properly (no worries, `apply_func` will handle it automatically).
 * Apply functions (`apply_func`) can run on one-dimensional input data just as well as on two-dimensional input data by passing `takes_1d=True` to [IndicatorFactory.with_apply_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_apply_func). This mode splits each input array (both Pandas and NumPy) into columns and builds a product of columns and parameter combinations. Benchmarks show that this has no real implications on performance + functions that process one column at a time are much easier to write.
 * `@talib` and `@talib_1d` annotations were merged into a single `@talib` annotation that can handle both one and two-dimensional input data
 * Removed automatic module search when parsing indicator expressions, which degraded performance. It's now recommended to use multi-line expressions and `import` statements.
 * Renamed `kwargs_to_args` to `kwargs_as_args` in [IndicatorFactory.with_apply_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_apply_func)
 * Refactored the [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute) function to enable chunking in indicators
 * Fixed the calculation of crossovers. Previously, it ignored a crossover if there was another crossover one tick behind.
 * Greatly optimized stacking of output arrays with one column after running an indicator
 * Refactored the `as_attrs_` behavior in [Config](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config). Keys won't be attached to the config instance anymore but managed dynamically (= less side effects when pickling and unpickling).
 * Implemented a wide range of inputs states, output states, and accumulators for the use in streaming functions, such as in [rolling_mean_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/rolling/#vectorbtpro.generic.nb.rolling.rolling_mean_1d_nb)
 * Made flexible indexing with [flex_select_auto_nb](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.flex_select_auto_nb) rotational. For example, if there is a smaller array with 3 columns and a bigger one with 6 columns, there is no need to tile the smaller array 2 times to match the bigger one - we can simply rotate over the smaller array.
 * Added support for short names in indicator expressions
 * Returns can be pre-computed in both [Portfolio.from_orders](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_orders) and [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) by passing the `fill_returns=True` flag
 * Fixed [save_animation](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#vectorbtpro.utils.image_.save_animation), which previously produced one less iteration
 * Wrote [SuperFast SuperTrend](https://vectorbt.pro/pvt_7a467f6b/tutorials/superfast-supertrend) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.0.9 (2 Feb, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-109-2-feb-2022 "Permanent link")

 * Upgraded the parser of indicator expressions:
 * Can evaluate the expression using [pandas.eval](https://pandas.pydata.org/docs/reference/api/pandas.eval.html)
 * Special variables and commands are annotated with the prefix `@`
 * Supports single as well as multi-line expressions
 * Context variables with the same name aren't needlessly re-computed anymore
 * Can parse the class name at the beginning of the expression
 * Supports one and two-dimensional TA-Lib indicators out-of-the-box
 * Supports magnet names for inputs, in-outputs, and parameters
 * Can parse settings from within the expression and pass them to [IndicatorFactory.from_expr](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_expr)
 * Can automatically resolve annotated indicators
 * Enabled plotting of any TA-Lib indicator programmatically by parsing its output flags
 * Implemented Numba-compiled functions for Wilder's EMA and STD (SP)
 * Renamed `from_custom_func` to `with_custom_func` and `from_apply_func` to `with_apply_func` since those are instance methods
 * Set `minp` (minimum periods) to `None` in generic rolling functions to make the values of incomplete windows NaN
 * Made parameter selection optional in [IndicatorFactory.with_apply_func](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_apply_func). Setting `select_params` to False will prepend the iteration index to the arguments of the apply function.
 * Refactored the `keep_pd=True` flag to avoid back-and-forth conversion between broadcasted Pandas objects and NumPy arrays. Pandas objects are now directly forwarded to the custom function without any pre-processing.
 * Renamed `custom_output_props` to `lazy_outputs`
 * Renamed `select_one` and `select_one_from_obj` to `select_col` and `select_col_from_obj` respectively in [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping)
 * Input arrays passed to TA-Lib indicators are converted to the data type `np.double`
 * Renamed `mapping` to `context` when it comes to templates
 * Updated plotting methods in [indicators.custom](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/)
 * [Data.get](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.get) also accepts symbol(s)
 * Greatly optimized [Data.concat](https://vectorbt.pro/pvt_7a467f6b/api/data/base/#vectorbtpro.data.base.Data.concat)
 * Wrote documentation on [Indicators](https://vectorbt.pro/pvt_7a467f6b/documentation/indicators/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.0.8 (25 Jan, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-108-25-jan-2022 "Permanent link")

 * Implemented the following Numba-compiled functions:
 * Ranking and rolling ranking (SP)
 * Covariance and rolling covariance (SP)
 * Rolling sum and product (SP)
 * Rolling weighted average (SP)
 * Rolling argmin and argmax
 * Demeaning within a group
 * Implemented volume-weighted average price (VWAP)
 * Built a powerful engine for parsing indicator expressions. Using [IndicatorFactory.from_expr](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_expr), an indicator can be automatically constructed out of an expression string, such as `"rolling_mean((low + high) / 2, 10)"`! [IndicatorFactory](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory) can recognize common inputs such as `low` and the number of outputs. For parameters and more cryptic inputs, the user can provide a prefix: `"rolling_mean(abs(in_ts), p_window)"`. Moreover, apart from preset functions such as `rolling_mean`, whenever it recognizes an unknown function, searches for its implementation in various parts of vectorbt and NumPy. Supports NumExpr to accelerate simpler expressions.
 * Translated each one of [WorldQuant's 101 Formulaic Alphas](https://arxiv.org/pdf/1601.00991.pdf) into an indicator expression and implemented a convenience method [IndicatorFactory.from_wqa101](https://vectorbt.pro/pvt_7a467f6b/api/indicators/factory/#vectorbtpro.indicators.factory.IndicatorFactory.from_wqa101) (also as a shortcut `vbt.wqa101`) for executing them
 * Unified column grouping for matrices and records across the entire codebase. Most logic now resides in the sub-package [base.grouping](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/). Also, most functions (apart from the portfolio-related ones) do not require strict group ordering anymore.
 * Added chunking specification for labeling functions
 * Fixed [Config.prettify](https://vectorbt.pro/pvt_7a467f6b/api/utils/config/#vectorbtpro.utils.config.Config.prettify) for non-string keys
 * Wrote [Basic RSI strategy](https://vectorbt.pro/pvt_7a467f6b/tutorials/basic-rsi) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.0.7 (16 Jan, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-107-16-jan-2022 "Permanent link")

 * Changed `int_` to `np.integer` when passed to `np.issubdtype`
 * Refactored auto-aligned initial cash to be based on free cash flows and cash deposits
 * Upgraded the string parser of [deep_getattr](https://vectorbt.pro/pvt_7a467f6b/api/utils/attr_/#vectorbtpro.utils.attr_.deep_getattr) to accept strings of chained method calls (more intuitive)
 * Implemented superfast Pearson correlation coefficient and its rolling version
 * Created the class [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable), which combines [Wrapping](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.Wrapping) and builder mixins
 * Metrics and subplots that require a single column won't raise an error if the object is two-dimensional and has only one column
 * [Grouper](https://vectorbt.pro/pvt_7a467f6b/api/base/grouping/#vectorbtpro.base.grouping.base.Grouper) can return a group map, which isn't tied to a strict group ordering and is easier to use outside of Numba
 * Wrote documentation on [Building blocks](https://vectorbt.pro/pvt_7a467f6b/documentation/building-blocks/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.0.6 (9 Jan, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-106-9-jan-2022 "Permanent link")

 * Benchmark can be disabled by passing `bm_close=False` to [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio)
 * Wrote documentation on [Fundamentals](https://vectorbt.pro/pvt_7a467f6b/documentation/fundamentals/) ![📔](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d4.svg)


# Version 1.0.5 (8 Jan, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-105-8-jan-2022 "Permanent link")

 * Fixed [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals) for `direction='both'` and `size_type='value'`. Previously, the position couldn't be properly reversed.
 * Avoid sorting paths in [FileData](https://vectorbt.pro/pvt_7a467f6b/api/data/custom/file/#vectorbtpro.data.custom.file.FileData) if they are passed as a sequence


# Version 1.0.4 (6 Jan, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-104-6-jan-2022 "Permanent link")

 * Set benchmark easily and also globally ([#32](https://github.com/polakowo/vectorbt.pro/issues/32 "GitHub Issue: polakowo/vectorbt.pro #32")) by passing `bm_close` to [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio). Works similarly to [Portfolio.close](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.close).
 * Shortened registry names (such as from `ca_registry` to `ca_reg`)


# Version 1.0.3 (5 Jan, 2022)[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/release-notes/2022/#version-103-5-jan-2022 "Permanent link")

 * Automatic discovery of symbols for local data ([#27](https://github.com/polakowo/vectorbt.pro/issues/27 "GitHub Issue: polakowo/vectorbt.pro #27")): No more need to specify a path to each CSV/HDF file or HDF key. Passing a path to a directory will traverse each file in this directory. Passing a [glob-style pattern](https://en.wikipedia.org/wiki/Glob_\(programming\)) will use `glob.glob` to traverse all files that match this pattern. Passing an HDF file will extract all keys inside this file. All the options above can be combined in arbitrary ways.
 * Minor fixes in the formatting module
 * Removed strict ordering of group and shape suffixes in [Portfolio.get_in_output](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.get_in_output) and [Portfolio.in_outputs_indexing_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.in_outputs_indexing_func). For instance, there is no more difference between in-outputs with names `myinout_2d_pc` and `myinout_pc_2d`.
 * Improved readability of cacheable setups: When displaying the status overview, objects are represented by shorter, human-readable strings, and also contain the position of this object in all the objects registered globally and sorted by time. For instance, `portfolio:2` means that there exist 2 more [Portfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio) objects created earlier than this object. This makes it easier to manage memory and to debug garbage collection.
 * Wrapping in-outputs automatically: Implements the method [Portfolio.get_in_output](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.get_in_output), which can be used to access and automatically wrap any in-output object from [Portfolio.in_outputs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.in_outputs).
 * All registries can be accessed directly via `vbt`
 * Updates and minor fixes to the ca_registry and ch_registry modules
 * Disabled parallelization of [generate_both](https://vectorbt.pro/pvt_7a467f6b/api/signals/accessors/#vectorbtpro.signals.accessors.SignalsAccessor.generate_both), which behaved unexpectedly
 * Fixed `in_outputs` in [Portfolio.from_order_func](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_order_func) to work with Numba 0.53.1. This requires the user to define `in_outputs` as a named tuple prior to passing to the method.
 * Added mapping of `window` to `rolling_period` in the QuantStats adapter