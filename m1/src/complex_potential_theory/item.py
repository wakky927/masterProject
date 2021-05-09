import numpy as np


class Item(object):
    """item object
    :ivar _Vx: x component of velocity
    :ivar _Vy: y component of velocity
    """

    def __init__(self):
        self._Vx = 0.0
        self._Vy = 0.0

    @property
    def v(self):
        """getter/setter of velocity
        :return array[V_x, V_y]: Optional(Tuple[float, float])
        """

        return self._Vx, self._Vy

    @property
    def vx(self):  # getter/setter of x component
        return self._Vx

    @property
    def vy(self):  # getter/setter of y component
        return self._Vy


class UniformFlow(Item):
    """uniform flow object
    :ivar _Vx: x component of velocity
    :ivar _Vy: y component of velocity

    :ivar _U: flow speed
    :ivar _alpha: angle
    """

    def __init__(self, u=0, alpha=0):
        """
        :param u: flow speed [m/s]
        :param alpha: angle [rad]
        """

        super().__init__()
        self._U = u
        self._alpha = alpha
        self.calc()

    def calc(self):  # velocity calculation
        self._Vx = self._U * np.cos(self._alpha)
        self._Vy = self._U * np.sin(self._alpha)


class Source(Item):
    """source object
    :ivar _Vx: x component of velocity
    :ivar _Vy: y component of velocity

    :ivar _m: source strength
    :ivar _x: x coordinate
    :ivar _y: y coordinate
    :ivar _x0: x coordinate of source
    :ivar _y0: y coordinate of source
    """

    def __init__(self, m=0, X=(0, 0), X0=(0, 0)):
        """
        :param m: source strength [m^2/s]
        :param X: coordinates [m]
        :param X0: source coordinates [m]
        """

        super().__init__()
        self._m = m
        self._x, self._y = X
        self._x0, self._y0 = X0
        self.calc()

    def calc(self):  # velocity calculation
        self._Vx = self._m * (self._x - self._x0) / ((self._x - self._x0)**2 + (self._y - self._y0)**2)
        self._Vy = self._m * (self._y - self._y0) / ((self._x - self._x0)**2 + (self._y - self._y0)**2)


class VortexLine(Item):
    """vortex line object
    :ivar _Vx: x component of velocity
    :ivar _Vy: y component of velocity

    :ivar _k: vortex strength
    :ivar _x: x coordinate
    :ivar _y: y coordinate
    :ivar _x0: x coordinate of vortex
    :ivar _y0: y coordinate of vortex
    """

    def __init__(self, k=0, X=(0, 0), X0=(0, 0)):
        """
        :param k: vortex strength [m^2/s]
        :param X: coordinates [m]
        :param X0: vortex coordinates [m]
        """

        super().__init__()
        self._k = k
        self._x, self._y = X
        self._x0, self._y0 = X0
        self.calc()

    def calc(self):  # velocity calculation
        self._Vx = self._k * (self._y - self._y0) / ((self._x - self._x0)**2 + (self._y - self._y0)**2)
        self._Vy = - self._k * (self._x - self._x0) / ((self._x - self._x0) ** 2 + (self._y - self._y0) ** 2)
