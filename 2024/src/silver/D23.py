from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def solve(lines: list[str]) -> int:
    total = 0
    values = []
        
    nodes = set()
    edges: dict[str, list[str]] = {}
    triangles: set[tuple[str, str, str]] = set()
    
    for line in lines:
        a, b = line.split('-')
        nodes.add(a)
        nodes.add(b)
        
        edges.setdefault(a, []).append(b)
        edges.setdefault(b, []).append(a)
        
    for node in nodes:
        if not node.startswith('t'):
            continue
        
        for i in range(len(edges[node])):
            for j in range(i + 1, len(edges[node])):
                a, b = edges[node][i], edges[node][j]
                 
                if b in edges[a]:
                    triangles.add(tuple(sorted([node, a, b])))
        
    values = list(triangles)
        
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
        
if __name__ == '__main__':
    main()