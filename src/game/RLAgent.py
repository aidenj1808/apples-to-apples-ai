JUDGE_STYLES = ["Default", "Contrarian", "Funny", "Edgy"]
MAX_CARDS = 7
TRAIN = False

import word_associations as wrd
import sys
import numpy as np
import spacy
import itertools
import time

'''
Class that represents the agent playing apples to apples. Should be able to 
draw cards, play red cards when a regular player, and judge red cards when a
judge. Requires a judge function in order to judge cards. By default, it picks
the red card most similar to the green card for that round.
'''

class State:

    def __init__(self, cards_hand):
        self.cards_hand = cards_hand   

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return (self.num_players, self.hand_size, self.cards_hand) == (other.num_players, other.hand_size, other.cards_hand)
    
    def __ne__(self, other):
        return not(self == other)
    
    def __str__(self):
        return f'{self.cards_hand}'

    def __repr__(self):
        return str(self)

class Policy:

    def __init__(self):
        #Store value of each action-state pair
        #dict of green cards with each dict value being a dict of the hand (state)
        #then value of playing each card in hand
        self.policy = {}
        

    #Assume hand is passed as sorted list
    def update(self, prev_green, next_green, red, prev_hand, new_hand, reward=0., step=1., discount=1.):

        next_state = State(new_hand)
        prev_state = State(prev_hand)
        value_hand = []

        for card in new_hand:
            value_hand.append(self.policy.setdefault(next_green, {}).setdefault(next_state, {}).setdefault(card, 0.))
        best = value_hand[np.argmax(value_hand)]
        

        Q = step*(reward + discount*best - self.policy[prev_green][prev_state][red])

        self.policy[prev_green][prev_state][red] += Q
        

    def get_value(self, green, red, hand):
        return self.policy[green][State(hand)][red]
    
    def get_best_card(self, green, hand):
        state = State(hand)
        value_hand = []
        for card in hand:
            value_hand.append(self.policy[green][state][card])
        
        return hand[np.argmax(value_hand)]
    
class Agent:
            

    def __init__(self, nlp, judge_style="Default"):
        self.hand = []
        self.points = 0
        self.nlp = nlp
        self.removed = {'R':[], 'G':[]}
        self.judges = [Judge(i, self.nlp) for i in JUDGE_STYLES]
        self.judge_style = Judge(judge_style, self.nlp)
        

    def init_policy(self, filename=None):
        if filename is None:
            self.value_func = Policy()
        else:
            pass

    #Add card to hand
    def add_card(self):

        while len(self.hand) < MAX_CARDS:

            card_name = input("Please enter a red card to add to my hand: ")
            self.hand.append(card_name)


    #Play best card given assessment of judges
    def play_card(self, green_card, judge_vals, judge_ind):
        
        judge_type = self.judges[np.argmax(judge_vals[judge_ind])]

        card = judge_type.evaluate(self.hand, green)

        self.hand.remove(card)

        return card
    
    #Remove cards played from pool of available cards
    def remove_from_pool(self, reds, green):

        for i in reds:

            self.removed['R'].append(i)

        self.removed['G'].append(green)

    #Find most likely judge for given card
    def find_max_judge(self, red, green):
        return np.argmax([judge.judge(red, green) for judge in self.judges])

    def train(self, train_time, reds, greens, num_points, num_players):

        start_time = time.time()
        rng = np.random.default_rng()

        self.wins = 0
        self.game_wins = 0
        self.games_played = 0

        while time.time() - start_time < train_time:

            while len(self.hand) < MAX_CARDS:
                candidate = None
                while candidate is None or candidate in self.hand:
                    candidate = reds[int(rng.uniform(0,len(reds)))]
                self.hand.append(candidate)

            #All player points and player judge assumptions
            player_pts = [0 for i in range(num_players)]
            #player_judge = [[0 for j in range(len(JUDGE_STYLES))] for i in range(int(sys.argv[1]) - 1)]
            #j_ind = 0

            self.hand.sort()
            roundNum = 0
            next_green = greens[int(rng.uniform(0,len(greens)))]
            while num_points not in player_pts:
                green_card = next_green

                round_hand = [reds[int(rng.uniform(0,len(reds)))] for i in range(num_players - 1)]
                agent_best = self.value_func.get_best_card(green_card, self.hand)
                round_hand.append(agent_best)

                round_hand_nlp = []

                for card in round_hand:
                    round_hand_nlp.append(self.nlp(card).similarity(self.nlp(green_card)))

                winner = np.argmax(round_hand_nlp)
                best = round_hand[np.argmax(round_hand_nlp)]

                player_pts[winner] += 1

                if best == self.value_func.get_best_card(green_card, self.hand):
                    self.wins+=1

                reward = 1. if agent_best == best else 0.                

                prev_hand = self.hand.copy()
                self.hand.remove(agent_best)
                candidate = self.hand[0]
                while candidate in self.hand:
                    candidate = reds[int(rng.uniform(0,len(reds)))]
                self.hand.append(candidate)

                self.hand.sort()
                next_green = greens[int(rng.uniform(0,len(greens)))]

                self.value_func.update(green_card, next_green, best, prev_hand, self.hand, reward=reward)
                roundNum += 1

                print(f'Round {roundNum} of game {self.games_played}')




            print(f"\nGAMEOVER - Player {player_pts.index(WINPOINT) + 1} wins!\n")
            self.hand = []
            self.games_played+=1
            if player_pts.index(WINPOINT) == 0:
                self.game_wins += 1
            


#Contains judging styles
class Judge:

    def __init__(self, name, nlp):
        self.name = name
        self.nlp = nlp

        match name:
            case "Default":
                self.judge = self.default

            case "Contrarian":
                self.judge = self.contrarian

            case "Funny":
                self.judge = self.funny

            case "Edgy":
                self.judge = self.edgy

    def default(self, red, green):
        return self.nlp(green).similarity(self.nlp(red))
    
    def contrarian(self, red, green):
        return -self.nlp(green).similarity(self.nlp(red))
    
    def funny(self, red, green):
        return self.nlp("Funny").similarity(self.nlp(f'{green} {red}'))
    
    def edgy(self, red, green):
        return self.nlp("Satire").similarity(self.nlp(f'{green} {red}'))
    
    def evaluate(self, reds, green):
        return reds[np.argmax([self.judge(i, green) for i in reds])]
    


if __name__ == '__main__':

    if len(sys.argv) < 5:
        print("USAGE: ./agent #Players #Points GreenExt RedExt [TrainingTime]")
        exit()

    #load NLP
    nlp = spacy.load("NLP")
    agent = Agent(nlp)

    agent.init_policy()
    #print(agent.value_func.policy['Loud']["Hitler"])

    # if TRAIN:
    #     print("Training Starting...")
    #     agent.train(float(sys.argv[5]), reds, greens, WINPOINT, NUM_PLAYERS)
    #     print(agent.games_played, agent.wins, agent.game_wins)

    

    agent.add_card()

    #All player points and player judge assumptions
    player_pts = [0 for i in range(int(sys.argv[1]))]
    player_judge = [[0 for j in range(len(JUDGE_STYLES))] for i in range(int(sys.argv[1]) - 1)]
    j_ind = 0

   

    roundNum = 0
    while WINPOINT not in player_pts:
        roundNum += 1
        print(f"\n###ROUND {roundNum}###\n")

        role = input("What role am I playing this round? 0 - Player; else - Judge: \n")

        if not int(role):

            green = input("Green card: ")

            red = agent.play_card(green, player_judge, j_ind)
            print(f"I play {red}")

            winner = input(f"Which player won (assume I am player 1/{int(sys.argv[1])})? ")

            roundCards = []
            for i in range(1,NUM_PLAYERS-1):
                roundCards.append(input(f"\nWhich card was played by another player? "))


            player_pts[int(winner) - 1] += 1
            player_judge[j_ind][agent.find_max_judge(roundCards[int(winner) - 2], green)] += 1
            j_ind += 1
            if j_ind == NUM_PLAYERS-1:
                j_ind = 0

            agent.add_card()

        else:
            green = input("Green card: ")
            roundCards = []

            for i in range(1,NUM_PLAYERS):
                roundCards.append(input(f"Enter player red card: "))

            print(f"Picked: {roundCards[0]}")
            winner = input(f"\nWhich player won (assume I am player 1/{int(sys.argv[1])})? ")
            player_pts[int(winner) - 1] += 1


    print(f"\nGAMEOVER - Player {player_pts.index(WINPOINT) + 1} wins!\n")
