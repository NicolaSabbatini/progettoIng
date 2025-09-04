import json
from datetime import datetime

from models.Contratto import Contratto
from models.Auto import Auto
class ContrattoAcquisto(Contratto): 
     
   def __init__(self):
        super().__init__()
        self.auto_model = Auto()


   def addBuyContract(self, user, auto, prezzoTot, durataGaranzia, tipoGaranzia):
        """Aggiunge un nuovo contratto"""

        datiAuto =self.auto_model.getCarById(auto)

        if datiAuto:
            datiAuto = f"{datiAuto['marca']} {datiAuto['modello']} {datiAuto['targa']}"
        else:
            return False, "Auto non trovata"
        
        if self.contracts:
            new_id = max(c['id'] for c in self.contracts) + 1
        else:
            new_id = 1
        new_buy_contract = {
            'id': new_id,
            'tipo': 'acquisto',
            'user': user,
            'auto': datiAuto,
            'price': prezzoTot,
            'durataGaranzia': durataGaranzia,
            'tipoGaranzia': tipoGaranzia,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.contracts.append(new_buy_contract)
        self.saveBuyContracts()
        return True, "Contratto creato con successo"
   
   def saveBuyContracts(self):
        """Salva i contratti nel file JSON"""
        with open(self.contracts_file, 'w', encoding='utf-8') as f:
            json.dump(self.contracts, f, indent=2, ensure_ascii=False)
    
