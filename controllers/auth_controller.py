from models.user_model import UserModel
from datetime import datetime

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
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