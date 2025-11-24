# terminal tools

import json
import requests
import subprocess

##
## chafa interface
##

def readbin(path):
    with open(path, 'rb') as fid:
        return fid.read()

def chafa(data, **kwargs):
    data = readbin(data) if isinstance(data, str) else data
    sargs = sum([
        [ f'--{k}', f'{v}' ] for k, v in kwargs.items() if v is not None
    ], [])
    subprocess.run([ 'chafa', *sargs, '-' ], input=data, stderr=subprocess.DEVNULL)

##
## server interface
##

class Gum:
    def __init__(self, host='localhost', port=3000, pixels=1024, size=25, format='svg', path='../gum.js/src/server.js'):
        args = [ 'node', path, '--host', host, '--port', str(port) ]
        self.server = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.url = f'http://{host}:{port}'
        self.default_format = format
        self.default_pixels = pixels
        self.default_size = size

    def __del__(self):
        self.server.terminate()

    def evaluate(self, code, pixels=None):
        pixels1 = self.default_pixels if pixels is None else pixels
        url = f'{self.url}/evaluate?size={pixels1}'
        headers = { 'Content-Type': 'text/plain' }
        response = requests.post(url, data=code, headers=headers)
        return response.text

    def render(self, code, pixels=None):
        pixels1 = self.default_pixels if pixels is None else pixels
        url = f'{self.url}/render?size={pixels1}'
        headers = { 'Content-Type': 'text/plain' }
        response = requests.post(url, data=code, headers=headers)
        return response.content

    def display(self, code, pixels=None, size=None, format=None):
        format1 = self.default_format if format is None else format
        size1 = self.default_size if size is None else size

        # evaluate or render
        if format1 == 'svg':
            data = self.evaluate(code, pixels=pixels).encode()
        elif format1 == 'png':
            data = self.render(code, pixels=pixels)
        else:
            raise ValueError(f'Invalid format: {format1}')

        # display on terminal
        chafa(data, size=size1)

    def __call__(self, *args, **kwargs):
        self.display(*args, **kwargs)

##
## javascript conversion
##

def stringify(value):
    if isinstance(value, Variable):
        return value.name
    return json.dumps(value)

def convert_opts(opts):
    return ' '.join([
        f'{k}={{{stringify(v)}}}' for k, v in opts.items()
    ])

def indent(lines):
    return '\n'.join([ f'  {line}' for line in lines ])

##
## gum constructors
##

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name

    def define(self):
        return f'{self.name} = {stringify(self.value)}'

class Element:
    def __init__(self, tag, unary, **args):
        self.tag = tag
        self.unary = unary
        self.args = args

    def inner(self):
        return ''

    def __str__(self):
        args = convert_opts(self.args)
        if self.unary:
            return f'<{self.tag} {args} />'
        else:
            inner = self.inner()
            return f'<{self.tag} {args}>\n{inner}\n</{self.tag}>'

class Group(Element):
    def __init__(self, children, tag='Group', **args):
        super().__init__(tag, False, **args)
        self.children = children

    def inner(self):
        return '\n'.join([ str(child) for child in self.children ])

class DataPath(Element):
    def __init__(self, **kwargs):
        super().__init__('DataPath', True, **kwargs)

class Plot(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='Plot', **args)

##
## plotting interface
##

plot_defaults = {
    'grid': True,
    'aspect': 2,
    'margin': 0.15,
    'grid_stroke': 'white',
    'axis_stroke': 'white',
    'axis_label_color': 'white',
}

# TODO: make a general Tag generating framework in for gum in Python

def test_data():
    import math
    import numpy as np
    import pandas as pd
    df = pd.DataFrame({
        'theta': np.linspace(0, 2 * math.pi, 100),
    })
    df['sin'] = np.sin(df['theta'])
    df['cos'] = np.cos(df['theta'])
    return df.set_index('theta')

class Viz(Gum):
    def __init__(self, size=75, **kwargs):
        super().__init__(size=size, **kwargs)

    def plot(self, data, display=True, **kwargs):
        # enforce defaults
        data = data.copy()
        if data.index.name is None:
            data.index.name = 'index'

        # data setters
        index = Variable(data.index.name, data.index.tolist())
        value = [ Variable(col, data[col].tolist()) for col in data.columns ]
        header = '\n'.join([ index.define(), *[ v.define() for v in value ] ])

        # data plotters
        plotters = [ DataPath(xvals=index, yvals=v, stroke='white') for v in value ]
        plot = Plot(plotters, **plot_defaults, **kwargs)

        # generate svg code
        code = f'{header}\n\nreturn {plot}'

        # render to svg
        if display:
            self.display(code)
        else:
            return code
