import itertools
import numpy as np
import matplotlib.pyplot as plt
from treys import Card, Deck, Evaluator

# Setup
evaluator = Evaluator()
your_hand = [Card.new('Ac'), Card.new('Ad')]
flop = [Card.new('Ah'), Card.new('2c'), Card.new('5h')]
known_cards = your_hand + flop

# Full deck without known cards
deck = Deck()
remaining_deck = [card for card in deck.cards if card not in known_cards]

# Generate all turn + river combinations
turn_river_combos = list(itertools.combinations(remaining_deck, 2))

# Store win ratio for each scenario
results = []

# Loop through all possible board completions
for turn, river in turn_river_combos:
    board = flop + [turn, river]
    full_known = known_cards + [turn, river]

    # Cards left for opponent hands
    available = [card for card in deck.cards if card not in full_known]

    win_count = 0
    total = 0

    # All possible opponent hands (2 cards, no overlap)
    for opp_hand in itertools.combinations(available, 2):
        your_score = evaluator.evaluate(board, your_hand)
        opp_score = evaluator.evaluate(board, list(opp_hand))

        if your_score < opp_score:
            win_count += 1
        total += 1

    win_ratio = win_count / total if total > 0 else 0
    results.append(win_ratio)

# Convert to 2D array with 1 row and N columns
heatmap = np.array(results).reshape(1, -1)

# Summary stats
total_cases = len(results)
wins = sum(1 for r in results if r == 1)
losses = sum(1 for r in results if r == 0)
draws = total_cases - wins - losses
win_pct = (wins / total_cases) * 100
loss_pct = (losses / total_cases) * 100
draw_pct = (draws / total_cases) * 100

# Plot heatmap as 1-row color strip
plt.figure(figsize=(20, 2))
plt.imshow(heatmap, cmap='RdYlGn', aspect='auto', interpolation='nearest')
plt.title(f"Poker Heatmap (All Outcomes Shown Individually)\n"
          f"Hand: ♣A♦A | Flop: ♥A♣2♥5 | "
          f"Wins: {wins} ({win_pct:.2f}%) | "
          f"Losses: {losses} ({loss_pct:.2f}%) | "
          f"Draws: {draw_pct:.2f}%")
plt.colorbar(label='Win Ratio (1 = Always Win, 0 = Always Lose)')
plt.yticks([])
plt.xlabel("Each tick = one turn+river scenario")
plt.tight_layout()
plt.show()
