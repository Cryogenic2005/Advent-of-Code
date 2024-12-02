from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = True

def calcPoints(winnings: list[int], values: list[int]) -> int:
    occur = -1
    for win in winnings:
        if win in values:
            occur += 1
            
    return 2**occur if occur >= 0 else 0

def solve(lines: list[str]) -> int:
    total = 0
    values = []
        
    for line in lines:
        # Preprocess the line
        # Remove card info
        line = line.strip().split(':')[1].strip()
        # Split the line into winnings and values
        winnings, numbers = line.split('|')
        
        winnings = [int(x) for x in winnings.split()]
        numbers = [int(x) for x in numbers.split()]
        
        values.append(calcPoints(winnings, numbers))
        
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
        f.write(str(sum) + '\n\n')
        f.write(str(values) + '\n\n')
        
        if REOUTPUT_INPUT:
            for i, value in enumerate(values):
                f.write(f'{lines[i].strip()} -> {value}\n')
        
if __name__ == '__main__':
    main()