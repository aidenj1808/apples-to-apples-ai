from matplotlib import pyplot as plt
import numpy as np
import csv

clusters = [10, 25, 50, 100]

for group in clusters:
    data = []

    with open(f"{group}/{group}_history.csv", 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(float(row[1]))

        
    plt.figure()
    plt.title(f"Sum of Rewards Per Game With Number of Clusters = {group}")
    plt.xticks(range(1, len(data)+1))
    plt.plot(range(1, len(data)+1),np.array(data))
    plt.xlabel("Game Number")
    plt.ylabel("Sum of Rewards")
    plt.show()
