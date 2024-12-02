from pathlib import Path
import re
from math import lcm
import pandas

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

VISUALIZE = True

def visualize(nodes: dict[str,tuple[str,str]]) -> None:
    from graphviz import Digraph
    
    dot = Digraph(format='png', engine='neato',
                    graph_attr=dict(sep='7'),
                    node_attr=dict(shape='circle',   
                                    margin='0',
                                    fontsize='8',
                                    width='0.4',
                                    height='0.4',
                                    fixedsize='true'))
    
    for node in nodes.keys():
        color = 'black'
        if node.endswith('A'):
            color = 'green'
        elif node.endswith('Z'):
            color = 'red'
        
        dot.node(node, color=color)
    
    for node, (left, right) in nodes.items():
        dot.edge(node, left, color='orange')
        dot.edge(node, right, color='blue')
    
    visualizationPath = ROOT / 'data' / 'visualization'
    visualizationName = visualizationPath / "P8_Graph_Visualization"
    dot.render(visualizationName, cleanup=True, view=True)
    return
    
def solve(lines: list[str]) -> int:
    total = 0
    values = []
    nodes: dict[str,tuple[str,str]] = {}
        
    route = lines[0].strip()
    for line in lines[2:]:
        res = re.search(r'(...) = \((...), (...)\)', line)
        
        nodes[res.group(1)] = (res.group(2), res.group(3))
    
    if VISUALIZE:
        visualize(nodes)
    
    # Retrieve all nodes ending with 'A'
    currNodes = []
    for node in nodes:
        if node.endswith('A'):
            currNodes.append(node)
            
    loopCnt = { node: 0 for node in currNodes }
            
    idx = 0 # Index of the route
    
    while True:
        dir = 0 if route[idx] == 'L' else 1
        idx = (idx + 1) % len(route)
        
        total += 1
        for i in range(len(currNodes)):
            currNodes[i] = nodes[currNodes[i]][dir]
        
        if currNodes[0].endswith('Z'):
            values.append(total)
        
        for i, node in enumerate(loopCnt.keys()):
            if loopCnt[node] != 0:
                continue
            
            if currNodes[i].endswith('Z'):
                loopCnt[node] = total
        
        if all([ val != 0 for val in loopCnt.values() ]):
            break
    
    values = loopCnt.values()
    total = lcm(*values)
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