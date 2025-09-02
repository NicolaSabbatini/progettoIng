import json
import os

class AutoModel:
    def __init__(self):
        self.auto_file = 'data/auto.json'
        os.makedirs('data', exist_ok=True)
        self.auto_list = []
        self.load_auto()

    def load_auto(self):
        """Carica le auto dal file JSON"""
        try:
            with open(self.auto_file, 'r', encoding='utf-8') as f:
                self.auto_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.auto_list = []
            self.save_auto()

    def save_auto(self):
        with open(self.auto_file, 'w', encoding='utf-8') as f:
            json.dump(self.auto_list, f, ensure_ascii=False, indent=2)

    def add_auto(self, marca, modello, anno, chilometri, prezzo, targa):
        if self.auto_list:
            new_id = max(c['id'] for c in self.auto_list) + 1
        else:
            new_id = 1
        new_auto = {
            'id': new_id,
            'marca': marca,
            'modello': modello,
            'anno': anno,
            'chilometri': chilometri,
            'prezzo': prezzo,
            'targa': targa,
            'visibile': True 
        }
        self.auto_list.append(new_auto)
        self.save_auto()
        return True, "Auto creata con successo"

    def get_all_auto(self):
        return [a for a in self.auto_list if a.get('visibile', True)]
    
    def get_every_auto(self):
        return self.auto_list
    
    def delete_auto(self, auto_id):
        """Elimina un'auto dato il suo id"""
        if self.auto_list is None:
            self.auto_list = []
        for i, auto in enumerate(self.auto_list):
            if auto['id'] == auto_id:
                del self.auto_list[i]
                self.save_auto()
                return True
        return False
    
    def rimuoviAuto(self, auto_id):
        if self.auto_list is None:
            self.auto_list = []
        auto_id = int(auto_id)  # sicurezza
        for auto in self.auto_list:
            print(f"Controllo auto {auto['id']} (visibile={auto['visibile']})")
            if auto['id'] == auto_id:
                auto['visibile'] = False
                self.save_auto()
                self.auto_list = self.load_auto()  # <-- aggiorna la lista!
                print("Trovata e modificata")
                return True
        print("Auto non trovata")
        return False
    
    def reimpostaAuto(self, auto_id):
        """Reimposta l'auto per essere visibile nel catalogo"""
        if self.auto_list is None:
            self.auto_list = []
        auto_id = int(auto_id)  # sicurezza
        for auto in self.auto_list:
            print(f"Controllo auto {auto['id']} (visibile={auto['visibile']})")
            if auto['id'] == auto_id:
                auto['visibile'] = True
                self.save_auto()
                self.auto_list = self.load_auto()  # <-- aggiorna la lista!
                print("Trovata e modificata")
                return True
        return False
    
    def update_auto(self, auto_id, marca=None, modello=None, anno=None, chilometri=None, prezzo=None, targa=None):
        """Aggiorna i dati di un'auto esistente"""
        if self.auto_list is None:
            self.auto_list = []
        auto_id = int(auto_id)
        for auto in self.auto_list:
            if auto['id'] == auto_id:
                if marca is not None:
                    auto['marca'] = marca
                if modello is not None:
                    auto['modello'] = modello
                if anno is not None:
                    auto['anno'] = anno
                if chilometri is not None:
                    auto['chilometri'] = chilometri
                if prezzo is not None:
                    auto['prezzo'] = prezzo
                if targa is not None:
                    auto['targa'] = targa
                self.save_auto()
                return True, "Auto aggiornata con successo"
        return False, "Auto non trovata"

    