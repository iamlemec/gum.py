<div align="center">
<h1>gum.py</h1>
<p>Python bindings for the gum visualization language</p>
</div>

A Python wrapper for [gum.js](https://github.com/CompendiumLabs/gum.js), a language for creating visualizations using a React-like JSX dialect that evaluates to SVG. Designed for general graphics, plots, graphs, and network diagrams.

Head to **[compendiumlabs.ai/gum](https://compendiumlabs.ai/gum)** for a live demo and documentation on the underlying gum.js library.

# Installation

```bash
pip install gum
```

Requires Node.js to be installed for the gum.js backend.

# Usage

Create visualizations using Python syntax that generates JSX:

```python
import gum
from gum import C
from gum.gen import Plot, SymLine

# Create a simple sine wave plot
plot = Plot(
    SymLine(fy=C.sin, stroke=C.blue, stroke_width=2),
    xlim=(0, 2*C.pi), ylim=(-1, 1), grid=True, margin=0.2, aspect=2,
)

# Display in terminal (requires chafa)
gum.display(plot) # or just `plot` if you're in IPython or Jupyter

# Or get the SVG string
svg = gum.evaluate(plot)

# Or get the JSX code
jsx = str(plot)
```

If you're in IPython or Jupyter, you don't even need to call `display`. Just type `plot` and it will automatically display the visualization inline.

## Pandas Integration

Plot DataFrames directly with high-level functions:

```python
import pandas as pd
import numpy as np
from gum import lines, points, bars

# Line plot from DataFrame
th = np.linspace(0, 2*np.pi, 100)
df = pd.DataFrame({ 'sin': np.sin(th), 'cos': np.cos(th) })
lines(df, margin=0.15)

# Bar chart from Series
bars(pd.Series({'A': 3, 'B': 8, 'C': 5}))
```

## Symbolic Expressions

Use `C` for constants and `V` for variables:

```python
from gum import C, V
from gum.gen import Plot, SymLine, SymPoints

# C references gum.js constants and functions
C.sin, C.cos, C.pi, C.blue, C.red

# Build symbolic expressions
decay = lambda x: C.exp(-x/2) * C.sin(3*x)

# V creates named variables bound to data
theta = V.theta(np.linspace(0, 2*np.pi, 100))
```

# CLI

Display gum visualizations directly in the terminal using `chafa`. Requires a terminal with image support, such as `ghostty`.

```bash
# Run a built-in demo
python -m gum -d plot -s 50

# Pipe JSX code
cat input.jsx | python -m gum
```

CLI options:

| Option | Description | Default |
|--------|-------------|---------|
| `-d, --demo <name>` | Run a named demo | - |
| `-s, --size <size>` | Terminal display size | 50 |
| `-t, --theme <theme>` | Theme: `light` or `dark` | dark |

Available demos: `plot`, `barplot`, `network`, `symline`, `grid`, `stack`, `text`, and more (see `gum/dem.py`).

# Jupyter Support

`gum.py` automatically renders SVG in IPython console and Jupyter notebooks:

```python
from gum import Plot, SymLine, C

# This will display inline in Jupyter
Plot(
    SymLine(fy=C.sin),
    xlim=(0, 2*C.pi), ylim=(-1, 1), grid=True,
)
```

# Components

gum.py wraps all gum.js components. Key ones include:

**Layout**: `Box`, `Frame`, `Stack`, `HStack`, `VStack`, `Grid`, `Points`

**Shapes**: `Rect`, `Ellipse`, `Circle`, `Line`, `Shape`, `Spline`

**Text**: `Text`, `TextFrame`, `Latex`, `Equation`

**Plotting**: `Plot`, `Graph`, `Axis`, `HAxis`, `VAxis`, `BarPlot`

**Symbolic**: `SymLine`, `SymPoints`, `SymShape`, `SymSpline`, `SymFill`, `SymField`

**Network**: `Node`, `Edge`, `Network`, `Arrow`

See the [gum.js documentation](https://compendiumlabs.ai/gum) for detailed component reference.
