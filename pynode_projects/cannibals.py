# Cannibals and Missionaries
import queue
import random

seen = [False] * 32
bfs_queue = queue.Queue()

# Create the next situation by adding a new node and/or edge
def next_situation(node, data):
    # Convert the data array to a single binary number (for the fun of it)
    binary_id = 0
    new_node = None
    for i in range(5): binary_id += (data[i] << (4 - i))
    
    # Add a new node, or connect to an existing one
    if seen[binary_id]:
        if not graph.adjacent(node, binary_id):
            graph.add_edge(node, binary_id, directed=True)
    else:
        new_node = graph.add_node(binary_id, "".join(map(str, data))).set_attribute("data", data)
        graph.add_edge(node, new_node, directed=True)
    seen[binary_id] = True
    return new_node

start = graph.add_node(0, "00000").set_attribute("data", [0, 0, 0, 0, 0])
end = None
seen[0] = True
bfs_queue.put(start)

while not bfs_queue.empty():
    # Use the next node on the queue
    node = bfs_queue.get()
    pause(500)
    node.set_color(Color.RED)
    node.highlight()
    pause(500)
    data = node.attribute("data")
    if data == [1, 1, 1, 1, 1]: end = node
    
    # Try adding all possible new nodes
    boat_side = data[4]
    new_boat_side = (data[4] + 1) % 2
    for p1 in range(4):
        for p2 in range(4):
            # Move 2 people
            if data[p1] != boat_side or data[p2] != boat_side: continue
            new_data = list(data)
            new_data[4] = new_boat_side
            new_data[p1] = new_boat_side
            new_data[p2] = new_boat_side
            
            # Number of missionaries and cannibals on the current side
            num_m = (1 if new_data[0] == new_data[4] else 0) + (1 if new_data[1] == new_data[4] else 0)
            num_c = (1 if new_data[2] == new_data[4] else 0) + (1 if new_data[3] == new_data[4] else 0)
            
            # Ignore invalid situations
            if num_m < num_c and num_m > 0: continue
            if (2 - num_m) < (2 - num_c) and (2 - num_m) > 0: continue
            
            # Add a new node to the queue
            new_node = next_situation(node, new_data)
            if new_node != None: bfs_queue.put(new_node)

# Reset node color
pause(1000)  
for node in graph.nodes():
    node.set_color(Color.DARK_GREY)
pause(500)

# Color start and end
start.set_color(Color.GREEN)
end.set_color(Color.GREEN)
pause(500)

# Randomly choose path
path = []
node = end
while node is not start:
    edge = node.incoming_edges()[random.randint(0, len(node.incoming_edges()) - 1)]
    path.append(edge)
    node = edge.source()

# Traverse the path
for edge in reversed(path):
    edge.traverse(color=Color.GREEN)
    pause(500)
