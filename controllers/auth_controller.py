from controllers.dashboard_controller import DashboardController
from models.user_model import UserModel
from datetime import datetime
from views.register_view import RegisterView
from views.dashboard_view import DashboardView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame

from models.user_model import UserModel
from models.auto_model import AutoModel
from models.contract_model import ContractModel

class AuthController:
    def __init__(self, login_view=None, register_view=None):
        self.user_model = UserModel()
        self.auto_model = AutoModel()
        self.contract_model = ContractModel()
        self.login_view = login_view
        self.register_view = register_view

        self.current_user = None
        self.login_time = None
    
    def login(self, username, password):
        """Gestisce il login dell'utente"""
        # Validazione input
        if not username.strip() or not password:
            return False, "Username e password sono obbligatori"
        
        # Autentica utente
        success, message = self.user_model.authenticate_user(username.strip(), password)
        
        if success:
            self.current_user = username.strip()
            self.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return success, message
    
    def register(self, username, email, password, confirm_password, name, surname, luogo, telefono, data):
        """Gestisce la registrazione di un nuovo utente"""
        # Validazioni
        if not all([username.strip(), email.strip(), password, confirm_password]):
            return False, "Tutti i campi sono obbligatori"
        
        if password != confirm_password:
            return False, "Le password non coincidono"
        
        if len(password) < 6:
            return False, "La password deve essere di almeno 6 caratteri"
        
        # Validazione email semplice
        if '@' not in email or '.' not in email:
            return False, "Formato email non valido"
        
        # Crea utente
        return self.user_model.create_user(username.strip(), email.strip(), password, name, surname, luogo, telefono, data)
    
    def logout(self):
        """Gestisce il logout dell'utente"""
        self.current_user = None
        self.login_time = None
    
    def get_current_user_data(self):
        """Ottiene i dati dell'utente corrente"""
        if not self.current_user:
            return None
        
        user_data = self.user_model.get_user(self.current_user)
        if user_data:
            user_data['username'] = self.current_user
            user_data['login_time'] = self.login_time
        return user_data
    
    def is_logged_in(self):
        """Verifica se un utente è loggato"""
        return self.current_user is not None


    
    
    def handle_login(self,usern, passw, parent):
        """Gestisce il click del bottone login"""
        #username = self.username_input.text().strip()
        #password = self.password_input.text()

        username = usern.strip()
        password = passw
        
        # Debug: stampa per verificare i valori
        print(f"Tentativo login - Username: '{username}', Password length: {len(password)}")
        
        if not username or not password:
            QMessageBox.warning(parent, 'Errore', 'Inserisci username e password')
            return False
        
        success, message = self.login(username, password)
        
        print(f"Risultato login - Success: {success}, Message: {message}")
        
        if success:
            QMessageBox.information(parent, 'Successo', 'Login effettuato con successo!')
            #self.show_dashboard()
            return True
        else:
            QMessageBox.warning(parent, 'Errore di Login', message)
            return False

    def show_register(self):
        """Mostra la finestra di registrazione"""
        if not self.register_view:
            self.register_view = RegisterView(self, self.login_view)
        self.register_view.show()
        self.login_view.hide()

    def show_dashboard(self):
        controller = DashboardController(self)
        self.dashboard_view = DashboardView(controller)
        #self.dashboard_view.update_user_info()
       
        #self.dashboard_view.show()
        
    
    def clear_fields(self):
        """Pulisce i campi di input"""
        self.login_view.username_input.clear()
        self.login_view.password_input.clear()