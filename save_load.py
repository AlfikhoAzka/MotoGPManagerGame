import json

def save_game(data):
    with open("save.json", "w") as f:
        json.dump(data, f)

def load_game():
    try:
        with open("save.json", "r") as f:
            return json.load(f)
    except:
        return None