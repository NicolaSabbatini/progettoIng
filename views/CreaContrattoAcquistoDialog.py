from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

from models.Auto import Auto

class CreaContrattoAcquistoDialog(QDialog):
    def __init__(self, parent=None, controller=None, contract_view=None):
        super().__init__(parent)
        self.controller = controller
        self.contract_view = contract_view
        self.setWindowTitle('Crea un nuovo contratto')
        self.setFixedSize(750,600)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: Arial;
                font-size: 18px;
            }
            QLabel {
                background-color: #2b2b2b;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 30px;
            }
            QLineEdit:focus {
                border: 1px solid #2e86de;
                background-color: black;
            }
            QDateEdit {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 30px;
                color: white;
            }
            QDateEdit:focus {
                border: 1px solid #2e86de;
                background-color: black;
            }
            QDateEdit::drop-down {
                border: none;
                background-color: #2e86de;
                border-radius: 3px;
                width: 20px;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 30px;
                color: white;
            }
            QComboBox:focus {
                border: 1px solid #2e86de;
                background-color: black;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #2e86de;
                border-radius: 3px;
                width: 20px;
            }
            QComboBox::down-arrow {
                border: none;
                background-color: transparent;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #2e86de;
                border: 1px solid #bbb;
            }
            QPushButton#primary_button {
                background-color: #2e86de;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton#primary_button:hover {
                background-color: #1b4f72;
            }
            QMessageBox {
                background-color: #2b2b2b;
                color: white;
                font-size: 18px;
                border-radius: 8px;
            }
            QMessageBox QLabel {
                color: white;
                background-color: #2b2b2b;
                font-size: 18px;
            }
            QMessageBox QPushButton {
                background-color: #2e86de;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QMessageBox QPushButton:hover {
                background-color: #1b4f72;
            }
            """)

        layout = QVBoxLayout(self)
        

        users_list = self.controller.user_controller.getClienti()
        if not users_list:
            users_list = []

        users_combo = QComboBox()
        users_combo.setObjectName('users_combo')
        for user in users_list:
            display_text = f"{user['name']} {user['surname']} - {user['username']}"
            users_combo.addItem(display_text)
        
        layout.addWidget(QLabel('Utente:'))
        layout.addWidget(users_combo)

        auto_list = self.controller.auto_controller.getAutoVisibili()
        if not auto_list:        
            auto_list = []

        auto_combo = QComboBox()
        auto_combo.setObjectName('auto_combo')
        for auto in auto_list:
            display_text = f"{auto['marca']} {auto['modello']} ({auto['anno']}) - {auto['targa']} (Prezzo: {auto['prezzo']}€)"
            auto_combo.addItem(display_text, auto['id'])
        layout.addWidget(QLabel('Seleziona auto:'))
        layout.addWidget(auto_combo)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('Prezzo:'))
        layout.addWidget(prezzo_input)

        durataGaranzia_input = QLineEdit()
        durataGaranzia_input.setPlaceholderText('durataGaranzia')
        layout.addWidget(QLabel('Durata Garanzia:'))
        layout.addWidget(durataGaranzia_input)

        tipoGaranzia_input = QComboBox()
        tipoGaranzia_input.addItems(["Base", "Plus", "Premium"])
        layout.addWidget(QLabel("Tipo garanzia:"))
        layout.addWidget(tipoGaranzia_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva contratto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.aggiungiContratto(users_combo,auto_combo,prezzo_input, durataGaranzia_input, tipoGaranzia_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def aggiungiContratto(self,users_combo,auto_combo,prezzo_input, durataGaranzia_input, tipoGaranzia_input):
        user = users_combo.currentText().split(' - ')[-1].strip(')')
        auto = auto_combo.currentData()
        prezzo = prezzo_input.text()
        durataGaranzia = durataGaranzia_input.text()
        tipoGaranzia = tipoGaranzia_input.currentText()


        if user and auto and prezzo and durataGaranzia and tipoGaranzia:
            self.controller.aggiungiContrattoAcquisto(user, auto, tipoGaranzia, durataGaranzia, prezzo)
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')
