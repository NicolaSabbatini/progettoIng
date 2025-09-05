from datetime import datetime

from controllers.GestoreAuto import GestoreAuto


from models.Contratto import Contratto
from models.ContrattoAcquisto import ContrattoAcquisto
from models.ContrattoNoleggio import ContrattoNoleggio
from models.Fattura import Fattura

from views.CreaContrattoAcquistoDialog import CreaContrattoAcquistoDialog
from views.CreaContrattoNoleggioDialog import CreaContrattoNoleggioDialog
from views.CreaFatturaDialog import CreaFatturaDialog

class GestoreContratti:
    def __init__(self, contract_view=None, dashboard_view=None, fatture_view=None):
        from controllers.GestoreUtenti import GestoreUtenti
        self.contract_view = contract_view
        self.dashboard_view = dashboard_view
        self.contract_model = Contratto()
        self.buy_contract_model = ContrattoAcquisto()
        self.rent_contract_model = ContrattoNoleggio()
        self.fatture_model = Fattura()
        self.auto_controller = GestoreAuto(self.dashboard_view)
        self.user_controller = GestoreUtenti() 
        self.fatture_view = fatture_view

    def aggiungiContrattoAcquisto(self, user, auto, tipoGaranzia, durataGaranzia, prezzoTot):
        """Aggiunge un nuovo contratto"""
        if not (user and auto and tipoGaranzia and durataGaranzia and prezzoTot):
            return False, "Tutti i campi del contratto sono obbligatori"
        
        success = self.buy_contract_model.addBuyContract(user, auto, prezzoTot, durataGaranzia, tipoGaranzia)
        self.auto_controller.eliminaAuto(auto)
        self.auto_controller.caricaAuto()
        self.rent_contract_model.loadContracts()
        self.buy_contract_model.loadContracts()
        self.contract_model.loadContracts()
        if self.contract_view:
            self.contract_view.refreshContracts()
        if success:
            return True, "Contratto aggiunto con successo"
        else:
            return False, "Errore durante l'aggiunta del contratto"

    def aggiungiContrattoNoleggio(self, user, auto, startDate, endDate, cauzione, tipoGaranzia, durataGaranzia, kmMax, prezzoTot):
        """Aggiunge un nuovo contratto"""
        if not (user and auto and startDate and endDate and cauzione and tipoGaranzia and durataGaranzia and kmMax and prezzoTot):
            return False, "Tutti i campi del contratto sono obbligatori"
        
        success = self.rent_contract_model.addRentContract(user, auto, startDate, endDate, cauzione, prezzoTot, durataGaranzia, tipoGaranzia, kmMax)
        self.auto_controller.rimuoviAuto(auto)
        self.auto_controller.caricaAuto()
        self.rent_contract_model.loadContracts()
        self.buy_contract_model.loadContracts()
        self.contract_model.loadContracts()
        if self.contract_view:
            self.contract_view.refreshContracts()
        if success:
            return True, "Contratto aggiunto con successo"
        else:
            return False, "Errore durante l'aggiunta del contratto"

    def aggiungiFattura(self, startDate, price, contractId):
        """Aggiunge un nuovo contratto"""
        if not (startDate and price):
            return False, "Tutti i campi della fattura sono obbligatori"
        
        self.fatture_model.addBill(startDate, price, contractId)
        return True, "fattura aggiunto con successo"
    
    def creaContrattoAcquistoDialog(self):  
        dialog = CreaContrattoAcquistoDialog(parent=None, controller=self, contract_view=self.contract_view)
        dialog.exec_()

    def creaContrattoNoleggioDialog(self):
        dialog = CreaContrattoNoleggioDialog(parent=None, controller=self, contract_view=self.contract_view)
        dialog.exec_()

    def creaFatturaDialog(self, contractId):
        dialog = CreaFatturaDialog(parent=None, controller=self, fatture_view=self.fatture_view, contract_id=contractId)
        dialog.exec_()

    def eliminaContrattieFatture(self, contractId, autoId, contract_view=None):
        """Elimina un contratto e tutte le sue fatture collegate"""
        # 1️ Elimina le fatture legate a quel contratto
        self.fatture_model.fatture = [
            f for f in self.fatture_model.fatture if f['contratto'] != contractId
        ]
        self.fatture_model.saveBills()
        self.contract_view = contract_view
        # 2️ Elimina il contratto
        success = self.contract_model.deleteContract(contractId)
        self.reimpostaAuto(autoId)  # Reimposta l'auto associata al contratto
        self.auto_controller.caricaAuto()
        self.rent_contract_model.loadContracts()
        self.buy_contract_model.loadContracts()
        self.contract_model.loadContracts()

        if contract_view:
            self.contract_view.refreshContracts()
        if success:
            return True, "Contratto e fatture collegate eliminate con successo"
        else:
            return False, "Errore durante l'eliminazione del contratto e delle fatture collegate"

    def getContratti(self):
        """Restituisce tutti i contratti"""
        return self.contract_model.getAllContracts()
    
    def getContrattiCliente(self, username=None):
        return self.contract_model.getClientContracts(username)

    def getFatturePerContratto(self, contractId):
        """Restituisce le fatture associate a un contratto specifico"""
        return self.fatture_model.getBillsByContract(contractId)
    
    def reimpostaAuto(self, autoId):
        """Reimposta l'auto per essere visibile nel catalogo"""
        success = self.auto_controller.reimpostaAuto(autoId)
        if success:
            return True, "Auto reimpostata con successo"
        else:
            return False, "Errore durante la reimpostazione dell'auto"

    def verificaScadenza(self, dashboard_view=None):
        today = datetime.now().date()
        expired_contracts = []
        for contract in self.contract_model.getAllContracts():
            if contract['tipo'] == 'noleggio':
                print(f"Controllo contratto ID {contract['id']} con end_date {contract['end_date']}")
                try:
                    end_date = datetime.strptime(contract["end_date"], '%d/%m/%Y').date()
                    if end_date < today:
                        print(f"Contratto scaduto trovato con end_date {contract['end_date']}")
                        expired_contracts.append(contract)
                except Exception as e:
                    print(f"Errore nel parsing della data {contract['end_date']}: {e}")

            if expired_contracts and dashboard_view:
                msg = "Contratti scaduti:\n"
                for c in expired_contracts:
                    print(f"Contratto scaduto trovato: ID {c['id']}, Utente {c['user']}, Auto {c['auto']}, End date {c['end_date']}")
                    msg += f"ID: {c['id']}, Utente: {c['user']}, Auto: {c['auto']}, End date: {c['end_date']}\n"
                    
                dashboard_view.showNotification(msg)
            elif dashboard_view:
                print("Nessun contratto scaduto trovato.")
                dashboard_view.notification_label.hide()


    



