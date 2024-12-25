from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def inBounds(grid, x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def neighbors(grid, x, y):
    neighbors = []
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        
        if not inBounds(grid, nx, ny):
            continue
        
        if grid[ny][nx] == '#':
            continue
        
        neighbors.append((nx, ny))
        
    return neighbors

def cheat_neighbors(grid, x, y, max_steps=2):
    queue = [(x, y)]
    visited = set()
    distance = {(x, y): 0}
    
    while queue:
        node = queue.pop(0)
                
        if node in visited:
            continue
            
        visited.add(node)
        
        if distance[node] >= max_steps:
            continue
        
        for dx, dy in DIRS:
            nx, ny = node[0] + dx, node[1] + dy
            
            if not inBounds(grid, nx, ny):
                continue
            
            if (nx, ny) in visited:
                continue
            
            distance[(nx, ny)] = distance[node] + 1
            queue.append((nx, ny))
            
    valid_stops = []
    for node in visited:
        if node == (x, y):
            continue
        
        if grid[node[1]][node[0]] == '#':
            continue
        
        valid_stops.append(((x, y), (node[0], node[1])))
            
    return valid_stops, distance

def bfs(grid, start):
    queue = [start]
    distance = {start: 0}
    visited = set()
    
    while queue:
        node = queue.pop(0)
        
        if node in visited:
            continue
        
        visited.add(node)
        
        for neighbor in neighbors(grid, node[0], node[1]):
            if neighbor not in visited:
                queue.append(neighbor)
                distance[neighbor] = distance[node] + 1
                
    return distance
    

def bfs_cheat(grid, start, end):
    MIN_SAVE = 100 # Save MIN_SAVE steps
    
    cheats = {} # (start, end) -> distance
    
    dist_from_start = bfs(grid, start)
    dist_to_end = bfs(grid, end)
    
    for node in dist_from_start.keys():
        if dist_to_end.get(node) is None:
            continue
        
        if dist_to_end[node] < MIN_SAVE:
            continue
        
        cheat_nodes, distance = cheat_neighbors(grid, node[0], node[1], 20)
        
        for c_start, c_end in cheat_nodes:
            # Can't get to the end with the cheated path
            if dist_to_end.get(c_end) is None:
                continue
            
            # Calculate the distance from the start to the end
            # using the cheated path
            cheated_dist = dist_from_start[node] + dist_to_end[c_end] + distance[c_end]
            
            # If the cheated path saves at least MIN_SAVE steps
            if dist_from_start[end] - cheated_dist >= MIN_SAVE:
                # print(c_start, c_end, cheated_dist)
                cheats[(node, c_end)] = cheated_dist
                
    return cheats

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    grid = [list(line) for line in lines]
    
    start, end = None, None
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'S':
                start = (x, y)
            elif grid[y][x] == 'E':
                end = (x, y)
                
    values = bfs_cheat(grid, start, end).items()
    
    total = len(values)
    return total, values

def main():
    lines = []
    
    # Read the input file
    with open(INPUT, 'r') as f:
        lines = f.readlines()
    
    lines = [line.strip() for line in lines] # Remove leading/trailing whitespace
    
    sum, values = solve(lines)
    print(f"Sum: {sum}\n")
            
    # Write the output
    with open(OUTPUT, 'w') as f:
        f.write(str(sum) + '\n\n')
        f.write(str(values) + '\n\n')
        
if __name__ == '__main__':
    main()