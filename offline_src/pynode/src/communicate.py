# Copyright (c) 2017 Alex Socha
# http://www.alexsocha.com/pynode

import subprocess
import time
import traceback
import sys
import os
from threading import Thread

from pynode.src import update
from pynode.src import pynode_core

# The location of the main.py file
APP_DIR = os.path.join(os.path.dirname(__file__), "../")

operating_system = None
pynode_process = None

monitor_thread = None
update_thread = None
run_thread = None

is_running = True

def set_run_function(func):
    global run_function
    run_function = func

def execute_run_function():
    try:
        pynode_core.reset()
        run_function()
        time.sleep(0.1)
        pynode_core.run_javascript_func("end_running")
    except: traceback.print_exc(file=sys.stderr)

def send_data(s):
    # Format the string correctly for JavaScript
    s = s.replace("\\n", "\\\\n")
    pynode_process.stdin.write(("pynode:" + s + "\n").encode())
    pynode_process.stdin.flush()

def recieve_data(s):
    try:
        if s.startswith("pynode:"):
            data = s[len("pynode:"):].strip()
            if data == "run":
                global run_thread
                run_thread = Thread(target=execute_run_function)
                run_thread.daemon = True
                run_thread.start()
            if data == "exit":
                pynode_process.kill()
                global is_running
                is_running = False
                return False
            if data.startswith("click:"):
                args = data.split(":")
                pynode_core.node_click(int(args[1]))
    except: pass
    return True

            
def monitor_data():
    try:
        while True:
            line = pynode_process.stdout.readline()
            if line is not None and line != "":
                if recieve_data(line.decode()) == False:
                    break
    except: pass
    wait_for_close()

def wait_for_close():
    try:
        pynode_process.wait()
        if update_thread is not None and update.is_updating:
            update_thread.join()
    except Exception as e:
        print(e)
    sys.exit(0)


def open_connection():
    try:
        file = open(os.path.join(os.path.dirname(__file__), "../cef/os.txt"))
        operating_system = file.readlines()[0].strip()
        file.close()

        global update_thread
        update_thread = Thread(target=update.check_update)
        update_thread.daemon = True
        update_thread.start()

        global pynode_process
        if operating_system == "win64":
            pynode_process = subprocess.Popen([os.path.join(APP_DIR, "cef/win64/pynode.exe")], shell=False, cwd=APP_DIR, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif operating_system == "win32":
            pynode_process = subprocess.Popen([os.path.join(APP_DIR, "cef/win32/pynode.exe")], shell=False, cwd=APP_DIR, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif operating_system == "macosx":
            pynode_process = subprocess.Popen([os.path.join(APP_DIR, "cef/macosx/pynode.app/Contents/MacOS/pynode")], shell=False, cwd=APP_DIR, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif operating_system == "linux":
            pynode_process = subprocess.Popen([os.path.join(APP_DIR, "cef/linux/pynode")], shell=False, cwd=APP_DIR, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)

        global monitor_thread
        monitor_thread = Thread(target=monitor_data)
        monitor_thread.start()
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
