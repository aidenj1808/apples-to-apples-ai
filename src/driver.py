import sys
import subprocess
from traceback import format_exc
from game import Deck


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
                hand.append(self.red_deck.draw_card().lower())

    def deal_round_cards(self) -> None:
        """
        Deals each agent a new red card if they weren't the judge in order to 
        have seven red cards in their hand.
        """
        for _, hand in self.agent_hands.items():
            if len(hand) != 7:
                hand.append(self.red_deck.draw_card().lower())

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

    def get_closest_output(self, cards: list[str], output: str) -> str | int:
        cards_with_output = []
        for card in cards:
            if output in card:
                cards_with_output.append(card)

        if len(cards_with_output) > 0:
            return cards_with_output[0]
        return -1
        
    def get_agent_plays(self, green_card: str) -> list[str]:
        agent_plays = []
        for i, agent in enumerate(self.agent_programs):
            if i == self.current_judge_index:
                continue

            hand = self.agent_hands[f"{i}-{agent}"]
            hand_arg = str(",".join(hand))

            agent_play = subprocess.run(["python3", agent, hand_arg, green_card],
                                        capture_output=True, text=True)
            agent_play = agent_play.stdout.strip().lower()

            if agent_play not in hand:
                closest_output = self.get_closest_output(hand_arg.split(","), agent_play)
                while closest_output == -1:
                    agent_play = subprocess.run(["python3", agent, hand_arg, green_card],
                                                capture_output=True, text=True)
                    agent_play = agent_play.stdout.strip().lower()
                    closest_output = self.get_closest_output(hand_arg.split(","), agent_play)

                agent_plays.append([f"{i}-{agent}", closest_output])
                self.agent_hands[self.agents[i]].remove(closest_output)
            else:
                agent_plays.append([f"{i}-{agent}", agent_play])
                self.agent_hands[self.agents[i]].remove(agent_play)

            if agent == "RLAgent.py":
                subprocess.run(["python3", agent, agent_play, green_card, ], text=True)


        return agent_plays

    def get_winning_results(self, agent_plays: list[str], green_card: str) -> list[str | int]:
        cards_played = [card for _, card in agent_plays]
        cards_played_arg = str(",".join(cards_played))

        winning_card = subprocess.run(["python3",
                                       self.agent_programs[self.current_judge_index],
                                       cards_played_arg,
                                       green_card],
                                      capture_output=True, text=True)
        winning_card = winning_card.stdout.strip().lower()

        if winning_card not in cards_played:
            winning_card = self.get_closest_output(cards_played_arg.split(","), winning_card)
            while winning_card == -1:
                winning_card = subprocess.run(["python3",
                                               self.agent_programs[self.current_judge_index],
                                               cards_played_arg,
                                               green_card],
                                              capture_output=True, text=True)
                winning_card = winning_card.stdout.strip().lower()
                winning_card = self.get_closest_output(cards_played_arg.split(","), winning_card)

        winning_agent = ""
        for agent, play in agent_plays:
            if play == winning_card:
                winning_agent = agent
                self.agent_scores[agent] += 1
                break
        return [winning_agent, winning_card, cards_played_arg]

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
        agent_plays = self.get_agent_plays(green_card)
        winning_agent, winning_card, cards_played = self.get_winning_results(agent_plays, green_card)

        results = (f"Winning Agent: {winning_agent}\n"
                   f"Winning Card: {winning_card}\n"
                   f"Judge: {self.agents[self.current_judge_index]}\n"
                   f"Green Card: {green_card}\n"
                   f"Cards Played: {cards_played}\n")
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
                self.deal_round_cards()

            for agent, score in self.agent_scores.items():
                if score == self.cards_to_win:
                    self.print_scores(self.agent_scores)
                    final_results[agent] += 1
                    print(f"{agent} won the game!\n\n")
                    break
            
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
    except Exception as e:
        print("Error", e)
        print(format_exc())
        print("Usage: python3 driver.py [agents] [number of games]")


if __name__ == "__main__":
    main()
