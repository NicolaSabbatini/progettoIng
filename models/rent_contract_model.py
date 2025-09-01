import json
import os
from datetime import datetime

from models.contract_model import ContractModel

class RentContractModel(ContractModel): 
     
    def __init__(self):
        super().__init__()

    


    def add_rent_contract(self, user, auto, start_date, end_date, cauzione, prezzoTot, durataGaranzia, tipoGaranzia, kmMax):
        """Aggiunge un nuovo contratto"""
        if self.contracts:
            new_id = max(c['id'] for c in self.contracts) + 1
        else:
            new_id = 1
        new_rent_contract = {
            'id': new_id,
            'tipo': 'noleggio',
            'user': user,
            'auto': auto,
            'start_date': start_date,
            'end_date': end_date,
            'cauzione': cauzione,
            'tipoGaranzia': tipoGaranzia,
            'durataGaranzia': durataGaranzia,
            'kmMax': kmMax,
            'prezzoTot': prezzoTot,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.contracts.append(new_rent_contract)
        self.save_rent_contracts()
        return True, "Contratto creato con successo"
    
    def save_rent_contracts(self):
        """Salva i contratti nel file JSON"""
        with open(self.contracts_file, 'w', encoding='utf-8') as f:
            json.dump(self.contracts, f, indent=2, ensure_ascii=False)

