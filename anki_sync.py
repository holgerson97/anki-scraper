import requests
import json

# AnkiConnect API URL
ANKI_CONNECT_URL = "http://localhost:8765"

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
                "tags": []
            }
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)

if __name__ == "__main__":
    deck_name = "Spanish"
    create_deck_response = create_deck(deck_name)
    
    words = build_json_from_file("./spanish_1000_words.csv")
    for w in words:
      add_card(deck_name, w, words[w])