from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def extrapolate(seq: list[int]) -> int:
    diff = [[val for val in seq]]
    
    while not all([val == 0 for val in diff[-1]]):
        new = []
        for i in range(1, len(diff[-1])):
            new.append(diff[-1][i] - diff[-1][i - 1])
        diff.append(new)
        
    for i in range(1, len(diff)):
        diff[-(i+1)].append(diff[-i][-1] + diff[-(i+1)][-1])
    
    return diff[0][-1]

def solve(lines: list[str]) -> int:
    total = 0
    values = []
        
    for line in lines:
        seq = line.strip().split()
        seq = [int(x) for x in seq]
        values.append(extrapolate(seq))
        
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