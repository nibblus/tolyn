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

from data.matrix import Matrix


class Node:
    """

    """
    def __init__(self):
        pass


class Edge:
    """

    """
    def __init__(self, start, end, directed):
        self.start = start
        self.end = end
        self._directed = directed

    @property
    def directed(self):
        """
        :return:
        """
        return self._directed

    @directed.setter
    def directed(self, value:bool):
        if isinstance(value, bool):
            self._directed= True
        else:
            raise




class Graph:
    """

    """

    def __init__(self):
        self.connectivity = Matrix()
        self.nodes = dict()

    def add(self, *args ) -> None:
        """
        Add a node to the graph
        :param node:
        :return:
        """
        for arg in args:
            if isinstance(arg, Node):
                if self.nodes.get(arg) is None:
                    self.nodes[arg] = len(self.nodes)
                    self.connectivity.a
            elif isinstance(arg, Edge):
                self.add(arg.start)
                self.add(arg.end)

