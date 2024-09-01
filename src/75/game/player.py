from difflib import SequenceMatcher


# create a player class for Apples to Apples which has a name and a hand of red cards and a score checks for AI players and associates correlation
class Player:
    def __init__(self, name, is_ai=False):
        self.name = name        #name of the player
        self.hand = []          #list of red cards in the player's hand
        self.score = 0          #score of the player
        self.is_ai = is_ai      #check if the player is an AI
        self.correlation = {}   #correlation of the player's hand to the green card

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def associate_correlation(self, green_card, red_cards):
        if self.is_ai:
            if green_card not in self.correlation:
                self.correlation[green_card] = {'Perfect Match': [], 'High Match': [], 'Low Match': []}
            for card in red_cards:
                similarity = self.calculate_similarity(card, green_card)
                if similarity == 1:
                    self.correlation[green_card]['Perfect Match'].append(card)
                elif similarity >= 0.7:
                    self.correlation[green_card]['High Match'].append(card)
                elif similarity >= 0.5:
                    self.correlation[green_card]['Low Match'].append(card)

    def play_red_card(self, green_card):
        if self.is_ai:
            best_match = None
            best_similarity = 0
            for card in self.hand:
                similarity = self.calculate_similarity(card, green_card)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = card
            return best_match

    def calculate_similarity(self, card1, card2):
        return SequenceMatcher(None, card1, card2).ratio()
