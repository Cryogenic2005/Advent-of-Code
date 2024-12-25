from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

DIRS = [(0,1), (1,0), (0,-1), (-1,0)]

def is_valid(grid, x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def bfs(grid, x, y):
    visited = set()
    dist = [[float('inf') for _ in range(len(grid[0]))] for _ in range(len(grid))]
    
    queue = [(x,y)]
    dist[y][x] = 0
    
    while queue:
        x, y = queue.pop(0)
        
        if (x,y) in visited:
            continue
        
        visited.add((x,y))
        
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            
            if not is_valid(grid, nx, ny):
                continue
            
            if grid[ny][nx] == '#':
                continue
            
            if (nx,ny) in visited:
                continue
            
            dist[ny][nx] = min(dist[ny][nx], dist[y][x] + 1)
            queue.append((nx,ny))
            
    return visited, dist
                
def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    WIDTH = 70 + 1
    grid = [['.' for _ in range(WIDTH)] for _ in range(WIDTH)]
    
    for line in lines[:min(1024, len(lines))]:
        x,y = line.split(',')
        grid[int(y)][int(x)] = '#'
       
    # for row in grid:
    #     print(''.join(row))
       
    visited, dist = bfs(grid, 0, 0) 
    total = dist[WIDTH-1][WIDTH-1]
    
    # for row in dist:
    #     print(row)
        
    # total = sum(values)
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