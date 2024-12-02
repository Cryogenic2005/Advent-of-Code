from pathlib import Path
from bisect import insort
import re

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

class Range:
    def __init__(self, source_start: int, dest_start: int, length: int):
        self.source_start = source_start
        self.dest_start = dest_start
        self.length = length
    
    def __getitem__(self, key: int) -> int:
        return self.dest_start + (key - self.source_start)
    
    def __lt__(self, other: 'Range') -> bool:
        return self.source_start < other.source_start
    
    def __repr__(self) -> str:
        return f"{self.source_start} to {self.source_start + self.length} -> {self.dest_start} to {self.dest_start + self.length}"
    
class RangeMap:
    def __init__(self, ranges: list[Range]):
        self.ranges = ranges
        self.ranges.sort()
        
    def add(self, source_start: int, dest_start: int, length: int):
        insort(self.ranges, Range(source_start, dest_start, length))
    
    def __getitem__(self, key: int) -> int:
        '''Get the value of the key, or key if the key is not found'''
        # Binary search
        start = 0
        end = len(self.ranges) - 1
        while start <= end:
            mid = (start + end) // 2
            mid_range = self.ranges[mid]
            
            if key < mid_range.source_start:
                end = mid - 1
                continue
            
            if key >= mid_range.source_start + mid_range.length:
                start = mid + 1
                continue
            
            # The key is within the range
            return mid_range[key]
            
        # If the key is not found, return itself
        return key
    
    def __repr__(self) -> str:
        return f"RangeMap({self.ranges})"
    

def solve(lines: list[str]) -> int:
    lowest = 0
    values = []
    maps: list[RangeMap] = []
        
    seeds = lines[0].split()[1:]
    seeds = [int(seed) for seed in seeds]
    
    for line in lines[1:]:
        line = line.strip()
        
        if line.endswith('map:'):
            maps.append(RangeMap([]))
            continue
            
        if re.match(r'\d+ \d+ \d+', line): # Line contains a range
            dest_start, source_start, length = line.split()
            
            source_start = int(source_start)
            dest_start = int(dest_start)
            length = int(length)
            
            maps[-1].add(source_start, dest_start, length)
    
    for seed in seeds:
        key = seed
        for map in maps:
            key = map[key]
            
        values.append(key)
    
    lowest = min(values)
    return lowest, values

def main():
    lines = []
    
    # Read the input file
    with open(INPUT, 'r') as f:
        lines = f.readlines()
    
    lowest, values = solve(lines)
    print(f"Lowest Location: {lowest}\n")
            
    # Write the output
    with open(OUTPUT, 'w') as f:
        f.write(str(lowest) + '\n\n')
        f.write(str(values) + '\n\n')
        
        if REOUTPUT_INPUT:
            for i, value in enumerate(values):
                f.write(f'{lines[i].strip()} -> {value}\n')
        
if __name__ == '__main__':
    main()