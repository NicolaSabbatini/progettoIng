from models.auto import Auto
from PyQt5.QtCore import QObject

class AutoController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.auto_model = Auto()

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
            auto = Auto(id,marca, modello, anno)
            self.auto_model.add_auto(auto)
            self.view.output_label.setText(f"Auto creata: {auto.scheda()}")
        else:
            self.view.output_label.setText("Inserisci tutti i campi.")

    def get_all_auto(self):
        return self.auto_model.get_all_auto()