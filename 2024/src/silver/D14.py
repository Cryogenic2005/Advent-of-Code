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
    
    points = []    
    velocity = []
    
    HEIGHT = 103
    WIDTH = 101
    
    for line in lines:
        if not line: continue
        
        res = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
        px, py, vx, vy = map(int, res.groups())
        points.append((px, py))
        velocity.append((vx, vy))
    
    TIME = 100

    for i in range(len(points)):
        px, py = points[i]
    
        px += velocity[i][0] * TIME
        py += velocity[i][1] * TIME
        
        px %= WIDTH
        py %= HEIGHT
        
        points[i] = (px, py)
            
    quad1 = []
    quad2 = []
    quad3 = []
    quad4 = []
    
    # Since dimensions are odd, center is at (WIDTH//2, HEIGHT//2)
    # Points at center are not considered in any quadrant
    half_width = WIDTH//2
    half_height = HEIGHT//2
    
    for p in points:
        x, y = p
        if x < half_width and y < half_height:
            quad1.append(p)
        elif x > half_width and y < half_height:
            quad2.append(p)
        elif x < half_width and y > half_height:
            quad3.append(p)
        elif x > half_width and y > half_height:
            quad4.append(p)
            
    values = [len(quad1), len(quad2), len(quad3), len(quad4)]
    total = values[0] * values[1] * values[2] * values[3]    
    
    print(f"Values: {values}")
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