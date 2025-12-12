# gum visualization

from itertools import cycle

from .gen import C, prefix_split, GumData, Gum, DataPath, DataPoints, Plot, BarPlot, VBar
from .gum import display

##
## themes
##

DEFAULT_BASE = {
    'aspect': 2,
    'margin': (0.2, 0.15),
}

DEFAULT_PLOT = {
    **DEFAULT_BASE,
    'grid': True,
    'line_stroke_width': 2,
}

DEFAULT_BARS = {
    **DEFAULT_BASE,
    'bar_border': 0,
    'bar_rounded': True,
    'bar_fill': '#888',
    'bar_fill_opacity': 0.5,
}

COLORS = [
    C.blue,
    C.green,
    C.red,
    C.yellow,
    C.purple,
    C.orange,
]

##
## plotting interface
##

def test_trig():
    import numpy as np
    import pandas as pd
    df = pd.DataFrame({ 'theta': np.linspace(0, 2 * np.pi, 100) })
    df['sin'] = np.sin(df['theta'])
    df['cos'] = np.cos(df['theta'])
    return df.set_index('theta')

def test_brown(N=3, T=100):
    import numpy as np
    import pandas as pd
    return pd.DataFrame({
        f'stock_{i}': np.random.randn(T).cumsum() / np.sqrt(T) for i in range(N)
    })

def ensure_series(data):
    import numpy as np
    import pandas as pd
    if isinstance(data, (np.ndarray, list, tuple, dict)):
        data = pd.Series(data, name='value')
    if not isinstance(data, pd.Series):
        raise ValueError(f'Unsupported type: {type(data)}')
    return data

def ensure_frame(data):
    import numpy as np
    import pandas as pd
    if isinstance(data, (np.ndarray, list, tuple)):
        data = pd.DataFrame({ 'value': data })
    elif isinstance(data, dict):
        data = pd.DataFrame({ k: ensure_series(v) for k, v in data.items() })
    elif isinstance(data, pd.Series):
        data = data.to_frame()
    if not isinstance(data, pd.DataFrame):
        raise ValueError(f'Unsupported type: {type(data)}')
    return data

def lines(frame, show=True, **kwargs0):
    # collect arguments
    kwargs = { **DEFAULT_PLOT, **kwargs0 }
    (line_args, display_args), plot_args = prefix_split(('line', 'display'), kwargs)

    # convert to dataframe
    frame = ensure_frame(frame)
    data = GumData.from_frame(frame)

    # data plotters
    lines = [
        DataPath(xvals=data.index, yvals=v, **{'stroke': c, **line_args})
        for v, c in zip(data, cycle(COLORS))
    ]

    # generate svg code
    plot = Plot(lines, **plot_args)

    # render svg
    if show:
        code = Gum(plot, vars=data)
        display(code, **display_args)
    else:
        return plot, data

def points(frame, show=True, **kwargs0):
    # collect arguments
    kwargs = { **DEFAULT_PLOT, **kwargs0 }
    (point_args, display_args), plot_args = prefix_split(('point', 'display'), kwargs)

    # convert to dataframe
    frame = ensure_frame(frame)
    data = GumData.from_frame(frame)

    # data plotters
    points = [
        DataPoints(xvals=data.index, yvals=v, **{'stroke': c, 'fill': c, **point_args})
        for v, c in zip(data, cycle(COLORS))
    ]

    # generate svg code
    plot = Plot(points, **plot_args)

    # render svg
    if show:
        code = Gum(plot, vars=data)
        display(code, **display_args)
    else:
        return plot, data

def bars(series, show=True, **kwargs0):
    # collect arguments
    kwargs = { **DEFAULT_BARS, **kwargs0 }
    (bar_args, display_args), plot_args = prefix_split(('bar', 'display'), kwargs)

    # convert to series
    series = ensure_series(series)

    # generate svg code
    bars = [ VBar(label=k, size=v, **bar_args) for k, v in series.items() ]
    plot = BarPlot(*bars, **plot_args)

    # render svg
    if show:
        display(plot, **display_args)
    else:
        return plot
