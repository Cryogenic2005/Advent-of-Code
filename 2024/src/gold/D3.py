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
    
    # Concat all the lines into one string
    line = ''.join(lines)
    
    pattern_mul = r'mul\((\d+),(\d+)\)'
    pattern_do = r'do\(\)'
    pattern_dont = r'don\'t\(\)'
    
    # Find all the do and don'ts
        
    toggle = []
        
    do = re.finditer(pattern_do, line)
    dont = re.finditer(pattern_dont, line)
    for match in do:
        toggle.append((True, match.start(0)))
        
    for match in dont:
        toggle.append((False, match.start(0)))
            
    toggle.sort(key=lambda x: x[1])
    
    # Find all the multiplications
    
    i = 0
    toggled = True
    res = re.finditer(pattern_mul, line)
    
    # Decide to add the value or not based on the toggles
    
    for match in res:
        a = int(match.group(1))
        b = int(match.group(2))

        if match.start(0) > toggle[0][1]:   
            while i+1 < len(toggle) and match.start(0) > toggle[i+1][1]:
                i += 1
            
            toggled = toggle[i][0]            
        
        if toggled:
            values.append(a * b)
        
    total = sum(values)
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