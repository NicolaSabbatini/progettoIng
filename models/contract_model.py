import json
import os
from datetime import datetime

class ContractModel:
    def __init__(self):
        self.contracts_file = 'data/contract.json'
        self.ensure_data_directory()
        self.load_contracts()

    def ensure_data_directory(self):
        """Crea la directory data se non esiste"""
        os.makedirs('data', exist_ok=True)

    def load_contracts(self):
        """Carica i contratti dal file JSON"""
        try:
            with open(self.contracts_file, 'r', encoding='utf-8') as f:
                self.contracts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.contracts = []
            self.save_contracts()

    def save_contracts(self):
        """Salva i contratti nel file JSON"""
        with open(self.contracts_file, 'w', encoding='utf-8') as f:
            json.dump(self.contracts, f, indent=2, ensure_ascii=False)

    def add_contract(self, user, auto, start_date, end_date, price, garanzia):
        """Aggiunge un nuovo contratto"""
        new_id = len(self.contracts) + 1
        new_contract = {
            'id': new_id,
            'user': user,
            'auto': auto,
            'start_date': start_date,
            'end_date': end_date,
            'price': price,
            'garanzia': garanzia,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.contracts.append(new_contract)
        self.save_contracts()
        return True, "Contratto creato con successo"

    def get_all_contracts(self):
        """Restituisce tutti i contratti"""
        return self.contracts
    
    def get_contracts(self, username=None):
        if username is None:
            return False
        else:
            return [contract for contract in self.contracts if contract.get('user') == username]
        

    def get_contract_by_id(self, contract_id):
        """Restituisce un contratto dato il suo id"""
        for contract in self.contracts:
            if contract['id'] == contract_id:
                return contract
        return None
    
    def delete_contract(self, contract_id):
        """Elimina un contratto dato il suo id"""
        for i, contract in enumerate(self.contracts):
            if contract['id'] == contract_id:
                del self.contracts[i]
                self.save_contracts()
                return True
        return False