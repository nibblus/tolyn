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

from testing.unit import ToBeTested


class DictException(Exception):
    """
    General Dict exception
    """
    pass


class KeyNotFoundException(DictException):
    """
    Exceptions related to keys
    """
    pass


class Dict(dict):
    """
    Extension of the dict base type
    """

    @ToBeTested
    def pop_keys(self, default_value, raise_if_not_empty: bool = False, *args) -> list:
        """
        Pop entries from the dict based on their key
        :param raise_if_not_present: If true, an exception will be raised if the key is not found
        :param raise_if_not_empty:
        :param args: key values to pop
        :return: list of values
        """
        ret = []
        for arg in args:
            ret.append(self.pop(arg))
        if raise_if_not_empty and len(self): raise Exception(f"Dict is not empty: {from_dict} ")

    def remove_keys(self, *args, raise_if_not_empty: bool = False) -> None:
        """
        Remove entries from the dict based on their key
        :param raise_if_not_empty:
        :param args:
        :return: list of values
        """
        for arg in args:
            self.pop(arg)
        if raise_if_not_empty and len(self):
            raise KeyError(f"Dict is not empty after removing the keys: {self} ")

    @ToBeTested
    def keyslist(self):
        """
        Return the keys in a list
        :return: list of keys
        """
        return list(self.keys())

    @ToBeTested
    def valueslist(self):
        """
        Return the values in a list
        :return: list of values
        """
        return list(self.values())