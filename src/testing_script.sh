#!/usr/bin/bash

#USAGE: bash testing_script NUM_GAMES

cd 65
for i in $(seq 1 $1)
do
    echo "---------------------------------------------------------------------"
    echo "                TESTING 65 Clusters Agent                            "
    echo "                        Game: $i                                     "
    echo "---------------------------------------------------------------------"
    python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py 1
done
