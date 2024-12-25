from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def moveEnd(s: list[str]) -> str:
    head_idx = 0
    tail_idx = len(s) - 1
    
    while head_idx < tail_idx:
        while head_idx < len(s) and s[head_idx] != '.':
            head_idx += 1
            
        while tail_idx >= 0 and s[tail_idx] == '.':
            tail_idx -= 1
        
        if head_idx < tail_idx:
            s[head_idx], s[tail_idx] = s[tail_idx], s[head_idx]
                
    return s

def checksum(s: list[str]) -> int:
    sum = 0
    
    for i, char in enumerate(s):
        if char == '.':
            break
        
        sum += int(char) * i
        
    return sum

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    filestr = lines[0]
    
    # build string
    idx = 0
    isFile = True
    blockstr: list[str] = []
    for char in filestr:
        val = int(char)
        if isFile:
            blockstr.extend([str(idx)] * val)
            idx += 1
        else:
            blockstr.extend(['.'] * val)
                
        isFile = not isFile
        
    blockstr = moveEnd(blockstr)
    total = checksum(blockstr)
    
    # total = sum(values)
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
        
        if REOUTPUT_INPUT:
            for i, value in enumerate(values):
                f.write(f'{lines[i].strip()} -> {value}\n')
        
if __name__ == '__main__':
    main()