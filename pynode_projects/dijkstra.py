# Dijkstra's Algorithm
import queue
import random

# Create a random graph
NUM_NODES = 12
NUM_EDGES = 15
data = graph.random(NUM_NODES, NUM_EDGES)
for element in data:
    if isinstance(element, Node):
        element.set_value("∞")
        element.set_priority(1000000)
        element.set_attribute("dist", 1000000)
    if isinstance(element, Edge): element.set_weight(random.randint(1, 20))
graph.add_all(data)
pause(1000)

# Select random start node
start = graph.nodes()[random.randint(0, len(graph.nodes()) - 1)]
start.set_value(0); start.set_priority(0); start.set_attribute("dist", 0)

# Create priority queue
pq = queue.PriorityQueue()
pq.put(start)
seen = {}
for n in graph.nodes(): seen[n] = False
while not pq.empty():
    # Get the node closest to the start node
    node = pq.get()
    if seen[node]: continue
    seen[node] = True
    node.set_size(node.size()*1.5)
    node.set_color(Color.RED)
    pause(400)
    # Update adjacent nodes
    for edge in node.outgoing_edges():
        edge.traverse(node, keep_path=True)
    pause(750)
    node.set_size(node.size()/1.5)
    for edge in node.outgoing_edges():
        target = edge.other_node(node)
        if not seen[target]:
            new_dist = node.attribute("dist") + edge.weight()
            # Only update if new distance is better than the previous one
            if new_dist < target.attribute("dist"):
                target.set_attribute("dist", new_dist)
                target.set_value(new_dist)
                target.set_priority(new_dist)
                # Store the edge used to reach this node
                target.set_attribute("path", edge)
                pq.put(target)
    pause(400)

# Reset node and edge color
pause(500)
for node in graph.nodes(): node.set_color(Color.DARK_GREY)
for edge in graph.edges(): edge.set_color(Color.LIGHT_GREY)
pause(1000)

# Select a random end node
end = None
for i in range(0, 100):
    end = graph.nodes()[random.randint(0, len(graph.nodes()) - 1)]
    if start is end or graph.adjacent(start, end): continue
    else: break
start.set_color(Color.GREEN)
end.set_color(Color.GREEN)
pause(1000)

# Get the shortest path
path = []
node = end
while node is not start:
    edge = node.attribute("path")
    node = edge.other_node(node)
    path.append((node, edge))
   
 # Animate the path
for n, e in reversed(path):
    e.traverse(n, Color.GREEN)
    pause(500)
