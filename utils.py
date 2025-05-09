import json

def open_language(lang: str):
    with open(f"static/languages/{lang}.json", encoding="utf-8") as f:
        return json.load(f)
    