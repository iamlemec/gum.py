# gum visualization

from .gen import C, prefix_split, Variable, Box, DataPath, Plot
from .gum import display

##
## themes
##

DEFAULT = {
    'grid': True,
    'aspect': 2,
    'margin': (0.2, 0.15),
    'line_stroke': C.blue,
    'line_stroke_width': 2,
}

THEMES = {
    'dark': {
        'grid_stroke': C.white,
        'axis_stroke': C.white,
        'axis_label_color': C.white,
    },
    'light': {
        'box_fill': C.white,
        'box_rounded': 0.025,
        'box_margin': 0.05,
    },
}

##
## plotting interface
##

def test_data():
    import math
    import numpy as np
    import pandas as pd
    df = pd.DataFrame({ 'theta': np.linspace(0, 2 * math.pi, 100) })
    df['sin'] = np.sin(df['theta'])
    df['cos'] = np.cos(df['theta'])
    return df.set_index('theta')

def plot(frame, size=75, theme='dark', pixels=None, format=None, show=True, **kwargs0):
    # collect arguments
    kwargs = { **DEFAULT, **THEMES[theme], **kwargs0 }
    (line_args, box_args), plot_args = prefix_split(('line', 'box'), kwargs)

    # value setters
    index = Variable(frame.index.name or 'index', frame.index.tolist())
    value = [ Variable(col, frame[col].tolist()) for col in frame.columns ]
    header = '\n'.join([ index.define(), *[ v.define() for v in value ] ])

    # data plotters
    lines = [ DataPath(xvals=index, yvals=v, **line_args) for v in value ]
    plot = Plot(lines, **plot_args)
    box = Box(plot, **box_args)

    # generate svg code
    code = f'{header}\n\nreturn {box}'

    # render svg
    if show:
        display(code, size=size, pixels=pixels, format=format)
    else:
        return code
