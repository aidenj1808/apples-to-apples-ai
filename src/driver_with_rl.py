import sys
import subprocess
import spacy
from traceback import format_exc
from game import Deck
from game.RLAgent import Agent, State, Policy

WIN_REWARD = 1.0
LOSE_REWARD = -0.5


class Driver():
    """
    A driver to simulate games of apples to apples against various AI agents.
    """
    def __init__(self, agents: list[str], n_games: int) -> None:
        """
        Initializes agent programs, and number of games from
        creating an instance. Initializes player count from the length of argv
        agents, an agents list from argv, a red deck, a green deck, the score to
        win the game, the current judge index, and the agent scores.
        """
        self.agent_programs = agents
        self.n_games = n_games
        self.player_count = len(agents)
        self.agents = [f"{i}-{agent}" for i, agent in enumerate(self.agent_programs)]
        self.red_deck = Deck("all_red_cards.csv")
        self.green_deck = Deck("all_green_cards.csv")
        self.winning_the_game = {4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 4, 10: 4}
        self.cards_to_win = self.winning_the_game[self.player_count]
        self.current_judge_index = 0
        self.current_judge = self.agents[self.current_judge_index]
        self.agent_scores = {f"{i}-{agent}": 0 for i, agent in enumerate(self.agent_programs)}

        self.rl_agent = Agent()
        self.rl_agent.init_policy()
        self.rl_agent_name = [agent for agent in self.agents if "RLAgent.py" in agent][0]
        
    def initialize_cards(self) -> None:
        """
        Initializes each agents hands, shuffles the red card deck then deals
        seven red cards to each agent playing the game.
        """
        self.agent_hands = {f"{i}-{agent}": [] for i, agent in enumerate(self.agent_programs)}
        self.red_deck.shuffle()

        for _ in range(7):
            # RL
            if len(self.rl_agent.hand) < 7:
                self.rl_agent.add_card(self.red_deck.draw_card().lower())
            for agent, hand in self.agent_hands.items():
                if agent != self.rl_agent_name:
                    hand.append(self.red_deck.draw_card().lower())

    def deal_round_cards(self) -> None:
        """
        Deals each agent a new red card if they weren't the judge in order to 
        have seven red cards in their hand.
        """
        for _, hand in self.agent_hands.items():
            if len(hand) != 7:
                hand.append(self.red_deck.draw_card().lower())

        # RL
        if len(self.rl_agent.hand) < 7:

            self.rl_agent.add_card(self.red_deck.draw_card().lower())

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


    def format_hand(self, hand: list[str]) -> str:
        hand = [card.replace(" ", "_") for card in hand]
        return ",".join(hand)

    def get_agent_play(self, agent: str, hand: list[str], green_card: str):
        print(f"{agent} is making a decision...")
        agent_program = agent.split("-")[1]
        formatted_hand = self.format_hand(hand)
        info = formatted_hand + " " + green_card

        proc = subprocess.Popen(["python3", agent_program],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

        stdout, _ = proc.communicate(info)
        play = stdout.strip().lower()
        while play not in hand:
            proc = subprocess.Popen(["python3", agent_program],
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
            stdout, _ = proc.communicate(info)
            play = stdout.strip().lower()
        self.agent_hands[agent].remove(play)
        return agent, play

    def get_agent_plays(self, green_card: str):
        agent_plays = []
        for agent, hand in self.agent_hands.items():
            if agent != self.current_judge and agent != self.rl_agent_name:
                agent_plays.append(self.get_agent_play(agent, hand, green_card))

        # RL
        if self.current_judge != self.rl_agent_name:
            print(f"{self.rl_agent_name} is making a decision...")
            agent_plays.append((self.rl_agent_name, self.rl_agent.play_card(green_card)))
        return agent_plays

    def rl_judge(self, agent_plays: tuple[str, str], green_card: str):
        cards_played = [card for _, card in agent_plays]
        winning_card = self.rl_agent.value_func.get_best_card(green_card, cards_played)
        winning_agent = ""
        for agent, card in agent_plays:
            if card == winning_card:
                winning_agent = agent
        return [winning_agent, winning_card, cards_played]

    def get_winning_results(self, agent_plays, green_card: str):
        print(f"{self.current_judge} is judging...")
        cards_played = [card for _, card in agent_plays]

        if self.current_judge == self.rl_agent_name:
            winning_agent, winning_card, cards_played = self.rl_judge(agent_plays, green_card)
            self.agent_scores[winning_agent] += 1
            return winning_agent, winning_card, cards_played

        formatted_cards_played = self.format_hand(cards_played)
        info = formatted_cards_played + " " + green_card

        proc = subprocess.Popen(["python3", self.agent_programs[self.current_judge_index]],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        winning_card, _ = proc.communicate(info)
        winning_card = winning_card.rstrip().lower()
        while winning_card not in cards_played:
            proc = subprocess.Popen(["python3", self.agent_programs[self.current_judge_index]],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            winning_card, _ = proc.communicate(info)
            winning_card = winning_card.rstrip().lower()

        winning_agent = ""
        for agent, play in agent_plays:
            if play == winning_card:
                winning_agent = agent
                self.agent_scores[agent] += 1
                break
        return [winning_agent, winning_card, cards_played]

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
        rl_prev_hand = self.rl_agent.hand.copy()

        green_card = self.green_deck.draw_card().lower()
        agent_plays = self.get_agent_plays(green_card)
        winning_agent, winning_card, cards_played = self.get_winning_results(agent_plays, green_card)

        results = (f"Winning Agent: {winning_agent}\n"
                   f"Winning Card: {winning_card}\n"
                   f"Judge: {self.agents[self.current_judge_index]}\n"
                   f"Green Card: {green_card}\n"
                   f"Cards Played: {cards_played}\n")
        print(results)

        next_green_card = self.green_deck.cards[-1]
        rl_agent_play = agent_plays[-1][1]
        reward = WIN_REWARD if winning_agent == self.rl_agent_name else LOSE_REWARD
        self.deal_round_cards()
        if self.current_judge != self.rl_agent_name:
            self.rl_agent.value_func.update(green_card, next_green_card, rl_agent_play, rl_prev_hand, self.rl_agent.hand, reward)

        self.current_judge_index = (self.current_judge_index + 1) % self.player_count
        self.current_judge = self.agents[self.current_judge_index]


    def print_scores(self, scores):
        print("Agent\t\t\tScore")
        for agent, score in scores.items():
            print(f"{agent}\t{score}")

    def main_loop(self) -> None:
        """
        The main simulation loop of the program. Loops for each n_games,
        initializes the game and while an agent isn't a winner it plays out a
        round and deals cards. If there is a winner, the winner is printed and
        the next game is played. After all games are played the final results
        are printed.
        """
        final_results = {agent: 0 for agent in self.agents}
        for k_game in range(1, self.n_games + 1):
            self.initialize_game()
            print(f"Game {k_game}\n")
            round = 1
            while not any([score == self.cards_to_win for _, score in self.agent_scores.items()]):
                print(f"Round: {round}")
                round += 1
                self.play_round()

            for agent, score in self.agent_scores.items():
                if score == self.cards_to_win:
                    self.print_scores(self.agent_scores)
                    final_results[agent] += 1
                    print(f"{agent} won the game!\n\n")
                    break
            self.rl_agent.hand = []
            
        final_results = list(sorted(final_results.items(), key=lambda x:x[1], reverse=True))
        print(f"Final Results for {self.n_games} Games:\n")
        print("Agent\t\t\tGames Won\tW/L%")
        for agent, games_won in final_results:
            print(f"{agent}\t{games_won}\t\t{games_won / self.n_games * 100:.2f}")


def main():
    try:
        arguments = sys.argv
        n_games = int(arguments[-1])
        driver = Driver(arguments[1: -1], n_games)
        driver.main_loop()
        driver.rl_agent.value_func.save()
    except Exception as e:
        print("Error", e)
        print(format_exc())
        print("Usage: python3 driver.py [agents] [number of games]")


if __name__ == "__main__":
    main()
