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

from collections.abc import Iterable

FILTER = {"_name", "_item_name"}


class Formatter:
    """
    Base class to add output formatting to a class
    """

    def __init__(self, format_name = None, format_item_name = None) -> None:
        self._name = format_name
        self._item_name = format_item_name

    @property
    def name(self) -> str:
        return self.__class__.__name__ if self._name is None else self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = str(value)

    @property
    def item_name(self) -> str:
        return "item" if self._item_name is None else self._item_name

    @item_name.setter
    def item_name(self, value: str) -> None:
        self.item_name = str(value)

    def attributes(self) -> dict:
        ret = vars(self).copy()
        for item in FILTER:
            ret.pop(item)
        return ret

    def str(self) -> str:
        return f"{self.__class__.__name__} : {vars(self)}"

    def html(self) -> str:
        return f"<P/>{self.str()}<P/>"

    def xml(self) -> str:
        attributes = self.attributes()
        inlist = " " if len(attributes) else ""
        inlist += " ".join([f'{name}="{value}"' for name, value in attributes.items()])

        iterlist = "".join([f"<item>{item}</item>" for item in self]) if isinstance(self, Iterable) else ""

        return f'<{self.name}{inlist}>{iterlist}</{self.name}>'










class List(list, Formatter):
    """
    list with formatting
    """
    def __init__(self, iterable = None, format_name=None, format_item_name=None, **kwargs):
        list.__init__(self, iterable)
        Formatter.__init__(self,format_name=format_name, format_item_name=format_item_name)
        self.header = "HEAD"


a = List([3,4], name = 'EEE')
print(a.xml())
a = Formatter(format_name="iets")
print(a.xml())






