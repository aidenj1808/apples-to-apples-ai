import sys
import random


def agent_function(hand: list[str], green_card: str) -> str:
    return random.choice(hand)

def main():
    hand = sys.argv[1].split(',')
    green_card = " ".join(sys.argv[2:])
    play = agent_function(hand, green_card)
    print(play)

if __name__ == "__main__":
    main()
