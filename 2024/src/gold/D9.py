from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def moveEnd(fileStr: list[list[str]]) -> list[list[str]]:
    tail_idx = len(fileStr) - 1
    
    while tail_idx >= 0:
        blk = fileStr[tail_idx]
        space = None
        for i in range(1, tail_idx, 2):
            if len(blk) <= len(fileStr[i]):
                space = i
                break
            
        if space is not None:
            fileStr[space] = fileStr[space][len(blk):]
            if tail_idx + 1 < len(fileStr):
                fileStr[tail_idx - 1].extend(fileStr[tail_idx + 1])
                fileStr.pop(tail_idx + 1)
                fileStr.pop(tail_idx)
            else:
                fileStr.pop(tail_idx)
            fileStr[tail_idx - 1].extend(['.'] * len(blk))
            fileStr.insert(space, blk) # insert file block
            fileStr.insert(space, []) # insert empty block
        else:
            tail_idx -= 2
    return fileStr

def buildString(fileStr: list[str]) -> list[list[str]]:
    idx = 0
    isFile = True
    blockstr: list[str] = []
    for char in fileStr:
        val = int(char)
        if isFile:
            blockstr.append([str(idx)] * val)
            idx += 1
        else:
            blockstr.append(['.'] * val)
                
        isFile = not isFile
    
    return blockstr

def checksum(s: list[str]) -> int:
    sum = 0
    
    for i, char in enumerate(s):
        if char == '.':
            continue
        
        sum += int(char) * i
        
    return sum

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    filestr = lines[0]
    blockStr = buildString(filestr)
    blockStr = moveEnd(blockStr)
    
    expandedBlockStr = []
    for block in blockStr:
        expandedBlockStr.extend(block)
    total = checksum(expandedBlockStr)    
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