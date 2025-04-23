# Discovery[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#discovery "Permanent link")

The arguments and optionally the description of any Python function or class can be displayed with [phelp](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.phelp). For example, we can quickly determine which inputs, outputs, and parameters does the indicator's `run()` function accept.

Print the specification of the TA-Lib's ATR
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-0-1)vbt.phelp(vbt.talib("atr").run)
 
[/code]

Note

This is not the same as calling the Python's `help` command - it only works on functions.


* * *

+


* * *

The attributes of any Python object can be listed with [pdir](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.pdir). This can become handy when trying to determine whether an object contains a specific attribute without having to search the API documentation.

Print the properties and methods of the Portfolio class
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-1-1)vbt.pdir(vbt.PF)
 
[/code]

Tip

We can even apply it on third-party objects such as packages!


* * *

+


* * *

Most VBT objects can be expanded and pretty-formatted to quickly unveil their contents with [pprint](https://vectorbt.pro/pvt_7a467f6b/api/utils/formatting/#vectorbtpro.utils.formatting.pprint). For example, it's a simple way to visually confirm whether the object has a correct shape and grouping.

Print the configuration of a Data instance
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-2-1)vbt.pprint(data)
 
[/code]


* * *

+


* * *

Most VBT objects can be connected to the API reference on the website and the source code on GitHub with [open_api_ref](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module.open_api_ref). The function takes an actual VBT object, its name, or its absolute path inside the package. It can also take third-party objects; in this case, it will search for them with [ DuckDuckGo](https://duckduckgo.com/) and open the first link.

How to open the online API reference
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-1)vbt.open_api_ref(vbt.nb) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-2)vbt.open_api_ref(vbt.nb.rolling_mean_nb) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-3)vbt.open_api_ref(vbt.PF) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-4)vbt.open_api_ref(vbt.Data.run) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-5)vbt.open_api_ref(vbt.Data.features) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-6)vbt.open_api_ref(vbt.ADX.adx_crossed_above) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-7)vbt.open_api_ref(vbt.settings) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-8)vbt.open_api_ref(pf.get_sharpe_ratio) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-9)vbt.open_api_ref((pf, "sharpe_ratio")) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-10)vbt.open_api_ref(pd.DataFrame) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-11)vbt.open_api_ref("vbt.PF") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-12)vbt.open_api_ref("SizeType") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-13)vbt.open_api_ref("DataFrame", module="pandas") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-3-14)vbt.open_api_ref("numpy.char.find", resolve=False) 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 

Tip

To get the link without opening it, use [get_api_ref](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module.get_api_ref), which takes the same arguments.


* * *

+


* * *

To open the first result to an arbitrary search query, use [imlucky](https://vectorbt.pro/pvt_7a467f6b/api/utils/module_/#vectorbtpro.utils.module.imlucky).

Ask a question if you feel lucky
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/discovery/#__codelineno-4-1)vbt.imlucky("How to create a structured NumPy array?") 
 
[/code]

 1.