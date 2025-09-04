import json
import os

class Fattura:
    def __init__(self):
        self.fatture_file = 'data/fatture.json'
        os.makedirs('data', exist_ok=True)
        self.loadBills()

    def addBill(self, data, price, contratto):
        """Aggiunge una nuova fattura"""
        new_id = len(self.fatture) + 1
        new_fattura = {
            'idfattura': new_id,
            'contratto': contratto,
            'data': data,
            'prezzo': price,
        }
        self.fatture.append(new_fattura)
        self.saveBills()
        return True, "Fattura creata con successo"
    
    def getBillsByContract(self, contract_id):
        """Restituisce tutte le fatture associate a un contratto specifico"""
        return [fattura for fattura in self.fatture if fattura['contratto'] == contract_id]

    def loadBills(self):
        """Carica le fatture dal file JSON"""
        try:
            with open(self.fatture_file, 'r', encoding='utf-8') as f:
                self.fatture = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.fatture = []
            self.saveBills()

    def saveBills(self):
        """Salva le fatture nel file JSON"""
        with open(self.fatture_file, 'w', encoding='utf-8') as f:
            json.dump(self.fatture, f, indent=2, ensure_ascii=False)
 
