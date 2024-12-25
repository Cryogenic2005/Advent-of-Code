from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

DIR = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def isValid(grid: list[str], x: int, y: int) -> bool:
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def bfs(grid: list[str], x: int, y: int) -> int:
    area = 0
    perimeter = 0
    
    if grid[y][x] == '0':
        return 0
    
    queue = [(x, y)]
    category = grid[y][x]
    
    while queue:
        x, y = queue.pop(0)
        if bfs.visited[y][x]:
            continue
        
        area += 1
        bfs.visited[y][x] = True
        
        for dir in DIR:
            new_x, new_y = x + dir[0], y + dir[1]
            if isValid(grid, new_x, new_y) and grid[new_y][new_x] == category:
                queue.append((new_x, new_y))
            else:
                perimeter += 1
    
    return area * perimeter

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    bfs.visited = [[False for _ in range(len(lines[y]))] for y in range(len(lines))]
    
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            values.append(bfs(lines, x, y))
        
    total = sum(values)
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