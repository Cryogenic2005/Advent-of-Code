from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def extractNumbers(schematic: list[str]) -> list[list[int]]:
    numbers = [[0 for _ in range(len(schematic[0]))] for _ in range(len(schematic))]
        
    for row, line in enumerate(schematic):
        start = 0
        current = 0
        
        for i, char in enumerate(line):
            # Check if the character is a number
            if char.isdigit():
                # Check if this is the start of the number
                if current == 0:
                    start = i
                
                # Update the current number
                current = current * 10 + int(char)
                continue
            
            if current != 0:
                for j in range(start, i):
                    numbers[row][j] = current
                    
                current = 0
            
        # Final check for the last number in the row
        if current != 0:
            for j in range(start, len(line)):
                numbers[row][j] = current

    return numbers

def calcGearRatio(numbers: list[list[int]], gearRow: int, gearCol: int) -> int:
    checkLeft = gearCol > 0
    checkRight = gearCol < len(numbers[0]) - 1
    val = []
    
    # Check the row above and below the gear
    for row in [gearRow - 1, gearRow + 1]:
        if row < 0 or row >= len(numbers):
            continue
        
        if numbers[row][gearCol] != 0:
            val.append(numbers[row][gearCol])
            continue # The number in the middle is a part number,
                        # so the two numbers on the sides can only refer to that same part number
                        # thus we can skip the rest of the row
        
        if checkLeft:
            if numbers[row][gearCol - 1] != 0:
                val.append(numbers[row][gearCol - 1])
        
        if checkRight:
            if numbers[row][gearCol + 1] != 0:
                val.append(numbers[row][gearCol + 1])
        
    if checkLeft:
        if numbers[gearRow][gearCol - 1] != 0:
            val.append(numbers[gearRow][gearCol - 1])
    
    if checkRight:
        if numbers[gearRow][gearCol + 1] != 0:
            val.append(numbers[gearRow][gearCol + 1])
        
    return val[0]*val[1] if len(val) == 2 else 0
        
def solve(schematic: list[str]) -> int:
    total = 0
    values = []
    
    # Strip the new line character from the end of each line
    schematic = [line.strip() for line in schematic]
    
    numbers = extractNumbers(schematic)
    
    for row in range(len(numbers)):
        for col in range(len(numbers[0])):
            if schematic[row][col] == '*':
                ratio = calcGearRatio(numbers, row, col)
                
                if(ratio != 0):
                    values.append(ratio)

    total = sum(values)
    return total, values

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
        
        f.write(str(values))
        
        # for i, value in enumerate(values):
        #     output = f'{lines[i].strip()} -> {value}\n'
        #     f.write(output)
        
if __name__ == '__main__':
    main()