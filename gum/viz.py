# gum visualization

from itertools import cycle
import numpy as np
import pandas as pd

from .gen import C, prefix_split, Var, Vars, Gum, Box, DataPath, Plot
from .gum import display

##
## themes
##

DEFAULT = {
    'aspect': 2,
    'margin': (0.2, 0.15),
    'line_stroke_width': 2,
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
    df = pd.DataFrame({ 'theta': np.linspace(0, 2 * np.pi, 100) })
    df['sin'] = np.sin(df['theta'])
    df['cos'] = np.cos(df['theta'])
    return df.set_index('theta')

def test_brown(N=3, T=100):
    return pd.DataFrame({
        f'stock_{i}': np.random.randn(T).cumsum() / np.sqrt(T) for i in range(N)
    })

def plot(frame, size=None, pixels=None, format=None, method=None, show=True, **kwargs0):
    # collect arguments
    kwargs = { **DEFAULT, **kwargs0 }
    line_args, plot_args = prefix_split('line', kwargs)

    # convert to dataframe
    if isinstance(frame, (np.ndarray, list, tuple)):
        frame = pd.Series(frame, name='value')
    if isinstance(frame, pd.Series):
        frame = frame.to_frame()

    # value setters
    index = Var.from_series(frame.index, name='index')
    vars = Vars.from_dataframe(frame)

    # data plotters
    lines = [
        DataPath(xvals=index, yvals=vars[v], **{'stroke': c, **line_args})
        for v, c in zip(vars, cycle(COLORS))
    ]

    # generate svg code
    plot = Plot(lines, **plot_args)
    code = Gum(plot, vars=[index, vars])

    # render svg
    if show:
        display(code, size=size, pixels=pixels, format=format, method=method)
    else:
        return plot, [index, vars]
