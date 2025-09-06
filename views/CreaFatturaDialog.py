from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QDateEdit, QMessageBox
from PyQt5.QtCore import Qt, QDate

class CreaFatturaDialog(QDialog):
    def __init__(self, parent=None, controller=None, fatture_view=None, contract_id=None):
        super().__init__(parent)
        self.controller = controller
        self.fatture_view = fatture_view
        self.contract_id = contract_id

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: Arial;
                font-size: 16px;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: black;
                min-height: 28px;
            }
            QLineEdit:focus {
                border: 1px solid #2e86de;
                background-color: black;
            }
            QLabel {
                font-size: 16px;
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
            QPushButton#primary_button {
                background-color: #2e86de;
                color: white;
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton#primary_button:hover {
                background-color: #1b4f72;
            }
            QMessageBox {
                background-color: #2b2b2b;
                color: white;
                font-size: 16px;
                border-radius: 8px;
            }
            QMessageBox QLabel {
                color: white;
                background-color: #2b2b2b;
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


        self.setWindowTitle('Crea un nuova fattura')
        self.setFixedSize(350,250)
        layout = QVBoxLayout(self)

        start_date_input = QDateEdit()
        start_date_input.setCalendarPopup(True)
        start_date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel('Data emissione:'))
        layout.addWidget(start_date_input)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('Prezzo fattura:'))
        layout.addWidget(prezzo_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva fattura')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.aggiungiFattura(start_date_input,prezzo_input, self.contract_id))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def aggiungiFattura(self, start_date_input, prezzo_input, contract_id):
        start_date = start_date_input.text()
        prezzo = prezzo_input.text()

        if start_date and prezzo:
            self.controller.aggiungiFattura(start_date,prezzo, contract_id)
            if self.fatture_view:
                self.fatture_view.refreshFatture()  # aggiorna la view!
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')  