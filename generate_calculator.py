import itertools

# Function to encode a single card
def encode_card(rank, suit):
    rank_dict = {r: i for i, r in enumerate('23456789TJQKA')}
    suit_dict = {'h': 0, 'd': 1, 'c': 2, 's': 3}
    return (rank_dict[rank] << 2) | suit_dict[suit]

# Function to encode a hand (two cards) into 16 bits
def encode_hand(card1, card2):
    card1_encoded = encode_card(card1[0], card1[1])
    card2_encoded = encode_card(card2[0], card2[1])
    return (card1_encoded << 6) | card2_encoded

# Generate all possible two-card combinations
odds_table = {}

import itertools

# Example structure for storing odds (using a dictionary for simplicity)
odds_table = {}

# Possible ranks and suits (simplified for demonstration)
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['h', 'd', 'c', 's']

# Generate all possible two-card combinations
all_hands = list(itertools.combinations(itertools.product(ranks, suits), 2))

# Function to calculate odds
def calculate_odds(hand1, hand2):
    rank_dict = {r: i for i, r in enumerate('23456789TJQKA')}
    all_cards = list(itertools.product(ranks, suits))
    
    # Exclude hand1 and hand2 cards from community card pool
    community_pool = [card for card in all_cards if card not in hand1 and card not in hand2]
    
    # Generate all possible community card combinations (5 cards)
    community_combinations = list(itertools.combinations(community_pool, 5))
    
    hand1_wins = 0
    hand2_wins = 0
    ties = 0
    
    for community in community_combinations:
        hand1_strength = evaluate_hand(hand1, community)
        hand2_strength = evaluate_hand(hand2, community)
        
        if hand1_strength > hand2_strength:
            hand1_wins += 1
        elif hand2_strength > hand1_strength:
            hand2_wins += 1
        else:
            ties += 1
    
    total = hand1_wins + hand2_wins + ties
    hand1_odds = (hand1_wins / total) * 100
    hand2_odds = (hand2_wins / total) * 100
    tie_odds = (ties / total) * 100
    
    return hand1_odds, hand2_odds, tie_odds

# Populate the odds table
for hand1, hand2 in itertools.combinations(all_hands, 2):
    odds = calculate_odds(hand1, hand2)
    odds_table[(hand1, hand2)] = odds

# Generate Verilog lookup table
with open('odds_lut.v', 'w') as f:
    f.write('module odds_lut(input [15:0] hand1, input [15:0] hand2, output reg [7:0] odds);\n')
    f.write('always @(*) begin\n')
    f.write('case ({hand1, hand2})\n')
    for (hand1, hand2), odds in odds_table.items():
        hand1_encoded = encode_hand(*hand1)
        hand2_encoded = encode_hand(*hand2)
        f.write(f'    32\'h{hand1_encoded:04x}{hand2_encoded:04x}: odds = 8\'d{odds};\n')
    f.write('endcase\n')
    f.write('end\n')
    f.write('endmodule\n')