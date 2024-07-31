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


MODELFILE = """
FROM llama3.1
SYSTEM You are a judge for the card game Apples to Apples. Given a hand of nouns that are red cards, determine the noun with the most association with the adjective which is the green card. Your output should only contain the one noun card and nothing else. If you can't say one then choose one. Your output should only be the word you choose and nothing else. Your output should not contain any explanation and just the single word or phrase.
"""

model_created = False
for model in ollama.list()["models"]:
    if model["name"] == "judge":
        model_created = True

if not model_created:
    ollama.create(model="judge", modelfile=MODELFILE) 

def agent_function(hand: list[str], green_card: str) -> str:
    prompt = f"Noun red cards: {str(hand)[1: -1]}, Adjective green card: {green_card}"
    output = ollama.generate(model="judge", prompt=prompt)
    return output["response"]
    
def main():
    hand = sys.argv[1].split(',')
    green_card = sys.argv[2]
    play = agent_function(hand, green_card)
    print(play)


if __name__ == "__main__":
    main()
