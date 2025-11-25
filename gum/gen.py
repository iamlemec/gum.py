# gum generation

import json
from collections import defaultdict

##
## javascript conversion
##

def stringify(value):
    if isinstance(value, (Variable, Constant)):
        return value.name
    return json.dumps(value)

def convert_opts(opts):
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
    pattr = defaultdict(dict)
    attr0 = {}
    for key, val in attr.items():
        for p in pres:
            p1 = f'{p}_'
            if key.startswith(p1):
                k1 = key[len(p1):]
                pattr[p][k1] = val
                break
        else:
            attr0[key] = val
    attr1 = [ pattr[p] for p in pres ]
    return attr1, attr0

##
## gum constructors
##

## values

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name

    def define(self):
        return f'{self.name} = {stringify(self.value)}'

class Constant:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class ConstantGenerator:
    def __getattr__(self, name):
        return Constant(name)

# singleton instance
C = ConstantGenerator()

## core elements

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
