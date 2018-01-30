# DFS Algorithm
import random

# Generate a random graph
NUM_NODES = 10
NUM_EDGES = 12
random_graph = graph.random(NUM_NODES, NUM_EDGES)
start = None
for element in random_graph:
    if isinstance(element, Node):
        element.set_value("")
        element.set_attribute("seen", False)
graph.add_all(random_graph)
pause(1000)

# Recursive DFS function
def dfs(node):
    if node.attribute("seen"): return
    node.set_attribute("seen", True)
    node.highlight()
    if node is not start: node.set_color(Color.BLUE)
    pause(500)
    for e in node.outgoing_edges():
        n = e.other_node(node)
        if n.attribute("seen"): continue
        e.traverse(node)
        pause(500)
        dfs(n)
        node.highlight()
        pause(500)

# Choose a random start node
start = graph.nodes()[random.randint(0, len(graph.nodes()) - 1)]
start.set_color(Color.GREEN)
pause(500)
dfs(start)
