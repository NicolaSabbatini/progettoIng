from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,)


class ModificaAutoDialog(QDialog):
    def __init__(self, controller, auto_data, parent=None, auto_view=None):
        
        super().__init__(parent)
        self.controller = controller
        self.auto_view = auto_view
        self.auto_id = auto_data["id"]

        self.setWindowTitle('Modifica Auto')
        self.setFixedSize(750, 650)
        layout = QVBoxLayout(self)

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

        # Campi precompilati
        self.marca_input = QLineEdit(auto_data["marca"])
        layout.addWidget(QLabel('Marca:'))
        layout.addWidget(self.marca_input)

        self.modello_input = QLineEdit(auto_data["modello"])
        layout.addWidget(QLabel('Modello:'))
        layout.addWidget(self.modello_input)

        self.anno_input = QLineEdit(str(auto_data["anno"]))
        layout.addWidget(QLabel('Anno:'))
        layout.addWidget(self.anno_input)

        self.chilometri_input = QLineEdit(str(auto_data["chilometri"]))
        layout.addWidget(QLabel('Chilometri:'))
        layout.addWidget(self.chilometri_input)

        self.prezzo_input = QLineEdit(str(auto_data["prezzo"]))
        layout.addWidget(QLabel('Prezzo:'))
        layout.addWidget(self.prezzo_input)

        self.targa_input = QLineEdit(auto_data["targa"])
        layout.addWidget(QLabel('Targa:'))
        layout.addWidget(self.targa_input)

        # Bottone per salvare le modifiche
        save_btn = QPushButton('Salva Modifiche')
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(self.salvaModifiche)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def salvaModifiche(self):
        """Aggiorna i dati dell’auto con i nuovi valori"""
        marca = self.marca_input.text()
        modello = self.modello_input.text()
        anno = self.anno_input.text()
        chilometri = self.chilometri_input.text()
        prezzo = self.prezzo_input.text()
        targa = self.targa_input.text()

        if marca and modello and anno and chilometri and prezzo and targa:
            success, message = self.controller.aggiornaAuto(
                self.auto_id,
                marca,
                modello,
                int(anno),
                int(chilometri),
                float(prezzo),
                targa
            )
            if success:
                if self.auto_view:
                    self.auto_view.refreshAuto()
                QMessageBox.information(self, "Successo", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Errore", message)
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')
