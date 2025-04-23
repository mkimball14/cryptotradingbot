# Indexing[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#indexing "Permanent link")

Most VBT objects, such as data instances and portfolios, can be indexed like regular Pandas objects using the `[]`, `iloc`, `loc`, and `xs` selectors. The operation is passed down to all arrays inside the instance, and a new instance with the new arrays is created.

Select a date range of a Data instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-0-1)new_data = data.loc["2020-01-01":"2020-12-31"]
 
[/code]


* * *

+


* * *

In addition, there's a special selector `xloc` that accepts a smart indexing instruction. Such an instruction can contain one or more positions, labels, dates, times, ranges, frequencies, or even date offsets. It's parsed automatically and translated into an array with integer positions that are internally passed to the `iloc` selector.

Various smart row indexing operations on a Data instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-1)new_data = data.xloc[::2] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-2)new_data = data.xloc[np.array([10, 20, 30])] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-3)new_data = data.xloc["2020-01-01 17:30"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-4)new_data = data.xloc["2020-01-01"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-5)new_data = data.xloc["2020-01"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-6)new_data = data.xloc["2020"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-7)new_data = data.xloc["2020-01-01":"2021-01-01"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-8)new_data = data.xloc["january":"april"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-9)new_data = data.xloc["monday":"saturday"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-10)new_data = data.xloc["09:00":"16:00"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-11)new_data = data.xloc["16:00":"09:00"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-12)new_data = data.xloc["monday 09:00":"friday 16:00"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-13)new_data = data.xloc[
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-14) vbt.autoidx(slice("monday", "friday"), closed_end=True) & 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-15) vbt.autoidx(slice("09:00", "16:00"), closed_end=False)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-16)]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-17)new_data = data.xloc["Y"] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-18)new_data = data.xloc[pd.Timedelta(days=7)] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-19)new_data = data.xloc[df.index.weekday == 0] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-1-20)new_data = data.xloc[pd.tseries.offsets.BDay()] 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 17. 


* * *

+


* * *

Not only rows can be selected but also columns by combining [rowidx](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.RowIdxr) and [colidx](https://vectorbt.pro/pvt_7a467f6b/api/base/indexing/#vectorbtpro.base.indexing.ColIdxr) instructions.

Various smart row and/or column indexing operations on a DataFrame accessor
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-2-1)new_df = df.vbt.xloc[vbt.colidx(0)].get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-2-2)new_df = df.vbt.xloc[vbt.colidx("BTC-USD")].get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-2-3)new_df = df.vbt.xloc[vbt.colidx((10, "simple", "BTC-USD"))].get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-2-4)new_df = df.vbt.xloc[vbt.colidx("BTC-USD", level="symbol")].get() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-2-5)new_df = df.vbt.xloc["2020", "BTC-USD"].get() 
 
[/code]

 1. 2. 3. 4. 5. 

Info

Without the `get()` call the accessor will be returned. There's **no need** for this call when indexing other VBT objects, such as portfolios.


* * *

+


* * *

Pandas accessors can also be used to modify the values under some rows and columns. This isn't possible for more complex VBT objects.

Enter at the beginning of the business day, exit at the end
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-3-1)entries.vbt.xloc[vbt.autoidx(slice("mon", "sat")) & vbt.autoidx("09:00")] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-3-2)exits.vbt.xloc[vbt.autoidx(slice("mon", "sat")) & (vbt.autoidx("16:00") << 1)] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-3-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-3-4)entries.vbt.xloc[vbt.pointidx(every="B", at_time="09:00")] = True 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/indexing/#__codelineno-3-5)exits.vbt.xloc[vbt.pointidx(every="B", at_time="16:00", indexer_method="before")] = True
 
[/code]

 1. 2. 3.