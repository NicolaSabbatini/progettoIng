from PyQt5.QtWidgets import (QFrame, QGridLayout)

from models.Auto import Auto
from views.CreaAutoDialog import CreaAutoDialog
from views.ModificaAutoDialog import ModificaAutoDialog

class GestoreAuto:
    def __init__(self, user_controller, dashboard_view=None):
        super().__init__()
        self.user_controller = user_controller
        self.dashboard_view = dashboard_view
        self.auto_model = Auto()

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

        success, msg = self.auto_model.update_auto(auto_id, marca, modello, anno, chilometri, prezzo, targa)
        if success:
            return True, "Auto modificata con successo"
        else:
            return False, msg



