from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def canCalc(target: int, nums: list[int]) -> bool:
    bitmap = ''
    for i in range(2**(len(nums)-1)):
        bitmap = bin(i)[2:].zfill(len(nums)-1)
        
        total = nums[0]
        for j in range(len(bitmap)):
            if bitmap[j] == '1':
                total *= nums[j+1]
            else:
                total += nums[j+1]
        
        if total == target:
            return True

    return False
        
def solve(lines: list[str]) -> int:
    total = 0
    values = []
    
    for line in lines:
        target, nums = line.split(':')
        target = int(target.strip())
        nums = [int(num) for num in nums.split()]
        
        if canCalc(target, nums):
            values.append(target)
        
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
        
        if REOUTPUT_INPUT:
            for i, value in enumerate(values):
                f.write(f'{lines[i].strip()} -> {value}\n')
        
if __name__ == '__main__':
    main()