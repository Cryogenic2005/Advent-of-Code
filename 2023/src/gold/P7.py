from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_FILENAME = Path(__file__).name.replace('.py', '.txt')
TYPE = Path(__file__).parent.name # "gold" or "silver"
INPUT = ROOT / 'data' / 'input' / DATA_FILENAME
OUTPUT = ROOT / 'data' / 'output' / TYPE / DATA_FILENAME

REOUTPUT_INPUT = False

class Hand:
    _CARD_STRENGTH_MAP = {
        '2': 0, '3': 1, '4': 2, '5': 3, # 2-5
        '6': 4, '7': 5, '8': 6, '9': 7, # 6-9
        'T': 8, 'J': -1, 'Q': 10, 'K': 11, 'A': 12 # 10-A, J is joker (wild card) with value -1
    }
    
    _HAND_STRENGTH_MAP = {
        'high_card': 0,
        'pair': 1,
        'two_pair': 2,
        'three_of_a_kind': 3,
        'full_house': 4,
        'four_of_a_kind': 5,
        'five_of_a_kind': 6,
    }
    
    def __init__(self, hand: str):
        self.hand = hand
        
    def getHandType(self) -> str:
        cardMap = {'J': 0} # Initialize the card map with the joker, we can delete it later
        for card in self.hand:
            cardMap[card[0]] = cardMap.get(card[0], 0) + 1
        
        # Handle Jokers differently:
        # Jokers are wild cards and can be used as any card
        # The best hand with a joker is always obtained by
        # mimicking the most frequent card in the hand
        jokerCount = cardMap['J']
        del cardMap['J']
        
        if cardMap == {}: # If the hand is all jokers
            return 'five_of_a_kind'
        
        mostFrequentCard = max(cardMap, key=cardMap.get)
        cardMap[mostFrequentCard] += jokerCount
        
        match len(cardMap):
            case 5:
                return 'high_card'
            case 4:
                return 'pair'
            case 3:
                return 'three_of_a_kind' if 3 in cardMap.values() else 'two_pair'
            case 2:
                return 'full_house' if 3 in cardMap.values() else 'four_of_a_kind'
            case 1:
                return 'five_of_a_kind'

        raise ValueError(f'Invalid hand: {self.hand}')
        
    def __lt__(self, other: 'Hand') -> bool:
        if self.getHandType() != other.getHandType():
            return self._HAND_STRENGTH_MAP[self.getHandType()] < self._HAND_STRENGTH_MAP[other.getHandType()]
        
        for i in range(5):
            if self._CARD_STRENGTH_MAP[self.hand[i][0]] != self._CARD_STRENGTH_MAP[other.hand[i][0]]:
                return self._CARD_STRENGTH_MAP[self.hand[i][0]] < self._CARD_STRENGTH_MAP[other.hand[i][0]]

def solve(lines: list[str]) -> int:
    total = 0
    values = []
    hands: list[tuple[Hand, int]] = []
        
    for line in lines:
        hand, bet = line.strip().split()
        
        if len(hand) != 5:
            raise ValueError('Invalid hand size')
        
        hands.append((Hand(hand), int(bet)))
        
    hands.sort(key=lambda x: x[0])
    
    for i, (_, bet) in enumerate(hands):
        total += bet * (i + 1)
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