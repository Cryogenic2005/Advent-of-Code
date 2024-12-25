from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def isSafe(report: list[str]) -> int:
    diff = report[1] - report[0]
    inc = diff > 0
    if abs(diff) > 3 or abs(diff) < 1:
        return 0
    
    for i in range(2, len(report)):
        diff = report[i] - report[i-1]
        if inc and diff < 0:
            return 0
        elif not inc and diff > 0:
            return 0
        
        if abs(diff) > 3 or abs(diff) < 1:
            return 0
        
    return 1

def solve(lines: list[str]) -> int:
    total = 0
    values = []
        
    for line in lines:
        report = line.strip().split()
        report = [int(x) for x in report]
        safe = isSafe(report)
        values.append(safe)
        
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