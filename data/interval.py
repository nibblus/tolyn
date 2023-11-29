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


from typing import Union

class IntervalException(Exception):
    """
    Exceptions specific for the Cave Interval
    """

    def __init__(self, *args, **kwargs) -> None:
        Exception.__init__(self, *args, **kwargs)


class Interval:
    """
    Functionality for mathematical interval
    """

    def __init__(self, left, right, left_inclusive=True, right_inclusive=True, auto_switch=False) -> None:
        if auto_switch and left is not None and right is not None:
            if left > right:
                temp = left
                left = right
                right = temp
                temp = left_inclusive
                left_inclusive = right_inclusive
                right_inclusive = temp

        if left is None and left_inclusive:
            raise IntervalException("Impossible: if left == None (-infinity) then left_inclusive must be set to False")
        if right is None and right_inclusive:
            raise IntervalException("Impossible: if right == None (+infinity) then right_inclusive must be set to False")
        if not (left is None or right is None) and ((left > right) or (left == right and not (left_inclusive and right_inclusive))):
            raise IntervalException("Impossible: left > right")
        self.left = left
        self.right = right
        self.left_inclusive = left_inclusive
        self.right_inclusive = right_inclusive

    def __contains__(self, value) -> bool:
        if self.left is None and self.right is None:
            return True
        if self.left is None:
            if value < self.right or (self.right_inclusive and value == self.right):
                return True
        if self.right is None:
            if value > self.left or (self.left_inclusive and value == self.left):
                return True
        return (self.left < value < self.right) or (self.left == value and self.left_inclusive) or (self.right == value and self.right_inclusive)

    def __repr__(self) -> str:
        ch1 = ']'
        if self.left_inclusive:
            ch1 = '['
        left = self.left
        if left is None:
            left = '-INF'
        right = self.right
        if right is None:
            right = '+INF'
        ch2 = '['
        if self.right_inclusive:
            ch2 = ']'
        return f"{ch1}{left}, {right}{ch2}"

    def reduce_value(self, value: Union[int, float]) -> Union[int, float]:
        """
        If a value is outside the current boundary, then determine the closest boundary that fits
        If a value is inside the current interval, then return the value itself.
        :param value: Any value
        :return: Value within the current interval
        """
        if value < self.left:
            if not self.left_inclusive:
                raise FrameworkException(f"Don't know how to reduce value {value} to exclusive left boundary  {self.left} in {self}")
            return self.left
        if value > self.right:
            if not self.right_inclusive:
                raise FrameworkException(f"Don't know how to reduce value {value} to exclusive right boundary  {self.right} in {self}")
            return self.right
        return value


if __name__ == '__main__':
    raise NotImplementedError(__name__)
