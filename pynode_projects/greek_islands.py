# Custom 'Activity' ADT used in the model
class Activity:
    name = ""
    cost = 0
    time = 0
    def create(): return Activity()
    def setType(self, n): self.name = n; return self
    def setCost(self, c): self.cost = c; return self
    def setTime(self, t): self.time = t; return self
    def getType(self): return self.name
    def getCost(self): return self.cost
    def getTime(self): return self.time
    
island_nodes = []
island_edges = []
island_coordinates = {}

BOAT_EMOJI = "\u26F5"
SPEEDBOAT_EMOJI = "\uD83D\uDEE5\uFE0F"
PLANE_EMOJI = "\u2708\uFE0F\uFE0F"

# Pre-defined activity names/emojis/estimated times and costs
# NOTE: This version of the model uses emojis to visually represent activities
# However, activity types are still stored as integers
ACTIVITY_NAMES = [("Racing", "\uD83C\uDFCE\uFE0F"), ("Mountain Climbing", "\u26F0\uFE0F"), ("Camping", "\uD83C\uDFD5\uFE0F"), ("Beach", "\uD83C\uDFD6\uFE0F"), ("Park", "\uD83C\uDFDE\uFE0F"), ("Stadium", "\uD83C\uDFDF\uFE0F"), ("Architechture", "\uD83C\uDFDB\uFE0F"), ("Hotel", "\uD83C\uDFE8"), ("Shopping", "\uD83D\uDED2"), ("Theme Park", "\uD83C\uDFA1")]
ACTIVITIES = [(ACTIVITY_NAMES[0], 54, 17), (ACTIVITY_NAMES[1], 32, 43), (ACTIVITY_NAMES[2], 12, 98), (ACTIVITY_NAMES[3], 5, 12), (ACTIVITY_NAMES[4], 7, 15), (ACTIVITY_NAMES[5], 25, 60), (ACTIVITY_NAMES[6], 42, 24), (ACTIVITY_NAMES[7], 84, 120), (ACTIVITY_NAMES[8], 33, 14), (ACTIVITY_NAMES[9], 46, 55)]

def create_node(name, activities, position, size):
    # Create a node
    position = ((position[0] * 3.0) - 1500, (position[1] * 3.0) - 1500)
    n = Node(name).set_position(position[0], position[1]).set_size(size)
    island_coordinates[name] = position
    
    # This is the array which contains all of the activities on an island
    activity_array = []
    
    text = name
    for a in activities:
        activity = Activity.create()
        activity.setType(a)
        
        # Automatically adjust the time and cost of an activity based on the amount of activities on the island
        # In theory, more activities -> island is larger and more popular -> activities take more time and are more expensive
        # Ideally, this would be specified manually, but due to time constraints a reasonable automatic process is used
        activity.setTime(int(ACTIVITIES[a][2] * (len(activities)**0.5)))
        activity.setCost(int(ACTIVITIES[a][1] * (len(activities)**0.5)))
        activity_array.append(activity)
        
        # Visually show the activities as text on each node
        text += "\n" + str(ACTIVITY_NAMES[a][1]) + str(activity.getTime()) + "m $" + str(activity.getCost())
    n.set_value(text)
    
    # Add the array of activities to the node, using PyNode's attribute system
    n.set_attribute("activities", activity_array)
    return n

def create_edges(node1, node2):
    # Calculate the distande between two islands, in kilometers
    d = (((island_coordinates[node1][0] - island_coordinates[node2][0]) ** 2 + (island_coordinates[node1][1] - island_coordinates[node2][1]) ** 2) ** 0.5) * 0.13
    
    edges = []
    transport = [1.0, 0.5, 1.5]
    for i in range(len(transport)):
        e = Edge(node2, node1)
        
        # Equations for calculating time and cost, detailed in the report
        x = transport[i]
        time = int(0.6 * (d / x))
        cost = int(1.005**d * 0.4 * x * d)
        
        # Add the time and cost data to the edge, using PyNode's attribute system
        e.set_attribute("time", time)
        e.set_attribute("cost", cost)
        
        # Set the visual appearance of the edge
        # Colors and emojis are used to better display the data visually
        e.set_weight((SPEEDBOAT_EMOJI if i == 0 else BOAT_EMOJI if i == 1 else PLANE_EMOJI) + str(time) + "m $" + str(cost))
        e.set_color(Color.BLUE if i == 0 else Color.YELLOW if i == 1 else Color.RED)
        edges.append(e)
    return edges

# Create islands
island_nodes.append(create_node("Paros", [0, 1, 5], (560, 596), 50))
island_nodes.append(create_node("Antiparos", [2], (519, 635), 35))
island_nodes.append(create_node("Naxos", [2, 4, 5, 9], (628, 591), 60))
island_nodes.append(create_node("Donousa", [3], (705, 568), 30))
island_nodes.append(create_node("Amorgos", [1, 7, 8], (730, 684), 45))
island_nodes.append(create_node("Sikinos", [6], (546, 763), 35))
island_nodes.append(create_node("Ios", [0, 9], (595, 743), 40))
island_nodes.append(create_node("Folegandros", [3], (494, 785), 35))
island_nodes.append(create_node("Sifnos", [2, 6], (448, 635), 40))
island_nodes.append(create_node("Milos", [4, 7, 9], (389, 749), 50))
island_nodes.append(create_node("Santorini", [1, 2], (623, 890), 40))
island_nodes.append(create_node("Anafi", [4, 8], (701, 894), 35))

# Create travel routes
island_edges += create_edges("Paros", "Antiparos")
island_edges += create_edges("Paros", "Sikinos")
island_edges += create_edges("Paros", "Naxos")
island_edges += create_edges("Antiparos", "Sikinos")
island_edges += create_edges("Antiparos", "Sifnos")
island_edges += create_edges("Naxos", "Anafi")
island_edges += create_edges("Naxos", "Donousa")
island_edges += create_edges("Naxos", "Amorgos")
island_edges += create_edges("Naxos", "Ios")
island_edges += create_edges("Naxos", "Sikinos")
island_edges += create_edges("Amorgos", "Donousa")
island_edges += create_edges("Ios", "Amorgos")
island_edges += create_edges("Ios", "Sikinos")
island_edges += create_edges("Ios", "Donousa")
island_edges += create_edges("Sifnos", "Folegandros")
island_edges += create_edges("Sifnos", "Sikinos")
island_edges += create_edges("Sikinos", "Milos")
island_edges += create_edges("Sikinos", "Folegandros")
island_edges += create_edges("Milos", "Sifnos")
island_edges += create_edges("Milos", "Antiparos")
island_edges += create_edges("Milos", "Folegandros")
island_edges += create_edges("Milos", "Naxos")
island_edges += create_edges("Milos", "Amorgos")
island_edges += create_edges("Santorini", "Amorgos")
island_edges += create_edges("Santorini", "Ios")
island_edges += create_edges("Santorini", "Sikinos")
island_edges += create_edges("Santorini", "Folegandros")
island_edges += create_edges("Santorini", "Naxos")
island_edges += create_edges("Santorini", "Milos")
island_edges += create_edges("Anafi", "Santorini")
island_edges += create_edges("Anafi", "Ios")
island_edges += create_edges("Anafi", "Amorgos")

# Add all data to the graph
graph.add_all(island_nodes + island_edges)
