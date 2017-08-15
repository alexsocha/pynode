from pynode.main import *

def run():
    graph.add_node('A')
    graph.add_node('B')
    graph.add_edge('A', 'B')

begin_pynode(run)
