from pathlib import Path
import re

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    nodes: dict[str,tuple[str,str]] = {}
        
    route = lines[0].strip()
    
    for line in lines[2:]:
        res = re.search(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)', line)
        
        nodes[res.group(1)] = (res.group(2), res.group(3))
        
    curr = 'AAA'
    idx = 0
    
    while curr != 'ZZZ':
        dir = route[idx]
        idx = (idx + 1) % len(route)
        
        curr = nodes[curr][0] if dir == 'L' else nodes[curr][1]
        values.append(curr)

    total = len(values)
    return total, values

def main():
    lines = []
    
    # Read the input file
    with open(INPUT, 'r') as f:
        lines = f.readlines()
    
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