from models.user_model import UserModel
from datetime import datetime

from models.user_model import UserModel
from models.auto import AutoModel
from models.contract_model import ContractModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self.auto_model = AutoModel()
        self.contract_model = ContractModel()
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