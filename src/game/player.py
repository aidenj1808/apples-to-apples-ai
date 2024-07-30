from difflib import SequenceMatcher

class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.hand = []
        self.score = 0
        self.is_ai = is_ai
        self.correlation = {}

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
            self.hand.remove(best_match)
            return best_match

    def calculate_similarity(self, card1, card2):
        return SequenceMatcher(None, card1, card2).ratio()


