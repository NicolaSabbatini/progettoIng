import json
import os

class AutoModel:
    def __init__(self):
        self.auto_file = 'data/auto.json'
        os.makedirs('data', exist_ok=True)
        self.auto_list = self.load_auto()

    def load_auto(self):
        try:
            with open(self.auto_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_auto(self):
        with open(self.auto_file, 'w', encoding='utf-8') as f:
            json.dump(self.auto_list, f, ensure_ascii=False, indent=2)

    def add_auto(self, marca, modello, anno, chilometri, prezzo, targa):
        # Generate a new id
        new_id = len(self.auto_list) + 1
        # Check for duplicates (optional)
        for auto in self.auto_list:
            if auto['marca'] == marca and auto['modello'] == modello and auto['anno'] == anno and auto['targa'] == targa and auto['chilometri'] == chilometri and auto['prezzo'] == prezzo:
                return False, "Auto già esistente"
        new_auto = {
            'id': new_id,
            'marca': marca,
            'modello': modello,
            'anno': anno,
            'chilometri': chilometri,
            'prezzo': prezzo,
            'targa': targa
        }
        self.auto_list.append(new_auto)
        self.save_auto()
        return True, "Auto creata con successo"

    def get_all_auto(self):
        return self.auto_list
    
    def delete_auto(self, auto_id):
        """Elimina un'auto dato il suo id"""
        for i, auto in enumerate(self.auto_list):
            if auto['id'] == auto_id:
                del self.auto_list[i]
                self.save_auto()
                return True
        return False