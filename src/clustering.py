import numpy as np
import csv

class Clustering:
    """
    Class that represents a clustering of word vectors. Used to reduce the state
    space to better inform the agent during learning, reducing learning time
    
    ...

    Attributes
    -----------
    n_clusters : int
    The number of clusters used for the state space reduction

    clustering : dict
    Dict of dicts where the outer-most keys are the cluster numbers, and the
    inner keys are the red cards. The value of the inner-most keys are the word
    embeddings

    Methods
    -------
    get_cluster(card : str)
    return the cluster number for a card

    get_embedding(card : str)
    return the word-embedding for a card

    load(filename : str | None)
    load in the clusterings from a csv file. If None is supplied, the file
    "n_clusters_clusters.csv" is loaded where n_clusters is the attribute
    n_clusters


    """

    def __init__(self, n_clusters : int, filename : str | None = None) -> None:
        self.n_clusters = n_clusters
        self.clustering = {}
        self.load(filename)

    def get_cluster(self, card : str) -> int:
        return list(self.clustering.keys())[list(self.clustering.keys()).index(card)]

    def get_embedding(self, card : str) -> np.ndarray:
        return self.clustering[self.get_cluster(card)][card]

    def load(self, filename : str | None = None) -> None:

        if filename is None:
            filename = f"{self.n_clusters}_clusters.csv"

        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            clust_num = 0
            temp = {}

            for line in csvreader:
                if line == f"CLUSTER{clust_num}":
                    if clust_num != 0:
                        self.clustering.update(f"{clust_num - 1}", temp)
                    temp.update({"CLUSTER": np.array(line[1], dtype=float)})
                    clust_num += 1
                
                else:
                    temp.update({line[0]: np.array(line[1:], dtype=float)})

#Call script directly with interperter to generate new clustering file

#USAGE : python3 clustering.py red_card_file green_card_file num_clusters
if __name__ == "__main__":
    pass