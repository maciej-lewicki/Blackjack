# TODO:
#  Improve count_points(): aces counting, count points only from part of cards (dealer's case) [Improvement]
#  Check blackjack on dealer's hand as a function [Improvement]
#  Unit tests after the first version to preserve usability (before extra features) [Project management]
#  Insurance, splitting, double [Extra features]
#  Tips for player, according to basic strategy [Super extra features]

# Total Time: 14.35h

import random


class Cards:
    """
    The class contains cards characteristics
    """
    suits = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10,
              'King': 10, 'Ace': 11}  # here Ace has 11 pts, it is checked later

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Cards.values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit

    def __le__(self, other):
        return Cards.values[str(self.rank)] <= Cards.values[str(other.rank)]


class Deck:
    """
    Prepares Deck and related actions
    """
    def __init__(self, number_of_decks=1):
        self.all_cards = []
        for i in range(number_of_decks):
            for suit in Cards.suits:
                for rank in Cards.ranks:
                    self.all_cards.append(Cards(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one_card(self):
        return self.all_cards.pop()


class Account:
    """
    The class to deal with wagers and the player's money/chips
    """
    def __init__(self, initial_amount, minimal_wager=5):
        self.amount = initial_amount
        self.minimal_wager = minimal_wager
        self.wager = 0

    def __str__(self):
        return f"At the moment you have {self.amount} on your account and {self.wager} on bet."

    def set_wager(self, wager):
        self.wager = wager

    def add_payoff(self, payoff):
        self.amount += payoff

    def above_minimal_wager(self):
        if self.amount < self.minimal_wager:
            print("You don't have enough money to play at this table - game over!")
            return False
        else:
            return True


class Hand:
    """
    The class to manage player's actions, covers also a dealer's hand
    """
    def __init__(self, card1, card2):
        self.players_hand = [card1, card2]
        self.players_hand_ranks = [card.rank for card in self.players_hand]
        self.players_hand_str = [str(card) for card in self.players_hand]
        self.points = self.count_points()

    def __str__(self):
        return f"{self.players_hand_str} on hand. They're summing up to {self.points} points"

    def hit(self, next_card):
        self.players_hand.append(next_card)
        self.players_hand_ranks.append(next_card.rank)
        self.players_hand_str.append(str(next_card))
        self.points = self.count_points()

    def stand(self):
        pass

    def count_points(self):
        # counting points remembering that Ace can take either 1 or 11
        # can be improved
        check_aces = [rank == 'Ace' for rank in self.players_hand_ranks]
        aces = [card for card, b in zip(self.players_hand_ranks, check_aces) if b]
        cards_without_aces = [card for card, b in zip(self.players_hand_ranks, check_aces) if not b]
        points = sum([Cards.values[rank] for rank in cards_without_aces])
        if len(aces) > 0:
            for ace in aces:
                if points > 10:
                    points += 1  # Ace's value is 1 point
                else:
                    points += 11
        return points

    def check_initial_blackjack(self):  # rewrite to check separately dealer's hand
        if self.points == 21:
            print("You have a blackjack!")
            return True, wager
        else:
            print("You don't get a blackjack at first strike - keep playing!")
            return False, wager


class Player:
    """
    container class for Hand and Account
    """

    def __init__(self, hand, account):
        self.hand = hand
        self.account = account

    def __str__(self):
        return f"Player has {self.hand}\n{self.account}"

    # the idea is that: in the main menu we will have only the function players_decision with parameters
    # this function will be pick up a parameter and get it through a whole proper-input chain
    # the proper-input framework will be the same for all decisions
    # but its core part will be steered from a function in a corresponding class
    # all underlying functions will return the same and we'll grab decision bool to decide what's next

    def players_decision(self, decision_parameter):
        # one container for all player's decisions
        improper_input = True
        decision = 0
        if decision_parameter == 'Next deal':
            function = self.next_game_decision
        elif decision_parameter == 'Wager':
            function = self.bet_wager_decision
        elif decision_parameter == "Next action":
            function = self.next_action_decision
        else:
            function = 0
        while improper_input:
            decision, improper_input = function()
        return decision

    def bet_wager_decision(self):
        # use set_wager method
        wager = int(input("What's your wager? "))
        if wager < self.account.minimal_wager:
            print(f"This bet is not available - it's below minimal wager {self.account.minimal_wager}. Bet more money!")
            improper_input = True
        else:
            if self.account.amount - wager < 0:
                print(f'This bet is not available - you do not have enough money! '
                      f'You can put maximum {self.account.amount}')
                improper_input = True
            else:
                print("Let's play!")
                improper_input = False
        return wager, improper_input

    def next_game_decision(self):
        player_choice = input('Would you like to play one more game? Pass Y or N. ')
        player_choice = player_choice[0].upper()  # only the first letter is taken
        if player_choice == 'Y':
            next_game = True
            improper_input = False
        elif player_choice == 'N':
            next_game = False
            improper_input = False
        else:
            print(f"You have to type either Yes or No. Try once again!")
            next_game = None
            improper_input = True
        return next_game, improper_input

    def next_action_decision(self):
        decision = input("What's your next move? S for Stand, H for Hit")
        decision = decision[0].upper()  # only the first letter is taken
        if decision == "S":
            players_action = "Stand"
            improper_input = False
        elif decision == "H":
            players_action = "Hit"
            improper_input = False
        else:
            print(f'Inappropriate input. Try once again!')
            players_action = "None"
            improper_input = True
        return players_action, improper_input

    def players_game(self, deck):
        game_continuing = True
        bust = False
        while game_continuing:
            next_action = self.players_decision("Next action")
            if next_action == "Stand":
                self.hand.stand()
                game_continuing = False
            elif next_action == "Hit":
                self.hand.hit(deck.deal_one_card())
                if self.hand.points > 21:
                    print(f"You bust! {self.hand}")
                    game_continuing = False
                    bust = True
                else:
                    print(self.hand)
                    game_continuing = True
                    if self.hand.points == 21 or (self.hand.points == 20 and 'Ace' not in self.hand.players_hand_ranks):
                        # Obviously, when player's got 21, (s)he wins. Otherwise, the game can be continued only if
                        # the next card will not cross the limit (the 2nd condition prevents against playing with
                        # 20 points on hand providing a player doesn't have an ace).
                        game_continuing = False
        return deck, bust


class Dealer:
    """
    container class for Hand and Account
    """

    def __init__(self, hand):
        self.hand = hand

    def __str__(self, number_of_showing_cards="all"):
        if number_of_showing_cards == 'all':
            return f"Dealer has {self.hand}"
        else:
            return f"Dealer has {self.hand.players_hand_str[:number_of_showing_cards]}"

    def dealers_game(self, deck):
        # A separate method to avoid ambiguity and manage 17-points limit decision
        game_continuing = True
        while game_continuing:
            if self.hand.points > 21:
                print("Dealer busts!")
                print(self)
                game_continuing = False
                return True
            else:
                if self.hand.points <= 17:  # soft 17
                    self.hand.hit(deck.deal_one_card())
                    game_continuing = True
                else:
                    self.hand.stand()
                    game_continuing = False
                    return False


# Game parameters
game_on = True
push = False
push_wager = 0
number_of_decks = 4

# Let's get ready to rumble! Game's on!

# define your amount (exchange money for casino chips) - save an amount
starting_sum = int(input("How much money you put at risk today? "))
players_stack = Account(starting_sum)

while game_on:

    # shuffling deck
    deck = Deck(number_of_decks)
    deck.shuffle()

    # dealing cards (one user, dealer, only two objects overall)
    # it's to add player's hand to appropriate class
    players_hand = Hand(deck.deal_one_card(), deck.deal_one_card())
    dealers_hand = Hand(deck.deal_one_card(), deck.deal_one_card())

    player = Player(players_hand, players_stack)
    dealer = Dealer(dealers_hand)

    # bet your wager, check if it's available
    wager = player.players_decision("Wager")
    player.account.set_wager(wager)

    # check if it's a standoff carried forward from previous deal
    if push:
        wager += push_wager

    # count points and show a gamer's hand
    print(player)

    # Initial blackjack and 3 results
    # Cast in a function
    blackjack, wager = player.hand.check_initial_blackjack()
    if blackjack:
        # resolve dealer's hand
        # if the same, we have a standoff
        if dealer.hand.points == 21:
            print("Push! Your money will stay on the table.")
            push = True
            push_wager = wager
        else:
            # otherwise, player wins
            print(dealer)
            print("You win!")
            # Conventionally, 3:2 payoff
            player.account.add_payoff(int(1.5*wager))
    else:
        # show a dealer's up-card
        print(dealer.__str__(1))  # print() and str() don't take additional arguments
        # it can be done without dunder methods, but I'd like to use them as a practice

        # Player's game. Player has to decide about next action after each step, it's not a one-stage process.
        # player's decision (hit and stand at the beg., later: insurance, double down, splitting even later)
        # count points =< 21 , if stand, turn to dealer
        deck, player_bust = player.players_game(deck)
        dealer_bust = dealer.dealers_game(deck)

        if player_bust:
            print("You loose!")
            player.account.add_payoff(-player.account.wager)
        else:
            if dealer_bust:
                print(f"You win!")
                player.account.add_payoff(wager)
            else:
                print(dealer)
                # Compare both hands and update account
                # it's important that player loses only this money which is put on bet in this deal
                # push_wager shouldn't be deduced from their account
                if player.hand.points > dealer.hand.points:
                    print(f"You win! You have {player.hand.points} on hand, "
                          f"whereas dealer has only {dealer.hand.points}.")
                    player.account.add_payoff(wager)
                    push = False  # Back to previous state
                elif player.hand.points < dealer.hand.points:
                    print(f"You lose! You have only {player.hand.points} on hand, "
                          f"whereas dealer has {dealer.hand.points}.")
                    player.account.add_payoff(-player.account.wager)
                    push = False  # Back to previous state
                else:
                    print("Push! Your money stay on the table.")
                    player.account.add_payoff(-player.account.wager)
                    push = True
                    push_wager = wager

    # Current account
    print(f"After this deal you're having {player.account.amount}.")
    if push:
        print(f"It's left {push_wager} on the table as a standoff.")
    else:
        print("There is no standoff on the table.")

    # ask player if they play again
    next_deal = player.players_decision("Next deal")

    if not next_deal:
        print(f"Thanks for your game! You're leaving the table with {player.account.amount}. Congrats!")
        game_on = False
