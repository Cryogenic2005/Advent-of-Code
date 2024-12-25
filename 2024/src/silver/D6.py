from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def outside(map: list[list[str]], x: int, y: int) -> bool:
    return x < 0 or x >= len(map) or y < 0 or y >= len(map[0])

def step(map: list[list[str]], x: int, y: int, dir: tuple[int,int]) -> tuple[int,int]:
    nextX = x + dir[0]
    nextY = y + dir[1]
    
    if outside(map, nextX, nextY):
        return (nextX, nextY, dir)
    
    if map[nextY][nextX] == '#':
        rot270 = (-dir[1], dir[0])
        return step(map, x, y, rot270)
    
    return (nextX, nextY, dir)

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    visited = [[False for _ in range(len(lines[0]))] for _ in range(len(lines))]
    
    x=0
    y=0
    
    # find start
    for i, line in enumerate(lines):
        if '^' in line:
            x = line.index('^')
            y = i
            break
        
    dir = (0, -1) # Up
    while not outside(lines, x, y):
        visited[y][x] = True
        x, y, dir = step(lines, x, y, dir)        
        
    total = sum([row.count(True) for row in visited])
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
        
        if REOUTPUT_INPUT:
            for i, value in enumerate(values):
                f.write(f'{lines[i].strip()} -> {value}\n')
        
if __name__ == '__main__':
    main()