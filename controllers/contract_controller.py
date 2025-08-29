from models.user_model import UserModel
from datetime import datetime



from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QDialog
from PyQt5.QtCore import Qt


from models.contract_model import ContractModel
from models.buy_contract_model import BuyContractModel
from models.rent_contract_model import RentContractModel
from controllers.fatture_controller import FattureController
from models.fatture_model import FattureModel
from views.contract_view import ContractView

class ContractController:
    def __init__(self, main_controller, contract_view=None, dashboard_view=None):
        self.main_controller = main_controller 
        self.contract_view = contract_view
        self.dashboard_view = dashboard_view
        self.contract_model = ContractModel()
        self.buy_contract_model = BuyContractModel()
        self.rent_contract_model = RentContractModel()
        self.fatture_model = FattureModel()


    def get_all_contracts(self):
        """Restituisce tutti i contratti"""
        return self.contract_model.get_all_contracts()
    
    def get_contracts(self, username=None):
        return self.contract_model.get_contracts(username)

    def crea_noleggio_contratto(self):
        dialog = CreaRentContract(parent=None, controller=self, contract_view=self.contract_view)
        dialog.exec_()

    def crea_acquisto_contratto(self):
        dialog = CreaBuyContract(parent=None, controller=self, contract_view=self.contract_view)
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
        
        self.rent_contract_model.add_rent_contract(user, auto, start_date, end_date, cauzione, prezzoTot, durataGaranzia, tipoGaranzia, kmMax)
        return True, "Contratto aggiunto con successo"


    def addo_acquisto_contratto(self, user, auto, tipoGaranzia, durataGaranzia, prezzoTot):
        """Aggiunge un nuovo contratto"""
        if not (user and auto and tipoGaranzia and durataGaranzia and prezzoTot):
            return False, "Tutti i campi del contratto sono obbligatori"
        
        self.buy_contract_model.add_buy_contract(user, auto, prezzoTot, durataGaranzia, tipoGaranzia)
        return True, "Contratto aggiunto con successo"
    
    def elimina_contratto(self, contract_id, contract_view=None):
        """Elimina un contratto"""
        if not contract_id:
            return False, "ID del contratto non valido"
        

        self.contract_view = contract_view
        success = self.contract_model.delete_contract(contract_id)
        if self.contract_view:
            self.contract_view.refresh_contracts()
        if success:
            return True, "Contratto eliminato con successo"
        else:
            return False, "Errore durante l'eliminazione del contratto"
    
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
        #self.reimpostaAuto(auto_id)  # Reimposta l'auto associata al contratto
        
        if contract_view:
            self.contract_view.refresh_contracts()
        if success:
            return True, "Contratto e fatture collegate eliminate con successo"
        else:
            return False, "Errore durante l'eliminazione del contratto e delle fatture collegate"
    
    def rimuoviAuto(self, autoId):
        self.main_controller.rimuoviAuto(autoId)

    def reimpostaAuto(self, autoId):
        """Reimposta l'auto per essere visibile nel catalogo"""
        success = self.main_controller.reimpostaAuto(autoId)
        if success:
            return True, "Auto reimpostata con successo"
        else:
            return False, "Errore durante la reimpostazione dell'auto"

class CreaRentContract(QDialog):
    def __init__(self, parent=None, controller=None, contract_view=None):
        super().__init__(parent)
        self.controller = controller
        self.contract_view = contract_view
        self.setWindowTitle('Crea un nuovo contratto')
        self.setFixedSize(850,650)
        layout = QVBoxLayout(self)

        user_input = QLineEdit()
        user_input.setPlaceholderText('user')
        layout.addWidget(QLabel('user:'))
        layout.addWidget(user_input)

        auto_input = QLineEdit()
        auto_input.setPlaceholderText('auto')
        layout.addWidget(QLabel('auto:'))
        layout.addWidget(auto_input)

        start_date_input = QLineEdit()
        start_date_input.setPlaceholderText('start_date')
        layout.addWidget(QLabel('start date:'))
        layout.addWidget(start_date_input)

        end_date_input = QLineEdit()
        end_date_input.setPlaceholderText('end_date')
        layout.addWidget(QLabel('end date:'))
        layout.addWidget(end_date_input)

        cauzione_input = QLineEdit()
        cauzione_input.setPlaceholderText('cauzione')
        layout.addWidget(QLabel('cauzione:'))
        layout.addWidget(cauzione_input)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('prezzo:'))
        layout.addWidget(prezzo_input)

        durataGaranzia_input = QLineEdit()
        durataGaranzia_input.setPlaceholderText('durata garanzia')
        layout.addWidget(QLabel('durata garanzia:'))
        layout.addWidget(durataGaranzia_input)

        tipoGaranzia_input = QLineEdit()
        tipoGaranzia_input.setPlaceholderText('tipo garanzia')
        layout.addWidget(QLabel('tipo garanzia:'))
        layout.addWidget(tipoGaranzia_input)

        kmMax_input = QLineEdit()
        kmMax_input.setPlaceholderText('chilometri massimi')
        layout.addWidget(QLabel('chilometri massimi:'))
        layout.addWidget(kmMax_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva contratto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_contract(user_input,auto_input,start_date_input,end_date_input,cauzione_input,prezzo_input, durataGaranzia_input, tipoGaranzia_input, kmMax_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def addi_contract(self,user_input,auto_input,start_date_input,end_date_input,cauzione_input,prezzo_input, durataGaranzia_input, tipoGaranzia_input, kmMax_input):
        user = user_input.text()
        auto = auto_input.text()
        start_date = start_date_input.text()
        end_date = end_date_input.text()
        cauzione = cauzione_input.text()
        prezzo = prezzo_input.text()
        durataGaranzia = durataGaranzia_input.text()
        tipoGaranzia = tipoGaranzia_input.text()
        kmMax = kmMax_input.text()



        if user and auto and start_date and end_date and cauzione and prezzo and durataGaranzia and tipoGaranzia and kmMax:
            self.controller.addo_noleggio_contratto(user, auto, start_date, end_date, cauzione, tipoGaranzia, durataGaranzia, kmMax, prezzo)
           # self.controller.rimuoviAuto(auto)
            
            self.contract_view.refresh_contracts()  # aggiorna la view!
            #if self.controller.dashboard_view:
                #self.controller.dashboard_view.refresh_auto_list()  # aggiorna lista auto nella dashboard
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')

class CreaBuyContract(QDialog):
    def __init__(self, parent=None, controller=None, contract_view=None):
        super().__init__(parent)
        self.controller = controller
        self.contract_view = contract_view
        self.setWindowTitle('Crea un nuovo contratto')
        self.setFixedSize(850,650)
        layout = QVBoxLayout(self)

        user_input = QLineEdit()
        user_input.setPlaceholderText('user')
        layout.addWidget(QLabel('user:'))
        layout.addWidget(user_input)

        auto_input = QLineEdit()
        auto_input.setPlaceholderText('auto')
        layout.addWidget(QLabel('auto:'))
        layout.addWidget(auto_input)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('prezzo:'))
        layout.addWidget(prezzo_input)

        durataGaranzia_input = QLineEdit()
        durataGaranzia_input.setPlaceholderText('durata garanzia')
        layout.addWidget(QLabel('durata garanzia:'))
        layout.addWidget(durataGaranzia_input)

        tipoGaranzia_input = QLineEdit()
        tipoGaranzia_input.setPlaceholderText('tipo garanzia')
        layout.addWidget(QLabel('tipo garanzia:'))
        layout.addWidget(tipoGaranzia_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva contratto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_contract(user_input,auto_input,prezzo_input, durataGaranzia_input, tipoGaranzia_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def addi_contract(self,user_input,auto_input,prezzo_input, durataGaranzia_input, tipoGaranzia_input):
        user = user_input.text()
        auto = auto_input.text()
        prezzo = prezzo_input.text()
        durataGaranzia = durataGaranzia_input.text()
        tipoGaranzia = tipoGaranzia_input.text()


        if user and auto and prezzo and durataGaranzia and tipoGaranzia:
            self.controller.addo_acquisto_contratto(user, auto, tipoGaranzia, durataGaranzia, prezzo)
           # self.controller.rimuoviAuto(auto)
         
            self.contract_view.refresh_contracts()  # aggiorna la view!
            #if self.controller.dashboard_view:
                #self.controller.dashboard_view.refresh_auto_list()  # aggiorna lista auto nella dashboard
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')

    