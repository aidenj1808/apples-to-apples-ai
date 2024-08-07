import sys
import random
import time


def agent_function(hand: list[str], green_card: str) -> str:
    time.sleep(3)
    return random.choice(hand)

def main():
    hand, green_card = sys.stdin.read().strip().split(" ", 1)
    hand = hand.split(",")
    hand = [card.replace("_", " ") for card in hand]
    play = agent_function(hand, green_card)
    print(play)


if __name__ == "__main__":
    main()
