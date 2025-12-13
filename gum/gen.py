# gum generation

import json
import inspect
from collections import defaultdict

from .utl import AlgMixin
from .gum import evaluate

##
## javascript conversion
##

def stringify(value):
    # convert functions to Functions
    if callable(value):
        value = Fun(value)

    # convert numeric values to lists
    if hasattr(value, 'tolist'):
        value = value.tolist()

    # short circuit for gum values
    if isinstance(value, (Var, Con, Fun, Element)):
        return str(value)

    # handle basic json types
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, float):
        return f'{value:g}'
    elif isinstance(value, str):
        return json.dumps(value) # handles escaping
    elif isinstance(value, (list, tuple)):
        return f'[{", ".join([ stringify(v) for v in value ])}]'
    elif isinstance(value, dict):
        return f'{{ {", ".join([ f'"{k}": {stringify(v)}' for k, v in value.items() ])} }}'
    else:
        raise ValueError(f'Unsupported type: {type(value)}')

def convert_child(value):
    enc = stringify(value)
    if isinstance(value, Element):
        return enc
    else:
        return f'{{ {enc} }}'

def convert_args(opts):
    return ' '.join([
        f'{k}={{{stringify(v)}}}' for k, v in opts.items()
    ])

def indented(text, n=2):
    tab = n * ' '
    lines = text.split('\n')
    return '\n'.join([ f'{tab}{line}' for line in lines ])

def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [ value ]

##
## arg handlers
##

def prefix_split(pres, attr):
    # handle single prefix
    if not isinstance(pres, (tuple, list)):
        pres = [ pres ]
        squeeze = True
    else:
        squeeze = False

    # collect attributes
    pattr = defaultdict(dict)
    attr0 = {}
    for key, val in attr.items():
        for p in pres:
            if key.startswith(f'{p}_'):
                k1 = key[len(p)+1:]
                pattr[p][k1] = val
                break
        else:
            attr0[key] = val

    # return attributes
    attr1 = pattr[pres[0]] if squeeze else [ pattr[p] for p in pres ]
    return attr1, attr0

##
## gum constructors
##

## values

class Var(AlgMixin):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @classmethod
    def from_series(cls, s, name=None):
        return cls(s.name or name, s)

    def __str__(self):
        return self.name

    def define(self):
        return f'const {self.name} = {stringify(self.value)}'

class Con(AlgMixin):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class VarGen:
    def __getattr__(self, name):
        def generator(value):
            return Var(name, value)
        return generator

class ConGen:
    def __getattr__(self, name):
        return Con(name)

    def __call__(self, value):
        return Con(value)

# singleton instances
V = VarGen()
C = ConGen()

## core elements

class Element:
    def __init__(self, tag, unary, **args):
        self.tag = tag
        self.unary = unary
        self.args = args

    def inner(self):
        return ''

    def __str__(self):
        args = convert_args(self.args)
        if self.unary:
            return f'<{self.tag} {args} />'
        else:
            inner = self.inner()
            return f'<{self.tag} {args}>\n{inner}\n</{self.tag}>'

    def _repr_svg_(self):
        return evaluate(self)

class Group(Element):
    def __init__(self, *children, tag='Group', **args):
        unary = len(children) == 0
        super().__init__(tag, unary, **args)
        self.children = children

    def inner(self):
        return '\n'.join([ indented(convert_child(c)) for c in self.children ])

## function elements

class Fun:
    def __init__(self, func):
        sig = inspect.signature(func)
        self.args = [ Con(p.name) for p in sig.parameters.values() ]
        self.ret = func(*self.args)

    def __str__(self):
        args = ', '.join([ str(a) for a in self.args ])
        return f'({args}) => ({self.ret})'

## layout elements

class Box(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='Box', **args)

class Frame(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='Frame', **args)

class Stack(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='Stack', **args)

class HStack(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='HStack', **args)

class VStack(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='VStack', **args)

## shape elements

class Rect(Element):
    def __init__(self, **kwargs):
        super().__init__('Rect', True, **kwargs)

class Ellipse(Element):
    def __init__(self, **kwargs):
        super().__init__('Ellipse', True, **kwargs)

class Square(Element):
    def __init__(self, **kwargs):
        super().__init__('Square', True, **kwargs)

class Circle(Element):
    def __init__(self, **kwargs):
        super().__init__('Circle', True, **kwargs)

## draw elements

class Line(Element):
    def __init__(self, **kwargs):
        super().__init__('Line', True, **kwargs)

class HLine(Element):
    def __init__(self, **kwargs):
        super().__init__('HLine', True, **kwargs)

class VLine(Element):
    def __init__(self, **kwargs):
        super().__init__('VLine', True, **kwargs)

## text elements

class Text(Group):
    def __init__(self, *children, **kwargs):
        super().__init__(*children, tag='Text', **kwargs)

## plot elements

class DataPath(Element):
    def __init__(self, *children, **kwargs):
        super().__init__('DataPath', True, **kwargs)

class DataPoints(Group):
    def __init__(self, *children, **kwargs):
        super().__init__(*children, tag='DataPoints', **kwargs)

class Graph(Group):
    def __init__(self, *children, **kwargs):
        super().__init__(*children, tag='Graph', **kwargs)

class Plot(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='Plot', **args)

##
## bar elements
##

class VBar(Element):
    def __init__(self, **kwargs):
        super().__init__('VBar', True, **kwargs)

class HBar(Element):
    def __init__(self, **kwargs):
        super().__init__('HBar', True, **kwargs)

class BarPlot(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='BarPlot', **args)

## container elements

class TitleFrame(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='TitleFrame', **args)

class Slide(Group):
    def __init__(self, *children, **args):
        super().__init__(*children, tag='Slide', **args)

##
## dataframe notion
##

def ensure_var(var, name=None):
    import numpy as np
    import pandas as pd
    if isinstance(var, (np.ndarray, list, tuple)):
        var = pd.Series(var)
    elif isinstance(var, pd.Index):
        var = var.to_series()
    if isinstance(var, pd.Series):
        var = Var.from_series(var, name=name)
    elif not isinstance(var, Var):
        raise ValueError(f'Unsupported type: {type(var)}')
    return var

class GumData:
    def __init__(self, data, index=None):
        self.index = ensure_var(index, name='index')
        self._data = [ ensure_var(v, name=f'value_{i}') for i, v in enumerate(data) ]

    @classmethod
    def from_frame(cls, frame):
        data = [ frame[col] for col in frame ]
        return cls(data, index=frame.index)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        self._data[name] = ensure_var(value, name=name)

    def define(self):
        return '\n'.join([ v.define() for v in [ self.index, *self._data ] ])

##
## top level
##

class Gum:
    def __init__(self, cont, vars=None):
        if vars is None:
            vars = []
        elif not isinstance(vars, (tuple, list)):
            vars = [ vars ]
        self.vars = vars
        self.content = cont

    def __str__(self):
        header = '\n'.join([ v.define() for v in self.vars ])
        if len(header) > 0:
            return f'{header}\n\nreturn {self.content}'
        else:
            return str(self.content)

    def _repr_svg_(self):
        return evaluate(self)
