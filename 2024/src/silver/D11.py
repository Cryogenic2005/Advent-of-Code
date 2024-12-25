from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def blink(stones: list[int]) -> list[int]:
    new_stones = deepcopy(stones)
    
    for i, stone in enumerate(stones):
        if stone == 0:
            new_stones[i] = 1
            continue
        
        digits = len(str(stone))
        
        if (digits%2) == 0:
            first_half = str(stone)[:digits//2]
            second_half = str(stone)[digits//2:]
            
            new_stones[i] = [int(first_half), int(second_half)]
        else:
            new_stones[i] *= 2024
            
    # split previous arrays
    i=0
    while i < len(new_stones):
        if isinstance(new_stones[i], list):
            half2 = new_stones[i][1]
            new_stones[i] = new_stones[i][0]
            new_stones.insert(i+1, half2)
            
        i += 1
            
    return new_stones

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    stones = [int(x) for x in lines[0].split()]
    
    for _ in range(25):
        values.append(len(stones))
        stones = blink(stones)
        
    total = len(stones)
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