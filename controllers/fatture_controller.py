from models.user_model import UserModel
from datetime import datetime



from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QDialog
from PyQt5.QtCore import Qt




from models.fatture_model import FattureModel


class FattureController:
    def __init__(self, main_controller, contract):
        self.main_controller = main_controller  # Reference to AuthController or main app controller
        self.fatture_model = FattureModel()
        self.contract = contract
    
    def get_all_fatture(self):
        """Restituisce tutti i contratti"""
        return self.fatture_model.get_all_fatture()

    def get_fatture_by_contratto(self, contract_id):
        """Restituisce le fatture associate a un contratto specifico"""
        return self.fatture_model.get_fatture_by_contract(contract_id)


