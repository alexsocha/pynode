# Copyright (c) 2017 Alex Socha
# http://www.alexsocha.com/pynode

import sys
import time
import traceback
import json
from threading import Thread
from threading import Timer as ThreadingTimer

from pynode.src import pynode_graphlib
from pynode.src import communicate

class PynodeCoreGlobals():
    GLOBAL_ID = 0
    GLOBAL_USER_ID = 0
    GLOBAL_DELAY_ID = 0
    event_timer = None
    do_events = True
    delay_type = {}
    delay_object = {}
    click_listener_func = {"f": None}

def enable_events(enable):
    PynodeCoreGlobals.do_events = enable

# Automatic internal IDs for nodes and edges
def next_global_id():
    id_value = PynodeCoreGlobals.GLOBAL_ID
    PynodeCoreGlobals.GLOBAL_ID += 1
    return id_value

# Automatic IDs for nodes
def next_user_id():
    id_value = PynodeCoreGlobals.GLOBAL_USER_ID
    PynodeCoreGlobals.GLOBAL_USER_ID += 1
    return id_value

# Automatic IDs for delays
def next_delay_id():
    id_value = PynodeCoreGlobals.GLOBAL_DELAY_ID
    PynodeCoreGlobals.GLOBAL_DELAY_ID += 1
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

def run_javascript_func(name, args=[]):
    # Send the name of the JavaScript function, and a list of arguments as a JSON string
    communicate.send_data(name + ":" + json.dumps(args))

def add_event(event, source=None):
    if PynodeCoreGlobals.do_events:
        if source is not None:
            if isinstance(source, pynode_graphlib.Node) and not pynode_graphlib.graph.has_node(source): return
            if isinstance(source, pynode_graphlib.Edge) and not pynode_graphlib.graph.has_edge(source): return
        if isinstance(event, EventPause):
            time.sleep(event.time / 1000.0)
        else:

            run_javascript_func(event.func, event.args)

def execute_function(func, args):
    try: func(*args)
    except: traceback.print_exc(file=sys.stderr)

def execute_function_async(func, args):
    t = Thread(target=execute_function, args=[func, args])
    t.daemon = True
    t.start()

def reset():
    try:
        PynodeCoreGlobals.GLOBAL_USER_ID = 0
        pynode_graphlib.graph._reset()
        pynode_graphlib.clear_delays()
        PynodeCoreGlobals.delay_type = {}
        run_javascript_func("js_clear")
    except: pass


def node_click(node_id):
    node = None
    if pynode_graphlib.graph is not None and PynodeCoreGlobals.click_listener_func["f"] is not None:
        for n in pynode_graphlib.graph.nodes():
            if n._internal_id == node_id: node = n
        if node is not None:
            execute_function_async(PynodeCoreGlobals.click_listener_func["f"], [node])

def execute_interval_func(timer_id, func, time):
    t = ThreadingTimer(time / 1000.0, execute_interval_func, (timer_id, func, time))
    PynodeCoreGlobals.delay_object[timer_id] = t
    t.start()
    func()

# An implementation of the JavaScript setTimeout and setInterval functions
class Timer:
    def set_timeout(self, func, time):
        timer_id = next_delay_id()
        t = ThreadingTimer(time / 1000.0, func)
        PynodeCoreGlobals.delay_object[timer_id] = t
        t.start()
        return timer_id
    def set_interval(self, func, time):
        timer_id = next_delay_id()
        execute_interval_func(timer_id, func, time)
        return timer_id
    def clear_timeout(self, timer_id):
        PynodeCoreGlobals.delay_object[timer_id].cancel()
        pass
    def clear_interval(self, timer_id):
        PynodeCoreGlobals.delay_object[timer_id].cancel()
        pass

def do_print(s):
    print(s)
    
timer = Timer()
js_update = "js_update"
js_add_node = "js_add_node"
js_remove_node = "js_remove_node"
js_add_edge = "js_add_edge"
js_remove_edge = "js_remove_edge"
js_add_all = "js_add_all"
js_remove_all = "js_remove_all"
js_set_spread = "js_set_spread"
js_clear = "js_clear"
js_node_set_value = "js_node_set_value"
js_node_set_position = "js_node_set_position"
js_node_get_position = "js_node_get_position"
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
