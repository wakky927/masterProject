import numpy as np


class Item(object):

    def __init__(self):
        self._Vx = 0
        self._Vy = 0

    @property
    def v(self):
        return self._Vx, self._Vy


class UniformFlow(Item):

    def __init__(self, u=0, alpha=0):
        super().__init__()
        self._U = u
        self._alpha = alpha
        self.calc()

    def calc(self):
        self._Vx = self._U * np.cos(self._alpha)
        self._Vy = self._U * np.sin(self._alpha)


class Source(Item):

    def __init__(self, m=0, X=(0, 0), X0=(0, 0)):
        super().__init__()
        self._m = m
        self._x, self._y = X
        self._x0, self._y0 = X0
        self.calc()

    def calc(self):
        self._Vx = self._m * (self._x - self._x0) / ((self._x - self._x0)**2 + (self._y - self._y0)**2)
        self._Vy = self._m * (self._y - self._y0) / ((self._x - self._x0)**2 + (self._y - self._y0)**2)


class Vortex(Item):

    def __init__(self, k=0, X=(0, 0), X0=(0, 0)):
        super().__init__()
        self._k = k
        self._x, self._y = X
        self._x0, self._y0 = X0
        self.calc()

    def calc(self):
        self._Vx = self._k * (self._y - self._y0) / ((self._x - self._x0)**2 + (self._y - self._y0)**2)
        self._Vy = - self._k * (self._x - self._x0) / ((self._x - self._x0) ** 2 + (self._y - self._y0) ** 2)
