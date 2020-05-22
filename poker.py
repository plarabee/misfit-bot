def rank_hand(hand):
    rank_counts = get_rank_dict(hand)

    if royal_flush(hand):
        return 'Royal Flush'
    if straight_flush(hand):
        return 'Straight Flush'
    if four_of_a_kind(rank_counts):
        return 'Four of a Kind'
    if full_house(rank_counts):
        return 'Full House'
    if flush(hand):
        return 'Flush'
    if straight(hand):
        return 'Straight'
    if three_of_a_kind(rank_counts):
        return 'Three of a Kind'
    if two_pair(rank_counts):
        return 'Two Pair'
    if pair(rank_counts):
        return 'Pair'
    return high_card(hand)


def get_rank_dict(hand):
    matches = {}

    for card in hand:
        if card.rank in matches:
            matches[card.rank] += 1
        else:
            matches[card.rank] = 1
    
    return matches


def sort_hand(hand):
    sorted_hand = []
    current_value = 1

    for card in hand:
        if card.value == current_value:
            sorted_hand.append(card)

        if current_value == 13:
            return sorted_hand
        else:
            current_value += 1


def royal_flush(hand):
    suit = ''

    ace_found = False
    for card in hand:
        if card.rank == 'Ace' and ace_found == False:
            ace_found = True
            suit = card.suit
    if ace_found == False:
        return False
    
    king_found = False
    for card in hand:
        if card.rank == 'King' and card.suit == suit:
            king_found = True
    if king_found == False:
        return False
    
    queen_found = False
    for card in hand:
        if card.rank == 'Queen' and card.suit == suit:
            queen_found = True
    if king_found == False:
        return False
    
    jack_found = False
    for card in hand: 
        if card.rank == 'Jack' and card.suit == suit:
            jack_found = True
    if jack_found == False:
        return False

    ten_found = False
    for card in hand:
        if card.rank == 'Ten' and card.suit == suit:
            ten_found = True
    if jack_found == False:
        return False
    
    return True


def straight_flush(hand):
    sorted_hand = sort_hand(hand)

    i = 0
    while i < len(sorted_hand) - 1:
        if sorted_hand[i].value == sorted_hand[i + 1].value + 1 or  \
            (sorted_hand[i].rank == 'King' and sorted_hand[i + 1].rank == 'Ace'):
              i += 1
        else:
            return False
    return True


def four_of_a_kind(rank_counts):
    for key in rank_counts:
        if rank_counts[key] >= 4:
            return True
    return False


def full_house(rank_counts):
    three_of_a_kind = False
    pair = False

    for key in rank_counts:
        if rank_counts[key] == 3:
            three_of_a_kind = True
        if rank_counts[key] == 2:
            pair = True
    
    if three_of_a_kind and pair:
        return True
    return False


def flush(hand):
    suit_counts = {}

    for card in hand:
        if card.suit in suit_counts.keys:
            suit_counts[card.suit] += 1
        else:
            suit_counts[card.suit] = 1
    
    if 5 in suit_counts.values:
        return True
    return False


""" TODO
def straight(hand):
"""


def three_of_a_kind(rank_counts):
    for key in rank_counts:
        if rank_counts[key] == 3:
            return True
    return False


def two_pair(rank_counts):
    num_pairs = 0
    for key in rank_counts:
        if rank_counts[key] == 2:
            num_pairs += 1
    
    if num_pairs == 2:
        return True
    return False


def pair(rank_counts):
    for key in rank_counts:
        if rank_counts[key] == 2:
            return True
        return False