import itertools
import random
import numpy as np
import matplotlib.pyplot as plt
from treys import Card, Deck, Evaluator

# Set up evaluator and known hand/board
evaluator = Evaluator()
your_hand = [Card.new('Ac'), Card.new('Ad')]
flop = [Card.new('Ah'), Card.new('2c'), Card.new('5h')]
known_cards = your_hand + flop

# Get remaining cards from the deck
deck = Deck()
remaining_deck = [card for card in deck.cards if card not in known_cards]

# Generate all turn+river combinations
turn_river_combos = list(itertools.combinations(remaining_deck, 2))

# Initialize results array
results = []

# Simulate each possible turn/river combo
for turn, river in turn_river_combos:
    board = flop + [turn, river]

    # Get fresh deck and remove known cards
    temp_deck = [card for card in remaining_deck if card not in (turn, river)]

    # Sample 2 random opponent hands (4 cards, no overlap)
    opp_hand_cards = random.sample(temp_deck, 4)
    opp1 = opp_hand_cards[:2]
    opp2 = opp_hand_cards[2:]

    your_score = evaluator.evaluate(board, your_hand)
    opp1_score = evaluator.evaluate(board, opp1)
    opp2_score = evaluator.evaluate(board, opp2)

    # Win if both opponents score worse (higher = worse)
    win = (your_score < opp1_score) and (your_score < opp2_score)
    results.append(1 if win else 0)

# Convert results to heatmap format
size = int(np.ceil(np.sqrt(len(results))))
heatmap = np.zeros((size, size))
heatmap.flat[:len(results)] = results

# Calculate win/loss stats
total = len(results)
wins = sum(results)
losses = total - wins
win_pct = (wins / total) * 100
loss_pct = 100 - win_pct

# Plot
plt.figure(figsize=(10, 10))
plt.imshow(heatmap, cmap='RdYlGn', interpolation='nearest')
plt.title(f"Poker Heatmap: Win (Green) vs Loss (Red)\nHand: ♣A♦A | Flop: ♥A♣2♥5\n"
          f"Wins: {wins} ({win_pct:.2f}%)  |  Losses: {losses} ({loss_pct:.2f}%)")
plt.colorbar(label='1 = Win, 0 = Loss')
plt.axis('off')
plt.tight_layout()
plt.show()
