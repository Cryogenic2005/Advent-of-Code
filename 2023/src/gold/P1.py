import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / TYPE / 'output' / DATA_FILENAME

DIGITS_MAP = {
    # By numbers
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    # By letters
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
}

def findFirstDigit(line: str) -> int:
    '''Find the first digit in a line using values from DIGITS_MAP'''
    matchValue = -1
    firstOccurrence = len(line)
    
    for key, value in DIGITS_MAP.items():
        res = re.search(rf'^.*?({key})', line)
        
        # If there is no match, continue to the next key
        if not res:
            continue
        
        # If occurred earlier, update the first occurrence
        if res.start(1) < firstOccurrence:
            matchValue = value
            firstOccurrence = res.start(1)
    
    return matchValue

def findLastDigit(line: str) -> int:
    '''Find the last digit in a line using values from DIGITS_MAP'''
    matchValue = -1
    lastOccurrence = -1
    
    for key, value in DIGITS_MAP.items():
        res = re.search(rf'^.*({key})', line)
        
        # If there is no match, continue to the next key
        if not res:
            continue
        
        # If occurred later, update the last occurrence
        if res.start(1) > lastOccurrence:
            matchValue = value
            lastOccurrence = res.start(1)
            
    return matchValue
        
def solve(lines: list[str]) -> int:
    sum = 0
    values = []
        
    for line in lines:
        first = findFirstDigit(line)
        last = findLastDigit(line)
        
        if first != -1 and last != -1:
            # Concatenate the first and last digits into a two-digit number
            values.append(first * 10 + last)
            sum += values[-1]
        else:
            raise ValueError('No digits found in line')
        
    return sum, values

def main():
    lines = []
    
    # Read the input file
    with open(INPUT, 'r') as f:
        lines = f.readlines()
    
    sum, values = solve(lines)
    print(f"Sum: {sum}")
            
    # Write the output
    with open(OUTPUT, 'w') as f:
        f.write(str(sum))
        f.write('\n\n')
        
        for i, value in enumerate(values):
            output = f'{lines[i].strip()} -> {value}\n'
            f.write(output)
        
if __name__ == '__main__':
    main()