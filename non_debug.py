# Use the below template to develop on the solution to play one play of the game and determine the loser.
# Keep your code as DRY(Do not Repeat Yourself) as possible.
# you are free to add classes, functions and variables as needed
# you are free to reorganize the code as needed.
# You can use any help necessary from the web even AI to solve this.
# Make your code as readable as possible.

ACE_VALUE = 14
family = ['S', 'H', 'C', 'D']
face_cards = ['J', 'Q', 'K', 'A']


def generate_deck() -> list:
    # donot hard code this function.
    # S2,S3, ... SA,H2,H3,...,HA,C2,C3,...,CA,D2,D3,...,DA in the same order
    return [(f, x) for f in family for x in range(2, ACE_VALUE+1)]


cards = generate_deck()
n_hands = 5
import random
random.seed(5)
random.shuffle(cards)
# make sure that generate deck generate the deck in the given order and use the above random seed for shuffling.


def distribute_cards(cards:list, n_hands:int):
    x = [[] for _ in range(n_hands)]
    p = 0
    for i in range(0, len(cards)):
        x[p].append(cards[i])
        p = (p + 1) % n_hands
    return x


hands = distribute_cards(cards, n_hands)


def find_starting_player_index():
    for i in range(0, len(hands)):
        if len(list(filter(lambda x: (x[0] == family[0] and x[1] == ACE_VALUE), hands[i]))) == 1:
            return i


def find_across_families(hand, least_numbered_card, family_order):
    for f in family_order:
        matching_cards = list(filter(lambda x: (x[0] == f and x[1] == least_numbered_card[1]), hand))
        if len(matching_cards) == 1:
            return matching_cards[0]


def find_smallest_card_in_family(hand, selected_family):
    return min(list(filter(lambda x: (x[0] == selected_family), hand)), key=lambda x: x[1], default=None)


def find_smallest_card(hand):
    return find_across_families(hand, min(hand, key=lambda x: x[1], default=None), family)


def find_highest_card(hand):
    return find_across_families(hand, max(hand, key=lambda x: x[1], default=None), family[::-1])


def remove(hand, card):
    hand.remove(card)
    return card


def play_hand(hand, cards_on_the_table)->bool: # use appropriate data types
    '''Play the card according to the rules by removing cards from hand and adding it to the cards on the table.
    Return a bool corresponding to whether the played card results in collecting the cards.
    Use that bool to play the next round.
    '''
    if len(hand) == 0:
        return True
    card = find_smallest_card_in_family(hand,cards_on_the_table[0][0])
    if card is None:
        cards_on_the_table.append(remove(hand, find_highest_card(hand)))
        return False
    else:
        cards_on_the_table.append(remove(hand, card))
        return True


def play_round(hands, starting_player:int)->int:
    '''modify hands according to the game play and return next player'''
    hand = hands[starting_player]
    if len(hand) == 0:
        return (starting_player + 1) % n_hands
    card = remove(hand, find_smallest_card(hands[starting_player]))
    cards_on_the_table = [card]
    highest_card_player = starting_player

    for i in range(0, n_hands-1):
        starting_player = (starting_player + 1) % n_hands
        if play_hand(hands[starting_player], cards_on_the_table) is False:
            hands[highest_card_player] = hands[highest_card_player] + cards_on_the_table
            return highest_card_player
        else:
            last_card_played = cards_on_the_table[len(cards_on_the_table)-1]
            if last_card_played[1] > card[1]:
                card = last_card_played
                highest_card_player = starting_player
    return highest_card_player


def n_remaining(hands):
    return sum(map(lambda x: len(x)>0, hands))


def play_game(hands):
    current_player = find_starting_player_index()
    while n_remaining(hands) > 1:
        current_player = play_round(hands, current_player)
    for i in range(0, n_hands):
        if len(hands[i]) > 0:
            return i, modify(hands[i])


# Just a utility function to replace 11 to 'J', 12 to 'Q' 13 to 'K' and 14 to 'A' during final printing.
def modify(hands):
    l = list()
    for card in hands:
        if card[1] > 10:
            l.append(str(card[0]) + face_cards[card[1]-11])
        else:
            l.append(str(card[0]) + str(card[1]))
    return l


loser, hand = play_game(hands)
print("loser ", loser, hand)
