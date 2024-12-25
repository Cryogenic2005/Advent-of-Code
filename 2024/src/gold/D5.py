from pathlib import Path
import re

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def shouldSwap(a: int, b: int, order: list[tuple[int, int]]) -> bool:
    if (a,b) in order or (b,a) in order:
        return (b,a) in order
    return False

def validate(order: list[tuple[int, int]], pages: list[int]) -> tuple[list[int],bool]:
    flag = False
    
    # Bubble
    for i in range(len(pages)):
        for j in range(len(pages) - i - 1):
            if shouldSwap(pages[j], pages[j+1], order):
                pages[j], pages[j+1] = pages[j+1], pages[j]
                flag = True
                
    return pages, flag

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    order = []
    
    for line in lines:
        if re.match(r'\d+\|\d+', line):
            a,b = line.split("|")
            order.append((int(a), int(b)))
            continue
        
        if line == "":
            continue

        pages = line.split(",")
        pages = [int(page) for page in pages]
        
        pages, flag = validate(order, pages)
        
        if flag:
            values.append(pages[len(pages) // 2])
            
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
        
        if REOUTPUT_INPUT:
            for i, value in enumerate(values):
                f.write(f'{lines[i].strip()} -> {value}\n')
        
if __name__ == '__main__':
    main()