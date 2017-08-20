# Copyright (c) 2017 Alex Socha
# http://www.alexsocha.com/pynode

from pynode.src import pynode_core
import random

def pause(time):
    pynode_core.add_event(pynode_core.EventPause(time))
def delay(func, time, args=[], repeat=False):
    def execute():
        pynode_core.execute_function(func, args)
    if repeat:
        delay_id = pynode_core.timer.set_interval(execute, time)
        pynode_core.PynodeCoreGlobals.delay_type[delay_id] = 1
        return delay_id
    else:
        delay_id = pynode_core.timer.set_timeout(execute, time)
        pynode_core.PynodeCoreGlobals.delay_type[delay_id] = 0
        return delay_id
def cancel_delay(delay_id):
    if delay_id in pynode_core.PynodeCoreGlobals.delay_type:
        if pynode_core.PynodeCoreGlobals.delay_type[delay_id] == 1: pynode_core.timer.clear_interval(delay_id)
        else: pynode_core.timer.clear_timeout(delay_id)
        del pynode_core.PynodeCoreGlobals.delay_type[delay_id]
def clear_delays():
    delay_ids = list(pynode_core.PynodeCoreGlobals.delay_type.keys())
    for delay_id in delay_ids:
        cancel_delay(delay_id)

def print_debug(value):
    pynode_core.do_print(str(value) + "\n")

def register_click_listener(func):
    pynode_core.PynodeCoreGlobals.click_listener_func["f"] = func

class Color:
    def __init__(self, red, green, blue, transparent=False):
        self._red = red; self._green = green; self._blue = blue
        self._transparent = transparent

    @staticmethod
    def rgb(red, green, blue):
        return Color(red, green, blue)

    def hex_string(self):
        if self._transparent: return "transparent"
        else: return "#%02x%02x%02x" % (self._red, self._green, self._blue)

    def __str__(self):
        return "(" + str(self._red) + "," + str(self._green) + "," + str(self._blue) + ")"

    def red(self): return self._red
    def green(self): return self._green
    def blue(self): return self._blue

Color.RED = Color(180, 0, 0)
Color.GREEN = Color(0, 150, 0)
Color.BLUE = Color(0, 0, 200)
Color.YELLOW = Color(255, 215, 0)
Color.WHITE = Color(255, 255, 255)
Color.LIGHT_GREY = Color(199, 199, 199)
Color.GREY = Color(127, 127, 127)
Color.DARK_GREY = Color(82, 82, 82)
Color.BLACK = Color(0, 0, 0)
Color.TRANSPARENT = Color(0, 0, 0, True)

class CustomStyle:
    def __init__(self, size, color, outline=Color.TRANSPARENT):
        self._size = size
        self._color = color
        self._outline = outline
        self._has_outline = outline is not None
    def data(self, element):
        return str(self._size) + "," + self._color.hex_string() + "," + (element._color.hex_string() if self._outline is None else self._outline.hex_string()) + "," + str(self._has_outline)

class Node:
    def __init__(self, *args, **kwds):
        arg_id = kwds["id"] if "id" in kwds else args[0] if len(args) > 0 else pynode_core.next_user_id()
        arg_value = kwds["value"] if "value" in kwds else args[1] if len(args) > 1 else arg_id
        self._id = arg_id
        self._value = arg_value
        self._incident_edges = []
        self._attributes = {}
        self._priority = 0
        self._position = None
        self._is_pos_relative = False
        self._labels = ["", ""]
        self._size = 12
        self._color = Color.DARK_GREY
        self._value_style = CustomStyle(13, Color.WHITE, None)
        self._label_styles = [CustomStyle(10, Color.GREY), CustomStyle(10, Color.GREY)]
        self._internal_id = pynode_core.next_global_id()

    def set_value(self, value):
        self._value = value
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_value, [self._internal_id, str(value) if value is not None else ""]), self)
        return self
    def value(self):
        return self._value

    def incident_edges(self):
        return list(self._incident_edges)
    def incoming_edges(self):
        return [e for e in self._incident_edges if not e._directed or e._target == self]
    def outgoing_edges(self):
        return [e for e in self._incident_edges if not e._directed or e._source == self]

    def adjacent_nodes(self):
        return [e._source if e._target is self else e._target for e in self._incident_edges]
    def predecessor_nodes(self):
        return [e._source if e._target is self else e._target for e in self.incoming_edges()]
    def successor_nodes(self):
        return [e._source if e._target is self else e._target for e in self.outgoing_edges()]

    def degree(self): return len(self._incident_edges)
    def indegree(self): return len(self.incoming_edges())
    def outdegree(self): return len(self.outgoing_edges())

    def set_attribute(self, name, value):
        self._attributes[name] = value
        return self
    def attribute(self, name):
        return self._attributes[name] if name in self._attributes else None

    def set_priority(self, value):
        self._priority = value
        return self
    def priority(self):
        return self._priority

    def set_position(self, x, y, relative=False):
        self._position = [x, y]
        self._is_pos_relative = relative
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_position, [self._internal_id, x, y, relative]), self)
        return self
    def position(self): return pynode_core.js_node_get_position(self)

    def set_label(self, text, label_id=0):
        self._labels[label_id] = text
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_label, [self._internal_id, str(text) if text is not None else "", label_id]), self)
        return self
    def label(self, label_id=0):
        return self._labels[label_id]

    def set_size(self, size):
        self._size = size
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_size, [self._internal_id, size]), self)
        return self
    def size(self): return self._size

    def set_color(self, color):
        self._color = color
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_color, [self._internal_id, color.hex_string(), self._value_style.data(self)]), self)
        return self
    def color(self): return self._color

    def set_text_size(self, size):
        self._value_style._size = size
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_value_style, [self._internal_id, self._value_style.data(self)]), self)
        return self
    def set_text_color(self, color):
        self._value_style._color = color
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_value_style, [self._internal_id, self._value_style.data(self)]), self)
        return self
    def set_value_style(self, size=None, color=None, outline=-1):
        self._value_style = CustomStyle(self._value_style._size if size is None else size, self._value_style._color if color is None else color, self._value_style._outline if outline == -1 else outline)
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_value_style, [self._internal_id, self._value_style.data(self)]), self)
        return self
    def set_label_style(self, size=None, color=None, outline=None, label_id=None):
        if label_id is None or (label_id != 0 and label_id != 1):
            style1 = CustomStyle(self._label_styles[0]._size if size is None else size, self._label_styles[0]._color if color is None else color, self._label_styles[0]._outline if outline is None else outline)
            style2 = CustomStyle(self._label_styles[1]._size if size is None else size, self._label_styles[1]._color if color is None else color, self._label_styles[1]._outline if outline is None else outline)
            self._label_styles[0] = style1
            self._label_styles[1] = style2
            pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_label_style, [self._internal_id, self._label_styles[0].data(self), 0]), self)
            pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_label_style, [self._internal_id, self._label_styles[1].data(self), 1]), self)
        else:
            style = CustomStyle(self._label_styles[label_id]._size if size is None else size,Color.WHITE if color is None else color, outline)
            self._label_styles[label_id] = style
            pynode_core.add_event(pynode_core.Event(pynode_core.js_node_set_label_style, [self._internal_id, self._label_styles[label_id].data(self), label_id]), self)
        return self

    def highlight(self, *args, **kwds):
        arg_color = kwds["color"] if "color" in kwds else args[0] if len(args) > 0 else None
        arg_size = kwds["size"] if "size" in kwds else args[1] if len(args) > 1 else self._size * 1.5
        pynode_core.add_event(pynode_core.Event(pynode_core.js_node_highlight, [self._internal_id, arg_size, arg_color.hex_string() if arg_color is not None else None]), self)

    def id(self):
        return self._id

    def _data(self):
        d = {"id": self._internal_id, "label": str(self._value) if self._value is not None else "", "labelStyle": self._value_style.data(self), "topRightLabel": str(self._labels[0]) if self._labels[0] is not None else "", "topLeftLabel": str(self._labels[1]) if self._labels[1] is not None else "", "topRightLabelStyle": self._label_styles[0].data(self), "topLeftLabelStyle": self._label_styles[1].data(self), "r": self._size, "color": self._color.hex_string(), "fixed": (self._position is not None), "static": (self._position is not None), "ax": 0, "ay": 0, "rx": 0.0, "ry": 0.0, "relativePosition": False}
        if self._position is not None:
            if self._is_pos_relative:
                d["relativePosition"] = True
                d["rx"] = self._position[0]; d["ry"] = self._position[1]
            else:
                d["ax"] = self._position[0]; d["ay"] = self._position[1]
                d["x"] = self._position[0]; d["y"] = self._position[1]
        return d

    def __lt__(self, other): return self._priority < other._priority if isinstance(other, Node) else NotImplemented
    def __le__(self, other): return self._priority <= other._priority if isinstance(other, Node) else NotImplemented
    def __gt__(self, other): return self._priority > other._priority if isinstance(other, Node) else NotImplemented
    def __ge__(self, other): return self._priority >= other._priority if isinstance(other, Node) else NotImplemented

    def __str__(self):
        return str(self._id)


class Edge:
    def __init__(self, source, target, weight=None, directed=False):
        self._source = source
        self._target = target
        self._weight = weight
        self._directed = directed
        self._attributes = {}
        self._priority = 0
        self._width = 2
        self._color = Color.LIGHT_GREY
        self._weight_style = CustomStyle(10, Color.GREY)
        self._internal_id = pynode_core.next_global_id()

    def source(self, target=None):
        # Deprecated
        if target is not None: return self.other_node(target)
        return self._source
    def target(self, source=None):
        # Deprecated
        if source is not None: return self.other_node(source)
        return self._target

    def set_weight(self, weight=None):
        self._weight = weight
        pynode_core.add_event(pynode_core.Event(pynode_core.js_edge_set_weight, [self._internal_id, str(weight) if weight is not None else ""]), self)
        return self
    def weight(self):
        return self._weight

    def set_directed(self, directed=True):
        self._directed = directed
        pynode_core.add_event(pynode_core.Event(pynode_core.js_edge_set_directed, [self._internal_id, self._directed]), self)
        return self
    def directed(self):
        return self._directed

    def other_node(self, node):
        return self._target if (self._source is node or self._source._id == node) else self._source

    def set_attribute(self, name, value):
        self._attributes[name] = value
        return self
    def attribute(self, name):
        return self._attributes[name] if name in self._attributes else None

    def set_priority(self, value):
        self._priority = value
        return self
    def priority(self):
        return self._priority

    def set_width(self, width=2):
        self._width = width
        pynode_core.add_event(pynode_core.Event(pynode_core.js_edge_set_width, [self._internal_id, width]), self)
        return self
    def width(self): return self._width

    def set_color(self, color=Color.LIGHT_GREY):
        self._color = color
        pynode_core.add_event(pynode_core.Event(pynode_core.js_edge_set_color, [self._internal_id, color.hex_string()]), self)
        return self
    def color(self): return self._color

    def set_weight_style(self, size=None, color=None, outline=None):
        self._weight_style = CustomStyle(self._weight_style._size if size is None else size, self._weight_style._color if color is None else color, self._weight_style._outline if outline is None else outline)
        pynode_core.add_event(pynode_core.Event(pynode_core.js_edge_set_weight_style, [self._internal_id, self._weight_style.data(self)]), self)
        return self

    def highlight(self, *args, **kwds):
        arg_color = kwds["color"] if "color" in kwds else args[0] if len(args) > 0 else None
        arg_width = kwds["width"] if "width" in kwds else args[1] if len(args) > 1 else self._width * 2
        pynode_core.add_event(pynode_core.Event(pynode_core.js_edge_highlight, [self._internal_id, arg_width, arg_color.hex_string() if arg_color is not None else None]), self)

    def traverse(self, initial_node=None, color=Color.RED, keep_path=True):
        if not graph.has_edge(self): return
        start = graph.node(initial_node) if initial_node is not None else self._source
        if not graph.has_node(start): return
        pynode_core.add_event(pynode_core.Event(pynode_core.js_edge_traverse, [self._internal_id, start._internal_id, color.hex_string(), keep_path]), self)

    def _data(self):
        d = {"id": self._internal_id, "source": self._source._internal_id, "target": self._target._internal_id, "weight": str(self._weight) if self._weight is not None else "", "directed": self._directed, "lineWidth": self._width, "weightStyle": self._weight_style.data(self), "stroke": self._color.hex_string()}
        return d

    def __lt__(self, other): return self._priority < other._priority if isinstance(other, Edge) else NotImplemented
    def __le__(self, other): return self._priority <= other._priority if isinstance(other, Edge) else NotImplemented
    def __gt__(self, other): return self._priority > other._priority if isinstance(other, Edge) else NotImplemented
    def __ge__(self, other): return self._priority >= other._priority if isinstance(other, Edge) else NotImplemented

    def __str__(self):
        return "(" + str(self._source) + "," + str(self._target) + ")"


class Graph:
    def __init__(self):
        self._nodes = {}
        self._edges = []
        self._has_edge_cache = {}
        self._spread = 80

    def add_node(self, *args, **kwds):
        if "node" in kwds: n = kwds["node"]
        elif len(args) > 0 and isinstance(args[0], Node): n = args[0]
        else: n = Node(*args, **kwds)
        if n._id in self._nodes: raise Exception("Duplicate node '" + str(n._id) + "'")
        self._nodes[n._id] = n
        pynode_core.add_event(pynode_core.Event(pynode_core.js_add_node, [n._data()]))
        pause(25)
        return n

    def remove_node(self, node):
        n = self.node(node)
        pynode_core.enable_events(False)
        for e in n.incident_edges():
            self.remove_edge(e)
        pynode_core.enable_events(True)
        del self._nodes[n._id]
        pynode_core.add_event(pynode_core.Event(pynode_core.js_remove_node, [n._internal_id]))
        pause(25)
        return n

    def node(self, id):
        if isinstance(id, Node) and id._id in self._nodes:
            return id
        elif id in self._nodes:
            return self._nodes[id]
        else:
            return None

    def nodes(self):
        return list(self._nodes.values())

    def add_edge(self, *args, **kwds):
        if "edge" in kwds: e = kwds["edge"]
        elif len(args) > 0 and isinstance(args[0], Edge): e = args[0]
        else:
            arg_source = kwds["source"] if "source" in kwds else args[0]
            arg_target = kwds["target"] if "target" in kwds else args[1]
            arg_weight = kwds["source"] if "source" in kwds else args[2] if len(args) > 2 else None
            arg_directed = kwds["directed"] if "directed" in kwds else args[3] if len(args) > 3 else False
            e = Edge(arg_source, arg_target, arg_weight, arg_directed)
        if self.has_edge(e): raise Exception("Instance of edge '" + str(e) + "' already in graph.")
        original_source = e._source
        original_target = e._target
        e._source = graph.node(e._source)
        e._target = graph.node(e._target)
        if e._source is None: raise Exception("Node '" + str(original_source) + "' doesn't exist.")
        if e._target is None: raise Exception("Node '" + str(original_target) + "' doesn't exist.")
        e._source._incident_edges.append(e)
        e._target._incident_edges.append(e)
        self._edges.append(e)
        self._has_edge_cache[e] = True
        pynode_core.add_event(pynode_core.Event(pynode_core.js_add_edge, [e._data()]))
        return e

    def remove_edge(self, *args, **kwds):
        remove_multiple = False
        if "edge" in kwds: edge = kwds["edge"]
        elif len(args) > 0 and isinstance(args[0], Edge): edge = args[0]
        else:
            arg_source = kwds["node1"] if "node1" in kwds else args[0]
            arg_target = kwds["node2"] if "node2" in kwds else args[1]
            arg_directed = kwds["directed"] if "directed" in kwds else args[2] if len(args) > 2 else False
            remove_multiple = True
        if remove_multiple:
            edge_list = self.edges_between(arg_source, arg_target, arg_directed)
            self.remove_all(edge_list)
            return edge_list
        else:
            edge._source._incident_edges.remove(edge)
            edge._target._incident_edges.remove(edge)
            self._edges.remove(edge)
            del self._has_edge_cache[edge]
            pynode_core.add_event(pynode_core.Event(pynode_core.js_remove_edge, [edge._internal_id]))
            return edge

    def edges(self):
        return list(self._edges)

    def set_directed(self, directed=True):
        for e in self._edges:
            e.set_directed(directed)

    def has_node(self, node):
        return self.node(node) is not None

    def has_edge(self, edge):
        return edge in self._has_edge_cache

    def adjacent(self, node1, node2, directed=False):
        if not self.has_node(node1) or not self.has_node(node2): return False
        for n in (self.node(node1).successor_nodes() if directed else self.node(node1).adjacent_nodes()):
            if n is self.node(node2): return True
        return False
    # Deprecated
    def adjacent_directed(self, source, target):
        return self.adjacent(source, target, True)

    def edges_between(self, node1, node2, directed=False):
        if not self.has_node(node1) or not self.has_node(node2): return []
        edge_list = self.node(node1).outgoing_edges() if directed else self.node(node1)._incident_edges
        return [edge for edge in edge_list if edge._target is self.node(node2) or edge._source is self.node(node2)]
    # Deprecated
    def edges_between_directed(self, source, target):
        return self.edges_between(source, target, True)

    def adjacency_matrix(self):
        m = {}
        for r in self._nodes.values():
            row = {}
            for c in self._nodes.values(): row[c._id] = 0
            m[r._id] = row
        for r in self._nodes.values():
            for c in r.successor_nodes():
                m[r._id][c._id] += 1
        return m

    @staticmethod
    def random(order, size, connected=True, mutligraph=False, initial_id=0):
        nodes = []
        edges = []
        adjacency_matrix = [[0 for c in range(order)] for r in range(order)]
        edges_remaining = size
        id_list = random.sample(range(initial_id, initial_id + order), order)
        for i in range(order):
            node = Node(id_list[i])
            if connected and edges_remaining > 0 and len(nodes) > 0:
                connected_node = nodes[random.randint(0, len(nodes) - 1)]
                if random.randint(0, 1) == 0: edges.append(Edge(node, connected_node))
                else: edges.append(Edge(connected_node, node))
                adjacency_matrix[id_list[i] - initial_id][connected_node._id - initial_id] += 1
                adjacency_matrix[connected_node._id - initial_id][id_list[i] - initial_id] += 1
                edges_remaining -= 1
            nodes.append(node)
        possible_edges = [(i, j) for i in range(order) for j in range(order)]
        random.shuffle(possible_edges)
        for e in possible_edges:
            if edges_remaining <= 0: break
            if (adjacency_matrix[e[0]][e[1]] == 0 and e[0] != e[1]) or mutligraph:
                edges.append(Edge(e[0] + initial_id, e[1] + initial_id))
                adjacency_matrix[e[0]][e[1]] += 1
                adjacency_matrix[e[1]][e[0]] += 1
                edges_remaining -= 1
        return nodes + edges

    def add_all(self, elements):
        new_elements = []
        pynode_core.enable_events(False)
        for x in elements:
            if isinstance(x, Node): new_elements.append((0, self.add_node(x)._data()))
            elif isinstance(x, Edge): new_elements.append((1, self.add_edge(x)._data()))
            else: new_elements.append((0, self.add_node(Node(x))._data()))
        pynode_core.enable_events(True)
        pynode_core.add_event(pynode_core.Event(pynode_core.js_add_all, [new_elements]))
        pause(55)

    def remove_all(self, elements):
        new_elements = []
        pynode_core.enable_events(False)
        for x in elements:
            if isinstance(x, Node): new_elements.append((0, self.remove_node(x)._data()))
            elif isinstance(x, Edge): new_elements.append((1, self.remove_edge(x)._data()))
            else: new_elements.append((0, self.remove_node(self.node(x))._data()))
        pynode_core.enable_events(True)
        pynode_core.add_event(pynode_core.Event(pynode_core.js_remove_all, [new_elements]))
        pause(55)

    def order(self): return len(self._nodes.values())
    def size(self): return len(self._edges)

    def set_spread(self, spread=80):
        self._spread = spread
        pynode_core.add_event(pynode_core.Event(pynode_core.js_set_spread, [spread]))

    def clear(self):
        self._reset()
        pynode_core.add_event(pynode_core.Event(pynode_core.js_clear, []))

    def _reset(self):
        self._nodes = {}
        self._edges = []
        self._has_edge_cache = {}

def _exec_code(src):
    namespace = globals()
    namespace["__name__"] = "__main__"
    exec(src, namespace, namespace)

graph = Graph()

