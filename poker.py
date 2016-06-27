import bisect
import copy
HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OK = 3
STRAIGHT = 4
FLUSH = 5
FULL_H = 6
FOUR_OK = 7
STRAIGHT_FL = 8
ROYAL_FL = 9

card_ranks = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "1": 1
}
LOW_ACE = 0
suits = {
    "C": 0,
    "S": 1,
    "D": 2,
    "H": 3
}


def poker(hands):
    """Takes players' hands and determines winning hand of a poker game
    :param hands: list of hands. Of which, hands are list of 2 char strings: e.g [["AS", "KS, "QS"..], ["8D", "9D", "10D"..]]
    :type hands:list[list[str]]
    :returns: winning hand
    :rtype: list[str]
    """
    return max(hands, key=hand_rank)



def hand_rank(hand):
    """ Returns hand rank as a tuple. When comparing hand ranks with max(), First value of tuple's are checked. Then second, etc. 
    E.g: (12,2,3) > (12,2,2)
    """

    # Scrub data into sorted list of tuples.
    hand_high_aces = scrub_hand(hand)

    # Duplicate aces to high and low
    # Reason: used for straight_"X" hands, where high/low aces matter
    hand_both_aces = low_aces(hand_high_aces)

    h_rank = None
    if h_rank is None:
        h_rank = straight_flush(hand_both_aces)
    if h_rank is None:
        h_rank = of_kind(hand_high_aces, 4)
    if h_rank is None:
        h_rank = full_house(hand_high_aces)
    if h_rank is None:
        h_rank = flush(hand_high_aces)
    if h_rank is None:
        h_rank = straight(hand_both_aces)
    if h_rank is None:
        h_rank = of_kind(hand_high_aces, 3)
    if h_rank is None:
        h_rank = two_pair(hand_high_aces)
    if h_rank is None:
        h_rank = of_kind(hand_high_aces, 2)
    if h_rank is None:
        h_rank = high_card(hand_high_aces)
    return h_rank


def scrub_hand(hand):
    """ Returns hand represented as a sorted (asc) list of tuples
    e.g: ["9S","TS","AH"] => [(9,1),(10,0),(14,3)]
    :param hand:
    :type hand: list[str]
    :return hand_scr: sorted (asc) list of tuples. Aces high and low.
    :rtype hand_scr: list[tuples]
    """

    hand_scr = sorted((card_ranks[x[0:-1]], suits[x[-1]]) for x in hand)
    return hand_scr


def low_aces(hand):
    """ Return hand with low and high aces included (if aces exist)
    e.g: [(9,1),(10,0),(14,3)] => [(0,3),(9,1),(10,0),(14,3)]
    :param hand:
    :type hand: list[tuples]
    
    """
    hand_low_aces = copy.deepcopy(hand)
    for i, j in reversed(hand):
        if i < card_ranks["A"]:
            break
        elif i > card_ranks["A"]:
            pass
        #Ace exists
        else:
            bisect.insort(hand_low_aces, (LOW_ACE, j))

    return hand_low_aces

def straight_flush(hand): 
    """
    :param hand: individual hand
    :type hand: sorted list[tuples]
    :returns hand_rank:
    :rtype: tuple
    """
    hand_rank = None
    # Add aces as high cards (low cards already inserted)
    # Strip off High Aces, so as not to double-count

    # Loops through hand. Tracks continous streaks, on a per-suit basis 
    # [Club=(first,last), Spade=(first,last)..]
    streak = [[None, None], [None, None], [None, None], [None, None]]

    # Hand - descending order
    for i, j in reversed(hand):
        # Non-continuous streak (or non-existent)
        if streak[j][0] is None or streak[j][1] > (i + 1):
            streak[j] = [i, i]
        # Continuous streak
        elif streak[j][1] == (i + 1):
            streak[j][1] = i
            # 5 cards
            if (streak[j][0] - streak[j][1]) == 4:
                hand_rank = (STRAIGHT_FL, streak[j][0])
                break

    # Convert to "well-known hands" convention
    if hand_rank is not None and hand_rank[1] == card_ranks["A"]:
        hand_rank = ROYAL_FL

    return hand_rank

def of_kind(hand, num):
    """
    :param hand: individual hand
    :type hand: sorted list[tuples]
    :returns hand_rank:
    :rtype: tuple
    """
    hand_rank = None

    kind_to_rank = {
        2:ONE_PAIR,
        3:THREE_OK,
        4:FOUR_OK
    }

    # Loops through hand. Tracks continous streaks, on a per-suit basis 
    # [Club=(first,last), Spade=(first,last)..]
    #[card_rank][number of occurences]
    streak = [None,None]

    # Hand - descending order
    for i, j in reversed(hand):
        # Non-continuous streak (or non-existent)
        if streak[0] is None or streak[0] != i:
            streak = [i, 1]
        # Continuous streak
        elif streak[0] == i:
            streak[1]+=1
            # 5 cards
            if streak[1] == num:
                hand_rank = (kind_to_rank[num], i)
                break

    return hand_rank

def full_house(hand):
    """
    :param hand: individual hand
    :type hand: sorted list[tuples]
    :returns hand_rank:
    :rtype: tuple
    """
    hand_rank = None

    # Loops through hand. Tracks continous streaks, on a per-suit basis 
    # [Club=(first,last), Spade=(first,last)..]
    #[card_rank][number of occurences]
    streak = [[None,None],[None,None]]

    # Hand - descending order
    for i, j in reversed(hand):
        # Non-continuous streak (or non-existent)
        if streak[0][0] is None:
            streak[0] = [i, 1]
        # Continuous streak
        elif streak[0][0] == i:
            streak[0][1]+=1
            if streak[1][0] is not None and ((streak[0][1] == 2 and streak[1][1] == 3) or (streak[0][1] == 3 and streak[1][1] == 2)):
                hand_rank = (FULL_H, streak[0][0])
                break
        elif streak[1][0] is None or streak[1][0] != i:
            if streak[1][0] is not None:
                streak[0] = streak[1]
            streak[1] = [i, 1]
        elif streak[1][0] == i:
            streak[1][1]+=1
            if (streak[0][1] == 2 and streak[1][1] == 3) or (streak[0][1] == 3 and streak[1][1] == 2):
                hand_rank = (FULL_H, streak[0][0])
                break
    return hand_rank

def flush(hand):
    """
    :param hand: individual hand
    :type hand: sorted list[tuples]
    :returns hand_rank:
    :rtype: tuple
    """
    hand_rank = None
    # Loops through hand. Tracks continous streaks, on a per-suit basis 
    # [Club=(highest, count), Spade=(highest,count)..]
    streak = [[None, None], [None, None], [None, None], [None, None]]

    # Hand - descending order
    for i, j in reversed(hand):
        if streak[j][0] is None:
            streak[j] = [i, 1]
        else:
            streak[j][1]+= 1
            # 5 cards
            if streak[j][1] == 5:
                hand_rank = (FLUSH, streak[j][0])
                break

    return hand_rank


def straight(hand):
    """
    :param hand: individual hand
    :type hand: sorted list[tuples]
    :returns hand_rank:
    :rtype: tuple
    """
    hand_rank = None
    # Add aces as high cards (low cards already inserted)
    # Strip off High Aces, so as not to double-count

    # Loops through hand. Tracks continous streaks, on a per-suit basis 
    # [Club=(first,last), Spade=(first,last)..]
    streak = [None, None]

    # Hand - descending order
    for i, j in reversed(hand):
        # Non-continuous streak (or non-existent)
        if streak[0] is None or streak[1] > (i + 1):
            streak = [i, i]
        # Continuous streak
        elif streak[1] == i:
            pass
        elif streak[1] == (i + 1):
            streak[1] = i
            # 5 cards
            if (streak[0] - streak[1]) == 4:
                hand_rank = (STRAIGHT, streak[0])
                break
            
    return hand_rank


def two_pair(hand):
    """
    :param hand: individual hand
    :type hand: sorted list[tuples]
    :returns hand_rank:
    :rtype: tuple
    """
    hand_rank = None

    # Loops through hand. Tracks continous streaks, on a per-suit basis 
    # [Club=(first,last), Spade=(first,last)..]
    #[card_rank][number of occurences]
    streak = [[None,None],[None,None]]

    # Hand - descending order
    for i, j in reversed(hand):
        # Non-continuous streak (or non-existent)
        if streak[0][0] is None:
            streak[0] = [i, 1]
        # Continuous streak
        elif streak[0][0] == i:
            streak[0][1]+=1
            if streak[1][0] is not None and streak[0][1] == 2 and streak[1][1] == 2:
                hand_rank = (FULL_H, streak[0][0])
                break
        elif streak[1][0] is None or streak[1][0] != i:
            streak[1] = [i, 1]
        elif streak[1][0] == i:
            streak[1][1]+=1
            if streak[0][1] == 2 and streak[1][1] == 2:
                hand_rank = (TWO_PAIR, streak[0][0])
                break
    return hand_rank

def high_card(hand):
    if hand is not None and len(hand) > 0:
        return (0, hand[0][0])


def test_poker():
    # Test cases for function poker()
    #sf = "6C 7C 8C 9C TC".split()
    #fk = "9D 9H 9S 9C 7D".split()
    #fh = "10D 10C 10H 7C 7D".split()
    #assert poker([sf,fk,fh]) == sf
    #assert poker([fk, fh]) == fk
    #assert poker([fh, fh]) == fh
    #return "tests pass"
    pass

def test_scrub_hand():
    t1 = "AH 9S TC"
    t2 = "TC AH 9S"
    t3 = "AD JC AC QH 2C JD AH 5S AS"

    print(scrub_hand(t1.split()))
    print(low_aces(scrub_hand(t1.split())))
    print(low_aces(scrub_hand(t3.split())))

def test_hand_rank():
    t1 = "AH KH QH JH TH 5H".split()
    t2 = "AH KS QS JS TS 9S".split()
    t3 = "AH 2H 3H 4H 5H KH".split()
    t2 = "KH QH JH TH 9H".split()
    t3 = "QH QS QD TH QC".split()
    t4 = "TH TS 2D 2H 2S KS".split()
    t5 = "AD JC AC QH 2C JD 5S".split()
    t6 = "JC AH AD AS KC KD KS KH".split()
    # assert(hand_rank(t1) == ROYAL_FL)
    # print(hand_rank(t1))
    #print(hand_rank(t3))
    #assert(hand_rank(t3) == (FOUR_OK, card_ranks["Q"]))
    print(hand_rank(t4))
    assert(hand_rank(t4) == (FULL_H, card_ranks["T"]))
    #assert(hand_rank(t4) == (FOUR_OK, card_ranks["K"]))
def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    s1 = "AS 2S 3S 4S 5C".split() # A-5 straight
    s2 = "2C 3C 4C 5S 6S".split() # 2-6 straight
    s3 = "TC JC QC KS AS".split() # 10-A straight
    tp = "5S 5D 9H 9C 6S".split() # two pair
    ah = "AS 2S 3S 4S 6C".split() # A high
    sh = "2S 3S 4S 6C 7D".split() # 7 high
    print(hand_rank(fh))
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    #assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert poker([s1, s2]) == [s2]
    assert poker([s1, tp]) == [s1]
test_hand_rank()
