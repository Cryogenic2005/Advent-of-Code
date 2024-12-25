from pathlib import Path
from queue import PriorityQueue


ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def isValid(grid, x, y):
    if grid[y][x] == '#':
        return False
    
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def bfs(grid, start, end):
    queue = PriorityQueue()
    queue.put((0, start, DIRS[2]))
    while not queue.empty():
        score, (x, y), direction = queue.get()
        
        for dx, dy in DIRS:
            if direction == (-dx, -dy):
                continue # Avoid reversing direction
            
            nx, ny = x + dx, y + dy
            
            if not isValid(grid, nx, ny):
                continue
            
            new_score = score + 1 # Moving 1 step costs 1
            if direction != (dx, dy): new_score += 1000 # Turning 90 degrees costs 1000
                
            if new_score > bfs.score[ny][nx][dx, dy]:
                continue
                
            bfs.score[ny][nx][dx, dy] = new_score
            queue.put((new_score, (nx, ny), (dx, dy)))
            
    minScore = min(bfs.score[end[1]][end[0]].values())
    tmp = []
    for (dx, dy), score in bfs.score[end[1]][end[0]].items():
        if score == minScore:
            tmp.append((minScore, end[0], end[1], dx, dy))

    trails = {end}
    while tmp:
        currScore, x, y, dx, dy = tmp.pop(0)
        
        px, py = x - dx, y - dy
        
        for dir, score in bfs.score[py][px].items():
            moveCost = 1 if (dx, dy) == dir else 1001
            newScore = currScore - moveCost
            
            if newScore != score: # Not the minimum score
                continue

            trails.add((px, py))
            tmp.append((newScore, px, py, dir[0], dir[1]))

    return minScore, len(trails)

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    grid = lines
    start = (0, 0)
    end = (0, 0)
    
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == 'S':
                start = (j, i)
            elif char == 'E':
                end = (j, i)
                
    bfs.score = [[{dir: float('inf') for dir in DIRS} for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for dir in DIRS:
        bfs.score[start[1]][start[0]][dir] = 0
    
    minScore, tiles = bfs(grid, start, end)
    total = tiles
        
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