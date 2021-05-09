import sys

import numpy as np


EPS = sys.float_info.epsilon  # machine epsilon


class Field(object):

    def __init__(self, x_range, y_range, div_num):
        self._x = np.linspace(x_range[0], x_range[1], div_num[0]+1)
        self._y = np.linspace(y_range[0], y_range[1], div_num[1]+1)
        self._coordinates = np.zeros((2, div_num[1]+1, div_num[0]+1))
        self.prevent_zero_div()
        self.mesh()

    def prevent_zero_div(self):
        self._x += EPS
        self._y += EPS

    def mesh(self):
        self._coordinates[0], self._coordinates[1] = np.meshgrid(self._x, self._y)
        return

    @property
    def coordinates(self):
        return self._coordinates


if __name__ == '__main__':
    field = Field((0, 100), (0, 50), (200, 25))
    c = field.coordinates
