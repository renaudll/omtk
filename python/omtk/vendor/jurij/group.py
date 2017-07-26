# -*- encoding: utf-8 -*-

# Finitely generated finite groups with decidable equality.

import types

class Group():
    def __init__(self, generators, operation, inverse=None, unit=None, power=None, additive=False):
        self.generators = frozenset(generators)
        self._inverse = inverse
        self._power = power
        self._operation = operation
        self.additive = additive
        if unit is not None:
            self.unit = unit
        else:
            # compute the unit
            x = next(iter(self.generators))
            (y,z) = (x, self.operation(x,x))
            while z != x:
                (y,z) = (z, self.operation(z,x))
            self.unit = y

    def operation(self, x, y):
        if isinstance(x, (AdditiveGroupElement, MultiplicativeGroupElement)):
            x = x.element
        if isinstance(y, (AdditiveGroupElement, MultiplicativeGroupElement)):
            y = y.element
        return self._operation(x,y)
        
    def inverse(self, x):
        if isinstance(x, (AdditiveGroupElement, MultiplicativeGroupElement)):
            x = x.element
        if self._inverse is not None:
            return self._inverse(x)
        else:
            y = self.unit
            while True:
                z = self.operation(y,x)
                if z == self.unit: return y
                else: y = z

    def power(self, x, k):
        if isinstance(x, (AdditiveGroupElement, MultiplicativeGroupElement)):
            x = x.element
        if self._power is not None:
            return self._power(x, k)
        else:
            def p(k):
                if k == 0: return self.unit
                y = p(k//2)
                y = self.operation(y,y)
                if k % 2 == 1: y = self.operation(y,x)
                return y
            if k < 0:
                k = -k
                x = self.inverse(x)
            return p(k)

    def elements(self):
        if hasattr(self, '_elements'):
            return self._elements
        else:
            self._elements = set()
            candidates = set(self.generators)
            while len(candidates) > 0:
                self._elements |= candidates
                candidates = set()
                for x in self._elements:
                    for y in self.generators:
                        z = self.operation(x,y)
                        if z not in self._elements:
                            candidates.add(z)
            return self._elements

    def size(self):
        return len(self.elements())

    def order(self, x):
        if isinstance(x, (AdditiveGroupElement, MultiplicativeGroupElement)):
            x = x.element
        k = 1
        y = x
        while y != self.unit:
            y = self.operation(y,x)
            k = k + 1
        return k

    def __call__(self,x):
        if isinstance(x, (AdditiveGroupElement, MultiplicativeGroupElement)):
            x = x.element
        if self.additive:
            return AdditiveGroupElement(self,x)
        else:
            return MultiplicativeGroupElement(self,x)

    def vertices(self):
        return self.elements()

    def edges(self):
        for x in self.elements():
            for g in self.generators:
                yield (x, self.operation(x,g))

    def edge_label(self,e):
        (x,y) = e
        return self.operation(self.inverse(x),y)


class AdditiveGroupElement():
    def __init__(self, g, x):
        self.group = g
        self.element = x

    def __repr__(self):
        return str(self.element)

    def __add__(self,y):
        return self.group(self.group.operation(self.element, y.element))

    def __neg__(self):
        return self.group(self.group.inverse(self.element))

    def __invert__(self):
        return self.group(self.group.inverse(self.element))

    def __sub__(self,y):
        return self.group(self.group.operation(self.element, self.group.inverse(y.element)))

    def __mul__(self,k):
        return self.group(self.group.power(self.element, k))

    def __rmul__(self,k):
        return self.group(self.group.power(self.element, k))

class MultiplicativeGroupElement():
    def __init__(self, g, x):
        self.group = g
        self.element = x

    def __repr__(self):
        return str(self.element)

    def __mul__(self,y):
        return self.group(self.group.operation(self.element, y.element))

    def __neg__(self):
        return self.group(self.group.inverse(self.element))

    def __div__(self,y):
        return self.group(self.group.operation(self.element, self.group.inverse(y.element)))

    def __truediv__(self,y):
        return self.__div__(y)

    def __pow__(self,k):
        return self.group(self.group.power(self.element, k))

    def inverse(self):
        return self.group(self.group.inverse(self.element))

    def order(self):
        return self.group.order(self.element)

def permutation_group(generators):
    def operation(p,q):
        return tuple(p[i] for i in q)
    def inverse(p):
        q = [0 for i in p]
        for (i,j) in enumerate(p):
            q[j] = i
        return tuple(q)
    unit = () if len(generators) == 0 else tuple(range(len(next(iter(generators)))))
    return Group(generators, operation=operation, inverse=inverse, unit=unit, additive=False)

def cyclic_group(k):
    return Group([1], operation=(lambda x,y: (x+y)%k), inverse=(lambda x: (k-x)%k), unit=0, additive=True)

def symmetric_group(k):
    t = tuple((1-i if i < 2 else i) for i in range(k))
    r = tuple((i+1)%k for i in range(k))
    return permutation_group((t,r))

def cartesian_product(g,h, additive=False):
    additive = additive or (g.additive and h.additive)
    return Group([(x,y) for x in g.generators for y in h.generators],
                 operation=(lambda x,y: (g.operation(x[0],y[0]), h.operation(x[1],y[1]))),
                 inverse = (lambda x: (g.inverse(x[0]), h.inverse(x[1]))),
                 power = (lambda x,k: (g.power(x[0],k), h.power(x[1],k))),
                 unit = (g.unit, h.unit),
                 additive = additive)

