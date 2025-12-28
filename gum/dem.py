# element demos

import sys
from .gen import C, V
from .gum import display
from . import gen as G

##
## utility functions
##

def linspace(start, stop, num):
    delta = (stop - start) / (num - 1)
    return [ start + i * delta for i in range(num) ]

##
## demo functions
##

def demo_gum():
    return G.Frame(
        G.Text('GUM'),
        padding=True,
        rounded=True,
    )

def demo_element():
    Tri = lambda pos0, pos1, pos2, **attr: G.Polygon(pos0, pos1, pos2, **attr)
    return Tri((0.5, 0.1), (0.9, 0.9), (0.1, 0.9), fill=C.gray)

def demo_box():
    return G.Frame(
        G.Text('hello!'),
        padding=True,
        rounded=True,
        border_stroke_dasharray=5,
    )

def demo_arrays():
    emoji = ['🗻', '🚀', '🐋', '🍉', '🍩']
    return G.Plot(
        *[G.Text(e, pos=[i+1, i+1], rad=0.4) for i, e in enumerate(emoji)],
        xlim=[0, 6],
        ylim=[0, 6],
        xticks=7,
        yticks=7,
        margin=0.15,
    )

def demo_axis():
    emoji = ['🗻', '🚀', '🐳', '🍉', '🍩']
    ticks = C.zip(C.linspace(0, 1, len(emoji)), emoji)
    return G.Box(
        G.HAxis(
            yrect=(0.45, 0.55),
            ticks=ticks,
            tick_side='outer',
            label_size=1,
        ),
        padding=True,
    )

def demo_barplot():
    return G.BarPlot(
        G.Bar(label='A', size=3, fill=C.red),
        G.Bar(label='B', size=8.5, fill=C.blue),
        G.Bar(label='C', size=6.5, fill=C.green),
        ylim=[0, 10],
        yticks=6,
        title='Example BarPlot',
        xlabel='Category',
        ylabel='Value',
        bar_rounded=True,
        bar_border=0,
        margin=0.25,
    )

def demo_colors():
    func = lambda x: -C.sin(x)
    pal = V.pal(C.palette(C.blue, C.red, (-1, 1)))
    shape_func = lambda x, y: G.Circle(fill=C.pal(y))
    size_func = lambda x, y: 0.1 * (1 + C.abs(y)) / 2
    xticks = [(x*C.pi, f'{x:.2g} π') for x in linspace(0, 2, 6)[1:]]
    plot = G.Plot(
        G.DataPath(fy=func),
        G.DataPoints(shape_func, fy=func, size=size_func, N=21),
        xlim=(0, 2*C.pi),
        ylim=(-1, 1),
        aspect=1.5,
        xanchor=0,
        xaxis_tick_side='both',
        xticks=xticks,
        grid=True,
        xlabel='phase',
        ylabel='amplitude',
        title='Inverted Sine Wave',
        margin=0.25,
    )
    return G.Gum(plot, vars=[pal])

def demo_datafield():
    return G.Frame(
        G.DataField(
            func=lambda x, y: 100 * x * y,
            xlim=(0, 1),
            ylim=(0, 1),
            N=15,
            stroke_width=2,
        ),
        rounded=0.02,
        margin=True,
        padding=0.075,
        border=2,
        fill=True,
    )

def demo_datafill():
    decay = lambda x: C.exp(-0.1*x) * C.sin(x)
    return G.Graph(
        G.DataFill(fy1=decay, fy2=0, fill=C.blue, fill_opacity=0.5, N=250),
        G.DataPath(fy=decay, N=250),
        xlim=(0, 6*C.pi),
        ylim=(-1, 1),
        aspect=C.phi,
    )

def demo_datapath():
    return G.Plot(
        G.DataPath(fy=C.sin, stroke=C.red, stroke_width=2),
        G.DataPath(fy=lambda x: C.sin(x) + 0.2*C.sin(5*x), stroke=C.blue, stroke_width=2),
        xlim=(0, 2*C.pi),
        ylim=(-1.5, 1.5),
        aspect=C.phi,
        margin=0.2,
        grid=True,
    )

def demo_datapoints():
    return G.Plot(
        G.DataPath(fy=C.sin, stroke=C.blue, stroke_width=2),
        G.DataPoints(
            lambda x, y: G.Rect(fill=C.white, rounded=0.3, aspect=2, spin=-C.r2d*C.atan(C.cos(x))),
            fy=C.sin,
            size=0.125,
            N=11,
        ),
        xlim=(0, 2*C.pi),
        ylim=(-1.5, 1.5),
        fill=True,
        grid=True,
        clip=True,
        margin=[0.25, 0.1],
    )

def demo_datapoly():
    freq, amp = 5, 0.25
    famp = lambda t: 1 + amp * C.sin(freq * t)
    fx = lambda t: famp(t) * C.cos(t)
    fy = lambda t: famp(t) * C.sin(t)
    return G.Frame(
        G.Graph(
            G.DataPoly(fx=fx, fy=fy, tlim=(0, 2*C.pi), N=500, fill=C.blue, opacity=0.75),
            xlim=(-1.5, 1.5),
            ylim=(-1.5, 1.5),
        ),
        rounded=True,
        fill=True,
    )

def demo_edge():
    return G.Network(
        G.TextNode('Hello', label='hello', pos=(0.25, 0.25)),
        G.TextNode('World!', label='world', pos=(0.75, 0.75)),
        G.Edge(node1='hello', node2='world', arrow1_fill=C.red, arrow2_fill=C.blue),
        # node_fill=C.gray,
        edge_arrow=True,
    )

def demo_ellipse():
    return G.Group(
        G.Ellipse(pos=(0.3, 0.2), rad=(0.2, 0.1)),
        G.Ellipse(pos=(0.6, 0.6), rad=(0.2, 0.25)),
    )

def demo_graph():
    return G.Graph(
        G.DataPoints(
            lambda x, y: G.Square(rounded=True, spin=C.r2d*x),
            fy=C.sin,
            xlim=(0, 2*C.pi),
            size=0.5,
            N=150,
        ),
        padding=(0.2, 0.4),
    )

def demo_grid():
    return G.Frame(
        G.Grid(
            *[
                G.Frame(
                    G.Group(
                        G.Arrow(direc=0, tail=1, pos=(1, 0.5), rad=0.5),
                        aspect=1,
                        spin=th,
                    ),
                    padding=True,
                    rounded=True,
                    fill=True,
                )
                for th in linspace(0, 360, 10)[:9]
            ],
            rows=3,
            spacing=True,
        ),
        padding=True,
        rounded=True,
    )

def demo_group():
    return G.Group(
        G.Rect(pos=(0.3, 0.3), rad=0.1, spin=15),
        G.Ellipse(pos=(0.7, 0.7), rad=0.1),
    )

def demo_latex():
    return G.VStack(
        G.TextFrame(G.Equation('\\int_0^{\\infty} \\exp(-x^2) dx = \\sqrt{\\pi}')),
        G.TextFrame(G.Equation('\\sin^2(\\theta) + \\cos^2(\\theta) = 1')),
        spacing=True,
    )

def demo_line():
    return G.Frame(
        G.Line(pos1=(0, 0), pos2=(1, 1)),
    )

def demo_math():
    return G.Frame(
        G.Plot(
            G.DataPath(fy=lambda x: C.exp(C.sin(x))),
            aspect=C.phi,
            xlim=(0, 2*C.pi),
            ylim=(0, 3),
            grid=True,
        ),
        margin=0.15,
    )

def demo_network():
    return G.Network(
        G.TextNode('Hello world', label='hello', pos=(0.25, 0.5), wrap=3),
        G.TextNode('This is a test of wrapping capabilities', label='test', pos=(0.75, 0.25), wrap=6),
        G.Node(G.Ellipse(aspect=1.5, fill=C.blue), label='ball', pos=(0.75, 0.75)),
        G.Edge(node1='hello', node2='test'),
        G.Edge(node1='hello', node2='ball', dir1='s', curve=3),
        aspect=1.5,
        node_yrad=0.15,
        node_rounded=True,
        # node_fill=C.gray,
        edge_arrow_fill=C.white,
    )

def demo_node():
    return G.Network(
        G.TextNode('Hello', label='hello', pos=(0.25, 0.25)),
        G.TextNode('World!', label='world', pos=(0.75, 0.75)),
        G.Edge(node1='hello', node2='world'),
        # node_fill=C.gray,
    )

def demo_plot():
    xticks = [(x*C.pi, f'{x:.2g} π') for x in linspace(0, 2, 6)[1:]]
    return G.Plot(
        G.DataPath(fy=lambda x: -C.sin(x), xlim=(0, 2*C.pi)),
        aspect=C.phi,
        xanchor=0,
        xticks=xticks,
        grid=True,
        xlabel='phase',
        ylabel='amplitude',
        title='Inverted Sine Wave',
        xaxis_tick_side='both',
        grid_stroke_dasharray=3,
        margin=0.25,
    )

def demo_points():
    return G.Plot(
        G.Points([(0, 0.5), (0.5, 0), (-0.5, 0), (0, -0.5)], size=0.02),
        G.Rect(pos=(0.5, 0.5), rad=0.1),
        G.Circle(pos=(-0.5, -0.5), rad=0.1),
        *[G.DataPath(fy=lambda x: C.sin(a*x)) for a in [0.5, 0.9, 1.5]],
        xlim=(-1, 1),
        ylim=(-1, 1),
        margin=0.3,
        grid=True,
        xlabel='time (seconds)',
        ylabel='space (meters)',
        title='Spacetime Vibes',
    )

def demo_polyline():
    return G.Polyline((0.3, 0.3), (0.3, 0.7), (0.7, 0.7), (0.7, 0.3))

def demo_rect():
    return G.Frame(
        G.Rect(pos=(0.25, 0.5), rad=(0.1, 0.2)),
    )

def demo_slide():
    return G.Slide(
        G.Text('Here\'s a plot of a sine wave below. It has to be the right size to fit in with the figure correctly.'),
        G.Plot(
            G.DataPath(fy=C.sin, stroke=C.blue, stroke_width=2),
            xlim=(0, 2*C.pi),
            ylim=(-1.5, 1.5),
            fill=True,
            grid=True,
            margin=(0.25, 0.05),
        ),
        G.Text('It ranges from low to high and has some extra vertical space to allow us to see the full curve.'),
        title='The Art of the Sine Wave',
    )

def demo_stack():
    Donut = lambda: G.Frame(G.Text('🍩'))
    return G.VStack(
        Donut(),
        G.HStack(
            Donut(),
            Donut(),
        ),
    )

def demo_textbox():
    return G.TextBox('hello', border=True, rounded=True, margin=True)

def demo_text():
    return G.TextFrame(
        G.Text('Hello World! You can mix text and '),
        G.Square(rounded=True, fill=C.blue),
        G.Text(' other elements together.'),
        rounded=True,
        wrap=10,
    )

def demo_titleframe():
    emoji = ['🍇', '🥦', '🍔', '🍉', '🍍', '🌽', '🍩', '🥝', '🍟']
    return G.TitleFrame(
        G.Grid(
            *[
                G.Frame(
                    G.Text(e),
                    aspect=True,
                    rounded=True,
                    fill=True,
                    padding=True,
                )
                for e in emoji
            ],
            rows=3,
            spacing=0.05,
        ),
        title='Fruits & Veggies',
        margin=True,
        padding=True,
        rounded=True,
    )

DEMOS = {
    'gum': demo_gum,
    'element': demo_element,
    'box': demo_box,
    'arrays': demo_arrays,
    'axis': demo_axis,
    'barplot': demo_barplot,
    'colors': demo_colors,
    'datafield': demo_datafield,
    'datafill': demo_datafill,
    'datapath': demo_datapath,
    'datapoints': demo_datapoints,
    'datapoly': demo_datapoly,
    'edge': demo_edge,
    'ellipse': demo_ellipse,
    'graph': demo_graph,
    'grid': demo_grid,
    'group': demo_group,
    'latex': demo_latex,
    'line': demo_line,
    'math': demo_math,
    'network': demo_network,
    'node': demo_node,
    'plot': demo_plot,
    'points': demo_points,
    'polyline': demo_polyline,
    'rect': demo_rect,
    'slide': demo_slide,
    'stack': demo_stack,
    'textbox': demo_textbox,
    'text': demo_text,
    'titleframe': demo_titleframe,
}

def demo(name):
    func = DEMOS[name]
    return func()
