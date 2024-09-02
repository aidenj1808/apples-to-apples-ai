import sys
import csv
from statistics import mean
import matplotlib.pyplot as plt


def main():
    args = sys.argv
    filename = args[1]

    with open(filename) as file:
        csv_reader = csv.reader(file)
        n_games = 0
        sum_of_rewards = []
        sum_of_rewards_averages = []
        for row in csv_reader:
            sum_of_rewards.append(float(row[1]))
            sum_of_rewards_averages.append(mean(sum_of_rewards))
            n_games += 1

    games = [x for x in range(1, n_games + 1)]
    plt.plot(games, sum_of_rewards_averages)
    plt.xlabel("Game")
    plt.ylabel("Average Sum of Rewards")
    plt.xticks([1] + [x for x in range(1, n_games + 1) if x % 10 == 0])
    plt.title("Average Sum of Rewards vs. Game")
    plt.show()


if __name__ == "__main__":
    main()
