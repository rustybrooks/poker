#!/usr/bin/env python

from collections import defaultdict
import operator
import itertools
import random

deck_suits = ['c', 'd', 'h', 's']
deck_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


class Deck:
    def __init__(self, cards=None, shuffle=False):
        self.deck = cards or range(52)
        if shuffle:
            self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)


def int_to_card(i):
    return '{}{}'.format(deck_ranks[i % 13], deck_suits[i//13])


def card_to_int(c):
    return deck_suits.index(c[1])*13 + deck_ranks.index(c[0])


class HandScore:
    def __init__(self, hand, ):
        self.hand = hand

        self.suits = defaultdict(int)
        self.ranks = defaultdict(int)

        for c in hand:
            if isinstance(c, str):
                self.suits[deck_suits.index(c[1])] += 1
                self.ranks[deck_ranks.index(c[0])] += 1
            else:
                self.suits[c//13] += 1
                self.ranks[c % 13] += 1

        self.flush = max(self.suits.values()) >= 5
        self.sorted_rank_count = sorted(self.ranks.items(), key=operator.itemgetter(1, 0), reverse=True)
        self.straight_flush = False

        self.straight = None

        running = 0
        for rank in [len(deck_ranks)] + range(len(deck_ranks)):
            if rank not in self.ranks:
                running = 0

            running += 1
            if running >= 5:
                self.straight = rank

    def generate_hand_type(self):
        if self.flush and self.straight:
            self.straight_flush = True

        if self.straight_flush:
            return 8
        elif self.sorted_rank_count[0][1] == 4:
            return 7
        elif self.flush:
            return 6
        elif self.sorted_rank_count[0][1] == 3:
            if self.sorted_rank_count[1][1] >= 2:
                return 5
            else:
                return 4
        elif self.straight:
            return 3
        elif self.sorted_rank_count[0][1] == 2:
            if self.sorted_rank_count[1][1] == 2:
                return 2
            else:
                return 1
        else:
            return 0

    @classmethod
    def pretty_hand_type(self, ht):
        hand_types = [
            'high card', '1pr', '2pr', 'straight', 'trips', 'full house', 'flush', 'quads', 'straight flush'
        ]
        return hand_types[ht]

#    print suits
#    print ranks


for hand in [
    ['Ac', 'Ad', '2c', '2s', '3h'],
    ['2c', '3d', '4c', '5s', '6h', '6c', '6d'],
    ['2c', '3d', '4c', '5s', '6h', '6c', '9d'],
]:
    print hand, HandScore.pretty_hand_type(HandScore(hand).generate_hand_type())


deck = range(4, 13) + [x+13 for x in range(4, 13)] + [x+13*2 for x in range(4, 13)] + [x+13*3 for x in range(4, 13)]
print len([deck_ranks[x%13] for x in deck])


found = defaultdict(list)
for i, hand in enumerate(itertools.combinations(deck, 7)):
    hc = tuple(sorted(x % 13 for x in hand))

    found[hc].append(hand)

    if i % 100000 == 0:
        print i, len(found.keys())


print i, len(found.keys())

for x in range(10):
    foo = random.choice(found.keys())
    print "--------------------------------"
    print foo, len(found[foo])
    for t in found[foo]:
        print "...", sorted([int_to_card(x) for x in t])