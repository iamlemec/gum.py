# gum visualization

from itertools import cycle

from .gen import C, prefix_split, Var, Vars, Gum, Box, DataPath, Plot
from .gum import display

##
## themes
##

DEFAULT_PLOT = {
    'aspect': 2,
    'grid': True,
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

def plot(frame, show=True, **kwargs0):
    import numpy as np
    import pandas as pd

    # collect arguments
    kwargs = { **DEFAULT_PLOT, **kwargs0 }
    (line_args, display_args), plot_args = prefix_split(('line', 'display'), kwargs)

    # convert to dataframe
    if isinstance(frame, (np.ndarray, list, tuple)):
        frame = pd.Series(frame, name='value')
    if isinstance(frame, pd.Series):
        frame = frame.to_frame()

    # value setters
    index = Var.from_series(frame.index, name='index')
    vars = Vars.from_dataframe(frame)
    vars1 = Vars(index=index, **vars)

    # data plotters
    lines = [
        DataPath(xvals=index, yvals=vars[v], **{'stroke': c, **line_args})
        for v, c in zip(vars, cycle(COLORS))
    ]

    # generate svg code
    plot = Plot(lines, **plot_args)

    # render svg
    if show:
        code = Gum(plot, vars=vars1)
        display(code, **display_args)
    else:
        return plot, vars1
