from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QGridLayout
from models.auto_model import AutoModel
from PyQt5.QtCore import Qt

class AutoController(QObject):
    def __init__(self, main_controller=None, auto_view=None, dashboard_view=None):
        super().__init__()
        self.main_controller = main_controller 
        self.dashboard_view = dashboard_view
        self.auto_view = auto_view
        self.auto_model = AutoModel()

    def center_window(self, view):
        """Centra la finestra sullo schermo"""
        screen = view.screen().availableGeometry()
        size = view.geometry()
        view.move(
            max(0, (screen.width() - view.width()) // 2),
            max(0, (screen.height() - view.height()) // 2)
        )

        
    def update_auto_display(self, view):
        """Aggiorna la visualizzazione delle auto nella dashboard"""
        auto_list = self.main_controller.get_all_auto()
        if not hasattr(view, 'auto_layout'):
            view.auto_layout = QGridLayout()
            view.auto_layout.setSpacing(10)
            view.auto_layout.setContentsMargins(0, 0, 0, 0)
            view.auto_frame = QFrame()
            view.auto_frame.setObjectName('info_frame')
            view.auto_frame.setLayout(view.auto_layout)
            view.layout().addWidget(view.auto_frame)
        # Pulisce il layout esistente
        for i in reversed(range(view.auto_layout.count())): 
            widget = view.auto_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        # Crea e aggiunge i widget per le auto
        if auto_list:
            view.create_auto_widgets(auto_list)
    
    def get_all_auto(self):
        """Restituisce tutte le auto"""
        return self.auto_model.get_all_auto()
    
    def crea_auto_dialog(self, dashboard_view=None):
        dialog = CreaAutoDialog(self, auto_view=self.auto_view)
        dialog.exec_()

    def addo_auto(self, marca, modello, anno, chilometri, prezzo, targa):
        """Aggiunge una nuova auto"""
        if not (marca and modello and anno and chilometri and prezzo and targa):
            return False, "Tutti i campi dell'auto sono obbligatori"
        
        self.auto_model.add_auto(marca,modello, anno, chilometri, prezzo, targa)
        return True, "Auto aggiunta con successo"
    

    def elimina_auto(self, auto_id, auto_view=None):
        """Elimina un'auto"""
        if not auto_id:
            return False, "ID dell'auto non valido"
        
        success = self.auto_model.delete_auto(auto_id)
        if self.auto_view:
            self.auto_view.refresh_auto()
        if success:
            return True, "Auto eliminata con successo"
        else:
            return False, "Errore durante l'eliminazione dell'auto"
    
class CreaAutoDialog(QDialog):
    def __init__(self, controller, parent=None, auto_view=None):
        super().__init__(parent)
        self.controller = controller
        self.auto_view = auto_view
        self.setWindowTitle('Crea una Nuova Auto')
        self.setFixedSize(650, 450)
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

        chilometri_input = QLineEdit()
        chilometri_input.setPlaceholderText('Chilometri')
        layout.addWidget(QLabel('Chilometri:'))
        layout.addWidget(chilometri_input)

        prezzo_input = QLineEdit()
        prezzo_input.setPlaceholderText('Prezzo')
        layout.addWidget(QLabel('Prezzo:'))
        layout.addWidget(prezzo_input)

        targa_input = QLineEdit()
        targa_input.setPlaceholderText('Targa')
        layout.addWidget(QLabel('Targa:'))
        layout.addWidget(targa_input)


        
      
        # Bottone per salvare l'auto
        save_btn = QPushButton('Salva Auto')  
        save_btn.setObjectName('primary_button')
        layout.addWidget(save_btn)
        save_btn.clicked.connect(lambda: self.addi_auto(marca_input, modello_input, anno_input, chilometri_input, prezzo_input, targa_input))
        
      
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)





    def addi_auto(self, marca_input, modello_input, anno_input, chilometri_input, prezzo_input, targa_input):
        marca = marca_input.text()
        modello = modello_input.text()
        anno = anno_input.text()
        chilometri = chilometri_input.text()
        prezzo = prezzo_input.text()
        targa = targa_input.text()

        if marca and modello and anno and chilometri and prezzo and targa:
            self.controller.addo_auto(marca, modello, anno, chilometri, prezzo, targa)
            if self.auto_view:
                self.auto_view.refresh_auto()  # aggiorna la view!
            self.accept()
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')
