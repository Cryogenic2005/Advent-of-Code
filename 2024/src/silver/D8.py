from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def isValid(x: int, y: int, lines: list[str]) -> bool:
    return y >= 0 and y < len(lines) and x >= 0 and x < len(lines[0])

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    antinode = [[False for _ in range(len(lines[0]))] for _ in range(len(lines))]
    node_map: dict[str, list[tuple[int,int]]] = {}
    
    for i, row in enumerate(lines):
        for j, char in enumerate(row):
            if char != '.':
                if char not in node_map:
                    node_map[char] = []
                
                node_map[char].append((j, i))
        
    for nodes in node_map:
        for i in range(len(node_map[nodes])):
            for j in range(i + 1, len(node_map[nodes])):
                node1 = node_map[nodes][i]
                node2 = node_map[nodes][j]
                
                dx = node1[0] - node2[0]
                dy = node1[1] - node2[1]
                
                antinode1 = (node1[0] + dx, node1[1] + dy)
                antinode2 = (node2[0] - dx, node2[1] - dy)
                
                if isValid(antinode1[0], antinode1[1], lines):
                    antinode[antinode1[1]][antinode1[0]] = True
                    
                if isValid(antinode2[0], antinode2[1], lines):
                    antinode[antinode2[1]][antinode2[0]] = True
    
    for i in range(len(antinode)):
        for j in range(len(antinode[0])):
            if antinode[i][j]:
                values.append((j, i))
                
    total = len(values)
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
        
        if REOUTPUT_INPUT:
            for i, value in enumerate(values):
                f.write(f'{lines[i].strip()} -> {value}\n')
        
if __name__ == '__main__':
    main()