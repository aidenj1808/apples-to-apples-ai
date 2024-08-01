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
    hand = sys.argv[1].split(',')
    green_card = " ".join(sys.argv[2:])
    play = agent_function(hand, green_card)
    print(play)


if __name__ == "__main__":
    main()
