# Tinycards automation
A simple nightly build of python script to automatically create and upload flashcards to [Tinycards](https://tinycards.duolingo.com/) from CSV file.

## Use case
As I studied Swedish language I caught myself using google translator all the time. The problem with it is that all the translation history is gone and so is understanding foreign words. So instead of google tranlator I discovered chrome extension [Rememberry](https://chrome.google.com/webstore/detail/rememberry-translate-and/dipiagiiohfljcicegpgffpbnjmgjcnf?hl=en-GB) which is a great alternative to traslate words from web and save them locally. The extension allows you to export as CSV. Once you have the CSV file with your words the current script will help to automatically create Tinycard's decks for you to practice flashcards offline using smartphone.

## Installation
Thanks to [@floscha](https://github.com/floscha) we have an unofficial pythin API for Tinycards:

```python
pip install tinycards
```

Clone the script and adjust as needed. 
When ready use as following:
```shell
python3 csv_to_desk.py example.csv "LS1512 Swedish A2"
```
Where the first argument is a file path and the second base name of the deck. 

**Note** that you can create local `.env` file and put there environmental variables for your Tinycards authentication credentials.

## Features
- Load data from provided CSV and split by custom amount of cards (default 15) in deck.
- Upload created decks to Tinycards with a custom cover image, description and TTS languages
