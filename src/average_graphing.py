import matplotlib.pyplot as plt
from numpy import average


n_clusters = [40, 45, 50, 55, 60]

def main():
    average_sum_of_rewards = []
    for clusters in n_clusters:
        with open(f"{clusters}/{clusters}_history.csv") as file:
            sum_of_rewards = []
            lines = 0
            while lines != 20:
                line = file.readline()
                data = float(line.strip().split(",")[1])
                sum_of_rewards.append(data)
                lines += 1

        average_sum_of_rewards.append(average(sum_of_rewards))
    
    plt.plot(n_clusters, average_sum_of_rewards)
    plt.ylabel("Average Sum of Rewards")
    plt.xlabel("Number of Clusters")
    plt.title(f"Average Sum of Rewards vs. Number of Clusters Over 20 Games")
    plt.show()


if __name__ == "__main__":
    main()
