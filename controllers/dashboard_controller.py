from models.user_model import UserModel
from datetime import datetime


from views.dashboard_view import DashboardView
from views.fatture_view import FattureView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QDialog

from models.user_model import UserModel
from models.auto_model import AutoModel
from models.contract_model import ContractModel


from controllers.auto_controller import AutoController

class DashboardController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Reference to AuthController or main app controller
        self.user_model = UserModel()
        self.auto_model = AutoModel()
        self.contract_model = ContractModel()
        self.auto_view = None
        self.dashboard_view = None


    def set_dashboard_view(self, view):
        """Collega la DashboardView a questo controller"""
        self.dashboard_view = view

    def center_window(self, view):
        """Centra la finestra sullo schermo"""
        screen = view.screen().availableGeometry()
        size = view.geometry()
        view.move(
            max(0, (screen.width() - view.width()) // 2),
            max(0, (screen.height() - view.height()) // 2)
        )

    def update_user_info(self, view):
        """Aggiorna le informazioni utente nella dashboard"""
        user_data = self.main_controller.get_current_user_data()
        if user_data:
            view.welcome_label.setText(f'Benvenuto, {user_data["username"]}!')
            view.username_label.setText(f'👤 Username: {user_data["username"]}')
            view.email_label.setText(f'📧 Email: {user_data["email"]}')
            view.created_label.setText(f'📅 Account creato: {user_data["created_at"]}')
            view.login_time_label.setText(f'🕐 Ultimo accesso: {user_data["login_time"]}')
            view.name_label.setText(f'Nome: {user_data.get("name", "N/A")}')
            view.surname_label.setText(f'Cognome: {user_data.get("surname", "N/A")}')
            view.luogo_label.setText(f'Luogo: {user_data.get("luogo", "N/A")}')
            view.telefono_label.setText(f'Telefono: {user_data.get("telefono", "N/A")}')
            view.data_label.setText(f'Data di nascita: {user_data.get("data", "N/A")}')

    def handle_logout(self, view):
        """Gestisce il logout"""
        self.main_controller.logout()
        self.main_controller.clear_fields()
        view.login_view.show()
        view.hide()

    
    
    def show_dashboard(self, username):
        """Mostra la dashboard dell'utente"""
        self.current_user = username
        self.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Inizializza la vista della dashboard
        self.dashboard_view = DashboardView(self)
        self.dashboard_view.show()

    
    
    def rimuoviAuto(self, autoId):
        """Rimuove un'auto e aggiorna la view"""
        self.auto_controller.rimuoviAuto(autoId)

        if self.dashboard_view:
            self.dashboard_view.refresh_auto_list()
    
    def reimpostaAuto(self, autoId):
        """Reimposta l'auto per essere visibile nel catalogo"""
        success = self.auto_model.reimpostaAuto(autoId)
        if success:
            return True, "Auto reimpostata con successo"
        else:
            return False, "Errore durante la reimpostazione dell'auto"