# Plotting[¶](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#plotting "Permanent link")

Any Pandas Series or DataFrame can be plotted via an accessor. There are two main pathways for plotting: 

 1. [GenericAccessor](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor) offering methods tailored specifically for vectorbtpro-typical workflows, and 
 2. [PXAccessor](https://vectorbt.pro/pvt_7a467f6b/api/px/accessors/#vectorbtpro.px.accessors.PXAccessor) offering methods parsed from [Plotly express](https://plotly.com/python/plotly-express/).

How to plot a Pandas object
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-1)fig = sr_or_df.vbt.plot() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-3)fig = pd.Series(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-4) np.asarray(y), 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-5) index=np.asarray(x)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-6)).vbt.scatterplot() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-7)fig = pf.value.vbt.lineplot() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-8)fig = pf.sharpe_ratio.vbt.barplot() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-9)fig = pf.returns.vbt.qqplot() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-10)fig = pf.allocations.vbt.areaplot(line_shape="hv") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-11)fig = pf.returns.vbt.histplot(trace_kwargs=dict(nbinsx=100)) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-12)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-13)monthly_returns = pf.returns_acc.resample("M").get()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-14)fig = monthly_returns.vbt.boxplot() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-15)fig = monthly_returns.vbt.heatmap() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-16)fig = monthly_returns.vbt.ts_heatmap() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-17)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-18)fig = pf.sharpe_ratio.vbt.heatmap( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-19) x_level="fast_window", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-20) y_level="slow_window",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-21) symmetric=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-22))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-23)fig = pf.sharpe_ratio.vbt.heatmap( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-24) x_level="fast_window", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-25) y_level="slow_window",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-26) slider_level="symbol",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-27) symmetric=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-28))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-29)fig = pf.sharpe_ratio.vbt.volume( 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-30) x_level="timeperiod", 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-31) y_level="upper_threshold",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-32) z_level="lower_threshold",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-33) symmetric=True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-34))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-35)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-36)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-37)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-0-38)fig = sr_or_df.vbt.px.ecdf() 
 
[/code]

 1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 


* * *

+


* * *

To plot multiple things over the same figure, get the figure from the first plotting method and pass it to each subsequent one.

Plot equity lines of two portfolios in the same figure
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-1-1)fig = pf1.value.vbt.lineplot()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-1-2)fig = pf2.value.vbt.lineplot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-1-3)fig.show()
 
[/code]

The same works to plot multiple columns of a portfolio or other complex object. When plotting a graph with subplots, there's an option to overlay each column automatically.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-2-1)pf.plot(per_column=True).show() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-2-2)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-2-3)fig = pf["BTC-USD"].plot(show_legend=False, show_column_label=True)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-2-4)fig = pf["ETH-USD"].plot(show_legend=False, show_column_label=True, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-2-5)fig.show() 
 
[/code]

 1. 2. 


* * *

+


* * *

The default theme can be changed globally in the settings. Available themes are registered under `themes` in [settings.plotting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.plotting).

Set the dark theme
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-3-1)vbt.settings.set_theme("dark")
 
[/code]


* * *

+


* * *

Trace parameters such as line color and marker shape can be changed with `trace_kwargs`. Some plotting methods have multiple of such arguments. For allowed parameters, see the Plotly documentation of the respective trace type, for example [Scatter](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scatter.html) for lines.

Change the color of the upper and lower line of a Bollinger Bands indicator
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-4-1)fig = bbands.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-4-2) upper_trace_kwargs=dict(line=dict(color="green")),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-4-3) lower_trace_kwargs=dict(line=dict(color="red"))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-4-4))
 
[/code]


* * *

+


* * *

Layout parameters can be changed by passing them directly to the plot method as variable keyword arguments.

Make the width and height of the plot variable rather than fixed
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-5-1)fig = df.vbt.plot(width=None, height=None)
 
[/code]


* * *

+


* * *

A plot with multiple subplots can be constructed with `vbt.make_subplots()`, which takes [the same arguments](https://plotly.com/python-api-reference/generated/plotly.subplots.make_subplots.html) as Plotly.

Create two subplots - one per row
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-6-1)fig = vbt.make_subplots(rows=2, cols=1)
 
[/code]


* * *

+


* * *

Most plotting methods accept the argument `add_trace_kwargs` (see [Figure.add_trace](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.add_trace)), which can be used to specify which subplot to plot the traces over.

Plot the first and second DataFrame over the first and second subplot respectively
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-7-1)df1.vbt.plot(add_trace_kwargs=dict(row=1, col=1), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-7-2)df2.vbt.plot(add_trace_kwargs=dict(row=2, col=1), fig=fig)
 
[/code]

Note

The provided figure `fig` must be created with `vbt.make_subplots()`.


* * *

+


* * *

Traces with two different scales but similar time scale can also be plotted next to each other by creating a secondary y-axis.

Plot the first and second DataFrame on the first and second y-axis respectively
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-8-1)fig = vbt.make_subplots(specs=[[{"secondary_y": True}]])
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-8-2)df1.vbt.plot(add_trace_kwargs=dict(secondary_y=False), fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-8-3)df2.vbt.plot(add_trace_kwargs=dict(secondary_y=True), fig=fig)
 
[/code]


* * *

+


* * *

The figure can be changed manually after creation. Below, `0` is the index of the trace in the figure.

Retrospectively change the title and the markers of the scatter plot
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-9-1)fig = df.vbt.scatterplot()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-9-2)fig.layout.title.text = "Scatter"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-9-3)fig.data[0].marker.line.width = 4
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-9-4)fig.data[0].marker.line.color = "black"
 
[/code]

Note

A plotting method can add multiple traces to the figure.


* * *

+


* * *

Settings related to plotting can be defined or changed globally in [settings.plotting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.plotting).

Change the background of any figure to black
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-10-1)vbt.settings["plotting"]["layout"]["paper_bgcolor"] = "rgb(0,0,0)"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-10-2)vbt.settings["plotting"]["layout"]["plot_bgcolor"] = "rgb(0,0,0)"
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-10-3)vbt.settings["plotting"]["layout"]["template"] = "vbt_dark"
 
[/code]

Same by registering an own theme
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-11-1)import plotly.io as pio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-11-2)import plotly.graph_objects as go
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-11-3)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-11-4)pio.templates["my_black"] = go.layout.Template(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-11-5) layout_paper_bgcolor="rgb(0,0,0)",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-11-6) layout_plot_bgcolor="rgb(0,0,0)",
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-11-7))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-11-8)vbt.settings["plotting"]["layout"]["template"] = "vbt_dark+my_black"
 
[/code]


* * *

+


* * *

Usually Plotly displays a homogeneous datetime index including time gaps such as non-business hours and weekends. To skip the gaps, we can use the `rangebreaks` property.

Skip non-business hours and weekends
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-12-1)fig = df.vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-12-2)fig.update_xaxes(
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-12-3) rangebreaks=[
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-12-4) dict(bounds=['sat', 'mon']),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-12-5) dict(bounds=[16, 9.5], pattern='hour'),
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-12-6) 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-12-7) ]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-12-8))
 
[/code]

 1. 

Note

Make sure that your data has the correct timezone to apply the above approach.

Skip all gaps automatically
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-1)fig = df.vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-2)fig.auto_rangebreaks() 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-3)fig.auto_rangebreaks(freq="D") 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-4)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-5)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-6)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-7)vbt.settings.plotting.auto_rangebreaks = True
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-8)vbt.settings.plotting.auto_rangebreaks = dict(freq="D")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-9)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-10)# ______________________________________________________________
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-11)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-12)def pre_show_func(fig):
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-13) fig.auto_rangebreaks(freq="D")
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-14)
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-15)vbt.settings.plotting.pre_show_func = pre_show_func 
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-16)fig = df.vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-13-17)fig.show() 
 
[/code]

 1. 2. 3. Skip NaN rows, or provide any other index to skip
 4. 5. 

Note

The above approach works only on figures produced by VBT methods.


* * *

+


* * *

To display a figure on an interactive HTML page, see [Interactive HTML Export](https://plotly.com/python/interactive-html-export/).

Save the figure to an HTML file
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-14-1)fig.write_html("fig.html")
 
[/code]

Save multiple figures to the same HTML file
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-15-1)with open("fig.html", "a") as f:
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-15-2) f.write(fig1.to_html(full_html=False))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-15-3) f.write(fig2.to_html(full_html=False))
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-15-4) f.write(fig3.to_html(full_html=False))
 
[/code]


* * *

+


* * *

To display a figure in a separate browser tab, see [Renderers](https://plotly.com/python/renderers/).

Make browser the default renderer
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-16-1)import plotly.io as pio
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-16-2)pio.renderers.default = "browser"
 
[/code]


* * *

+


* * *

If a figure takes too much time to display, maybe the amount of data is the problem? If this is the case, [plotly-resampler](https://github.com/predict-idlab/plotly-resampler) may come to the rescue to resample any (primarily scatter) data on the fly.

Enable plotly-resampler globally
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-17-1)vbt.settings.plotting.use_resampler = True
 
[/code]

Another approach is by selecting a date range of particular interest.

Display one year of data
[code]
 [](https://vectorbt.pro/pvt_7a467f6b/cookbook/plotting/#__codelineno-18-1)fig = fig.select_range(start="2023", end="2024")
 
[/code]