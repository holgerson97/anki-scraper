import requests
import json
import os

# AnkiConnect API URL
ANKI_CONNECT_URL = "http://localhost:8765"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

def create_deck(deck_name):
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    return response.json()
  
def build_json_from_file(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
          parts = line.strip().split('\t')
          data[parts[1]] = parts[2]
              
    return data

def add_card(deck_name, front, back):
    print(front, back)
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": [
                    "source:spanish",
                    "target:german"
                ]
            }
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    print(response.json())

# Function to check if a card exists with a given word
def check_card_exist(deck_name, word):
    # Define the AnkiConnect request
    request_data = {
        "action": "findNotes",
        "params": {
            "query": f'"Front:{word}" deck:"{deck_name}"'  # Search for cards with "Front" field equal to the word
        }
    }

    # Make request to AnkiConnect
    response = requests.post(ANKI_CONNECT_URL, json=request_data)
    response_data = response.json()

    # Check if any notes were found
    if response_data:
        return True
    else:
        return False

def translate_card(card):
    headers = {"Authorization": "DeepL-Auth-Key " + os.environ["DEEPL_TOKEN"]}

    payload = {
        "text": [
            card
        ],
        "source_lang": "ES",
        "target_lang": "DE"
    }

    response = requests.post(url=DEEPL_URL, headers=headers, json=payload)
    data = response.json().get("translations")[0]["text"]
    return data
  
if __name__ == "__main__":
    deck_name = "SpanishToGerman"
    create_deck_response = create_deck(deck_name)
        
    words = build_json_from_file("../spanish_1000_words.csv")
    
    for w in words:
        if not check_card_exist(deck_name, w):
            translation = translate_card(w)
            add_card(deck_name, w, translation)