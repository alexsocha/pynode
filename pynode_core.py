import sys
import time
import traceback
import javascript
import random
import json
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
        if isinstance(event, Event) and isinstance(event.func, str) and event.func.startswith("js_"):
            event.args = [event.func, json.dumps(event.args)]
            event.func = window["js_run_function"]
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

def js_clear():
    window.greuler_instance.graph.removeEdges(window.greuler_instance.graph.edges)
    window.greuler_instance.graph.removeNodes(window.getGraphNodes())
    js_update(True)

# This is a workaround for a feature that should be implemented properly but isn't. Try not to use it.
def js_node_get_position(node):
    if window.greuler_instance.graph.hasNode({"id": node._internal_id}):
        return (int(window.greuler_instance.graph.getNode({"id": node._internal_id}).x), int(window.greuler_instance.graph.getNode({"id": node._internal_id}).y))
    elif node._position is None: return None
    else:
        if node._is_pos_relative: return (int(node._position[0] * window.greuler_instance.options.data.size[0]), int(node._position[1] * window.greuler_instance.options.data.size[1]))
        else: return (int(node._position[0]), int(node._position[1]))

# These functions have been moved over to JavaScript
js_add_node = "js_add_node"
js_remove_node = "js_remove_node"
js_add_edge = "js_add_edge"
js_remove_edge = "js_remove_edge"
js_add_all = "js_add_all"
js_remove_all = "js_remove_all"
js_set_spread = "js_set_spread"
js_node_set_value = "js_node_set_value"
js_node_set_position = "js_node_set_position"
js_node_set_label = "js_node_set_label"
js_node_set_size = "js_node_set_size"
js_node_set_color = "js_node_set_color"
js_node_set_value_style = "js_node_set_value_style"
js_node_set_label_style = "js_node_set_label_style"
js_node_highlight = "js_node_highlight"
js_edge_set_weight = "js_edge_set_weight"
js_edge_set_directed = "js_edge_set_directed"
js_edge_set_width = "js_edge_set_width"
js_edge_set_color = "js_edge_set_color"
js_edge_set_weight_style = "js_edge_set_weight_style"
js_edge_highlight = "js_edge_highlight"
js_edge_traverse = "js_edge_traverse"
