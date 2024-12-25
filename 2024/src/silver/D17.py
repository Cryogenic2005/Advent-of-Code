from pathlib import Path
import re

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    reg_a = re.match(r'Register A: (\d+)', lines[0])
    reg_b = re.match(r'Register B: (\d+)', lines[1])
    reg_c = re.match(r'Register C: (\d+)', lines[2])
    program = lines[4].split(':')[1].strip().split(',')
    
    reg_a = int(reg_a.group(1))
    reg_b = int(reg_b.group(1))
    reg_c = int(reg_c.group(1))
    program = [int(x) for x in program]
    
    pc = 0
    output = []
    while pc < len(program):
        if pc+1 >= len(program):
            break
        
        opcode = program[pc]
        operand = program[pc+1]
        
        literal_operand = operand
        combo_operand = operand
        if operand >= 4: # Adjust combo operand if operand is 4 or greater
            match operand:
                case 4: combo_operand = reg_a
                case 5: combo_operand = reg_b
                case 6: combo_operand = reg_c
                case _: combo_operand = None # Error, should not happen
            
        match opcode:
            case 0: reg_a //= (2**combo_operand)
            case 1: reg_b ^= literal_operand
            case 2: reg_b = combo_operand % 8
            case 3: pc = program[pc+1] if reg_a != 0 else pc
            case 4: reg_b ^= reg_c
            case 5: output.append(combo_operand % 8)
            case 6: reg_b = reg_a // 2**combo_operand
            case 7: reg_c = reg_a // 2**combo_operand
                
        if opcode != 3 or reg_a == 0: # If jumped, don't increment pc
            pc += 2
        
    values = ','.join(map(str, output))
    print(f"Values: {values}")
    # total = sum(values)
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