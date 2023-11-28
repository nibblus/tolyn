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
from typing import Iterable, Tuple, Any, Type
from typing_extensions import SupportsIndex
from formatting.format import Formatter


class Vector(Formatter, list):
    """
    Representation of a mathematical vector.
    """

    def __init__(self, data=None, width: int = 0, initial_value=None, value_func=None):
        Formatter.__init__(self)
        if data is None:
            list.__init__(self)
            if initial_value is not None and value_func is not None: raise Exception()
            if initial_value is not None: value_func= lambda x: initial_value
            data
            for i in range(width):
                self.append(value_func(i))
            self.append()
        else:
            list.__init__(self, data)
            if width is not None: raise Exception()
            if initial_value is not None: raise Exception()
            if value_func is not None: raise Exception()






    def __init(self, width: int, initial_value=None, value_func=None):
        Formatter.__init__(self)
        list.__init__(self)

        if value_func is None:
            value_func = lambda x : 0 if initial_value is None else lambda x : initial_value
        elif initial_value is not None:
            raise NotImplementedError("initial value and value func can not be used together")
        for row in range(self._dimension[1]):
            for col in range(self.dimension[0]):
                self[row][col] = value_func(self[row][col])
        if value_func is None:
            if  initial_value IS None:
                initial_value = 0

    @staticmethod
    def check_index(*values) -> None:
        for value in values:
            value = int(value)
            if value < 1:
                raise OverflowError()

    def operate(self, func):
        for i in  len(self):
            self[i] = func(self[i])

    def check_dimension(self, other):
        if self._dimension != other._dimension:
            raise ValueError("Dimensions must be identical")

    @property
    def name(self) -> str:
        return super().name

    @property
    def item_name(self) -> str:
        return super().item_name

    def attributes(self) -> dict:
        return super().attributes()

    def str(self) -> str:
        return super().str()

    def html(self) -> str:
        return super().html()

    def xml(self) -> str:
        return super().xml()

    @property
    def __class__(self: _T) -> Type[_T]:
        return super().__class__

    # def __new__(cls: Type[_T]) -> _T:
    #     return super().__new__(cls)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __eq__(self, other: object) -> bool:

        return super().__eq__(o)

    def __ne__(self, o: object) -> bool:
        return super().__ne__(o)

    def __len__(self):
        pass

    def __add__(self, other):
        self.check_dimension()
        self.operate(other, )

        pass

    def __sub__(self, other):
        pass

    def __divmod__(self, other):
        pass

    def __bool__(self):
        pass

    def __float__(self):
        pass

    def __int__(self):
        pass

    def __abs__(self):
        pass

    def __neg__(self):
        pass

    def __and__(self, other):
        pass

    def __or__(self):
        pass

    def __xor__(self, other):
        pass
    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()

    def __hash__(self) -> int:
        return super().__hash__()

    def __format__(self, format_spec: str) -> str:
        return super().__format__(format_spec)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __delattr__(self, name: str) -> None:
        super().__delattr__(name)

    def __sizeof__(self) -> int:
        return super().__sizeof__()

    def __reduce__(self) -> str | Tuple[Any, ...]:
        return super().__reduce__()

    def __reduce_ex__(self, protocol: SupportsIndex) -> str | Tuple[Any, ...]:
        return super().__reduce_ex__(protocol)

    def __dir__(self) -> Iterable[str]:
        return super().__dir__()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

    def __floor__(self):
        pass

    def __ceil__(self):
        pass

    def __hex__(self):
        pass

    def __oct__(self):
        pass

    def __round__(self, n=None):
        self.operate





