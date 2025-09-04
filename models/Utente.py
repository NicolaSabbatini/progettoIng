# models/user_model.py - Model per la gestione degli utenti
import hashlib
import json
import os
from datetime import datetime

class Utente:
    def __init__(self):
        self.users_file = 'data/users.json'
        os.makedirs('data', exist_ok=True)
        self.users = {}
        self.loadUsers()

    def authenticateUser(self, username, password):
        """Autentica un utente"""
        if username not in self.users:
            return False, "Username non trovato"
        
        if self.users[username]['password'] != self.hashPassword(password):
            return False, "Password non corretta"
        
        return True, "Login effettuato con successo"
    
    def createUser(self, username, email, password, name, surname, luogo, telefono, data):
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
            'password': self.hashPassword(password),
            'luogo': luogo,
            'telefono': telefono,
            'data': data,
            'ruolo': 'cliente',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.saveUser()
        return True, "Utente creato con successo"
    
    def getAllClients(self):
        """Restituisce tutti gli utenti"""
        return [user for user in self.users.values() if user.get('ruolo') == 'cliente']
    
    def getRole(self, username):
        user = self.getUser(username)
        if user:
            return user.get('ruolo', 'cliente')  # default 'cliente' se non impostato
        return None
    
    def getUser(self, username):
        """Ottieni informazioni di un utente"""
        return self.users.get(username, None)
    
    def hashPassword(self, password):
        """Hash della password usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def loadUsers(self):
        """Carica gli utenti dal file JSON"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}
            self.saveUser()
    
    def saveUser(self):
        """Salva gli utenti nel file JSON"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)

    
    def updateUser(self, username, password=None, name=None, surname=None, email=None, luogo=None, telefono=None, data=None):
        """Aggiorna i dati di un utente esistente"""
        if username not in self.users:
            return False, "Utente non trovato"
        
        if email and any(user['email'] == email and user != self.users[username] for user in self.users.values()):
            return False, "Email già registrata da un altro utente"
        
        if name:
            self.users[username]['name'] = name
        if surname:
            self.users[username]['surname'] = surname
        if email:
            self.users[username]['email'] = email
        if luogo:
            self.users[username]['luogo'] = luogo
        if password:
            self.users[username]['password'] = self.hashPassword(password)
        if telefono:
            self.users[username]['telefono'] = telefono
        if data:
            self.users[username]['data'] = data
        
        
        self.saveUser()
        return True, "Dati utente aggiornati con successo"
    
    def deleteUser(self, username):
        """Elimina un utente"""
        if username in self.users:
            del self.users[username]
            self.saveUser()
            return True
        return False

    

    



    