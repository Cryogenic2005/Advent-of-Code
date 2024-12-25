from pathlib import Path
import re
from graphviz import Digraph

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def calcWire(wire1: bool, op: str, wire2: bool) -> bool:
    match op:
        case 'AND':
            return wire1 & wire2
        case 'OR':
            return wire1 | wire2
        case 'XOR':
            return wire1 ^ wire2
        case _:
            raise ValueError(f"Invalid operation: {op}")

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    wires_dependents = {}
    wires = {}
    
    i = 0
    while lines[i] != '':
        name, value = lines[i].split(': ')
        wires[name] = bool(int(value))
        
        i += 1
        
    for line in lines[i+1:]:
        if line == '':
            continue
        
        res = re.match(r'(.+) ([A-Z]+) (.+) -> (.+)', line)
        w1, op, w2, wire3 = res.groups()
        
        wires_dependents[wire3] = (w1, op, w2)
        
    for wire3, (wire1, op, wire2) in wires_dependents.items():
        if wire3 in wires:
            continue
        
        process = [wire3]
        while process:
            wire = process[-1]
            
            if wire in wires:
                process.pop()
                continue
            
            w1, op, w2 = wires_dependents[wire]
            
            if w1 not in wires:
                process.append(w1)
                continue
                
            if w2 not in wires:
                process.append(w2)
                continue
            
            wires[wire] = calcWire(wires[w1], op, wires[w2])
            process.pop()
        
        wires[wire3] = calcWire(wires[wire1], op, wires[wire2])
        
    # Below is code to help find the first mismatch
    # Then I looked at the graph and fix the input by hand
    
    x, y, z = 0, 0, 0
    for wire, value in wires.items():
        if wire.startswith('x') and wires[wire]:
            x += 2 ** int(wire[1:])
        elif wire.startswith('y') and wires[wire]:
            y += 2 ** int(wire[1:])
        elif wire.startswith('z') and wires[wire]:
            z += 2 ** int(wire[1:])
            
    expected_z = x + y
    expected_z_bits = [int(bit) for bit in bin(expected_z)[2:]]
    
    
    print(f"x: {x}, y: {y}, z: {expected_z}")
    # Print in bits
    print(f"True x: 0{bin(x)[2:]}")
    print(f"True y: 0{bin(y)[2:]}")
    print(f"True z: {bin(expected_z)[2:]}")
    print(f"Real z: {bin(z)[2:]}")
    
    # Print first mismatch in reverse order
    for i in range(1, len(expected_z_bits)+1):
        if expected_z_bits[-i] != z % 2:
            print(f"First mismatch: {i-1}")
            break
        z //= 2

    # Create a graph to visualize the circuit
    
    graph_view = Digraph(engine='neato', format='png')
    
    for wire, value in wires.items():
        graph_view.node(wire, color='green' if value else 'red')
    
    for wire3, (wire1, op, wire2) in wires_dependents.items():
        graph_view.edge(wire1, wire3)
        graph_view.edge(wire2, wire3)
        
    graph_view.render('graph', view=True, cleanup=True)
    
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