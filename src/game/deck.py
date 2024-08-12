<<<<<<< HEAD
import random

class Deck():
    def __init__(self, filename):
        self.cards = []
        self.size = 0
        self.filename = filename

        with open(filename, 'r') as file:
            file.readline()
            for line in file:
                _, card, _ = line.strip().split(",", 2)
                self.cards.append(card)
                self.size += 1

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        self.size -= 1
        return self.cards.pop()
=======
import random

class Deck():
    def __init__(self, filename):
        self.cards = []
        self.size = 0
        self.filename = filename

        with open(filename, 'r') as file:
            file.readline()
            for line in file:
                _, card, _ = line.strip().split(",", 2)
                self.cards.append(card)
                self.size += 1

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        self.size -= 1
        return self.cards.pop(0)
>>>>>>> 88cbc23 (Commit interim changes)
