## utils

## mixins

class AlgMixin:
    def __add__(self, other):
        return type(self)(f'({self})+({other})')

    def __radd__(self, other):
        return type(self)(f'({other})+({self})')

    def __sub__(self, other):
        return type(self)(f'({self})-({other})')

    def __rsub__(self, other):
        return type(self)(f'({other})-({self})')

    def __mul__(self, other):
        return type(self)(f'({self})*({other})')

    def __rmul__(self, other):
        return type(self)(f'({other})*({self})')

    def __truediv__(self, other):
        return type(self)(f'({self})/({other})')

    def __rtruediv__(self, other):
        return type(self)(f'({other})/({self})')

    def __pow__(self, other):
        return type(self)(f'({self})**({other})')

    def __rpow__(self, other):
        return type(self)(f'({other})**({self})')

    def __mod__(self, other):
        return type(self)(f'({self})%({other})')

    def __rmod__(self, other):
        return type(self)(f'({other})%({self})')

    def __eq__(self, other):
        return type(self)(f'({self})==({other})')

    def __req__(self, other):
        return type(self)(f'({other})==({self})')

    def __ne__(self, other):
        return type(self)(f'({self})!=({other})')

    def __rne__(self, other):
        return type(self)(f'({other})!=({self})')

    def __gt__(self, other):
        return type(self)(f'({self})>({other})')

    def __rgt__(self, other):
        return type(self)(f'({other})>({self})')

    def __ge__(self, other):
        return type(self)(f'({self})>=({other})')

    def __rge__(self, other):
        return type(self)(f'({other})>=({self})')

    def __lt__(self, other):
        return type(self)(f'({self})<({other})')

    def __rlt__(self, other):
        return type(self)(f'({other})<({self})')

    def __le__(self, other):
        return type(self)(f'({self})<=({other})')

    def __rle__(self, other):
        return type(self)(f'({other})<=({self})')

    def __and__(self, other):
        return type(self)(f'({self})&&({other})')

    def __rand__(self, other):
        return type(self)(f'({other})&&({self})')

    def __or__(self, other):
        return type(self)(f'({self})||({other})')

    def __ror__(self, other):
        return type(self)(f'({other})||({self})')

    def __xor__(self, other):
        return type(self)(f'({self})^({other})')

    def __rxor__(self, other):
        return type(self)(f'({other})^({self})')

    def __neg__(self):
        return type(self)(f'-({self})')

    def __pos__(self):
        return type(self)(f'+({self})')
