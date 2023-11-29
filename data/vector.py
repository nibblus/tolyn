"""
    This file is part of tolyn.

    tolyn is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import math
from typing import Union, Optional


class Vector(list):
    """
    A vector is a list of numeric values
    """

    def __init__(self, *args, **kwargs) -> None:
        list.__init__(self, *args, **kwargs)
        if len(kwargs) == 0:
            if len(args) == 0:  # no parameter delivered
                return
            if type(args[0]) in (tuple, list):
                if len(args) > 1:
                    raise TypeError("List provided, no second argument allowed")
                for value in args[0]:
                    self.append(value)
                return
            else:
                for value in args:
                    self.append(value)
                return
        else:
            if len(args) != 0:
                raise TypeError("Named arguments provided, no unnamed arguments allowed")
            for kwarg in kwargs:
                if kwarg not in ["width", "default"]:
                    raise TypeError(f"kwarg {kwarg} no supported")
            width = kwargs.get("width")
            default = kwargs.get("default")
            if width is None:
                raise RuntimeError("width must be positive integer")
            if type(width) != int or width < 0:
                raise RuntimeError("width must be positive integer")
            if default is None:
                default = 0
            for i in range(width):
                self.append(default)

    def __abs__(self):
        ret = Vector(width=0)
        for value in self:
            ret.append(abs(value))
        return ret

    def __add__(self, other):
        return Vector(value=list(self) + list(other))

    def __setitem__(self, key, value):
        self.check_type(value)
        super().__setitem__(key, value)

    def __cmp__(self, other):
        return self.distance().__cmp__(other.distance())

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __le__(self, other):
        return self.distance() <= other.distance()

    def __eq__(self, other):
        if self is None or other is None or len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.distance() > other.distance()

    def __ge__(self, other):
        return self.distance() >= other.distance()

    def distance(self, other=None) -> float:
        """
        Calculate Cartesian distance between two vectors, if no second vector is given then the origin is implied
        :param other: Another vector
        :return: Mathematical Distance
        """
        if other is None:
            other = Vector(width=len(self))
        if not isinstance(other, Vector):
            raise TypeError("argument must be a vector")
        elif len(self) == 0 or len(other) == 0 or len(self) != len(other):
            raise IndexError("vectors can not be empty and must be equal size")
        total = 0
        for i in range(len(self)):
            term = (self[i] - other[i])
            total += term * term
        return math.sqrt(total)

    def horizontal(self):
        """
        Get the 1st value of the vector - X dimension
        :return: the 1st value of the vector - X dimension
        """
        return self.x()

    def vertical(self):
        """
        Get the 2nd value of the vector - Y dimension
        :return: the 2nd value of the vector - Y dimension
        """
        return self.y()

    def depth(self):
        """
        Get the 3rd value of the vector - Z dimension
        :return: the 3rd value of the vector - Z dimension
        """
        return self.z()

    def x(self):
        """
        Get the 1st value of the vector
        :return: the 1st value of the vector
        """
        return self._safe_indexed_value(0)

    def y(self):
        """
        Get the 2nd value of the vector
        :return: the 2nd value of the vector
        """
        return self._safe_indexed_value(1)

    def z(self):
        """
        Get the 3rd value of the vector
        :return: the 3rd value of the vector
        """
        return self._safe_indexed_value(2)

    def u(self):
        """
        Get the 4th value of the vector
        :return: the 4th value of the vector
        """
        return self._safe_indexed_value(3)

    def v(self):
        """
        Get the 5th value of the vector
        :return: the 5th value of the vector
        """
        return self._safe_indexed_value(4)

    def w(self):
        """
        Get the 6th value of the vector
        :return: the 6th value of the vector
        """
        return self._safe_indexed_value(5)

    def _safe_indexed_value(self, index: int) -> Union[float, int, None]:
        """
        Return the indexed value if index is in range, otherwise None
        :param index: 0-based index
        :return: value if None
        """
        try:
            return self[index]
        except IndexError:
            return None

    @staticmethod
    def check_type(value) -> Optional[bool]:
        """
        Check the value type
        :param value:
        :raise TypeError: If value type is not accepted
        """
        if type(value) not in (int, float):
            raise TypeError("Can not add non-numeric value")
        return True

    def append(self, value: object) -> None:
        """
        Append the value to the vector
        :param value: Value to append
        """
        self.check_type(value)
        super().append(value)

    def abs(self):
        """
        Return a vector with  absolute values of the original
        :return: a vector with  absolute values of the original
        """
        ret = Vector()
        for v in self:
            ret.append(abs(v))
        return ret

    def rotate_left(self) -> None:
        """
        Rotate the values 1 position left
        """
        if 0 <= len(self) <= 1:
            return
        temp = self.pop(0)
        self.append(temp)

    def rotate_right(self) -> None:
        """
        Rotate the values 1 position right
        """
        if 0 <= len(self) <= 1:
            return
        temp = self.pop(-1)
        self.insert(0, temp)


if __name__ == '__main__':
    raise NotImplementedError(__file__)
