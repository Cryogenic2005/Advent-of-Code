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
    
    buyer_seqs: list[dict[tuple[int,int,int,int], int]] = []
    unique_tuples: set[tuple[int,int,int,int]] = set()
    
    for i, line in enumerate(lines):
        prev_secret = None
        secret = int(line)
        changes = []
        buyer_seqs.append(dict())
        
        for _ in range(2000):
            prev_secret = secret
            secret = nextSecret(secret)
            changes.append((secret % 10) - (prev_secret % 10))
            
            if len(changes) >= 4:
                pattern = tuple(changes[-4:])
                if pattern not in buyer_seqs[-1]:
                    buyer_seqs[-1][pattern] = secret % 10
                    unique_tuples.add(pattern)
        
        if i % 100 == 0:
            print(f"i: {i}, progress: {i / len(lines) * 100:.2f}%")
        
        values.append(secret)
    
    print(len(unique_tuples))
    
    max_total = 0
    for i, key in enumerate(unique_tuples):
        sales = [buyer_seq.get(key, 0) for buyer_seq in buyer_seqs]
        total = sum(sales)
        if total > max_total:
            max_total = total
            values = sales
            
        if i % 2500 == 0:
            print(f"i: {i}, progress: {i / len(unique_tuples) * 100:.2f}%")
                        
    total = sum(values)
    return max_total, values

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