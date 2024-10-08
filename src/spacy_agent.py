import sys
import spacy


nlp = spacy.load("en_core_web_lg")

def agent_function(hand: list[str], green_card: str) -> str:
    associations = []
    green_card_doc = nlp(green_card)
    for red_card in hand:
        red_card_doc = nlp(red_card)
        association = red_card_doc.similarity(green_card_doc)
        associations.append([red_card, association])

    associations_sorted = sorted(associations, key=lambda x:x[1], reverse=True)
    return associations_sorted[0][0]

def main():
    hand, green_card = sys.stdin.read().strip().split(" ", 1)
    hand = hand.split(",")
    hand = [card.replace("_", " ") for card in hand]
    play = agent_function(hand, green_card)
    print(play)


if __name__ == "__main__":
    main()
