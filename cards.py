from __future__ import annotations
from dataclasses import dataclass, field
from functools import total_ordering
from abc import ABC, abstractmethod
from random import shuffle as rand_shuffle, seed as rand_seed


@total_ordering
@dataclass()
class PlayingCard():
    rank: str
    suit: str
    
    _inputrank_to_rank = {
        "1": 'a',
        "2": '2',
        "3": '3',
        "4": '4',
        "5": '5',
        "6": '6',
        "7": '7',
        "8": '8',
        "9": '9',
        "10": '10',
        "11": 'j',
        "12": 'q',
        "13": 'k',
        "14": 'a',
        "j": "j",
        "q": "q",
        "k": "k",
        "a": "a",
    }
    _suits = ["c", "d", "h", "s"]
    _ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", 'j', 'q', 'k', 'a']
    
    def __init__(self, rank: str | int, suit: str) -> None:
        self.rank = str(rank)
        self.suit = suit
        self.__post_init__()
    
    def __post_init__(self) -> None:
        # Check suit
        if (not isinstance(self.suit, str)): raise TypeError(f"Suit must be type str but got {type(self.suit).__name__} instead")
        if (self.suit.lower() not in ["d", "h", "s", "c"]): raise ValueError(f"'{self.suit}' not in allowed suits [D, H, S, C]")
        
        # Check rank
        if (not (isinstance(self.rank, str) or isinstance(self.rank, int))): raise TypeError(f"Rank must be type str or int but got {type(self.rank).__name__} instead")
        if (str(self.rank) not in self._inputrank_to_rank): raise ValueError(f"Expected rank in {self._inputrank_to_rank.keys()}, but got {self.rank} instead")
        
        self.rank = self._inputrank_to_rank[str(self.rank)]
        
    def __str__(self) -> str: 
        return f"{self.rank.upper()}{self.suit.upper()}"
    
    def __eq__(self, other) -> bool:
        if (not isinstance(other, PlayingCard)): return NotImplemented
        return (self.rank == other.rank) and (self.suit == other.suit)
    
    def __lt__(self, other) -> bool:
        if (not isinstance(other, PlayingCard)): return NotImplemented
        self_rank_index = PlayingCard._ranks.index(self.rank)
        other_rank_index = PlayingCard._ranks.index(other.rank)
        
        # Check rank
        if (self_rank_index != other_rank_index):
            return self_rank_index < other_rank_index
        
        # Same rank, now by suit
        self_suit_index = PlayingCard._suits.index(self.suit)
        other_suit_index = PlayingCard._suits.index(other.suit)
        return self_suit_index < other_suit_index

    def __repr__(self) -> str:
        return self.__str__()
    
@dataclass
class Deck:
    cards: list = field(default_factory = list[PlayingCard])
    
    def generate_playingcard_deck(self) -> None:
        for suit in PlayingCard._suits:
            for rank in PlayingCard._ranks:
                self.cards.append(PlayingCard(rank, suit))
                
    def shuffle(self, seed: int | None = None) -> None:
        rand_seed(seed)
        rand_shuffle(self.cards)
        
    def deal_to_hand(self, hand: Hand, count: int = 1) -> None:
        for i in range(count):
            hand.append(self.pop())
            
    def append(self, card: PlayingCard) -> None: self.cards.append(card)
    
    def deal_to_hands(self, hands: list[Hand], cards_per_hand: int = 1) -> None:
        for i in range(cards_per_hand):
            for hand in hands:
                hand.append(self.pop())
                
    def pop(self) -> PlayingCard: return self.cards.pop()
    
@dataclass
class Hand:
    cards: list[PlayingCard] = field(default_factory = list)
    
    def append(self, card: PlayingCard) -> None: self.cards.append(card)
    
    def draw(self, deck: Deck, count: int = 1) -> None:
        for i in range(count):
            self.append(deck.pop())
            
    def __len__(self) -> int: return len(self.cards)
    
    def sort(self, reverse = False) -> None: self.cards.sort(reverse = not reverse)
    
    def __iter__(self):
        self._iter_index = 0
        return self
    
    def __next__(self) -> PlayingCard:
        if self._iter_index >= len(self.cards): raise StopIteration
        card = self.cards[self._iter_index]
        self._iter_index += 1
        return card

    def has_straight(self) -> bool:
        if (len(self) < 5): return False
        hand_copy = Hand(self.cards[:])
        hand_copy.sort()
        curr_cards = []
        for index,card in enumerate(hand_copy):
            if (len(curr_cards) == 0): 
                curr_cards.append(card)
                continue
            
            last_rank = get_rank_value(curr_cards[-1].rank)
            curr_rank = get_rank_value(card.rank)
            
            if (last_rank == curr_rank + 1): curr_cards.append(card)
            elif (last_rank == curr_rank): continue
            else: curr_cards = [curr_cards[-1]] # We found a card that is too far from the last card, resetting at this new point
            
            if (len(curr_cards) >= 5): return True

        
        return False
    
    def evaluate_hand(self) -> int:
        hand_copy = Hand(self.cards[:])
        hand_copy.sort()
        
        rank_counts = {}
        suit_counts = {}
        for card in hand:
            if (card.rank not in rank_counts): rank_counts[card.rank] = [card]
            else: rank_counts[card.rank].append(card)

            if (card.suit not in suit_counts): suit_counts[card.suit] = [card]
            else: suit_counts[card.suit].append(card)
            
        for rank in rank_counts: rank_counts[rank].sort(reverse = True)
        for suit in suit_counts: suit_counts[suit].sort(reverse = True)
        
        hands_satisfied = [0]
        print(rank_counts, suit_counts)
        
        # 10. Royal flush - Ace high straight and flush
        if (len(hand) >= 5): # Hand requires at least 5 cards
            for suit in suit_counts:
                if (len(suit_counts[suit]) != 5): continue # Current suit does not have enough cards
                for card in suit_counts[suit]:
                    print(card, end = " ")
                print()
        
        # 9. Straight flush - Straight and flush
        if (len(hand) >= 5): # Hand requires at least 5 cards
            ...
            
        # 8. Four of a kind - Four of the same rank
        if (len(hand) >= 4): # Hand requires at least 4 cards
            ...
            
        # 7. Full house - Two of one rank and 3 of another rank
        if (len(hand) >= 5): # Hand requires at least 5 cards
            ...
            
        # 6. Flush - Five of the same suit
        if (len(hand) >= 5): # Hand requires at least 5 cards
            ...
            
        # 5. Straight - Five consecutive ranks (Ace counts as 14 and 1)
        if (len(hand) >= 5): # Hand requires at least 5 cards
            ...
            
        # 4. Three of a kind - Three of the same rank
        if (len(hand) >= 3): # Hand requires at least 3 cards
            for rank in rank_counts:
                if (len(rank_counts[rank])) >= 3:
                    hands_satisfied.append(4)
                    break

        # 3. Two pair - Two of one rank and two of another rank
        if (len(hand) >= 4): # Hand requires at least 4 cards
            diff_rank_pairs = 0
            for rank in rank_counts:
                if (len(rank_counts[rank])) >= 2:
                    diff_rank_pairs += 1
                
                if (diff_rank_pairs >= 2):
                    hands_satisfied.append(3)
                    break

        # 2. Pair - Two of the same rank
        if (len(hand) >= 2): # Hand requires at least 2 cards
            for rank in rank_counts:
                if (len(rank_counts[rank])) >= 2:
                    hands_satisfied.append(2)
                    break
        
        if (len(hand) >= 1): hands_satisfied.append(1) # 1. High card - Any single card
        print(hands_satisfied)
        return max(hands_satisfied)

def get_rank_value(rank: str) -> int:
    try:
        value = int(rank)
    except:
        value = ['j', 'q', 'k', 'a'].index(rank) + 11
    return value


deck = Deck()
deck.generate_playingcard_deck()

hand = Hand()
hand.draw(deck, 5)
rand_shuffle(hand.cards)
print(f"Has straight: {hand.has_straight()}")
print(f"Hand score: {hand.evaluate_hand()}")