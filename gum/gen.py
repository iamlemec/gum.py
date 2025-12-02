# gum generation

import json
from collections import defaultdict

##
## javascript conversion
##

def stringify(value):
    # short circuit for defined values
    if isinstance(value, (Var, Const)):
        return value.name

    # convert numeric values to lists
    if hasattr(value, 'tolist'):
        value = value.tolist()

    # convert to json
    return json.dumps(value)

def convert_args(opts):
    return ' '.join([
        f'{k}={{{stringify(v)}}}' for k, v in opts.items()
    ])

def indented(lines, n=2):
    tab = n * ' '
    return '\n'.join([ f'{tab}{line}' for line in lines ])

def ensure_list(value):
    if isinstance(value, (list, tuple)):
        return list(value)
    return [ value ]

##
## arg handlers
##

def prefix_split(pres, attr):
    # handle single prefix
    if not isinstance(pres, list):
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

class Var:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @classmethod
    def from_series(cls, s, name=None):
        return cls(s.name or name, s.values)

    def __str__(self):
        return self.name

    def define(self):
        return f'{self.name} = {stringify(self.value)}'

class Const:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class ConstGen:
    def __getattr__(self, name):
        return Const(name)

class VareGen:
    def __getattr__(self, name):
        def generator(value):
            return Var(name, value)
        return generator

# singleton instances
C = ConstGen()
V = VareGen()

# variable collection
class Vars(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def from_dataframe(cls, df):
        return cls(**{ col: Var.from_series(df[col]) for col in df })

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def define(self):
        return '\n'.join([ v.define() for v in self.values() ])

## top level

class Gum:
    def __init__(self, cont, vars=None):
        if vars is None:
            vars = []
        elif not isinstance(vars, list):
            vars = [ vars ]
        self.vars = vars
        self.content = cont

    def __str__(self):
        header = '\n'.join([ v.define() for v in self.vars ])
        if len(header) > 0:
            return f'{header}\n\nreturn {self.content}'
        else:
            return str(self.content)

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

class Group(Element):
    def __init__(self, children, tag='Group', **args):
        super().__init__(tag, False, **args)
        self.children = ensure_list(children)

    def inner(self):
        return indented(self.children)

## layout elements

class Box(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='Box', **args)

class Frame(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='Frame', **args)

class Stack(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='Stack', **args)

class HStack(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='HStack', **args)

class VStack(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='VStack', **args)

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

## text elements

class Text(Group):
    def __init__(self, children, **kwargs):
        super().__init__(children, tag='Text', **kwargs)

## plot elements

class DataPath(Element):
    def __init__(self, **kwargs):
        super().__init__('DataPath', True, **kwargs)

class DataPoints(Group):
    def __init__(self, children, **kwargs):
        super().__init__(children, tag='DataPoints', **kwargs)

class Plot(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='Plot', **args)

## container elements

class TitleFrame(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='TitleFrame', **args)

class Slide(Group):
    def __init__(self, children, **args):
        super().__init__(children, tag='Slide', **args)
