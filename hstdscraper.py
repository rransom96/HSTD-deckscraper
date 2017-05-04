import requests
import math
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
                            other_cards['{}'.format(card_name)].append(card_count)
                        else:
                            other_cards['{}'.format(card_name)] = [card_count]
    # while sum(deck.values()) < 30:
    for cards in one_of_every_deck:
        deck['{}'.format(cards)] = 1
    for cards in two_of_every_deck:
        deck['{}'.format(cards)] = 2
    for cards in other_cards:
        if cards not in deck.keys():
            # deck['{}'.format(cards)] = (sum([int(counts) for counts in
            #                             other_cards[cards]]) // 8)
            deck['{}'.format(cards)] = math.ceil((sum([int(counts) for counts in
                                             other_cards[cards]]) //
                                                  len(deck_lists)))
    print(sum(deck.values()),"/30 cards in deck")

    return deck


if __name__ == '__main__':
    url = input("Enter a Hearthstone Top Decks Compare URL.")
    response = requests.get(url)
    if response.status_code == 200:
        deck_list = cards_in_decks(response)
        print(deck_list)
    else:
        print("Url could not be downloaded. Url returned a status code of {}")\
            .format(response.status_code)
