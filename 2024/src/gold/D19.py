from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

memoize = {}

def countPossible(target: str, patterns: list[str]) -> int:
    global memoize
    if memoize.get(target) != None:
        return memoize[target]
    
    memoize[target] = 0
    
    for pattern in patterns:
        if len(target) < len(pattern):
            continue
        
        if target.startswith(pattern):
            memoize[target] += countPossible(target[len(pattern):], patterns)
        
    return memoize[target]

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    patterns = lines[0].split(',')
    for i in range(len(patterns)):
        patterns[i] = patterns[i].strip()
    patterns.sort(key=len, reverse=True)
    
    global memoize
    memoize = {"": 1}
    
    for line in lines[2:]:
        values.append(countPossible(line, patterns))

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