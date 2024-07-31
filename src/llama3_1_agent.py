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
Pull Llama3.1:
All:
ollama pull llama3.1

"""
import sys
import ollama


def agent_function(hand: list[str], green_card: str) -> str:
    hand = [card.lower() for card in hand]
    prompt = (f"What noun is most associated with {green_card}? {hand}."
        "Give me just your answer as one word and no explanation or punctuation.")
    output = ollama.generate(model="llama3.1", prompt=prompt)["response"]
    return output

    
def main():
    hand = sys.argv[1].split(',')
    green_card = sys.argv[2]
    play = agent_function(hand, green_card)
    print(play)


if __name__ == "__main__":
    main()
