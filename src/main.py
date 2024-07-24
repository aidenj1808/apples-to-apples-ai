from game import ApplesToApples, Deck

#------------------------------------------------------------------------------------------------
# set up the game, create data for the green deck and the red deck 
# generate a list of adjectives and a list of nouns for game play from imported text files
def main():
    # create a list of players
    players = ["Tyler", "Darion", "Aiden", "Malcom", "AI"]

    # create instances of Decks (red/green)
    red_deck = Deck("all_red_cards.csv")
    green_deck = Deck("all_green_cards.csv")

    # create an instance of the game
    game = ApplesToApples(players, red_deck, green_deck)
    # start the game
    game.start_game()
#------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
