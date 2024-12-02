from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / TYPE / 'output' / DATA_FILENAME

def isPartNumber(schematic: list[str], start: int, end: int, row: int) -> bool:
    '''Check if the schematic is a part number'''
    
    # Check surrounding characters around number for special characters
    for i in range(max(row - 1, 0), min(row + 2, len(schematic))): # Check row above and below
        for j in range(max(start - 1, 0), min(end + 2, len(schematic[row]))): # Check column from before to after
            if schematic[i][j] != '.' and not schematic[i][j].isdigit():
                return True
            
    return False

def solve(schematic: list[str]) -> int:
    total = 0
    values = []
    
    # Strip the new line character from the end of each line
    schematic = [line.strip() for line in schematic]
        
    for row, line in enumerate(schematic):
        start = 0
        end = 0
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
            
            # There is no digit to update, check if there is a part number to validate
            if current == 0:
                continue
            else:
                end = i - 1
            
            # Check if this is a part number
            if isPartNumber(schematic, start, end, row):
                values.append(current)
                
            current = 0
            
        # Final check in case the number is at the end of the line
        if current != 0 and isPartNumber(schematic, start, len(line) - 1, row):
            values.append(current)                

    total = sum(values)                
    return total, values

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
        
        f.write(str(values))
        
        # for i, value in enumerate(values):
        #     output = f'{lines[i].strip()} -> {value}\n'
        #     f.write(output)
        
if __name__ == '__main__':
    main()