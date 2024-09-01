#!/usr/bin/bash

#USAGE: bash testing_script NUM_GAMES

cd 65
echo "-------------------------------------------------------------------------"
echo "                      TESTING 65 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 70
echo "-------------------------------------------------------------------------"
echo "                      TESTING 70 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 75
echo "-------------------------------------------------------------------------"
echo "                      TESTING 75 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1
