import sys
import matplotlib.pyplot as plt


def main():
    filename = sys.argv[1]
    n_clusters = filename.split("/")[0]
    
    all_rewards = []
    with open(filename) as file:
        for line in file:
            all_rewards.append(float(line.split(",")[1]))

    games = [x for x in range(1, len(all_rewards) + 1)]

    plt.plot(games, all_rewards)
    plt.ylabel("Sum of Rewards")
    plt.xlabel("Game Number")
    plt.xticks([0] + [x for x in games if x % 5 == 0])
    plt.title(f"Sum of Rewards Per Game With Number of Clusters = {n_clusters}")
    plt.show()


if __name__ == "__main__":
    # USAGE: python3 agent_reward_graphing filename (eg. 10/10_history.csv)
    main()
