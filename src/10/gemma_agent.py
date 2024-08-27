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
pip3 install ollama

Windows:
pip install ollama
-----------------------------
Pull Gemma2:
All:
ollama pull gemma2

"""
import sys
import ollama


def agent_function(hand: list[str], green_card: str) -> str:
    hand = [card.lower() for card in hand]
    prompt = (f"Given these words or phrases, {str(hand)[1: -1]} Which is most "
              f"associated with {green_card}?"
               "Give me just your answer exactly how the word is written, "
               "no explanation or punctuation.")
    output = ollama.generate(model="gemma2", prompt=prompt)["response"]
    return output

def main():
    hand, green_card = sys.stdin.read().strip().split(" ", 1)
    hand = hand.split(",")
    hand = [card.replace("_", " ") for card in hand]
    play = agent_function(hand, green_card)
    print(play)


if __name__ == "__main__":
    main()
