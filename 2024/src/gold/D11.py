from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def blink(stone: int, count: int) -> int:
    if count == 0:
        return 1
    
    if (stone, count) in blink.dp_map:
        return blink.dp_map[(stone, count)]
    
    res = 0
    
    str_stone = str(stone)
    
    if stone == 0:
        res = blink(1, count-1)
    elif len(str_stone) % 2 == 0:
        half1 = int(str_stone[:len(str_stone)//2])
        half2 = int(str_stone[len(str_stone)//2:])
        res = blink(half1, count-1) + blink(half2, count-1)
    else: # count == 0
        res = blink(stone*2024, count-1)
        
    blink.dp_map[(stone, count)] = res
    
    return res

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    stones = [int(x) for x in lines[0].split()]
    
    blink.dp_map = {}
    for stone in stones:
        values.append(blink(stone, 75))
        
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