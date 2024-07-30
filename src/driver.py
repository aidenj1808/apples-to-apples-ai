import sys
import subprocess
from game import Deck

class Driver():
    """
    A driver to simulate games of apples to apples against various AI agents.
    """
    def __init__(self, player_count: int, agents: list[str], n_games: int) -> None:
        """
        Initializes player count, agent programs, and number of games from
        creating an instance. Initializes an agents list from argv, a red deck,
        a green deck, the score to win the game, the current judge index, and
        the agent scores.
        """
        self.player_count = player_count
        self.agent_programs = agents
        self.n_games = n_games
        self.agents = [f"{i}-{agent}" for i, agent in enumerate(self.agent_programs)]
        self.red_deck = Deck("all_red_cards.csv")
        self.green_deck = Deck("all_green_cards.csv")
        self.winning_the_game = {4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 4, 10: 4}
        self.cards_to_win = self.winning_the_game[player_count]
        self.current_judge_index = 0
        self.agent_scores = {f"{i}-{agent}": 0 for i, agent in enumerate(self.agent_programs)}
        
    def initialize_cards(self) -> None:
        """
        Initializes each agents hands, shuffles the red card deck then deals
        seven red cards to each agent playing the game.
        """
        self.agent_hands = {f"{i}-{agent}": [] for i, agent in enumerate(self.agent_programs)}
        self.red_deck.shuffle()

        for _ in range(7):
            for _, hand in self.agent_hands.items():
                hand.append(self.red_deck.draw_card())

    def deal_round_cards(self) -> None:
        """
        Deals each agent a new red card if they weren't the judge in order to 
        have seven red cards in their hand.
        """
        for _, hand in self.agent_hands.items():
            if len(hand) == 7:
                continue
            hand.append(self.red_deck.draw_card())

    def reset_scores(self) -> None:
        """ Resets all agent's scores to 0. """
        self.agent_scores = {f"{i}-{agent}": 0 for i, agent in enumerate(self.agent_programs)}

    def initialize_game(self) -> None:
        """
        Initializes a new game of apples to apples by reseting the red and green
        decks and shuffling them, reseting the agent's scores, and initializing
        their cards
        """
        self.green_deck = Deck("all_green_cards.csv")
        self.green_deck.shuffle()

        self.red_deck = Deck("all_red_cards.csv")
        self.red_deck.shuffle()

        self.reset_scores()

        self.initialize_cards()

    def play_round(self) -> None:
        """
        A green card is drawn from the deck, then a subprocess is ran on each
        agent to capture their stdout of their decision on playing a red card
        based on the green card drawn. Given the cards played, the current agent
        judge picks a winning cards based on the green card drawn. The winning
        agent gains one score and the results of the round are printed. The
        current judge index gets assigned to the next agent in the list with 
        rotation.
        """
        green_card = self.green_deck.draw_card()
        agent_plays = []
        for i, agent in enumerate(self.agent_programs):
            if i == self.current_judge_index:
                continue
            hand = str(self.agent_hands[f"{i}-{agent}"])[1: -1].replace("'", "")
            agent_play = subprocess.run(["python3", agent, hand, green_card],
                                        capture_output=True)
            agent_plays.append([f"{i}-{agent}", agent_play.stdout.strip().decode()])

        cards_played = str([card for _, card in agent_plays])[1: -1].replace("'", "")
        winning_card = subprocess.run(["python3", self.agent_programs[self.current_judge_index], cards_played, green_card],
                                      capture_output=True)
        winning_card = winning_card.stdout.strip().decode()
        winning_agent = ""
        for agent, play in agent_plays:
            if play == winning_card:
                winning_agent = agent
                self.agent_scores[agent] += 1
                break

        results = f"Winning Agent: {winning_agent}\n"
        results += f"Winning Card: {winning_card}\n"
        results += f"Judge: {self.agents[self.current_judge_index]}\n"
        results += f"Green Card: {green_card}\n"
        results += f"Cards Played: {cards_played}\n"
        print(results)
        self.current_judge_index = (self.current_judge_index + 1) % self.player_count

    def print_scores(self, scores):
        print("Agent\t\t\tScore")
        for agent, score in scores.items():
            print(f"{agent}\t{score}")

    def main_loop(self) -> None:
        """
        The main simulation loop of the program. Loops for each n_games,
        initializes the game and while an agent isn't a winner it plays out a
        round and deals cards. If there is a winner, the winner is printed and
        the next game is played.
        """
        for k_game in range(1, self.n_games + 1):
            self.initialize_game()
            print(f"Game {k_game}\n")
            round = 1
            while not any([score == self.cards_to_win for _, score in self.agent_scores.items()]):
                print(f"Round: {round}")
                round += 1
                self.play_round()
                self.deal_round_cards()

            for agent, score in self.agent_scores.items():
                if score == self.cards_to_win:
                    self.print_scores(self.agent_scores)
                    print(f"{agent} won the game!\n\n")

                    break


def main():
    arguments = sys.argv

    driver = Driver(4, arguments[1:], 2)
    driver.main_loop()


if __name__ == "__main__":
    main()
