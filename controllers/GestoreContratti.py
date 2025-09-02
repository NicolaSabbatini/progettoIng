from datetime import datetime

from controllers.GestoreAuto import GestoreAuto

from models.Contratto import Contratto
from models.ContrattoAcquisto import ContrattoAcquisto
from models.ContrattoNoleggio import ContrattoNoleggio
from models.Fattura import Fattura

from views.CreaContrattoAcquistoDialog import CreaContrattoAcquistoDialog
from views.CreaContrattoNoleggioDialog import CreaContrattoNoleggioDialog
from views.CreaFatturaDialog import CreaFattura

class GestoreContratti:
    def __init__(self, contract_view=None, dashboard_view=None, fatture_view=None):
        
        self.contract_view = contract_view
        self.dashboard_view = dashboard_view
        self.contract_model = Contratto()
        self.buy_contract_model = ContrattoAcquisto()
        self.rent_contract_model = ContrattoNoleggio()
        self.fatture_model = Fattura()
        self.auto_controller = GestoreAuto(self.dashboard_view) 
        self.fatture_view = fatture_view

    def get_all_contracts(self):
        """Restituisce tutti i contratti"""
        return self.contract_model.get_all_contracts()
    
    def get_contracts(self, username=None):
        return self.contract_model.get_contracts(username)

    def crea_noleggio_contratto(self):
        dialog = CreaContrattoNoleggioDialog(parent=None, controller=self, contract_view=self.contract_view)
        dialog.exec_()

    def crea_acquisto_contratto(self):  
        dialog = CreaContrattoAcquistoDialog(parent=None, controller=self, contract_view=self.contract_view)
        dialog.exec_()

    
    def center_window(self, view):
        """Centra la finestra sullo schermo"""
        screen = view.screen().availableGeometry()
        size = view.geometry()
        view.move(
            max(0, (screen.width() - view.width()) // 2),
            max(0, (screen.height() - view.height()) // 2)
        )


    def addo_noleggio_contratto(self, user, auto, start_date, end_date, cauzione, tipoGaranzia, durataGaranzia, kmMax, prezzoTot):
        """Aggiunge un nuovo contratto"""
        if not (user and auto and start_date and end_date and cauzione and tipoGaranzia and durataGaranzia and kmMax and prezzoTot):
            return False, "Tutti i campi del contratto sono obbligatori"
        

        
        success = self.rent_contract_model.add_rent_contract(user, auto, start_date, end_date, cauzione, prezzoTot, durataGaranzia, tipoGaranzia, kmMax)
        self.rimuoviAuto(auto)
        self.auto_controller.load_auto()
        self.rent_contract_model.load_contracts()
        self.buy_contract_model.load_contracts()
        self.contract_model.load_contracts()
        if self.contract_view:
            self.contract_view.refresh_contracts()
        if success:
            return True, "Contratto aggiunto con successo"
        else:
            return False, "Errore durante l'aggiunta del contratto"


    def addo_acquisto_contratto(self, user, auto, tipoGaranzia, durataGaranzia, prezzoTot):
        """Aggiunge un nuovo contratto"""
        if not (user and auto and tipoGaranzia and durataGaranzia and prezzoTot):
            return False, "Tutti i campi del contratto sono obbligatori"
        
        
        success = self.buy_contract_model.add_buy_contract(user, auto, prezzoTot, durataGaranzia, tipoGaranzia)
        self.rimuoviAuto(auto)
        self.auto_controller.load_auto()
        self.rent_contract_model.load_contracts()
        self.buy_contract_model.load_contracts()
        self.contract_model.load_contracts()
        if self.contract_view:
            self.contract_view.refresh_contracts()
        if success:
            return True, "Contratto aggiunto con successo"
        else:
            return False, "Errore durante l'aggiunta del contratto"
            
    
    def delete_contract_and_fatture(self, contract_id, auto_id, contract_view=None):
        """Elimina un contratto e tutte le sue fatture collegate"""


        # 1️ Elimina le fatture legate a quel contratto
        self.fatture_model.fatture = [
            f for f in self.fatture_model.fatture if f['contratto'] != contract_id
        ]
        self.fatture_model.save_fatture()
        

        self.contract_view = contract_view
        # 2️ Elimina il contratto
        success = self.contract_model.delete_contract(contract_id)
        self.reimpostaAuto(auto_id)  # Reimposta l'auto associata al contratto
        self.auto_controller.load_auto()
        self.rent_contract_model.load_contracts()
        self.buy_contract_model.load_contracts()
        self.contract_model.load_contracts()

        if contract_view:
            self.contract_view.refresh_contracts()
        if success:
            return True, "Contratto e fatture collegate eliminate con successo"
        else:
            return False, "Errore durante l'eliminazione del contratto e delle fatture collegate"
    
    def rimuoviAuto(self, autoId):
        self.auto_controller.rimuoviAuto(autoId)

    def reimpostaAuto(self, autoId):
        """Reimposta l'auto per essere visibile nel catalogo"""
        success = self.auto_controller.reimpostaAuto(autoId)
        if success:
            return True, "Auto reimpostata con successo"
        else:
            return False, "Errore durante la reimpostazione dell'auto"
        
    def check_contracts_and_notify_dashboard(self, dashboard_view=None):
        today = datetime.now().date()
        expired_contracts = []
        for contract in self.contract_model.get_all_contracts():
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
                    
                dashboard_view.show_notification(msg)
            elif dashboard_view:
                print("Nessun contratto scaduto trovato.")
                dashboard_view.notification_label.hide()



    def get_all_fatture(self):
        """Restituisce tutti i contratti"""
        return self.fatture_model.get_all_fatture()

    def get_fatture_by_contratto(self, contract_id):
        """Restituisce le fatture associate a un contratto specifico"""
        return self.fatture_model.get_fatture_by_contract(contract_id)
    
    def create_fattura_button(self, contract_id):
        dialog = CreaFattura(parent=None, controller=self, fatture_view=self.fatture_view, contract_id=contract_id)
        dialog.exec_()

    def addo_fattura(self, start_date, price, contract_id):
        """Aggiunge un nuovo contratto"""
        if not (start_date and price):
            return False, "Tutti i campi del contratto sono obbligatori"
        
        self.fatture_model.add_fattura(start_date, price, contract_id)
        return True, "fattura aggiunto con successo"

