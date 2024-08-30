import sys
import matplotlib.pyplot as plt


def main():
    filename = sys.argv[1]
    n_clusters = filename.split("/")[0]

    all_rewards = []
    with open(filename) as file:
        for line in file:
            all_rewards.append(float(line.strip().split(",")[1]))
    games = [x for x in range(1, len(all_rewards) + 1)]
    
    try:
        if sys.argv[2] == "trend":
            total_sum_rewards = []
            with open(filename) as file:
                for line in file:
                    data = float(line.strip().split(",")[1])
                    if total_sum_rewards:
                        total_sum_rewards.append(data + total_sum_rewards[-1])
                    else:
                        total_sum_rewards.append(data)

            plt.plot(games, total_sum_rewards)
            plt.ylabel("Total Sum of Rewards")
            plt.xlabel("Game Number")
            plt.xticks([0] + [x for x in games if x % 5 == 0])
            plt.title(f"Sum of Rewards Total Trend Per Game With Number of Clusters = {n_clusters}")
            plt.show()

        else:
            plt.plot(games, all_rewards)
            plt.ylabel("Sum of Rewards")
            plt.xlabel("Game Number")
            plt.xticks([0] + [x for x in games if x % 5 == 0])
            plt.title(f"Sum of Rewards Per Game With Number of Clusters = {n_clusters}")
            print(f"Total sum of rewards: {sum(all_rewards)}")
            plt.show()

    except Exception as e:
        print("Usage: python3 agent_reward_graphing.py filename trend - error:", e)


if __name__ == "__main__":
    # USAGE: python3 agent_reward_graphing filename (eg. 10/10_history.csv)
    # or
    # USAGE: python3 agent_reward_graphing filename (eg. 10/10_history.csv) trend
    main()
