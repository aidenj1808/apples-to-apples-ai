#!/usr/bin/bash

#USAGE: bash testing_script NUM_GAMES

cd 10
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 25
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 50
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 100
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1
