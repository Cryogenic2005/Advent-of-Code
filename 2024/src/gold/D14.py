from pathlib import Path
import re

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    velocity = []
    
    HEIGHT = 103
    WIDTH = 101
    
    for line in lines:
        if not line: continue
        
        res = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
        px, py, vx, vy = map(int, res.groups())
        values.append((px, py))
        velocity.append((vx, vy))
    
    time = 0
    flag = True
    point_map = {}
    
    while flag:
        flag = False
        point_map = {}
        time += 1
        for i in range(len(values)):
            px, py = values[i]
        
            px += velocity[i][0]
            py += velocity[i][1]
            
            while px < 0: px += WIDTH
            while py < 0: py += HEIGHT
            
            px %= WIDTH
            py %= HEIGHT
            
            values[i] = (px, py)
            point_map[(px, py)] = point_map.get((px, py), 0) + 1
            
            # Check if the point is in the same place as another point
            if point_map[(px, py)] > 1:
                flag = True            
        
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if (j, i) in values:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()
        
        
    print(f"Time: {time}")
    
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