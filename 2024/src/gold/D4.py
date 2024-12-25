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
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            x, y = j, i
                
            cond = isValid(board, x + 1, y + 1) \
                and isValid(board, x + 1, y - 1) \
                and isValid(board, x - 1, y + 1) \
                and isValid(board, x - 1, y - 1)
                
            if not cond:
                continue
            
            xmasCheck = False
            if direction[0] == 0:
                xmasCheck = board[x][y] == 'A' \
                    and board[x + 1][y + direction[1]] == 'S' \
                    and board[x - 1][y + direction[1]] == 'S' \
                    and board[x + 1][y - direction[1]] == 'M' \
                    and board[x - 1][y - direction[1]] == 'M'
            else: # direction[1] == 0
                xmasCheck = board[x][y] == 'A' \
                    and board[x + direction[0]][y + 1] == 'S' \
                    and board[x + direction[0]][y - 1] == 'S' \
                    and board[x - direction[0]][y + 1] == 'M' \
                    and board[x - direction[0]][y - 1] == 'M'
                    
            if xmasCheck:
                total += 1
                
    return total

def solve(lines: list[str]) -> int:
    total = 0
    values = []
        
    board = [line.strip() for line in lines]
    dirs = [(0,1), (0,-1), (1,0), (-1,0)]
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