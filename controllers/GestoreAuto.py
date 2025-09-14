from models.Auto import Auto
from views.CreaAutoDialog import CreaAutoDialog
from views.ModificaAutoDialog import ModificaAutoDialog

class GestoreAuto:
    def __init__(self, user_controller, dashboard_view=None):
        super().__init__()
        self.user_controller = user_controller
        self.dashboard_view = dashboard_view
        self.auto_model = Auto()

    def aggiornaAuto(self, autoId, marca, modello, anno, chilometri, prezzo, targa):
        """Effettua l'aggiornamento vero e proprio nel model"""
        if not autoId:
            return False, "ID dell'auto non valido"

        success, msg = self.auto_model.updateCar(autoId, marca, modello, anno, chilometri, prezzo, targa)
        return success, msg

    def aggiungiAuto(self, marca, modello, anno, chilometri, prezzo, targa):
        """Aggiunge una nuova auto"""
        if not (marca and modello and anno and chilometri and prezzo and targa):
            return False, "Tutti i campi dell'auto sono obbligatori"

        self.auto_model.addCar(marca, modello, anno, chilometri, prezzo, targa)
        return True, "Auto aggiunta con successo"
    
    def caricaAuto(self):
        """Carica le auto dal modello"""
        self.auto_model.loadCars()


    def creaAutoDialog(self):
        dialog = CreaAutoDialog(self, auto_view=self.auto_view)
        dialog.exec_()

    def eliminaAuto(self, autoId, view=None):
        """Elimina un'auto"""
        if not autoId:
            return False, "ID dell'auto non valido"

        self.auto_model.deleteCar(autoId)
        if view:
            self.auto_view.refreshAuto()
        return
        
    def getAllAuto(self):
        """Restituisce tutte le auto, visibili e non"""
        return self.auto_model.getCarList()
    
    def getAutoVisibili(self):
        """Restituisce tutte le auto"""
        return self.auto_model.getAvailableCar()
    
    def modificaAutoDialog(self, autoId, marca, modello, anno, chilometri, prezzo, targa, auto_view=None):
        """Apre il dialog di modifica per un'auto"""
        auto_data = {
            "id": autoId,
            "marca": marca,
            "modello": modello,
            "anno": anno,
            "chilometri": chilometri,
            "prezzo": prezzo,
            "targa": targa
        }
        dialog = ModificaAutoDialog(self, auto_data, auto_view=auto_view)
        dialog.exec_()

    def reimpostaAuto(self, autoId):
        """Reimposta l'auto per essere visibile nel catalogo"""
        success = self.auto_model.resetCar(autoId)
        if success:
            return True, "Auto reimpostata con successo"
        else:
            return False, "Errore durante la reimpostazione dell'auto"
            
    def rimuoviAuto(self, autoId):
        success = self.auto_model.removeCar(autoId)
        if success:
            return True, "Auto rimossa dal catalogo"
        else:
            return False, "Errore durante l'eliminazione dell'auto"
        

        
    


    


