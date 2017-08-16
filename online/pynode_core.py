import sys
import time
import traceback
import javascript
import random
from browser import document, window, alert, timer
from browser.local_storage import storage

import pynode_graphlib

class PynodeCoreGlobals():
    GLOBAL_ID = 0
    GLOBAL_USER_ID = 0
    event_queue = []
    event_timer = None
    update_timer = None
    do_events = True
    has_ended = False
    do_update = True
    fix_layout = True
    did_fix_layout = False
    did_update_layout = False
    delay_type = {}
    click_listener_func = {"f": None}
    positioning_counter = None
    error = ""

def enable_events(enable):
    PynodeCoreGlobals.do_events = enable
def enable_update(enable):
    PynodeCoreGlobals.do_update = enable

def next_global_id():
    id_value = PynodeCoreGlobals.GLOBAL_ID
    PynodeCoreGlobals.GLOBAL_ID += 1
    return id_value

def next_user_id():
    id_value = PynodeCoreGlobals.GLOBAL_USER_ID
    PynodeCoreGlobals.GLOBAL_USER_ID += 1
    return id_value

class Event():
    def __init__(self, func, args):
        self.func = func
        self.args = args
    def execute(self):
        self.func(*self.args)
class EventPrint(Event):
    def __init__(self, func, args):
        super().__init__(func, args)
class EventPause():
    def __init__(self, time):
        self.time = time

def add_event(event, source=None):
    if PynodeCoreGlobals.do_events:
        if source is not None:
            if isinstance(source, pynode_graphlib.Node) and not pynode_graphlib.graph.has_node(source): return
            if isinstance(source, pynode_graphlib.Edge) and not pynode_graphlib.graph.has_edge(source): return
        PynodeCoreGlobals.event_queue.append(event)

def format_string_HTML(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>").replace("\"", "&quot;").replace("'", "&apos;").replace(" ", "&nbsp;")

def do_print(s, color=None):
    if color is not None: window.writeOutput("<p style='display:inline;color:" + color + ";'>" + format_string_HTML(s) + "</p>", True)
    else: window.writeOutput("<p style='display:inline;'>" + format_string_HTML(s) + "</p>", True)

def do_print_formatted(s):
    window.writeOutput(s, True)

class PrintOutput:
    def write(self, data):
        add_event(EventPrint(do_print, [str(data)]))
        #do_print(data)
    def flush(self):
        pass

class ErrorOutput:
    def write(self, data):
        PynodeCoreGlobals.error += "<p style='display:inline;color:red;'>" + format_string_HTML(str(data)) + "</p>"
        #document["console"].innerHTML += "<p style='display:inline;color:red;'>" + format_string_HTML(str(data)) + "</p>"
    def flush(self):
        pass

sys.stdout = PrintOutput()
sys.stderr = ErrorOutput()

def end_playing():
    if not PynodeCoreGlobals.has_ended:
        clear_button_run()
        document["runPlay"].style.display = "inherit"
        document["run"].bind("click", button_play)
        do_print("Done\n", color="green")
    PynodeCoreGlobals.has_ended = True

def play_events():
    try:
        try:
            if len(PynodeCoreGlobals.event_queue) > 0:
                event = PynodeCoreGlobals.event_queue[0]
                delay = 5
                if isinstance(event, EventPause):
                    delay = event.time
                else:
                    event.execute()
                del PynodeCoreGlobals.event_queue[0]
                PynodeCoreGlobals.event_timer = timer.set_timeout(play_events, delay)
            else:
                PynodeCoreGlobals.event_timer = timer.set_timeout(play_events, 100)
                end_playing()
        except:
            traceback.print_exc(file=sys.stderr)
            handle_exception(False)
            end_playing()
        sys.exit()
    except:
        pass

def handle_exception(emptyPrint=True):
    try:
        if PynodeCoreGlobals.event_queue is not None and emptyPrint:
            for event in PynodeCoreGlobals.event_queue:
                if isinstance(event, EventPrint):
                    event.execute()
        do_print_formatted(PynodeCoreGlobals.error)
    except:
        pass

def execute_function(func, args):
    try:
        func(*args)
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        handle_exception(False)

def reset(clear_console=True):
    try:
        PynodeCoreGlobals.GLOBAL_USER_ID = 0
        if clear_console: window.writeOutput("", False)
        pynode_graphlib.graph._reset()
        pynode_graphlib.clear_delays()
        js_clear()
        if PynodeCoreGlobals.event_timer is not None: timer.clear_timeout(PynodeCoreGlobals.event_timer)
        if PynodeCoreGlobals.update_timer is not None: timer.clear_timeout(PynodeCoreGlobals.update_timer)
        PynodeCoreGlobals.event_queue = [EventPause(100)]
        PynodeCoreGlobals.fix_layout = True
        PynodeCoreGlobals.did_fix_layout = False
        PynodeCoreGlobals.did_update_layout = False
        PynodeCoreGlobals.has_ended = False
        PynodeCoreGlobals.delay_type = {}
        PynodeCoreGlobals.positioning_counter = 0
        PynodeCoreGlobals.error = ""
        window.set_layout_type()
        window.registerClickListener(node_click)
        window.clickListenerFunc = None
    except:
        timer.set_timeout(reset, 20)

def clear_button_run():
    document["runPlay"].style.display = "none"
    document["runPlayLoad"].style.display = "none"
    document["runPause"].style.display = "none"
    document["runResume"].style.display = "none"
    document["run"].unbind("click")
    document["run"].bind("click", save_code)

def button_play(event):
    reset()
    clear_button_run()
    document["runPlayLoad"].style.display = "inherit"
    document["run"].bind("click", button_pause)
    timer.set_timeout(do_play, 20)

def do_play():
    src = window.getCode()
    try:
        success = True
        try:
            pynode_graphlib._exec_code(src)
        except Exception as exc:
            traceback.print_exc(file=sys.stderr)
            handle_exception()
            success = False
        clear_button_run()
        document["runPause"].style.display = "inherit"
        document["run"].bind("click", button_pause)
        if success: play_events()
        else: end_playing()
        sys.exit()
    except:
        pass

def button_pause(event):
    clear_button_run()
    document["runResume"].style.display = "inherit"
    document["run"].bind("click", button_resume)
    if PynodeCoreGlobals.event_timer is not None:
        timer.clear_timeout(PynodeCoreGlobals.event_timer)

def button_resume(event):
    clear_button_run()
    document["runPause"].style.display = "inherit"
    document["run"].bind("click", button_pause)
    PynodeCoreGlobals.event_timer = timer.set_timeout(play_events, 0)

def button_stop(event):
    clear_button_run()
    document["runPlay"].style.display = "inherit"
    document["run"].bind("click", button_play)
    reset(False)
    if PynodeCoreGlobals.event_timer is not None:
        timer.clear_timeout(PynodeCoreGlobals.event_timer)

def button_restart(event):
    button_play(event)

def node_click(node_id):
    node = None
    if pynode_graphlib.graph is not None and PynodeCoreGlobals.click_listener_func["f"] is not None:
        for n in pynode_graphlib.graph.nodes():
            if n._internal_id == node_id: node = n
        if node is not None:
            execute_function(PynodeCoreGlobals.click_listener_func["f"], [node])

def save_code(event):
    window.saveCode()

def update_instant():
    try: window.greuler_instance.update({"skipLayout": True})
    except: PynodeCoreGlobals.update_timer = timer.set_timeout(update_instant, 20)

def update_instant_layout():
    try: window.updateLayout()
    except: PynodeCoreGlobals.update_timer = timer.set_timeout(update_instant_layout, 20)

def refresh_layout():
    window.refreshLayout()

def js_update(layout=True):
    if PynodeCoreGlobals.do_update:
        try:
            if layout:
                PynodeCoreGlobals.update_timer = timer.set_timeout(update_instant_layout, 50)
                window.updateLayout()
            else:
                PynodeCoreGlobals.update_timer = timer.set_timeout(update_instant, 50)
                window.greuler_instance.update({"skipLayout": True})
        except:
            pass

def js_add_node(data):
    if not data["static"]:
        x = 0; y = 0
        size = int(PynodeCoreGlobals.positioning_counter ** 0.5)
        if size**2 != PynodeCoreGlobals.positioning_counter: size += 1
        if size % 2 == 0: size += 1
        half_size = int(size / 2.0)
        difference = size**2 - PynodeCoreGlobals.positioning_counter
        if difference <= size: y = -half_size; x = -half_size + (size - difference)
        elif difference <= (size * 2) - 1: y = -half_size + (difference - size); x = -half_size
        elif difference <= (size * 3) - 2: y = half_size; x = -half_size + (difference - (size * 2)) + 1
        elif difference <= (size * 4) - 3: y = -half_size + (size - (difference - (size * 3) + 3)); x = half_size
        data["x"] = (window.greuler_instance.options.data.size[0] / 2.0) + (x * 25); data["y"] = (window.greuler_instance.options.data.size[1] / 2.0) + (-y * 25)
        PynodeCoreGlobals.positioning_counter += 1
    window.greuler_instance.graph.addNode(data)
    js_update(True)
    timer.set_timeout(refresh_layout, 65)

def js_remove_node(node_id):
    window.greuler_instance.graph.removeNode({"id": node_id})
    js_update(True)

def js_add_edge(data):
    window.greuler_instance.graph.addEdge(data)
    if len(window.greuler_instance.graph.edges) >= len(window.greuler_instance.graph.nodes) - 3 and (len(window.greuler_instance.graph.nodes) - 2) % 9 == 0: PynodeCoreGlobals.positioning_counter = 0
    js_update(True)

def js_remove_edge(edge_id):
    window.greuler_instance.graph.removeEdge({"id": edge_id})
    js_update(True)

def js_add_all(element_data):
    enable_update(False)
    for x in element_data:
        if x[0] == 0: js_add_node(x[1])
        elif x[0] == 1: js_add_edge(x[1])
    enable_update(True)
    js_update(True)

def js_remove_all(element_data):
    enable_update(False)
    for x in element_data:
        if x[0] == 0: js_remove_node(x[1]["id"])
        elif x[0] == 1: js_remove_edge(x[1]["id"])
    enable_update(True)
    js_update(True)

def js_set_spread(spread):
    window.greuler_instance.graph.linkDistance = spread
    window.greuler_instance.options.data.linkDistance = spread
    js_update(True)

def js_clear():
    window.greuler_instance.graph.removeEdges(window.greuler_instance.graph.edges)
    window.greuler_instance.graph.removeNodes(window.getGraphNodes())
    js_update(True)

def js_node_set_value(node_id, value):
    if window.greuler_instance.graph.hasNode({"id": node_id}):
        window.greuler_instance.graph.getNode({"id": node_id}).label = value
        js_update(False)

def js_node_set_position(node_id, x, y, relative):
    if window.greuler_instance.graph.hasNode({"id": node_id}):
        n = window.greuler_instance.graph.getNode({"id": node_id})
        if x is None or y is None:
            n.fixed = False
            n.static = True
            return
        n.fixed = True
        n.static = True
        n.relativePosition = relative
        if relative: n.rx = x; n.ry = y
        else: n.ax = x; n.ay = y; n.x = x; n.y = y
        timer.set_timeout(update_instant_layout, 215)

def js_node_get_position(node):
    if window.greuler_instance.graph.hasNode({"id": node._internal_id}):
        return (int(window.greuler_instance.graph.getNode({"id": node._internal_id}).x), int(window.greuler_instance.graph.getNode({"id": node._internal_id}).y))
    elif node._position is None: return None
    else:
        if node._is_pos_relative: return (int(node._position[0] * window.greuler_instance.options.data.size[0]), int(node._position[1] * window.greuler_instance.options.data.size[1]))
        else: return (int(node._position[0]), int(node._position[1]))

def js_node_set_label(node_id, text, label_id):
    if window.greuler_instance.graph.hasNode({"id": node_id}):
        n = window.greuler_instance.graph.getNode({"id": node_id})
        if label_id == 0: n.topRightLabel = text
        elif label_id == 1: n.topLeftLabel = text
        js_update(False)

def js_node_set_size(node_id, size):
    if window.greuler_instance.graph.hasNode({"id": node_id}):
        window.greuler_instance.graph.getNode({"id": node_id}).r = size
        window.greuler_instance.selector.getNode({"id": node_id}).transition("highlight_node_size").duration(0)
        window.greuler_instance.selector.getNode({"id": node_id}).transition("node_size").duration(500).attr("r", size)
        js_update(True)

def js_node_set_color(node_id, color, text_style):
    if window.greuler_instance.graph.hasNode({"id": node_id}):
        window.greuler_instance.graph.getNode({"id": node_id}).color = color
        window.greuler_instance.graph.getNode({"id": node_id}).labelStyle = text_style
        window.greuler_instance.selector.getNode({"id": node_id}).transition("highlight_node_color").duration(0)
        window.greuler_instance.selector.getNodeOuter({"id": node_id}).selectAll("text.label").transition("highlight_node_outline").duration(0)
        window.greuler_instance.selector.getNode({"id": node_id}).transition("node_color").duration(500).attr("fill", color)
        if str(text_style).split(",")[3] == "False": window.greuler_instance.selector.getNodeOuter({"id": node_id}).selectAll("text.label").transition("node_stroke_color").duration(500).attr("stroke", str(text_style).split(",")[2])
        js_update(False)

def js_node_set_value_style(node_id, style):
    if window.greuler_instance.graph.hasNode({"id": node_id}):
        window.greuler_instance.graph.getNode({"id": node_id}).labelStyle = style
        window.greuler_instance.selector.getNodeOuter({"id": node_id}).selectAll("text.label").transition("highlight_node_outline").duration(0)
        window.greuler_instance.selector.getNodeOuter({"id": node_id}).selectAll("text.label").transition("node_stroke_color").duration(0)
        if str(style).split(",")[3] == "False": window.greuler_instance.selector.getNodeOuter({"id": node_id}).selectAll("text.label").attr("stroke", str(style).split(",")[2])
        js_update(False)

def js_node_set_label_style(node_id, style, label_id):
    if window.greuler_instance.graph.hasNode({"id": node_id}):
        if label_id == 0: window.greuler_instance.graph.getNode({"id": node_id}).topRightLabelStyle = style
        elif label_id == 1: window.greuler_instance.graph.getNode({"id": node_id}).topLeftLabelStyle = style
        js_update(False)

def js_node_highlight(node_id, size=None, color=None):
    if window.greuler_instance.graph.hasNode({"id": node_id}):
        data = {}
        if size is not None: data["size"] = size
        if color is not None: data["color"] = color
        window.greuler_instance.selector.highlightNode({"id": node_id}, data)

def js_edge_set_weight(edge_id, weight):
    if window.greuler_instance.graph.hasEdge({"id": edge_id}):
        window.greuler_instance.graph.getEdge({"id": edge_id}).weight = weight
        js_update(False)

def js_edge_set_directed(edge_id, directed):
    if window.greuler_instance.graph.hasEdge({"id": edge_id}):
        window.greuler_instance.graph.getEdge({"id": edge_id}).directed = directed
        js_update(False)

def js_edge_set_width(edge_id, width):
    if window.greuler_instance.graph.hasEdge({"id": edge_id}):
        window.greuler_instance.graph.getEdge({"id": edge_id}).lineWidth = width
        window.greuler_instance.selector.getEdge({"id": edge_id}).transition("highlight_edge_width").duration(0)
        window.greuler_instance.selector.getEdge({"id": edge_id}).transition("edge_width").duration(500).attr("stroke-width", width)
        js_update(False)

def js_edge_set_color(edge_id, color):
    if window.greuler_instance.graph.hasEdge({"id": edge_id}):
        window.greuler_instance.graph.getEdge({"id": edge_id}).stroke = color
        animate_edge = window.greuler_instance.selector.getEdge({"id": edge_id})
        window.greuler_instance.selector.getEdge({"id": edge_id}).transition("highlight_edge_color").duration(0)
        animate_edge.transition("edge_color").duration(500).attr("stroke", color)

def js_edge_set_weight_style(edge_id, style):
    if window.greuler_instance.graph.hasEdge({"id": edge_id}):
        window.greuler_instance.graph.getEdge({"id": edge_id}).weightStyle = style
        js_update(False)

def js_edge_highlight(edge_id, width=None, color=None):
    if window.greuler_instance.graph.hasEdge({"id": edge_id}):
        data = {}
        if width is not None: data["width"] = width
        if color is not None: data["color"] = color
        window.greuler_instance.selector.highlightEdge({"id": edge_id}, data)

def js_edge_traverse(edge_id, initial_node_id, color, keep_path):
    if window.greuler_instance.graph.hasEdge({"id": edge_id}):
        window.greuler_instance.selector.traverseEdge({"id": edge_id}, {"stroke": color, "keepStroke": keep_path}, initial_node_id)
