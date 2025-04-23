figure

#  figure module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure "Permanent link")

Utilities for constructing and displaying figures.

* * *

## get_domain function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L62-L69 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.get_domain "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-0-1)get_domain(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-0-2)    ref,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-0-3)    fig
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-0-4))
    

Get domain of a coordinate axis.

* * *

## make_figure function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L385-L419 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_figure "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-1-1)make_figure(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-1-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-1-3)    use_widgets=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-1-4)    use_resampler=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-1-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-1-6))
    

Make a new Plotly figure.

If `use_widgets` is True, returns [FigureWidget](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureWidget "vectorbtpro.utils.figure.FigureWidget"), otherwise [Figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.Figure "vectorbtpro.utils.figure.Figure").

If `use_resampler` is True, additionally wraps the class using `plotly_resampler`.

Defaults are defined under [plotting](https://vectorbt.pro/pvt_7a467f6b/api/_settings/#vectorbtpro._settings.plotting "vectorbtpro._settings.plotting").

* * *

## make_subplots function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L422-L429 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_subplots "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-2-1)make_subplots(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-2-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-2-3)    use_widgets=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-2-4)    use_resampler=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-2-5)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-2-6))
    

Make Plotly subplots using [make_figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.make_figure "vectorbtpro.utils.figure.make_figure").

* * *

## resolve_axis_refs function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L39-L59 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.resolve_axis_refs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-3-1)resolve_axis_refs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-3-2)    add_trace_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-3-3)    xref=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-3-4)    yref=None
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-3-5))
    

Get x-axis and y-axis references.

* * *

## Figure class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L291-L310 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.Figure "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-4-1)Figure(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-4-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-4-3)    empty_layout=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-4-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-4-5))
    

Figure.

Extends `plotly.graph_objects.Figure`.

Create a new :class:Figure instance

## Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#parameters "Permanent link")

data The 'data' property is a tuple of trace instances __ that may be specified as__

  * A list or tuple of trace instances (e.g. [Scatter(...), Bar(...)])
  * A single trace instance (e.g. Scatter(...), Bar(...), etc.)
  * A list or tuple of dicts of string/value properties where:
  * The 'type' property specifies the trace type One of: ['bar', 'barpolar', 'box', 'candlestick', 'carpet', 'choropleth', 'choroplethmap', 'choroplethmapbox', 'cone', 'contour', 'contourcarpet', 'densitymap', 'densitymapbox', 'funnel', 'funnelarea', 'heatmap', 'heatmapgl', 'histogram', 'histogram2d', 'histogram2dcontour', 'icicle', 'image', 'indicator', 'isosurface', 'mesh3d', 'ohlc', 'parcats', 'parcoords', 'pie', 'pointcloud', 'sankey', 'scatter', 'scatter3d', 'scattercarpet', 'scattergeo', 'scattergl', 'scattermap', 'scattermapbox', 'scatterpolar', 'scatterpolargl', 'scattersmith', 'scatterternary', 'splom', 'streamtube', 'sunburst', 'surface', 'table', 'treemap', 'violin', 'volume', 'waterfall']

  * All remaining properties are passed to the constructor of the specified trace type




(e.g. [{'type': 'scatter', ...}, {'type': 'bar, ...}])

layout The 'layout' property is an instance of Layout __ that may be specified as__

  * An instance of :class:`plotly.graph_objs.Layout`
  * A dict of string/value properties that will be passed to the Layout constructor



Supported dict properties:
    
    
      activeselection
          :class:`plotly.graph_objects.layout.Activeselec
          tion` instance or dict with compatible
          properties
      activeshape
          :class:`plotly.graph_objects.layout.Activeshape
          ` instance or dict with compatible properties
      annotations
          A tuple of
          :class:`plotly.graph_objects.layout.Annotation`
          instances or dicts with compatible properties
      annotationdefaults
          When used in a template (as
          layout.template.layout.annotationdefaults),
          sets the default property values to use for
          elements of layout.annotations
      autosize
          Determines whether or not a layout width or
          height that has been left undefined by the user
          is initialized on each relayout. Note that,
          regardless of this attribute, an undefined
          layout width or height is always initialized on
          the first call to plot.
      autotypenumbers
          Using "strict" a numeric string in trace data
          is not converted to a number. Using *convert
          types* a numeric string in trace data may be
          treated as a number during automatic axis
          `type` detection. This is the default value;
          however it could be overridden for individual
          axes.
      barcornerradius
          Sets the rounding of bar corners. May be an
          integer number of pixels, or a percentage of
          bar width (as a string ending in %).
      bargap
          Sets the gap (in plot fraction) between bars of
          adjacent location coordinates.
      bargroupgap
          Sets the gap (in plot fraction) between bars of
          the same location coordinate.
      barmode
          Determines how bars at the same location
          coordinate are displayed on the graph. With
          "stack", the bars are stacked on top of one
          another With "relative", the bars are stacked
          on top of one another, with negative values
          below the axis, positive values above With
          "group", the bars are plotted next to one
          another centered around the shared location.
          With "overlay", the bars are plotted over one
          another, you might need to reduce "opacity" to
          see multiple bars.
      barnorm
          Sets the normalization for bar traces on the
          graph. With "fraction", the value of each bar
          is divided by the sum of all values at that
          location coordinate. "percent" is the same but
          multiplied by 100 to show percentages.
      boxgap
          Sets the gap (in plot fraction) between boxes
          of adjacent location coordinates. Has no effect
          on traces that have "width" set.
      boxgroupgap
          Sets the gap (in plot fraction) between boxes
          of the same location coordinate. Has no effect
          on traces that have "width" set.
      boxmode
          Determines how boxes at the same location
          coordinate are displayed on the graph. If
          "group", the boxes are plotted next to one
          another centered around the shared location. If
          "overlay", the boxes are plotted over one
          another, you might need to set "opacity" to see
          them multiple boxes. Has no effect on traces
          that have "width" set.
      calendar
          Sets the default calendar system to use for
          interpreting and displaying dates throughout
          the plot.
      clickmode
          Determines the mode of single click
          interactions. "event" is the default value and
          emits the `plotly_click` event. In addition
          this mode emits the `plotly_selected` event in
          drag modes "lasso" and "select", but with no
          event data attached (kept for compatibility
          reasons). The "select" flag enables selecting
          single data points via click. This mode also
          supports persistent selections, meaning that
          pressing Shift while clicking, adds to /
          subtracts from an existing selection. "select"
          with `hovermode`: "x" can be confusing,
          consider explicitly setting `hovermode`:
          "closest" when using this feature. Selection
          events are sent accordingly as long as "event"
          flag is set as well. When the "event" flag is
          missing, `plotly_click` and `plotly_selected`
          events are not fired.
      coloraxis
          :class:`plotly.graph_objects.layout.Coloraxis`
          instance or dict with compatible properties
      colorscale
          :class:`plotly.graph_objects.layout.Colorscale`
          instance or dict with compatible properties
      colorway
          Sets the default trace colors.
      computed
          Placeholder for exporting automargin-impacting
          values namely `margin.t`, `margin.b`,
          `margin.l` and `margin.r` in "full-json" mode.
      datarevision
          If provided, a changed value tells
          `Plotly.react` that one or more data arrays has
          changed. This way you can modify arrays in-
          place rather than making a complete new copy
          for an incremental change. If NOT provided,
          `Plotly.react` assumes that data arrays are
          being treated as immutable, thus any data array
          with a different identity from its predecessor
          contains new data.
      dragmode
          Determines the mode of drag interactions.
          "select" and "lasso" apply only to scatter
          traces with markers or text. "orbit" and
          "turntable" apply only to 3D scenes.
      editrevision
          Controls persistence of user-driven changes in
          `editable: true` configuration, other than
          trace names and axis titles. Defaults to
          `layout.uirevision`.
      extendfunnelareacolors
          If `true`, the funnelarea slice colors (whether
          given by `funnelareacolorway` or inherited from
          `colorway`) will be extended to three times its
          original length by first repeating every color
          20% lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      extendiciclecolors
          If `true`, the icicle slice colors (whether
          given by `iciclecolorway` or inherited from
          `colorway`) will be extended to three times its
          original length by first repeating every color
          20% lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      extendpiecolors
          If `true`, the pie slice colors (whether given
          by `piecolorway` or inherited from `colorway`)
          will be extended to three times its original
          length by first repeating every color 20%
          lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      extendsunburstcolors
          If `true`, the sunburst slice colors (whether
          given by `sunburstcolorway` or inherited from
          `colorway`) will be extended to three times its
          original length by first repeating every color
          20% lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      extendtreemapcolors
          If `true`, the treemap slice colors (whether
          given by `treemapcolorway` or inherited from
          `colorway`) will be extended to three times its
          original length by first repeating every color
          20% lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      font
          Sets the global font. Note that fonts used in
          traces and other layout components inherit from
          the global font.
      funnelareacolorway
          Sets the default funnelarea slice colors.
          Defaults to the main `colorway` used for trace
          colors. If you specify a new list here it can
          still be extended with lighter and darker
          colors, see `extendfunnelareacolors`.
      funnelgap
          Sets the gap (in plot fraction) between bars of
          adjacent location coordinates.
      funnelgroupgap
          Sets the gap (in plot fraction) between bars of
          the same location coordinate.
      funnelmode
          Determines how bars at the same location
          coordinate are displayed on the graph. With
          "stack", the bars are stacked on top of one
          another With "group", the bars are plotted next
          to one another centered around the shared
          location. With "overlay", the bars are plotted
          over one another, you might need to reduce
          "opacity" to see multiple bars.
      geo
          :class:`plotly.graph_objects.layout.Geo`
          instance or dict with compatible properties
      grid
          :class:`plotly.graph_objects.layout.Grid`
          instance or dict with compatible properties
      height
          Sets the plot's height (in px).
      hiddenlabels
          hiddenlabels is the funnelarea & pie chart
          analog of visible:'legendonly' but it can
          contain many labels, and can simultaneously
          hide slices from several pies/funnelarea charts
      hiddenlabelssrc
          Sets the source reference on Chart Studio Cloud
          for `hiddenlabels`.
      hidesources
          Determines whether or not a text link citing
          the data source is placed at the bottom-right
          cored of the figure. Has only an effect only on
          graphs that have been generated via forked
          graphs from the Chart Studio Cloud (at
          <https://chart-studio.plotly.com> or on-premise).
      hoverdistance
          Sets the default distance (in pixels) to look
          for data to add hover labels (-1 means no
          cutoff, 0 means no looking for data). This is
          only a real distance for hovering on point-like
          objects, like scatter points. For area-like
          objects (bars, scatter fills, etc) hovering is
          on inside the area and off outside, but these
          objects will not supersede hover on point-like
          objects in case of conflict.
      hoverlabel
          :class:`plotly.graph_objects.layout.Hoverlabel`
          instance or dict with compatible properties
      hovermode
          Determines the mode of hover interactions. If
          "closest", a single hoverlabel will appear for
          the "closest" point within the `hoverdistance`.
          If "x" (or "y"), multiple hoverlabels will
          appear for multiple points at the "closest" x-
          (or y-) coordinate within the `hoverdistance`,
          with the caveat that no more than one
          hoverlabel will appear per trace. If *x
          unified* (or *y unified*), a single hoverlabel
          will appear multiple points at the closest x-
          (or y-) coordinate within the `hoverdistance`
          with the caveat that no more than one
          hoverlabel will appear per trace. In this mode,
          spikelines are enabled by default perpendicular
          to the specified axis. If false, hover
          interactions are disabled.
      hoversubplots
          Determines expansion of hover effects to other
          subplots If "single" just the axis pair of the
          primary point is included without overlaying
          subplots. If "overlaying" all subplots using
          the main axis and occupying the same space are
          included. If "axis", also include stacked
          subplots using the same axis when `hovermode`
          is set to "x", *x unified*, "y" or *y unified*.
      iciclecolorway
          Sets the default icicle slice colors. Defaults
          to the main `colorway` used for trace colors.
          If you specify a new list here it can still be
          extended with lighter and darker colors, see
          `extendiciclecolors`.
      images
          A tuple of
          :class:`plotly.graph_objects.layout.Image`
          instances or dicts with compatible properties
      imagedefaults
          When used in a template (as
          layout.template.layout.imagedefaults), sets the
          default property values to use for elements of
          layout.images
      legend
          :class:`plotly.graph_objects.layout.Legend`
          instance or dict with compatible properties
      map
          :class:`plotly.graph_objects.layout.Map`
          instance or dict with compatible properties
      mapbox
          :class:`plotly.graph_objects.layout.Mapbox`
          instance or dict with compatible properties
      margin
          :class:`plotly.graph_objects.layout.Margin`
          instance or dict with compatible properties
      meta
          Assigns extra meta information that can be used
          in various `text` attributes. Attributes such
          as the graph, axis and colorbar `title.text`,
          annotation `text` `trace.name` in legend items,
          `rangeselector`, `updatemenus` and `sliders`
          `label` text all support `meta`. One can access
          `meta` fields using template strings:
          `%{meta[i]}` where `i` is the index of the
          `meta` item in question. `meta` can also be an
          object for example `{key: value}` which can be
          accessed %{meta[key]}.
      metasrc
          Sets the source reference on Chart Studio Cloud
          for `meta`.
      minreducedheight
          Minimum height of the plot with
          margin.automargin applied (in px)
      minreducedwidth
          Minimum width of the plot with
          margin.automargin applied (in px)
      modebar
          :class:`plotly.graph_objects.layout.Modebar`
          instance or dict with compatible properties
      newselection
          :class:`plotly.graph_objects.layout.Newselectio
          n` instance or dict with compatible properties
      newshape
          :class:`plotly.graph_objects.layout.Newshape`
          instance or dict with compatible properties
      paper_bgcolor
          Sets the background color of the paper where
          the graph is drawn.
      piecolorway
          Sets the default pie slice colors. Defaults to
          the main `colorway` used for trace colors. If
          you specify a new list here it can still be
          extended with lighter and darker colors, see
          `extendpiecolors`.
      plot_bgcolor
          Sets the background color of the plotting area
          in-between x and y axes.
      polar
          :class:`plotly.graph_objects.layout.Polar`
          instance or dict with compatible properties
      scattergap
          Sets the gap (in plot fraction) between scatter
          points of adjacent location coordinates.
          Defaults to `bargap`.
      scattermode
          Determines how scatter points at the same
          location coordinate are displayed on the graph.
          With "group", the scatter points are plotted
          next to one another centered around the shared
          location. With "overlay", the scatter points
          are plotted over one another, you might need to
          reduce "opacity" to see multiple scatter
          points.
      scene
          :class:`plotly.graph_objects.layout.Scene`
          instance or dict with compatible properties
      selectdirection
          When `dragmode` is set to "select", this limits
          the selection of the drag to horizontal,
          vertical or diagonal. "h" only allows
          horizontal selection, "v" only vertical, "d"
          only diagonal and "any" sets no limit.
      selectionrevision
          Controls persistence of user-driven changes in
          selected points from all traces.
      selections
          A tuple of
          :class:`plotly.graph_objects.layout.Selection`
          instances or dicts with compatible properties
      selectiondefaults
          When used in a template (as
          layout.template.layout.selectiondefaults), sets
          the default property values to use for elements
          of layout.selections
      separators
          Sets the decimal and thousand separators. For
          example, *. * puts a '.' before decimals and a
          space between thousands. In English locales,
          dflt is ".," but other locales may alter this
          default.
      shapes
          A tuple of
          :class:`plotly.graph_objects.layout.Shape`
          instances or dicts with compatible properties
      shapedefaults
          When used in a template (as
          layout.template.layout.shapedefaults), sets the
          default property values to use for elements of
          layout.shapes
      showlegend
          Determines whether or not a legend is drawn.
          Default is `true` if there is a trace to show
          and any of these: a) Two or more traces would
          by default be shown in the legend. b) One pie
          trace is shown in the legend. c) One trace is
          explicitly given with `showlegend: true`.
      sliders
          A tuple of
          :class:`plotly.graph_objects.layout.Slider`
          instances or dicts with compatible properties
      sliderdefaults
          When used in a template (as
          layout.template.layout.sliderdefaults), sets
          the default property values to use for elements
          of layout.sliders
      smith
          :class:`plotly.graph_objects.layout.Smith`
          instance or dict with compatible properties
      spikedistance
          Sets the default distance (in pixels) to look
          for data to draw spikelines to (-1 means no
          cutoff, 0 means no looking for data). As with
          hoverdistance, distance does not apply to area-
          like objects. In addition, some objects can be
          hovered on but will not generate spikelines,
          such as scatter fills.
      sunburstcolorway
          Sets the default sunburst slice colors.
          Defaults to the main `colorway` used for trace
          colors. If you specify a new list here it can
          still be extended with lighter and darker
          colors, see `extendsunburstcolors`.
      template
          Default attributes to be applied to the plot.
          This should be a dict with format: `{'layout':
          layoutTemplate, 'data': {trace_type:
          [traceTemplate, ...], ...}}` where
          `layoutTemplate` is a dict matching the
          structure of `figure.layout` and
          `traceTemplate` is a dict matching the
          structure of the trace with type `trace_type`
          (e.g. 'scatter'). Alternatively, this may be
          specified as an instance of
          plotly.graph_objs.layout.Template.  Trace
          templates are applied cyclically to traces of
          each type. Container arrays (eg `annotations`)
          have special handling: An object ending in
          `defaults` (eg `annotationdefaults`) is applied
          to each array item. But if an item has a
          `templateitemname` key we look in the template
          array for an item with matching `name` and
          apply that instead. If no matching `name` is
          found we mark the item invisible. Any named
          template item not referenced is appended to the
          end of the array, so this can be used to add a
          watermark annotation or a logo image, for
          example. To omit one of these items on the
          plot, make an item with matching
          `templateitemname` and `visible: false`.
      ternary
          :class:`plotly.graph_objects.layout.Ternary`
          instance or dict with compatible properties
      title
          :class:`plotly.graph_objects.layout.Title`
          instance or dict with compatible properties
      titlefont
          Deprecated: Please use layout.title.font
          instead. Sets the title font. Note that the
          title's font used to be customized by the now
          deprecated `titlefont` attribute.
      transition
          Sets transition options used during
          Plotly.react updates.
      treemapcolorway
          Sets the default treemap slice colors. Defaults
          to the main `colorway` used for trace colors.
          If you specify a new list here it can still be
          extended with lighter and darker colors, see
          `extendtreemapcolors`.
      uirevision
          Used to allow user interactions with the plot
          to persist after `Plotly.react` calls that are
          unaware of these interactions. If `uirevision`
          is omitted, or if it is given and it changed
          from the previous `Plotly.react` call, the
          exact new figure is used. If `uirevision` is
          truthy and did NOT change, any attribute that
          has been affected by user interactions and did
          not receive a different value in the new figure
          will keep the interaction value.
          `layout.uirevision` attribute serves as the
          default for `uirevision` attributes in various
          sub-containers. For finer control you can set
          these sub-attributes directly. For example, if
          your app separately controls the data on the x
          and y axes you might set
          `xaxis.uirevision=*time*` and
          `yaxis.uirevision=*cost*`. Then if only the y
          data is changed, you can update
          `yaxis.uirevision=*quantity*` and the y axis
          range will reset but the x axis range will
          retain any user-driven zoom.
      uniformtext
          :class:`plotly.graph_objects.layout.Uniformtext
          ` instance or dict with compatible properties
      updatemenus
          A tuple of
          :class:`plotly.graph_objects.layout.Updatemenu`
          instances or dicts with compatible properties
      updatemenudefaults
          When used in a template (as
          layout.template.layout.updatemenudefaults),
          sets the default property values to use for
          elements of layout.updatemenus
      violingap
          Sets the gap (in plot fraction) between violins
          of adjacent location coordinates. Has no effect
          on traces that have "width" set.
      violingroupgap
          Sets the gap (in plot fraction) between violins
          of the same location coordinate. Has no effect
          on traces that have "width" set.
      violinmode
          Determines how violins at the same location
          coordinate are displayed on the graph. If
          "group", the violins are plotted next to one
          another centered around the shared location. If
          "overlay", the violins are plotted over one
          another, you might need to set "opacity" to see
          them multiple violins. Has no effect on traces
          that have "width" set.
      waterfallgap
          Sets the gap (in plot fraction) between bars of
          adjacent location coordinates.
      waterfallgroupgap
          Sets the gap (in plot fraction) between bars of
          the same location coordinate.
      waterfallmode
          Determines how bars at the same location
          coordinate are displayed on the graph. With
          "group", the bars are plotted next to one
          another centered around the shared location.
          With "overlay", the bars are plotted over one
          another, you might need to reduce "opacity" to
          see multiple bars.
      width
          Sets the plot's width (in px).
      xaxis
          :class:`plotly.graph_objects.layout.XAxis`
          instance or dict with compatible properties
      yaxis
          :class:`plotly.graph_objects.layout.YAxis`
          instance or dict with compatible properties
    

frames The 'frames' property is a tuple of instances of __ Frame that may be specified as__

  * A list or tuple of instances of plotly.graph_objs.Frame
  * A list or tuple of dicts of string/value properties that will be passed to the Frame constructor



Supported dict properties:
    
    
      baseframe
          The name of the frame into which this frame's
          properties are merged before applying. This is
          used to unify properties and avoid needing to
          specify the same values for the same properties
          in multiple frames.
      data
          A list of traces this frame modifies. The
          format is identical to the normal trace
          definition.
      group
          An identifier that specifies the group to which
          the frame belongs, used by animate to select a
          subset of frames.
      layout
          Layout properties which this frame modifies.
          The format is identical to the normal layout
          definition.
      name
          A label by which to identify the frame
      traces
          A list of trace indices that identify the
          respective traces in the data attribute
    

skip_invalid: bool If True, invalid properties in the figure specification will be skipped silently. If False (default) invalid properties in the figure specification will result in a ValueError

## Raises[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#raises "Permanent link")

ValueError if a property in the specification of data, layout, or frames is invalid AND skip_invalid is False

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [FigureMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin "vectorbtpro.utils.figure.FigureMixin")
  * `plotly.basedatatypes.BaseFigure`
  * `plotly.graph_objs._figure.Figure`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.figure.FigureMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.figure.FigureMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.figure.FigureMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.figure.FigureMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.figure.FigureMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.figure.FigureMixin.find_messages")
  * [FigureMixin.auto_rangebreaks](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks "vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks")
  * [FigureMixin.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.copy "vectorbtpro.utils.figure.FigureMixin.copy")
  * [FigureMixin.resolve_show_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.resolve_show_args "vectorbtpro.utils.figure.FigureMixin.resolve_show_args")
  * [FigureMixin.save_svg_for_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs "vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs")
  * [FigureMixin.select_range](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.select_range "vectorbtpro.utils.figure.FigureMixin.select_range")
  * [FigureMixin.show_png](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_png "vectorbtpro.utils.figure.FigureMixin.show_png")
  * [FigureMixin.show_svg](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_svg "vectorbtpro.utils.figure.FigureMixin.show_svg")
  * [FigureMixin.skip_index](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.skip_index "vectorbtpro.utils.figure.FigureMixin.skip_index")



* * *

### show method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L308-L310 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.Figure.show "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-5-1)Figure.show(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-5-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-5-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-5-4))
    

Show a figure using either the default renderer(s) or the renderer(s) specified by the renderer argument

## Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#parameters_1 "Permanent link")

renderer: str or None (default None) A string containing the names of one or more registered renderers (separated by '+' characters) or None. If None, then the default renderers specified in plotly.io.renderers.default are used.

validate: bool (default True) True if the figure should be validated before being shown, False otherwise.

width: int or float An integer or float that determines the number of pixels wide the plot is. The default is set in plotly.js.

height: int or float An integer or float that determines the number of pixels wide the plot is. The default is set in plotly.js.

config: dict A dict of parameters to configure the figure. The defaults are set in plotly.js.

## Returns[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#returns "Permanent link")

None

* * *

## FigureMixin class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L75-L288 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-6-1)FigureMixin()
    

Mixin class for figures.

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

  * [Figure](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.Figure "vectorbtpro.utils.figure.Figure")
  * [FigureResampler](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureResampler "vectorbtpro.utils.figure.FigureResampler")
  * [FigureWidget](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureWidget "vectorbtpro.utils.figure.FigureWidget")
  * [FigureWidgetResampler](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureWidgetResampler "vectorbtpro.utils.figure.FigureWidgetResampler")



* * *

### auto_rangebreaks method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L188-L212 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-7-1)FigureMixin.auto_rangebreaks(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-7-2)    index=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-7-3)    inplace=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-7-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-7-5))
    

Set range breaks automatically based on [get_rangebreaks](https://vectorbt.pro/pvt_7a467f6b/api/utils/datetime_/#vectorbtpro.utils.datetime_.get_rangebreaks "vectorbtpro.utils.datetime_.get_rangebreaks").

* * *

### copy method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L78-L80 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.copy "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-8-1)FigureMixin.copy(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-8-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-8-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-8-4))
    

Create a copy of the figure.

* * *

### resolve_show_args method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L222-L250 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.resolve_show_args "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-9-1)FigureMixin.resolve_show_args(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-9-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-9-3)    auto_rangebreaks=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-9-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-9-5))
    

Display the figure.

* * *

### save_svg_for_docs method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L264-L288 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-10-1)FigureMixin.save_svg_for_docs(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-10-2)    figure_name,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-10-3)    dir_path=PosixPath('svg'),
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-10-4)    mkdir_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-10-5)    show=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-10-6)    show_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-10-7)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-10-8))
    

Save the figure in both light and dark SVG format for documentation.

* * *

### select_range method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L82-L186 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.select_range "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-11-1)FigureMixin.select_range(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-11-2)    start=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-11-3)    end=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-11-4)    inplace=False
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-11-5))
    

Select a range.

Start and end index can be integers but also datetime-like objects.

* * *

### show method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L252-L254 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-12-1)FigureMixin.show(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-12-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-12-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-12-4))
    

Display the figure.

* * *

### show_png method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L256-L258 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_png "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-13-1)FigureMixin.show_png(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-13-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-13-3))
    

Display the figure in PNG format.

* * *

### show_svg method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L260-L262 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_svg "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-14-1)FigureMixin.show_svg(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-14-2)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-14-3))
    

Display the figure in SVG format.

* * *

### skip_index method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L214-L220 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.skip_index "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-15-1)FigureMixin.skip_index(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-15-2)    skip_index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-15-3)    inplace=True
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-15-4))
    

Skip index values.

* * *

## FigureResampler class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L338-L357 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureResampler "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-16-1)FigureResampler(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-16-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-16-3)    empty_layout=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-16-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-16-5))
    

Figure resampler.

Extends `plotly.graph_objects.Figure`.

Initialize a dynamic aggregation data mirror using a dash web app.

## Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#parameters_2 "Permanent link")

figure: BaseFigure The figure that will be decorated. Can be either an empty figure (e.g., `go.Figure()`, `make_subplots()`, `go.FigureWidget`) or an existing figure. convert_existing_traces: bool A bool indicating whether the high-frequency traces of the passed `figure` should be resampled, by default True. Hence, when set to False, the high-frequency traces of the passed `figure` will not be resampled. default_n_shown_samples: int, optional The default number of samples that will be shown for each trace, by default 1000.
    
    
    !!! note
        - This can be overridden within the [`add_trace`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_trace] method.
        - If a trace withholds fewer datapoints than this parameter,
          the data will *not* be aggregated.
    

default_downsampler: AbstractAggregator, optional An instance which implements the AbstractAggregator interface and will be used as default downsampler, by default `MinMaxLTTB` with `MinMaxLTTB` is a heuristic to the LTTB algorithm that uses pre-selection of min-max values (default 4 per bin) to speed up LTTB (as now only 4 values per bin are considered by LTTB). This min-max ratio of 4 can be changed by initializing `MinMaxLTTB` with a different value for the `minmax_ratio` parameter. 
    
    
    !!! note
        This can be overridden within the [`add_trace`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_trace] method.
    

default_gap_handler: AbstractGapHandler, optional An instance which implements the AbstractGapHandler interface and will be used as default gap handler, by default `MedDiffGapHandler`. `MedDiffGapHandler` will determine gaps by first calculating the median aggregated x difference and then thresholding the aggregated x delta on a multiple of this median difference. 
    
    
    !!! note
        This can be overridden within the [`add_trace`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_trace] method.
    

resampled_trace_prefix_suffix: str, optional A tuple which contains the `prefix` and `suffix`, respectively, which will be added to the trace its legend-name when a resampled version of the trace is shown. By default a bold, orange `[R]` is shown as prefix (no suffix is shown). show_mean_aggregation_size: bool, optional Whether the mean aggregation bin size will be added as a suffix to the trace its legend-name, by default True. convert_traces_kwargs: dict, optional A dict of kwargs that will be passed to the [`add_trace`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_trace] method and will be used to convert the existing traces. 
    
    
    !!! note
        This argument is only used when the passed ``figure`` contains data and
        ``convert_existing_traces`` is set to True.
    

create_overview: bool, optional Whether an overview will be added to the figure (also known as rangeslider), by default False. An overview is a bidirectionally linked figure that is placed below the FigureResampler figure and shows a coarse version on which the current view of the FigureResampler figure is highlighted. The overview can be used to quickly navigate through the data by dragging the selection box. !!! note - In the case of subplots, the overview will be created for each subplot column. Only a single subplot row can be captured in the overview, this is by default the first row. If you want to customize this behavior, you can use the `overview_row_idxs` argument. - This functionality is not yet extensively validated. Please report any issues you encounter on GitHub. overview_row_idxs: list, optional A list of integers corresponding to the row indices (START AT 0) of the subplots columns that should be linked with the column its corresponding overview. By default None, which will result in the first row being utilized for each column. overview_kwargs: dict, optional A dict of kwargs that will be passed to the `update_layout` method of the overview figure, by default {}, which will result in utilizing the [`default`][_DEFAULT_OVERVIEW_LAYOUT_KWARGS] overview layout kwargs. verbose: bool, optional Whether some verbose messages will be printed or not, by default False. show_dash_kwargs: dict, optional A dict that will be used as default kwargs for the [`show_dash`][figure_resampler.figure_resampler.FigureResampler.show_dash] method. !!! note The passed kwargs to the [`show_dash`][figure_resampler.figure_resampler.FigureResampler.show_dash] method will take precedence over these defaults.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [FigureMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin "vectorbtpro.utils.figure.FigureMixin")
  * `abc.ABC`
  * `plotly.basedatatypes.BaseFigure`
  * `plotly.graph_objs._figure.Figure`
  * `plotly_resampler.figure_resampler.figure_resampler.FigureResampler`
  * `plotly_resampler.figure_resampler.figure_resampler_interface.AbstractFigureAggregator`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.figure.FigureMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.figure.FigureMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.figure.FigureMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.figure.FigureMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.figure.FigureMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.figure.FigureMixin.find_messages")
  * [FigureMixin.auto_rangebreaks](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks "vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks")
  * [FigureMixin.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.copy "vectorbtpro.utils.figure.FigureMixin.copy")
  * [FigureMixin.resolve_show_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.resolve_show_args "vectorbtpro.utils.figure.FigureMixin.resolve_show_args")
  * [FigureMixin.save_svg_for_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs "vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs")
  * [FigureMixin.select_range](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.select_range "vectorbtpro.utils.figure.FigureMixin.select_range")
  * [FigureMixin.show_png](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_png "vectorbtpro.utils.figure.FigureMixin.show_png")
  * [FigureMixin.show_svg](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_svg "vectorbtpro.utils.figure.FigureMixin.show_svg")
  * [FigureMixin.skip_index](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.skip_index "vectorbtpro.utils.figure.FigureMixin.skip_index")



* * *

### show method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L355-L357 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureResampler.show "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-17-1)FigureResampler.show(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-17-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-17-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-17-4))
    

Show a figure using either the default renderer(s) or the renderer(s) specified by the renderer argument

## Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#parameters_3 "Permanent link")

renderer: str or None (default None) A string containing the names of one or more registered renderers (separated by '+' characters) or None. If None, then the default renderers specified in plotly.io.renderers.default are used.

validate: bool (default True) True if the figure should be validated before being shown, False otherwise.

width: int or float An integer or float that determines the number of pixels wide the plot is. The default is set in plotly.js.

height: int or float An integer or float that determines the number of pixels wide the plot is. The default is set in plotly.js.

config: dict A dict of parameters to configure the figure. The defaults are set in plotly.js.

## Returns[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#returns_1 "Permanent link")

None

* * *

## FigureWidget class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L313-L332 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureWidget "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-18-1)FigureWidget(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-18-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-18-3)    empty_layout=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-18-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-18-5))
    

Figure widget.

Extends `plotly.graph_objects.FigureWidget`.

Create a new :class:FigureWidget instance

## Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#parameters_4 "Permanent link")

data The 'data' property is a tuple of trace instances __ that may be specified as__

  * A list or tuple of trace instances (e.g. [Scatter(...), Bar(...)])
  * A single trace instance (e.g. Scatter(...), Bar(...), etc.)
  * A list or tuple of dicts of string/value properties where:
  * The 'type' property specifies the trace type One of: ['bar', 'barpolar', 'box', 'candlestick', 'carpet', 'choropleth', 'choroplethmap', 'choroplethmapbox', 'cone', 'contour', 'contourcarpet', 'densitymap', 'densitymapbox', 'funnel', 'funnelarea', 'heatmap', 'heatmapgl', 'histogram', 'histogram2d', 'histogram2dcontour', 'icicle', 'image', 'indicator', 'isosurface', 'mesh3d', 'ohlc', 'parcats', 'parcoords', 'pie', 'pointcloud', 'sankey', 'scatter', 'scatter3d', 'scattercarpet', 'scattergeo', 'scattergl', 'scattermap', 'scattermapbox', 'scatterpolar', 'scatterpolargl', 'scattersmith', 'scatterternary', 'splom', 'streamtube', 'sunburst', 'surface', 'table', 'treemap', 'violin', 'volume', 'waterfall']

  * All remaining properties are passed to the constructor of the specified trace type




(e.g. [{'type': 'scatter', ...}, {'type': 'bar, ...}])

layout The 'layout' property is an instance of Layout __ that may be specified as__

  * An instance of :class:`plotly.graph_objs.Layout`
  * A dict of string/value properties that will be passed to the Layout constructor



Supported dict properties:
    
    
      activeselection
          :class:`plotly.graph_objects.layout.Activeselec
          tion` instance or dict with compatible
          properties
      activeshape
          :class:`plotly.graph_objects.layout.Activeshape
          ` instance or dict with compatible properties
      annotations
          A tuple of
          :class:`plotly.graph_objects.layout.Annotation`
          instances or dicts with compatible properties
      annotationdefaults
          When used in a template (as
          layout.template.layout.annotationdefaults),
          sets the default property values to use for
          elements of layout.annotations
      autosize
          Determines whether or not a layout width or
          height that has been left undefined by the user
          is initialized on each relayout. Note that,
          regardless of this attribute, an undefined
          layout width or height is always initialized on
          the first call to plot.
      autotypenumbers
          Using "strict" a numeric string in trace data
          is not converted to a number. Using *convert
          types* a numeric string in trace data may be
          treated as a number during automatic axis
          `type` detection. This is the default value;
          however it could be overridden for individual
          axes.
      barcornerradius
          Sets the rounding of bar corners. May be an
          integer number of pixels, or a percentage of
          bar width (as a string ending in %).
      bargap
          Sets the gap (in plot fraction) between bars of
          adjacent location coordinates.
      bargroupgap
          Sets the gap (in plot fraction) between bars of
          the same location coordinate.
      barmode
          Determines how bars at the same location
          coordinate are displayed on the graph. With
          "stack", the bars are stacked on top of one
          another With "relative", the bars are stacked
          on top of one another, with negative values
          below the axis, positive values above With
          "group", the bars are plotted next to one
          another centered around the shared location.
          With "overlay", the bars are plotted over one
          another, you might need to reduce "opacity" to
          see multiple bars.
      barnorm
          Sets the normalization for bar traces on the
          graph. With "fraction", the value of each bar
          is divided by the sum of all values at that
          location coordinate. "percent" is the same but
          multiplied by 100 to show percentages.
      boxgap
          Sets the gap (in plot fraction) between boxes
          of adjacent location coordinates. Has no effect
          on traces that have "width" set.
      boxgroupgap
          Sets the gap (in plot fraction) between boxes
          of the same location coordinate. Has no effect
          on traces that have "width" set.
      boxmode
          Determines how boxes at the same location
          coordinate are displayed on the graph. If
          "group", the boxes are plotted next to one
          another centered around the shared location. If
          "overlay", the boxes are plotted over one
          another, you might need to set "opacity" to see
          them multiple boxes. Has no effect on traces
          that have "width" set.
      calendar
          Sets the default calendar system to use for
          interpreting and displaying dates throughout
          the plot.
      clickmode
          Determines the mode of single click
          interactions. "event" is the default value and
          emits the `plotly_click` event. In addition
          this mode emits the `plotly_selected` event in
          drag modes "lasso" and "select", but with no
          event data attached (kept for compatibility
          reasons). The "select" flag enables selecting
          single data points via click. This mode also
          supports persistent selections, meaning that
          pressing Shift while clicking, adds to /
          subtracts from an existing selection. "select"
          with `hovermode`: "x" can be confusing,
          consider explicitly setting `hovermode`:
          "closest" when using this feature. Selection
          events are sent accordingly as long as "event"
          flag is set as well. When the "event" flag is
          missing, `plotly_click` and `plotly_selected`
          events are not fired.
      coloraxis
          :class:`plotly.graph_objects.layout.Coloraxis`
          instance or dict with compatible properties
      colorscale
          :class:`plotly.graph_objects.layout.Colorscale`
          instance or dict with compatible properties
      colorway
          Sets the default trace colors.
      computed
          Placeholder for exporting automargin-impacting
          values namely `margin.t`, `margin.b`,
          `margin.l` and `margin.r` in "full-json" mode.
      datarevision
          If provided, a changed value tells
          `Plotly.react` that one or more data arrays has
          changed. This way you can modify arrays in-
          place rather than making a complete new copy
          for an incremental change. If NOT provided,
          `Plotly.react` assumes that data arrays are
          being treated as immutable, thus any data array
          with a different identity from its predecessor
          contains new data.
      dragmode
          Determines the mode of drag interactions.
          "select" and "lasso" apply only to scatter
          traces with markers or text. "orbit" and
          "turntable" apply only to 3D scenes.
      editrevision
          Controls persistence of user-driven changes in
          `editable: true` configuration, other than
          trace names and axis titles. Defaults to
          `layout.uirevision`.
      extendfunnelareacolors
          If `true`, the funnelarea slice colors (whether
          given by `funnelareacolorway` or inherited from
          `colorway`) will be extended to three times its
          original length by first repeating every color
          20% lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      extendiciclecolors
          If `true`, the icicle slice colors (whether
          given by `iciclecolorway` or inherited from
          `colorway`) will be extended to three times its
          original length by first repeating every color
          20% lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      extendpiecolors
          If `true`, the pie slice colors (whether given
          by `piecolorway` or inherited from `colorway`)
          will be extended to three times its original
          length by first repeating every color 20%
          lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      extendsunburstcolors
          If `true`, the sunburst slice colors (whether
          given by `sunburstcolorway` or inherited from
          `colorway`) will be extended to three times its
          original length by first repeating every color
          20% lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      extendtreemapcolors
          If `true`, the treemap slice colors (whether
          given by `treemapcolorway` or inherited from
          `colorway`) will be extended to three times its
          original length by first repeating every color
          20% lighter then each color 20% darker. This is
          intended to reduce the likelihood of reusing
          the same color when you have many slices, but
          you can set `false` to disable. Colors provided
          in the trace, using `marker.colors`, are never
          extended.
      font
          Sets the global font. Note that fonts used in
          traces and other layout components inherit from
          the global font.
      funnelareacolorway
          Sets the default funnelarea slice colors.
          Defaults to the main `colorway` used for trace
          colors. If you specify a new list here it can
          still be extended with lighter and darker
          colors, see `extendfunnelareacolors`.
      funnelgap
          Sets the gap (in plot fraction) between bars of
          adjacent location coordinates.
      funnelgroupgap
          Sets the gap (in plot fraction) between bars of
          the same location coordinate.
      funnelmode
          Determines how bars at the same location
          coordinate are displayed on the graph. With
          "stack", the bars are stacked on top of one
          another With "group", the bars are plotted next
          to one another centered around the shared
          location. With "overlay", the bars are plotted
          over one another, you might need to reduce
          "opacity" to see multiple bars.
      geo
          :class:`plotly.graph_objects.layout.Geo`
          instance or dict with compatible properties
      grid
          :class:`plotly.graph_objects.layout.Grid`
          instance or dict with compatible properties
      height
          Sets the plot's height (in px).
      hiddenlabels
          hiddenlabels is the funnelarea & pie chart
          analog of visible:'legendonly' but it can
          contain many labels, and can simultaneously
          hide slices from several pies/funnelarea charts
      hiddenlabelssrc
          Sets the source reference on Chart Studio Cloud
          for `hiddenlabels`.
      hidesources
          Determines whether or not a text link citing
          the data source is placed at the bottom-right
          cored of the figure. Has only an effect only on
          graphs that have been generated via forked
          graphs from the Chart Studio Cloud (at
          <https://chart-studio.plotly.com> or on-premise).
      hoverdistance
          Sets the default distance (in pixels) to look
          for data to add hover labels (-1 means no
          cutoff, 0 means no looking for data). This is
          only a real distance for hovering on point-like
          objects, like scatter points. For area-like
          objects (bars, scatter fills, etc) hovering is
          on inside the area and off outside, but these
          objects will not supersede hover on point-like
          objects in case of conflict.
      hoverlabel
          :class:`plotly.graph_objects.layout.Hoverlabel`
          instance or dict with compatible properties
      hovermode
          Determines the mode of hover interactions. If
          "closest", a single hoverlabel will appear for
          the "closest" point within the `hoverdistance`.
          If "x" (or "y"), multiple hoverlabels will
          appear for multiple points at the "closest" x-
          (or y-) coordinate within the `hoverdistance`,
          with the caveat that no more than one
          hoverlabel will appear per trace. If *x
          unified* (or *y unified*), a single hoverlabel
          will appear multiple points at the closest x-
          (or y-) coordinate within the `hoverdistance`
          with the caveat that no more than one
          hoverlabel will appear per trace. In this mode,
          spikelines are enabled by default perpendicular
          to the specified axis. If false, hover
          interactions are disabled.
      hoversubplots
          Determines expansion of hover effects to other
          subplots If "single" just the axis pair of the
          primary point is included without overlaying
          subplots. If "overlaying" all subplots using
          the main axis and occupying the same space are
          included. If "axis", also include stacked
          subplots using the same axis when `hovermode`
          is set to "x", *x unified*, "y" or *y unified*.
      iciclecolorway
          Sets the default icicle slice colors. Defaults
          to the main `colorway` used for trace colors.
          If you specify a new list here it can still be
          extended with lighter and darker colors, see
          `extendiciclecolors`.
      images
          A tuple of
          :class:`plotly.graph_objects.layout.Image`
          instances or dicts with compatible properties
      imagedefaults
          When used in a template (as
          layout.template.layout.imagedefaults), sets the
          default property values to use for elements of
          layout.images
      legend
          :class:`plotly.graph_objects.layout.Legend`
          instance or dict with compatible properties
      map
          :class:`plotly.graph_objects.layout.Map`
          instance or dict with compatible properties
      mapbox
          :class:`plotly.graph_objects.layout.Mapbox`
          instance or dict with compatible properties
      margin
          :class:`plotly.graph_objects.layout.Margin`
          instance or dict with compatible properties
      meta
          Assigns extra meta information that can be used
          in various `text` attributes. Attributes such
          as the graph, axis and colorbar `title.text`,
          annotation `text` `trace.name` in legend items,
          `rangeselector`, `updatemenus` and `sliders`
          `label` text all support `meta`. One can access
          `meta` fields using template strings:
          `%{meta[i]}` where `i` is the index of the
          `meta` item in question. `meta` can also be an
          object for example `{key: value}` which can be
          accessed %{meta[key]}.
      metasrc
          Sets the source reference on Chart Studio Cloud
          for `meta`.
      minreducedheight
          Minimum height of the plot with
          margin.automargin applied (in px)
      minreducedwidth
          Minimum width of the plot with
          margin.automargin applied (in px)
      modebar
          :class:`plotly.graph_objects.layout.Modebar`
          instance or dict with compatible properties
      newselection
          :class:`plotly.graph_objects.layout.Newselectio
          n` instance or dict with compatible properties
      newshape
          :class:`plotly.graph_objects.layout.Newshape`
          instance or dict with compatible properties
      paper_bgcolor
          Sets the background color of the paper where
          the graph is drawn.
      piecolorway
          Sets the default pie slice colors. Defaults to
          the main `colorway` used for trace colors. If
          you specify a new list here it can still be
          extended with lighter and darker colors, see
          `extendpiecolors`.
      plot_bgcolor
          Sets the background color of the plotting area
          in-between x and y axes.
      polar
          :class:`plotly.graph_objects.layout.Polar`
          instance or dict with compatible properties
      scattergap
          Sets the gap (in plot fraction) between scatter
          points of adjacent location coordinates.
          Defaults to `bargap`.
      scattermode
          Determines how scatter points at the same
          location coordinate are displayed on the graph.
          With "group", the scatter points are plotted
          next to one another centered around the shared
          location. With "overlay", the scatter points
          are plotted over one another, you might need to
          reduce "opacity" to see multiple scatter
          points.
      scene
          :class:`plotly.graph_objects.layout.Scene`
          instance or dict with compatible properties
      selectdirection
          When `dragmode` is set to "select", this limits
          the selection of the drag to horizontal,
          vertical or diagonal. "h" only allows
          horizontal selection, "v" only vertical, "d"
          only diagonal and "any" sets no limit.
      selectionrevision
          Controls persistence of user-driven changes in
          selected points from all traces.
      selections
          A tuple of
          :class:`plotly.graph_objects.layout.Selection`
          instances or dicts with compatible properties
      selectiondefaults
          When used in a template (as
          layout.template.layout.selectiondefaults), sets
          the default property values to use for elements
          of layout.selections
      separators
          Sets the decimal and thousand separators. For
          example, *. * puts a '.' before decimals and a
          space between thousands. In English locales,
          dflt is ".," but other locales may alter this
          default.
      shapes
          A tuple of
          :class:`plotly.graph_objects.layout.Shape`
          instances or dicts with compatible properties
      shapedefaults
          When used in a template (as
          layout.template.layout.shapedefaults), sets the
          default property values to use for elements of
          layout.shapes
      showlegend
          Determines whether or not a legend is drawn.
          Default is `true` if there is a trace to show
          and any of these: a) Two or more traces would
          by default be shown in the legend. b) One pie
          trace is shown in the legend. c) One trace is
          explicitly given with `showlegend: true`.
      sliders
          A tuple of
          :class:`plotly.graph_objects.layout.Slider`
          instances or dicts with compatible properties
      sliderdefaults
          When used in a template (as
          layout.template.layout.sliderdefaults), sets
          the default property values to use for elements
          of layout.sliders
      smith
          :class:`plotly.graph_objects.layout.Smith`
          instance or dict with compatible properties
      spikedistance
          Sets the default distance (in pixels) to look
          for data to draw spikelines to (-1 means no
          cutoff, 0 means no looking for data). As with
          hoverdistance, distance does not apply to area-
          like objects. In addition, some objects can be
          hovered on but will not generate spikelines,
          such as scatter fills.
      sunburstcolorway
          Sets the default sunburst slice colors.
          Defaults to the main `colorway` used for trace
          colors. If you specify a new list here it can
          still be extended with lighter and darker
          colors, see `extendsunburstcolors`.
      template
          Default attributes to be applied to the plot.
          This should be a dict with format: `{'layout':
          layoutTemplate, 'data': {trace_type:
          [traceTemplate, ...], ...}}` where
          `layoutTemplate` is a dict matching the
          structure of `figure.layout` and
          `traceTemplate` is a dict matching the
          structure of the trace with type `trace_type`
          (e.g. 'scatter'). Alternatively, this may be
          specified as an instance of
          plotly.graph_objs.layout.Template.  Trace
          templates are applied cyclically to traces of
          each type. Container arrays (eg `annotations`)
          have special handling: An object ending in
          `defaults` (eg `annotationdefaults`) is applied
          to each array item. But if an item has a
          `templateitemname` key we look in the template
          array for an item with matching `name` and
          apply that instead. If no matching `name` is
          found we mark the item invisible. Any named
          template item not referenced is appended to the
          end of the array, so this can be used to add a
          watermark annotation or a logo image, for
          example. To omit one of these items on the
          plot, make an item with matching
          `templateitemname` and `visible: false`.
      ternary
          :class:`plotly.graph_objects.layout.Ternary`
          instance or dict with compatible properties
      title
          :class:`plotly.graph_objects.layout.Title`
          instance or dict with compatible properties
      titlefont
          Deprecated: Please use layout.title.font
          instead. Sets the title font. Note that the
          title's font used to be customized by the now
          deprecated `titlefont` attribute.
      transition
          Sets transition options used during
          Plotly.react updates.
      treemapcolorway
          Sets the default treemap slice colors. Defaults
          to the main `colorway` used for trace colors.
          If you specify a new list here it can still be
          extended with lighter and darker colors, see
          `extendtreemapcolors`.
      uirevision
          Used to allow user interactions with the plot
          to persist after `Plotly.react` calls that are
          unaware of these interactions. If `uirevision`
          is omitted, or if it is given and it changed
          from the previous `Plotly.react` call, the
          exact new figure is used. If `uirevision` is
          truthy and did NOT change, any attribute that
          has been affected by user interactions and did
          not receive a different value in the new figure
          will keep the interaction value.
          `layout.uirevision` attribute serves as the
          default for `uirevision` attributes in various
          sub-containers. For finer control you can set
          these sub-attributes directly. For example, if
          your app separately controls the data on the x
          and y axes you might set
          `xaxis.uirevision=*time*` and
          `yaxis.uirevision=*cost*`. Then if only the y
          data is changed, you can update
          `yaxis.uirevision=*quantity*` and the y axis
          range will reset but the x axis range will
          retain any user-driven zoom.
      uniformtext
          :class:`plotly.graph_objects.layout.Uniformtext
          ` instance or dict with compatible properties
      updatemenus
          A tuple of
          :class:`plotly.graph_objects.layout.Updatemenu`
          instances or dicts with compatible properties
      updatemenudefaults
          When used in a template (as
          layout.template.layout.updatemenudefaults),
          sets the default property values to use for
          elements of layout.updatemenus
      violingap
          Sets the gap (in plot fraction) between violins
          of adjacent location coordinates. Has no effect
          on traces that have "width" set.
      violingroupgap
          Sets the gap (in plot fraction) between violins
          of the same location coordinate. Has no effect
          on traces that have "width" set.
      violinmode
          Determines how violins at the same location
          coordinate are displayed on the graph. If
          "group", the violins are plotted next to one
          another centered around the shared location. If
          "overlay", the violins are plotted over one
          another, you might need to set "opacity" to see
          them multiple violins. Has no effect on traces
          that have "width" set.
      waterfallgap
          Sets the gap (in plot fraction) between bars of
          adjacent location coordinates.
      waterfallgroupgap
          Sets the gap (in plot fraction) between bars of
          the same location coordinate.
      waterfallmode
          Determines how bars at the same location
          coordinate are displayed on the graph. With
          "group", the bars are plotted next to one
          another centered around the shared location.
          With "overlay", the bars are plotted over one
          another, you might need to reduce "opacity" to
          see multiple bars.
      width
          Sets the plot's width (in px).
      xaxis
          :class:`plotly.graph_objects.layout.XAxis`
          instance or dict with compatible properties
      yaxis
          :class:`plotly.graph_objects.layout.YAxis`
          instance or dict with compatible properties
    

frames The 'frames' property is a tuple of instances of __ Frame that may be specified as__

  * A list or tuple of instances of plotly.graph_objs.Frame
  * A list or tuple of dicts of string/value properties that will be passed to the Frame constructor



Supported dict properties:
    
    
      baseframe
          The name of the frame into which this frame's
          properties are merged before applying. This is
          used to unify properties and avoid needing to
          specify the same values for the same properties
          in multiple frames.
      data
          A list of traces this frame modifies. The
          format is identical to the normal trace
          definition.
      group
          An identifier that specifies the group to which
          the frame belongs, used by animate to select a
          subset of frames.
      layout
          Layout properties which this frame modifies.
          The format is identical to the normal layout
          definition.
      name
          A label by which to identify the frame
      traces
          A list of trace indices that identify the
          respective traces in the data attribute
    

skip_invalid: bool If True, invalid properties in the figure specification will be skipped silently. If False (default) invalid properties in the figure specification will result in a ValueError

## Raises[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#raises_1 "Permanent link")

ValueError if a property in the specification of data, layout, or frames is invalid AND skip_invalid is False

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [FigureMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin "vectorbtpro.utils.figure.FigureMixin")
  * `ipywidgets.widgets.domwidget.DOMWidget`
  * `ipywidgets.widgets.widget.LoggingHasTraits`
  * `ipywidgets.widgets.widget.Widget`
  * `plotly.basedatatypes.BaseFigure`
  * `plotly.basewidget.BaseFigureWidget`
  * `plotly.graph_objs._figurewidget.FigureWidget`
  * `traitlets.traitlets.HasDescriptors`
  * `traitlets.traitlets.HasTraits`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.figure.FigureMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.figure.FigureMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.figure.FigureMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.figure.FigureMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.figure.FigureMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.figure.FigureMixin.find_messages")
  * [FigureMixin.auto_rangebreaks](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks "vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks")
  * [FigureMixin.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.copy "vectorbtpro.utils.figure.FigureMixin.copy")
  * [FigureMixin.resolve_show_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.resolve_show_args "vectorbtpro.utils.figure.FigureMixin.resolve_show_args")
  * [FigureMixin.save_svg_for_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs "vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs")
  * [FigureMixin.select_range](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.select_range "vectorbtpro.utils.figure.FigureMixin.select_range")
  * [FigureMixin.show_png](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_png "vectorbtpro.utils.figure.FigureMixin.show_png")
  * [FigureMixin.show_svg](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_svg "vectorbtpro.utils.figure.FigureMixin.show_svg")
  * [FigureMixin.skip_index](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.skip_index "vectorbtpro.utils.figure.FigureMixin.skip_index")



* * *

### show method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L330-L332 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureWidget.show "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-19-1)FigureWidget.show(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-19-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-19-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-19-4))
    

Show a figure using either the default renderer(s) or the renderer(s) specified by the renderer argument

## Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#parameters_5 "Permanent link")

renderer: str or None (default None) A string containing the names of one or more registered renderers (separated by '+' characters) or None. If None, then the default renderers specified in plotly.io.renderers.default are used.

validate: bool (default True) True if the figure should be validated before being shown, False otherwise.

width: int or float An integer or float that determines the number of pixels wide the plot is. The default is set in plotly.js.

height: int or float An integer or float that determines the number of pixels wide the plot is. The default is set in plotly.js.

config: dict A dict of parameters to configure the figure. The defaults are set in plotly.js.

## Returns[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#returns_2 "Permanent link")

None

* * *

## FigureWidgetResampler class[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L359-L378 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureWidgetResampler "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-20-1)FigureWidgetResampler(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-20-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-20-3)    empty_layout=False,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-20-4)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-20-5))
    

Figure widget resampler.

Extends `plotly.graph_objects.FigureWidget`.

Instantiate a resampling data mirror.

## Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#parameters_6 "Permanent link")

figure: BaseFigure The figure that will be decorated. Can be either an empty figure (e.g., `go.Figure()`, `make_subplots()`, `go.FigureWidget`) or an existing figure. convert_existing_traces: bool A bool indicating whether the high-frequency traces of the passed `figure` should be resampled, by default True. Hence, when set to False, the high-frequency traces of the passed `figure` will not be resampled. default_n_shown_samples: int, optional The default number of samples that will be shown for each trace, by default 1000.
    
    
    !!! note
        * This can be overridden within the [`add_trace`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_trace] method.
        * If a trace withholds fewer datapoints than this parameter,
          the data will *not* be aggregated.
    

default_downsampler: AbstractAggregator An instance which implements the AbstractSeriesDownsampler interface and will be used as default downsampler, by default `MinMaxLTTB`. 
    
    
    !!! note
        This can be overridden within the [`add_trace`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_trace] method.
    

default_gap_handler: GapHandler An instance which implements the AbstractGapHandler interface and will be used as default gap handler, by default `MedDiffGapHandler`. 
    
    
    !!! note
        This can be overridden within the [`add_trace`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_trace] method.
    

resampled_trace_prefix_suffix: str, optional A tuple which contains the `prefix` and `suffix`, respectively, which will be added to the trace its legend-name when a resampled version of the trace is shown. By default, a bold, orange `[R]` is shown as prefix (no suffix is shown). show_mean_aggregation_size: bool, optional Whether the mean aggregation bin size will be added as a suffix to the trace its legend-name, by default True. convert_traces_kwargs: dict, optional A dict of kwargs that will be passed to the [`add_traces`][figure_resampler.figure_resampler_interface.AbstractFigureAggregator.add_traces] method and will be used to convert the existing traces. 
    
    
    !!! note
        This argument is only used when the passed ``figure`` contains data and
        ``convert_existing_traces`` is set to True.
    

verbose: bool, optional Whether some verbose messages will be printed or not, by default False.

**Superclasses**

  * [Base](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base "vectorbtpro.utils.base.Base")
  * [FigureMixin](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin "vectorbtpro.utils.figure.FigureMixin")
  * `abc.ABC`
  * `ipywidgets.widgets.domwidget.DOMWidget`
  * `ipywidgets.widgets.widget.LoggingHasTraits`
  * `ipywidgets.widgets.widget.Widget`
  * `plotly.basedatatypes.BaseFigure`
  * `plotly.basewidget.BaseFigureWidget`
  * `plotly.graph_objs._figurewidget.FigureWidget`
  * `plotly_resampler.figure_resampler.figure_resampler_interface.AbstractFigureAggregator`
  * `plotly_resampler.figure_resampler.figurewidget_resampler.FigureWidgetResampler`
  * `traitlets.traitlets.HasDescriptors`
  * `traitlets.traitlets.HasTraits`



**Inherited members**

  * [Base.chat](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.chat "vectorbtpro.utils.figure.FigureMixin.chat")
  * [Base.find_api](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_api "vectorbtpro.utils.figure.FigureMixin.find_api")
  * [Base.find_assets](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_assets "vectorbtpro.utils.figure.FigureMixin.find_assets")
  * [Base.find_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_docs "vectorbtpro.utils.figure.FigureMixin.find_docs")
  * [Base.find_examples](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_examples "vectorbtpro.utils.figure.FigureMixin.find_examples")
  * [Base.find_messages](https://vectorbt.pro/pvt_7a467f6b/api/utils/base/#vectorbtpro.utils.base.Base.find_messages "vectorbtpro.utils.figure.FigureMixin.find_messages")
  * [FigureMixin.auto_rangebreaks](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks "vectorbtpro.utils.figure.FigureMixin.auto_rangebreaks")
  * [FigureMixin.copy](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.copy "vectorbtpro.utils.figure.FigureMixin.copy")
  * [FigureMixin.resolve_show_args](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.resolve_show_args "vectorbtpro.utils.figure.FigureMixin.resolve_show_args")
  * [FigureMixin.save_svg_for_docs](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs "vectorbtpro.utils.figure.FigureMixin.save_svg_for_docs")
  * [FigureMixin.select_range](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.select_range "vectorbtpro.utils.figure.FigureMixin.select_range")
  * [FigureMixin.show_png](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_png "vectorbtpro.utils.figure.FigureMixin.show_png")
  * [FigureMixin.show_svg](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.show_svg "vectorbtpro.utils.figure.FigureMixin.show_svg")
  * [FigureMixin.skip_index](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureMixin.skip_index "vectorbtpro.utils.figure.FigureMixin.skip_index")



* * *

### show method[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/figure.py#L376-L378 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#vectorbtpro.utils.figure.FigureWidgetResampler.show "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-21-1)FigureWidgetResampler.show(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-21-2)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-21-3)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#__codelineno-21-4))
    

Show a figure using either the default renderer(s) or the renderer(s) specified by the renderer argument

## Parameters[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#parameters_7 "Permanent link")

renderer: str or None (default None) A string containing the names of one or more registered renderers (separated by '+' characters) or None. If None, then the default renderers specified in plotly.io.renderers.default are used.

validate: bool (default True) True if the figure should be validated before being shown, False otherwise.

width: int or float An integer or float that determines the number of pixels wide the plot is. The default is set in plotly.js.

height: int or float An integer or float that determines the number of pixels wide the plot is. The default is set in plotly.js.

config: dict A dict of parameters to configure the figure. The defaults are set in plotly.js.

## Returns[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/figure/#returns_3 "Permanent link")

None
