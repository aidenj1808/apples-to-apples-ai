import os
from src.game.apples_to_apples import ApplesToApples
from src.game.deck import Deck
from src.game.player import Player

def main():
    player_names = ["P1", "P2", "P3", "AI"]
    players = [Player(name, is_ai=(name == "AI")) for name in player_names]

    red_deck_path = os.path.join('src', 'all_red_cards.csv')
    green_deck_path = os.path.join('src', 'all_green_cards.csv')
    red_deck = Deck(red_deck_path)
    green_deck = Deck(green_deck_path)

    game = ApplesToApples(players, red_deck, green_deck)

    game.start_game()

if __name__ == "__main__":
    main()

