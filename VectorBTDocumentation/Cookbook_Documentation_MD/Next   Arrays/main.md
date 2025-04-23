# Arrays[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#arrays "Permanent link")


# Displaying[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#displaying "Permanent link")

Any array, be it a NumPy array, Pandas object, or even a regular list, can be displayed as a table with [ptable](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.ptable), regardless of its size. When the function is called in a IPython environment such as Jupyter Lab, the table will become interactive.

Print out an array in various ways
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-0-1)vbt.ptable(df) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-0-2)vbt.ptable(df, ipython=False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-0-3)vbt.ptable(df, ipython=False, tabulate=False) 
 
[/code]

 1. 2. 3. 


# Wrapper[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#wrapper "Permanent link")

A wrapper can be extracted from any array-like object with [ArrayWrapper.from_obj](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.from_obj).

Extract the wrapper from various objects
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-1-1)wrapper = data.symbol_wrapper 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-1-2)wrapper = pf.wrapper 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-1-3)wrapper = df.vbt.wrapper 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-1-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-1-5)wrapper = vbt.ArrayWrapper.from_obj(sr) 
 
[/code]

 1. 2. 3. 4. 


* * *

+


* * *

An empty Pandas array can be created with [ArrayWrapper.fill](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.fill).

Create an empty array with the same shape, index, and columns as in another array
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-2-1)new_float_df = wrapper.fill(np.nan) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-2-2)new_bool_df = wrapper.fill(False) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-2-3)new_int_df = wrapper.fill(-1) 
 
[/code]

 1. 2. 3. 


* * *

+


* * *

A NumPy array can be wrapped with a Pandas Series or DataFrame with [ArrayWrapper.wrap](https://vectorbt.pro/pvt_7a467f6b/api/base/wrapping/#vectorbtpro.base.wrapping.ArrayWrapper.wrap).

Convert NumPy array to Pandas
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-3-1)df = wrapper.wrap(arr)
 
[/code]


# Product[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#product "Permanent link")

Product of multiple DataFrames can be achieved with the accessor method [BaseAccessor.x](https://vectorbt.pro/pvt_7a467f6b/api/base/accessors/#vectorbtpro.base.accessors.BaseAccessor.x). It can be called both as an instance and a class method.

Cross-join columns of multiple DataFrames
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-4-1)new_df1, new_df2 = df1.vbt.x(df2) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-4-2)new_df1, new_df2, new_df3 = df1.vbt.x(df2, df3) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/arrays/#__codelineno-4-3)new_dfs = vbt.pd_acc.x(*dfs) 
 
[/code]

 1. 2. 3.