import requests
import bs4
from bs4 import BeautifulSoup


def cards_in_decks(response):
    soup = BeautifulSoup(response.content, "html.parser")
    deck_lists = soup.find_all(["div"], class_="comp-deck-col card-list")
    one_of_every_deck = []
    two_of_every_deck = []
    other_cards = {}
    deck = {}

    for decks in deck_lists:
        # Cycles through decks.
        dlist = decks.find('ul', class_="deck-class")
        cardlist = dlist.find_all(['li'])
        for li in cardlist:
            # Cycle through cards in each deck. Taking the card name and count.
            if type(li) == bs4.element.Tag and li['class'] != ['blank']:
                card_count = li.find('span', class_='card-count').get_text()
                card_name = li.find('span', class_='card-name').get_text()
                if card_name not in one_of_every_deck and \
                        card_name not in two_of_every_deck:
                    # Checks to see if card is already in a list.
                    if 'match' in li['class']:
                        # Checks if a card is in every deck. If so how many.
                        if card_count == "1":
                            one_of_every_deck.append(card_name)
                        elif card_count == "2":
                            two_of_every_deck.append(card_name)
                    else:
                        # If not, add the card name and count into a dictionary as
                        # {card name : [card count]}
                        if card_name in other_cards:
                            other_cards['{}'.format(card_name)]\
                                .append(card_count)
                        else:
                            other_cards['{}'.format(card_name)] = [card_count]
    for cards in one_of_every_deck:
        deck['{}'.format(cards)] = 1
    for cards in two_of_every_deck:
        deck['{}'.format(cards)] = 2
    for cards in other_cards:
        if cards not in deck.keys():
            deck['{}'.format(cards)] = (sum([int(counts) for counts
                                                       in other_cards[cards]]) /
                                              len(deck_lists))
    return deck


def deck_size(deck):
    side_board = [cards for cards in deck if round(deck[cards]) == 0]
    main_deck = {card: count for (card, count) in deck.items() if card
                 not in side_board}

    if sum(main_deck.values()) > 30:
        while sum(main_deck.values()) > 30:
            least_used_card = min(deck, key=deck.get)
            print(least_used_card)
            if least_used_card in main_deck:
                main_deck.pop(least_used_card)
        for cards in main_deck:
            main_deck[cards] = round(main_deck[cards])
        print(sum(main_deck.values()))
        return main_deck
    elif round(sum(main_deck.values())) < 30:
        for cards in main_deck:
            main_deck[cards] = round(main_deck[cards])
        print(sum(main_deck.values()))
        print(
            "Cards that other people are using (Most used to least used): \n",
            side_board)
        return main_deck

    else:
        for cards in main_deck:
            main_deck[cards] = round(main_deck[cards])
        print(sum(main_deck.values()))
        return main_deck


if __name__ == '__main__':
    url = input("Enter a Hearthstone Top Decks Compare URL.")
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
    if response.status_code == 200:
        deck_list = cards_in_decks(response)
        deck_list = deck_size(deck_list)
        print("Cards the show up in at least once in at least half of the "
                "decks: \n", deck_list)
    else:
        print("Url could not be downloaded. Url returned a status code of ",
              response.status_code)
