#imports
import numpy as np
import csv
import ast
import random
import clustering as clust


class State:
    """
    Class that represents a game state based on the cards in a hand supplied.

    ...

    Attributes
    ----------
    cards_hand : list of str
        a sorted copy of the hand supplied during initialization

    """

    def __init__(self, cards_hand):
        hand = cards_hand.copy()
        hand.sort()
        self.cards_hand = hand

    #Below methods are required for dictionary use

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return self.cards_hand == other.cards_hand
    
    def __ne__(self, other):
        return not(self == other)
    
    def __str__(self):
        return f'{self.cards_hand}'

    def __repr__(self):
        return str(self)

class Policy:
    """
    Class that represents a policy or state-action pair value function. Keeps
    track of an agent's understanding of the value of state-action value pairs.
    Includes methods that find the best action to take from a given state, update
    values, and save/load from a csv file

    ...

    Attributes
    ----------
    policy : dict
        a dictionary of dictionaries of dictionaries. From outside to inside,
        policy keeps track of green cards, states, and then the value of playing
        a red card from that state.

    Methods
    -------
    update(prev_green, next_green, red, prev_hand, new_hand, reward, step, discount):
        use Q-learning to update the policy. Uses the green card from the previous
        round, the green card from the next round, the red card the agent just
        played, the agent's hand from the previous round, the agent's hand from
        the next round, and then values for the reward, step-size, and discount.

    get_value(green, red, hand):
        return the value of playing a red card given the hand its played from and
        the green card it will be played with.

    get_best_card(green, hand):
        return the highest value red card to play given a hand and the green card
        currently in play.

    load():
        attempt to load a policy from a file called "policy.csv"

    save():
        save the currently learned policy to a file called "policy.csv"

    """

    def __init__(self, clusters=10):
        #Store value of each action-state pair
        #dict of green cards with each dict value being a dict of the hand (state)
        #then value of playing each card in hand
        self.policy = {}

        if clusters != 0:
            self.cluster_map = clust.Clustering()
            self.cluster = True
        else:
            self.cluster = False

        
        

    #Assume hand is passed as sorted list
    def update(self, prev_green, next_green, red, prev_hand, new_hand, reward=0., step=0.5, discount=0.9):

        if self.cluster:
            next_state = State([self.cluster_map.get_cluster(card) for card in new_hand])
            prev_state = State([self.cluster_map.get_cluster(card) for card in prev_hand])
            # red = self.cluster_map.get_cluster(red)
            prev_green = self.cluster_map.get_cluster(prev_green.lower())
            next_green = self.cluster_map.get_cluster(next_green.lower())

        else:

            next_state = State(new_hand)
            prev_state = State(prev_hand)


            prev_green = prev_green.lower()
            next_green = next_green.lower() 

        best_card = self.get_best_card(next_green, new_hand)
        best_value = self.get_value(next_green, best_card, new_hand)
        
        td = step * (reward + discount * best_value)
        Q = (1-step) * self.get_value(prev_green, red, prev_hand)

        red_ind = prev_hand.index(red)
        self.policy[prev_green][prev_state][red_ind] = Q + td

        # print(prev_green, next_green, prev_hand, new_hand, red)
        

    def get_value(self, green, red, hand):
        if self.cluster:
            state = State([self.cluster_map.get_cluster(card) for card in hand])
            red = self.cluster_map.get_cluster(red)

        else:
            state = State(hand)
        
        red_ind = state.cards_hand.index(red)
        copy_indices = np.nonzero(np.array(state.cards_hand) == state.cards_hand[red_ind])[0]
        ind = random.randint(0,len(copy_indices)-1)
        chosen_ind = copy_indices[ind]

        return self.policy.setdefault(green, {}).setdefault(state, [0. for i in state.cards_hand])[chosen_ind]
    
    def get_best_card(self, green, hand):
        if self.cluster:
            state = State([self.cluster_map.get_cluster(card) for card in hand])
        else:
            state = State(hand)
        value_hand = self.policy.setdefault(green, {}).setdefault(state, [0. for i in state.cards_hand])

        #if more than one state-action pair has the same value, choose randomly
        #to encourage exploration and fairer judging

        #find the index of the max value state-action pair
        #then choose randomly from all the state-action pairs that share the
        #same value
        max_value = np.argmax(value_hand)
        
        max_value_indices = np.nonzero(np.array(value_hand) == value_hand[max_value])[0]
        ind = random.randint(0,len(max_value_indices)-1)
        chosen_ind = max_value_indices[ind]

        return hand[chosen_ind]


    def load(self):

        try:
            with open('policy.csv', 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)

                green = ''
                state = None
                red = []

                for row in csvreader:
                    if len(row) == 1:
                        green = row[0]

                    else:
                        state = State(ast.literal_eval(row[0]))
                        red = row[1:]
                        temp = []
                        for string in red:
                            temp.append(float(string.split('=')[1]))
                        self.policy.setdefault(green, {}).update({state: temp})
                        

        except Exception as e:
            print("Could not load policy file",e)
            raise e
        

    def save(self):

        with open('policy.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for green in self.policy:
                csvwriter.writerow([green])
                
                for state in self.policy[green]:
                    export_string = [str(state.cards_hand)]
        
                    for i in range(len(state.cards_hand)):
                        export_string.append(f'{state.cards_hand[i]}={self.policy[green][state][i]}')
                    
                    csvwriter.writerow(export_string)


class Agent:
    """
    Class that represents a player in a game of Apples to Apples. This agent
    uses reinforcement learning to learn from playing what cards are best to
    play based on the cards in its hand compared to the green card currently
    in play. Should facilitate all the actions a player can take. Uses Q-learning.

    ...

    Attributes
    ----------
    hand : list
        list of strings representing the agent's hand
    points : int
        how many points it currently has in the round
    value_func :
        keeps track of an agent's percieved value of state-action pairs

        
    Methods
    -------
    init_policy(filename):
        initialize agent policy. By default it attempts to load in a csv file
        called "policy.csv". If this fails, a new policy is initialized

    add_card(red_card):
        Add a new red card to the agent's hand

    play_card(green_card):
        play a red card from the agent's hand based on the green card supplied
        and its understanding of its value

    """    
            

    def __init__(self):
        self.hand = []
        self.points = 0

        self.history = []
        

    def init_policy(self, filename="policy.csv"):

        self.value_func = Policy()


        try:
            self.value_func.load()

        except Exception as e:
            print("Existing policy could not be found\nA new one will be initialized\n")

    #Add card to hand
    def add_card(self, red_card: str):
        self.hand.append(red_card)


    #Play best card given assessment of judges
    def play_card(self, green_card):
        agent_best = self.value_func.get_best_card(green_card, self.hand)
        self.hand.remove(agent_best)
        return agent_best
    
    def export_history(self, filename=None):
        if filename is None:
            filename = f"{self.value_func.cluster_map.num_clust}_history.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            for i in range(len(self.history)):
                csvwriter.writerow([f"Game{i+1}", np.average(self.history[i])])