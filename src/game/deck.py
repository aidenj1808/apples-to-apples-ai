import random

class Deck():
    def __init__(self, filename):
        self.cards = []
        self.size = 0
        self.filename = filename

        with open(filename, 'r') as file:
            for line in file:
                self.cards.append(line.strip())
                self.size += 1

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        self.size -= 1
        return self.cards.pop(0)
