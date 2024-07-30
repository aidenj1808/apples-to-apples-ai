import random
from .player import Player
from .deck import Deck
from .word_associations import get_all_associations, get_adj_associations, get_noun_associations

class ApplesToApples:
    def __init__(self, players, red_deck, green_deck):
        self.players = players
        self.red_deck = red_deck
        self.green_deck = green_deck

        self.red_deck.shuffle()
        self.green_deck.shuffle()

        self.current_judge_index = random.randint(0, len(self.players)-1)
        self.deal_hands()

    def deal_hands(self):
        for player in self.players:
            for _ in range(7):
                card = self.red_deck.draw_card()
                player.hand.append(card)

    def start_game(self):
        while not self.game_over():
            self.pick_and_play_round()


    def pick_and_play_round(self):
        current_judge = self.players[self.current_judge_index]
        print(f"\nJudge: {current_judge.name}")
        green_card = self.green_deck.draw_card()
        print(f"Green card picked: {green_card}")
        red_cards = self.pick_red_cards(green_card)
        print("Red cards picked by other players (in random order):")
        for name, card in red_cards.items():
            print(f"{name}: {card}")
        winner_name = self.pick_winner(red_cards)
        print(f"Winner: {winner_name}")
        for player in self.players:
            if player.name == winner_name:
                player.score += 1
                print(f"{player.name} won the round and has {player.score} points.")
                if player.score == 4:
                    print(f"{player.name} has won the game!")
                return self.current_judge_index == (self.current_judge_index + 1) % len(self.players)



    def pick_red_cards(self, green_card):
        red_cards = {}
        print(f"\nGreen card for this round: {green_card}")

        for i, player in enumerate(self.players):
            if i != self.current_judge_index:
                if player.is_ai:
                    card = player.play_red_card(green_card)
                    print(f"\n{player.name} (AI) played: {card}")
                else:
                    print(f"\n{player.name}, it's your turn.")
                    print("Your hand:", player.hand)
                    card_index = int(input("Enter the index of the red card you want to play: "))
                    card = player.hand.pop(card_index)
                    player.hand.append(self.red_deck.draw_card())
                red_cards[player.name] = card
                for p in self.players:
                    if p != player:
                        p.associate_correlation(green_card, [card])
        return red_cards

    def pick_winner(self, red_cards):
        judge = self.players[self.current_judge_index]
    
        if judge.is_ai:
            return random.choice(list(red_cards.keys()))
    
        print("Judge, it's your turn to pick the winning red card.")
        for i, (name, card) in enumerate(red_cards.items()):
            print(f"{i}: {name} - {card}")
        winner_index = int(input("Enter the index of the winning red card: "))
        winner_name = list(red_cards.keys())[winner_index]
        return winner_name

    def game_over(self):
        return any(player.score == 4 for player in self.players)

