from models.user_model import UserModel
from datetime import datetime



from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QDialog
from PyQt5.QtCore import Qt


from models.auto_model import AutoModel
from models.contract_model import ContractModel

class ContractController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Reference to AuthController or main app controller
        self.auto_model = AutoModel()
        self.contract_model = ContractModel()

    def crea_contratto(self):
        dialog = CreaContract(self, self.controller)
        dialog.exec_()

    
class CreaContract(QDialog):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle('Crea un nuovo contratto')
        self.setFixedSize(350,250)
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

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('prezzo:'))
        layout.addWidget(prezzo_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva contratto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_contract(user_input,auto_input,start_date_input,end_date_input,prezzo_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def addi_contract(self, user_input, auto_input, start_date_input, end_date_input, prezzo_input):
        user = user_input.text()
        auto = auto_input.text()
        start_date = start_date_input.text()
        end_date = end_date_input.text()
        prezzo = prezzo_input.text()


        if user and auto and start_date and end_date and prezzo:
            self.controller.addo_contratto(user,auto,start_date,end_date,prezzo)
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')
