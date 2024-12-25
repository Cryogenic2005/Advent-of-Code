from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

def getTernary(num: int) -> str:
    if num == 0:
        return '0'
    
    ternary = ''
    while num:
        num, remainder = divmod(num, 3)
        ternary = str(remainder) + ternary
    
    return ternary

def canCalc(target: int, nums: list[int]) -> bool:
    bitmap = ''
    for i in range(3**(len(nums)-1)):
        bitmap = getTernary(i).zfill(len(nums)-1)
        
        total = nums[0]
        for j in range(len(bitmap)):
            if bitmap[j] == '0':
                total += nums[j+1]
            elif bitmap[j] == '1':
                total *= nums[j+1]
            elif bitmap[j] == '2': # Concatenate
                total = int(str(total) + str(nums[j+1]))
                
            if total > target:
                break
        
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