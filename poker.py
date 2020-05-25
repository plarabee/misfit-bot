def rank_hand(hand):
    rank_counts = get_rank_dict(hand)

    if royal_flush(hand):
        return 'Royal Flush', False
    if straight_flush(hand):
        return 'Straight Flush', False
    if four_of_a_kind(rank_counts):
        return 'Four of a Kind', False
    if full_house(rank_counts):
        return 'Full House', False
    if flush(hand):
        return 'Flush', False
    if straight(hand):
        return 'Straight', False
    if three_of_a_kind(rank_counts):
        return 'Three of a Kind', False
    if two_pair(rank_counts):
        return 'Two Pair', False
    if pair(rank_counts):
        return 'Pair', False
    return high_card(hand), True


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

    for i in range(1, 13):
        for card in hand:
            if card.value == i:
                sorted_hand.append(card)
    
    return sorted_hand


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
    if queen_found == False:
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
    if ten_found == False:
        return False
    
    return True


def straight_flush(hand):
    sorted_hand = sort_hand(hand)
    winning_suit = sorted_hand[0].suit

    i = 0
    while i < len(sorted_hand) - 1:
        if sorted_hand[i].suit != winning_suit:
            return False

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
        if card.suit in suit_counts.keys():
            suit_counts[card.suit] += 1
        else:
            suit_counts[card.suit] = 1
    
    if 5 in suit_counts.values():
        return True

    return False


def straight(hand):
    sorted_hand = sort_hand(hand)

    i = 0
    while i < len(sorted_hand) - 1:
        if sorted_hand[i].value == sorted_hand[i + 1].value + 1 or  \
            (sorted_hand[i].rank == 'King' and sorted_hand[i + 1].rank == 'Ace'):
              i += 1
        else:
            return False
    return True


def three_of_a_kind(rank_counts):
    if 3 in rank_counts.values():
        return True
    return False


def two_pair(rank_counts):
    num_pairs = 0
    for key in rank_counts.keys():
        if rank_counts[key] == 2:
            num_pairs += 1
    
    if num_pairs == 2:
        return True
    return False


def pair(rank_counts):
    if 2 in rank_counts.values():
        return True
    return False


def high_card(hand):
    high_card = hand[0]

    for card in hand:
        if card.rank == 'Ace':
            return card.rank
        
        if card.value > high_card.value:
            high_card = card

    return high_card.rank