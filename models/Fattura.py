import json
import os

class Fattura:
    def __init__(self):
        self.fatture_file = 'data/fatture.json'
        self.ensure_data_directory()
        self.load_fatture()

    def ensure_data_directory(self):
        """Crea la directory data se non esiste"""
        os.makedirs('data', exist_ok=True)

    def load_fatture(self):
        """Carica le fatture dal file JSON"""
        try:
            with open(self.fatture_file, 'r', encoding='utf-8') as f:
                self.fatture = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.fatture = []
            self.save_fatture()

    def save_fatture(self):
        """Salva le fatture nel file JSON"""
        with open(self.fatture_file, 'w', encoding='utf-8') as f:
            json.dump(self.fatture, f, indent=2, ensure_ascii=False)

    def add_fattura(self, data, price, contratto):
        """Aggiunge una nuova fattura"""
        new_id = len(self.fatture) + 1
        new_fattura = {
            'idfattura': new_id,
            'contratto': contratto,
            'data': data,
            'prezzo': price,
        }
        self.fatture.append(new_fattura)
        self.save_fatture()
        return True, "Fattura creata con successo"

    def get_all_fatture(self):
        """Restituisce tutte le fatture"""
        return self.fatture

    def get_fattura_by_id(self, idfattura):
        """Restituisce una fattura dato il suo id"""
        for fattura in self.fatture:
            if fattura['idfattura'] == idfattura:
                return fattura
        return None
    
    def get_fatture_by_contract(self, contract_id):
        """Restituisce tutte le fatture associate a un contratto specifico"""
        return [fattura for fattura in self.fatture if fattura['contratto'] == contract_id]