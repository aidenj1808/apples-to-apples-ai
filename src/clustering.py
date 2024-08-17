import numpy as np
import csv
import toolz

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
        return self.clustering[card]

    def get_embedding(self, card : str) -> np.ndarray:
        return self.clustering[self.get_cluster(card)][card]

    def load(self, filename : str | None = None) -> None:

        if filename is None:
            filename = f"{self.n_clusters}_clusters.csv"

        with open(filename, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)

            for line in csvreader:
                # if len(line) == 2:
                #     self.clustering.update({line[0] : line[1]})
                    
                #else:
                self.clustering.update({line[0]: line[1]})

#Call script directly with interperter to generate new clustering file

#USAGE : python3 clustering.py red_card_file green_card_file num_clusters
if __name__ == "__main__":

    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import KMeans
    import sys

    red_card_file = sys.argv[1]
    green_card_file = sys.argv[2]
    num_clusters = int(sys.argv[3])

    red_cards = []
    green_cards = []
    with open("all_green_cards.csv", newline='') as file:
        file.readline()
        for line in file:
            data = line.strip().split(",", 2)
            if data[0] != "party_set":
                break
            green_cards.append(data[1])

    with open("all_red_cards.csv", newline='') as file:
        file.readline()
        for line in file:
            data = line.strip().split(",", 2)
            if data[0] != "party_set":
                break
            red_cards.append(data[1])

    # List of models https://sbert.net/docs/sentence_transformer/pretrained_models.html
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
    #RED CLUSTERS
    red_embeddings = model.encode(red_cards)

    red_embeddings = red_embeddings / np.linalg.norm(red_embeddings, axis=1, keepdims=True)


    
    kmeans = KMeans(n_clusters=num_clusters).fit(red_embeddings)
    
    temp = zip(red_cards, kmeans.labels_)

    with open(f"{num_clusters}_clusters.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # for i in range(num_clusters):
        #     csvwriter.writerow([f"CLUSTER{i}", kmeans.cluster_centers_[i]])
        for triple in temp:
            csvwriter.writerow(triple)
