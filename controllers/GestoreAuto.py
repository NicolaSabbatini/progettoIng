from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QFrame, QGridLayout
)
from models.auto_model import AutoModel


class GestoreAuto:
    def __init__(self, user_controller, dashboard_view=None):
        super().__init__()
        self.user_controller = user_controller
        self.dashboard_view = dashboard_view
        self.auto_model = AutoModel()

    def center_window(self, view):
        """Centra la finestra sullo schermo"""
        screen = view.screen().availableGeometry()
        size = view.geometry()
        view.move(
            max(0, (screen.width() - view.width()) // 2),
            max(0, (screen.height() - view.height()) // 2)
        )

    def load_auto(self):
        """Carica le auto dal modello"""
        self.auto_model.load_auto()

    def update_auto_display(self, view):
        """Aggiorna la visualizzazione delle auto nella dashboard"""
        auto_list = self.auto_model.get_all_auto()
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
    
    def get_every_auto(self):
        """Restituisce tutte le auto, visibili e non"""
        return self.auto_model.get_every_auto()

    def crea_auto_dialog(self, dashboard_view=None):
        dialog = CreaAutoDialog(self, auto_view=self.auto_view)
        dialog.exec_()

    def addo_auto(self, marca, modello, anno, chilometri, prezzo, targa):
        """Aggiunge una nuova auto"""
        if not (marca and modello and anno and chilometri and prezzo and targa):
            return False, "Tutti i campi dell'auto sono obbligatori"

        self.auto_model.add_auto(marca, modello, anno, chilometri, prezzo, targa)
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

    def rimuoviAuto(self, autoId):
        success = self.auto_model.rimuoviAuto(autoId)
        if success:
            return True, "Auto rimossa dal catalogo"
        else:
            return False, "Errore durante l'eliminazione dell'auto"
        

    def reimpostaAuto(self, autoId):
        """Reimposta l'auto per essere visibile nel catalogo"""
        success = self.auto_model.reimpostaAuto(autoId)
        if success:
            return True, "Auto reimpostata con successo"
        else:
            return False, "Errore durante la reimpostazione dell'auto"
        
    

    def modificaAuto(self, auto_id, marca, modello, anno, chilometri, prezzo, targa, auto_view=None):
        """Apre il dialog di modifica per un'auto"""
        auto_data = {
            "id": auto_id,
            "marca": marca,
            "modello": modello,
            "anno": anno,
            "chilometri": chilometri,
            "prezzo": prezzo,
            "targa": targa
        }
        dialog = ModificaAutoDialog(self, auto_data, auto_view=auto_view)
        dialog.exec_()

    def salvaModificaAuto(self, auto_id, marca, modello, anno, chilometri, prezzo, targa):
        """Effettua l’aggiornamento vero e proprio nel model"""
        if not auto_id:
            return False, "ID dell'auto non valido"

        success = self.auto_model.update_auto(auto_id, marca, modello, anno, chilometri, prezzo, targa)
        if success:
            return True, "Auto modificata con successo"
        else:
            return False, "Errore durante la modifica dell'auto"



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


class ModificaAutoDialog(QDialog):
    def __init__(self, controller, auto_data, parent=None, auto_view=None):
        """
        Finestra di dialogo per modificare un'auto esistente.
        """
        super().__init__(parent)
        self.controller = controller
        self.auto_view = auto_view
        self.auto_id = auto_data["id"]

        self.setWindowTitle('Modifica Auto')
        self.setFixedSize(650, 450)
        layout = QVBoxLayout(self)

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
        save_btn.clicked.connect(self.salva_modifiche)

        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

    def salva_modifiche(self):
        """Aggiorna i dati dell’auto con i nuovi valori"""
        marca = self.marca_input.text()
        modello = self.modello_input.text()
        anno = self.anno_input.text()
        chilometri = self.chilometri_input.text()
        prezzo = self.prezzo_input.text()
        targa = self.targa_input.text()

        if marca and modello and anno and chilometri and prezzo and targa:
            success, message = self.controller.salvaModificaAuto(
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
                    self.auto_view.refresh_auto()
                QMessageBox.information(self, "Successo", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Errore", message)
        else:
            QMessageBox.warning(self, 'Errore', 'Inserisci tutti i campi.')
