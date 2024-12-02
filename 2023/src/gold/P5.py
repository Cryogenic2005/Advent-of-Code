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
        self.sourceStart = source_start
        self.destStart = dest_start
        self.length = length
    
    def mapRange(self, rangeKey: tuple[int,int]) -> tuple[int,int]:
        '''Map a range of values to their corresponding values'''
        # Find intersection of the range with the given range
        rangeKeyStart = max(rangeKey[0], self.sourceStart)
        rangeKeyEnd = min(rangeKey[0] + rangeKey[1], self.sourceStart + self.length)
        
        if rangeKeyStart >= rangeKeyEnd: # No intersection
            return (-1, 0)
        
        # Map the range
        mappedRangeStart = self.destStart + (rangeKeyStart - self.sourceStart)
        mappedRangeEnd = self.destStart + (rangeKeyEnd - self.sourceStart)
        
        # Return the mapped range
        return (mappedRangeStart, mappedRangeEnd - mappedRangeStart)
    
    def __getitem__(self, key: int) -> int:
        return self.destStart + (key - self.sourceStart)
    
    def __lt__(self, other: 'Range') -> bool:
        return self.sourceStart < other.sourceStart
    
    def __repr__(self) -> str:
        return f"{self.sourceStart} to {self.sourceStart + self.length} -> {self.destStart} to {self.destStart + self.length}"
    
class RangeMap:
    def __init__(self, ranges: list[Range]):
        self._ranges = ranges
        
    def add(self, source_start: int, dest_start: int, length: int):
        insort(self._ranges, Range(source_start, dest_start, length)) # Insert the range into the sorted list
        
    def mapRange(self, rangeKey: tuple[int,int]) -> list[tuple[int,int]]:
        '''Map a range of values to their corresponding values'''
        rangeKeyStart = rangeKey[0]
        rangeKeyEnd = rangeKey[0] + rangeKey[1]
        
        mappedRanges = []
        
        currPos = rangeKeyStart
        rangeId = self._binarySearchRange(currPos, True)
        range = self._ranges[rangeId] if 0 <= rangeId < len(self._ranges) else None
        
        while currPos < rangeKeyEnd:
            # Map the remaining values to themselves, if
            # - The range is None (reached the end of the ranges)
            # - We are before the start of the next range
            if range is None or currPos < range.sourceStart:
                closestRangeEnd = range.sourceStart if range is not None else rangeKeyEnd
                mappedRanges.append((currPos, closestRangeEnd - currPos))
                currPos = range.sourceStart if range is not None else rangeKeyEnd
                continue
                
            closestRangeEnd = min(range.sourceStart + range.length, rangeKeyEnd)
            mappedRanges.append(range.mapRange((currPos, closestRangeEnd - currPos)))
            currPos = closestRangeEnd
            
            # Get the next range
            rangeId += 1
            range = self._ranges[rangeId] if 0 <= rangeId < len(self._ranges) else None
    
        return mappedRanges
    
    def _binarySearchRange(self, key: int, nearestHigher: bool = False) -> int:
        '''
        Binary search for the range that contains the key.
        If the key is not found, return -1 if nearestHigher is False,
        else return the index of the nearest range that is higher than the key.
        '''
        
        start = 0
        end = len(self._ranges) - 1
        rangePos = -1
        while start <= end:
            mid = (start + end) // 2
            
            if key < self._ranges[mid].sourceStart:
                end = mid - 1
                if nearestHigher: # Only update the rangePos if we are looking for the nearest higher range
                    rangePos = mid
                continue
            
            if key >= self._ranges[mid].sourceStart + self._ranges[mid].length:
                start = mid + 1
                continue
            
            # The key is within the range
            return mid
        
        return rangePos
    
    def __getitem__(self, key: int) -> int:
        '''Get the value of the key, or key if the key is not found'''
        res = self._binarySearchRange(key)
        # If the key is not found, return itself
        return key if res == -1 else self._ranges[res][key]
    
    def __repr__(self) -> str:
        return f"RangeMap({self._ranges})"
    

def solve(lines: list[str]) -> int:
    lowest = 0
    values = []
    maps: list[RangeMap] = []
        
    seedRangesValues = lines[0].split()[1:] # Split by space, remove the first element
    seedRanges = zip(seedRangesValues[::2], seedRangesValues[1::2]) # Pair the seed ranges together
    seedRanges = [(int(start), int(range)) for start, range in seedRanges] # Convert the seed ranges to integers
    
    # Process the map ranges
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
    
    # Iterate through all the seed ranges and process them
    for start, len in seedRanges:
        keyRanges = [(start, len)]
        for map in maps:
            newKeyRanges = []
            for keyRange in keyRanges:
                newKeyRanges.extend(map.mapRange(keyRange))
            keyRanges = newKeyRanges
            
        # Append potential smallest value generated by this seed range
        values.append(min(keyRanges, key=lambda x: x[0])[0])
    
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