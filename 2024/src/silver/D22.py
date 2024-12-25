from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

def mix(a: int, b: int) -> int:
    return a ^ b

def prune(a: int) -> int:
    return a % 16777216

def nextSecret(secret: int) -> int:
    secret = prune(mix(secret, 64 * secret))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, 2048 * secret))
    
    return secret

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    for line in lines:
        secret = int(line)
        for _ in range(2000):
            secret = nextSecret(secret)
        
        values.append(secret)
        
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