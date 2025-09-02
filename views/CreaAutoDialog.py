from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)

class CreaAutoDialog(QDialog):
    def __init__(self, controller, parent=None, auto_view=None):
        super().__init__(parent)
        self.controller = controller
        self.auto_view = auto_view
        self.setWindowTitle('Crea una Nuova Auto')
        self.setFixedSize(650, 450)
        layout = QVBoxLayout(self)

        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText('Marca')
        layout.addWidget(QLabel('Marca:'))
        layout.addWidget(self.marca_input)

        self.modello_input = QLineEdit()
        self.modello_input.setPlaceholderText('Modello')
        layout.addWidget(QLabel('Modello:'))
        layout.addWidget(self.modello_input)

        self.anno_input = QLineEdit()
        self.anno_input.setPlaceholderText('Anno')
        layout.addWidget(QLabel('Anno:'))
        layout.addWidget(self.anno_input)

        self.chilometri_input = QLineEdit()
        self.chilometri_input.setPlaceholderText('Chilometri')
        layout.addWidget(QLabel('Chilometri:'))
        layout.addWidget(self.chilometri_input)

        self.prezzo_input = QLineEdit()
        self.prezzo_input.setPlaceholderText('Prezzo')
        layout.addWidget(QLabel('Prezzo:'))
        layout.addWidget(self.prezzo_input)

        self.targa_input = QLineEdit()
        self.targa_input.setPlaceholderText('Targa')
        layout.addWidget(QLabel('Targa:'))
        layout.addWidget(self.targa_input)

        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva Auto')
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(self.addi_auto)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def addi_auto(self):
        marca = self.marca_input.text()
        modello = self.modello_input.text()
        anno = self.anno_input.text()
        chilometri = self.chilometri_input.text()
        prezzo = self.prezzo_input.text()
        targa = self.targa_input.text()

        if marca and modello and anno and chilometri and prezzo and targa:
            self.controller.addo_auto(marca, modello, anno, chilometri, prezzo, targa)
            if self.auto_view:
                self.auto_view.refresh_auto()
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')


