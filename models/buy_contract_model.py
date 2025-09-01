import json
import os
from datetime import datetime

from models.contract_model import ContractModel

class BuyContractModel(ContractModel): 
     
   def __init__(self):
        super().__init__()


   def add_buy_contract(self, user, auto, prezzoTot, durataGaranzia, tipoGaranzia):
        """Aggiunge un nuovo contratto"""
        if self.contracts:
            new_id = max(c['id'] for c in self.contracts) + 1
        else:
            new_id = 1
        new_buy_contract = {
            'id': new_id,
            'tipo': 'acquisto',
            'user': user,
            'auto': auto,
            'price': prezzoTot,
            'durataGaranzia': durataGaranzia,
            'tipoGaranzia': tipoGaranzia,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.contracts.append(new_buy_contract)
        self.save_buy_contracts()
        return True, "Contratto creato con successo"
   
   def save_buy_contracts(self):
        """Salva i contratti nel file JSON"""
        with open(self.contracts_file, 'w', encoding='utf-8') as f:
            json.dump(self.contracts, f, indent=2, ensure_ascii=False)
    
