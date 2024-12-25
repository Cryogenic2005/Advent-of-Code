from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

LEFT = '<'
RIGHT = '>'
UP = '^'
DOWN = 'v'

WALL = '#'
EMPTY = '.'
ROBOT = '@'
BOX = 'O'

def inBounds(grid: list[list[str]], x: int, y: int) -> bool:
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def tryPushBox(grid: list[list[str]], x: int, y: int, dx: int, dy: int) -> bool:
    assert grid[y][x] == BOX
    
    new_x = x + dx
    new_y = y + dy
    
    if not inBounds(grid, new_x, new_y):
        return False
    
    if grid[new_y][new_x] == WALL:
        return False
    
    if grid[new_y][new_x] == EMPTY:
        grid[new_y][new_x] = BOX
        return True
    
    if grid[new_y][new_x] == BOX:
        if tryPushBox(grid, new_x, new_y, dx, dy):
            grid[new_y][new_x] = BOX
            return True
        else:
            return False

    raise Exception("Invalid state")
        
def tryMove(grid: list[list[str]], x: int, y: int, dx: int, dy: int) -> tuple[int, int]:
    new_x = x + dx
    new_y = y + dy
    
    if not inBounds(grid, new_x, new_y):
        return x, y
    
    if grid[new_y][new_x] == WALL:
        return x, y
    
    if grid[new_y][new_x] == EMPTY:
        return new_x, new_y
        
    # If there is a box
    if tryPushBox(grid, new_x, new_y, dx, dy):
        return new_x, new_y
    
    return x, y

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    grid = []
    
    i = 0
    while lines[i] != '':
        grid.append(list(lines[i]))
        i += 1
    
    robot_x, robot_y = -1, -1
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == ROBOT:
                robot_x, robot_y = x, y
                break
    
    for line in lines[i+1:]:
        for dir in line:
            grid[robot_y][robot_x] = EMPTY
            
            if dir == LEFT:
                robot_x, robot_y = tryMove(grid, robot_x, robot_y, -1, 0)
            elif dir == RIGHT:
                robot_x, robot_y = tryMove(grid, robot_x, robot_y, 1, 0)
            elif dir == UP:
                robot_x, robot_y = tryMove(grid, robot_x, robot_y, 0, -1)
            elif dir == DOWN:
                robot_x, robot_y = tryMove(grid, robot_x, robot_y, 0, 1)
                
            grid[robot_y][robot_x] = ROBOT
            
            # print(dir)
            # for y in range(len(grid)):
            #     print(''.join(grid[y]))
                
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == BOX:
                values.append(100 * y + x)
    
        
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