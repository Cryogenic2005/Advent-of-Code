import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / TYPE / 'output' / DATA_FILENAME

COLOR_MAX_MAP = {
    'red': 12, 'green': 13, 'blue': 14
}

def validateGame(line: str) -> tuple[bool, int]:
    '''Validate the game and return the ID if it is valid'''
    # Check if the line is valid
    res_id = re.search(r'Game (\d+):', line)
    
    if not res_id:
        raise ValueError(f'Invalid line: {line}')
    
    id = int(res_id.group(1))
    
    line = line[res_id.end():]
    reveals = line.split(';')
    for reveal in reveals:
        cubes = reveal.strip().split(',')
        for cube in cubes:
            cube_info = cube.strip().split(' ')
            
            count = int(cube_info[0])
            color = cube_info[1]
            
            if count > COLOR_MAX_MAP[color]:
                return False, id
            
    return True, id

def solve(lines: list[str]) -> int:
    sum = 0
    values = []
        
    for line in lines:
        isValid, id = validateGame(line)
        
        if isValid:
            sum += id
        values.append(isValid)
        
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