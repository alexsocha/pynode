import random

class GameData:
    grid = [[0,0,0],[0,0,0],[0,0,0]]
    turn = 1
    turn_node = None

def create_graph():
    nodes = [[], [], []]
    edges = []
    for r in range(0, 3):
        node_row = []
        for c in range(0, 3):
            node = Node((r, c), "").set_size(20).set_value_style(size=20).set_attribute("valid", True).set_attribute("index", (r, c))
            node.set_position(((r-1)*0.25)+0.5, ((c-1)*0.25)+0.5, True)
            nodes[r].append(node)
    for x in range(0, 3):
        edges.append(Edge(nodes[x][0], nodes[x][1])); edges.append(Edge(nodes[x][1], nodes[x][2]))
        edges.append(Edge(nodes[0][x], nodes[1][x])); edges.append(Edge(nodes[1][x], nodes[2][x]))
    edges.append(Edge(nodes[0][0], nodes[1][1])); edges.append(Edge(nodes[1][1], nodes[2][2]))
    edges.append(Edge(nodes[2][0], nodes[1][1])); edges.append(Edge(nodes[1][1], nodes[0][2]))
    GameData.turn_node = Node("").set_color(Color.TRANSPARENT).set_text_color(Color.DARK_GREY).set_text_size(20).set_position(0.5, 0.9, True).set_attribute("valid", False)
    graph.add_all(nodes[0] + nodes[1] + nodes[2] + [GameData.turn_node] + edges)

# Returns a list of the player's three winning positions, or None if the player hasn't won
def win_sequence(grid, player):
    for r in range(0, 3):
        if grid[r][0] == player and grid[r][1] == player and grid[r][2] == player: return [(r,0),(r,1),(r,2)]
    for c in range(0, 3):
        if grid[0][c] == player and grid[1][c] == player and grid[2][c] == player: return [(0,c),(1,c),(2,c)]
    if grid[0][0] == player and grid[1][1] == player and grid[2][2] == player: return [(0,0),(1,1),(2,2)]
    if grid[0][2] == player and grid[1][1] == player and grid[2][0] == player: return [(0,2),(1,1),(2,0)]
    return None

# Finds all positions wich would result in a win
def get_wins(grid, player):
    positions = []
    for r in range(0, 3):
        for c in range(0, 3):
            if grid[r][c] != 0: continue
            new_grid = [x[:] for x in grid]
            new_grid[r][c] = player
            if win_sequence(new_grid, player) is not None:
                positions.append((r, c))
    return positions

# Finds al positions which result in a 'fork' (2 or more potential winning positions)
def get_forks(grid, player):
    positions = []
    for r in range(0, 3):
        for c in range(0, 3):
            if grid[r][c] != 0: continue
            new_grid = [x[:] for x in grid]
            new_grid[r][c] = player
            if len(get_wins(new_grid, player)) >= 2:
                positions.append((r, c))
    return positions

# Calculates the best move
def get_best_move(grid, player):
    opponent = 1 if player == 2 else 2
    corners = [(0, 0), (0, 2), (2, 2), (2, 0)]
    sides = [(0, 1), (1, 0), (2, 1), (1, 2)]
    num_moves = 0
    for r in range(0, 3):
        for c in range(0, 3): num_moves += 1 if grid[r][c] != 0 else 0

    # 1. Win
    wins = get_wins(grid, player)
    if len(wins) > 0: return random.choice(wins)

    # 2. Block
    opponent_wins = get_wins(grid, opponent)
    if len(opponent_wins) > 0: return random.choice(opponent_wins)

    # 3. Fork
    forks = get_forks(grid, player)
    if len(forks) > 0: return random.choice(forks)

    # 4. Block Fork
    opponent_forks = get_forks(grid, opponent)
    if len(opponent_forks) > 0:
        # Option 1
        if random.randint(0, 1) == 0 or True:
            for r in range(0, 3):
                for c in range(0, 3):
                    if grid[r][c] != 0: continue
                    new_grid = [x[:] for x in grid]
                    new_grid[r][c] = player
                    new_wins = get_wins(new_grid, player)
                    if len(new_wins) > 0:
                        new_grid[new_wins[0][0]][new_wins[0][1]] = opponent
                        if len(get_wins(new_grid, opponent)) < 2: return (r, c)
        # Option 2
        print("block fork 2 " + str(opponent_forks[0]))
        return random.choice(opponent_forks)

    # 5. Center (Or corner if first move)
    if num_moves == 0: return (1, 1) if random.randint(0, 1) == 0 else random.choice(corners)
    elif grid[1][1] == 0: return (1, 1)

    # 6. Opposite Corner
    for c in range(0, 4):
        if grid[corners[c][0]][corners[c][1]] == opponent and grid[corners[(c+2)%4][0]][corners[(c+2)%4][1]] == 0:
            return corners[(c+2)%4]

    # 6. Empty Corner
    empty_corners = [c for c in corners if grid[c[0]][c[1]] == 0]
    if len(empty_corners) > 0: return random.choice(empty_corners)

    # 6. Empty Side
    empty_sides = [s for s in sides if grid[s[0]][s[1]] == 0]
    if len(empty_sides) > 0: return random.choice(empty_sides)

# Checks for a win or tie, and performs an animation
def check_end_game(grid):
    winner = 1
    sequence = win_sequence(grid, 1)
    if sequence is None:
        sequence = win_sequence(grid, 2)
        winner = 2
    if sequence is not None:
        GameData.turn = 3
        if winner == 1: GameData.turn_node.set_value("Player Wins! (This shouldn't be possible...)")
        else: GameData.turn_node.set_value("Computer Wins!")
        edge1 = graph.edges_between(graph.node(sequence[0]), graph.node(sequence[1]))[0]
        edge2 = graph.edges_between(graph.node(sequence[1]), graph.node(sequence[2]))[0]
        color = Color.RED if winner == 2 else Color.GREEN
        edge1.traverse(graph.node(sequence[0]), color)
        pause(500)
        edge2.traverse(graph.node(sequence[1]), color)
        return True
    num_moves = 0
    for r in range(0, 3):
        for c in range(0, 3): num_moves += 1 if grid[r][c] != 0 else 0
    if num_moves >= 9:
        GameData.turn = 3
        GameData.turn_node.set_value("Draw!")
        return True
    return False

def player_turn():
    if not check_end_game(GameData.grid):
        GameData.turn = 1
        GameData.turn_node.set_value("Turn: Player")

def on_click(node):
    if GameData.turn == 1 and node.attribute("valid"):
        index = node.attribute("index")
        if GameData.grid[index[0]][index[1]] == 0:
            node.highlight()
            node.set_value("O")
            node.set_color(Color.GREEN)
            GameData.grid[index[0]][index[1]] = 1
            GameData.turn = 2
            delay(computer_turn, 1000)

def computer_turn():
    if not check_end_game(GameData.grid):
        GameData.turn = 2
        GameData.turn_node.set_value("Turn: Computer")
        move = get_best_move(GameData.grid, 2)
        GameData.grid[move[0]][move[1]] = 2
        node = graph.node(move)
        node.highlight()
        node.set_value("X")
        node.set_color(Color.RED)
        delay(player_turn, 1000)

def start_game():
    if random.randint(0, 1) == 0: player_turn()
    else:
        GameData.turn = 2
        GameData.turn_node.set_value("Turn: Computer")
        delay(computer_turn, 500)

register_click_listener(on_click)
create_graph()
start_game()
