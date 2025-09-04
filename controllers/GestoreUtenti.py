from models.Utente import Utente
from datetime import datetime
from views.RegisterView import RegisterView
from views.DashboardView import DashboardView
from PyQt5.QtWidgets import QMessageBox

from models.Auto import Auto
from models.Contratto import Contratto


class GestoreUtenti:
    def __init__(self, login_view=None, register_view=None, dashboard_view=None):
        self.user_model = Utente()
        self.auto_model = Auto()
        self.contract_model = Contratto()
        self.login_view = login_view
        self.register_view = register_view
        self.dashboard_view = dashboard_view
        self.current_user = None
        self.login_time = None
    
    def aggiornaInfoUtente(self, view):
        """Aggiorna le informazioni utente nella dashboard"""
        user_data = self.getDatiUtenteLoggato()
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

    def getClienti(self):
        """Restituisce tutti gli utenti"""
        return self.user_model.getAllClients()

    def getDatiUtenteLoggato(self):
        """Ottiene i dati dell'utente corrente"""
        if not self.current_user:
            return None
        user_data = self.user_model.getUser(self.current_user)
        if user_data:
            user_data['username'] = self.current_user
            user_data['login_time'] = self.login_time
        return user_data

    def getRuoloUtente(self):
            """Restituisce il ruolo dell'utente loggato"""
            user_data = self.getDatiUtenteLoggato()
            if user_data:
                return user_data.get("ruolo")
            return None

    def login(self, username, password, parent):
        """Gestisce login e UI insieme"""

        username = username.strip()
        password = password

        # Debug: stampa per verificare i valori
        print(f"Tentativo login - Username: '{username}', Password length: {len(password)}")

        # Validazione input
        if not username or not password:
            QMessageBox.warning(parent, 'Errore', 'Inserisci username e password')
            return False

        # Autenticazione utente
        success, message = self.user_model.authenticateUser(username, password)

        if success:
            self.current_user = username
            self.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            QMessageBox.information(parent, 'Successo', 'Login effettuato con successo!')
            self.visualizzaDashboard(username)
            self.login_view.username_input.clear()
            self.login_view.password_input.clear()
            self.login_view.hide()
            return True
        else:
            QMessageBox.warning(parent, 'Errore di Login', message)
            return False
 
    def logout(self):
        """Gestisce il logout dell'utente"""
        self.current_user = None
        self.login_time = None
        self.login_view.username_input.clear()
        self.login_view.password_input.clear()
        self.login_view.show()
        self.dashboard_view.hide()
    
    def register(self, username, email, password, confirmPassword, nome, cognome, luogo, telefono, data):
        """Gestisce la registrazione di un nuovo utente"""
        # Validazioni
        if not all([username.strip(), email.strip(), password, confirmPassword]):
            return False, "Tutti i campi sono obbligatori"
        
        if password != confirmPassword:
            return False, "Le password non coincidono"
        
        if len(password) < 6:
            return False, "La password deve essere di almeno 6 caratteri"
        
        # Validazione email semplice
        if '@' not in email or '.' not in email:
            return False, "Formato email non valido"
        
        # Crea utente
        return self.user_model.createUser(username.strip(), email.strip(), password, nome, cognome, luogo, telefono, data) 
       
    def visualizzaDashboard(self, username):
        """Mostra la dashboard dell'utente"""
        self.current_user = username
        self.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Inizializza la vista della dashboard
        self.dashboard_view = DashboardView(self)
        self.dashboard_view.show()
    
    def visualizzaRegistrazione(self):
        """Mostra la finestra di registrazione"""
        if not self.register_view:
            self.register_view = RegisterView(self, self.login_view)
        self.register_view.show()
        self.login_view.hide()