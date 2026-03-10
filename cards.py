from dataclasses import dataclass, field
from functools import total_ordering
from abc import ABC
from random import shuffle as rand_shuffle, seed as rand_seed

@dataclass
class Card(ABC): pass

@total_ordering
@dataclass()
class PlayingCard(Card):
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
    cards: list = field(default_factory = list[Card])
    
    def generate_playingcard_deck(self) -> None:
        for rank in PlayingCard._ranks:
            for suit in PlayingCard._suits:
                self.cards.append(PlayingCard(rank, suit))
                
    def shuffle(self, seed: int | None = None) -> None:
        rand_seed(seed)
        rand_shuffle(self.cards)
        
    def deal_to_hand(self, hand: Hand, count: int = 1) -> None:
        for i in range(count):
            hand.append(self.pop())
            
    def append(self, card: Card) -> None: self.cards.append(card)
    
    def deal_to_hands(self, hands: list[Hand], cards_per_hand: int = 1) -> None:
        for i in range(cards_per_hand):
            for hand in hands:
                hand.append(self.pop())
                
    def pop(self) -> Card:
        return self.cards.pop()
    
    
@dataclass
class Hand:
    cards: list = field(default_factory = list[Card])
    
    def append(self, card: Card) -> None: self.cards.append(card)
    
deck = Deck()
deck.generate_playingcard_deck()
deck.shuffle()

hand_1 = Hand()
hand_2 = Hand()
deck.deal_to_hands([hand_1, hand_2], 5)
print(hand_1, hand_2)