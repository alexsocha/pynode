# Prim's Algorithm
import random
import queue

# Generate a random graph
NUM_NODES = 10
NUM_EDGES = 12
random_graph = graph.random(NUM_NODES, NUM_EDGES)
start = None
for element in random_graph:
    if isinstance(element, Node):
        element.set_value("")
    if isinstance(element, Edge):
        # Assign a random weight to each edge
        element.set_weight(random.randint(1, 32))
        element.set_priority(element.weight())
        element.set_attribute("selected", False)
    element.set_attribute("seen", False)
graph.add_all(random_graph)

# Use a priority queue finding the shortest edge
pq = queue.PriorityQueue()
pause(1000)

# Visit a node and add all unseen incident edges to the priority queue
def visit_node(n):
    if n.attribute("seen"): return
    n.set_color(Color(219, 112, 147))
    n.highlight()
    n.set_attribute("seen", True)
    pause(500)
    for e in n.incident_edges():
        if not e.attribute("seen"):
            e.set_color(Color.GREY)
            e.set_attribute("seen", True)
            pq.put(e)
    pause(500)
 
# Choose a random start node
start = graph.nodes()[random.randint(0, len(graph.nodes()) - 1)]
visit_node(start)

while not pq.empty():
    # Get the next shortest edge
    e = pq.get()
    # Avoid cycles
    if e.source().attribute("seen") and e.target().attribute("seen"):
        e.traverse(color=Color.RED, keep_path=False)
        pause(500)
        e.set_color(Color.LIGHT_GREY)
        pause(500)
        continue
    # Visit adjacent node
    visited_node = e.source() if e.source().attribute("seen") else e.target()
    e.traverse(visited_node, Color(219, 112, 147))
    pause(1000)
    visit_node(e.target(visited_node))

# Now all the edges are connected together :)
for n in graph.nodes():
    heart = "❤"
    n.set_value(heart)
    n.highlight()
 