from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

ORTHOGONAL = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def isValid(grid: list[list[int]], y: int, x: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def dfs_trailheads(grid: list[list[int]], y: int, x: int, curr_height: int = 0) -> int|list[tuple[int,int]]:
    if curr_height == 9:
        return 1

    sum = 0    
    for dx, dy in ORTHOGONAL:
        new_y, new_x = y + dy, x + dx
        if isValid(grid, new_y, new_x) and (grid[new_y][new_x] == (curr_height + 1)):
            sum += dfs_trailheads(grid, new_y, new_x, curr_height + 1)
    
    return sum

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    topoMap = [[int(x) for x in line] for line in lines]
    
    for row_idx, row in enumerate(topoMap):
        for col_idx, col in enumerate(row):
            if col == 0:
                values.append(dfs_trailheads(topoMap, row_idx, col_idx))
    
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