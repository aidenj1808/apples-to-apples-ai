import sys
import matplotlib.pyplot as plt


# Usage: python3 results_graphing.py filename (eg. 65/results.csv)
filename = sys.argv[1]
with open(filename) as file:
    agent_wins = {}

    file.readline()
    for line in file:
        data = line.strip().split(",")
        agent = data[1].split("-")[1].split(".")[0]
        if agent not in agent_wins:
            agent_wins.update({agent: 0})

        score = int(data[2])
        if score == 8:
            agent_wins[agent] += 1

agent_wins = dict(sorted(agent_wins.items(), key=lambda x:x[1], reverse=True))
agents = list(agent_wins.keys())
wins = list(agent_wins.values())
plt.bar(agents, wins, color="black")
plt.xlabel("Agent")
plt.ylabel("Wins")
plt.yticks([x for x in range(0, max(agent_wins.values()) + 5, 5)])
plt.title("Number of Wins for Each Agent Over 100 Games")
plt.show()
