# Integrations[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#integrations "Permanent link")

[PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer) integrates nicely with various third-party libraries.


# PyPortfolioOpt[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#pyportfolioopt "Permanent link")

> [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/en/latest/) is a library that implements portfolio optimization methods, including classical efficient frontier techniques and Black-Litterman allocation, as well as more recent developments in the field like shrinkage and Hierarchical Risk Parity, along with some novel experimental features like exponentially-weighted covariance matrices.

PyPortfolioOpt implements a range of optimization methods that are very easy to use. The optimization procedure consists of several distinct steps (some of them may be skipped depending on the optimizer):

 * Calculate the expected returns (mostly located in `pfopt.expected_returns`)
 * Calculate the covariance matrix (mostly located in `pfopt.risk_models`)
 * Initialize and set up an optimizer (mostly located in `pypfopt.efficient_frontier`, with the base class located in `pypfopt.base_optimizer`) including objectives, constraints, and target
 * Run the optimizer to get the weights
 * Convert the weights into a discrete allocation (optional)

For example, let's perform the mean-variance optimization (MVO) for maximum Sharpe:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-1)>>> from pypfopt.expected_returns import mean_historical_return
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-2)>>> from pypfopt.risk_models import CovarianceShrinkage
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-3)>>> from pypfopt.efficient_frontier import EfficientFrontier
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-5)>>> expected_returns = mean_historical_return(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-6)>>> cov_matrix = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-7)>>> optimizer = EfficientFrontier(expected_returns, cov_matrix)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-8)>>> weights = optimizer.max_sharpe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-9)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-10)OrderedDict([('ADAUSDT', 0.1166001117223088),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-11) ('BNBUSDT', 0.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-12) ('BTCUSDT', 0.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-13) ('ETHUSDT', 0.8833998882776911),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-0-14) ('XRPUSDT', 0.0)])
 
[/code]


# Parsing[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#parsing "Permanent link")

Thanks to an outstanding work done by [@robertmartin8](https://github.com/robertmartin8 "GitHub User: robertmartin8"), the entire codebase of PyPortfolioOpt (with a few exceptions) has consistent argument and function namings, such that we can build a semantic web of functions acting as inputs to other functions. Why this is important? Because the user just needs to provide the target function (let's say, `EfficientFrontier.max_sharpe`), and we can programmatically figure out the entire call stack having the pricing data alone! And if the user passes any additional keyword arguments, we can check which functions from the stack accept those arguments and automatically pass them.

For the example above, the web looks like this:

(Reload the page if the diagram doesn't show up)

And here comes vectorbt into play. First, it implements a function [resolve_pypfopt_func_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.resolve_pypfopt_func_kwargs) that takes an arbitrary PyPortfolioOpt function, and resolves its arguments. Whenever an argument passed by the user has been matched with an argument in the function's signature, it marks this argument to be passed to the function. Let's try it out on expected returns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-1)>>> from vectorbtpro.portfolio.pfopt.base import resolve_pypfopt_func_kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-3)>>> vbt.phelp(mean_historical_return) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-4)mean_historical_return(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-5) prices,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-6) returns_data=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-7) compounding=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-8) frequency=252,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-9) log_returns=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-10)):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-11) Calculate annualised mean (daily) historical return from input (daily) asset prices.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-12) Use ``compounding`` to toggle between the default geometric mean (CAGR) and the
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-13) arithmetic mean.
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-15)>>> print(vbt.prettify(resolve_pypfopt_func_kwargs(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-16)... mean_historical_return, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-17)... prices=data.get("Close"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-18)... freq="1h", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-19)... year_freq="365d",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-20)... other_arg=100 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-21)... )))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-22){
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-23) 'prices': <pandas.core.frame.DataFrame object at 0x7f9428052c50 of shape (8767, 5)>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-24) 'returns_data': False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-25) 'compounding': True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-26) 'frequency': 8760.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-27) 'log_returns': False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-1-28)}
 
[/code]

 1. 2. 3. 4. 

And now let's run it on `EfficientFrontier`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-1)>>> print(vbt.prettify(resolve_pypfopt_func_kwargs(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-2)... EfficientFrontier, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-3)... prices=data.get("Close")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-4)... )))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-5){
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-6) 'expected_returns': <pandas.core.series.Series object at 0x7f9479927128 of shape (5,)>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-7) 'cov_matrix': <pandas.core.frame.DataFrame object at 0x7f94280528d0 of shape (5, 5)>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-8) 'weight_bounds': (
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-9) 0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-10) 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-11) ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-12) 'solver': None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-13) 'verbose': False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-14) 'solver_options': None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-2-15)}
 
[/code]

We see that vectorbt magically resolved arguments `expected_returns` and `cov_matrix` using [resolve_pypfopt_expected_returns](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.resolve_pypfopt_expected_returns) and [resolve_pypfopt_cov_matrix](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.resolve_pypfopt_cov_matrix) respectively. If we provided those two arguments manually, vectorbt would use them right away. We can also provide those arguments as strings to change the function with which they are generated:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-1)>>> print(vbt.prettify(resolve_pypfopt_func_kwargs(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-2)... EfficientFrontier, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-3)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-4)... expected_returns="ema_historical_return",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-5)... cov_matrix="sample_cov"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-6)... )))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-7){
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-8) 'expected_returns': <pandas.core.series.Series object at 0x7f9428044cf8 of shape (5,)>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-9) 'cov_matrix': <pandas.core.frame.DataFrame object at 0x7f942805bf60 of shape (5, 5)>,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-10) 'weight_bounds': (
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-11) 0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-12) 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-13) ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-14) 'solver': None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-15) 'verbose': False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-16) 'solver_options': None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-3-17)}
 
[/code]


# Auto-optimization[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#auto-optimization "Permanent link")

Knowing how to parse and resolve function arguments, vectorbt implements a function [pypfopt_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.pypfopt_optimize), which takes user requirements and translates them into function calls. The usage of this function cannot be easier!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-4-1)>>> vbt.pypfopt_optimize(prices=data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-4-2){'ADAUSDT': 0.1166,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-4-3) 'BNBUSDT': 0.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-4-4) 'BTCUSDT': 0.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-4-5) 'ETHUSDT': 0.8834,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-4-6) 'XRPUSDT': 0.0}
 
[/code]

In short, [pypfopt_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.pypfopt_optimize) first resolves the optimizer using [resolve_pypfopt_optimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.resolve_pypfopt_optimizer), which, in turn, triggers a waterfall of argument resolutions by [parsing arguments](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#parsing), including the calculation of the expected returns and the risk model quantifying asset risk. Then, it adds objectives and constraints to the optimizer instance. Finally, it calls the target metric method (such as `max_sharpe`) or custom convex/non-convex objective using the same parsing procedure as we did above. If wanted, it can also translate continuous weights into discrete ones using `DiscreteAllocation`.

Since multiple PyPortfolioOpt functions can require the same argument that has to be pre-computed yet, [pypfopt_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.pypfopt_optimize) deploys a built-in caching mechanism. Additionally, if any of the arguments weren't used, it throws a warning (which can be mitigated by setting `silence_warnings` to True) stating that an argument wasn't required by any function in the call stack.

Below, we will demonstrate various optimizations done both using PyPortfolioOpt and vectorbt. Optimizing a long/short portfolio to minimise total variance:

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-1)>>> S = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-2)>>> ef = EfficientFrontier(None, S, weight_bounds=(-1, 1))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-3)>>> ef.min_volatility()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-4)>>> weights = ef.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-5)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-6)OrderedDict([('ADAUSDT', -0.01118),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-7) ('BNBUSDT', 0.09695),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-8) ('BTCUSDT', 0.9624),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-9) ('ETHUSDT', -0.10516),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-5-10) ('XRPUSDT', 0.05699)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-1)>>> vbt.pypfopt_optimize( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-3)... expected_returns=None,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-4)... weight_bounds=(-1, 1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-5)... target="min_volatility"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-7){'ADAUSDT': -0.01118,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-8) 'BNBUSDT': 0.09695,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-9) 'BTCUSDT': 0.9624,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-10) 'ETHUSDT': -0.10516,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-6-11) 'XRPUSDT': 0.05699}
 
[/code]

 1. `CovarianceShrinkage.ledoit_wolf` and `EfficientFrontier` are used by default

Optimizing a portfolio to maximise the Sharpe ratio, subject to direction constraints:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-7-1)directions = ["long", "long", "long", "short", "short"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-7-2)direction_mapper = dict(zip(data.symbols, directions))
 
[/code]

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-1)>>> from pypfopt.expected_returns import capm_return
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-3)>>> mu = capm_return(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-4)>>> S = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-5)>>> ef = EfficientFrontier(mu, S, weight_bounds=(-1, 1))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-6)>>> for symbol, direction in direction_mapper.items():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-7)... idx = data.symbols.index(symbol)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-8)... if direction == "long":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-9)... ef.add_constraint(lambda w, _idx=idx: w[_idx] >= 0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-10)... if direction == "short":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-11)... ef.add_constraint(lambda w, _idx=idx: w[_idx] <= 0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-12)>>> ef.max_sharpe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-13)>>> weights = ef.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-14)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-15)OrderedDict([('BTCUSDT', 0.26614),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-16) ('ETHUSDT', 0.433),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-17) ('BNBUSDT', 0.30086),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-18) ('XRPUSDT', 0.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-8-19) ('ADAUSDT', 0.0)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-1)>>> constraints = []
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-2)>>> for symbol, direction in direction_mapper.items():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-3)... idx = data.symbols.index(symbol)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-4)... if direction == "long":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-5)... constraints.append(lambda w, _idx=idx: w[_idx] >= 0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-6)... if direction == "short":
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-7)... constraints.append(lambda w, _idx=idx: w[_idx] <= 0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-8)>>> vbt.pypfopt_optimize( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-9)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-10)... expected_returns="capm_return",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-11)... cov_matrix="ledoit_wolf",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-12)... target="max_sharpe",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-13)... weight_bounds=(-1, 1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-14)... constraints=constraints,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-16){'BTCUSDT': 0.26614,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-17) 'ETHUSDT': 0.433,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-18) 'BNBUSDT': 0.30086,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-19) 'XRPUSDT': 0.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-9-20) 'ADAUSDT': 0.0}
 
[/code]

Optimizing a portfolio to maximise the Sharpe ratio, subject to sector constraints:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-1)>>> sector_mapper = {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-2)... "ADAUSDT": "DeFi",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-3)... "BNBUSDT": "DeFi",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-4)... "BTCUSDT": "Payment",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-5)... "ETHUSDT": "DeFi",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-6)... "XRPUSDT": "Payment"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-7)... }
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-8)>>> sector_lower = {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-9)... "DeFi": 0.75
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-10)... }
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-10-11)>>> sector_upper = {}
 
[/code]

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-1)>>> mu = capm_return(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-2)>>> S = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-3)>>> ef = EfficientFrontier(mu, S)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-4)>>> ef.add_sector_constraints(sector_mapper, sector_lower, sector_upper)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-5)>>> adausdt_index = ef.tickers.index("ADAUSDT")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-6)>>> ef.add_constraint(lambda w: w[adausdt_index] == 0.10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-7)>>> ef.max_sharpe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-8)>>> weights = ef.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-9)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-10)OrderedDict([('ADAUSDT', 0.1),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-11) ('BNBUSDT', 0.2772),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-12) ('BTCUSDT', 0.0524),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-13) ('ETHUSDT', 0.3728),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-11-14) ('XRPUSDT', 0.1976)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-1)>>> adausdt_index = list(sector_mapper.keys()).index("ADAUSDT")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-2)>>> vbt.pypfopt_optimize( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-3)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-4)... expected_returns="capm_return",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-5)... sector_mapper=sector_mapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-6)... sector_lower=sector_lower,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-7)... sector_upper=sector_upper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-8)... constraints=[lambda w: w[adausdt_index] == 0.10]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-10){'ADAUSDT': 0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-11) 'BNBUSDT': 0.2772,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-12) 'BTCUSDT': 0.0524,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-13) 'ETHUSDT': 0.3728,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-12-14) 'XRPUSDT': 0.1976}
 
[/code]

 1. `CovarianceShrinkage.ledoit_wolf`, `EfficientFrontier`, and `EfficientFrontier.max_sharpe` are used by default

Optimizing a portfolio to maximise return for a given risk, subject to sector constraints, with an L2 regularisation objective:

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-1)>>> from pypfopt.objective_functions import L2_reg
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-3)>>> mu = capm_return(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-4)>>> S = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-5)>>> ef = EfficientFrontier(mu, S)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-6)>>> ef.add_sector_constraints(sector_mapper, sector_lower, sector_upper)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-7)>>> ef.add_objective(L2_reg, gamma=0.1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-8)>>> ef.efficient_risk(0.15)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-9)>>> weights = ef.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-10)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-11)OrderedDict([('ADAUSDT', 0.26004),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-12) ('BNBUSDT', 0.24466),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-13) ('BTCUSDT', 0.10778),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-14) ('ETHUSDT', 0.2453),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-13-15) ('XRPUSDT', 0.14222)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-1)>>> vbt.pypfopt_optimize( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-3)... expected_returns="capm_return",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-4)... sector_mapper=sector_mapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-5)... sector_lower=sector_lower,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-6)... sector_upper=sector_upper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-7)... objectives=["L2_reg"], 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-8)... gamma=0.1, 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-9)... target="efficient_risk",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-10)... target_volatility=0.15 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-12){'ADAUSDT': 0.26004,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-13) 'BNBUSDT': 0.24466,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-14) 'BTCUSDT': 0.10778,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-15) 'ETHUSDT': 0.2453,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-14-16) 'XRPUSDT': 0.14222}
 
[/code]

 1. `CovarianceShrinkage.ledoit_wolf` and `EfficientFrontier` are used by default
 2. Objective can be provided as an attribute of the `pypfopt.objective_functions` module
 3. Gets recognized as an argument of the objective function
 4. Gets recognized as an argument of the target metric method

Optimizing along the mean-semivariance frontier:

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-1)>>> from pypfopt import EfficientSemivariance
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-2)>>> from pypfopt.expected_returns import returns_from_prices
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-4)>>> mu = capm_return(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-5)>>> returns = returns_from_prices(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-6)>>> returns = returns.dropna()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-7)>>> es = EfficientSemivariance(mu, returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-8)>>> es.efficient_return(0.01)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-9)>>> weights = es.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-10)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-11)OrderedDict([('ADAUSDT', 0.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-12) ('BNBUSDT', 0.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-13) ('BTCUSDT', 1.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-14) ('ETHUSDT', 0.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-15-15) ('XRPUSDT', 0.0)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-16-1)>>> vbt.pypfopt_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-16-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-16-3)... expected_returns="capm_return",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-16-4)... optimizer="efficient_semivariance", 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-16-5)... target="efficient_return",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-16-6)... target_return=0.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-16-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-16-8){'ADAUSDT': 0.0, 'BNBUSDT': 0.0, 'BTCUSDT': 1, 'ETHUSDT': 0.0, 'XRPUSDT': 0.0}
 
[/code]

 1. The second argument of `EfficientSemivariance` is `returns`, which is recognized as such by vectorbt and converted from prices automatically

Minimizing transaction costs:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-17-1)>>> initial_weights = np.array([1 / len(data.symbols)] * len(data.symbols))
 
[/code]

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-1)>>> from pypfopt.objective_functions import transaction_cost
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-3)>>> mu = mean_historical_return(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-4)>>> S = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-5)>>> ef = EfficientFrontier(mu, S)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-6)>>> ef.add_objective(transaction_cost, w_prev=initial_weights, k=0.001)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-7)>>> ef.add_objective(L2_reg, gamma=0.05)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-8)>>> ef.min_volatility()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-9)>>> weights = ef.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-10)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-11)OrderedDict([('ADAUSDT', 0.16025),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-12) ('BNBUSDT', 0.2),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-13) ('BTCUSDT', 0.27241),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-14) ('ETHUSDT', 0.2),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-18-15) ('XRPUSDT', 0.16734)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-1)>>> vbt.pypfopt_optimize( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-3)... objectives=["transaction_cost", "L2_reg"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-4)... w_prev=initial_weights, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-5)... k=0.001,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-6)... gamma=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-7)... target="min_volatility"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-9){'ADAUSDT': 0.16025,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-10) 'BNBUSDT': 0.2,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-11) 'BTCUSDT': 0.27241,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-12) 'ETHUSDT': 0.2,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-19-13) 'XRPUSDT': 0.16734}
 
[/code]

 1. `mean_historical_return`, `CovarianceShrinkage.ledoit_wolf`, and `EfficientFrontier` are used by default

Custom convex objective:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-20-1)>>> import cvxpy as cp
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-20-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-20-3)>>> def logarithmic_barrier_objective(w, cov_matrix, k=0.1):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-20-4)... log_sum = cp.sum(cp.log(w))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-20-5)... var = cp.quad_form(w, cov_matrix)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-20-6)... return var - k * log_sum
 
[/code]

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-1)>>> mu = mean_historical_return(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-2)>>> S = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-3)>>> ef = EfficientFrontier(mu, S, weight_bounds=(0.01, 0.3))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-4)>>> ef.convex_objective(logarithmic_barrier_objective, cov_matrix=S, k=0.001)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-5)>>> weights = ef.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-6)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-7)OrderedDict([('ADAUSDT', 0.12214),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-8) ('BNBUSDT', 0.22175),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-9) ('BTCUSDT', 0.3),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-10) ('ETHUSDT', 0.21855),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-21-11) ('XRPUSDT', 0.13756)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-1)>>> vbt.pypfopt_optimize( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-3)... weight_bounds=(0.01, 0.3),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-4)... k=0.001,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-5)... target=logarithmic_barrier_objective 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-7){'ADAUSDT': 0.12214,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-8) 'BNBUSDT': 0.22175,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-9) 'BTCUSDT': 0.3,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-10) 'ETHUSDT': 0.21855,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-22-11) 'XRPUSDT': 0.13756}
 
[/code]

 1. `mean_historical_return`, `CovarianceShrinkage.ledoit_wolf`, and `EfficientFrontier` are used by default
 2. The second argument of `logarithmic_barrier_objective` is `cov_matrix`, which is recognized as such by vectorbt and calculated automatically (or retrieved from cache)

Custom non-convex objective:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-23-1)>>> def deviation_risk_parity(w, cov_matrix):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-23-2)... cov_matrix = np.asarray(cov_matrix)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-23-3)... n = cov_matrix.shape[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-23-4)... rp = (w * (cov_matrix @ w)) / cp.quad_form(w, cov_matrix)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-23-5)... return cp.sum_squares(rp - 1 / n).value
 
[/code]

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-1)>>> mu = mean_historical_return(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-2)>>> S = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-3)>>> ef = EfficientFrontier(mu, S)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-4)>>> ef.nonconvex_objective(deviation_risk_parity, ef.cov_matrix)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-5)>>> weights = ef.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-6)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-7)OrderedDict([('ADAUSDT', 0.17421),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-8) ('BNBUSDT', 0.19933),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-9) ('BTCUSDT', 0.2515),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-10) ('ETHUSDT', 0.1981),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-24-11) ('XRPUSDT', 0.17686)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-1)>>> vbt.pypfopt_optimize( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-3)... target=deviation_risk_parity, 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-4)... target_is_convex=False
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-6){'ADAUSDT': 0.17421,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-7) 'BNBUSDT': 0.19933,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-8) 'BTCUSDT': 0.2515,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-9) 'ETHUSDT': 0.1981,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-25-10) 'XRPUSDT': 0.17686}
 
[/code]

 1. `mean_historical_return`, `CovarianceShrinkage.ledoit_wolf`, and `EfficientFrontier` are used by default
 2. The second argument of `deviation_risk_parity` is `cov_matrix`, which is recognized as such by vectorbt and calculated automatically (or retrieved from cache)

Black-Litterman Allocation ([read more](https://pyportfolioopt.readthedocs.io/en/latest/BlackLitterman.html)):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-1)>>> sp500_data = vbt.YFData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-2)... "^GSPC", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-3)... start=data.wrapper.index[0], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-4)... end=data.wrapper.index[-1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-6)>>> market_caps = data.get("Close") * data.get("Volume")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-7)>>> viewdict = {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-8)... "ADAUSDT": 0.20, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-9)... "BNBUSDT": -0.30, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-10)... "BTCUSDT": 0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-11)... "ETHUSDT": -0.2, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-12)... "XRPUSDT": 0.15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-26-13)... }
 
[/code]

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-1)>>> from pypfopt.black_litterman import (
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-2)... market_implied_risk_aversion,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-3)... market_implied_prior_returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-4)... BlackLittermanModel
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-7)>>> S = CovarianceShrinkage(data.get("Close")).ledoit_wolf()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-8)>>> delta = market_implied_risk_aversion(sp500_data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-9)>>> prior = market_implied_prior_returns(market_caps.iloc[-1], delta, S)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-10)>>> bl = BlackLittermanModel(S, pi=prior, absolute_views=viewdict)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-11)>>> rets = bl.bl_returns()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-12)>>> ef = EfficientFrontier(rets, S)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-13)>>> ef.min_volatility()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-14)>>> weights = ef.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-15)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-16)OrderedDict([('ADAUSDT', 0.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-17) ('BNBUSDT', 0.06743),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-18) ('BTCUSDT', 0.89462),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-19) ('ETHUSDT', 0.0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-27-20) ('XRPUSDT', 0.03795)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-1)>>> vbt.pypfopt_optimize( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-3)... expected_returns="bl_returns", 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-4)... market_prices=sp500_data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-5)... market_caps=market_caps.iloc[-1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-6)... absolute_views=viewdict,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-7)... target="min_volatility"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-9){'ADAUSDT': 0.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-10) 'BNBUSDT': 0.06743,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-11) 'BTCUSDT': 0.89462,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-12) 'ETHUSDT': 0.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-28-13) 'XRPUSDT': 0.03795}
 
[/code]

 1. `mean_historical_return` and `EfficientFrontier` are used by default
 2. `BlackLittermanModel`, `delta`, `prior`, and `bl_returns` are all resolved automatically

Hierarchical Risk Parity ([read more](https://pyportfolioopt.readthedocs.io/en/latest/OtherOptimizers.html#hierarchical-risk-parity-hrp)):

PyPortfolioOptVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-1)>>> from pypfopt import HRPOpt
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-3)>>> rets = returns_from_prices(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-4)>>> hrp = HRPOpt(rets)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-5)>>> hrp.optimize()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-6)>>> weights = hrp.clean_weights()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-7)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-8)OrderedDict([('ADAUSDT', 0.19415),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-9) ('BNBUSDT', 0.24834),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-10) ('BTCUSDT', 0.22827),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-11) ('ETHUSDT', 0.15217),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-29-12) ('XRPUSDT', 0.17707)])
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-1)>>> vbt.pypfopt_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-2)... prices=data.get("Close"), 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-3)... optimizer="hrp",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-4)... target="optimize"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-6){'ADAUSDT': 0.19415,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-7) 'BNBUSDT': 0.24834,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-8) 'BTCUSDT': 0.22827,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-9) 'ETHUSDT': 0.15217,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-30-10) 'XRPUSDT': 0.17707}
 
[/code]

 1. Returns are recognized as such by vectorbt and converted from prices automatically


# Argument groups[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#argument-groups "Permanent link")

In cases where two functions require an argument with the same name but you want to pass different values to them, pass the argument as an instance of [pfopt_func_dict](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.pfopt_func_dict) where keys should be functions or their names, and values should be different argument values:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-1)>>> vbt.pypfopt_optimize( 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-3)... expected_returns="bl_returns", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-4)... market_prices=sp500_data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-5)... market_caps=market_caps.iloc[-1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-6)... absolute_views=viewdict,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-7)... target="min_volatility",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-8)... cov_matrix=vbt.pfopt_func_dict({
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-9)... "EfficientFrontier": "sample_cov", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-10)... "_def": "ledoit_wolf" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-11)... })
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-13){'ADAUSDT': 0.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-14) 'BNBUSDT': 0.05013,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-15) 'BTCUSDT': 0.91912,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-16) 'ETHUSDT': 0.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-31-17) 'XRPUSDT': 0.03075}
 
[/code]

 1. 2. 


# Periodically[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#periodically "Permanent link")

So, why does vectorbt implement a special parser for PyPortfolioOpt instead of using the original, modularly-built API of the library? 

Having a single function that rules them all makes it much easier to use as an optimization function. For example, vectorbt uses sensible defaults for expected returns and other variables, and knows exactly where those variables should be used. In addition, being able to pass arbitrary keyword arguments and letting vectorbt distribute them over functions enables easier testing of multiple argument combinations using groups. 

Let's demonstrate this by using [PortfolioOptimizer.from_pypfopt](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_pypfopt), which uses [pypfopt_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.pypfopt_optimize) as `optimize_func`. Optimize for the maximum Sharpe in the previous week:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-32-1)>>> pfo = vbt.PortfolioOptimizer.from_pypfopt(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-32-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-32-3)... every="W"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-32-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-32-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-32-6)>>> pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/pypfopt.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/pypfopt.dark.svg#only-dark)

And here's how easy it's to test multiple combinations of the argument `target`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-1)>>> pfo = vbt.PortfolioOptimizer.from_pypfopt(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-2)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-3)... every="W",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-4)... target=vbt.Param([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-5)... "max_sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-6)... "min_volatility", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-7)... "max_quadratic_utility"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-8)... ])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-33-11)>>> pfo.plot(column="min_volatility").show() 
 
[/code]

 1. 

Group 3/3

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/pypfopt_groups.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/pypfopt_groups.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-34-1)>>> pf = pfo.simulate(data, freq="1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-34-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-34-3)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-34-4)target
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-34-5)max_sharpe 2.779042
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-34-6)min_volatility 1.862926
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-34-7)max_quadratic_utility 2.352667
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-34-8)Name: sharpe_ratio, dtype: float64
 
[/code]

We see that optimizing for the maximum Sharpe also yields the highest out-of-sample Sharpe. Great!


# Manually[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#manually "Permanent link")

We can also wrap the [pypfopt_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.pypfopt_optimize) function manually, for example, to do some data preprocessing or weight postprocessing:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-1)>>> def optimize_func(prices, index_slice, **kwargs):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-2)... period_prices = prices.iloc[index_slice]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-3)... return vbt.pypfopt_optimize(prices=period_prices, **kwargs)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-5)>>> pfo = vbt.PortfolioOptimizer.from_optimize_func(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-6)... data.symbol_wrapper,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-7)... optimize_func,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-8)... prices=data.get("Close"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-9)... index_slice=vbt.Rep("index_slice"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-10)... every="W"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-35-11)... )
 
[/code]


# Riskfolio-Lib[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#riskfolio-lib "Permanent link")

> [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib) is a library for making quantitative strategic asset allocation or portfolio optimization in Python made in Peru 🇵🇪. Its objective is to help students, academics and practitioners to build investment portfolios based on mathematically complex models with low effort. It is built on top of [cvxpy](https://www.cvxpy.org/) and closely integrated with [pandas](https://pandas.pydata.org/) data structures.

Similarly to PyPortfolioOpt, Riskfolio-Lib also implements a range of portfolio optimization tools. A common optimization procedure consists of the following steps:

 * Load price data and convert it into returns
 * Create and set up a new portfolio (usually with the suffix `Portfolio`)
 * Depending on the model selected, run one or more methods (usually with the suffix `stats`) that pre-calculate various statistics required by the optimization method
 * Run the optimization method (usually with the suffix `optimization`) to get the weights

For example, let's perform the mean-variance optimization (MVO) for maximum Sharpe:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-1)>>> import riskfolio as rp
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-3)>>> returns = data.get("Close").vbt.to_returns()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-4)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-5)>>> port = rp.Portfolio(returns=returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-6)>>> port.assets_stats(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-7)... method_mu="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-8)... method_cov="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-9)... d=0.94
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-11)>>> w = port.optimization(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-12)... model="Classic",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-13)... rm="MV",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-14)... obj="Sharpe",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-15)... rf=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-16)... l=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-17)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-19)>>> w.T
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-20) ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-36-21)weights 0.207779 1.043621e-08 0.336897 0.455323 3.650466e-09
 
[/code]

Hint

Why doesn't `assets_stats` return anything? Because it calculates `mu` and `cov` and overrides the portfolio attributes `port.mu` and `port.cov` in place.


# Parsing[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#parsing_1 "Permanent link")

Using the way above to produce a vector of weights from vectors of returns is great, but dividing the optimization procedure into a set of different function calls makes it harder to parameterize. What we need is just one function that can express an arbitrary Riskfolio-Lib setup, preferably defined using keyword arguments alone. To make one function out of many, we need to know the inputs of each function, the outputs, and how those functions play together. Thanks to the consistent naming of arguments and functions in Riskfolio-Lib (kudos to [@dcajasn](https://github.com/dcajasn "GitHub User: dcajasn")!), but also to the [entire collection of tutorials](https://riskfolio-lib.readthedocs.io/en/latest/examples.html), we can crystallize out the order of function calls depending on the optimization task.

For example, the optimization method [Portfolio.optimization](https://riskfolio-lib.readthedocs.io/en/latest/portfolio.html#Portfolio.Portfolio.optimization) with the model "Classic" would require the statistic method [Portfolio.assets_stats](https://riskfolio-lib.readthedocs.io/en/latest/portfolio.html#Portfolio.Portfolio.assets_stats) to be called first. The model "FM" would require the statistic methods [Portfolio.assets_stats](https://riskfolio-lib.readthedocs.io/en/latest/portfolio.html#Portfolio.Portfolio.assets_stats) and [Portfolio.factors_stats](https://riskfolio-lib.readthedocs.io/en/latest/portfolio.html#Portfolio.Portfolio.factors_stats) to be called. If the user also provided constraints, then we would additionally need to pre-process them by the respective [constraints function](https://riskfolio-lib.readthedocs.io/en/latest/constraints.html). 

Let's say we've established the call stack, how do we distribute arguments over the functions? We can read the signature of each function:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-37-1)>>> from vectorbtpro.utils.parsing import get_func_arg_names
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-37-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-37-3)>>> get_func_arg_names(port.assets_stats)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-37-4)['method_mu', 'method_cov', 'd']
 
[/code]

If the user passes an argument called `method_mu`, it should be passed to this function and to any other function listing this argument as it mostly like means the same thing. To resolve the arguments that need to be passed to the respective Riskfolio-Lib function, there is a convenient function [resolve_riskfolio_func_kwargs](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.resolve_riskfolio_func_kwargs):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-1)>>> from vectorbtpro.portfolio.pfopt.base import resolve_riskfolio_func_kwargs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-3)>>> resolve_riskfolio_func_kwargs(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-4)... port.assets_stats,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-5)... method_mu="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-6)... method_cov="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-7)... model="Classic"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-38-9){'method_mu': 'hist', 'method_cov': 'hist'}
 
[/code]

In a case where any of the arguments need to be overridden for one particular function only, we can provide `func_kwargs` dictionary with functions as keys and keyword arguments as values:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-1)>>> resolve_riskfolio_func_kwargs(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-2)... port.assets_stats,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-3)... method_mu="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-4)... method_cov="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-5)... model="Classic",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-6)... func_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-7)... assets_stats=dict(method_mu="ewma1"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-8)... optimization=dict(model="BL")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-39-11){'method_mu': 'ewma1', 'method_cov': 'hist'}
 
[/code]

This way, we can let vectorbt distribute the arguments, but still reserve the possibility of doing this manually using `func_kwargs`.


# Auto-optimization[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#auto-optimization_1 "Permanent link")

Knowing how to parse and resolve function arguments, vectorbt once again implements a function that can take a single set of keyword arguments and translate them into an optimization procedure - [riskfolio_optimize](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.riskfolio_optimize). This function is as easy to use as the one for PyPortfolioOpt!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-40-1)>>> vbt.riskfolio_optimize(returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-40-2){'ADAUSDT': 0.20777948652846492,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-40-3) 'BNBUSDT': 1.0435918170753283e-08,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-40-4) 'BTCUSDT': 0.33689720861500716,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-40-5) 'ETHUSDT': 0.45532329077024425,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-40-6) 'XRPUSDT': 3.6503655112892327e-09}
 
[/code]

Under the hood, it first resolves the portfolio class by reading the argument `port_cls`, and then creates a new portfolio instance by passing any keyword arguments that match the signature of its constructor method `__init__`. After this, it determines the optimization method by reading the argument `opt_method`, which is `"optimization"` by default. Knowing the optimization method and the model (provided via the argument `model`), it can figure out which statistic methods prior to the optimization should be executed and in what order. The names of those statistic methods are saved in `stats_methods`, unless they are already provided by the user. The next step is the resolution of any asset classes, constraints, and views, and translating them into keyword arguments that can be consumed by the methods that follow in the call stack. For instance, asset classes are pre-processed using the function [resolve_asset_classes](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.resolve_asset_classes), which allows the user to pass `asset_classes` using a range of convenient formats otherwise not supported by Riskfolio-Lib. Having all keyword arguments ready, the function executes the statistic methods (if any), and finally, the optimization method. It then returns the weights as a dictionary with the columns (i.e., asset names) from the returns array as keys.

Below, we will demonstrate various optimizations done both using Riskfolio-Lib and vectorbt. Ulcer Index Portfolio Optimization for Mean Risk ([notebook](https://nbviewer.org/github/dcajasn/Riskfolio-Lib/tree/master/examples/)):

Riskfolio-LibVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-1)>>> port = rp.Portfolio(returns=returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-2)>>> port.assets_stats(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-3)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-4)... method_cov="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-5)... d=0.94
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-7)>>> w = port.optimization(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-8)... model="Classic", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-9)... rm="UCI", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-10)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-11)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-12)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-13)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-15)>>> w.T
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-16) ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-41-17)weights 4.421983e-11 1.922731e-11 0.8343 0.1657 9.143250e-11
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-1)>>> vbt.riskfolio_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-2)... returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-3)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-4)... method_cov="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-5)... d=0.94,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-6)... model="Classic", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-7)... rm="UCI", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-8)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-9)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-10)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-11)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-13){'ADAUSDT': 4.4219828299615346e-11,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-14) 'BNBUSDT': 1.9227309961407513e-11,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-15) 'BTCUSDT': 0.8342998038068898,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-16) 'ETHUSDT': 0.16570019603823058,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-42-17) 'XRPUSDT': 9.143250192538338e-11}
 
[/code]

Worst Case Mean Variance Portfolio Optimization using box and elliptical uncertainty sets ([notebook](https://nbviewer.org/github/dcajasn/Riskfolio-Lib/tree/master/examples/)):

Riskfolio-LibVBTvectorbt (using func_kwargs)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-1)>>> port = rp.Portfolio(returns=returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-2)>>> port.assets_stats(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-3)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-4)... method_cov="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-5)... d=0.94
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-7)>>> port.wc_stats(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-8)... box="s", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-9)... ellip="s", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-10)... q=0.05, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-11)... n_sim=3000, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-12)... window=3, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-13)... dmu=0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-14)... dcov=0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-15)... seed=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-16)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-17)>>> w = port.wc_optimization(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-18)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-19)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-20)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-21)... Umu="box", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-22)... Ucov="box"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-23)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-24)>>> w.T
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-25) ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-43-26)weights 8.434620e-11 4.298850e-11 0.385894 0.614106 4.185089e-11
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-1)>>> vbt.riskfolio_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-2)... returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-3)... opt_method="wc", 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-4)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-5)... method_cov="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-6)... box="s", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-7)... ellip="s", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-8)... q=0.05, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-9)... n_sim=3000, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-10)... window=3, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-11)... dmu=0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-12)... dcov=0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-13)... seed=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-14)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-15)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-16)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-17)... Umu="box", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-18)... Ucov="box"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-19)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-20){'ADAUSDT': 8.434620227152581e-11,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-21) 'BNBUSDT': 4.2988498616065945e-11,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-22) 'BTCUSDT': 0.38589404919778153,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-23) 'ETHUSDT': 0.6141059506330329,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-44-24) 'XRPUSDT': 4.185089189555317e-11}
 
[/code]

 1. Use the worst-case optimization method

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-1)>>> vbt.riskfolio_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-2)... returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-3)... func_kwargs=dict( 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-4)... assets_stats=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-5)... opt_method="wc",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-6)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-7)... method_cov="hist"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-8)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-9)... wc_stats=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-10)... box="s", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-11)... ellip="s", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-12)... q=0.05, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-13)... n_sim=3000, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-14)... window=3, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-15)... dmu=0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-16)... dcov=0.1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-17)... seed=0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-18)... ),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-19)... wc_optimization=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-20)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-21)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-22)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-23)... Umu="box", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-24)... Ucov="box"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-26)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-27)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-28){'ADAUSDT': 8.434620227152581e-11,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-29) 'BNBUSDT': 4.2988498616065945e-11,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-30) 'BTCUSDT': 0.38589404919778153,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-31) 'ETHUSDT': 0.6141059506330329,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-45-32) 'XRPUSDT': 4.185089189555317e-11}
 
[/code]

 1. Functions listed as keys must come in the order as they should be called. Everything ending with `stats` will be interpreted as a statistic method (one or multiple). Everything ending with `optimization` will be interpreted as an optimization function (only one).

Mean Variance Portfolio with Short Weights ([notebook](https://nbviewer.org/github/dcajasn/Riskfolio-Lib/tree/master/examples/)):

Riskfolio-LibVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-1)>>> port = rp.Portfolio(returns=returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-2)>>> port.sht = True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-3)>>> port.uppersht = 0.3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-4)>>> port.upperlng = 1.3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-5)>>> port.budget = 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-6)>>> port.assets_stats(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-7)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-8)... method_cov="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-9)... d=0.94
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-11)>>> w = port.optimization(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-12)... model="Classic", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-13)... rm="MV", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-14)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-15)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-16)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-17)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-18)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-19)>>> w.T
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-20) ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-46-21)weights 0.295482 -2.109934e-07 0.456143 0.548375 -0.299999
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-1)>>> vbt.riskfolio_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-2)... returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-3)... sht=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-4)... uppersht=0.3,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-5)... upperlng=1.3,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-6)... budget=1.0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-7)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-8)... method_cov="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-9)... d=0.94,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-10)... rm="MV", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-11)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-12)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-13)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-14)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-16){'ADAUSDT': 0.2954820993653493,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-17) 'BNBUSDT': -2.1099344275128538e-07,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-18) 'BTCUSDT': 0.45614303697962627,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-19) 'ETHUSDT': 0.5483745379125106,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-47-20) 'XRPUSDT': -0.2999994632634474}
 
[/code]

Constraints on Assets ([notebook](https://nbviewer.org/github/dcajasn/Riskfolio-Lib/tree/master/examples/)):

Riskfolio-LibVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-1)>>> port = rp.Portfolio(returns=returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-2)>>> port.assets_stats(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-3)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-4)... method_cov="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-5)... d=0.94
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-7)>>> asset_classes = {"Assets": returns.columns.tolist()}
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-8)>>> asset_classes = pd.DataFrame(asset_classes)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-9)>>> constraints = { 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-10)... "Disabled": [False, False],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-11)... "Type": ["All Assets", "Assets"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-12)... "Set": ["", ""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-13)... "Position": ["", "BTCUSDT"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-14)... "Sign": [">=", "<="],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-15)... 'Weight': [0.1, 0.15],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-16)... "Type Relative": ["", ""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-17)... "Relative Set": ["", ""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-18)... "Relative": ["", ""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-19)... "Factor": ["", ""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-20)... }
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-21)>>> constraints = pd.DataFrame(constraints)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-22)>>> A, B = rp.assets_constraints(constraints, asset_classes)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-23)>>> port.ainequality = A
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-24)>>> port.binequality = B
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-25)>>> w = port.optimization(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-26)... model="Classic",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-27)... rm="MV",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-28)... obj="Sharpe",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-29)... rf=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-30)... l=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-31)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-32)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-33)>>> w.T
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-34) ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-48-35)weights 0.181443 0.1 0.15 0.468557 0.1
 
[/code]

 1. 

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-1)>>> vbt.riskfolio_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-2)... returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-3)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-4)... method_cov="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-5)... constraints=[{ 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-6)... "Type": "All Assets",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-7)... "Sign": ">=",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-8)... "Weight": 0.1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-9)... }, {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-10)... "Type": "Assets",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-11)... "Position": "BTCUSDT",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-12)... "Sign": "<=",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-13)... "Weight": 0.15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-14)... }],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-15)... d=0.94,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-16)... rm="MV", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-17)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-18)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-19)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-20)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-21)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-22){'ADAUSDT': 0.181442978888792,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-23) 'BNBUSDT': 0.10000000609450148,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-24) 'BTCUSDT': 0.1499998352568763,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-25) 'ETHUSDT': 0.4685571774444982,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-49-26) 'XRPUSDT': 0.10000000231533206}
 
[/code]

 1. No need to construct an entire DataFrame, vectorbt will do it for us! Also, no need to provide `asset_classes`, they will be taken from the columns.

Constraints on Asset Classes ([notebook](https://nbviewer.org/github/dcajasn/Riskfolio-Lib/tree/master/examples/)):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-50-1)>>> tags = [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-50-2)... "Smart contracts",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-50-3)... "Smart contracts",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-50-4)... "Payments",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-50-5)... "Smart contracts",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-50-6)... "Payments"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-50-7)... ]
 
[/code]

Riskfolio-LibVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-1)>>> port = rp.Portfolio(returns=returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-2)>>> port.assets_stats(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-3)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-4)... method_cov="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-5)... d=0.94
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-7)>>> asset_classes = {
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-8)... "Assets": returns.columns.tolist(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-9)... "Tags": tags
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-10)... }
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-11)>>> asset_classes = pd.DataFrame(asset_classes)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-12)>>> constraints = { 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-13)... "Disabled": [False],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-14)... "Type": ["Classes"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-15)... "Set": ["Tags"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-16)... "Position": ["Smart contracts"],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-17)... "Sign": [">="],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-18)... 'Weight': [0.8],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-19)... "Type Relative": [""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-20)... "Relative Set": [""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-21)... "Relative": [""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-22)... "Factor": [""],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-23)... }
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-24)>>> constraints = pd.DataFrame(constraints)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-25)>>> A, B = rp.assets_constraints(constraints, asset_classes)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-26)>>> port.ainequality = A
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-27)>>> port.binequality = B
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-28)>>> w = port.optimization(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-29)... model="Classic",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-30)... rm="MV",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-31)... obj="Sharpe",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-32)... rf=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-33)... l=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-34)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-35)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-36)>>> w.T
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-37) ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-51-38)weights 0.227839 5.856725e-10 0.2 0.572161 1.852774e-10
 
[/code]

 1. 

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-1)>>> vbt.riskfolio_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-2)... returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-3)... method_mu="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-4)... method_cov="hist", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-5)... asset_classes={"Tags": tags},
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-6)... constraints=[{
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-7)... "Type": "Classes",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-8)... "Set": "Tags",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-9)... "Position": "Smart contracts",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-10)... "Sign": ">=",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-11)... "Weight": 0.8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-12)... }],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-13)... d=0.94,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-14)... rm="MV", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-15)... obj="Sharpe", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-16)... rf=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-17)... l=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-18)... hist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-19)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-20){'ADAUSDT': 0.22783907021563807,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-21) 'BNBUSDT': 5.856745345006487e-10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-22) 'BTCUSDT': 0.19999999471503008,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-23) 'ETHUSDT': 0.5721609342983793,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-52-24) 'XRPUSDT': 1.852779892852209e-10}
 
[/code]

Nested Clustered Optimization (NCO) ([notebook](https://nbviewer.org/github/dcajasn/Riskfolio-Lib/tree/master/examples/)):

Riskfolio-LibVBT
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-1)>>> port = rp.HCPortfolio(returns=returns)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-2)>>> w = port.optimization(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-3)... model="NCO",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-4)... codependence="pearson",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-5)... covariance="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-6)... obj="MinRisk",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-7)... rm="MV",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-8)... rf=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-9)... l=2,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-10)... linkage="ward",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-11)... max_k=10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-12)... leaf_order=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-14)>>> w.T
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-15) ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-53-16)weights 6.402583e-09 0.05898 0.911545 3.331509e-09 0.029475
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-1)>>> vbt.riskfolio_optimize(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-2)... returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-3)... port_cls="HCPortfolio", 

 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-4)... model="NCO",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-5)... codependence="pearson",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-6)... covariance="hist",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-7)... obj="MinRisk",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-8)... rm="MV",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-9)... rf=0,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-10)... l=2,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-11)... linkage="ward",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-12)... max_k=10,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-13)... leaf_order=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-14)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-15){'ADAUSDT': 6.402581338827853e-09,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-16) 'BNBUSDT': 0.05897978986842499,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-17) 'BTCUSDT': 0.9115447868616637,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-18) 'ETHUSDT': 3.3315084935084894e-09,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-54-19) 'XRPUSDT': 0.029475413535821407}
 
[/code]

 1. Specify the name of the portfolio class

Note

If you're getting the message "The problem doesn't have a solution with actual input parameters" when using the "MOSEK" solver, make sure to install and activate [MOSEK](https://www.mosek.com/). Also, you can try out "ECOS".


# Periodically[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#periodically_1 "Permanent link")

As mentioned earlier, having one function that rules them all is not only easier to operate with, but its main purpose is to be parameterized and used in rebalancing with [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer). In particular, the optimization function above is used by the method [PortfolioOptimizer.from_riskfolio](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_riskfolio), which calls it periodically. Let's demonstrate its power by optimizing for the maximum Sharpe in the previous week:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-55-1)>>> pfo = vbt.PortfolioOptimizer.from_riskfolio(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-55-2)... returns=returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-55-3)... every="W"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-55-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-55-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-55-6)>>> pfo.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/riskfolio.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/riskfolio.dark.svg#only-dark)

What about parameters? We can wrap any (also nested) argument with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param) to test multiple parameter combinations. Let's test various maximum `BTCUSDT` weights to see if constraints are working properly:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-1)>>> pfo = vbt.PortfolioOptimizer.from_riskfolio(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-2)... returns=returns,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-3)... constraints=[{
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-4)... "Type": "Assets",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-5)... "Position": "BTCUSDT",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-6)... "Sign": "<=",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-7)... "Weight": vbt.Param([0.1, 0.2, 0.3], name="BTCUSDT_maxw") 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-8)... }],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-9)... every="W",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-10)... param_search_kwargs=dict(incl_types=list) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-56-11)... )
 
[/code]

 1. 2. 

Group 3/3
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-57-1)>>> pfo.allocations.groupby("BTCUSDT_maxw").max()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-57-2)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-57-3)BTCUSDT_maxw 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-57-4)0.1 1.0 1.0 0.1 1.0 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-57-5)0.2 1.0 1.0 0.2 1.0 1.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-57-6)0.3 1.0 1.0 0.3 1.0 1.0
 
[/code]

Works flawlessly ![👌](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f44c.svg)


# Universal portfolios[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#universal-portfolios "Permanent link")

Note

To install this package, first install vectorbtpro and then universal-portfolios, not them together. Since its dependency versions are quite strict, you may want to ignore its dependencies altogether by running `pip install -U universal-portfolios --no-deps`.

> The purpose of [Universal Portfolios](https://github.com/Marigold/universal-portfolios) is to put together different Online Portfolio Selection (OLPS) algorithms and provide unified tools for their analysis.

In contrast to PyPortfolioOpt, where weights are generated based on a specific range in time, the purpose of OLPS is to choose portfolio weights in every period to maximize its final wealth. That is, the generated weights have always the shape of the original array.

Let's take a look at the uniform allocation (UCRP):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-1)>>> from universal import tools, algos
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-3)>>> with vbt.WarningsFiltered(): 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-4)... algo = algos.CRP()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-5)... algo_result = algo.run(data.get("Close"))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-7)>>> algo_result.weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-8)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT CASH
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-9)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-10)2020-01-01 00:00:00+00:00 0.2 0.2 0.2 0.2 0.2 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-11)2020-01-01 01:00:00+00:00 0.2 0.2 0.2 0.2 0.2 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-12)2020-01-01 02:00:00+00:00 0.2 0.2 0.2 0.2 0.2 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-13)... ... ... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-14)2020-12-31 21:00:00+00:00 0.2 0.2 0.2 0.2 0.2 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-15)2020-12-31 22:00:00+00:00 0.2 0.2 0.2 0.2 0.2 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-16)2020-12-31 23:00:00+00:00 0.2 0.2 0.2 0.2 0.2 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-17)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-58-18)[8767 rows x 6 columns]
 
[/code]

 1. 

As we see, Universal Portfolios has generated and allocated weights at each single timestamp, which is pretty unrealistic because rebalancing that frequently is unsustainable in practice, unless the frequency of data is low. Additionally, iterating over this amount of data with this library is usually **quite slow**.

To account for this, we should downsample the pricing array to a longer time frame, and then upsample back to the original index. Let's try this out on the `DynamicCRP` algorithm by downsampling to the daily frequency first:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-1)>>> with vbt.WarningsFiltered():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-2)... algo = algos.DynamicCRP(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-3)... n=30, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-4)... min_history=7, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-5)... metric='sharpe', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-6)... alpha=0.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-8)... algo_result = algo.run(data.get("Close").resample("D").last())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-9)... down_weights = algo_result.weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-11)>>> down_weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-12)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-13)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-14)2020-01-01 00:00:00+00:00 2.000000e-01 2.000000e-01 0.200000 2.000000e-01 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-15)2020-01-02 00:00:00+00:00 2.000000e-01 2.000000e-01 0.200000 2.000000e-01 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-16)2020-01-03 00:00:00+00:00 2.000000e-01 2.000000e-01 0.200000 2.000000e-01 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-17)... ... ... ... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-18)2020-12-29 00:00:00+00:00 8.475716e-09 8.176270e-09 0.664594 8.274986e-09 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-19)2020-12-30 00:00:00+00:00 0.000000e+00 0.000000e+00 0.656068 0.000000e+00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-20)2020-12-31 00:00:00+00:00 0.000000e+00 0.000000e+00 0.655105 0.000000e+00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-21)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-22)symbol XRPUSDT 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-23)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-24)2020-01-01 00:00:00+00:00 2.000000e-01 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-25)2020-01-02 00:00:00+00:00 2.000000e-01 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-26)2020-01-03 00:00:00+00:00 2.000000e-01 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-27)... ... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-28)2020-12-29 00:00:00+00:00 9.004152e-09 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-29)2020-12-30 00:00:00+00:00 0.000000e+00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-30)2020-12-31 00:00:00+00:00 0.000000e+00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-31)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-59-32)[366 rows x 5 columns]
 
[/code]

Notice how the calculation still takes a considerable amount of time, even by reducing the total number of re-allocation timestamps by 24 times.

Let's bring the weights back to the original time frame:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-1)>>> weights = down_weights.vbt.realign(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-2)... data.wrapper.index,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-3)... freq="1h",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-4)... source_rbound=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-5)... target_rbound=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-6)... ffill=False 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-8)>>> weights
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-9)symbol ADAUSDT BNBUSDT BTCUSDT ETHUSDT XRPUSDT
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-10)Open time 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-11)2020-01-01 00:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-12)2020-01-01 01:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-13)2020-01-01 02:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-14)... ... ... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-15)2020-12-31 21:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-16)2020-12-31 22:00:00+00:00 NaN NaN NaN NaN NaN
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-17)2020-12-31 23:00:00+00:00 0.0 0.0 0.655105 0.0 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-60-19)[8766 rows x 5 columns]
 
[/code]

 1. 2. 

This array can now be used in simulation.

To simplify the workflow introduced above, vectorbt implements a class method [PortfolioOptimizer.from_universal_algo](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.from_universal_algo), which triggers the entire simulation with Universal Portfolios and, after done, picks the allocations at specific dates from the resulting DataFrame. By default, it picks the timestamps of non-NA, non-repeating weights. The method itself takes the algorithm (`algo`) and the pricing data (`S`). The former can take many value types: from the name or instance of the algorithm class (must be a subclass of `universal.algo.Algo`), to the actual result of the algorithm (of type `universal.result.AlgoResult`).

Let's run the same algorithm as above, but now using [PortfolioOptimizer](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer). We will also test multiple value combinations for `n`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-1)>>> with vbt.WarningsFiltered():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-2)... down_pfo = vbt.PortfolioOptimizer.from_universal_algo(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-3)... "DynamicCRP",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-4)... data.get("Close").resample("D").last(),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-5)... n=vbt.Param([7, 14, 30, 90]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-6)... min_history=7, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-7)... metric='sharpe', 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-8)... alpha=0.01
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-61-11)>>> down_pfo.plot(column=90).show()
 
[/code]

Group 4/4

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/universal.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/universal.dark.svg#only-dark)

We can then upsample the optimizer back to the original time frame by constructing an instance of [Resampler](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler) and passing it to [PortfolioOptimizer.resample](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/pfopt/base/#vectorbtpro.portfolio.pfopt.base.PortfolioOptimizer.resample):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-62-1)>>> resampler = vbt.Resampler(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-62-2)... down_pfo.wrapper.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-62-3)... data.wrapper.index, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-62-4)... target_freq="1h"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-62-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-62-6)>>> pfo = down_pfo.resample(resampler)
 
[/code]

Note

An allocation at the end of a daily bar will be placed at the end of the first hourly bar on that day, which may be undesired if the allocation uses any information from that daily bar. To account for this, calculate and use the right bounds of both indexes with [Resampler.get_rbound_index](https://vectorbt.pro/pvt_7a467f6b/api/base/resampling/base/#vectorbtpro.base.resampling.base.Resampler.get_rbound_index).

And finally, use the new optimizer in a simulation:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-1)>>> pf = pfo.simulate(data, freq="1h")
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-3)>>> pf.sharpe_ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-4)n
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-5)7 2.913174
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-6)14 3.456085
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-7)30 3.276883
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-8)90 2.176654
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-63-9)Name: sharpe_ratio, dtype: float64
 
[/code]


# Custom algorithm[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#custom-algorithm "Permanent link")

Let's create our own mean-reversion algorithm using Universal Portfolios. The idea is that badly performing stocks will revert to its mean and have higher returns than those above their mean.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-1)>>> from universal.algo import Algo
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-3)>>> class MeanReversion(Algo):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-4)... PRICE_TYPE = 'log'
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-5)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-6)... def __init__(self, n):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-7)... self.n = n
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-8)... super().__init__(min_history=n)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-9)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-10)... def init_weights(self, cols):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-11)... return pd.Series(np.zeros(len(cols)), cols)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-12)... 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-13)... def step(self, x, last_b, history):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-14)... ma = history.iloc[-self.n:].mean()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-15)... delta = x - ma
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-16)... w = np.maximum(-delta, 0.)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-17)... return w / sum(w)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-18)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-19)>>> with vbt.WarningsFiltered():
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-20)... pfo = vbt.PortfolioOptimizer.from_universal_algo(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-21)... MeanReversion,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-22)... data.get("Close").resample("D").last(), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-23)... n=30, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-24)... every="W" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-25)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-26)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/portfolio-optimization/integrations/#__codelineno-64-27)>>> pfo.plot().show()
 
[/code]

 1. 2. 3. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/universal_custom.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/pf-opt/universal_custom.dark.svg#only-dark)

Now it's your turn: create and implement a simple optimization strategy that would make sense in the real world - you'd be amazed how complex and interesting some strategies can become after starting with something really basic ![🙂](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f642.svg)

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/portfolio-optimization/integrations.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/PortfolioOptimization.ipynb)