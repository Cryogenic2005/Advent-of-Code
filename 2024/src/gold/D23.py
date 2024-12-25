from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def bron_kerbosch(R: set[str], P:set[str], X:set[str], graph: dict[str, set[str]]):
    # Copied from geeksforgeeks since I never heard of this algorithm until the contest :(
    # (I probably won't consider this unless I knew this was NP-hard)
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosch(
            R.union({v}),
            P.intersection(graph[v]),
            X.intersection(graph[v]),
            graph
        )
        X.add(v)

def solve(lines: list[str]) -> int:
    total = 0
    values = []
        
    nodes = set()
    edges: dict[str, set[str]] = {}
    
    for line in lines:
        a, b = line.split('-')
        
        nodes.add(a)
        nodes.add(b)
        
        edges.setdefault(a, set()).add(b)
        edges.setdefault(b, set()).add(a)
        
    graph = {key: set(edges[key]) for key in edges}

    for clique in bron_kerbosch(set(), set(graph.keys()), set(), graph):
        if len(clique) > total:
            total = len(clique)
            values = sorted(list(clique))
        
    print(values)
        
    total = ','.join(values)
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