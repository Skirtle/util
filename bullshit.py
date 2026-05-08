import cards, util
import random

def check_claim(table: str, hand: list[cards.PlayingCard]) -> bool:
    card_names = {
        "Ace": "a",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5",
        "Six": "6",
        "Seven": "7",
        "Eight": "8",
        "Nine": "9",
        "Ten": "10",
        "Jack": "j",
        "Queen": "q",
        "King": "k"
    }
    for card in hand:
        if (cards.PlayingCard(card_names[table], card.suit) != card): 
            return False 
    return True

if __name__ == "__main__":
    # Create players
    PLAYER_COUNT = 4
    SEED = 2
    deck = cards.Deck()
    deck.generate_playingcard_deck(True, SEED)
    players: list[cards.Hand] = [cards.Hand() for _ in range(PLAYER_COUNT)]
    deck.deal_to_hands(players, 13)

    for index,player in enumerate(players):
        print(f"Player {index + 1}: {player}")

    current_player = -1
    for index,player in enumerate(players):
        if (cards.PlayingCard("A", "S") in player):
            current_player = index
            break
    
    print(f"Starting player is player {current_player + 1}")
    card_order = util.rotate(cards.PlayingCard._ranks)
    card_names = {
        "a": "Ace",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
        "10": "Ten",
        "j": "Jack",
        "q": "Queen",
        "k": "King"
    }
    turn_number = 0
    last_claim = {
        "table": "",
        "count": 0
    }

    stack = []

    while True:
        print(f"Player {current_player + 1}'s turn at a {card_names[card_order[turn_number % 13]]}'s table")

        # Player chooses cards
        choices = [""]
        while (choices[0] == ""):
            prev_player = (current_player - 1) % PLAYER_COUNT

            if (len(players[prev_player]) == 0):
                # Auto BS call
                choices = "bs"
                auto_bs = True
            else:
                print(f"[{turn_number + 1}] Player {current_player + 1}, you have {players[current_player]}: ", end = "")
                choices = input().strip()
                auto_bs = False

            # Calling BS here
            if (choices in ["bs", "bullshit"]):
                if (len(stack) == 0):
                    print(f"Can't call bullshit on a empty table")
                    choices = [""]
                    continue
                if (last_claim["count"] != 1): s = "s"
                else: s = ""
                print(f"Player {current_player + 1} calls bullshit on player {prev_player + 1}'s {last_claim['count']} {last_claim['table']}{s}")

                # Check the call
                last_played = stack[len(stack) - last_claim["count"]:]
                called_bluff = not check_claim(last_claim["table"], last_played)
                if (called_bluff):
                    print(f"{last_played} have been revealed, player {prev_player + 1} was bullshitting")
                    # Previous player lied, put stack into previous hand and reset stack
                    for c in stack:
                        players[prev_player].append(c)
                    stack = []
                else:
                    print(f"{last_played} have been revealed, player {prev_player + 1} wasn't kidding")
                    if (auto_bs): exit(f"Player {prev_player + 1} wins the game!")
                    # Previous player told the truth, put stack into current hand and reset stack
                    for c in stack:
                        players[current_player].append(c)
                    stack = []
                
                # Go to next turn
                break

            # Not a BS call, convert input into cards
            choices = choices.split(" ")
            if (choices[0] == ""): continue
            try:
                cards_chosen = [cards.str_to_card(c) for c in choices]
            except:
                print(f"Did not understand a card in your choices of {choices}")
                choices = [""]
                continue
            
            # Confirm they have those cards
            reset_flag = False
            for card in cards_chosen:
                if (card not in players[current_player]):
                    print(f"Player {current_player + 1}, you can't choose {card}, it is not in your hand")
                    choices = [""] # Reset choosing
                    reset_flag = True
            if (reset_flag): continue

            # They have the chosen cards, time to remove them
            print(f"Player {current_player + 1} claims {len(cards_chosen)} {card_names[card_order[turn_number % 13]]}'s")
            for card in cards_chosen:
                players[current_player].cards.remove(card) # Remove card from hand
                stack.append(card) # Put card into stack
                last_claim["count"] = len(cards_chosen)
                last_claim["table"] = card_names[card_order[turn_number % 13]]
        
        turn_number += 1
        current_player = (current_player + 1) % PLAYER_COUNT
