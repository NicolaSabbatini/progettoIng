from models.user_model import UserModel
from datetime import datetime



from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QDialog
from PyQt5.QtCore import Qt




from models.fatture_model import FattureModel


class FattureController:
    def __init__(self, main_controller, contract, fatture_view=None):
        self.main_controller = main_controller  # Reference to AuthController or main app controller
        self.fatture_view = fatture_view
        self.fatture_model = FattureModel()
        self.contract = contract
    
    def get_all_fatture(self):
        """Restituisce tutti i contratti"""
        return self.fatture_model.get_all_fatture()

    def get_fatture_by_contratto(self, contract_id):
        """Restituisce le fatture associate a un contratto specifico"""
        return self.fatture_model.get_fatture_by_contract(contract_id)
    
    def create_fattura_button(self, contract_id):
        dialog = CreaFattura(parent=None, controller=self, fatture_view=self.fatture_view, contract_id=contract_id)
        dialog.exec_()

    def addo_fattura(self, user, start_date, price, contract_id):
        """Aggiunge un nuovo contratto"""
        if not (user and start_date and price):
            return False, "Tutti i campi del contratto sono obbligatori"
        
        self.fatture_model.add_fattura(user, start_date, price, contract_id)
        return True, "fattura aggiunto con successo"


class CreaFattura(QDialog):
    def __init__(self, parent=None, controller=None, fatture_view=None, contract_id=None):
        super().__init__(parent)
        self.controller = controller
        self.fatture_view = fatture_view
        self.contract_id = contract_id


        self.setWindowTitle('Crea un nuova fattura')
        self.setFixedSize(350,250)
        layout = QVBoxLayout(self)

        user_input = QLineEdit()
        user_input.setPlaceholderText('user')
        layout.addWidget(QLabel('user:'))
        layout.addWidget(user_input)

        start_date_input = QLineEdit()
        start_date_input.setPlaceholderText('start_date')
        layout.addWidget(QLabel('start date:'))
        layout.addWidget(start_date_input)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('prezzo:'))
        layout.addWidget(prezzo_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva fattura')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_fattura(user_input,start_date_input,prezzo_input, self.contract_id))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def addi_fattura(self, user_input, start_date_input, prezzo_input, contract_id):
        user = user_input.text()
        start_date = start_date_input.text()
        prezzo = prezzo_input.text()


        if user and start_date and prezzo:
            self.controller.addo_fattura(user,start_date,prezzo, contract_id)
            if self.fatture_view:
                self.fatture_view.refresh_contracts()  # aggiorna la view!
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')