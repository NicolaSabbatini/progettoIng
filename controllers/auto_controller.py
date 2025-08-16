from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.auto_model import AutoModel
from views.auto_view import AutoView
from PyQt5.QtCore import Qt

class AutoController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.auto_model = AutoModel()

        self.view.salva_btn.clicked.connect(self.crea_auto)

    def crea_auto(self):
        id = len(self.auto_model.get_all_auto()) + 1
        if id in self.auto_model.auto_list:
            self.view.output_label.setText("Auto già esistente")
            return  
        
        marca = self.view.marca_input.text()
        modello = self.view.modello_input.text()
        anno = self.view.anno_input.text()

        if marca and modello and anno:
            auto = AutoModel(id,marca, modello, anno)
            self.auto_model.add_auto(auto)
            self.view.output_label.setText(f"Auto creata: {auto.scheda()}")
        else:
            self.view.output_label.setText("Inserisci tutti i campi.")

    def get_all_auto(self):
        return self.auto_model.get_all_auto()
    
class CreaAutoDialog(QDialog):
    def __init__(self,controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle('Crea una Nuova Auto')
        self.setFixedSize(350, 250)
        layout = QVBoxLayout(self)

        marca_input = QLineEdit()
        marca_input.setPlaceholderText('Marca')
        layout.addWidget(QLabel('Marca:'))
        layout.addWidget(marca_input)

        modello_input = QLineEdit()
        modello_input.setPlaceholderText('Modello')
        layout.addWidget(QLabel('Modello:'))
        layout.addWidget(modello_input)

        anno_input = QLineEdit()
        anno_input.setPlaceholderText('Anno')
        layout.addWidget(QLabel('Anno:'))
        layout.addWidget(anno_input)
        
      
        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva Auto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_auto(marca_input, modello_input, anno_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)





    def addi_auto(self, marca_input, modello_input, anno_input):
        marca = marca_input.text()
        modello = modello_input.text()
        anno = anno_input.text()

        if marca and modello and anno:
            self.controller.addo_auto(marca, modello, anno)
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')
