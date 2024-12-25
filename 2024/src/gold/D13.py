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
    
    it = 0
    while it < len(lines):
        if lines[it] == '':
            it += 1
            continue
        
        res1 = re.match(r'Button A: X\+(\d+), Y\+(\d+)', lines[it])
        res2 = re.match(r'Button B: X\+(\d+), Y\+(\d+)', lines[it+1])
        res3 = re.match(r'Prize: X=(\d+), Y=(\d+)', lines[it+2])
        it += 3
        
        ax, ay = int(res1.group(1)), int(res1.group(2))
        bx, by = int(res2.group(1)), int(res2.group(2))
        cx, cy = int(res3.group(1)), int(res3.group(2))
        
        cx += 10000000000000
        cy += 10000000000000
    
        # Solve m1 * ax + n1 * bx = cx
        #       m1 * ay + n1 * by = cy
        det = ax * by - ay * bx
        dm = cx * by - cy * bx
        dn = ax * cy - ay * cx
        
        if det != 0:
            if dm % det != 0 or dn % det != 0:
                continue
            
            m1 = dm // det
            n1 = dn // det
            
            if 0 <= m1 and 0 <= n1:
                values.append(3*m1 + n1)
                    
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