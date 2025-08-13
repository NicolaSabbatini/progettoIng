from models.user_model import UserModel
from datetime import datetime


from views.dashboard_view import DashboardView
from views.fatture_view import FattureView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout

from models.user_model import UserModel
from models.auto_model import AutoModel
from models.contract_model import ContractModel

class DashboardController:
    def __init__(self, main_controller):
        self.main_controller = main_controller  # Reference to AuthController or main app controller
        self.user_model = UserModel()
        self.auto_model = AutoModel()
        self.contract_model = ContractModel()





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
        view.login_view.clear_fields()
        view.login_view.show()
        view.hide()

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
    
    def show_dashboard(self, username):
        """Mostra la dashboard dell'utente"""
        self.current_user = username
        self.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Inizializza la vista della dashboard
        self.dashboard_view = DashboardView(self)
        self.dashboard_view.show()

    def get_all_auto(self):
        """Restituisce tutte le auto"""
        return self.auto_model.get_all_auto()
    
    def addo_auto(self, marca, modello, anno):
        """Aggiunge una nuova auto"""
        if not (marca and modello and anno):
            return False, "Tutti i campi dell'auto sono obbligatori"
        
        self.auto_model.add_auto(marca,modello, anno)
        return True, "Auto aggiunta con successo"
    
    def get_all_contracts(self):
        """Restituisce tutti i contratti"""
        return self.contract_model.get_all_contracts()
    
    def addo_contratto(self, user, auto, start_date, end_date, price):
        """Aggiunge un nuovo contratto"""
        if not (user and auto and start_date and end_date and price):
            return False, "Tutti i campi del contratto sono obbligatori"
        
        self.contract_model.add_contract(user, auto, start_date, end_date, price)
        return True, "Contratto aggiunto con successo"
    
    def show_fatture_view(self, parent, contract):
        self.fattture_view = FattureView(self)
        self.fattture_view.show()