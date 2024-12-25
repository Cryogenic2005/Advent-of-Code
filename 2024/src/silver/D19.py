from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

memoize = {}

def isPossible(line: str, patterns: list[str]) -> bool:
    global memoize
    if memoize.get(line) != None:
        return memoize[line]
    
    memoize[line] = False
    
    for pattern in patterns:
        if len(line) < len(pattern):
            continue
        
        if line.startswith(pattern) and isPossible(line[len(pattern):], patterns):
            memoize[line] = True
            return True
        
    return False

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    patterns = lines[0].split(',')
    for i in range(len(patterns)):
        patterns[i] = patterns[i].strip()
    patterns.sort(key=len, reverse=True)
    
    global memoize
    memoize = {"": True}
    for pattern in patterns:
        memoize[pattern] = True
    
    for line in lines[2:]:
        values.append(isPossible(line, patterns))
                        
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