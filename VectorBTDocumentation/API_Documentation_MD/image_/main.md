image_

#  image_ module[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/image_.py "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#vectorbtpro.utils.image_ "Permanent link")

Utilities for images.

* * *

## hstack_image_arrays function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/image_.py#L23-L30 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#vectorbtpro.utils.image_.hstack_image_arrays "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-0-1)hstack_image_arrays(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-0-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-0-3)    b
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-0-4))
    

Stack NumPy images horizontally.

* * *

## save_animation function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/image_.py#L43-L134 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#vectorbtpro.utils.image_.save_animation "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-1)save_animation(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-2)    fname,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-3)    index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-4)    plot_func,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-5)    *args,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-6)    delta=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-7)    step=1,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-8)    fps=3,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-9)    writer_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-10)    show_progress=True,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-11)    pbar_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-12)    to_image_kwargs=None,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-13)    **kwargs
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-1-14))
    

Save animation to a file.

**Args**

**`fname`** : `str`
    File name.
**`index`** : `sequence`
    Index to iterate over.
**`plot_func`** : `callable`
    

Plotting function.

Must take subset of `index`, `*args`, and `**kwargs`, and return either a Plotly figure, image that can be read by `imageio.imread`, or a NumPy array.

**`*args`**
    Positional arguments passed to `plot_func`.
**`delta`** : `int`
    Window size of each iteration.
**`step`** : `int`
    Step of each iteration.
**`fps`** : `int`
    

Frames per second.

Will be translated to `duration` by `1000 / fps`.

**`writer_kwargs`** : `dict`
    Keyword arguments passed to `imageio.get_writer`.
**`show_progress`** : `bool`
    Whether to show the progress bar.
**`pbar_kwargs`** : `dict`
    Keyword arguments passed to [ProgressBar](https://vectorbt.pro/pvt_7a467f6b/api/utils/pbar/#vectorbtpro.utils.pbar.ProgressBar "vectorbtpro.utils.pbar.ProgressBar").
**`to_image_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.to_image`.
**`**kwargs`**
    Keyword arguments passed to `plot_func`.

**Usage**
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-1)>>> from vectorbtpro import *
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-2)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-3)>>> def plot_data_window(index, data):
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-4)...     return data.loc[index].plot()
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-5)
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-6)>>> data = vbt.YFData.pull("BTC-USD", start="2020", end="2021")
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-7)>>> vbt.save_animation(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-8)...     "plot_data_window.gif",
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-9)...     data.index,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-10)...     plot_data_window,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-11)...     data,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-12)...     delta=90,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-13)...     step=10
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-2-14)... )
    

* * *

## vstack_image_arrays function[](https://github.com/polakowo/vectorbt.pro/blob/6e344a8230eaf718593f4570378486ee1d4178f6/vectorbtpro/utils/image_.py#L33-L40 "Jump to source")[¶](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#vectorbtpro.utils.image_.vstack_image_arrays "Permanent link")
    
    
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-3-1)vstack_image_arrays(
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-3-2)    a,
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-3-3)    b
    [](https://vectorbt.pro/pvt_7a467f6b/api/utils/image_/#__codelineno-3-4))
    

Stack NumPy images vertically.
