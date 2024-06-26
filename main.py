# Use the below template to develop on the solution to play one play of the game and determine the loser.
# Keep your code as DRY(Do not Repeat Yourself) as possible.
# you are free to add classes, functions and variables as needed
# you are free to reorganize the code as needed.
# You can use any help necessary from the web even AI to solve this.
# Make your code as readable as possible.

debug = True
ACE_VALUE = 14
SPADE = 'S'
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


# print function
def myprint(hands):
    if debug:
        i = 0
        for hand in hands:
            if len(hand) != 0:
                print(i, "->", hand, len(hand))
            i = i + 1


# Just a utility function to replace 11 to 'J' during final printing.
def modify(hands):
    l = list()
    for card in hands:
        if card[1] >= 11:
            l.append(str(card[0]) + face_cards[card[1]-11])
        else:
            l.append(str(card[0]) + str(card[1]))
    return l


def find_starting_player_index():
    for i in range(0,len(hands)):
        for card in hands[i]:
            if card[0] == SPADE and card[1] == ACE_VALUE:
                return i


def find_smallest_card_in_family(hand,selected_family):
    return min(list(filter(lambda x: (x[0] == selected_family), hand)), key=lambda x: x[1], default=None)


def find_smallest_card(hand):
    return find_across_families(hand, min(hand, key=lambda x: x[1], default=None), family)


def find_highest_card(hand):
    return find_across_families(hand, max(hand, key=lambda x: x[1], default=None), family[::-1])


def find_across_families(hand, m, family):
    m_card = None
    for f in family:
        if m_card is not None:
            break
        for card in hand:
            if card[0] == f and m[1] == card[1]:
                m_card = card
                break
    return m_card


def remove(hand, card):
    hand.remove(card)


def play_hand(hand, cards_on_the_table)->bool: # use appropriate data types
    '''Play the card according to the rules by removing cards from hand and adding it to the cards on the table.
    Return a bool corresponding to whether the played card results in collecting the cards.
    Use that bool to play the next round.
    '''
    if len(hand) == 0:
        return True
    card = find_smallest_card_in_family(hand,cards_on_the_table[0][0])
    if card is None:
        card = find_highest_card(hand)
        hand.remove(card)
        cards_on_the_table.append(card)
        return False
    else:
        remove(hand,card)
        cards_on_the_table.append(card)
        return True


def play_round(hands,starting_player:int)->int:
    '''modify hands according to the game play and return next player'''
    hand = hands[starting_player]
    if len(hand) == 0:
        starting_player = starting_player + 1
        if starting_player == n_hands:
            starting_player = 0
        return starting_player
    card = find_smallest_card(hands[starting_player])
    if debug:
        print("Starting of Round:  Starting Player ", starting_player,  " Smallest Card",  card)
    remove(hand, card)

    cards_on_the_table = list()
    cards_on_the_table.append(card)
    ns = starting_player

    for i in range(0, n_hands-1):
        starting_player = starting_player + 1
        if starting_player == n_hands:
            starting_player = 0
        flag = play_hand(hands[starting_player], cards_on_the_table)
        if flag is False:
            if debug:
                print("Cards  ", cards_on_the_table, "added to player ", ns)
            hand = hands[ns]
            for c in cards_on_the_table:
                hand.append(c)
            return ns
        else:
            c = cards_on_the_table[len(cards_on_the_table)-1]
            if c[1] > card[1]:
                card = c
                ns = starting_player
    if debug:
        print("Cards on Table ", cards_on_the_table , " are removed from the game")
        print("Next Round Starting Player ", ns)
    return ns


def n_remaining(hands):
    return sum(map(lambda x: len(x)>0,hands))


def play_game(hands):
    current_player = find_starting_player_index()
    iter = 1
    while n_remaining(hands) > 1:
        if debug:
            print("*********************")
            print("iteration ",iter)
        iter = iter + 1
        myprint(hands)
        current_player = play_round(hands, current_player)

    for i in range(0,n_hands):
        if len(hands[i]) > 0:
            return i, modify(hands[i])


loser, hand = play_game(hands)
print("loser ", loser,hand)

