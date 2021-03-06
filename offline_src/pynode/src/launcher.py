# Copyright (c) 2017 Alex Socha
# https://alexsocha.github.io/pynode

from pynode.src import communicate

def set_run_function(func):
    communicate.set_run_function(func)

def begin_pynode(run_func=None):
    set_run_function(run_func)
    communicate.open_connection()
