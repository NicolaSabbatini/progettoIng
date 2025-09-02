# models/user_model.py - Model per la gestione degli utenti
import hashlib
import json
import os
from datetime import datetime

class Utente:
    def __init__(self):
        self.users_file = 'data/users.json'
        os.makedirs('data', exist_ok=True)
        self.load_users()
    
    def load_users(self):
        """Carica gli utenti dal file JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}
            self.save_users()
    
    def save_users(self):
        """Salva gli utenti nel file JSON"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)
    
    def hash_password(self, password):
        """Hash della password usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password, name, surname, luogo, telefono, data):
        """Crea un nuovo utente"""
        if username in self.users:
            return False, "Username già esistente"
        
        if any(user['email'] == email for user in self.users.values()):
            return False, "Email già registrata"
        
        self.users[username] = {
            'name': name,
            'surname': surname,
            'email': email,
            'username': username,
            'password': self.hash_password(password),
            'luogo': luogo,
            'telefono': telefono,
            'data': data,
            'ruolo': 'cliente',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.save_users()
        return True, "Utente creato con successo"
    
    def authenticate_user(self, username, password):
        """Autentica un utente"""
        if username not in self.users:
            return False, "Username non trovato"
        
        if self.users[username]['password'] != self.hash_password(password):
            return False, "Password non corretta"
        
        return True, "Login effettuato con successo"
    
    def get_user(self, username):
        """Ottieni informazioni di un utente"""
        return self.users.get(username, None)
    
    def get_role(self, username):
        user = self.get_user(username)
        if user:
            return user.get('ruolo', 'cliente')  # default 'cliente' se non impostato
        return None

    