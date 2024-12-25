from pathlib import Path
import re

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def validate(order: list[tuple[int, int]], pages: list[str]) -> bool:
    idx_map = {}
    
    for i, page in enumerate(pages):
        idx_map[page] = i
        
    for a, b in order:
        if a in idx_map.keys() and b in idx_map.keys():
            if idx_map[a] > idx_map[b]:
                return False
    return True

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
        
        if validate(order, pages):
            values.append(pages[len(pages) // 2])
            
    total = sum(values)
    return total, values
                
class InputTransformer:
    def __init__(self, lines: list[str], toInt: bool = False, delimiter: str = ' ') -> None:
        self.lines = lines
        self.delimiter = delimiter
        if toInt:
            self.lines = [int(line) for line in self.lines]
        
    def fromVerticalLists(self) -> list[list[str|int]]:
        listCount = len(self.lines[0].split(self.delimiter))
        lists = [[] for _ in range(listCount)]
        
        for line in self.lines:
            lists.append([c for c in line.split(self.delimiter)])
            
    def fromHorizontalLists(self) -> list[list[str|int]]:
        return [line.split(self.delimiter) for line in self.lines]
    
    def fromMap(self) -> list[list[str|int]]:
        return self.lines

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