#!/usr/bin/bash

#USAGE: bash testing_script NUM_GAMES

cd 40
echo "-------------------------------------------------------------------------"
echo "                      TESTING 40 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 45
echo "-------------------------------------------------------------------------"
echo "                      TESTING 45 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 55
echo "-------------------------------------------------------------------------"
echo "                      TESTING 55 Cluster Games                           "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1

cd ..
cd 60
echo "-------------------------------------------------------------------------"
echo "                      TESTING 60 Cluster Games                          "
echo "-------------------------------------------------------------------------"
python3 driver_async_rl.py llama_agent.py gemma_agent.py sbert_agent.py RLAgent.py $1
