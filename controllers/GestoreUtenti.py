from models.Utente import Utente
from datetime import datetime
from views.RegisterView import RegisterView
from views.DashboardView import DashboardView
from PyQt5.QtWidgets import QMessageBox

from models.Auto import Auto
from models.Contratto import Contratto

from views.ModificaUtenteDialog import ModificaUtenteDialog


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
    
    def modificaUtenteDialog(self, dashboard_view):
        """Apre il dialog per modificare l'utente"""
        if not self.current_user:
            return
        user_data = self.getDatiUtenteLoggato()
        dialog = ModificaUtenteDialog(self, user_data, dashboard_view=dashboard_view)
        if dialog.exec_():  # modale
            self.dashboard_view.refreshUtente()

    def aggiornaUtente(self, username, old_password, new_password, name, surname, email, luogo, telefono, data):
        # Validazioni
        if not all([username.strip(), email.strip(), name, surname, luogo, telefono, data]):
            return False, "Tutti i campi sono obbligatori"
        
        if old_password:
            # Verifica la vecchia password
            result = self.user_model.authenticateUser(username, old_password)
            if isinstance(result, tuple):
                success, msg = result
            else:
                success = result
            if not success:
                return False, "Vecchia password errata"
        
        if new_password:
            if len(new_password) < 6:
                return False, "La password deve essere di almeno 6 caratteri"
        
        # Validazione email semplice
        if '@' not in email or '.' not in email:
            return False, "Formato email non valido"

        try:
            # Aggiorna utente nel model
            success = self.user_model.updateUser(username, new_password, name, surname, email, luogo, telefono, data)
            if success:
                return True, "Utente aggiornato con successo"
            else:
                return False, "Impossibile aggiornare l'utente"
        except Exception as e:
            return False, f"Errore: {str(e)}"
    
    def aggiornaInfoUtente(self, dashboard_view):
        """Aggiorna le informazioni dell'utente visualizzate nella dashboard"""
        user_data = self.getDatiUtenteLoggato()
        if user_data:
            dashboard_view.username_label.setText(f"Username: {user_data.get('username', '')}")
            dashboard_view.email_label.setText(f"Email: {user_data.get('email', '')}")
            dashboard_view.name_label.setText(f"Nome: {user_data.get('name', '')}")
            dashboard_view.surname_label.setText(f"Cognome: {user_data.get('surname', '')}")
            dashboard_view.luogo_label.setText(f"Luogo di nascita: {user_data.get('luogo', '')}")
            dashboard_view.telefono_label.setText(f"Telefono: {user_data.get('telefono', '')}")
            dashboard_view.data_label.setText(f"Data di nascita: {user_data.get('data', '')}")
            dashboard_view.login_time_label.setText(f"Login effettuato il: {user_data.get('login_time', '')}")
            dashboard_view.created_label.setText(f"Utente creato il: {user_data.get('created_at', '')}")

            dashboard_view.welcome_label.setText(f"Benvenuto, {user_data.get('name', '')}!")
    

    def eliminaUtente(self, parent):
        """Elimina il profilo dell'utente corrente dopo conferma"""
        today = datetime.now().date()
        print(f"Utente corrente: {self.current_user}")
        
        
        self.contract_model.loadContracts()
        contracts = self.contract_model.getClientContracts(self.current_user)
        for c in contracts :
            if c.get('tipo') == 'noleggio':
                end_date = datetime.strptime(c["end_date"], '%d/%m/%Y').date()
                if end_date > today:
                    ##########
                    print(f"Contratto di noleggio attivo trovato con end_date {c['end_date']}")
                    return False, "Non puoi procedere all'eliminazione con contratti di noleggio attivi"

        success = self.user_model.deleteUser(self.current_user)
        if success:
            if self.dashboard_view:
                self.dashboard_view.close()
                self.current_user = None
                self.visualizzaLogin()
                self.login_view.clearFields()
                return True, "Profilo eliminato con successo"
        else:
            return False, "Errore durante l'eliminazione del profilo"
        
    
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

        #
        print(f" i tuoi contratti sono: {self.contract_model.getClientContracts(username)}")

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


    def visualizzaLogin(self):
        self.login_view.show()
        self.login_view.clearFields()
        