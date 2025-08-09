from models.auto import Auto
from PyQt5.QtCore import QObject

class AutoController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.auto = None

        self.view.salva_btn.clicked.connect(self.crea_auto)

    def crea_auto(self):
        marca = self.view.marca_input.text()
        modello = self.view.modello_input.text()
        anno = self.view.anno_input.text()

        if marca and modello and anno:
            self.auto = Auto(marca, modello, anno)
            self.view.output_label.setText(f"Auto creata: {self.auto.scheda()}")
        else:
            self.view.output_label.setText("Inserisci tutti i campi.")