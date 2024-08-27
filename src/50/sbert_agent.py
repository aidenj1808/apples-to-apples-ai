"""
Installation:

Create virtual environment:
Mac/Linux:
python3 -m venv .venv

Windows:
python -m venv .venv
-----------------------------
Activate virtual environment:
Mac/Linux:
source .venv/bin/activate

Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
-----------------------------
Pip install:
Mac/Linux:
pip3 install -U sentence-transformers

Windows:
pip install -U sentence-transformers
"""
import sys
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def agent_function(hand: list[str], green_card: str):
    hand_embeddings = model.encode(hand)
    green_card_embedding = model.encode(green_card)

    similarities = model.similarity(hand_embeddings, green_card_embedding)
    card_scores = {card: score for card, score in zip(hand, similarities)}
    card_scores_sorted = sorted(card_scores.items(), key=lambda x:x[1], reverse=True)
    return card_scores_sorted[0][0]

def main():
    hand, green_card = sys.stdin.read().strip().split(" ", 1)
    hand = hand.split(",")
    hand = [card.replace("_", " ") for card in hand]
    play = agent_function(hand, green_card)
    print(play)


if __name__ == "__main__":
    main()
