import csv
import os
import sys
import math
from getpass import getpass

from tinycards import Tinycards
from tinycards.model import Deck


DEBUG = False

DECK_CARDS_PER_UNIT = 15  # Amount of cards per deck
DECK_COVER_PATH = 'cover.png'  # Path for cover image
DECK_DESC = 'Automatically generated deck from CSV file for Rivstart A1+A2 vocabulary'
DECK_TTS_LANGUAGES = ['en', 'sv']  # TTS languages. [front, back]
DECK_REMOVE_EXISTING = True  # Remove all cards from deck if modifying an existing one


def csv_to_deck(csv_path, deck_base_name):
    """
    Creates a Tinycards deck from a CSV file.
    The CSV file is expected to have two columns
    """
    # Extract data from CSV file.
    word_pairs = []
    pairs_amount = 0
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            word_pairs.append((row[1], row[0]))
        pairs_amount = len(word_pairs)

    if not DEBUG:
        client_tinycards = Tinycards(user_identifier, user_password)

    if pairs_amount == 0:
        print('No word pairs were found in CSV')
        sys.exit()

    decks = math.ceil(pairs_amount/DECK_CARDS_PER_UNIT)
    for index, deck in enumerate(range(decks)):
        # Get deck by name. If doesn't exist - create new
        subdeck_name = f'{deck_base_name} - {index}'
        if not DEBUG:
            deck = client_tinycards.find_deck_by_title(subdeck_name)
            if not deck:
                deck = Deck(subdeck_name)
                deck = client_tinycards.create_deck(deck)
            elif DECK_REMOVE_EXISTING:
                deck.cards = []

        # Customize deck
        deck.cover = DECK_COVER_PATH
        deck.description = DECK_DESC
        deck.tts_languages = DECK_TTS_LANGUAGES

        # Populate deck with cards from CSV data
        for pair in range(DECK_CARDS_PER_UNIT):
            try:
                deck.add_card(word_pairs.pop())
            except IndexError:
                pass

        # Save changes to Tinycards
        if not DEBUG:
            client_tinycards.update_deck(deck)

    if not DEBUG:
        print(f'Successfully created {decks} decks from {pairs_amount} word pairs')
    else:
        print('Dry run. No Tinycard decks were created')
        print(f'{decks} decks from {pairs_amount} word pairs are ready to be uploaded')


if __name__ == '__main__':
    # Take identifier and password from ENV or ask user if not set.
    user_identifier = os.environ.get('TINYCARDS_IDENTIFIER')
    if not user_identifier:
        print('Input identifier (e.g. email):')
        user_identifier = input()
    user_password = os.environ.get('TINYCARDS_PASSWORD')
    if not user_password:
        print('Input password:')
        user_password = getpass()

    if len(sys.argv[1:]) < 2:
        print('Please specify which CSV file to use and deck base name')
        print('For example "python3 csv_to_deck.py 05-05-2020.csv RememberlyDeck-05-05-2020"')
        sys.exit()
    csv_to_deck(sys.argv[1], sys.argv[2])
