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

class GraphException(Exception):
    """
    Graph related exceptions
    """

    pass

class Node:
    """
    Base class of graph nodes or vertices
    """

    def __init__(self):
        self.incoming = set()
        self.outgoing = set()

class Edge:
    """
    Representation of a directional edge
    """

    def __init__(self, start: Node=None, end: Node = None):
        self.start = start
        self.end =end

    def __repr__(self) -> str:
        return f'E({self.start} -> {self.end})'




class Graph:
    """
    Graph
    """

    def __init__(self):
        self._nodes = set()
        self._edges = set()

    @property
    def nodes(self):
        raise GraphException("Not accessible")

    @property
    def edges(self):
        raise GraphException("Not accessible")

    def add_nodes(self, *nodes):
        for node in nodes:
            self._nodes.add(node)

    def add_node(self, *nodes):
        self.add_nodes(nodes)

    def add_edge(self, edge:Edge):
        self.add_nodes(edge.start, edge.end)
        self.add_edge(edge)
        edge.start.outgoing.add(edge.end)
        edge.end.incoming.add(edge.start)









if __name__ == "__name__":
    raise NotImplementedError()
