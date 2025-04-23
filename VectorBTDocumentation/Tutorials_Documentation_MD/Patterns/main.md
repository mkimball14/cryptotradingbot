# Patterns[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#patterns "Permanent link")

Patterns provide a sense of order in what might otherwise appear chaotic. They tend to emerge everywhere in nature: shapes like circles in road signs or the rectangles in windows and doors. Just like children who gradually learn how to function in a completely unknown environment by looking for regularities, financial market participants need to learn how to navigate their complex, ever-changing environment as well. And just like our little fellows who have parents and teachers to assist their learning process (and Google, of course), we have a wonderful tool to assist ours — quantitative analysis. 

In this context, patterns are the distinctive formations created by the movements of prices on a chart and are the foundation of technical analysis. They help to suggest what prices might do next, based on what they have done in the past. For example, we can query all the occurrences of the picture we observe today from the past, to analyze how the things developed each time and to make a more nuanced trading decision by accounting for various possibilities. Patterns are especially useful in identifying points of transition between rising and falling trends, which is the quintessence of successful entry and exit timing. But patterns do not give any guarantee to result in the same outcome as before, neither they last forever: as opposed to the real world with its consistent structure and behavior, the financial world is dominated by noise and [false positives](https://en.wikipedia.org/wiki/False_positives_and_false_negatives) coming from intense interactions of people, systems, and other entities, and so finding something that works slightly better than random in a specific market regime is already an achievement - an exciting game with probabilities.

Let's create a simple use case where we want to identify the [Double Top](https://www.investopedia.com/terms/d/doubletop.asp) pattern. Let's pull two years of the daily `BTCUSDT` history as our baseline data:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-0-1)>>> from vectorbtpro import *
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-0-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-0-3)>>> data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-0-4)... "BTCUSDT", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-0-5)... start="2020-06-01 UTC", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-0-6)... end="2022-06-01 UTC"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-0-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-0-8)>>> data.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/data.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/data.dark.svg#only-dark)

By quickly scanning the picture, we can identify probably the most apparent occurrence of this pattern between October and December 2021:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-1-1)>>> data_window = data.loc["2021-09-25":"2021-11-25"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-1-2)>>> data_window.plot(plot_volume=False).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/data_window.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/data_window.dark.svg#only-dark)

As human beings, we can easily detect patterns in visual data. But how can it be done programmatically, where everything revolves around numbers? It would be expensive, unnecessary, and most likely in-effective training a [DNN](https://en.wikipedia.org/wiki/Deep_learning) just for this simple task. Following the wisdom "the simpler the algorithm, the better" for noisy data, we should design an algorithm that does the job conventionally, that is, by using loops and basic math.

Since one pattern can only be matched against one feature of data, we will use the [typical price](https://en.wikipedia.org/wiki/Typical_price):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-2-1)>>> price_window = data_window.hlc3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-2-2)>>> price_window.vbt.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/hlc3.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/hlc3.dark.svg#only-dark)

Let's design the pattern first. Price patterns are identified using a series of lines and/or curves. The "Double Top" pattern, for instance, can be represented by the following array:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-3-1)>>> pattern = np.array([1, 2, 3, 2, 3, 2])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-3-2)>>> pd.Series(pattern).vbt.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/double_top_pattern.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/double_top_pattern.dark.svg#only-dark)

It's important to note that the length and the absolute values of the pattern definition are of no importance; if the pattern runs from 1 to 3 or 1 to 60 will not make any difference because the pattern will be stretched horizontally and vertically to fit the respective price. What affects the computation though is how individual points are located in relation to each other. For example, the first point `2` comes exactly in the middle between the points `1` and `3`, meaning if the asset jumped in price to match the second point, it would ideally make the same jump to reach the first peak. Furthermore, since some numbers such as `2` and `3` repeat, we don't expect the price at those points to deviate much, which is useful for defining support/resistance lines. 

Another important rule is concerned around the horizontal pattern structure: irrespective of the value at any point, the location (timing) of the point is also relative to the location of the surrounding points. For example, if the first point was matched on `2020-01-01` and the second point on `2020-01-03`, the third point is expected to match on `2020-01-06`. This also means that if any part of the pattern requires more time to develop and thus changes the horizontal structure, matching would become less likely.


# Interpolation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#interpolation "Permanent link")

After we have defined our pattern, we need to bring it and the price to the same length. In image processing, increasing the size of an image requires reconstruction of the image by [interpolating](https://en.wikipedia.org/wiki/Interpolation) new pixels. Reducing the size of an image requires [downsampling](https://en.wikipedia.org/wiki/Downsampling_\(signal_processing\)) of the existing pixels. In pattern processing, the approach is similar; the only difference is that we're working on one-dimensional arrays instead of two-dimensional. We also prefer interpolation (stretching) over downsampling (shrinking) to avoid information loss. This means that if the price is smaller than the pattern, it should be stretched to match the length of the pattern rather than compressing the pattern to match the length of the price.

There are four main interpolation modes in pattern processing: linear, nearest neighbor, discrete, and mixed. All of them are implemented using the Numba-compiled function [interp_resize_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/patterns/#vectorbtpro.generic.nb.patterns.interp_resize_1d_nb), which takes an array, a target size, and an interpolation mode of the type [InterpMode](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.InterpMode). The implementation is highly efficient: it goes through the array only once and doesn't require creation of additional arrays apart from the final array.


# Linear[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#linear "Permanent link")

The linear interpolation algorithm involves estimating a new value by connecting two adjacent known values with a straight line (see [here](https://scientific-python.readthedocs.io/en/latest/notebooks_rst/1_Interpolation/1D_interpolation.html#linear-interpolation) for an illustration). 

Let's stretch our pattern array to 10 points:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-4-1)>>> resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-4-2)... pattern, 10, vbt.enums.InterpMode.Linear
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-4-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-4-4)>>> resized_pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-4-5)array([1. , 1.55555556, 2.11111111, 2.66666667, 2.77777778,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-4-6) 2.22222222, 2.33333333, 2.88888889, 2.55555556, 2. ])
 
[/code]

This mode works best if the target size is close to `2 * n - 1`, where `n` is the original size of the array. In such a case, the characteristics of the resized array will closely match that of the original array. Otherwise, the relation of points to each other will be violated, unless the target size is sufficiently bigger than the original size. This is best demonstrated below, where we resize the array to the length of 7, 11, and 30 points respectively:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-5-1)>>> def plot_linear(n):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-5-2)... resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-5-3)... pattern, n, vbt.enums.InterpMode.Linear
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-5-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-5-5)... return pd.Series(resized_pattern).vbt.plot()
 
[/code]

7 points11 points30 points
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-6-1)>>> plot_linear(7).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/linear_7.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/linear_7.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-7-1)>>> plot_linear(11).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/linear_11.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/linear_11.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-8-1)>>> plot_linear(30).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/linear_30.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/linear_30.dark.svg#only-dark)

Why is the first graph so "ugly"? Because the algorithm needs to keep the same distance between each pair of points in the resized array. To stretch a 6-point array to 7 points, the algorithm first needs to split the graph of the 6-point array into 7 parts, and then to select the value that's located at the mid-point of each part, like this:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-9-1)>>> resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-9-2)... pattern, 7, vbt.enums.InterpMode.Linear
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-9-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-9-4)>>> ratio = (len(pattern) - 1) / (len(resized_pattern) - 1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-9-5)>>> new_points = np.arange(len(resized_pattern)) * ratio
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-9-6)>>> fig = pd.Series(pattern).vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-9-7)>>> pd.Series(resized_pattern, index=new_points).vbt.scatterplot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-9-8)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/linear_7_scatter.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/linear_7_scatter.dark.svg#only-dark)

As we can see, linear interpolation is all about selecting a specific number of equidistant values from the original array, and the greater is the number of points, the better is the result. The main issue is that whenever the target size is suboptimal, the scale of the resized array will change. In the example above, the pattern will be distorted and the original link between the points with the value `2` will be gone. But there are other interpolation algorithms that do better here.


# Nearest[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#nearest "Permanent link")

The nearest neighbor algorithm selects the value of the nearest point and does not consider the values of other points at all (see [here](https://scientific-python.readthedocs.io/en/latest/notebooks_rst/1_Interpolation/1D_interpolation.html#nearest-aka-piecewise-interpolation) for an illustration). This way, the resized array will consist exclusively of the values in the original array and there won't be any intermediate values as floating numbers present:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-10-1)>>> resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-10-2)... pattern, 10, vbt.enums.InterpMode.Nearest
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-10-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-10-4)>>> resized_pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-10-5)array([1., 2., 2., 3., 3., 2., 2., 3., 3., 2.])
 
[/code]

Info

The resized array will always be floating for consistency reasons.

And here are resized arrays for different target sizes:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-11-1)>>> def plot_nearest(n):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-11-2)... resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-11-3)... pattern, n, vbt.enums.InterpMode.Nearest
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-11-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-11-5)... return pd.Series(resized_pattern).vbt.plot()
 
[/code]

7 points11 points30 points
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-12-1)>>> plot_nearest(7).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/nearest_7.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/nearest_7.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-13-1)>>> plot_nearest(11).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/nearest_11.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/nearest_11.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-14-1)>>> plot_nearest(30).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/nearest_30.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/nearest_30.dark.svg#only-dark)

As we can see, each graph above is basically a step curve consisting of horizontal and vertical lines. Because of this, it may be challenging to apply since we expect the price to change gradually rather to jump around sharply, thus this interpolation mode should be used only when the original array is granular enough to smoothen the transitions between local extrema.

Hint

The `2 * n - 1` rule doesn't hold for this mode.


# Discrete[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#discrete "Permanent link")

The discrete interpolation algorithm selects the value depending on whether it's closer to the target position than other values, and if not, sets it to NaN. This mode guarantees to produce an array with values taken from the original array only once, but may still change their temporal distribution. This makes most sense in scenarios where the transition between each pair of points is of no interest.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-15-1)>>> resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-15-2)... pattern, 10, vbt.enums.InterpMode.Discrete
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-15-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-15-4)>>> resized_pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-15-5)array([ 1., nan, 2., nan, 3., 2., nan, 3., nan, 2.])
 
[/code]

Here's a comparison of differently-resized arrays:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-1)>>> def plot_discrete(n):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-2)... resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-3)... pattern, n, vbt.enums.InterpMode.Discrete
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-5)... return pd.Series(resized_pattern).vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-6)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-7)... line=dict(dash="dot"), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-8)... connectgaps=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-16-10)... )
 
[/code]

7 points11 points30 points
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-17-1)>>> plot_discrete(7).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/discrete_7.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/discrete_7.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-18-1)>>> plot_discrete(11).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/discrete_11.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/discrete_11.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-19-1)>>> plot_discrete(30).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/discrete_30.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/discrete_30.dark.svg#only-dark)

Each of the graphs contains exactly 6 points that have been mapped to a new interval by trying to keep the distance between them as equal as possible. Similarly to the linear interpolation, this mode also yields the best results only if the target size is `2 * n - 1`, while other sizes distort the temporal distribution of the points. In contrast to the linear interpolation though, this mode respects the absolute values of the original array such that the point `2` is always guaranteed to be on the midway between the points `1` and `3`.


# Mixed[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#mixed "Permanent link")

The mixed interpolation algorithm is a mix of the linear and discrete interpolation algorithms. First, it calls the discrete interpolator, and if the value is NaN, it calls the linear interpolator. This way, we are guaranteed to include each value from the original array at least once to keep the original scaling, and at the same time connect them by linearly interpolating the intermediate values - the best of both worlds.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-20-1)>>> resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-20-2)... pattern, 10, vbt.enums.InterpMode.Mixed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-20-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-20-4)>>> resized_pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-20-5)array([1. , 1.55555556, 2. , 2.66666667, 3. ,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-20-6) 2. , 2.33333333, 3. , 2.55555556, 2. ])
 
[/code]

Let's demonstrate how the mixed approach "fixes" the scale problem of the linear approach:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-1)>>> def plot_mixed(n):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-2)... lin_resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-3)... pattern, n, vbt.enums.InterpMode.Linear
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-5)... mix_resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-6)... pattern, n, vbt.enums.InterpMode.Mixed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-8)... fig = pd.Series(lin_resized_pattern, name="Linear").vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-9)... pd.Series(mix_resized_pattern, name="Mixed").vbt.plot(fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-21-10)... return fig
 
[/code]

7 points11 points30 points
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-22-1)>>> plot_mixed(7).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/mixed_7.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/mixed_7.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-23-1)>>> plot_mixed(11).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/mixed_11.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/mixed_11.dark.svg#only-dark)
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-24-1)>>> plot_mixed(30).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/mixed_30.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/mixed_30.dark.svg#only-dark)

Info

As you probably noticed, the last pattern line is not entirely straight on the graph. This is because by using the mixed interpolation we're interpolating some points linearly and some discretely to retain the original scale. Producing a clean line would require us to go through the data more than once, thus we chose performance over visual aesthetics.

We have restored the original connection between various points, hence this algorithm should be (and is) the default choice when it comes to interpolation without gaps.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-25-1)>>> resized_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-25-2)... pattern, len(price_window), vbt.enums.InterpMode.Mixed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-25-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-25-4)>>> resized_pattern.shape
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-25-5)(62,)
 
[/code]


# Rescaling[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#rescaling "Permanent link")

After we brought the pattern and the price to the same length, we need to bring them to the same scale as well in order to make them comparable. For this, we need to compute the minimum and maximum of the pattern and price, and rescale the pattern to match the scale of the price. We can use the Numba-compiled function [rescale_nb](https://vectorbt.pro/pvt_7a467f6b/api/utils/array_/#vectorbtpro.utils.array_.rescale_nb), which takes an array, the scale of the array, and the target scale:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-26-1)>>> pattern_scale = (resized_pattern.min(), resized_pattern.max())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-26-2)>>> price_window_scale = (price_window.min(), price_window.max())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-26-3)>>> rescaled_pattern = vbt.utils.array_.rescale_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-26-4)... resized_pattern, pattern_scale, price_window_scale
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-26-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-26-6)>>> rescaled_pattern = pd.Series(rescaled_pattern, index=price_window.index)
 
[/code]

We can now finally overlay the pattern over the price:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-1)>>> fig = price_window.vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-2)>>> rescaled_pattern.vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-3)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-4)... fill="tonexty", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-5)... fillcolor="rgba(255, 0, 0, 0.25)"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-6)... ), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-7)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-27-9)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/rescaled_pattern.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/rescaled_pattern.dark.svg#only-dark)


# Rebasing[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#rebasing "Permanent link")

Another way to bring both arrays to the same scale is by using rebasing, which makes the first value of both arrays equal, and all other values are rescaled using their relative distance to the starting point. This is useful in the case where our pattern should also enforce a certain percentage change from the starting point. For example, let's enforce the relative distance between the peak and the starting point of 60%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-1)>>> pct_pattern = np.array([1, 1.3, 1.6, 1.3, 1.6, 1.3])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-2)>>> resized_pct_pattern = vbt.nb.interp_resize_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-3)... pct_pattern, len(price_window), vbt.enums.InterpMode.Mixed
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-5)>>> rebased_pattern = resized_pct_pattern / resized_pct_pattern[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-6)>>> rebased_pattern *= price_window.values[0]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-7)>>> rebased_pattern = pd.Series(rebased_pattern, index=price_window.index)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-8)>>> fig = price_window.vbt.plot()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-9)>>> rebased_pattern.vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-10)... trace_kwargs=dict(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-11)... fill="tonexty", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-12)... fillcolor="rgba(255, 0, 0, 0.25)"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-13)... ), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-14)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-28-16)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/rebased_pattern.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/rebased_pattern.dark.svg#only-dark)


# Fitting[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#fitting "Permanent link")

Interpolation and rescaling are required to bring both the pattern and the price to the same length and scale respectively; the goal is to enable them to be compared and combined as regular NumPy arrays. Instead of performing the steps above manually though, let's take a look at a special function that does the entire work for us: [fit_pattern_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/patterns/#vectorbtpro.generic.nb.patterns.fit_pattern_nb).
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-29-1)>>> new_pattern, _ = vbt.nb.fit_pattern_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-29-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-29-3)... pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-29-4)... interp_mode=vbt.enums.InterpMode.Mixed,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-29-5)... rescale_mode=vbt.enums.RescaleMode.Rebase 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-29-6)... )
 
[/code]

 1. 2. 3. 

What does `_` mean? The function actually returns two arrays: one for pattern and one for maximum error (see [Max error](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#max-error)). Since we don't need the array for maximum error, we ignore it by substituting the variable with `_`. Let's make sure that the automatically-generated array contains the same values as the manually-generated one:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-30-1)>>> np.testing.assert_array_equal(new_pattern, rebased_pattern)
 
[/code]

No errors raised - both arrays are identical!


# Similarity[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#similarity "Permanent link")

Our arrays are now perfectly comparable, so how do we calculate their similarity? The algorithm is rather easy: compute the absolute, element-wise distances between the values of both arrays, and add them up (a.k.a. [Mean Absolute Error](https://en.wikipedia.org/wiki/Mean_absolute_error) or MAE). At the same time, compute the maximum possible absolute, element-wise distances, and add them up. The maximum distance is calculated relative to the global minimum and maximum value. Finally, divide both totals and subtract from 1 to get the similarity score that ranges between 0 and 1:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-1)>>> abs_distances = np.abs(rescaled_pattern - price_window.values)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-2)>>> mae = abs_distances.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-3)>>> max_abs_distances = np.column_stack((
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-4)... (price_window.max() - rescaled_pattern), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-5)... (rescaled_pattern - price_window.min())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-6)... )).max(axis=1)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-7)>>> max_mae = max_abs_distances.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-8)>>> similarity = 1 - mae / max_mae
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-9)>>> similarity
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-31-10)0.8726845123416802
 
[/code]

To penalize large distances and make the pattern detection more "strict", we can switch the distance measure to the root of sum of squared distances (a.k.a. [Root Mean Squared Error](https://en.wikipedia.org/wiki/Root-mean-square_deviation) or RMSE):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-1)>>> quad_distances = (rescaled_pattern - price_window.values) ** 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-2)>>> rmse = np.sqrt(quad_distances.sum())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-3)>>> max_quad_distances = np.column_stack((
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-4)... (price_window.max() - rescaled_pattern), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-5)... (rescaled_pattern - price_window.min())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-6)... )).max(axis=1) ** 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-7)>>> max_rmse = np.sqrt(max_quad_distances.sum())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-8)>>> similarity = 1 - rmse / max_rmse
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-9)>>> similarity
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-32-10)0.8484851233108504
 
[/code]

As a further adaptation, we could have also removed the root from the equation above and calculated just the sum of squared distances (a.k.a. [Mean Squared Error](https://en.wikipedia.org/wiki/Mean_squared_error) or MSE):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-1)>>> quad_distances = (rescaled_pattern - price_window.values) ** 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-2)>>> mse = quad_distances.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-3)>>> max_quad_distances = np.column_stack((
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-4)... (price_window.max() - rescaled_pattern), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-5)... (rescaled_pattern - price_window.min())
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-6)... )).max(axis=1) ** 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-7)>>> max_mse = max_quad_distances.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-8)>>> similarity = 1 - mse / max_mse
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-9)>>> similarity
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-33-10)0.9770432421418718
 
[/code]

Note

Since the maximum distance is now the power of 2 of the absolute maximum distance, the similarity will often cross the mark of 90% and above, thus do not forget to adapt your thresholds as well.

If you're frightened of writing the code above each time you need to measure the similarity between two arrays, don't! As with everything, there is the convenient Numba-compiled function [pattern_similarity_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/patterns/#vectorbtpro.generic.nb.patterns.pattern_similarity_nb), which combines all the steps above to produce a single number. This function accepts many options for interpolation, rescaling, and distance measurement, and runs in [O(n)](https://en.wikipedia.org/wiki/Time_complexity) time without creating any new arrays. Due to its exceptional efficiency and compilation with Numba, we can run the function millions of times in a fraction of a second ![🔥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f525.svg) The only difference to our approach above is that it rescales the price array to the pattern scale, not the other way around (which we used for plotting reasons).

Let's explore the power of this function by replicating our pipeline above: 
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-34-1)>>> vbt.nb.pattern_similarity_nb(price_window.values, pattern)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-34-2)0.8726845123416802
 
[/code]

The same score as we produced manually ![👀](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f440.svg)

Let's calculate the similarity score for `pct_pattern` with rebasing:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-35-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-35-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-35-3)... pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-35-4)... rescale_mode=vbt.enums.RescaleMode.Rebase 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-35-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-35-6)0.8647140967291362
 
[/code]

 1. 

Let's get the similarity score from interpolating the pattern using the nearest-neighbor interpolation, rebasing, and RMSE:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-36-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-36-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-36-3)... pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-36-4)... interp_mode=vbt.enums.InterpMode.Nearest, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-36-5)... rescale_mode=vbt.enums.RescaleMode.Rebase,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-36-6)... distance_measure=vbt.enums.DistanceMeasure.RMSE 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-36-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-36-8)0.76151009787845
 
[/code]

 1. 2. 

Since often we're not only interested in getting the similarity measure but also in being able to visualize and debug the pattern, we can call the accessor method [GenericSRAccessor.plot_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.plot_pattern), which reconstructs the similarity calculation and displays various artifacts visually. That is, if we want it to produce an accurate plot, we need to provide the same arguments as we provide to the similarity calculation function. Our last example produced a similarity of 75%, let's visualize the fit:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-37-1)>>> price_window.vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-37-2)... pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-37-3)... interp_mode="nearest", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-37-4)... rescale_mode="rebase",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-37-5)... fill_distance=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-37-6)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/plot_pattern.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/plot_pattern.dark.svg#only-dark)

We see that the biggest discrepancy comes at the valley in the middle: the interpolated pattern expects the price to dip deeper than it actually does. Let's add 15% to that point to increase the similarity:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-1)>>> adj_pct_pattern = np.array([1, 1.3, 1.6, 1.45, 1.6, 1.3])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-2)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-3)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-4)... adj_pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-5)... interp_mode=vbt.enums.InterpMode.Nearest,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-6)... rescale_mode=vbt.enums.RescaleMode.Rebase,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-7)... distance_measure=vbt.enums.DistanceMeasure.RMSE
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-38-9)0.8086016654243109
 
[/code]

And here's how the discrete interpolation applied to the new pattern looks like:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-39-1)>>> price_window.vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-39-2)... adj_pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-39-3)... interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-39-4)... rescale_mode="rebase",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-39-5)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/plot_pattern_discrete.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/plot_pattern_discrete.dark.svg#only-dark)

The pattern trace has become a scatter plot rather than a line plot because the similarity is calculated based solely on those points whereas the greyed out points are ignored. If we calculated the similarity score once again, we would see a number higher than previously because the pattern at those points matches the price pretty accurately:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-40-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-40-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-40-3)... adj_pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-40-4)... interp_mode=vbt.enums.InterpMode.Discrete,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-40-5)... rescale_mode=vbt.enums.RescaleMode.Rebase,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-40-6)... distance_measure=vbt.enums.DistanceMeasure.RMSE
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-40-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-40-8)0.8719692914480557
 
[/code]


# Relative[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#relative "Permanent link")

Since the price is not static, and it may change significantly during the period of comparison, we should be interested in calculating the relative as opposed to the absolute distance (error). For example, if the first price point is `10` and the last price point is `1000`, the distance to the latter would have a much greater impact on the similarity score than the distance to the former. Let's re-calculate the score manually and automatically using relative distances:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-1)>>> abs_pct_distances = abs_distances / rescaled_pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-2)>>> pct_mae = abs_pct_distances.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-3)>>> max_abs_pct_distances = max_abs_distances / rescaled_pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-4)>>> max_pct_mae = max_abs_pct_distances.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-5)>>> similarity = 1 - pct_mae / max_pct_mae
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-6)>>> similarity
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-7)0.8732697724295595
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-9)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-10)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-11)... pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-12)... error_type=vbt.enums.ErrorType.Relative 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-41-14)0.8732697724295594
 
[/code]

 1. 

The difference is not that big in our scenario, but here's what happens when the price moves sharply:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-2)... np.array([10, 30, 100]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-3)... np.array([1, 2, 3]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-4)... error_type=vbt.enums.ErrorType.Absolute
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-6)0.8888888888888888
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-8)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-9)... np.array([10, 30, 100]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-10)... np.array([1, 2, 3]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-11)... error_type=vbt.enums.ErrorType.Relative
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-42-13)0.9575911789652247
 
[/code]

In both examples, the pattern has been rescaled to `[10, 55, 100]` using the min-max rescaler (default). In first example though, the normalized error is `abs(30 - 55) / (100 - 30) = 0.36`, while in the second example the normalized error is `(abs(30 - 55) / 55) / ((100 - 30) / 30) = 0.19`, which also takes into account the volatility of the price.


# Inverse[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#inverse "Permanent link")

We can also invert the pattern internally:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-43-1)>>> vbt.nb.pattern_similarity_nb(price_window.values, pattern, invert=True)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-43-2)0.32064009029620244
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-43-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-43-4)>>> price_window.vbt.plot_pattern(pattern, invert=True).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/inverted_pattern.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/inverted_pattern.dark.svg#only-dark)

Note

This isn't the same as simply inverting the score.

To produce the inverted pattern manually:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-44-1)>>> pattern.max() + pattern.min() - pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-44-2)array([3, 2, 1, 2, 1, 2])
 
[/code]


# Max error[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#max-error "Permanent link")

Sometimes we may want to define patterns as "corridors" within which the price should move. If any of the corridor points were violated, we can either set the distance at that point to the maximum distance (`max_error_strict=False`), or set the entire similarity to NaN (`max_error_strict=True`). Such a corridor is referred to as "maximum error". This error can be provided through the array-like argument `max_error`, which should be defined in the same way as the pattern; that is, it mostly needs to have the same length and scale as the pattern.

For example, if we chose the min-max rescaling and the pattern was defined from `1` to `6`, a maximum error of `0.5` would be `0.5 / (6 - 1) = 0.1`, that is, 10% of the pattern's scale. Let's query the similarity of our original pattern without and with a corridor of `0.5`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-3)... pattern,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-4)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-5)0.8726845123416802
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-6)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-7)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-8)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-9)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-10)... max_error=np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-45-12)0.8611332262389184
 
[/code]

Since `max_error` is a flexible argument, we can also provide it as a zero-dimensional or one-dimensional array with one value, which will be valid for each point in the pattern:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-46-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-46-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-46-3)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-46-4)... max_error=np.array([0.5]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-46-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-46-6)0.8611332262389184
 
[/code]

 1. 

The similarity score has decreased, which means that some corridor points were violated. Let's visualize the entire thing to see where exactly:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-47-1)>>> price_window.vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-47-2)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-47-3)... max_error=0.5 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-47-4)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_error.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_error.dark.svg#only-dark)

We can see two points that were violated, thus their distance to the price was set to the maximum possible distance, which brought the similarity down. If we enabled the strict mode though, the similarity would have become NaN to notify the user that it didn't pass the test:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-48-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-48-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-48-3)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-48-4)... max_error=np.array([0.5]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-48-5)... max_error_strict=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-48-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-48-7)nan
 
[/code]

If we're interested in relative distances using `ErrorType.Relative`, the maximum error should be provided as a percentage change:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-3)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-4)... max_error=np.array([0.1]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-5)... error_type=vbt.enums.ErrorType.Relative
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-7)0.8548520433078988
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-8)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-9)>>> price_window.vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-10)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-11)... max_error=0.1,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-12)... error_type="relative"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-49-13)... ).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_error_relative.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_error_relative.dark.svg#only-dark)

The same goes for the rescaling using rebasing mode, where irrespective of the error type each error must be given as a percentage change. For example, if the current pattern value has been mapped the price of `12000` and the maximum error is `0.1`, the corridor will encompass all the values from `12000 * 0.9 = 10800` to `12000 * 1.1 = 13200`. Let's permit deviations for the adjusted percentage pattern of no more than 20% at the first level, 10% at the second level, and 5% at the third level:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-3)... adj_pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-4)... rescale_mode=vbt.enums.RescaleMode.Rebase,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-5)... max_error=np.array([0.2, 0.1, 0.05, 0.1, 0.05, 0.1]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-6)... max_error_strict=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-8)nan
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-9)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-10)>>> price_window.vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-11)... adj_pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-12)... rescale_mode="rebase",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-13)... max_error=np.array([0.2, 0.1, 0.05, 0.1, 0.05, 0.1])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-50-14)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_error_rebase.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_error_rebase.dark.svg#only-dark)

As we can see, some points go outside the corridor. If we added additional 5% to all points, the pattern would pass the test easily:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-51-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-51-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-51-3)... adj_pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-51-4)... rescale_mode=vbt.enums.RescaleMode.Rebase,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-51-5)... max_error=np.array([0.2, 0.1, 0.05, 0.1, 0.05, 0.1]) + 0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-51-6)... max_error_strict=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-51-7)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-51-8)0.8789689066239321
 
[/code]


# Interpolation[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#interpolation_1 "Permanent link")

But is there a way to provide the maximum error discretely? That is, can we force the function to adhere to the corridor at certain points rather than at all points gradually? By default, the maximum error gets interpolated the same way as the pattern (linearly in our case). To make the maximum error array interpolate differently, provide a different mode as `max_error_interp_mode`. For example, let's only force the peak points to be within the corridor of 10%. For this, we need to use the discrete interpolation mode and set all the intermediate points to NaN:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-2)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-3)... adj_pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-4)... rescale_mode=vbt.enums.RescaleMode.Rebase,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-5)... max_error=np.array([np.nan, np.nan, 0.1, np.nan, 0.1, np.nan]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-6)... max_error_interp_mode=vbt.enums.InterpMode.Discrete,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-7)... max_error_strict=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-9)0.8789689066239321
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-11)>>> price_window.vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-12)... adj_pct_pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-13)... rescale_mode="rebase",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-14)... max_error=np.array([np.nan, np.nan, 0.1, np.nan, 0.1, np.nan]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-15)... max_error_interp_mode="discrete"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-52-16)... ).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_error_discrete.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_error_discrete.dark.svg#only-dark)

Even though the scatter points of the maximum error are connected by a greyed-out line, there is no requirement for the price to be between those lines, only between each pair of purple points.


# Max distance[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#max-distance "Permanent link")

Final question: is there a way to tweak the maximum distance? Yes! We can use the maximum error as the maximum distance by enabling `max_error_as_maxdist`. This has the following implications: the smaller is the maximum distance at any point, the heavier the volatility of the price at that point affects the similarity. Let's compare our original pattern without and with the maximum distance cap of `0.5` (10% of the scale):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-1)>>> vbt.nb.pattern_similarity_nb(price_window.values, pattern)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-2)0.8726845123416802
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-4)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-5)... price_window.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-6)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-7)... max_error=np.array([0.5]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-8)... max_error_as_maxdist=True
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-53-10)0.6193594883412921
 
[/code]

This way, we introduced a penalty for a heightened volatility of the price.

Note

You can also set a different maximum distance at different points in the pattern. Just note that points with a larger maximum distance will have more weight in the similarity calculation than points with a smaller maximum distance. Consider a scenario where there are two points with the maximum distance of `100` and `1` respectively. Even if we had a perfect match at the second point, the similarity would be largely based on the distance at the first point.


# Further filters[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#further-filters "Permanent link")

When matching a huge amount of price windows against a pattern, we may want to skip some windows due to a volatility that is either too low or too high. This is possible by setting the arguments `min_pct_change` and `max_pct_change` respectively:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-54-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-54-2)... price_window.values, pattern, max_pct_change=0.3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-54-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-54-4)nan
 
[/code]

A nice side effect of this is an increased performance: if the test fails, the price window will be traversed only once to get the minimum and maximum value.

We can also filter out similarity scores that are below some predefined threshold. For example, let's set the minimum similarity to 90%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-55-1)>>> vbt.nb.pattern_similarity_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-55-2)... price_window.values, pattern, min_similarity=0.9
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-55-3)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-55-4)nan
 
[/code]

Hint

Don't be afraid of NaNs, they simply mean _"didn't pass some tests, should be ignored during analysis"_.

Setting a similarity threshold has also a performance benefit: if at some point the algorithm notices that the threshold cannot be reached anymore, even if the remaining points had matched perfectly, it will abort and set the final score to NaN. Depending on the threshold, this makes the computation 30% faster on average.


# Rolling similarity[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#rolling-similarity "Permanent link")

We've learned the theory behind pattern recognition, now it's time to get our hands dirty. To search a price space for a pattern, we need to roll a window over that space. This can be accomplished using the accessor method [GenericAccessor.rolling_pattern_similarity](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.rolling_pattern_similarity), which takes the same arguments as we used before, but also the length of the window to roll. If the length is `None`, it will be set to the length of the pattern array.

Let's roll a window of 30 data points over the entire typical price, and match against a pattern that has a discrete soft corridor of 5%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-1)>>> price = data.hlc3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-2)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-3)>>> similarity = price.vbt.rolling_pattern_similarity(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-4)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-5)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-6)... error_type="relative",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-7)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-8)... max_error_interp_mode="discrete"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-10)>>> similarity.describe()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-11)count 701.000000
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-12)mean 0.499321
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-13)std 0.144088
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-14)min 0.148387
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-15)25% 0.394584
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-16)50% 0.502231
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-17)75% 0.607962
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-18)max 0.838393
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-56-19)dtype: float64
 
[/code]

We see that among 701 comparisons roughly a half has produced a score below 50%. The highest score sits at around 84%. Let's visualize the best match:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-1)>>> end_row = similarity.argmax() + 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-2)>>> start_row = end_row - 30
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-3)>>> fig = data.iloc[start_row:end_row].plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-4)>>> price.iloc[start_row:end_row].vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-5)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-6)... error_type="relative", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-7)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-8)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-9)... plot_obj=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-10)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-57-12)>>> fig.show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_rolling_similarity.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/max_rolling_similarity.dark.svg#only-dark)

Pretty accurate, right? And this window matches even better than the window we investigated previously. But what about the lowest similarity, is it the same as inverting the pattern? No!
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-1)>>> end_row = similarity.argmin() + 1
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-2)>>> start_row = end_row - 30
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-3)>>> fig = data.iloc[start_row:end_row].plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-4)>>> price.iloc[start_row:end_row].vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-5)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-6)... invert=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-7)... error_type="relative",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-8)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-9)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-10)... plot_obj=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-11)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-58-13)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/min_rolling_similarity.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/min_rolling_similarity.dark.svg#only-dark)

Inverting the score will invalidate all the requirements that we put initially, thus you should always start a new pattern search with the `invert` flag enabled:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-1)>>> inv_similarity = price.vbt.rolling_pattern_similarity(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-2)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-3)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-4)... invert=True, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-5)... error_type="relative",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-6)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-7)... max_error_interp_mode="discrete"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-8)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-9)>>> end_row = inv_similarity.argmax() + 1 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-10)>>> start_row = end_row - 30
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-11)>>> fig = data.iloc[start_row:end_row].plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-12)>>> price.iloc[start_row:end_row].vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-13)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-14)... invert=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-15)... error_type="relative",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-16)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-17)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-18)... plot_obj=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-19)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-20)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-59-21)>>> fig.show()
 
[/code]

 1. 2. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/inv_rolling_similarity.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/inv_rolling_similarity.dark.svg#only-dark)

The best match isn't exactly a good fit, but still much better than the previous one.


# Indicator[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#indicator "Permanent link")

Once we've settled the optimal pattern parameters through exploration and debugging, we should start concerning ourselves with integrating the pattern detection component into our backtesting stack. This can be done through running the process inside an indicator. Since indicators must return output arrays of the same shape as their input arrays, we can safely use the rolling pattern similarity as output. For this, we can use the [PATSIM](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/patsim/#vectorbtpro.indicators.custom.patsim.PATSIM) indicator, which takes a price array as the only input, and all the arguments related to calculating the pattern similarity as parameters, including the pattern array itself! Another advantage of this indicator is the ability to automatically convert arguments provided as a string (such as `interp_mode`) into a Numba-compatible format. Finally, indicators are great for testing many windows as the accuracy of pattern detection heavily depends on the choice of window length.

Let's test multiple window combinations along with the same setup as above:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-60-1)>>> patsim = vbt.PATSIM.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-60-2)... price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-60-3)... vbt.Default(pattern), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-60-4)... error_type=vbt.Default("relative"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-60-5)... max_error=vbt.Default(0.05),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-60-6)... max_error_interp_mode=vbt.Default("discrete"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-60-7)... window=[30, 45, 60, 75, 90]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-60-8)... )
 
[/code]

 1. 

We can plot the similarity development using the method [PATSIM.plot](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/patsim/#vectorbtpro.indicators.custom.patsim.PATSIM.plot). As any other plotting method, it allows only one column to be plotted, thus we need to specify the column name beforehand using the argument `column`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-61-1)>>> patsim.wrapper.columns 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-61-2)Int64Index([30, 45, 60, 75, 90], dtype='int64', name='patsim_window')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-61-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-61-4)>>> patsim.plot(column=60).show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/patsim.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/patsim.dark.svg#only-dark)

The generated similarity series is as fascinating as the price series itself, and can be used in all sorts of technical analysis on its own ![📐](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f4d0.svg)

But probably an even more informative plot can be produced by [PATSIM.overlay_with_heatmap](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/patsim/#vectorbtpro.indicators.custom.patsim.PATSIM.overlay_with_heatmap), which overlays a price line with a similarity heatmap:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-62-1)>>> patsim.overlay_with_heatmap(column=60).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/patsim_heatmap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/patsim_heatmap.dark.svg#only-dark)

Info

Bright vertical lines on the graph are located at the very end of their windows, that is, where the pattern is marked as completed. Hence, the similarity score is safe to use in backtesting.

So, how do we use this indicator in signal generation? We can compare the resulting similarity score to a threshold to derive signals. For our example above, let's set a threshold of 80% to build the exit signals:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-1)>>> exits = patsim.similarity >= 0.8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-2)>>> exits.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-3)patsim_window
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-4)30 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-5)45 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-6)60 14
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-7)75 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-8)90 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-63-9)dtype: int64
 
[/code]

If we wanted to test multiple thresholds, we could have also used the parameter `min_similarity`, which would set all scores falling below it to NaN, but also make pattern recognition faster on average. Deriving the signals would be as simple as checking whether each element is NaN. We'll additionally test the inverted pattern:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-1)>>> patsim = vbt.PATSIM.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-2)... price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-3)... vbt.Default(pattern),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-4)... error_type=vbt.Default("relative"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-5)... max_error=vbt.Default(0.05),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-6)... max_error_interp_mode=vbt.Default("discrete"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-7)... window=[30, 45, 60, 75, 90],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-8)... invert=[False, True],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-9)... min_similarity=[0.7, 0.8],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-10)... param_product=True 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-12)>>> exits = ~patsim.similarity.isnull() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-13)>>> exits.sum()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-14)patsim_window patsim_invert patsim_min_similarity
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-15)30 False 0.7 68
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-16) 0.8 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-17) True 0.7 64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-18) 0.8 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-19)... ... ... ...
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-20)90 False 0.7 61
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-21) 0.8 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-22) True 0.7 70
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-23) 0.8 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-64-24)dtype: int64
 
[/code]

 1. 2. 

What if we're not interested in having the window as a backtestable parameter, but rather we want to create a signal as soon as any of the windows at that row crossed the similarity threshold? This way, we would be able to react immediately once a pattern of any length was detected. This is easily achievable using Pandas:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-65-1)>>> groupby = [ 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-65-2)... name for name in patsim.wrapper.columns.names 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-65-3)... if name != "patsim_window"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-65-4)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-65-5)>>> max_sim = patsim.similarity.groupby(groupby, axis=1).max() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-65-6)>>> entries = ~max_sim.xs(True, level="patsim_invert", axis=1).isnull() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-65-7)>>> exits = ~max_sim.xs(False, level="patsim_invert", axis=1).isnull() 
 
[/code]

 1. 2. 3. 4. 

Let's plot the entry and exit signals corresponding to the threshold of 80%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-66-1)>>> fig = data.plot(ohlc_trace_kwargs=dict(opacity=0.5))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-66-2)>>> entries[0.8].vbt.signals.plot_as_entries(price, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-66-3)>>> exits[0.8].vbt.signals.plot_as_exits(price, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-66-4)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/patsim_signals.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/patsim_signals.dark.svg#only-dark)

Apart from a few failed regular and inverted double top patterns, our indicator does great. By further tweaking the pattern similarity parameters and choosing a somewhat more strict pattern configuration, we could easily filter out most failed patterns.


# Search[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#search "Permanent link")

Searching for patterns of a variable length using indicators with a parametrizable window is expensive: each window would require allocation of an array of _at least_ the same shape as the entire price array. We need a more compressed representation of a pattern search result. Gladly, the vectorbt's native support for record arrays makes exactly this possible! 

The procedural logic is implemented by the Numba-compiled function [find_pattern_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.find_pattern_1d_nb) and its two-dimensional version [find_pattern_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.find_pattern_nb). The idea is the following: iterate over the rows of a price array, and at each row, iterate over a range of windows headed forward/backward. For each window, run the [pattern_similarity_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/patterns/#vectorbtpro.generic.nb.patterns.pattern_similarity_nb) function to get the similarity score. If the score passes all requirements and thus is not NaN, create a NumPy record of the type [pattern_range_dt](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.pattern_range_dt), which stores the start index (including), the end index (excluding or including if it's the last index), and the similarity score. This record gets appended to a record array and returned to the user. The function is capable of selecting rows and windows randomly given a certain probability to decrease the number of candidates, and handling overlapping pattern ranges. Also, it's incredibly time and memory efficient ![⚡](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/26a1.svg)

Let's search for the pattern we defined above by rolling a window of the size from 30 to 90, and requiring the similarity score to be at least 85%:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-1)>>> pattern_range_records = vbt.nb.find_pattern_1d_nb(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-2)... price.values, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-3)... pattern,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-4)... window=30, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-5)... max_window=90,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-6)... error_type=vbt.enums.ErrorType.Relative,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-7)... max_error=np.array([0.05]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-8)... max_error_interp_mode=vbt.enums.InterpMode.Discrete,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-9)... min_similarity=0.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-11)>>> pattern_range_records
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-67-12)array([(0, 0, 270, 314, 1, 0.86226468), (1, 0, 484, 540, 1, 0.89078042)])
 
[/code]

 1. 2. 3. 

The call returned two records, with 86% and 89% (!) similarity respectively. The first window is `314 - 270 = 44` data points long, the second `540 - 484 = 56`. Let's plot the second fit by also plotting what happened for 30 bars after the pattern:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-1)>>> start_row = pattern_range_records[1]["start_idx"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-2)>>> end_row = pattern_range_records[1]["end_idx"]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-3)>>> fig = data.iloc[start_row:end_row + 30].plot(plot_volume=False)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-4)>>> price.iloc[start_row:end_row].vbt.plot_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-5)... pattern, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-6)... error_type="relative",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-7)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-8)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-9)... plot_obj=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-10)... fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-68-12)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/find_pattern.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/find_pattern.dark.svg#only-dark)

Voilà, it's the same pattern we processed at the beginning of this tutorial! This example should signify how important it is to test a dense grid of windows to find optimal matches. As opposed to the [PATSIM](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/patsim/#vectorbtpro.indicators.custom.patsim.PATSIM) indicator, this approach consumes almost no memory, and implements a range of tricks to make the calculation faster, such as pre-calculating the price's expanding minimum and maximum values.

As always, using the raw Numba-compiled function is all fun and games until you meet a more convenient method that wraps it: [PatternRanges.from_pattern_search](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.from_pattern_search). This class method takes all the parameters accepted by [find_pattern_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.find_pattern_1d_nb), builds a grid of parameter combinations, splits the price array into one-dimensional column arrays, and executes each parameter combination on each column array using the function [execute](https://vectorbt.pro/pvt_7a467f6b/api/utils/execution/#vectorbtpro.utils.execution.execute), which allows for both sequential and parallel processing. After processing all the input combinations, the method concatenates the resulting record arrays, and wraps them with the class [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges). This class extends the base class [Ranges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges) with the similarity field and various pattern analysis and plotting methods. Enough theory, let's do the same as above using this method:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-1)>>> pattern_ranges = vbt.PatternRanges.from_pattern_search(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-2)... price, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-3)... pattern,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-4)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-5)... max_window=90,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-6)... error_type="relative", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-7)... max_error=0.05, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-8)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-9)... min_similarity=0.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-11)>>> pattern_ranges
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-69-12)<vectorbtpro.generic.ranges.PatternRanges at 0x7f8bdab039d0>
 
[/code]

 1. 2. 3. 

If the price is a Pandas object, there is also an accessor method [GenericAccessor.find_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericAccessor.find_pattern) that calls the class method above and can save us a few lines:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-2)... pattern,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-3)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-4)... max_window=90,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-5)... error_type="relative",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-6)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-7)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-8)... min_similarity=0.85
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-70-9)... )
 
[/code]

Let's take a look at the records in a human-readable format:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-71-1)>>> pattern_ranges.records_readable
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-71-2) Pattern Range Id Column Start Index \
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-71-3)0 0 0 2021-02-26 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-71-4)1 1 0 2021-09-28 00:00:00+00:00 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-71-5)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-71-6) End Index Status Similarity 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-71-7)0 2021-04-11 00:00:00+00:00 Closed 0.862265 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-71-8)1 2021-11-23 00:00:00+00:00 Closed 0.890780 
 
[/code]

Also, the returned [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges) instance stores the search configuration that was used to generate those records, per column. The property [PatternRanges.search_configs](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.search_configs) returns a list of such configurations, each being an instance of the data class [PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC) (stands for "Pattern Search Config"). There is the same number of search configurations as we have columns.

Hint

Take a look at the [documentation of PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC), it describes in detail each parameter used in pattern search.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-1)>>> pattern_ranges.wrapper.columns
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-2)Int64Index([0], dtype='int64')
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-4)>>> pattern_ranges.search_configs
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-5)[PSC(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-6) pattern=array([1, 2, 3, 2, 3, 2]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-7) window=30, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-8) max_window=120, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-9) row_select_prob=1.0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-10) window_select_prob=1.0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-11) roll_forward=False,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-12) interp_mode=3, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-13) rescale_mode=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-14) vmin=nan, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-15) vmax=nan, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-16) pmin=nan, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-17) pmax=nan, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-18) invert=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-19) error_type=1, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-20) distance_measure=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-21) max_error=array([0.05]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-22) max_error_interp_mode=2, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-23) max_error_as_maxdist=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-24) max_error_strict=False, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-25) min_pct_change=nan, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-26) max_pct_change=nan, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-27) min_similarity=0.85, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-28) max_one_per_row=True,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-29) max_overlap=0, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-30) max_records=None, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-31) name=None
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-72-32))]
 
[/code]

This one configuration instance contains all the argument names and values that were passed to [find_pattern_1d_nb](https://vectorbt.pro/pvt_7a467f6b/api/generic/nb/records/#vectorbtpro.generic.nb.records.find_pattern_1d_nb). Why do we need to keep it? For plotting! Remember how inconvenient it was having to provide to a plotting method the exact same arguments that were used in the similarity calculation. To make things more streamlined, each pattern range instance keeps track of the search configuration for each column to be plotted. The plotting itself is done with the method [PatternRanges.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.plot), which uses the method [Ranges.plot](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.Ranges.plot) for plotting the data and ranges, and the method [GenericSRAccessor.plot_pattern](https://vectorbt.pro/pvt_7a467f6b/api/generic/accessors/#vectorbtpro.generic.accessors.GenericSRAccessor.plot_pattern) for plotting the patterns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-73-1)>>> pattern_ranges.plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/pattern_ranges.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/pattern_ranges.dark.svg#only-dark)

By default, it fills the distance between the price and the pattern (set `fill_distance=False` to hide) and it doesn't display the corridor (set `plot_max_error=True` to show). As any other subclass of [Analyzable](https://vectorbt.pro/pvt_7a467f6b/api/generic/analyzable/#vectorbtpro.generic.analyzable.Analyzable), an instance of [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges) behaves in many regards like a regular Pandas object. For example, we can filter a date range using the regular `loc` and `iloc` operations to zoom in into any pattern programmatically.

Note

When selecting a date range, the indexing operation will filter out all range records that do not _completely_ fall in the new date range. That is, if a pattern range starts on `2020-01-01` and lasts until `2021-01-01`, it will be included in the new pattern range instance if the new date range encompasses that period fully, for example `2019-01-01` to `2021-01-01`, but not `2019-01-01` to `2020-12-31`.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-74-1)>>> pattern_ranges.loc["2021-09-01":"2022-01-01"].plot().show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/pattern_ranges_zoomed.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/pattern_ranges_zoomed.dark.svg#only-dark)

Info

You might have noticed that the bright area is larger than the window by one bar, but also that the green marker is located further away from the last window point. This is because the field `end_idx` represents the excluding end of the range - the first point after the last window point. This is needed to calculate the duration of any range properly. The only exception is when the last window point is the last point in the entire price array: in such a case, the marker will be placed at that point and the range will be marked as open. Open ranges don't mean that the pattern isn't completed though.

Since the entire information is now represented using records, we can query various useful metrics to describe the results:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-1)>>> pattern_ranges.stats()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-2)Start 2020-06-01 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-3)End 2022-05-31 00:00:00+00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-4)Period 730 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-5)Total Records 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-6)Coverage 0.136986
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-7)Overlap Coverage 0.0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-8)Duration: Min 44 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-9)Duration: Median 50 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-10)Duration: Max 56 days 00:00:00
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-11)Similarity: Min 0.862265
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-12)Similarity: Median 0.876523
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-13)Similarity: Max 0.89078
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-75-14)dtype: object
 
[/code]

Here, for example, we see that there are two non-overlapping patterns covering 13.7% of the entire period. We also see various duration and similarity quantiles.


# Overlapping[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#overlapping "Permanent link")

In the example above, we were searching a total of `90 - 30 + 1 = 61` windows at each single row. Why haven't we got any overlapping ranges? Because, by default, overlapping is not allowed. There are two (optional) mechanisms implemented. First, whenever there are multiple windows starting at the same row, the algorithm will select the one with the highest similarity. This means that the number of filled records is always guaranteed to be equal or below the number of rows in the price array. Second, whenever there are multiple consecutive records regardless of whether they start at the same row but with overlapping ranges, the algorithm will also select the one with the highest similarity.

But sometimes, there might be a need to permit overlapping ranges; for example, one pattern might start right before another pattern ends; or, one big pattern might encompass a range of smaller patterns. Such scenarios can be addressed by tweaking the argument `overlap_mode` of the type [OverlapMode](https://vectorbt.pro/pvt_7a467f6b/api/generic/enums/#vectorbtpro.generic.enums.OverlapMode). Setting it to `AllowAll` will disable both mechanisms and append every single record. Setting it to `Allow` will disable the second mechanism while only filtering those ranges that start at the same row. Setting it to `Disallow` will enable both mechanisms (default), while setting it to any other positive integer will treat it as the maximum number of rows any two neighboring ranges are allowed to share.

Important

Setting the argument to `AllowAll` may produce a record array that is bigger than the price array. In such a case, you need to manually increase the number of records to be allocated using `max_records`, for example, `max_records=len(price) * 2`.

Let's allow overlapping ranges as long as they don't start at the same row:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-2)... pattern,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-3)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-4)... max_window=120,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-5)... error_type="relative",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-6)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-7)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-8)... min_similarity=0.85,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-9)... overlap_mode="allow" 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-11)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-12)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-13)16
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-15)>>> pattern_ranges.overlap_coverage
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-76-16)0.9642857142857143
 
[/code]

 1. 

We see that instead of 2, there are now 16 ranges that have been detected. Also, ranges overlap by 96%, which means that there are probably no ranges that don't share rows with other ranges. Let's visualize the entire thing:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-77-1)>>> pattern_ranges.plot(plot_zones=False, plot_patterns=False).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/pattern_ranges_overlap.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/pattern_ranges_overlap.dark.svg#only-dark)

As shown in the graph, there are only two global matches, each being confirmed by windows of varying lengths. If we set `overlap_mode="disallow"`, only the most similar windows in each region would remain.

Info

There is an argument that controls the direction in which windows are rolled - `roll_forward`. If this argument is `False` (default), ranges will be sorted by the end index and may have multiple records pointing to the same start index. Otherwise, ranges will be sorted by the start index and may have multiple records pointing to the same end index.


# Random selection[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#random-selection "Permanent link")

Sometimes, not every row and window combination is worth searching. If the input data is too big, or there are too many parameter combinations involved, the search would take ages to complete in vectorbt's terms (it would still be incredibly fast though!). To make searchable regions more sparse, we can introduce a probability of picking a certain row/window. For instance, if the probability is `0.5`, the algorithm would search every second row/window on average. Let's set a probability of 50% for rows and 25% for windows, and benchmark the execution to see whether it would make the execution 8 times faster on average:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-1)>>> def run_prob_search(row_select_prob, window_select_prob):
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-2)... return price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-3)... pattern,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-4)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-5)... max_window=120,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-6)... row_select_prob=row_select_prob, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-7)... window_select_prob=window_select_prob,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-8)... error_type="relative",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-9)... max_error=0.05,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-10)... max_error_interp_mode="discrete",
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-11)... min_similarity=0.8, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-12)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-13)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-14)>>> %timeit run_prob_search(1.0, 1.0)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-15)111 ms ± 247 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-16)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-17)>>> %timeit run_prob_search(0.5, 0.25)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-78-18)15 ms ± 183 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 
[/code]

 1. 2. 

Just note that, unless you set a random seed (argument `seed`), detected pattern ranges may vary greatly with each method call. Let's run the function `run_prob_search` 100 times and plot the number of filled records:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-79-1)>>> run_prob_search(1.0, 1.0).count() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-79-2)6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-79-3)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-79-4)>>> pd.Series([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-79-5)... run_prob_search(0.5, 0.25).count() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-79-6)... for i in range(100)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-79-7)... ]).vbt.plot().show()
 
[/code]

 1. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/random_selection.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/random_selection.dark.svg#only-dark)

Hint

The lower the selection probabilities are, the less likely you will detect all patterns in a single call, thus always make sure to run the same search multiple times to assess the stability of the detection accuracy.


# Params[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#params "Permanent link")

The beauty of the class method [PatternRanges.search_configs](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.search_configs) is in its ability to behave like a full-blown indicator. It uses the same mechanism for broadcasting and combining parameters as the vectorbt's broadcaster; both are based on the function [combine_params](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.combine_params). To mark any argument as a parameter, we need to wrap it with [Param](https://vectorbt.pro/pvt_7a467f6b/api/utils/params/#vectorbtpro.utils.params.Param). This will have several implications: the parameter will be broadcasted and combined with other parameters, and it will be reflected as a standalone level in the final column hierarchy.

Let's test 4 patterns: "V-Top", "V-Bottom", a rising market and a falling market pattern.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-2)... vbt.Param([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-3)... [1, 2, 1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-4)... [2, 1, 2],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-5)... [1, 2, 3],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-6)... [3, 2, 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-7)... ]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-8)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-9)... max_window=120,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-80-10)... )
 
[/code]

Param 4/4

Since we provided more than one parameter combination, the executor displayed a progress bar. Let's counter the number of found patterns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-81-1)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-81-2)pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-81-3)list_0 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-81-4)list_1 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-81-5)list_2 7
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-81-6)list_3 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-81-7)Name: count, dtype: int64
 
[/code]

We see that the argument `pattern` received four lists. Let's make it more verbose by providing an index that gives each list a name:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-2)... vbt.Param([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-3)... [1, 2, 1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-4)... [2, 1, 2],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-5)... [1, 2, 3],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-6)... [3, 2, 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-7)... ], keys=["v-top", "v-bottom", "rising", "falling"]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-8)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-9)... max_window=120,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-11)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-12)pattern
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-13)v-top 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-14)v-bottom 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-15)rising 7
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-16)falling 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-82-17)Name: count, dtype: int64
 
[/code]

Let's display the three detected falling patterns:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-83-1)>>> pattern_ranges.plot(column="falling").show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/params_falling.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/params_falling.dark.svg#only-dark)

But there are many more falling patterns on the chart, why haven't they been recognized? Because 1) the algorithm searched only regions that are at least 30 bars long, 2) the default minimum similarity threshold is 85%, such that the algorithm picked only those regions that were the most similar to a straight line, and 3) the algorithm removed any overlapping regions.

Now, let's pass multiple parameters. In such a case, their values will be combined to build a Cartesian product of all parameter combinations. Let's additionally test multiple similarity thresholds:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-2)... vbt.Param([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-3)... [1, 2, 1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-4)... [2, 1, 2],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-5)... [1, 2, 3],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-6)... [3, 2, 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-7)... ], keys=["v-top", "v-bottom", "rising", "falling"]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-8)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-9)... max_window=120,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-10)... min_similarity=vbt.Param([0.8, 0.85])
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-12)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-13)pattern min_similarity
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-14)v-top 0.80 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-15) 0.85 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-16)v-bottom 0.80 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-17) 0.85 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-18)rising 0.80 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-19) 0.85 7
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-20)falling 0.80 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-21) 0.85 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-84-22)Name: count, dtype: int64
 
[/code]

We can finally see some detected "V-Bottom" ranges:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-85-1)>>> pattern_ranges.plot(column=("v-bottom", 0.8)).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/params_v_bottom.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/params_v_bottom.dark.svg#only-dark)

What if we didn't want to build a product of some parameters? For instance, what if we wanted to use different window lengths for different patterns? This is possible by providing a level. Parameters that are linked to the same level are not combined, only broadcasted together.
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-2)... vbt.Param([
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-3)... [1, 2, 1],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-4)... [2, 1, 2],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-5)... [1, 2, 3],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-6)... [3, 2, 1]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-7)... ], keys=["v-top", "v-bottom", "rising", "falling"], level=0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-8)... window=vbt.Param([30, 30, 7, 7], level=0), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-9)... max_window=vbt.Param([120, 120, 30, 30], level=0),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-10)... min_similarity=vbt.Param([0.8, 0.85], level=1) 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-11)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-12)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-13)pattern window max_window min_similarity
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-14)v-top 30 120 0.80 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-15) 0.85 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-16)v-bottom 30 120 0.80 3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-17) 0.85 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-18)rising 7 30 0.80 27
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-19) 0.85 23
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-20)falling 7 30 0.80 25
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-21) 0.85 15
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-86-22)Name: count, dtype: int64
 
[/code]

 1. 2. 

Note

If used, level must be provided for all parameters. You can also re-order the column levels of some parameters by assigning them a lower/higher level.


# Configs[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#configs "Permanent link")

It's worth noting that in a case where we have multiple assets, each parameter will be applied on the entire price array. But what if we wanted to search for different patterns in the price of different assets? Remember how each instance of [PatternRanges](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges) keeps track of the search configuration of each individual column in [PatternRanges.search_configs](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.search_configs)? In the same way, we can manually provide search configurations using the argument `search_configs`, which must be provided as a list of [PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC) instances (per entire price), or a list of lists of [PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC) instances (per column). This way, we can define arbitrary parameter combinations.

To better illustrate the usage, let's fetch the price of `BTCUSDT` and `ETHUSDT` symbols, and search for the "Double Top" pattern in both assets, and for any occurrence of the latest 30 bars in each asset individually:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-1)>>> mult_data = vbt.BinanceData.pull(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-2)... ["BTCUSDT", "ETHUSDT"], 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-3)... start="2020-06-01 UTC", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-4)... end="2022-06-01 UTC"
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-5)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-6)>>> mult_price = mult_data.hlc3
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-7)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-8)>>> pattern_ranges = mult_price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-9)... search_configs=[
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-10)... vbt.PSC(pattern=[1, 2, 3, 2, 3, 2], window=30), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-11)... [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-12)... vbt.PSC(pattern=mult_price.iloc[-30:, 0]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-13)... vbt.PSC(pattern=mult_price.iloc[-30:, 1]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-14)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-15)... ],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-16)... min_similarity=0.8 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-18)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-19)search_config symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-20)0 BTCUSDT 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-21)1 ETHUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-22)2 BTCUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-23)3 ETHUSDT 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-87-24)Name: count, dtype: int64
 
[/code]

 1. 2. 3. 

Hint

We can provide arguments to [PSC](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PSC) in a human-readable format. Each config will be prepared for the use in Numba automatically.

We see that the column hierarchy now contains two levels: the identifier of the search config, and the column name. Let's make it more verbose by choosing a name for each config:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-1)>>> pattern_ranges = mult_price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-2)... search_configs=[
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-3)... vbt.PSC(pattern=[1, 2, 3, 2, 3, 2], window=30, name="double_top"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-4)... [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-5)... vbt.PSC(pattern=mult_price.iloc[-30:, 0], name="last"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-6)... vbt.PSC(pattern=mult_price.iloc[-30:, 1], name="last"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-7)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-8)... ],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-9)... min_similarity=0.8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-10)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-11)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-12)search_config symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-13)double_top BTCUSDT 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-14) ETHUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-15)last BTCUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-16) ETHUSDT 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-88-17)Name: count, dtype: int64
 
[/code]

We can also combine search configurations and parameters. In this case, the method will clone the provided search configurations by the number of parameter combinations, and override the parameters of each search configuration by the current parameter combination. Let's test various rescaling modes:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-1)>>> pattern_ranges = mult_price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-2)... search_configs=[
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-3)... vbt.PSC(pattern=[1, 2, 3, 2, 3, 2], window=30, name="double_top"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-4)... [
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-5)... vbt.PSC(pattern=mult_price.iloc[-30:, 0], name="last"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-6)... vbt.PSC(pattern=mult_price.iloc[-30:, 1], name="last"),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-7)... ]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-8)... ],
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-9)... rescale_mode=vbt.Param(["minmax", "rebase"]),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-10)... min_similarity=0.8,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-11)... open=mult_data.open, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-12)... high=mult_data.high,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-13)... low=mult_data.low,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-14)... close=mult_data.close,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-15)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-16)>>> pattern_ranges.count()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-17)rescale_mode search_config symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-18)minmax double_top BTCUSDT 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-19) ETHUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-20) last BTCUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-21) ETHUSDT 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-22)rebase double_top BTCUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-23) ETHUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-24) last BTCUSDT 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-25) ETHUSDT 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-89-26)Name: count, dtype: int64
 
[/code]

 1. 

For example, our search for a pattern based on the 30 last bars in `ETHUSDT` found 8 occurrences similar by shape (min-max rescaling) and only 2 occurrences similar by shape and percentage change (rebasing):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-90-1)>>> pattern_ranges.plot(column=("rebase", "last", "ETHUSDT")).show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/configs_and_params.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/configs_and_params.dark.svg#only-dark)

The first range has the similarity of 85%, while the second range is still open and has the similarity of 100%, which makes sense because it was used as a pattern.

Note

Again, open range doesn't mean that it hasn't finished developing - it only means that the last point in the range is the last point in the price array such that the duration can be calculated correctly.


# Mask[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#mask "Permanent link")

So, how do we use a pattern range instance to generate signals? Since such an instance usually stores only ranges that passed a certain similarity threshold, we only need to know whether there is any range that closes at a particular row and column. Such a mask can be generated by calling the property [PatternRanges.last_pd_mask](https://vectorbt.pro/pvt_7a467f6b/api/generic/ranges/#vectorbtpro.generic.ranges.PatternRanges.last_pd_mask):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-1)>>> mask = pattern_ranges.last_pd_mask
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-2)>>> mask.sum() 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-3)rescale_mode search_config symbol 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-4)minmax touble_top BTCUSDT 6
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-5) ETHUSDT 4
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-6) last BTCUSDT 5
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-7) ETHUSDT 8
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-8)rebase touble_top BTCUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-9) ETHUSDT 0
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-10) last BTCUSDT 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-11) ETHUSDT 2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-91-12)dtype: int64
 
[/code]

 1. 

We can then use this mask, for example, in [Portfolio.from_signals](https://vectorbt.pro/pvt_7a467f6b/api/portfolio/base/#vectorbtpro.portfolio.base.Portfolio.from_signals).


# Indicator[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#indicator_1 "Permanent link")

If we don't care about plotting and analyzing pattern ranges, we can use the same [PATSIM](https://vectorbt.pro/pvt_7a467f6b/api/indicators/custom/patsim/#vectorbtpro.indicators.custom.patsim.PATSIM) indicator that we used previously to generate a Series/DataFrame with similarity scores. What we didn't discuss previously though is that this indicator also takes the arguments `max_window`, `row_select_prob`, and `window_select_prob`. Let's prove that the indicator produces the same similarity scores as pattern ranges:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-1)>>> pattern_ranges = price.vbt.find_pattern(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-2)... pattern,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-3)... window=30,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-4)... max_window=120,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-5)... row_select_prob=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-6)... window_select_prob=0.5,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-7)... overlap_mode="allow", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-8)... seed=42
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-9)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-10)>>> pr_mask = pattern_ranges.map_field(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-11)... "similarity", 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-12)... idx_arr=pattern_ranges.last_idx.values
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-13)... ).to_pd()
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-14)>>> pr_mask[~pr_mask.isnull()]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-15)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-16)2021-03-23 00:00:00+00:00 0.854189
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-17)2021-03-26 00:00:00+00:00 0.853817
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-18)2021-04-10 00:00:00+00:00 0.866913
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-19)2021-04-11 00:00:00+00:00 0.866106
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-20)2021-11-17 00:00:00+00:00 0.868276
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-21)2021-11-18 00:00:00+00:00 0.873757
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-22)2021-11-21 00:00:00+00:00 0.890225
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-23)2021-11-23 00:00:00+00:00 0.892541
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-24)2021-11-24 00:00:00+00:00 0.879475
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-25)2021-11-26 00:00:00+00:00 0.877245
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-26)2021-11-27 00:00:00+00:00 0.872172
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-27)dtype: float64
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-28)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-29)>>> patsim = vbt.PATSIM.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-30)... price,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-31)... vbt.Default(pattern), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-32)... window=vbt.Default(30),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-33)... max_window=vbt.Default(120),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-34)... row_select_prob=vbt.Default(0.5),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-35)... window_select_prob=vbt.Default(0.5),
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-36)... min_similarity=vbt.Default(0.85), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-37)... seed=42
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-38)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-39)>>> ind_mask = patsim.similarity
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-40)>>> ind_mask[~ind_mask.isnull()]
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-41)Open time
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-42)2021-03-23 00:00:00+00:00 0.854189
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-43)2021-03-26 00:00:00+00:00 0.853817
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-44)2021-04-10 00:00:00+00:00 0.866913
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-45)2021-04-11 00:00:00+00:00 0.866106
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-46)2021-11-17 00:00:00+00:00 0.868276
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-47)2021-11-18 00:00:00+00:00 0.873757
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-48)2021-11-21 00:00:00+00:00 0.890225
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-49)2021-11-23 00:00:00+00:00 0.892541
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-50)2021-11-24 00:00:00+00:00 0.879475
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-51)2021-11-26 00:00:00+00:00 0.877245
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-52)2021-11-27 00:00:00+00:00 0.872172
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-92-53)dtype: float64
 
[/code]

 1. 2. 3. 


# Combination[¶](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#combination "Permanent link")

We know how to generate signals from one pattern found in one array, but what about a use case where our signals should only be triggered upon a combination of patterns found across different arrays? For example, how do we quantify convergence and divergence? To combine multiple patterns conditionally, we need to combine their similarity scores. For example, below we're searching for a bearish divergence between the high price and MACD:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-1)>>> price_highs = vbt.PATSIM.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-2)... data.high, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-3)... pattern=np.array([1, 3, 2, 4]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-4)... window=40,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-5)... max_window=50
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-6)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-7)>>> macd = data.run("talib_macd").macd 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-8)>>> macd_lows = vbt.PATSIM.run(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-9)... macd, 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-10)... pattern=np.array([4, 2, 3, 1]), 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-11)... window=40,
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-12)... max_window=50
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-13)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-14)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-15)>>> fig = vbt.make_subplots(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-16)... rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-17)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-18)>>> fig.update_layout(height=500)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-19)>>> data.high.rename("Price").vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-20)... add_trace_kwargs=dict(row=1, col=1), fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-21)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-22)>>> macd.rename("MACD").vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-23)... add_trace_kwargs=dict(row=2, col=1), fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-24)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-25)>>> price_highs.similarity.rename("Price Sim").vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-26)... add_trace_kwargs=dict(row=3, col=1), fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-27)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-28)>>> macd_lows.similarity.rename("MACD Sim").vbt.plot(
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-29)... add_trace_kwargs=dict(row=3, col=1), fig=fig
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-30)... )
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-93-31)>>> fig.show()
 
[/code]

 1. 2. 3. 

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/macd_divergence.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/macd_divergence.dark.svg#only-dark)

Upon looking at the chart, we can confirm that the selected parameters accurately represent the events we are looking for - the regions where the price and MACD is rising and falling respectively also leads to the rise of their similarity score. We also can derive the optimal similarity threshold that would yield a moderate amount of crossovers - 80%. In addition, the points where the price's similarity line crosses the threshold often happens slightly before the MACD's, thus it's insufficient to simply test whether both crossovers happen at the same time - we need to introduce a waiting time using the rolling "any" operation. Below, for example, we get an exit signal if both similarities crossed the threshold during the last 10 bars, and not necessarily at the same time:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-94-1)>>> cond1 = (price_highs.similarity >= 0.8).vbt.rolling_any(10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-94-2)>>> cond2 = (macd_lows.similarity >= 0.8).vbt.rolling_any(10)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-94-3)>>> exits = cond1 & cond2
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-94-4)>>> fig = data.plot(ohlc_trace_kwargs=dict(opacity=0.5))
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-94-5)>>> exits.vbt.signals.plot_as_exits(data.close, fig=fig)
 [](https://vectorbt.pro/pvt_7a467f6b/tutorials/patterns-and-projections/patterns/#__codelineno-94-6)>>> fig.show()
 
[/code]

![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/macd_divergence_exits.light.svg#only-light) ![](https://vectorbt.pro/pvt_7a467f6b/assets/images/tutorials/patterns/macd_divergence_exits.dark.svg#only-dark)

Fore more ideas, take a look into [Signal Development](https://vectorbt.pro/pvt_7a467f6b/tutorials/signal-development).

[ Python code](https://vectorbt.pro/pvt_7a467f6b/assets/jupytext/tutorials/patterns-and-projections/patterns.py.txt) [ Notebook](https://github.com/polakowo/vectorbt.pro/blob/main/notebooks/PatternsProjections.ipynb)