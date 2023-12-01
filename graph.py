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
from xml.etree import ElementTree


def pop_keys(from_dict: dict, raise_if_not_empty: bool, *args):
    for arg in args:
        from_dict.pop(arg)
    if raise_if_not_empty and len(from_dict): raise Exception(f"Dict is not empty: {from_dict} ")


class Node:
    """
    Representation of a node
    """

    def __init__(self):
        pass


class Edge:
    """

    """

    def __init__(self, start: Node, end: Node, directed: bool):
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
    def directed(self, value: bool):
        if isinstance(value, bool):
            self._directed = True
        else:
            raise

    def __repr__(self) -> str:
        return f"Edge({self.start}{'-->' if self._directed else '<->'}{self.end}"


class UndirectedEdge(Edge):
    def __init__(self, start, end):
        Edge.__init__(self, start, end, False)


class DirectedEdge(Edge):
    def __init__(self, start, end):
        Edge.__init__(self, start, end, True)


class Graph:
    """

    """

    def __init__(self):
        self.connectivity = Matrix()
        self.nodes = dict()

    def add(self, *args) -> None:
        """
        Add a node to the graph
        :param node:
        :return:
        """
        for arg in args:
            if isinstance(arg, Node):
                if self.nodes.get(arg) is None:
                    self.nodes[arg] = len(self.nodes)
                    self.connectivity.add_column()
                    self.connectivity.add_row([0 for i in range(self.connectivity.width())])
            elif isinstance(arg, Edge):
                self.add(arg.start)
                self.add(arg.end)
                # pos_start, post_end = self.nodes.keys().


class Component:

    def __init__(self, index=None, component_id: str = None):
        self.component_id = component_id
        self.ccount = None
        self.comp_class = None
        self.ems_class = None
        self.flags = None
        self.index = index
        self.level = None
        self.phases = None
        self.prev_indx = None
        self.trace_class = None
        self.comp_class = None
        self.comp_class_desc = None
        self.connect_class = None
        self.connect_class_desc = None
        self.dead_state = None
        self.dead_state_desc = None
        self.description = None
        self.destn_id = None
        self.diagram_dressing = None
        self.diagram_dressing_desc = None
        self.dsh_dressing = None
        self.dsh_dressing_desc = None
        self.live_state = None
        self.live_state_desc = None
        self.normal_priority = None
        self.parent_id = None
        self.patch_number = None
        self.phase = None
        self.phases_present = None
        self.phases_present_desc = None
        self.priority = None
        self.record_id = None
        self.source_id = None
        self.status_desc = None
        self.sld_class = None
        self.sld_class_desc = None
        self.substation_id = None
        self.substation_class = None
        self.substation_class_desc = None
        self.status = None
        self.trace_class = None
        self.trace_class_desc = None

    def __repr__(self):
        return f"Component: {self.index} {self.component_id}"


class Trace:
    def __init__(self):
        # actual data from xml
        self.from_comp = None
        self.actual_comp = None
        self.name = None
        self.status = None
        self.expected_components = None
        self.expected_ends = None
        self.components = []
        self.ends = []

        # helper data
        self.all_components = dict()

    def __repr__(self):
        return f"Trace: from={self.from_comp} / {self.actual_comp} / {self.name} / {self.status}: components = {len(self.components)}/{self.expected_components}   ends = {len(self.ends)}/{self.expected_ends}"

    def load_component(self, component_id: str) -> Component:
        """
        Component factory
        :param component_id: component_id
        :return: Component instance
        """
        component = self.all_components.get(component_id)
        if component is None:
            component = Component(component_id=component_id)
            self.all_components[component_id] = component
        return component

    def load_trace_component(self, node):
        if node.tag != "component": raise Exception(f"{node.tag} is unexpected. It should be 'component'")
        records = node.findall("record")
        if len(records) != 1: raise Exception(f"must have exactly  1 <record>")
        component_id = records[0].attrib["id"]

        component = self.load_component(component_id)
        component.index = node.attrib.get("indx")

        for child in node:
            if child.tag == "record":
                for record_value in child:
                    if record_value.tag not in component.__dict__:
                        raise Exception(f"did not expect field  {record_value.tag} in recordtag {child.tag} for {component}")
                    component.__setattr__(record_value.tag, record_value.text)
                continue
            if len(child.attrib):
                raise Exception(f"did not expect attributes {child.attrib} in tag {child.tag}")
            if child.tag not in component.__dict__:
                raise Exception(f"did not expect field  {child.tag} in tag {node.tag}")
            component.__setattr__(child.tag, int(child.text))
        component.parent_id = None if component.parent_id is None else self.load_component(component.parent_id)
        component.source_id = None if component.source_id is None else self.load_component(component.source_id)
        component.destn_id = None if component.destn_id is None else self.load_component(component.destn_id)
        component.substation_id = None if component.substation_id is None else self.load_component(component.substation_id)




    def load_trace_from_xml(self, filename: str) -> bool:
        """
        Load an XML_trace result from file
        :param filename: full path and filename
        :return: Successfully or not
        """
        try:
            root = ElementTree.parse(filename).getroot()
            if root.tag != "traces": raise Exception("root is not <traces>")
            for trace  in root:
                if trace.tag != "trace": raise Exception(" <traces> child is not <trace>")
                self.from_comp, self.actual_comp, self.name, self.status = self.load_component(trace.attrib.get('from')), self.load_component(trace.attrib.get('actual')), trace.attrib.get('name'), trace.attrib.get('status')
                pop_keys(trace.attrib, True, 'from', 'actual', 'name', 'status')
                for child in trace:
                    if child.tag == "components":
                        self.expected_components = child.attrib.get('total')
                        pop_keys(child.attrib, True, 'total')
                        for sub_child in child:
                            self.load_trace_component(sub_child)

                    elif child.tag == "ends":
                        self.expected_ends = child.attrib.get('total')
                        pop_keys(child.attrib, True, 'total')
                    else:
                        raise Exception(f"Did no expect /traces/trace/{child.tag}")
        except Exception as e:
            print(e)
            return False
        return True




if __name__ == "__main__":
    tr = Trace()
    tr.load_trace_from_xml("c:/Temp/trace.xml")
    pass
