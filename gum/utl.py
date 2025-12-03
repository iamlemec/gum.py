## utils

## mixins

class AlgMixin:
    def __add__(self, other):
        return type(self)(f'{self} + {other}')

    def __sub__(self, other):
        return type(self)(f'{self} - {other}')

    def __mul__(self, other):
        return type(self)(f'{self} * {other}')

    def __truediv__(self, other):
        return type(self)(f'{self} / {other}')

    def __pow__(self, other):
        return type(self)(f'{self} ** {other}')

    def __mod__(self, other):
        return type(self)(f'{self} % {other}')

    def __eq__(self, other):
        return type(self)(f'{self} == {other}')

    def __ne__(self, other):
        return type(self)(f'{self} != {other}')

    def __gt__(self, other):
        return type(self)(f'{self} > {other}')

    def __ge__(self, other):
        return type(self)(f'{self} >= {other}')

    def __lt__(self, other):
        return type(self)(f'{self} < {other}')

    def __le__(self, other):
        return type(self)(f'{self} <= {other}')

    def __and__(self, other):
        return type(self)(f'{self} && {other}')

    def __or__(self, other):
        return type(self)(f'{self} || {other}')

    def __xor__(self, other):
        return type(self)(f'{self} ^ {other}')

    def __neg__(self):
        return type(self)(f'-{self}')

    def __pos__(self):
        return type(self)(f'+{self}')
