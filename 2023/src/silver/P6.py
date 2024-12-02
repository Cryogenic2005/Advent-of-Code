from pathlib import Path
from math import ceil, floor

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def solve(lines: list[str]) -> int:
    count = 1
    values = []
        
    times = lines[0].split()[1:]
    times = [int(x) for x in times]
    
    distances = lines[1].split()[1:]
    distances = [int(x) for x in distances]
    
    races = zip(times, distances)
    
    # Possible times must satisfy the inequality:
    # x^2 - t*x + (d+1) <= 0
    for t, d in races:
        delta = t*t - 4*(d+1)
        
        if delta < 0:
            values.append(0)
            continue
        
        # Solve the quadratic equation
        x1 = ceil((t - delta**0.5) / 2)
        x2 = floor((t + delta**0.5) / 2)
        
        # Also clamp the values within [0, t]
        x1 = max(0, min(t, x1))
        x2 = max(0, min(t, x2))
        
        values.append(x2 - x1 + 1)
        
    # Take product of all values
    for value in values:
        count *= value
    return count, values

def main():
    lines = []
    
    # Read the input file
    with open(INPUT, 'r') as f:
        lines = f.readlines()
    
    count, values = solve(lines)
    print(f"Count: {count}\n")
            
    # Write the output
    with open(OUTPUT, 'w') as f:
        f.write(str(count) + '\n\n')
        f.write(str(values) + '\n\n')
        
        if REOUTPUT_INPUT:
            for i, value in enumerate(values):
                f.write(f'{lines[i].strip()} -> {value}\n')
        
if __name__ == '__main__':
    main()