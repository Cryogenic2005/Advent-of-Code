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

WALL2 = ['#', '#']
EMPTY2 = ['.', '.']
ROBOT2 = ['@', '.']
BOXLEFT = '['
BOXRIGHT = ']'
BOX2 = ['[', ']']

def inBounds(grid: list[list[str]], x: int, y: int) -> bool:
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def tryPushBox(grid: list[list[str]], x: int, y: int, dx: int, dy: int, push = True) -> bool:
    if grid[y][x] == EMPTY:
        return True
    
    box_y = y
    box_y_new = box_y + dy
    box_left_x = x if grid[y][x] == BOXLEFT else x - 1
    box_right_x = box_left_x + 1
    
    if not inBounds(grid, box_left_x + dx, box_y_new) or not inBounds(grid, box_right_x + dx, box_y_new):
        return False
    
    if grid[box_y_new][box_left_x + dx] == WALL or grid[box_y_new][box_right_x + dx] == WALL:
        return False
        
    if dy == 0: # Pushing horizontally
        if dx == -1: # Pushing left
            if tryPushBox(grid, box_left_x + dx, box_y, dx, dy, False):
                if push:
                    tryPushBox(grid, box_left_x + dx, box_y, dx, dy)
                    grid[box_y][box_left_x + dx] = BOXLEFT
                    grid[box_y][box_left_x] = BOXRIGHT
                    grid[box_y][box_right_x] = EMPTY
                return True
            
            return False
        
        # Pushing right
        if tryPushBox(grid, box_right_x + dx, box_y, dx, dy, False):
            if push:
                tryPushBox(grid, box_right_x + dx, box_y, dx, dy)
                grid[box_y][box_right_x + dx] = BOXRIGHT
                grid[box_y][box_right_x] = BOXLEFT
                grid[box_y][box_left_x] = EMPTY
            return True
        
        return False
    
    # Pushing vertically
    if grid[box_y_new][box_left_x] == BOXLEFT and grid[box_y_new][box_right_x] == BOXRIGHT:
        if tryPushBox(grid, box_left_x, box_y_new, dx, dy, False):
            if push:
                tryPushBox(grid, box_left_x, box_y_new, dx, dy)
                grid[box_y_new][box_left_x] = BOXLEFT
                grid[box_y_new][box_right_x] = BOXRIGHT
                grid[box_y][box_left_x] = EMPTY
                grid[box_y][box_right_x] = EMPTY
            return True

        return False
        
    if tryPushBox(grid, box_left_x, box_y_new, dx, dy, False) and tryPushBox(grid, box_right_x, box_y_new, dx, dy, False):
        if push:
            tryPushBox(grid, box_left_x, box_y_new, dx, dy)
            tryPushBox(grid, box_right_x, box_y_new, dx, dy)
            grid[box_y_new][box_left_x] = BOXLEFT
            grid[box_y_new][box_right_x] = BOXRIGHT
            grid[box_y][box_left_x] = EMPTY
            grid[box_y][box_right_x] = EMPTY
        return True

    return False        
        
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

def transformGrid(grid: list[str]) -> list[list[str]]:
    new_grid = []
    for y in range(len(grid)):
        new_grid.append([])
        for x in range(len(grid[0])):
            if grid[y][x] == WALL:
                new_grid[y].extend(WALL2)
            elif grid[y][x] == EMPTY:
                new_grid[y].extend(EMPTY2)
            elif grid[y][x] == ROBOT:
                new_grid[y].extend(ROBOT2)
            elif grid[y][x] == BOX:
                new_grid[y].extend(BOX2)
    return new_grid

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    grid = []
    
    i = 0
    while lines[i] != '':
        grid.append(list(lines[i]))
        i += 1
        
    grid = transformGrid(grid)
    
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
            if grid[y][x] == BOXLEFT:
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