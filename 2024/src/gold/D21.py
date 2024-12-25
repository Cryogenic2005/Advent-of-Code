from pathlib import Path
from queue import PriorityQueue

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

UP, DOWN, LEFT, RIGHT, ACTIVATE = '^', 'v', '<', '>', 'A'
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
DIR_TO_ARROW_MAP = {
    (0, 1): DOWN,
    (0, -1): UP,
    (1, 0): RIGHT,
    (-1, 0): LEFT
}

ARROW_TO_DIR_MAP = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0)
}

NUMERICAL_KEYPAD = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
]

DIRECTIONAL_KEYPAD = [
    [None, '^', 'A'],
    ['<', 'v', '>']
]

def isValidMove(keypad: list[list[str]], pos: tuple[int, int]) -> bool:
    return 0 <= pos[0] < len(keypad[0]) and 0 <= pos[1] < len(keypad) and keypad[pos[1]][pos[0]] != None
    
def findAbsolute(instruction: str, isNumericKeypad: bool = False) -> tuple[int, int]:
    if not hasattr(findAbsolute, 'memoize'):
        findAbsolute.memoize = {}
        
    if (isNumericKeypad, instruction) in findAbsolute.memoize:
        return findAbsolute.memoize[(isNumericKeypad, instruction)]
    
    for y, row in enumerate(NUMERICAL_KEYPAD if isNumericKeypad else DIRECTIONAL_KEYPAD):
        for x, key in enumerate(row):
            findAbsolute.memoize[(isNumericKeypad, key)] = (x, y)
            if key == instruction:
                return (x, y)

def instructionsToMove(instruction: str, start: tuple[int, int], depth: int = 2, isNumericKeyPad: bool = False) -> int:
    if not hasattr(instructionsToMove, 'memoize'):
        instructionsToMove.memoize = {}
        
    if depth == -1:
        return 1 # Base case: User is the one executing the instruction, hence the cost is always 1
    
    # Memoize: The min cost to move to a certain instruction from a certain starting position
    if (instruction, start, depth, isNumericKeyPad) in instructionsToMove.memoize:
        return instructionsToMove.memoize[(instruction, start, depth, isNumericKeyPad)]
    
    keypad = NUMERICAL_KEYPAD if isNumericKeyPad else DIRECTIONAL_KEYPAD
    
    queue = PriorityQueue()
    queue.put((0, start, findAbsolute(ACTIVATE))) # (cost, curr_pos, lower_pos), sorted by cost via priority queue
    visited_states = set() # State: Same position, same lower depth position, potentially different cost
    
    while not queue.empty():
        cost, pos, lower_pos = queue.get()
        
        # If we've already visited this state, skip it
        # Since there is a more optimal path to reach this state
        if (pos, lower_pos) in visited_states:
            continue
        
        # Mark the current state as visited
        visited_states.add((pos, lower_pos))
        
        # Memoize the most optimal path to reach the current instruction
        # We need to press the activate button to output the instruction
        if cost >= instructionsToMove.memoize.get((instruction, start, depth, isNumericKeyPad), float('inf')):
            continue
        
        # If we've reached the target instruction, return the cost (guaranteed to be the lowest by priority queue)
        if keypad[pos[1]][pos[0]] == instruction:
            instructionsToMove.memoize[(instruction, start, depth, isNumericKeyPad)] = min(
                instructionsToMove.memoize.get((instruction, start, depth, isNumericKeyPad), float('inf')),
                cost + instructionsToMove(ACTIVATE, lower_pos, depth - 1)
            )
        
        # Try all possible moves
        for move in [UP, DOWN, LEFT, RIGHT]:
            new_pos = (pos[0] + ARROW_TO_DIR_MAP[move][0], pos[1] + ARROW_TO_DIR_MAP[move][1])
            
            if not isValidMove(keypad, new_pos):
                continue
            
            new_cost = cost + instructionsToMove(move, lower_pos, depth - 1)
            new_lower_pos = findAbsolute(move) # Update the lower position after each instruction
            
            queue.put((new_cost, new_pos, new_lower_pos))
    
    return instructionsToMove.memoize[(instruction, start, depth, isNumericKeyPad)]
    
def complexity(code: str) -> int:
    numericCode = int(code[:-1])
    instLength = 0
    
    # print(f"From 3 to 7: {instructionsToMove('7', findAbsolute('3', True), isNumericKeyPad = True)}")
    
    curr_pos = findAbsolute(ACTIVATE, isNumericKeypad = True)
    for char in code:
        instLength += instructionsToMove(char, curr_pos, depth = 25, isNumericKeyPad = True)
        # print(f"Instruction: {char}, Length: {instructionsToMove(char, curr_pos, isNumericKeyPad = True)}")
        curr_pos = findAbsolute(char, isNumericKeypad = True) # Update the current position after each instruction
        
    print(f"Code: {code}, Length: {instLength}, Numeric Code: {numericCode}")
    return instLength * numericCode
            
def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    for line in lines:
        values.append(complexity(line))
        
    total = sum(values)
    return total, values

def main():
    lines = []
    
    # Read the input file
    with open(INPUT, 'r') as f:
        lines = f.readlines()
    
    lines = [line.strip() for line in lines] # Remove leading/trailing whitespace
    
    sum, values = solve(lines)
    print(f"Sum: {sum}\n")
            
    # Write the output
    with open(OUTPUT, 'w') as f:
        f.write(str(sum) + '\n\n')
        f.write(str(values) + '\n\n')
        
if __name__ == '__main__':
    main()