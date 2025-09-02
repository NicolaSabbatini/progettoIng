from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog
from PyQt5.QtCore import Qt

class CreaFattura(QDialog):
    def __init__(self, parent=None, controller=None, fatture_view=None, contract_id=None):
        super().__init__(parent)
        self.controller = controller
        self.fatture_view = fatture_view
        self.contract_id = contract_id


        self.setWindowTitle('Crea un nuova fattura')
        self.setFixedSize(350,250)
        layout = QVBoxLayout(self)

        start_date_input = QLineEdit()
        start_date_input.setPlaceholderText('start_date')
        layout.addWidget(QLabel('data emissione:'))
        layout.addWidget(start_date_input)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('prezzo')
        layout.addWidget(QLabel('prezzo fattura:'))
        layout.addWidget(prezzo_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva fattura')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_fattura(start_date_input,prezzo_input, self.contract_id))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def addi_fattura(self, start_date_input, prezzo_input, contract_id):
        start_date = start_date_input.text()
        prezzo = prezzo_input.text()


        if start_date and prezzo:
            self.controller.addo_fattura(start_date,prezzo, contract_id)
            if self.fatture_view:
                self.fatture_view.refresh_fatture()  # aggiorna la view!
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')  