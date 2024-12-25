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
    # dist = [[float('inf') for _ in range(len(grid[0]))] for _ in range(len(grid))]
    
    queue = [(x,y)]
    # dist[y][x] = 0
    
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
            
            # dist[ny][nx] = min(dist[ny][nx], dist[y][x] + 1)
            queue.append((nx,ny))
            
    return visited # , dist

def isEscapePossible(lines, sim_byte, width = 70) -> bool:
    WIDTH = width + 1
    grid = [['.' for _ in range(WIDTH)] for _ in range(WIDTH)]
    
    for line in lines[:min(sim_byte, len(lines))]:
        x,y = line.split(',')
        grid[int(y)][int(x)] = '#'
       
    # for row in grid:
    #     print(''.join(row))
       
    visited = bfs(grid, 0, 0)     
    return (WIDTH-1, WIDTH-1) in visited
                
def solve(lines: list[str]) -> int:
    lo = 0
    hi = len(lines)
    res = -1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        
        if isEscapePossible(lines, mid):
            lo = mid + 1
        else:
            hi = mid - 1
            res = mid
            
    byte = lines[res-1].split(',')
    byte = (int(byte[0]), int(byte[1]))
    return byte, [res]

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