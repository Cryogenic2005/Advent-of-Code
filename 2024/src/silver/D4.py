from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def isValid(board: list[str], x: int, y: int) -> bool:
    return 0 <= y < len(board) and 0 <= x < len(board[0])

def countXmas(board: list[str], direction: tuple[int, int]) -> int:
    x, y = 0, 0
    total = 0
    letter = ['X','M','A','S']
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            x, y = j, i
            curr = 0
            
            while board[y][x] == letter[curr]:
                curr += 1
                x += direction[0]
                y += direction[1]
                
                if curr == 4:
                    total += 1
                    break
                
                if not isValid(board, x, y):
                    break
                
                
    return total

def solve(lines: list[str]) -> int:
    total = 0
    values = []
        
    board = [line.strip() for line in lines]
    dirs = [(0,1), (0,-1), (1,1), (1,-1), (1,0), (-1,0), (-1,1), (-1,-1)]
    for d in dirs:
        values.append(countXmas(board, d))
        
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