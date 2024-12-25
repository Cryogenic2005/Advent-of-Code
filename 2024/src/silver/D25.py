from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    locks: list[tuple[int,int,int,int,int]] = []
    keys: list[tuple[int,int,int,int,int]] = []
    
    # Every lock/key is 5 characters wide
    # Every lock/key is 7 lines long,
    #   with one blank line between each lock/key
    for i in range(0, len(lines), 8):
        heights = [0, 0, 0, 0, 0]
        isLock = lines[i] == '#####'
        
        for line in lines[i:i+7]:
            for j, c in enumerate(line):
                if c == '#':
                    heights[j] += 1
                    
        if isLock:
            locks.append(tuple(heights))
        else:
            keys.append(tuple(heights))
        
    # For each lock, find all keys that has no overlapping heights    
    for lock in locks:
        keyCnt = 0
        for key in keys:
            if all([lock[i] + key[i] <= 7 for i in range(5)]):
                keyCnt += 1
                
        values.append(keyCnt)
        
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