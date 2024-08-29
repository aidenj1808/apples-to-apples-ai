#!/usr/bin/bash

#USAGE: bash testing_script NUM_GAMES

cd 10
echo "-------------------------------------------------------------------------"
echo "                      TESTING 10 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 25
echo "-------------------------------------------------------------------------"
echo "                      TESTING 25 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 50
echo "-------------------------------------------------------------------------"
echo "                      TESTING 50 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 100
echo "-------------------------------------------------------------------------"
echo "                      TESTING 100 Cluster Games                          "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1
