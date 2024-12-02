from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def calcGamePower(line: str) -> int:
    '''Calculate the power of the game'''
    
    # Split into each reveal
    reveals = line.split(':')[1] \
        .strip() \
        .split(';')
        
    minMap = {
        'red': 0, 'green': 0, 'blue': 0
    }
    
    for reveal in reveals:
        # Split the cubes into different colors
        cubes = reveal.strip().split(',')
        for cube in cubes:
            # Split the cube info (count and color)
            cube_info = cube.strip().split(' ')
            
            count = int(cube_info[0])
            color = cube_info[1]
            
            if count > minMap[color]:
                minMap[color] = count
            
    power = minMap['red'] * minMap['green'] * minMap['blue']
    return power

def solve(lines: list[str]) -> int:
    sum = 0
    values = []
        
    for line in lines:
        power = calcGamePower(line)
        
        sum += power
        values.append(power)
        
    return sum, values

def main():
    lines = []
    
    # Read the input file
    with open(INPUT, 'r') as f:
        lines = f.readlines()
    
    sum, values = solve(lines)
    print(f"Sum: {sum}\n")
            
    # Write the output
    with open(OUTPUT, 'w') as f:
        f.write(str(sum))
        f.write('\n\n')
        
        for i, value in enumerate(values):
            output = f'{lines[i].strip()} -> {value}\n'
            f.write(output)
        
if __name__ == '__main__':
    main()