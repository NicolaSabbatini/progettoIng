import json
import os

class Contratto:
    def __init__(self):
        self.contracts_file = 'data/contract.json'
        os.makedirs('data', exist_ok=True)
        self.loadContracts()      

    def deleteContract(self, contract_id):
        """Elimina un contratto dato il suo id"""
        for i, contract in enumerate(self.contracts):
            if contract['id'] == contract_id:
                del self.contracts[i]
                self.saveContracts()
        return

    def getAllContracts(self):
        """Restituisce tutti i contratti"""
        return self.contracts
    
    def getClientContracts(self, username=None):
        if username is None:
            return False
        else:
            return [contract for contract in self.contracts if contract.get('user') == username]

    def loadContracts(self):
        """Carica i contratti dal file JSON"""
        try:
            with open(self.contracts_file, 'r', encoding='utf-8') as f:
                self.contracts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.contracts = []
            self.saveContracts()

    def saveContracts(self):
        """Salva i contratti nel file JSON"""
        with open(self.contracts_file, 'w', encoding='utf-8') as f:
            json.dump(self.contracts, f, indent=2, ensure_ascii=False)